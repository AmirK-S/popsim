# a38. La version continue et la version par camp du test des items sensibles au mode

## Errata du 9 septembre 2026

Corrections apportees a la suite de la seconde relecture adverse,
`resultats/a45-relecture-adverse-2.md`. **Le corps du rapport n'est pas reecrit** ; chaque
point cite la phrase d'origine, donne la correction et donne la preuve. Recalculs :
`analyses/a47_chute_segmentations.py`, `analyses/a47_verifications.py` et
`analyses/a47_income_v6.py` ; tableaux `resultats/a47-*.csv` ; synthese
`resultats/a47-errata-2.md`. Aucun script existant n'a ete modifie, aucun appel de modele
de langage, lecture seule sur `data/` et sur les caches de a25, a28 et a35.

### E1. Section 4.4 lecture 4 : « seule l'etiquette change » devient un contraste de conditionnement. Objection a45 numero 1, contradiction D1.

**Phrase d'origine.** « **L'etiquette est ce qui produit la caricature.** C2, persona
demographique de onze attributs dont `polviews`, vaut 1,62 [1,06 ; 2,10]. C3, 119 reponses
d'enquete et aucune demographie, vaut 0,52 [0,20 ; 0,82]. [...] Meme modele, Qwen3-4B, meme
temperature, memes 150 personnes, memes items : **seule l'etiquette change.** »

**Correction.** La derniere proposition est fausse. Le rapport decrit lui meme, dans la
phrase precedente, les deux entrees qui different : onze attributs sans les reponses contre
119 reponses sans les attributs. Ecrire « seule l'etiquette change » contredit le contenu de
la meme lecture. La formulation juste est « ce contraste de conditionnement, dont les deux
facteurs sont confondus, deplace le facteur de 1,62 a 0,52 ».

**Ce que les deux invites contiennent, mesure sur le code.**
[CONFIRME, `analyses/a5_agents_locaux_gss.py`, `systeme_c2` lignes 164 a 177 et `systeme_c3`
lignes 180 a 196]

| | contenu de l'invite systeme | etiquette ideologique | reponses de la personne |
|---|---|---|---|
| C2 | les **onze attributs** de `demographic_summary.csv`, et rien d'autre | oui, ligne `Political ideology` | **aucune** |
| C3 | les **environ 119 items de contexte**, question et reponse en clair | **non** | oui, toutes |

C2 et C3 ne different donc pas par la presence ou l'absence de l'etiquette : **ils echangent
integralement leur entree**. Le contraste melange deux changements, le retrait de l'etiquette
et le remplacement de la personne par onze attributs ; ses deux facteurs sont confondus et
aucun des textes du dossier ne les separe.

**Ce que le second facteur vaut a lui seul.** `B1 argmax` est une regression sur les memes
onze attributs, `B2 argmax` un plus proche voisin sur les memes 119 items **sans aucune
demographie** [CONFIRME, `a2_baselines_gss.py` lignes 178 et 188 : `enc.transform` n'alimente
que `B1`, `B2` ne voit que `codes[:, contexte]`]. A moteur statistique constant et sans
aucune ablation d'etiquette, le passage de l'un a l'autre deplace la chute sous permutation
de **0,175 a 0,357 du plancher humain**, un facteur 2,0 ; le passage de C2 a C3 vaut un
facteur 6,2 [MESURE, `a47-chute-deux-segmentations.csv`, segmentation `S_ideo`].

**L'ablation propre n'est pas dans ce dossier.** Elle est le run R3 de la nuit du 8 au
9 septembre : C3 plus etiquette contre C3, et C2 prive de la seule ligne `Political
ideology` contre C2. Tant qu'il n'a pas rendu, aucun texte ne doit ecrire « ablation de
l'etiquette » ni « seule l'etiquette bouge ».

### E2. Section 4 : le facteur d'amplification est une quantite de gabarit, pas une quantite de personne. Objection a45 numero 3, contradiction D2.

**Phrase d'origine.** « Les quatre conditions riches de Stanford et C2 exagerent l'ecart d'un
facteur 1,6 a 3,2, avec des intervalles qui excluent 1 dans les cinq cas. »

**Correction.** Le chiffre est juste et reproduit. Ce qu'il mesure ne l'est pas :
`a28_test1_mode.mesurer` construit le score de desirabilite d'une condition, dans un camp et
sur un item, par `compte(mat, j, it)`, qui **denombre les modalites sur les lignes du camp**.
Le facteur d'amplification est donc une fonctionnelle de la seule table de contingence
(camp, modalite) : **il mesure les marges par camp, pas les personnes**, et il releve mot
pour mot du critere de Yuan que a44 applique au reste du dossier. Il doit etre cite comme
quantite de gabarit, systematiquement a cote d'une quantite de personne, la chute sous
permutation.

**Preuve, invariance exacte sous permutation des personnes a l'interieur de leur camp.**
[MESURE, `a47-a38-invariance-facteur.csv`, produit par `analyses/a47_verifications.py`, qui
reimporte `a28_test1_mode.mesurer` et `a38_mesures.desirabilite_humaine` sans une ligne de
changement]

| condition | perimetre | facteur, vraie assignation | facteur, apres permutation intra camp | ecart |
|---|---|---|---|---|
| `agents v8` | 1 052 | 3,091378 | **3,091378** | **0,00e+00** |
| `agents composite` | 1 052 | 1,828597 | 1,828597 | 0,00e+00 |
| `B1 argmax` | 1 052 | 1,208929 | 1,208929 | 0,00e+00 |
| `B2 argmax` | 1 052 | 0,973468 | 0,973468 | 0,00e+00 |
| humains vague 2 | 1 052 | 1,025092 | 1,025092 | 0,00e+00 |
| **C2** | 150 | **1,616674** | **1,616674** | **0,00e+00** |
| **C3** | 150 | **0,523026** | **0,523026** | **0,00e+00** |

Les 27 lignes du fichier sont a ecart nul. Les valeurs publiees par a38 sont reproduites au
millieme. La relecture adverse ajoute que le generateur nul conditionnellement independant
de a44, parametre sur les marginales de segment, reproduit le facteur de `v8` a 3,092, celui
de `composite` a 1,830 et celui de `B1` a 1,210, soit **100,0 a 100,1 pour cent**
[a45 section 2.1, 30 replicats, non recalcule ici].

**Consequence pour a44.** Le tableau 9.2 de a44, qui recense les quantites de gabarit, ne
mentionne pas a38 alors que a38 precede a44 de sept minutes. Le meme raisonnement vaut sans
recalcul pour l'unanimite de a30, deja reconnue par a44, et pour la pente de a37 : le Gini
Simpson d'un camp sur un item et le rapport droite sur gauche par item sont eux aussi des
fonctionnelles de la table (camp, modalite).

### E3. Section 4.4 lectures 2 et 3 : `B2 argmax` ne recoit aucune demographie. Objection a45 numero 2.3, contradiction D4.

**Phrase d'origine.** « Ce n'est pas un effet de predicteur : `B2 argmax` est la methode la
plus exacte du jeu, 0,6717 en a28, et elle est a 1,01 », precede par « les trois predicteurs
statistiques **qui recoivent l'etiquette** reproduisent l'ecart humain sans l'exagerer.
`B2 argmax` a 1,01, `B3 foret` a 1,03, `B1 argmax` a 1,24. Ils ont la meme information
ideologique que les agents. »

