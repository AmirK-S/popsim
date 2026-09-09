# D1. Les donnees qui manquaient aux trois programmes : ce qui a ete obtenu cette nuit

Ecrit dans la nuit du 9 au 10 septembre 2026, en parallele de R1 et de i3b. Aucun appel de
modele de langage. Aucun fichier existant du depot n'a ete modifie. Livrables associes :
`resultats/d1-anes-appariement.csv`, `demandes/`, et quatre fichiers `PROVENANCE.md` dans
`data/`.

---

## Reponse en une ligne

**Sur les cinq donnees que MOONSHOTS declarait manquantes ou non verifiees, deux sont
telechargees et posees sur la machine cette nuit, les microdonnees du Survey of Consumer
Expectations avec leurs identifiants de panel et les donnees de croyance de second ordre
d'Ahler et Sood, une troisieme est acquise a moitie, le cote synthetique du repondant de
Westwood, et les deux qui restent, l'ANES et un fichier reel a contamination documentee,
n'etaient pas telechargeables cette nuit et ont chacune leur lettre ; en passant, le module
GSS de l'ANES, qui aurait donne l'appariement parfait aux 149 items, est vide de toute reponse
dans les fichiers publics de 2020 comme de 2024.** [CONFIRME]

---

## 1. Tableau de bord

| source | obtenu | volume | licence | ce que ca debloque | ce qu'Amir doit faire |
|---|---|---|---|---|---|
| Survey of Consumer Expectations, Fed de New York | **oui** | 194,5 Mo, 4 fichiers | conditions FRBNY, redistribution autorisee avec attribution | programme C, mois 1, version menages, en entier | rien pour commencer ; la lettre 02 ne leve qu'un point de jointure |
| Ahler et Sood 2018, replication | **oui** | 5,1 Mo | CC0 1.0 | programme A, le referent humain de croyance de second ordre | rien |
| Westwood 2025, PNAS, materiel OSF | **oui, cote synthetique** | 28 Mo, 27 923 reponses generees | depot public sans licence declaree | programme B, un fabricant adverse de plus, le plus dur | rien pour l'usage ; lettre 05 pour le cote humain |
| Codebooks ANES 2020, 2024 et cumulatif | **oui** | 5,7 Mo de PDF, 2,3 Mo de HTML | documentation publique via SDA Berkeley | l'appariement item par item, fait cette nuit | rien |
| Microdonnees ANES | **non** | | | programme A, version forte | **compte ANES, lettre 01** |
| Fichier reel a contamination documentee | **non** | | | programme B, mois 3 | **lettres 03 et 04** |
| Seconde population humaine hors Etats Unis | **non, mais deux voies ouvertes sans lettre** | | | programme B, mois 6, et programme C | **signer la declaration LISS, telecharger le BES** |

---

## 2. ANES

### 2.1 Le site est inaccessible depuis cette machine

`electionstudies.org` repond **HTTP 403 a toutes les requetes**, page d'accueil, `data-center` et
URL de fichier comprises, avec le challenge Cloudflare « Just a moment... Enable JavaScript and
cookies to continue ». Ni WebFetch ni curl avec en tete de navigateur complet ne passent.
[CONFIRME] Ce n'est pas une conclusion sur la politique d'acces de l'ANES, c'est un constat de
blocage reseau. La question « faut il un compte » reste donc **non verifiee a la source** ; la
lettre 01 la pose.

Deux voies de contournement ont ete examinees. La documentation officielle est servie sans
blocage par **SDA, UC Berkeley**, et c'est par la que tout le travail de cette nuit est passe.
Les microdonnees existent aussi dans le paquet R `anesr` de James Martherus, qui heberge
`timeseries_2020.rda` et `timeseries_cum.rda` sur GitHub [CONFIRME, API GitHub] : elles n'ont
pas ete telechargees, parce que c'est un miroir tiers non autoritatif, qu'il ne contient pas
2024, et que ni R ni `pyreadr` ne sont installes ici.

### 2.2 L'ANES 2024 existe

