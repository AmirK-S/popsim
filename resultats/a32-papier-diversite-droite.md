# a32. Le papier derriere l'image « plus de diversite de pensee a droite »

Date : 2026-09-08. Statut : papier identifie et lu en entier (version preprint auteur,
25 pages, identique en substance a la version publiee). Aucun fichier existant modifie.

---

## 0. Identification

L'image de Reddit est la **Figure 2** de :

> Adrian Lüders, Dino Carpentras, Michael Quayle, *Attitude networks as intergroup
> realities : Using network-modelling to research attitude-identity relationships in
> polarized political contexts*, **British Journal of Social Psychology** 63(1), 2024,
> 37-51. DOI [10.1111/bjso.12665](https://doi.org/10.1111/bjso.12665). Mise en ligne
> 2023-07-11. PMID 37431984.
> Preprint libre : PsyArXiv, DOI [10.31234/osf.io/apkzv](https://doi.org/10.31234/osf.io/apkzv),
> telechargeable sur `https://osf.io/download/apkzv/`.
> Materiel supplementaire, code et donnees : `https://osf.io/345yv/`.

[CONFIRME, preprint p. 16, legendes de la Figure 2] Les trois libelles de l'image
correspondent mot pour mot au texte du papier :

> « Figure 2: Extracted Attitude Network »

> « Figure 2a: A visual representation of the extracted attitude space revealing a
> distribution of forty attitudes into two clusters. Note: Dark Blue = Strong
> Disagreement; Pale Blue = Moderate Disagreement; Grey = Neutral; Orange = Moderate
> Agreement; Red = Strong Agreement. »

> « Figure 2b: Two attitude clusters depicting latent Democrat (blue) and Republican
> (red) belief-sets. »

**Le titre de l'image n'est pas du papier.** [CONFIRME, recherche plein texte OpenAlex
sur `"more diversity of thought on the political Right"`, 0 occurrence dans l'ensemble
du corpus indexe ; et lecture integrale du preprint] La phrase « There is more diversity
of thought on the political Right than on the political Left. Although they pride
themselves on open-mindedness, liberal thinking actually coalesces around a very narrow
set of opinion, whereas the Right diverges widely » n'apparait nulle part dans le
papier. C'est une glose ajoutee par celui qui a poste l'image. Le papier dit
explicitement le contraire de cette glose (section 4 ci dessous).

Deux papiers du meme groupe complètent le dossier et ont ete lus egalement :

- **Papier de methode.** Dino Carpentras, Adrian Lüders, Michael Quayle, *Response Item
  Network (ResIN) : A network-based approach to explore attitude systems*, **Humanities
  and Social Sciences Communications** 11:589, 2024. DOI
  [10.1057/s41599-024-03037-x](https://doi.org/10.1057/s41599-024-03037-x). Acces libre.
- **Papier de mesure longitudinale.** Yijing Chen, Anne Speer, Bart de Bruin, Dino
  Carpentras, *A « Broken Egg » of U.S. Political Beliefs : Using Response-Item Network
  (ResIN) to Measure Ideological Polarization*, preprint OSF
  [10.31219/osf.io/autkb](https://doi.org/10.31219/osf.io/autkb), 2024-2025, egalement
  depose ETH Zurich (`10.3929/ethz-c-000790335`).

Aucun des trois n'est present dans `corpus/05` (verifie par grep sur ResIN, Lüders,
Carpentras, Quayle). C'est de la matiere nouvelle pour le dossier.

---

## 1. Quelles donnees

Deux jeux, un principal et une replication.

**Echantillon principal.** [CONFIRME, preprint p. 11] N = 402 recrutes sur Prolific
Academic, 6 exclus a un controle d'attention, **N = 396 effectifs**. Criteres :
resident americain, 18 ans et plus, anglophone natif, soutien declare aux Democrates,
Republicains ou Independants, 98 % d'approbation prealable. 50,5 % hommes, 48,7 %
femmes, 0,8 % non binaires ; 83,6 % blancs ; age moyen 34 ans (ET 11,7).

Point capital pour la suite : **58,1 % se declarent Democrates, 28 % Independants,
13,9 % Republicains**, soit environ 55 Republicains dans l'echantillon. Les auteurs
reponderent par des poids Gallup 2021 et notent en note de bas de page :

> « Running the analysis without re-weighting the sample produces qualitatively similar
> results. »

**Items.** [CONFIRME, Online Supplementary A.1, telecharge depuis OSF] Huit items,
echelle de Likert a 5 points, de « strong disagreement » a « strong agreement » :

1. Abortion should be illegal.
2. The government should take steps to make incomes more equal.
3. All unauthorized immigrants should be sent back to their home country.
4. The federal budget for welfare programs should be increased.
5. Lesbian, gay and trans couples should be allowed to legally marry.
6. The government should regulate business to protect the environment.
7. The federal government should make it more difficult to buy a gun.
8. The federal government should make a concerted effort to improve social and economic
   conditions for African Americans.

[CONFIRME, papier de methode HSSC 2024, p. 8] Six des huit items sont ecrits de sorte
que « Strongly agree » soit la position democrate ; les deux autres sont inverses a la
redaction puis **recodes apres collecte** pour homogeneiser :

> « Of these 8 items, 6 were written in such a way that the answer "Strongly agree" was
> more associated with a Democrat position and "Strongly disagree" with a Republican
> position. The remaining 2 items instead were inversely coded to prevent respondents
> from simply providing the same answer to all 8 items. After data collection, we
> inverted those two items, to obtain consistent patterns. »

Dans le BJSP le recodage va dans l'autre sens : « All items were (re)coded so that
disagreement referred to liberal positions and agreement to conservative positions ».
La couleur de la Figure 2a code donc un niveau de reponse **apres recodage**, pas une
position brute.

**Autres mesures.** Identification partisane par items uniques sur 7 points ;
thermometres de sentiment 1 a 100 envers Democrates, Republicains, Independants ; biais
de groupe = thermometre Democrate moins thermometre Republicain.

**Etude par vignettes.** 40 vignettes (8 items x 5 options de reponse), 8 tirees au
hasard par participant, chacune suivie d'une categorisation (100 points) et d'un
thermometre.

**Replication.** [CONFIRME, preprint p. 19] ANES 2020, **N = 8 280**, echantillon
representatif de la population adulte americaine, huit items proches, essentiellement
la vague pre electorale, deux items venant de la vague post electorale. Codes ANES
donnes dans le supplementaire : V201336 (avortement), V202257 (reduction des ecarts de
revenus), V201417 (immigres sans papiers), V201312 (depenses d'aide sociale), V201262
(regulation environnementale des entreprises), V202337 (achat d'armes), V201258 (aide
aux Noirs). Ces items ANES n'ont pas le meme nombre de modalites que les items maison,
ce que les auteurs signalent : « the ANES items presented different (ordinal) options ».

---

## 2. Quelle methode exacte

La methode s'appelle **ResIN**, Response-Item Network. Elle n'est pas de ce papier ci,
elle vient de Carpentras, Lüders et Quayle 2021-2024.

**Noeuds.** [CONFIRME, preprint p. 14 « Network Modelling »] Un noeud n'est pas un item,
c'est **une modalite de reponse a un item**. Chaque position d'echelle est encodee en
variable indicatrice :

> « we dummy-coded each scale position (i.e., response-option) in the original dataset.
> This resulted in a new dataset in which each column reflects a different item (e.g.,
> "gun control:strongly agree") and each row a different participant. »

8 items x 5 modalites = **40 noeuds**. C'est la difference structurante avec la Belief
Network Analysis de Boutyline et Vaisey (present dans `corpus/05` sous 05-48), ou un
noeud est un item et une arete une correlation entre items.

**Aretes.** [CONFIRME, preprint p. 14, formule explicite] Coefficient phi de Guilford
1941 entre deux colonnes binaires :

phi(i,j) = ( n11 n00 moins n10 n01 ) / racine( n1. n0. n.1 n.0 )

C'est le coefficient de Pearson applique a deux binaires. Les paires de modalites du
**meme item** sont exclues, puisque mutuellement exclusives. Dans le papier de methode
et dans le papier « Broken Egg », seules les associations **positives** sont retenues
comme poids d'arete ; le notebook d'analyse depose sur OSF contient bien une fonction
`pears_pos` qui ramene a zero toute correlation negative.

**Disposition spatiale.** [CONFIRME, preprint p. 14] Algorithme dirige par les forces de
NetworkX (Hagberg et al. 2008, c'est a dire Fruchterman-Reingold) : les aretes sont des
ressorts, les noeuds se repoussent. Le papier « Broken Egg » ajoute une ACP sur les
coordonnees obtenues pour aligner la dimension principale sur l'axe X, puis colore les
noeuds par le penchant partisan moyen des repondants qui ont choisi cette modalite.

**Position d'une personne.** [CONFIRME, preprint p. 17] La position d'un individu est la
**moyenne des coordonnees des 40 noeuds correspondant a ses 8 reponses**, sur un axe X
normalise de -1 a +1.

**Et la mesure de diversite, alors ?** C'est le point decisif de ta question.

[CONFIRME, preprint p. 15] **Il n'y en a aucune.** Le constat d'un amas democrate
compact et d'un nuage republicain etale est obtenu **par inspection visuelle**, sans
statistique :

> « Figure 2a depicts the extracted attitude network. A visual inspection of the network
> reveals two attitude clusters. »

> « the cluster reflecting the Democrat belief-system almost exclusively contained
> extreme attitudes as indicated by strong disagreement with each of the eight items.
> Conversely, the cluster reflecting the Republican belief-system contained a wider
> range of attitude responses ranging from mild disagreement to maximum agreement. »

Pas de dispersion calculee, pas de densite de reseau, pas de nombre de clusters teste,
pas d'entropie, pas d'intervalle de confiance sur l'ecart entre les deux amas. Les
seules statistiques du papier portent sur **autre chose** (voir section 3). Le nombre de
clusters n'est meme pas estime ici : c'est dans le papier de methode HSSC que la
partition en deux est confirmee, par modularite de Louvain sous Gephi.

Les seules mesures quantitatives de « dispersion des camps » de toute cette
litterature sont dans le papier « Broken Egg », et elles ne disent pas ce que dit la
glose de Reddit (section 4).

---

## 3. Quel resultat chiffre et sa robustesse

Ce qui est chiffre dans le papier :

| Hypothese | Resultat, echantillon Prolific N=396 | Replication ANES 2020 N=8280 |
|---|---|---|
| H1 position reseau vs identification partisane | r = 0,72, p < 0,001 | r = 0,73, p < 0,001 |
| H2 position reseau vs biais de groupe affectif | r = 0,73, p < 0,001 | r = 0,79, p < 0,001 |
| H3 position d'une attitude vs categorisation d'autrui | r = 0,90, p < 0,001 | non refait |
| H4 divergence attitudinale vs evaluation affective | r = 0,49, p < 0,001 | non refait |

[CONFIRME, preprint p. 18-20]

Ces quatre correlations sont fortes et pre enregistrees. **Aucune ne mesure la diversite
d'un camp.** Elles mesurent que la geometrie du reseau capte bien l'identite partisane,
ce qui est la these du papier.

**Ce qui est dit de l'asymetrie, et rien de plus.** [CONFIRME, preprint p. 19, robustness
check] :

> « The obtained network (Figure 4) was comparable to the one we obtained based on our
> own sample with a tighter Democrat cluster of mainly extreme attitudes and a looser
> Republican cluster with moderate to extreme viewpoints. »

C'est la seule replication de l'asymetrie, et elle est encore une fois **qualitative**.

**Robustesse : ce qui manque.**

- **Taille d'effet : aucune.** Pas de statistique d'ecart entre les deux amas.
- **Intervalle de confiance : aucun** sur cette comparaison. Le papier « Broken Egg »,
  lui, produit des IQR par 200 reechantillonnages a 80 % ; ce papier ci ne le fait pas.
- **Sensibilite au choix des items : non testee.** Or les auteurs eux memes posent en
  note de bas de page 4 :
  > « "Extremity" should thereby be understood as a function of both, the formulation of
  > the item and the response. »
  Deux des huit items ont ete recodes apres coup, et six sur huit ont leur pole
  democrate du meme cote. [HYPOTHESE] Un dispositif ou six items sur huit pointent dans
  la meme direction fabrique mecaniquement un pole « tout en desaccord fort » tres dense
  du cote qui repond de facon coherente, et laisse l'autre cote occuper tout le reste de
  l'espace. L'asymetrie observee pourrait etre en partie une propriete du questionnaire.
- **Composition demographique des camps : non controlee.** Aucun modele avec covariables,
  aucune stratification par age, sexe, education ou race. La seule correction est la
  reponderation Gallup des trois groupes partisans.
- **Desequilibre d'effectif non traite.** [HYPOTHESE, mienne, non testee par les auteurs]
  Avec 13,9 % de Republicains, soit environ 55 personnes, les coefficients phi
  impliquant des modalites majoritairement republicaines sont estimes sur beaucoup moins
  de repondants que ceux du cote democrate. Des phi plus bruites et en moyenne plus
  faibles donnent des ressorts plus faibles, donc un placement plus disperse par
  l'algorithme dirige par les forces. **Un nuage plus etale du cote minoritaire est
  exactement ce qu'un bruit d'echantillonnage produirait.** La replication ANES 2020, ou
  les deux camps sont bien peuples, affaiblit cette objection sans l'annuler : il reste
  a verifier si le meme deficit d'effectif joue par modalite.
- **Fidelite test retest de la forme du reseau : jamais mesuree** dans aucun des trois
  papiers.
- **Reproductibilite de l'algorithme : bien etablie**, elle. [CONFIRME, HSSC 2024, p. 11]
  50 simulations, 1 250 correlations entre relances de l'algorithme dirige par les forces
  sur le meme reseau : correlation moyenne des coordonnees X **0,99985**, ecart type
  2e-16. Le placement n'est pas un artefact de graine aleatoire.
- **Validite de la coordonnee X : forte.** [CONFIRME, HSSC 2024, p. 8-10] La position X
  d'un noeud correle a **r = 0,97 (p < 1e-27)** avec la moyenne de la courbe
  caracteristique d'item issue d'une analyse IRT sur les memes donnees ; sur 100
  simulations avec modele gradue, ResIN est plus proche de l'IRT que le positionnement
  multidimensionnel dans **98 %** des cas (correlations respectives 0,976 et 0,941 sur
  donnees reelles). Autrement dit : **la methode est solide, c'est la lecture
  « diversite » qui ne l'est pas.**

---

## 4. Face a `corpus/05` : contradiction, autre mesure, ou autre population ?

**Ce n'est pas une contradiction. C'est une autre mesure, sur une autre population, et le
papier lui meme refuse la lecture que Reddit lui prete.**

**a. Le papier desavoue explicitement la glose.** [CONFIRME, preprint p. 24, discussion] :

> « The pattern does not imply that Republicans are more tolerant than Democrats, nor
> that Republicans could deal better with attitudinal uncertainty. It does imply,
> however, that -at this particular moment in time- Democrats and Republicans are
> constructing and managing their partisan identities differently in relation to the
> topics reflected in these questionnaire items. »

Trois restrictions dans une seule phrase : pas de tolerance, pas de gestion de
l'incertitude, et « at this particular moment in time ». La glose de Reddit transforme
un constat de structure identitaire, date et lie a huit items, en trait cognitif stable
des deux camps. C'est un saut que les auteurs interdisent.

**b. Le papier explique l'asymetrie par le symbolique, pas par le cognitif.** [CONFIRME,
preprint p. 24] Les auteurs renvoient a Mason et Wronski 2018 : l'appartenance
categorielle (blanc, chretien) compte davantage pour la construction de l'identite
republicaine, donc on peut etre republicain avec des vues liberales sur le mariage gay.
**C'est exactement la lecture deja retenue par `corpus/05`** dans sa synthese, a propos
de 05-03 : « les auteurs l'attribuent a la desirabilite differentielle des deux
etiquettes, pas a une difference cognitive ». Le nouveau papier ne renverse pas cette
lecture, il l'appuie avec un autre outil.

**c. Le sens de la mesure d'origine est le meme, et de meme faible ampleur.**
`corpus/05` a deja 05-03 (Treier et Hillygus 2009) : 38 % des conservateurs declares
sortent de leur quadrant contre 35 % des liberaux. Un ecart de trois points de
pourcentage, dans le sens d'une droite un peu plus heterogene. La Figure 2 de Lüders et
al. est la meme famille de fait, en image et sans chiffre.

**d. Et sur la mesure quantitative, la direction s'inverse selon l'annee.** C'est le
resultat le plus important de tout ce rapport. [CONFIRME, Chen, Speer, de Bruin et
Carpentras, « Broken Egg », section 4.2 et conclusion] Sur cinq items communs aux six
vagues ANES 2000, 2004, 2008, 2012, 2016 et 2020, avec IQR par 200 reechantillonnages a
80 % :

> « we identify an intriguing partisan asymmetry in belief system constraint, with
> Democrats' belief systems generally appearing less coherent than that of Republicans
> during this period - a pattern that only recently reversed in 2020. »

> « Compared to its Republican counterpart, the Democratic subgraph generally showed a
> lower link density, with the exception of 2020. [...] Subgraph density among
> Republicans peaked out early on in 2008, with the density level continuously declining
> from 2008 to 2020. »

Densite globale du reseau : de 0,032 a 0,049, soit **+51,1 % de 2000 a 2020**, avec le
saut le plus fort entre 2016 et 2020.

Traduction. La densite de liens d'un sous graphe partisan est l'inverse d'une mesure de
diversite : plus c'est dense, plus les attitudes du camp sont verrouillees ensemble. De
2000 a 2016, c'est le sous graphe **republicain** qui est le plus dense, donc le moins
divers. **2020 est la premiere annee ou l'ordre s'inverse.** Or Lüders et al. utilisent
precisement l'ANES **2020** pour leur replication, et un echantillon Prolific collecte
en 2021-2022.

Conclusion pour le dossier : **la Figure 2 est un instantane pris dans la seule annee
ou l'asymetrie va dans ce sens la, et la meme equipe montre par ailleurs qu'elle allait
dans l'autre sens les seize annees precedentes.** La proposition « la droite est plus
variee » n'est pas un fait structurel ; c'est une valeur de 2020 sur cinq items ANES.

**e. Consequence sur `corpus/05`.** Rien a corriger dans la synthese existante. La
phrase « Aucune asymetrie ne peut etre postulee dans notre protocole » tient, et sort
renforcee : on dispose maintenant d'une serie temporelle qui change de signe. Ce qui
change, c'est qu'on gagne trois entrees et surtout **un instrument** (ResIN plus densite
de sous graphe) applicable a nos propres donnees.

---

## 5. Reproductible chez nous ? Oui, et sur les deux jeux

La methode est simple a ecrire : encodage disjonctif, phi par paires hors item, filtrage
des phi negatifs, Fruchterman-Reingold, ACP de rotation, densite par sous graphe. Le
notebook des auteurs (`Analysis_code.ipynb`, OSF 345yv, telecharge et lu) est du Python
pur avec `networkx`, `scipy.stats`, `pandas` et `matplotlib`, plus un `import winsound`
qui echoue hors Windows et qu'il faudra retirer. Il existe aussi un paquet R officiel :
**CRAN `ResIN` 2.3.1**, 2026-03-13, par Warncke, Carpentras et Lüders, avec une vignette
« Getting started with ResIN ». Nos analyses etant en Python, reecrire les 60 lignes est
plus rapide que d'ajouter une dependance R.

### 5.1 GSS, correspondance des items

[CONFIRME, inspection de `data/gss-panel/gss2020panel_r1a.dta`, 4 296 variables, suffixes
`_1a`, `_1b`, `_2` pour les trois vagues du panel 2016-2020] Les huit items du papier
ont presque tous un homologue GSS :

| Item du papier | Variable GSS | Modalites |
|---|---|---|
| 1. Abortion should be illegal | `abany`, `abnomore`, `abrape` | binaires oui/non |
| 2. Government make incomes more equal | `eqwlth` | 7 points |
| 3. Send unauthorized immigrants home | `letin1a` | 4 points |
| 4. Increase welfare budget | `natfare`, `natfarey` | 3 points |
| 5. Gay couples allowed to marry | `marhomo` | 5 points, Likert |
| 6. Regulate business for environment | `natenvir`, `natenviry` | 3 points |
| 7. Harder to buy a gun | `gunlaw` | binaire |
| 8. Improve conditions for African Americans | `helpblk` (5 pts), `natrace` (3 pts) | 5 ou 3 points |
| Identification partisane | `partyid` | 7 points, 0 = Strong Democrat a 6 = Strong Republican |
| Ideologie declaree | `polviews` | 7 points |

Deux reserves. D'abord, l'heterogeneite du nombre de modalites (2, 3, 4, 5 et 7 points)
est un probleme reel : le nombre de noeuds par item varie de 2 a 7, et le degre moyen
d'un noeud depend mecaniquement du nombre de modalites de son item. Les auteurs de
« Broken Egg » vivent avec ce probleme sans le corriger. Chez nous il faut au minimum
une variante a nombre de modalites egalise. Ensuite, `abany` et `gunlaw` etant binaires,
la finesse ordinale qui fait tout l'interet de ResIN disparait sur ces deux items.

**Atout propre au GSS panel :** trois vagues sur les memes personnes. On peut mesurer la
**fidelite test retest de la forme du reseau**, ce qu'aucun des trois papiers ne fait.

### 5.2 Twin-2K-500, correspondance quasi parfaite

[CONFIRME, `data/twin2k500/question_catalog_and_human_response_csv/question_catalog.json`
et `wave4_response_label.csv`] C'est le meilleur terrain des deux.

- **QID287**, bloc « False consensus », question « Would you support or oppose... »,
  **matrice de 10 items** sur une echelle a **5 points** : « Strongly oppose », « Somewhat
  oppose », « Neither oppose nor support », « Somewhat support », « Strongly support ».
  Colonnes `QID287_1` a `QID287_7`, `QID287_10`, `QID287_11`, `QID287_12`. Contenu :
  taxe carbone, 40 % des investissements energie propre vers les communautes pauvres,
  electricite sans carbone en 2035, Medicare for All, option publique, voie vers la
  citoyennete pour les sans papiers, conge parental obligatoire, taxe de 2 % au dessus
  de 50 millions de patrimoine, augmentation des expulsions, bons de sante pour les
  seniors en remplacement de Medicare.
  **10 items x 5 modalites = 50 noeuds**, contre 40 chez les auteurs, avec la meme
  structure exacte d'echelle.
- **QID20**, « In politics today, do you consider yourself a » : Republican, Democrat,
  Independent, Something else.
- **QID22**, « In general, would you describe your political views as » : Very
  conservative a Very liberal, 5 points.
- **N = 2 058** repondants humains.
- Repartition partisane : **847 Democrates, 540 Republicains, 609 Independants, 62
  autres**. Bien plus equilibree que les 58,1 / 13,9 du papier. **C'est ce qui permet de
  trancher l'hypothese du bruit d'echantillonnage de la section 3.**
- **QID287 est pose en vague 1-3 et en vague 4**, sur les memes personnes. On a donc
  deux reseaux du meme groupe a deux moments : test retest de la forme du reseau,
  gratuitement.
- Deux items sont inverses par construction (expulsions, bons de sante), ce qui permet
  de tester directement la sensibilite au recodage denoncee en section 3.

### 5.3 Code

Une seule fonction, environ 60 lignes, a poser en `analyses/a32_resin.py` :

```
1. charger le tableau de reponses individuelles (GSS ou Twin), coder DK / refus en NaN
2. encodage disjonctif : une colonne binaire par couple (item, modalite)
3. phi(i,j) pour toutes les paires de modalites d'items DIFFERENTS
   (phi sur binaires = scipy.stats.pearsonr sur les colonnes 0/1)
4. mettre a zero les phi negatifs, seuiller eventuellement, construire nx.Graph pondere
5. nx.spring_layout(G, weight='weight', seed=...) puis ACP pour aligner l'axe principal sur X
6. colorer chaque noeud par la moyenne du partyid (GSS) ou du code QID20 (Twin)
   des repondants qui ont choisi cette modalite
7. affecter chaque noeud a un camp selon la majorite qui l'endosse, puis calculer
   densite(sous graphe D) et densite(sous graphe R)
8. IC : 200 reechantillonnages de 80 % des repondants, IQR sur les deux densites
```

Points de vigilance a inscrire dans le script :

- **Filtrer les phi negatifs change le resultat.** A faire dans les deux variantes.
- **Egaliser le nombre de modalites par item** dans au moins une variante, sinon la
  densite depend du questionnaire.
- **Reponderer, ou non**, et publier les deux.
- **Controler le desequilibre d'effectif** : reechantillonner les deux camps a effectif
  egal avant de comparer les densites. C'est le test qui manque au papier.
- Ne jamais rapporter une conclusion tiree d'un simple regard sur le graphe. C'est
  precisement la faute de la Figure 2.

---

## 6. Ce que cela permet de tester sur les simulations

L'intuition de la mission est juste, et elle devient un protocole exploitable. Mais elle
demande d'etre reformulee, parce que la premisse « la droite est plus variee » n'est pas
un fait acquis (section 4d).

**Le bon enonce n'est pas « la droite est plus variee ». C'est : les deux camps humains
ont des geometries d'attitudes differentes, et cette difference change de signe selon
l'annee et selon la mesure. Une simulation qui part d'une etiquette partisane devrait
detruire cette difference, quelle qu'en soit la direction.**

Trois tests, du plus simple au plus severe.

**T1. Le ratio de densite par camp.** Calculer sur les humains les deux densites de
sous graphe, D et R, et le ratio densite(D) / densite(R). Refaire l'operation sur les
agents. `a1`, `a6` et `a18` mesurent deja un ratio de dispersion agents sur humains,
mais **globalement** ou par axe. Ici la quantite est **par camp** et **relationnelle**,
donc insensible a un simple retrecissement uniforme des reponses. Prediction, en
prolongement de la double distorsion : les agents devraient produire un ratio plus
proche de 1 que les humains, c'est a dire **effacer la difference de geometrie entre
camps**, tout en sur separant les deux amas le long de l'axe X.

**T2. L'occupation du centre.** [CONFIRME, preprint p. 23] Le papier note que les
modalites neutres tombent du cote republicain :

> « because neutral issue positions are largely embedded into the Republican
> belief-system (rather than being equally distributed between Republicans and
> Democrats), they may get "pulled over" to the Republican extreme. »

C'est une observation testable directement. Chez les humains, ou vont les modalites
« Neither oppose nor support » de QID287 ? Chez les agents etiquetes ? **Prediction
forte : un agent qui recoit une etiquette partisane place les modalites neutres au
milieu, symetriquement, parce qu'il derive ses reponses du stereotype de l'etiquette et
non d'une position vecue.** Si on observe cela, on a une signature d'ecrasement qui ne
se voit sur aucune de nos mesures actuelles, puisque les moyennes par item peuvent etre
justes pendant que la geometrie est fausse.

**T3. Le test decisif, sans etiquette contre avec etiquette.** La condition C3 du
protocole (sans etiquette) contre C2 (avec etiquette). Mesurer T1 et T2 dans les deux.
Si l'ecrasement de la difference entre camps est plus fort en C2 qu'en C3, alors
**l'etiquette est bien le mecanisme**, et non le modele. C'est la version geometrique de
ce que `a18` decompose deja en C2 et C3 sur la variance.

Un piege a eviter : ResIN est asymetrique par construction dans le sens ou il ne
suppose pas que les deux camps ont la meme forme, ce qui est son interet, mais la
densite d'un sous graphe depend du nombre de noeuds affectes a ce camp. Si les agents
n'utilisent jamais certaines modalites, ces noeuds disparaissent et la densite bouge
pour une raison triviale. **Il faut rapporter, a cote de chaque densite, le nombre de
modalites effectivement utilisees.** C'est le meme diagnostic que `a6` fait deja sur les
items ordinaux.

---

## Ce que je n'ai pas pu verifier

1. **La version publiee du BJSP.** Wiley renvoie un 403, le depot institutionnel de
   l'Universite de Limerick et Figshare ne servent pas le PDF, et Europe PMC n'a pas le
   texte integral. J'ai lu la version preprint auteur de 25 pages, celle deposee sur
   PsyArXiv. Les figures, les chiffres, les legendes et les phrases de discussion citees
   ici en viennent. **Je n'ai pas pu verifier si la version publiee ajoute une section
   Limitations**, ce qui est plausible apres relecture par les pairs. Le preprint n'en a
   pas.
2. **L'image exacte de Reddit.** Je n'ai pas vu l'image. L'identification repose sur la
   correspondance mot pour mot des trois libelles que tu m'as transmis avec les legendes
   de la Figure 2 du papier. Cette correspondance est totale, y compris « forty
   attitudes », mais je ne peux pas exclure qu'un billet ait recadre ou recolorie la
   figure.
3. **L'origine de la phrase titre.** Je peux affirmer qu'elle n'est pas dans le papier.
   Je n'ai pas pu identifier **qui** l'a ecrite, faute de budget de recherche web
   (200 appels sur 200 consommes des le debut de la seance). Il reste donc possible
   qu'elle vienne d'un billet secondaire qui commente le papier, ou d'un simple
   commentaire de posteur.
4. **Les valeurs numeriques exactes des densites par camp du papier « Broken Egg ».**
   Elles sont dans la Figure 7, que `pdftotext` ne rend pas. J'ai les bornes d'axe
   (environ 0,04 a 0,10 pour les sous graphes) et le texte qui donne le sens de
   l'ecart et l'annee de l'inversion, mais pas les six couples de valeurs.
5. **Le statut de publication du « Broken Egg ».** Preprint OSF plus depot ETH Zurich,
   avec deux versions (`autkb` et `autkb_v2`). Je n'ai pas verifie s'il est passe en
   revue. Ses resultats sont donc [CONFIRME] quant a ce que le texte dit, mais le texte
   n'est pas arbitre.
6. **L'appendice B du papier**, qui liste les positions d'items par amas, existe dans le
   supplementaire mais je n'en ai extrait que la partie A.1 et les notes de figure ; les
   figures du supplementaire sont des images.
7. **L'hypothese du bruit d'echantillonnage** (section 3) est de moi et n'a ete testee
   par personne. Le test existe et il est peu couteux : c'est le point 4 des vigilances
   de la section 5.3.
8. **Je n'ai pas execute une seule ligne de ResIN.** Tout ce qui est ecrit en sections 5
   et 6 est un plan verifie sur la disponibilite reelle des variables dans
   `data/gss-panel` et `data/twin2k500`, pas un resultat.