**Correction.** `B2 argmax` est un plus proche voisin par **distance de Hamming sur les
seuls items de contexte** ; l'encodeur de demographies n'entre jamais dans son calcul. Il ne
recoit ni ideologie, ni parti, ni aucun des onze attributs. Seuls `B1` et `B3` les recoivent.
L'argument « trois predicteurs a etiquette reproduisent l'ecart » se reduit donc a deux, et
`B1`, celui des deux qui reproduit le mieux l'information de l'invite de `v8`, est a **1,24
avec un intervalle qui exclut 1**. `B2` a 1,01 est l'analogue statistique de C3, pas de C2 :
il dit qu'un predicteur nourri des 119 items ne caricature pas, ce qui est un autre resultat
et un resultat plus faible.

**Ce qu'il faut ecrire.** « Les deux predicteurs qui recoivent les onze attributs sont a 1,03
et 1,24, ce dernier excluant 1 ; le predicteur nourri des 119 items sans demographie est a
1,01. »

**Preuve.** [CONFIRME, `analyses/a2_baselines_gss.py` : ligne 178 `xt, xe =
enc.transform(x[tr]), enc.transform(x[te])` alimente `B0` et `B1` seuls ; lignes 188 a 191,
`d = distance_hamming(codes[np.ix_(te, contexte)], codes[np.ix_(tr, contexte)])` puis
`b2_voisins(d, ...)`, ou `contexte` est un ensemble d'items et jamais un encodage
demographique. Sortie de `analyses/a47_verifications.py`, bloc 3.]

### E4. Section 4 et hypothese K4 : C2 et C3 sont les deux conditions du contraste, et ce sont les deux qui ne passent pas Holm. Objection a45 numero 4, contradiction D3.

**Phrase d'origine.** « **Les deux intervalles ne se recouvrent pas**, et le signe de la
difference droite moins gauche s'inverse [MESURE]. »

**Correction.** Deux intervalles disjoints ne sont pas un test, et **aucun test apparie de
la difference C2 moins C3 n'est publie**. Sur la correction declaree du rapport, hypothese
K4, famille de 52 tests, `p` de Holm : **C2 vaut exactement 1,0000 et C3 vaut 0,2640**. Les
huit tests qui passent Holm sont **les six conditions de Stanford et les deux temoins `B0`**,
c'est a dire precisement les conditions qui ne permettent aucune inference sur le
conditionnement.

**Preuve.** [MESURE, `a38-corrections.csv`, hypothese `K4 camp`, colonne
`p_holm_famille_complete`]

| condition | `p` brut | **`p` Holm, famille de 52** | `p` BH, famille de 52 | `p` Holm, sous famille de 13 |
|---|---|---|---|---|
| `agents composite`, `entretien (v3)`, `enquete`, `v6`, `B0 mode`, `B0 tirage`, `v8` | 0,00005 | **0,0026** | 0,00037 | 0,00065 |
| `agents v7` | 0,00015 | **0,0068** | 0,00098 | 0,00090 |
| **`C3`** | 0,0060 | **0,2640** | 0,0347 | 0,0300 |
| `B1 argmax` | 0,0264 | **1,0000** | 0,1375 | 0,1058 |
| **`C2`** | 0,0298 | **1,0000** | 0,1409 | 0,1058 |

S'y ajoute que l'intervalle du facteur divise l'intervalle de la difference par un
denominateur **fixe**, `facteur = 1 moins difference / ecart_humain`, `ecart_humain` etant
traite comme une constante, 0,2219 sur 150 personnes et 0,2361 sur 1 052 : l'incertitude du
plancher humain n'est pas propagee.

**Ce qu'il faut ecrire.** « Les huit tests qui passent Holm sont les six conditions de
Stanford et les deux temoins ; C2 et C3, les deux conditions du contraste de conditionnement,
ne passent pas la correction principale, Holm 1,00 et 0,26, et ne passent que Benjamini
Hochberg sur la sous famille. »

---

Rapport du 8 septembre 2026. Il execute les tests T1 et T5 de
`corpus/lecture-complete/04-desirabilite-sociale-opinions-cachees.md`, section « Ce que ca
permet de tester chez nous tout de suite », et la ligne de partage comportement verifiable
contre attitude que la meme lecture designe comme la variable qui explique le desaccord de
la litterature.

Zero appel de modele de langage. Lecture seule sur `data/traces/` et
`data/osf-t6g7k-stanford/`. Cinq scripts nouveaux, `analyses/a38_extraire_norc.py`,
`a38_commun.py`, `a38_ampleurs.py`, `a38_mesures.py`, `a38_tests.py`, `a38_figure.py`.
Aucun script existant n'a ete modifie ; `a2_commun`, `a2_baselines_gss`, `a5_evaluer`,
`a5_agents_locaux_gss`, `a25_commun`, `a25_mesures`, `a28_commun`, `a28_test1_mode` et
`a30_commun` sont importes tels quels. La fonction de mesure par item est
`a28_test1_mode.mesurer`, reprise sans une ligne de changement : le controle de
reproduction porte sur 3 874 couples condition et item et donne un ecart maximal de
distance de 5,0 fois 10 puissance moins 7, qui est l'arrondi du CSV de a28 [MESURE].

Sorties : `a38-ampleurs-items.csv`, `a38-couverture.csv`, `a38-par-item-condition.csv`,
`a38-desirabilite-humaine-par-camp.csv`, `a38-par-camp.csv`, `a38-continu.csv`,
`a38-comportement.csv`, `a38-verification-pole-endogroupe.csv`, `a38-camp.csv`,
`a38-camp-robustesse.csv`, `a38-corrections.csv`, `a38-contraste-de-groupe.csv`,
`a38-robustesse.csv`, `a38-figure-mode-continu.png` et `.svg`.

---

## Reponse en une ligne

**La version continue de T1 ne survit pas au remplacement du score fabrique de a28 par les
ampleurs reellement publiees : aucune correlation ne se distingue de zero pour aucune
methode, et le contraste de groupe tombe de plus 0,356 avec p = 0,0009 a plus 0,176 avec
p = 0,047 ; en revanche la version par camp de T5 donne le resultat le plus net du projet
sur ce theme, les quatre conditions riches de Stanford et C2 exagerent l'ecart ideologique
humain d'un facteur 1,6 a 3,2 quand tous les predicteurs statistiques qui recoivent la meme
etiquette le reproduisent entre 0,97 et 1,24 et que les memes humains reinterroges sont a
0,98, et c'est l'etiquette qui le produit, C2 avec etiquette a 1,62 [1,06 ; 2,10] contre C3
sans etiquette a 0,52 [0,20 ; 0,82]** [MESURE, `a38-camp.csv`, perimetres 150 et 1 052].

---

## La famille d'hypotheses, fixee avant les resultats

Recopiee sans retouche de l'entete de `analyses/a38_commun.py`. Elle prolonge celle de a28
sans la rejouer : les 52 tests de a28 ne sont pas repris, ce sont d'autres tests sur les
memes donnees.

| | enonce | nombre |
|---|---|---|
| **K1** primaire, T1 continu, distance | pour chacune des 13 methodes non humaines, la correlation de rang entre l'ampleur de mode MESUREE par item et la distance agent contre humain par item est positive. Score M1, perimetre 150 | 13 |
| **K2** primaire, T1 continu, dispersion | la meme avec le rapport d'entropie agent sur humain, prediction de signe NEGATIF. Score M1, perimetre 150 | 13 |
| **K3** secondaire, comportement contre attitude | pour chacune des 13 methodes, le contraste de distance sensible moins temoin est plus grand sur les comportements declares que sur les attitudes. Perimetre 150 | 13 |
| **K4** secondaire, par camp | pour chacune des 13 methodes, l'ecart de desirabilite agent contre humain differe entre le bloc de gauche et le bloc de droite, sur les items pourvus d'un pole d'endogroupe documente. Perimetre 150 | 13 |