**ANES 2024 Time Series Study Full Release, 5 521 cas, publie le 8 aout 2025**, codebook HTML
produit le 8 septembre 2025. Et **ANES Cumulative Datafile 1948-2024, 73 745 cas, publie le
5 fevrier 2026**. [CONFIRME avec URL, https://sda.berkeley.edu/archive.htm]

### 2.3 Les items de placement existent et sont renseignes

C'est le point qui decide de la version forte du programme A, et la reponse est oui.

- **Placement des partis** sur l'echelle liberal-conservateur en 7 points : `V201206` et
  `V201207` en 2020, `V241183` et `V241184` en 2024, `VCF0503` et `VCF0504` dans le fichier
  cumulatif 1948-2024. Renseignes, avec des distributions qui portent deja le resultat attendu :
  en 2020, 79 pour cent des repondants placent le parti democrate en 1, 2 ou 3, et 82,9 pour
  cent placent le parti republicain en 5, 6 ou 7, contre une auto declaration ou 22 pour cent
  seulement se disent moderes et 14,5 pour cent n'y ont pas pense. [MESURE, codebook SDA
  `nes2020full`]
- **Placement gauche-droite CSES en 11 points** : `V202437` et `V202438` en 2020, `V242436` et
  `V242437` en 2024, `VCF9241` et `VCF9242` dans le cumulatif.
- **Placement sur les echelles d'enjeux** : il existe, mais **pour les candidats, pas pour les
  partis**, en 2020 comme en 2024. Sept echelles en 2020 : depenses et services, defense,
  assurance maladie, emploi et revenu garantis, aide aux Noirs, environnement contre emploi,
  avortement. L'ANES 2024 ajoute une echelle d'avortement en 7 points, `V241250` et `V241251`.
  Vingt deux items de placement de candidat au total, listes dans le CSV.
- **Ideologie et parti** : `V201200` auto placement en 7 points, `V201231x` identification
  partisane resumee en 7 points, `V202439` auto placement CSES, `V201228` question brute.

Consequence de conception : la comparaison a trois termes que le programme A promet, realite
contre croyance humaine contre croyance du modele, se fait **sur l'echelle liberal-conservateur
au niveau du parti**, et **sur les echelles d'enjeux au niveau du candidat**. Ce n'est pas la
meme cible. Demander a un modele ou se situe « le parti republicain » sur l'assurance maladie
n'a pas d'homologue humain dans l'ANES ; demander ou se situe « le candidat republicain » en a
un. C'est un choix a poser avant de lancer les appels, pas apres.

### 2.4 Le module GSS de l'ANES est vide

L'ANES 2020 contient un bloc de 61 variables, `V202575` a `V202635`, prefixees « GSS », qui
reprennent litteralement des items du GSS : les depenses par domaine, `natspac`, `natenvir`,
`natheal`, `natcity`, `natcrime`, `natdrug`, `nateduc` ; le bonheur ; la confiance dans la
medecine et dans la communaute scientifique. L'ANES 2024 en garde 14, `V242608` a `V242621`,
avec cette fois la confiance dans la Cour supreme, dans l'armee et dans la presse.

**Aucune de ces variables ne contient une seule reponse valide.** En 2020, les 8 280 cas se
repartissent entierement entre 77 entretiens supprimes, 754 sans post election, 103 interrompus
et 7 346 « Inapplicable ». En 2024, les modalites valides sont declarees dans le codebook mais
chacune a un effectif de zero, et les 5 521 cas tombent tous dans les codes negatifs. L'univers
declare est « IF R IS IN GSS SAMPLE ». [CONFIRME, codebooks SDA `nes2020full` et `anes2024full`,
verifie sur les tableaux de frequences]

Ce n'est pas un artefact de la version preliminaire : le constat est identique dans la version
preliminaire de juin 2021 et dans la version complete d'octobre 2021.

Ce que cela veut dire pour le programme A. L'appariement parfait, meme libelle, memes modalites,
memes personnes, existe sur le papier et n'existe pas dans les fichiers publics. Soit les
reponses sont dans un fichier GSS ou dans une publication conjointe, soit le module n'a jamais
ete administre. La lettre 01 pose la question ; c'est la seule question de la nuit dont la
reponse peut changer la forme du mois 1.

### 2.5 L'appariement, `resultats/d1-anes-appariement.csv`

177 lignes, cinq roles. Construit a partir des 149 items de `a30-gss-par-item.csv` d'un cote,
et des index de variables ANES extraits des codebooks SDA de l'autre, 1 771 variables pour 2020,
1 722 pour 2024, 1 030 pour le cumulatif.

Colonnes : `role`, `item_gss`, `famille_gss`, `item_anes`, `etude_anes`, `libelle_anes`,
`type_appariement`, `confiance`, `statut_donnees_anes`, `modalites_gss`, `modalites_anes`,
`note`.

Bilan sur les 149 items du GSS :

| confiance | nombre | lecture |
|---|---|---|
| identique | 12 | meme libelle, memes modalites, **mais vides** dans le fichier public |
| elevee | 12 | meme objet, recodage direct ou quasi direct |
| moyenne | 12 | meme concept, echelle ou instrument different |
| faible | 10 | concept voisin, format tres different |
| absent | 103 | aucun equivalent dans l'ANES 2020 ni 2024 |

Les 12 appariements a confiance elevee sont : `cappun` avec `V201345x` ; `marhomo` avec
`V201416` ; `fefam` avec `V202290x`, dont la formulation est quasi mot pour mot celle du GSS ;
`racdif4` avec `V202303` ; `discaff` avec `V202252x` ; `letin1a` avec `V202232`, meme echelle
dans le meme sens ; `attend` avec `V201453` ; `bible` avec `V201434` ; `reborn` avec `V201456` ;
`class` avec `V202352` ; `vote16` et `pres16` avec `V201102` et `V201103`.

Les 103 absents ne sont pas une surprise, ils sont une information : la batterie Stouffer de
libertes civiles, les onze items `spk*`, `col*`, `lib*`, n'a aucun equivalent ; la batterie de
confiance `con*` non plus, sauf par les quatre items du module GSS 2024, vides ; les cinq items
de fin de vie non plus ; la morale sexuelle non plus. **L'ANES n'est pas un GSS avec des
placements de partis en plus.** Le recouvrement utilisable est de 34 items sur 149, dont 12
seulement au niveau eleve, et il porte massivement sur les enjeux polarises, ce qui est
precisement le sous ensemble ou l'exageration attendue est la plus forte : le tableau du
programme A sera fait de bons items, mais d'un echantillon biaise d'items, et il faut le dire.

---

## 3. Survey of Consumer Expectations

**Obtenu, integralement, sans compte.** 194,5 Mo, quatre fichiers Excel plus le questionnaire du
module central. Empreintes et details dans `data/sce-fed-ny/PROVENANCE.md`.