**Correction principale : Holm sur les 52.** Correction secondaire rapportee a cote :
Benjamini Hochberg sur les 52. Les corrections par sous famille de 13 sont aussi donnees.

**N'entrent PAS dans la famille**, et sont rapportes comme des descriptions : la ligne
`humains vague 2`, temoin negatif et non hypothese ; les scores M2 et M3, qui melangent des
constructions differentes et servent de controle de robustesse ; le perimetre 1 052,
echantillon emboite ; les contrastes de GROUPE, huit conditions a modele de langage contre
cinq predicteurs statistiques, post hoc au meme titre qu'en a28 section 1.6 et auxquels
aucune correction n'est appliquee ; les sous ensembles d'items de K4.

---

## 1. Le protocole : d'ou vient chaque ampleur

### 1.1 Ce que a25 declarait impossible et qui ne l'est pas

a25, point 1 de « ce que je n'ai pas pu verifier » : « NORC ne publie pas d'ampleur par
item [...] la version continue de la prediction n'est donc pas testable en l'etat ». C'est
exact de la note de sensibilite au mode de 2022, qui ne donne que trois classes. C'est faux
de NORC dans son ensemble : le catalogue des rapports methodologiques du GSS porte au moins
cinq pieces qui donnent une ampleur continue item par item [CONFIRME, lues dans les PDF].

a28 avait construit une reponse intermediaire, son score S2, en attribuant une valeur en
points par DOMAINE, avec cinq entrees marquees [HYPOTHESE] et une couverture de 5 des 12
items sensibles. a38 remplace ce score par des mesures, item par item.

### 1.2 Les six sources, telechargees et depouillees le 8 septembre 2026

Les tables sont transcrites a la main dans `analyses/a38_extraire_norc.py`, avec leur table
et leur page, et ecrites dans `data/norc-mode/` avec un `PROVENANCE.md` portant les
empreintes SHA-256 des PDF. Ce repertoire n'est pas versionne, `data/` etant dans
`.gitignore` ; le code versionne est la source, les CSV sont la sortie.

| source | table et page | ce qui est mesure | items de nos 149 | famille |
|---|---|---|---|---|
| **MR099**, Smith et Dennis 2004 | Table 3, page 15 | GSS 2002 en face a face contre panel web Knowledge Networks, traitement A, don't know exclus des deux cotes, 17 items de depense | **16** | mode |
| **MR141**, Sparkman et al. 2024 | Table 4, pages 10 a 12, colonnes 2022, cas web | condition sans modalite volontaire contre condition avec, GSS 2022 | **17** | conception |
| **MR010**, Smith 1981 | page 225 | part des « non » a la question absolue qui approuvent au moins une situation concrete | **1** | regime |
| **MR021**, Smith | pages 3 et 9 | participation declaree contre estimation tiree des resultats officiels ; ecart absolu moyen sur le choix de candidat | **3** | mode |
| **MR086**, Smith 1995 | page 10 | sante auto declaree selon la presence d'un tiers | **1** | mode |
| **Atlas NBER 33920**, Bursztyn, Haaland, Rover et Roth 2025 | Appendix Table A2 page 39, A3 page 40 | prevalence declaree contre registre individuel, six domaines | **2** | mode |

**Une source verifiee et vide, consignee pour qu'on ne la rouvre pas.** MR145, *Recent
Changes in GSS Questions on Religion*, mars 2026, donne bien une ampleur de mode par
modalite, 2022 en face a face contre web : protestants 45,4 contre 36,1 pour cent, sans
religion 24,3 contre 32,7, catholiques 20,9 contre 21,4 [CONFIRME, tables 2 et 3]. Mais il
ne porte que sur `RELIG`, `DENOM` et `OTHER`, aucune des trois n'etant dans nos 149 items ;
`relig16*` et `jew16*` sont la religion a seize ans, une autre variable. **Aucun de nos
quatre poles religieux, `attend`, `pray`, `reborn`, `savesoul`, ne recoit d'ampleur
chiffree** [MESURE].

**Ce que l'atlas NBER couvre, et ce qu'il ne peut pas couvrir.** Son critere d'inclusion
est severe et explicite : uniquement les etudes qui apparient declaration et registre au
niveau de l'individu. Il ne contient donc que des comportements verifiables. Sur nos 149
items du GSS, **deux** tombent dans un de ses six domaines : `vote16` par Kleven 2022, non
participation reelle 14 pour cent contre declaree 11 pour cent sur 26 333 personnes, soit
3,0 points ; et `unemp` par Dutz et al. 2021, 9 pour cent contre 8, soit 1,0 point
[MESURE]. **Le fait que l'atlas soit presque vide sur nos items n'est pas une lacune de
l'atlas, c'est le resultat central de la section 3 de ce rapport.**

### 1.3 Trois familles qui ne mesurent pas la meme chose, et trois scores

Elles ne sont jamais fondues sans le dire.

- **mode** : un contraste de mode de collecte au sens strict, ou entre declaration et
  registre. MR099, MR021, MR086, atlas. C'est la seule famille qui mesure ce que la these
  appelle « les humains se surveillent ».
- **conception** : MR141, la part de repondants qui prennent une modalite volontaire des
  qu'elle est visible. Ce n'est pas de la desirabilite, c'est de la conception d'item, et
  l'ampleur y est d'un ordre de grandeur au dessus. C'est un **confondant** de la famille
  mode, pas une de ses variantes.
- **regime** : MR010, le passage de la question absolue a la question situationnelle.

D'ou trois scores. **M1 = mode seule**, c'est le score pre enregistre de K1 et K2.
**M2 = M1 union conception**, controle. **M3 = M2 union regime**, couverture maximale et
homogeneite minimale. Toutes les ampleurs sont en points de pourcentage. **Une ampleur
absente reste absente, elle n'est jamais remplacee par zero.**

### 1.4 Combien d'items ont une ampleur, combien n'en ont pas

[MESURE, `a38-couverture.csv`]

| classe NORC | items | avec M1 | avec M2 | avec M3 |
|---|---|---|---|---|
| sensible | 12 | **4** | 4 | 4 |
| a investiguer | 13 | 1 | 1 | 1 |
| temoin negatif | 65 | 12 | 12 | 13 |
| mixte, ecarte des deux bras par a25 | 4 | **4** | 4 | 4 |
| non teste par NORC | 55 | 0 | 17 | 17 |
| **total** | **149** | **21** | **38** | **39** |

**Vingt et un items sur 149 ont une ampleur de mode mesuree ; 128 n'en ont pas** [MESURE].
Avec les deux autres familles, 39 sur 149, et 110 n'en ont pas.

Sur les **12 items sensibles**, quatre seulement recoivent une ampleur : `natrace/y` a 13,8
points, la plus grande des 17 items de depense de MR099 ; `natchld` a 5,8 ; `natroad` a
0,36 ; `vote16` a 10,0 par MR021. Les huit autres, `coneduc`, `conlegis`, `conmedic`,
`spkrac/y`, `polabuse/y`, `polattak/y`, `xmarsex` et `attend`, n'ont aucune ampleur
publiee [MESURE]. C'est mieux que le score S2 de a28, qui n'en couvrait 5 que par
transposition de domaine, et c'est loin d'etre bon.

**Un gain reel et un seul.** Les quatre items « mixte » que a25 devait ecarter des deux
bras, `natspac/y`, `natheal/y`, `natcity/y` et `natfare/y`, parce que Stanford fusionne
sous un meme nom de colonne deux formes que NORC classe differemment, **recoivent tous une
ampleur continue** et rentrent donc dans le test. La version continue recupere ce que la
version categorielle jetait.

---

## 2. K1 et K2 : la version continue ne tient pas