Licence : conditions generales de la Federal Reserve Bank of New York, qui accordent
explicitement l'acces automatise, le telechargement, l'usage, la copie, la distribution et les
oeuvres derivees, contre le maintien de la mention de source. [CONFIRME avec URL,
https://www.newyorkfed.org/privacy/termsofuse] C'est le regime le plus ouvert des cinq sources
de la nuit, plus ouvert que le GSS, dont NORC interdit la redistribution.

**Les identifiants de panel sont publics.** Les quatre premieres colonnes sont `date`, `userid`,
`tenure`, `weight`. [CONFIRME] C'etait le point que MOONSHOTS listait comme non verifie et dont
le mois 1 du programme C dependait.

Structure mesuree en lisant les fichiers :

| fichier | observations | variables | mois | periode | personnes | vagues par personne |
|---|---|---|---|---|---|---|
| 13-16 | 56 444 | 220 | 43 | 2013-06 a 2016-12 | 8 735 | 6,46 |
| 17-19 | 47 681 | 220 | 36 | 2017-01 a 2019-12 | 7 379 | 6,46 |
| 20-24 | 71 976 | 229 | 60 | 2020-01 a 2024-12 | 9 751 | 7,38 |
| latest | 10 559 | 229 | 10 | 2025-01 a 2025-10 | 2 159 | 4,89 |

[MESURE] Environ 1 200 repondants par mois, aucun doublon de couple date et personne.

Ce que cela debloque, tel quel, sans une lettre et sans un euro : le plancher de reinterrogation
a un mois et a douze mois sur les memes menages, qui est le denominateur du programme C ; la
dispersion des anticipations par cohorte d'age, d'education et de revenu, par les variables
`_AGE_CAT`, `_EDU_CAT`, `_HH_INC_CAT` ; et la deformation de cette dispersion **apres** le choc
de 2025, qui est posterieur a la coupure des modeles installes, avec dix mois deja publies.
La distribution complete des anticipations d'inflation est disponible par personne et par mois,
pas seulement la moyenne : `Q9_mean`, `Q9_var`, `Q9_iqr`, les trois quartiles et les dix bacs de
probabilite a un an, la meme chose a trois ans et a cinq ans.

Le seul point d'ombre est la **stabilite de `userid` d'un fichier a l'autre**, qui n'est
documentee nulle part sur la page. Elle ne bloque rien a l'interieur d'un fichier, elle bloque
la trajectoire longue d'un menage de 2019 a 2025. Lettre 02.

---

## 4. Un fichier reel a contamination documentee

Trois sources ont ete evaluees. Aucune ne donne aujourd'hui un flux reel melange a un taux vrai.

### 4.1 Westwood 2025, PNAS : obtenu, mais c'est la moitie de la piece

`10.1073/pnas.2518075122`, publie le 20 novembre 2025, en acces libre. La declaration de
disponibilite renvoie vers OSF, noeud `ektqr`, **qui est public** : le jeton `view_only` du texte
n'est pas necessaire. [CONFIRME]

Telecharge : 85 fichiers, 28 Mo. Le moteur du repondant synthetique, `solver.py` et cinq invites
systeme dont une democrate, une republicaine et une pro chinoise ; neuf scripts R ; et surtout
**34 fichiers CSV, 27 923 reponses generees par 300 profils**, avec demographie declaree, parti,
Etat, et pour chaque reponse le texte de la question et la justification produite par le modele.
L'auteur a volontairement retire les scripts d'injection dans Qualtrics, et c'est la bonne
decision ; nous n'en avons pas l'usage.

Ce que ca vaut pour le programme B : un fabricant adverse de plus, et le plus dur de la liste,
puisqu'il passe 99,8 pour cent de 6 000 essais de controles d'attention standard. Il se branche
dans la chaine de i3 sans rien demander a personne.

Ce que ca ne vaut pas : **ce n'est pas une contamination reelle**. Il y a une source synthetique
pure d'un cote, et pas de flux humain melange a un taux connu. Le melange doit etre fabrique par
nous, ce qui reste un melange fabrique. La limite que i3 s'ecrit a lui meme n'est pas levee.

### 4.2 La consultation de 2017 sur la neutralite du reseau

C'est la seule contamination reelle a taux vrai etabli par une autorite. Le fichier au niveau du
commentaire, avec l'etiquette de faussete, n'est pas public : aucun depot de ce type n'a ete
trouve, et les depots publics de commentaires ne portent que des regroupements par duplication,
pas la qualification officielle. Lettre 03, adressee au procureur general de l'Etat de New York,
en copie a la FCC.

### 4.3 Une plateforme d'enquete ou un institut

Aucune plateforme n'a publie a ce jour un fichier de repondants bannis avec leurs reponses
fermees etiquetees. Lettre 04, generique, avec la liste des destinataires possibles et l'argument
qui les interesse : le plancher de detection de leur propre flux, chiffre que personne ne leur
donne aujourd'hui.

### 4.4 Ce qui a ete cherche et non trouve

Un jeu academique de detection de repondants inattentifs ou assistes avec verite terrain, sur
Harvard Dataverse : les requetes sur Kennedy et la crise de qualite de MTurk, et sur Bisbee et
les remplacements synthetiques, n'ont rien rendu de pertinent. [HYPOTHESE] Ces jeux existent
peut etre ailleurs, sur OSF ou en annexe de revue ; la recherche web de la session etait epuisee,
elle n'a pas pu etre poussee. C'est le premier point a reprendre a la prochaine session.

---

## 5. Une seconde population humaine hors Etats Unis

Quatre panels examines. Deux sont en libre service, deux exigent une demarche.

| panel | acces | cout | delai | verdict |
|---|---|---|---|---|
| **LISS**, Pays Bas | signature en ligne d'une declaration, puis telechargement | gratuit pour la recherche non commerciale | cinq jours ouvres annonces | **la voie a prendre en premier** |
| **British Election Study** | telechargement libre, aucun compte | gratuit | immediat | **a prendre ce soir** |
| **ELIPSS**, France, CDSP | procedure non documentee sur le site public | inconnu | inconnu | lettre 06 |
| **SOEP**, Allemagne | contrat de diffusion signe | gratuit pour l'academique | non annonce | lettre 07, sous reserve |

Le point dur est le SOEP : sa page d'acces dit **« Individuals (without an institutional
affiliation) are not permitted to use the SOEP data »**, et exige des institutions non
allemandes la preuve d'une activite de recherche independante. [CONFIRME avec URL,
https://www.diw.de/en/diw_01.c.601584.en/data_access.html] Un chercheur independant sans
rattachement ne passe pas. La lettre 07 pose la question du rattachement plutot que de deposer
un dossier qui sera refuse.

Le LISS, a l'inverse, est explicitement ouvert : « The published data can be accessed free of
charge for scientific or policy relevant (non-commercial) research », declaration a signer sur
`https://liss.statements.centerdata.nl/`, puis archive sur
`https://www.dataarchive.lissdata.nl/`. [CONFIRME avec URL] Les etudiants y sont admis avec un
mot de passe valable deux ans. C'est la seconde population humaine de reference la moins chere
et la plus rapide a obtenir, et elle ne demande aucune lettre.

Le BES est en telechargement libre : « All data listed here can be freely downloaded. By
downloading the data you agree to the terms and conditions of use ». [CONFIRME avec URL,
https://www.britishelectionstudy.com/data/] Le panel internet couvre 21 vagues de 2014 a 2020,
donc plusieurs ruptures, dont le referendum de 2016. Les sous pages de telechargement renvoient
403 depuis cette machine, comme l'ANES ; il faudra un navigateur.

---

## 6. Ahler et Sood, obtenu en passant

`doi:10.7910/DVN/CLMQ8E`, Harvard Dataverse, **licence CC0 1.0**, telechargeable sans compte.
5,1 Mo. Cinq jeux individuels : l'enquete YouGov de composition percue des partis, l'experience
sur la perception d'extremite, l'experience sur l'affect partisan, l'experience sur les
explications alternatives, et le code de replication. [CONFIRME]

C'est le referent humain de croyance de second ordre du programme A, celui que MOONSHOTS citait
sans savoir s'il etait accessible. Les huit items de composition sont dans le codebook, avec
`pid3`, `pid7` et `ideo5`.

Un detail qui vaut une preuve : le `readme.txt` reclame `anes_timeseries_2012.dta` pour faire
tourner le script principal, **et ce fichier n'est pas dans l'archive**, alors que tout le reste
y est sous CC0. C'est la trace directe de la regle ANES sur la redistribution.

---

## 7. Ce qu'Amir doit faire lui meme

Par ordre de rendement, du plus rapide au plus long.

1. **Signer la declaration LISS**, cinq minutes, sur https://liss.statements.centerdata.nl/ ,
   puis attendre cinq jours ouvres. C'est la seconde population humaine de reference du
   programme B mois 6 et du programme C, et c'est gratuit.
2. **Telecharger le British Election Study** depuis un navigateur, sur
   https://www.britishelectionstudy.com/data/ , panel internet vagues 1 a 21. Aucun compte, mais
   le site refuse cette machine en ligne de commande.
3. **Ouvrir un compte ANES** sur https://electionstudies.org/data-center/ , depuis un navigateur,
   et **envoyer la lettre 01** a `anes@electionstudies.org`. La lettre contient la question sur
   le module GSS vide, qui est la seule question de la nuit dont la reponse peut changer la
   forme du mois 1 du programme A. Recuperer 2020 Full Release et 2024 Full Release en CSV.
4. **Envoyer la lettre 03** au procureur general de l'Etat de New York. C'est la demande a plus
   long delai et a plus fort rendement : sans elle, le programme B publie une methode et pas une
   mesure.
5. **Choisir un destinataire pour la lettre 04** et l'envoyer. Une plateforme de panel qui
   publie sur la qualite des donnees est plus susceptible de repondre qu'un institut de sondage.
6. **Envoyer la lettre 05** a Sean Westwood. Cout nul, chance reelle : il vient de publier que
   le probleme est existentiel, et nous lui apportons un detecteur.
7. **Envoyer la lettre 06** au CDSP et la **lettre 07** au SOEP. La 07 est une question
   d'eligibilite avant dossier, pas un dossier.
8. **Envoyer la lettre 02** a la Fed de New York, quand il y aura une minute. Elle ne bloque
   rien, elle ouvre la trajectoire longue des menages.

Toutes les lettres attendent trois champs : `[AFFILIATION]`, `[NOM ET SIGNATURE]`, `[DATE]`.

---

## 8. Ce qui n'a pas ete verifie, et ce qui pourrait etre faux

1. **Les conditions d'acces reelles de l'ANES.** Le site n'a pas pu etre lu. Les conditions
   citees dans `data/anes-codebooks/PROVENANCE.md` viennent du paquet `anesr`, tierce partie, et
   sont marquees [PROBABLE]. Il est possible que le telechargement soit libre et que le blocage
   ne soit qu'un pare feu ; dans ce cas la lettre 01 se reduit a sa question sur le module GSS.
2. **Le module GSS vide.** Le constat porte sur les codebooks HTML produits par SDA, pas sur les
   fichiers de donnees eux memes. Il est theoriquement possible que SDA ait charge une version
   des fichiers dont ce bloc a ete retire. Le fait que les modalites valides soient declarees
   avec un effectif de zero en 2024 rend cette hypothese peu vraisemblable, mais elle n'est pas
   exclue. A verifier des que le fichier officiel est en main.
3. **L'appariement lui meme.** Il est fonde sur les libelles de variables des codebooks ANES et
   sur les modalites lues dans les tableaux de frequences, pas sur une lecture integrale des
   formulations de question dans les guides PDF, qui sont en main mais dont l'extraction en
   colonnes est bruitee. Les 12 appariements a confiance elevee ont ete verifies un par un sur
   les modalites ; les 12 a confiance moyenne ne l'ont pas ete au dela du libelle. Deux d'entre
   eux, `vote16` et `pres16` vers `V201102` et `V201103`, ont ete poses par deduction sur le
   libelle et confirmes dans l'index, pas dans le tableau de frequences.
4. **La stabilite de `userid` de la SCE entre fichiers.** Non verifiee, et verifiable en interne
   : il suffirait de tester le recouvrement des identifiants entre le fichier 17-19 et le
   fichier 20-24. Ce test n'a pas ete lance cette nuit pour ne pas prendre de coeurs a i3b.
5. **Les jeux academiques de detection avec verite terrain.** Recherche interrompue, budget de
   recherche web epuise a l'ouverture de la session, budget OpenAlex epuise en cours de route.
   Une absence de resultat n'est pas une preuve d'absence, et ce dossier a deja vu la recherche
   par absence ceder plusieurs fois.
6. **Le module GSS 2024 pourrait etre administre a une vague ulterieure.** L'ANES 2024 a une
   version complete d'aout 2025 ; rien ne dit qu'il n'y aura pas une version 2 avec le module
   rempli.
7. **Le fichier `latest` de la SCE s'arrete en octobre 2025.** Le choc tarifaire de 2025 est donc
   couvert sur dix mois seulement, ce qui est suffisant pour une deformation de dispersion mais
   court pour une trajectoire.