Figure : `a38-figure-mode-continu.png` et `.svg`, panneaux de gauche et du milieu pour les
nuages, panneau de droite pour la lecture.

### 2.1 Aucune correlation ne se distingue de zero

[MESURE, `a38-continu.csv`, perimetre 150, metrique de distance]

| condition | M1 mode, 21 items | IC 95 % items | p brut | M2, 38 items | M3, 39 items |
|---|---|---|---|---|---|
| C3 | **+0,290** | [-0,171 ; +0,676] | 0,200 | +0,100 | +0,159 |
| agents v8 | +0,174 | [-0,331 ; +0,592] | 0,443 | -0,120 | -0,066 |
| agents v7 | +0,139 | [-0,340 ; +0,559] | 0,541 | +0,155 | +0,171 |
| agents enquete | +0,036 | [-0,370 ; +0,451] | 0,878 | -0,045 | -0,095 |
| C2 | -0,021 | [-0,453 ; +0,451] | 0,924 | +0,057 | +0,126 |
| agents demographiques (v6) | -0,028 | [-0,515 ; +0,451] | 0,900 | -0,057 | +0,016 |
| agents entretien (v3) | -0,039 | [-0,521 ; +0,459] | 0,866 | +0,009 | +0,070 |
| agents composite | -0,170 | [-0,660 ; +0,377] | 0,461 | -0,203 | -0,224 |
| B3 foret | +0,033 | [-0,468 ; +0,563] | 0,890 | -0,044 | +0,027 |
| B2 argmax | -0,089 | [-0,513 ; +0,363] | 0,697 | -0,279 | -0,191 |
| B1 argmax | -0,117 | [-0,571 ; +0,369] | 0,611 | -0,164 | -0,078 |
| B0 tirage | -0,171 | [-0,623 ; +0,367] | 0,448 | -0,256 | -0,166 |
| B0 mode | -0,300 | [-0,708 ; +0,155] | 0,184 | +0,115 | +0,152 |
| *humains vague 2* | -0,233 | [-0,662 ; +0,326] | 0,304 | -0,045 | -0,102 |

**Aucun p brut ne descend sous 0,18.** Les intervalles bootstrap sur les items font tous
plus d'un point de large et contiennent tous zero, ce qui est attendu avec 21 items. Sur la
dispersion, K2, le tableau est le meme et le meilleur p vaut 0,119, `agents entretien (v3)`
a plus 0,353 [-0,106 ; +0,693], **de signe oppose a la prediction** [MESURE].

### 2.2 Le contraste de groupe, post hoc, s'affaiblit nettement

[MESURE, `a38-contraste-de-groupe.csv`, permutation des etiquettes de methode, 20 000
tirages]

| quantite | moyenne des 8 conditions a langage | moyenne des 5 predicteurs | difference | p |
|---|---|---|---|---|
| K1 distance, **M1 mode**, perimetre 150 | +0,047 | -0,129 | **+0,176** | **0,047** |
| K1 distance, M1 mode, perimetre 1 052 | +0,018 | -0,141 | +0,159 | 0,059 |
| K1 distance, M2, perimetre 150 | -0,013 | -0,126 | +0,113 | 0,176 |
| K1 distance, M3, perimetre 150 | +0,020 | -0,051 | +0,071 | 0,398 |
| K2 dispersion, M1 mode, perimetre 150 | +0,061 | +0,040 | +0,021 | 0,835 |
| K2 dispersion, M3, perimetre 1 052 | -0,141 | +0,058 | -0,199 | 0,035 |

**A comparer sans indulgence avec a28.** Le meme contraste de groupe, calcule sur le score
S2 fabrique par domaine, valait **plus 0,356 avec p = 0,0009** (a28, section 1.6). Sur les
ampleurs reellement publiees, il vaut **plus 0,176 avec p = 0,047**, et il disparait des
qu'on elargit la couverture. **Le motif le plus net de a28 tenait donc pour une part au
score que a28 avait fabrique.** Le signe est le meme, l'ordre de grandeur est divise par
deux, et le p passe de trois chiffres apres la virgule a la frontiere.

### 2.3 Le confondant de conception, mesure

MR141 donne, sur 17 items communs, la part de repondants qui prennent la modalite
volontaire des qu'elle est affichee, de 7,3 pour cent sur `discaffw` a 63,9 pour cent sur
`aged`. La lecture 04 le posait comme un test qui peut faire tomber une partie du resultat
de a25 : si la correlation est forte, une part de l'ecart attribue au modele vient de ce
que l'humain disposait d'une echappatoire que l'agent n'a jamais eue.

[MESURE, `a38-robustesse.csv`, perimetre 150, correlation de rang entre part de modalite
volontaire et distance, 17 items] : `agents enquete` **moins 0,547**, `B0 tirage` moins
0,311, `B2 argmax` moins 0,252, `agents demographiques (v6)` moins 0,201, `B1 argmax` moins
0,186, `agents composite` moins 0,150, `humains vague 2` moins 0,141, `C3` plus 0,311, `C2`
plus 0,071, `agents entretien (v3)` plus 0,156.

**La correlation est negative pour neuf methodes sur treize, et elle n'est pas plus forte
chez les modeles de langage que chez les predicteurs statistiques.** Le confondant existe
et il ne va pas dans le sens de l'objection : les agents ne s'ecartent pas davantage la ou
l'humain avait une echappatoire, ils s'en ecartent plutot moins. Le test etait a faire, il
est fait, et il ne detruit rien [MESURE].

### 2.4 Deux controles qui manquent de puissance

`M1 sur les seules attitudes` ne laisse que 16 items et `M1 sans les items de depense` que
5, sous le seuil de six paires en dessous duquel la correlation n'est pas calculee
[MESURE]. **Seize des 21 items couverts par M1 sont des items de depense publique** : la
version continue de T1 est, en pratique, un test sur la famille `nat*` et sur elle seule.
C'est sa limite principale et elle n'est pas reparable sans nouvelles mesures.

---

## 3. La ligne de partage comportement verifiable contre attitude

### 3.1 Le classement, et pourquoi trois classes et non deux

La lecture 04 designe cette ligne comme la variable qui explique le desaccord de la
litterature, dans ses contradictions numero 1 et numero 2 : les etudes qui trouvent de la
desirabilite disposent d'une verite terrain individuelle et portent sur des
**comportements** ; celles qui n'en trouvent pas portent sur des **attitudes**. L'atlas
NBER l'inscrit dans son critere d'inclusion [CONFIRME], Smith 1995 le mesure sur le GSS lui
meme, ou la presence d'un tiers ne change aucune attitude [CONFIRME].

Trois classes et non deux, declarees dans `a38_commun.py`. Est un **comportement declare**
un item qui demande au repondant de rapporter ce qu'il a fait, ce qu'il fait, ou un etat de
fait le concernant, et dont un registre pourrait en principe donner la valeur. Est une
**auto evaluation** un item qui lui demande de noter sa propre situation sur une echelle
subjective. Tout le reste est une **attitude**. L'auto evaluation est isolee parce que Ye,
Fulton et Tourangeau 2011 proposent, sur 18 comparaisons, une explication concurrente et
plus economique de ce qu'on y observe : le mode ne pousse pas vers le pole desirable, il
pousse vers l'extremite positive de l'echelle [PROBABLE].

Repartition des 149 items : **42 comportements, 95 attitudes, 12 auto evaluations**
[MESURE]. Dans les 12 items sensibles de NORC : **2 comportements**, `vote16` et `attend`,
et **10 attitudes**. Dans les 65 temoins : 11 comportements, 45 attitudes, 9 auto
evaluations. Aucun item sensible n'est une auto evaluation, la colonne correspondante est
donc vide.

### 3.2 Le contraste de a28 est un phenomene d'attitudes, exactement la ou la litterature n'en attend pas

[MESURE, `a38-comportement.csv`, perimetre 150, metrique de distance, contraste sensible
moins temoin]

| condition | comportements, 2 contre 11 items | attitudes, 10 contre 45 items | difference | IC 95 % items | p |
|---|---|---|---|---|---|
| agents v8 | -0,010 | **+0,093** | -0,103 | [-0,267 ; +0,056] | 0,317 |
| agents demographiques (v6) | -0,031 | **+0,071** | -0,102 | [-0,199 ; -0,011] | 0,198 |
| agents composite | -0,018 | **+0,070** | -0,089 | [-0,175 ; -0,017] | 0,126 |
| agents entretien (v3) | +0,003 | **+0,084** | -0,081 | [-0,178 ; +0,008] | 0,138 |
| agents enquete | -0,003 | **+0,062** | -0,065 | [-0,147 ; +0,011] | 0,262 |
| agents v7 | +0,040 | +0,038 | +0,002 | [-0,094 ; +0,093] | 0,973 |
| B3 foret | +0,040 | +0,000 | +0,040 | [-0,066 ; +0,142] | 0,617 |
| B2 argmax | +0,045 | +0,008 | +0,037 | [-0,106 ; +0,180] | 0,637 |
| B1 argmax | +0,032 | +0,006 | +0,026 | [-0,067 ; +0,115] | 0,642 |
| B0 tirage | -0,002 | -0,008 | +0,006 | [-0,029 ; +0,039] | 0,810 |
| B0 mode | -0,039 | -0,006 | -0,033 | [-0,195 ; +0,122] | 0,862 |
| **C3** | **+0,102** | +0,024 | +0,078 | [-0,293 ; +0,449] | 0,678 |
| **C2** | **+0,104** | +0,030 | +0,074 | [-0,244 ; +0,393] | 0,686 |
| *humains vague 2* | -0,008 | -0,002 | -0,006 | [-0,026 ; +0,013] | 0,713 |

**Aucune condition ne passe K3, et c'est la moindre des choses avec deux items sensibles
d'un cote.** Le resultat qui compte est ailleurs, dans le contraste de groupe post hoc
[MESURE, `a38-contraste-de-groupe.csv`] :

| quantite | 8 conditions a langage | 5 predicteurs | difference | p |
|---|---|---|---|---|
| contraste sur les **attitudes seules** | +0,0591 | +0,0002 | **+0,0588** | **0,0012** |
| contraste sur les **comportements seuls** | +0,0233 | +0,0151 | +0,0082 | 0,768 |
| difference des deux | -0,0357 | +0,0149 | -0,0506 | 0,191 |

**Enonce, et il faut le porter tel quel.** Le motif qui fait tout le resultat de a25 et de
a28, huit conditions a modele de langage qui s'ecartent plus des humains sur les items
sensibles quand cinq predicteurs statistiques ne le font pas, **est entier sur les
attitudes et absent sur les comportements declares** : plus 0,059 avec p = 0,0012 d'un
cote, plus 0,008 avec p = 0,77 de l'autre [MESURE].

Or c'est **l'inverse** de ce que la litterature humaine predit. La desirabilite mesuree
contre verite terrain est un phenomene de comportement verifiable : l'atlas l'inscrit dans
son critere d'inclusion, Smith 1995 ne trouve aucun effet de presence d'un tiers sur les
attitudes du GSS, et la liste des resultats negatifs sur les attitudes politiques est
longue, Coppock 2017, Lax Phillips et Stollwerk 2016, les deux rapports AAPOR, Engelhardt
2021, Magalhaes et Aarslew 2025 sur 24 pays, Kaftan 2024 sur 14 000 repondants [CONFIRME
via la lecture 04].

**Consequence directe pour la redaction.** Ce que a25 et a28 mesurent ne peut donc pas
s'appeler « la simulation devie la ou les humains se surveillent », puisque la ou les
humains se surveillent de facon etablie, les comportements verifiables, la simulation ne
devie pas plus qu'ailleurs. La formulation qui survit est : **la simulation devie la ou
NORC a mesure que la distribution bouge avec le mode, et cette deviation est un phenomene
d'attitude**. C'est plus faible, c'est plus etrange, et c'est ce qui est mesure
[HYPOTHESE pour l'interpretation, MESURE pour le fait].

**La reserve de puissance, en clair.** Deux items sensibles du cote comportement, `vote16`
et `attend`. Le contraste sur les comportements repose sur ces deux la, et il n'a aucune
puissance. Ce qui est solide est le contraste sur les attitudes, dix items, et le fait que
le contraste de groupe y soit a p = 0,0012 alors qu'il est nul sur l'autre bras.

---

## 4. K4 : la version par camp, et le resultat le plus net du rapport

### 4.1 Le probleme pose par Oceno 2025, et comment il est traite ici

a25 fixe, item par item, un pole socialement desirable unique valable pour toute la
population. Oceno 2025 montre sur l'ANES 2012 et 2016 que cette hypothese est fausse pour
les items evaluatifs : sur les emotions positives, le sens s'inverse selon le camp et selon
l'objet, « Republicans' positive emotions in 2016 mirror, in reverse, those of Democrats in
2012 » [CONFIRME].

Deux lectures concurrentes, toutes deux documentees.

- **Lecture A, norme societale unique.** Il existe un pole presentable pour tout le monde,
  et c'est le camp dont la position sincere s'en ecarte qui se tait. Berinsky 1999 sur la
  race, Bursztyn Egorov et Fiorin 2020 sur l'immigration, Coffman Coffman et Ericson 2017
  sur l'hostilite envers les gays, Gibson et Sutherland 2023 sur l'asymetrie de l'auto
  censure, Valentim 2024 sur ce qui se passe quand la norme cede.
- **Lecture B, norme d'endogroupe.** La desirabilite est une fonction de la cible et de
  l'approbation du groupe de reference, Crandall Eshleman et O'Brien 2002 sur 105 groupes
  sociaux ; l'attitude declaree suit « almost exclusively » la position affichee du parti,
  Cohen 2003 ; une etiquette ideologique code une disposition a suivre et non une position,
  Barber et Pope 2019.

**Ce que a38 declare, et c'est peu.** Le score de desirabilite reste celui de a25,
inchange, et c'est le pole de la lecture A. Ce qui est declare item par item, c'est
uniquement de quel cote de ce score se trouve la position typique de la droite. **Un seul
bit par item**, ce qui est beaucoup moins contestable qu'un pole invente par camp. Le signe
de l'ecart suffit alors a departager : droite positive et gauche nulle donne la lecture A,
droite negative et gauche positive donne la lecture B.

**Vingt neuf items sur 149 recoivent un bit declare ; 120 sont exclus faute de source**
[MESURE]. Sont notamment exclus, et la raison est ecrite dans le code : `nataid/y` et
`natarms/y`, ou le clivage partisan s'inverse et ou Smith et Dennis relevent eux memes une
large majorite hostile a l'aide etrangere ; toute l'echelle de tolerance de Stouffer, ou
deux normes s'opposent et ou a25 refuse deja de fixer un pole ; toute la famille `con*`, ou
la confiance dans la presse, dans la science et dans le pouvoir federal a change de camp au
moins une fois depuis 2016, ce qui est exactement le motif d'Oceno ; toute la religion, ou
MR145 retire une part de l'ecart de mode a la desirabilite ; et tous les items
d'avortement, de peine de mort et d'armes, auxquels a25 ne donne aucun pole.

### 4.2 Le bit declare, verifie sur les humains

`a38-verification-pole-endogroupe.csv`. **Sur 29 items, 28 sont confirmes par les humains
de la vague 1 au perimetre 1 052, et 27 au perimetre 150** [MESURE]. Le seul echec est
`natroad`, les depenses d'autoroutes, ou l'ecart entre camps vaut moins 0,009 point : ce
n'est pas un item partisan. Le test rejoue sans lui ne bouge pas, section 4.5.

Les ecarts humains les plus grands, gauche moins droite, sur le score de desirabilite
[MESURE, perimetre 1 052] : `racdif1` plus 0,603, `natrace/y` plus 0,463, `racdif3` plus
0,457, `homosex` plus 0,431, `marhomo` plus 0,397, `letin1a` plus 0,377. Les plus petits :
`natroad` moins 0,009, `racdif2` plus 0,015, `natspac/y` plus 0,023.

### 4.3 L'echelle de lecture, donnee par les humains eux memes

Soit `ecart_humain` l'ecart de score de desirabilite entre le bloc de gauche et le bloc de
droite dans la population humaine de la vague 1, moyenne sur les 29 items. Il vaut
**plus 0,2219** au perimetre 150 et **plus 0,2361** au perimetre 1 052 [MESURE]. Alors, par
construction :

```
difference droite moins gauche  =  ecart_humain  moins  ecart_simule
```

ce qui donne trois reperes exacts et non arbitraires :

- **facteur d'amplification 0** : la methode ignore completement le camp ;
- **facteur 1** : la methode reproduit exactement l'ecart humain entre camps ;
- **facteur superieur a 1** : la methode **exagere** l'ecart entre camps.

Le facteur d'amplification vaut `ecart_simule / ecart_humain`. **Le controle qui valide
l'echelle** : les memes humains reinterroges a deux semaines valent **0,984
[0,873 ; 1,091]** au perimetre 150 et **1,025 [0,986 ; 1,064]** au perimetre 1 052
[MESURE]. L'echelle est bien calibree.

### 4.4 Le resultat

[MESURE, `a38-camp.csv`, perimetre 150, 29 items, permutation de signe appariee par item,
20 000 tirages]

| condition | ecart gauche | ecart centre | ecart droite | droite moins gauche | IC 95 % items | p | **facteur d'amplification** | IC |
|---|---|---|---|---|---|---|---|---|
| **agents v8** | +0,143 | +0,048 | **-0,338** | **-0,481** | [-0,549 ; -0,409] | **0,0000** | **3,17** | [2,84 ; 3,47] |
| agents entretien (v3) | +0,054 | -0,029 | **-0,187** | **-0,241** | [-0,295 ; -0,187] | **0,0000** | **2,09** | [1,85 ; 2,33] |
| agents enquete | +0,101 | +0,060 | -0,090 | **-0,191** | [-0,239 ; -0,143] | **0,0000** | **1,86** | [1,65 ; 2,08] |
| agents composite | +0,054 | -0,024 | -0,129 | **-0,184** | [-0,229 ; -0,139] | **0,0000** | **1,83** | [1,63 ; 2,03] |
| **C2**, avec etiquette | +0,025 | -0,047 | -0,112 | **-0,137** | [-0,244 ; -0,012] | **0,0298** | **1,62** | [1,06 ; 2,10] |
| B1 argmax | +0,085 | +0,065 | +0,032 | -0,053 | [-0,095 ; -0,010] | **0,0264** | 1,24 | [1,04 ; 1,43] |
| B3 foret | +0,088 | +0,097 | +0,080 | -0,008 | [-0,058 ; +0,040] | 0,771 | 1,03 | [0,82 ; 1,26] |
| B2 argmax | +0,091 | +0,101 | +0,088 | -0,003 | [-0,036 ; +0,030] | 0,877 | 1,01 | [0,86 ; 1,16] |
| *humains vague 2* | -0,014 | -0,013 | -0,011 | +0,003 | [-0,020 ; +0,028] | 0,784 | *0,98* | [0,87 ; 1,09] |
| **C3**, sans etiquette | +0,076 | +0,129 | +0,182 | **+0,106** | [+0,039 ; +0,178] | **0,0060** | **0,52** | [0,20 ; 0,82] |
| agents v7 | +0,093 | +0,118 | +0,229 | **+0,136** | [+0,078 ; +0,202] | **0,0001** | 0,39 | [0,09 ; 0,65] |
| agents demographiques (v6) | +0,037 | +0,105 | +0,194 | **+0,157** | [+0,102 ; +0,218] | **0,0000** | 0,29 | [0,02 ; 0,54] |
| B0 tirage | -0,083 | -0,000 | +0,134 | **+0,218** | [+0,160 ; +0,278] | **0,0000** | 0,02 | [-0,25 ; +0,28] |
| B0 mode | +0,027 | +0,127 | +0,249 | **+0,222** | [+0,165 ; +0,283] | **0,0000** | -0,00 | [-0,28 ; +0,26] |

Le perimetre 1 052 donne le meme classement et les memes ordres de grandeur, avec `agents
v8` a 3,09, `entretien (v3)` a 2,07, `enquete` a 1,88, `composite` a 1,83, `B1` a 1,21,
`B2` a 0,97, `B3` a 0,99, `v7` a 0,27, `v6` a 0,31, `B0 mode` a moins 0,01 et les humains a
1,03 [MESURE].

**Cinq lectures, dans l'ordre de solidite.**

1. **Les deux `B0` sont a zero, et c'est une identite et non un resultat.** `B0 mode`
   predit la modalite majoritaire de la population entiere et `B0 tirage` echantillonne
   dans la marginale globale : ni l'un ni l'autre ne recoit d'information sur la personne,
   donc leur population simulee est la meme dans les deux camps, donc l'ecart simule est
   nul par construction. **Ils bornent le bas de l'echelle**, exactement comme `B0 tirage`
   bornait le haut de la selectivite en a28 section 2.3.
2. **Les trois predicteurs statistiques qui recoivent l'etiquette reproduisent l'ecart
   humain sans l'exagerer.** `B2 argmax` a 1,01, `B3 foret` a 1,03, `B1 argmax` a 1,24 dont
   l'intervalle exclut 1 de justesse. Ils ont la meme information ideologique que les
   agents, et la meme reponse deterministe par argmax.
3. **Les quatre conditions riches de Stanford et C2 exagerent l'ecart d'un facteur 1,6 a
   3,2**, avec des intervalles qui excluent 1 dans les cinq cas. **Ce n'est pas un effet de
   predicteur** : `B2 argmax` est la methode la plus exacte du jeu, 0,6717 en a28, et elle
   est a 1,01.
4. **L'etiquette est ce qui produit la caricature.** C2, persona demographique de onze
   attributs dont `polviews`, vaut 1,62 [1,06 ; 2,10]. C3, 119 reponses d'enquete et aucune
   demographie, vaut 0,52 [0,20 ; 0,82]. **Les deux intervalles ne se recouvrent pas**, et
   le signe de la difference droite moins gauche s'inverse [MESURE]. Meme modele,
   Qwen3-4B, meme temperature, memes 150 personnes, memes items : seule l'etiquette change.
5. **Trois conditions sous reproduisent l'ecart, `v6` a 0,29, `v7` a 0,39, C3 a 0,52.**
   Elles se comportent comme des methodes partiellement aveugles au camp. Pour C3
   l'explication est directe, elle n'a pas l'etiquette. Pour `v6` et `v7`, qui l'ont, elle
   n'est pas etablie ici.

**Ce que cela ajoute a a28 test 3.** a28 mesurait deja une substitution de la personne par
le groupe, mais sa mesure ne separait rien : les humains reinterroges y etaient a 0,537 et
`B1 argmax` a 0,552, contre 0,371 a 0,715 pour les agents. **Ici la mesure separe**, parce
que le plancher humain vaut exactement 1 et que les predicteurs statistiques a etiquette
valent 1 aussi. C'est la meme substitution, mesuree sur une echelle ou elle devient
lisible.

Un exemple item par item, perimetre 1 052, ecart de desirabilite agent contre humain
[MESURE, `a38-par-camp.csv`] :

| item | camp | agents composite | agents v8 | B2 argmax | B0 mode | humains vague 2 |
|---|---|---|---|---|---|---|
| `homosex` | gauche | +0,068 | +0,122 | +0,099 | +0,123 | -0,001 |
| `homosex` | droite | +0,033 | **-0,344** | +0,128 | **+0,554** | -0,022 |
| `natrace/y` | gauche | +0,090 | +0,211 | +0,116 | -0,187 | -0,025 |
| `natrace/y` | droite | **-0,150** | **-0,239** | +0,018 | **+0,307** | +0,002 |
| `racdif1` | gauche | -0,019 | +0,185 | +0,115 | +0,189 | -0,024 |
| `racdif1` | droite | -0,139 | -0,147 | -0,006 | **+0,792** | -0,009 |

Sur `homosex`, `agents v8` deplace la droite simulee de 0,344 point vers le pole hostile et
la gauche de 0,122 point vers le pole tolerant ; `B0 mode`, qui ignore le camp, deplace la
droite de 0,554 point vers le pole tolerant. Les deux erreurs sont grandes et de sens
oppose.

### 4.5 Robustesse au sous ensemble d'items

Quinze des 29 items sont des items de depense publique, ou Smith et Dennis refusent
explicitement de lire le pole pro depense comme le pole socialement desirable. Le test est
donc rejoue sans eux [MESURE, `a38-camp-robustesse.csv`, perimetre 150, facteur
d'amplification] :

| condition | tous, 29 items | sans les depenses, 14 items | depenses seules, 15 items | sans `natroad`, 28 items |
|---|---|---|---|---|
| agents v8 | 3,17 | 2,50 | 4,06 | 3,15 |
| agents entretien (v3) | 2,09 | 1,71 | 2,59 | 2,09 |
| agents enquete | 1,86 | 1,76 | 2,00 | 1,84 |
| agents composite | 1,83 | 1,38 | 2,43 | 1,81 |
| C2 | 1,62 | 1,10 | 2,32 | 1,56 |
| B1 argmax | 1,24 | 1,29 | 1,17 | 1,26 |
| B3 foret | 1,03 | 1,11 | 0,93 | 1,05 |
| B2 argmax | 1,01 | 1,00 | 1,03 | 1,01 |
| humains vague 2 | 0,98 | 0,94 | 1,05 | 1,00 |
| C3 | 0,52 | 0,54 | 0,50 | 0,50 |
| v7 | 0,39 | 0,30 | 0,50 | 0,39 |
| v6 | 0,29 | 0,37 | 0,19 | 0,30 |
| B0 mode | -0,00 | -0,00 | +0,00 | -0,00 |

**Le classement est le meme dans les quatre colonnes.** L'amplification est plus forte sur
les items de depense que sur les autres, ce qui affaiblit un peu C2, a 1,10 hors depenses,
mais aucune inversion ne se produit.

---

## 5. Corrections pour tests multiples

[MESURE, `a38-corrections.csv`, famille de 52 tests declaree avant les resultats]

| correction | tests sous 0,05 | meilleur p ajuste |
|---|---|---|
| **Holm sur les 52** | **8** | **0,0026** |
| Benjamini Hochberg sur les 52 | 9 | 0,0004 |
| Holm par sous famille de 13 | 9 | 0,0006 |
| Benjamini Hochberg par sous famille de 13 | 11 | 0,0001 |

Les huit tests qui passent Holm sur la famille complete appartiennent **tous a K4** :
`agents v8`, `agents entretien (v3)`, `agents enquete`, `agents demographiques (v6)`,
`agents composite`, `B0 tirage`, `B0 mode` et `agents v7`. Le neuvieme, C3, passe
Benjamini Hochberg a 0,0347 mais pas Holm, a 0,264. C2 et `B1 argmax` sont a 1,000 par Holm
et respectivement 0,141 et 0,138 par Benjamini Hochberg.

**Aucun test de K1, K2 ou K3 ne passe quoi que ce soit**, le meilleur p brut de ces trois
sous familles valant 0,119.

Contraste avec a28, ou aucune condition ne passait la correction sur aucune hypothese. **Ce
rapport produit les premiers tests du theme qui survivent a une correction declaree
d'avance**, et ce sont ceux du volet par camp.

---

## 6. La figure

`resultats/a38-figure-mode-continu.png` et `.svg`, perimetre 150. Panneau de gauche : nuage
item par item, abscisse l'ampleur de mode M1 en points, ordonnee la distance moyenne aux
humains sur les huit conditions a modele de langage, barre verticale d'ecart type entre
conditions, item nomme. Panneau du milieu : le meme nuage pour les cinq predicteurs
statistiques. Panneau de droite : la correlation de rang de chaque methode avec son
intervalle bootstrap sur les items et son p.

La lecture voulue est celle du panneau de droite : **les treize intervalles contiennent
zero, et les points rouges sont en moyenne a droite des points bleus, sans separation.** La
droite tracee dans les deux nuages est une droite des moindres carres, guide de lecture
seulement ; la statistique commentee est la correlation de rang.

---

## Ce que cela change a `ARBITRAGE.md`

`ARBITRAGE.md` ecrit, point 1 : « La simulation devie la ou les humains se surveillent.
Vrai en bloc, faux methode par methode. [...] C'est un indice solide, pas encore une
preuve. » Trois corrections et une addition.

1. **L'indice est plus faible qu'ecrit.** Le contraste de groupe passe de plus 0,356 avec
   p = 0,0009 sur le score fabrique de a28 a plus 0,176 avec p = 0,047 sur les ampleurs
   publiees, et il disparait des que la couverture s'elargit [MESURE, section 2.2]. La
   phrase « vrai en bloc » reste vraie, mais elle tient a une valeur a la frontiere de 5
   pour cent, sur 21 items dont 16 sont des items de depense.
2. **« La ou les humains se surveillent » ne peut plus s'ecrire.** Le contraste est entier
   sur les attitudes, p = 0,0012, et nul sur les comportements declares, p = 0,77, alors
   que la desirabilite mesuree contre verite terrain est un phenomene de comportement
   verifiable [MESURE, section 3.2]. La formulation exacte est : la simulation devie la ou
   NORC a mesure que la distribution bouge avec le mode, et cette deviation est un
   phenomene d'attitude.
3. **L'option A gagne une jambe et elle est solide.** `ARBITRAGE.md` defend la phrase « une
   societe simulee a partir d'etiquettes remplace chaque personne par son groupe ». a38 en
   donne la version chiffree la plus propre du projet : sur 29 items ideologiques a bit
   documente, les conditions riches et C2 exagerent l'ecart entre camps d'un facteur 1,6 a
   3,2, tous les predicteurs statistiques a etiquette sont entre 0,97 et 1,24, les memes
   humains reinterroges sont a 0,98, et le passage de C2 a C3 fait tomber le facteur de
   1,62 a 0,52 par le seul retrait de l'etiquette [MESURE, section 4.4]. **Ces tests
   passent Holm sur la famille de 52 declaree d'avance**, ce qu'aucun test de a25 ni de a28
   n'avait fait.
4. **A ajouter a la liste « ce qui est tombe ».** L'idee que le confondant de conception
   d'item, la modalite volontaire de MR141, expliquerait une part du resultat de a25.
   Mesure : la correlation est negative pour neuf methodes sur treize et n'est pas plus
   forte chez les modeles de langage [MESURE, section 2.3]. L'objection est levee.
5. **La question ouverte de la nuit de calcul se precise.** Kahan et ses coauteurs
   predisent que la capacite renforce la conformite au groupe. Le facteur d'amplification
   de la section 4.4 est la quantite exacte a rejouer sur un modele plus gros : la
   prediction dirigee est qu'il monte au dessus de 1,62.

---

## Ce que je n'ai pas pu verifier

1. **Vingt et un items sur 149 ont une ampleur de mode, et seize d'entre eux sont des items
   de depense.** La version continue de T1 est en pratique un test sur la famille `nat*`.
   Les deux controles qui auraient departage, « attitudes seules » et « sans les depenses »,
   tombent a 16 et 5 items, sous le seuil de calcul. **La version continue n'a pas la
   puissance de conclure et ce rapport ne conclut pas.**
2. **Huit des douze items sensibles de NORC n'ont aucune ampleur publiee**, dont les quatre
   qui portent le resultat de a25 sur les items nominaux, `spkrac/y`, `polabuse/y`,
   `polattak/y`, et `attend`. Les obtenir demande le recalcul sur microdonnees du GSS 2022,
   qui n'est pas fait ici.
3. **Les trois familles d'ampleur ne mesurent pas la meme chose.** M2 et M3 melangent un
   contraste de mode, un effet de conception d'item et un changement de regime de reponse.
   Ils sont rapportes comme controles et jamais comme mesure principale, mais le lecteur
   qui juge M1 trop etroit et M3 incoherent a raison sur les deux points.
4. **MR086 n'a ete depouille que par son corps de texte.** Les tables 2, 4 et 5 donnent des
   niveaux de probabilite par item, mais la numerisation du PDF ne permet pas de rattacher
   a coup sur une valeur a sa ligne. Un seul item en sort, `health`. MR021 a la meme
   limite, deja signalee par la lecture 04.
5. **Le bit de pole d'endogroupe repose sur une loi generale appliquee item par item.** La
   position typique des camps sur ces 29 items est etablie par Cohen 2003, Barber et Pope
   2019 et Crandall et al. 2002 comme une loi, pas comme une mesure sur ces items la. Elle
   est verifiee a posteriori sur les humains, 28 sur 29, ce qui est un controle et non une
   preuve d'anteriorite : le bit a ete ecrit avant la verification, le journal de session
   le montre, et la seule verification possible pour un tiers est la lecture du code.
6. **Le controle par identification partisane n'est pas fait.** a30 etablit que `polviews`
   a une fiabilite de 0,66 contre 0,84 pour `partyid`, et que le changement d'ancrage est
   le controle le plus important. K4 n'emploie que la partition `bloc3` sur l'ideologie.
   C'est la premiere chose a ajouter.
7. **Les camps du perimetre 150 comptent 63, 45 et 42 personnes.** Les intervalles de C2 et
   C3 en portent la trace, ils sont deux a quatre fois plus larges que ceux des conditions
   de Stanford. Le perimetre 1 052 confirme le motif mais ne contient ni C2 ni C3.
8. **Le facteur d'amplification est une quantite nouvelle et non validee ailleurs.** Il est
   defini ici, il a un plancher et un plafond interpretables, et le controle humain le
   calibre a 0,98. Il n'a jamais servi ailleurs dans la litterature et personne ne l'a
   critique.
9. **`agents v6` et `agents v7` sous reproduisent l'ecart entre camps alors qu'elles ont
   l'etiquette.** Aucune explication n'est etablie ici. C'est le fait le plus genant du
   volet K4 pour la lecture « c'est l'etiquette qui produit la caricature ».
10. **Rien n'est teste sur Twin-2K-500 ni sur le WVS.** Les ampleurs NORC n'existent que
    pour le GSS, et la partition par camp de a30 existe pour les deux, donc K4 est
    transposable et n'a pas ete transpose.
11. **L'ampleur de `vote16` vaut 10,0 points par MR021 et 3,0 par l'atlas.** Les deux sont
    conservees dans `a38-ampleurs-items.csv` et la priorite declaree retient MR021, parce
    qu'il mesure sur le GSS. L'ecart de 7 points entre deux sources sur le meme
    comportement est la meilleure illustration de la fragilite du score continu.
12. **Les prompts de C2 et C3 n'ont toujours pas ete compares a ceux de l'archive de
    Stanford**, limite ouverte depuis a17.

---

## Questions ouvertes pour Simon

1. **Le facteur d'amplification par camp doit il devenir la mesure principale du projet ?**
   C'est la seule quantite mesuree jusqu'ici qui separe les modeles de langage des
   predicteurs statistiques **au niveau de chaque condition**, qui a un plancher et un
   plafond interpretables, qui est calibree par un controle humain a 0,98, et dont les
   tests passent une correction declaree d'avance. Les mesures de a25, a28 et a30 ne font
   aucune de ces quatre choses.
2. **Faut il retirer de `ARBITRAGE.md` la formule « la ou les humains se surveillent » ?**
   Le contraste est nul sur les comportements verifiables, qui sont le seul endroit ou la
   litterature etablit que les humains se surveillent. Garder la formule expose a une
   objection directe et documentee ; la remplacer coute une phrase.
3. **Que faire de `agents v6` et `agents v7` ?** Elles ont l'etiquette et elles
   sous reproduisent l'ecart entre camps, a 0,29 et 0,39, contre 1,6 a 3,2 pour les quatre
   conditions riches. Soit la caricature vient de la richesse du persona et non de
   l'etiquette seule, soit ces deux conditions ont un defaut propre. C'est un travail d'une
   heure sur les traces de l'archive et il change l'enonce.
4. **Faut il rejouer K4 sur `partyid` avant d'en parler ?** a30 a fait de ce controle sa
   regle. Une heure de calcul, aucun appel de modele.
5. **La version continue de T1 vaut elle d'etre poursuivie ?** Elle a coute la lecture de
   six rapports et elle rend 21 items dont 16 de depense, un p de 0,047 sur le contraste de
   groupe, et rien au niveau des conditions. La seule facon de la sauver est le recalcul des
   ecarts de mode sur les microdonnees du GSS 2022, deja pose en question ouverte 2 de a25.
   Est ce que cela vaut la nuit de calcul, sachant que K4 tient sans ?
6. **Le contraste de groupe post hoc doit il continuer a etre rapporte ?** Il porte le
   resultat de a28 et il porte encore le peu qui reste de K1. Sa limite est la meme depuis
   a28 : les 13 methodes ne sont pas des unites echangeables. Il faudrait soit le
   pre enregistrer pour la suite, soit cesser de s'appuyer dessus.

---

## Rejouer

```
A38_PDF_DIR=<repertoire des PDF> .venv/bin/python analyses/a38_extraire_norc.py
.venv/bin/python analyses/a38_ampleurs.py
.venv/bin/python analyses/a38_mesures.py --cache /tmp/a25-matrices.pkl \
    --cache-foret /tmp/a28-foret.npy
.venv/bin/python analyses/a38_tests.py --tirages 20000
.venv/bin/python analyses/a38_figure.py --perimetre 150
```

Sans les caches de a25 et de a28, `a38_mesures.py` recalcule les baselines et la foret,
environ cinq minutes ; avec les caches, quatre secondes. `a38_tests.py` prend trente
secondes, la figure trois. Graine 20260908 partout. Aucun appel de modele, aucune ecriture
hors de `resultats/` et de `data/norc-mode/`.
