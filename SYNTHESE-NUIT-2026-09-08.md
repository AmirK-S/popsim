# Synthese de la nuit du 7 au 8 septembre 2026

Document final de la nuit, ecrit le 8 septembre a 05 h 30. Dix neuf chantiers ont rendu leur
rapport entre 22 h 38 et 05 h 25 (a5 a a23). Le run de calcul a5 est termine a 05 h 01 :
**C2 et C3 completes, 22 350 appels chacune, 150 personnes, 149 items**. Les deux evaluations
du matin ont tourne a 05 h 02 et leurs chiffres sont dans ce document.

Deux calculs tournent encore et **ne sont pas dans ce document** : C3F jusqu'a 06 h 20, qui
sera partielle, environ 57 personnes sur 150, puis l'extension de C2 jusqu'a 08 h 30. Toute
ligne C3F ou extension qui apparaitrait dans une sortie de ce matin porte sur une trace
partielle et ne doit pas etre lue (a23 section 0).

Convention : chaque chiffre porte son rapport source entre parentheses. Les niveaux [CONFIRME]
[MESURE] [PROBABLE] [HYPOTHESE] sont conserves la ou ils changent la lecture. Les chiffres
annules par un errata ne figurent pas, sauf pour dire qu'ils sont annules.

---

## En une page

### Ce que le run detruit

1. **Nos deux agents locaux sont domines sur les deux axes du plan exactitude et diversite par
   une regression logistique sur les seules demographies** : C3 a 0,5817 d'exactitude et
   67,4 pour cent de diversite conservee contre 0,6281 et 73,1 pour cent pour B1, ecart apparie
   -4,64 points [-5,71 ; -3,60] (a23). Le front de Pareto de ce plan, humains exclus, ne
   contient que deux points, les agents composite de Stanford et B0 tirage : tout le reste est
   domine, C3 par quatre methodes et C2 par six (a23). [MESURE]
2. **C3 tombe sous la modalite majoritaire des qu'on sort des six familles thematiques** :
   0,5541 contre 0,5798 pour B0 mode sur les 91 items hors famille, quand il est a 0,6249
   contre 0,6205 sur les 58 items de famille (a23). Dix items expliquent 61 pour cent du
   deficit face a B1 : sur ceux la le modele ne se trompe pas de personne, il substitue sa
   modalite a celle de la population, "Other" pour 133 personnes sur `dwelown16` la ou 110
   humains repondent "own or is buying" (a23). [MESURE]
3. **Le modele est certain et faux** : ECE de 0,4410 pour C2 et 0,3787 pour C3 ; dans le decile
   de confiance 0,9 a 1,0, qui porte 20 101 appels, la confiance moyenne vaut 0,9950 et
   l'exactitude reelle 0,5450 (a23). Le smoke test de a5, qui annoncait 0,66 sur 80 cellules,
   etait optimiste. Version population du meme fait : une seule modalite couvre plus de 90 pour
   cent des personnes sur 46 items sur 149 pour C2 et 43 pour C3, contre 13 chez les humains
   (a23). [MESURE]
4. **La phrase "les agents battent B2 en regime famille retiree" sort du dossier.** C3F retire
   du contexte la famille entiere de l'item cible, donc C3F est necessairement inferieur ou
   egal a C3 sur ces 58 items, ou C3 vaut 0,6249 ; la cible est 0,6621 (a23, a8 errata E1).
   [PROBABLE, sur une inegalite qui ne peut jouer que dans un sens]

### Ce que le run etablit

5. **L'etiquette ideologique dans l'invite commande le signe du gonflement, et c'est le plan
   experimental qui manquait a la litterature.** A modele egal, temperature egale, memes
   personnes, memes items, meme pipeline : C2, qui porte l'etiquette, gonfle l'axe ideologie a
   **8,16 [5,43 ; 15,55]**, exactement comme `gss_v8` a 8,95 [6,00 ; 16,80] ; C3, qui ne la
   porte pas, l'**ecrase a 0,73 [0,47 ; 0,99]**, intervalles disjoints (a23). C'est la
   replication interne, sur un autre modele et une autre invite, du fait que a19 avait etabli
   sur l'archive de Stanford. [MESURE]
6. **Le controle de la vague 2 passe a 150 personnes sur trois axes** : ideologie
   1,11 [0,93 ; 1,41] en entropie et 1,01 [0,86 ; 1,20] en Gini Simpson, profil croise
   0,97 [0,70 ; 1,19], age 1,10 [0,83 ; 1,66] ; au niveau agrege 1,046 [0,912 ; 1,237] contre
   1,167 avec un intervalle debordant sur la trace partielle de 55 personnes (a23, a18). Les
   ratios inter du run sont publiables sur ces trois axes, sur aucun autre. [MESURE]
7. **La question 3 de a7 est fermee sur 44 700 appels : le deficit de dispersion totale n'est
   pas dans le decodage.** Lire la distribution complete au lieu de durcir par argmax rend
   1,4 point sur les 34,6 manquants pour C2, 0,654 vers 0,668, et 1,9 point sur 32,6 pour C3,
   0,674 vers 0,693 ; la temperature qu'il faudrait vaut 6,29 et 6,27, ce qui porterait
   l'entropie individuelle de 0,117 a 1,007 bit, facteur 8,6 (a23, a18). La famille A de
   `exploration/09`, le decodage, est fermee par une mesure sur deux regimes d'invite ; reste
   la famille B, le conditionnement. [CONFIRME]
8. **Le pipeline reproduit la mesure fondatrice du projet a zero point pres** : accord par
   paires de C2 sur ces 150 personnes 66,4 pour cent contre 49,3 chez les memes humains
   reinterroges, la ou a0 mesurait 66,4 contre 49,5 sur les agents demographiques de Stanford
   et 1 052 personnes (a23, a18, a0). [CONFIRME]

### Ce que le run ne separe pas

9. **L'absence de gonflement de C3 est soit un resultat majeur, soit une incapacite du modele
   de 4 milliards de parametres, et rien dans ce run ne separe les deux** (a23). Si un modele
   plus gros dans le meme regime sans etiquette gonfle comme les agents enquete de Stanford,
   alors l'essentialisme identitaire apparait avec la capacite, ce qui est publiable ; s'il ne
   gonfle pas non plus, le gonflement du regime questionnaire est une propriete de la chaine de
   Stanford, invite comprise, et le papier change de cible. Une nuit de calcul tranche.
10. **Aucune des trois issues prevues par a15 n'est observee.** Ce qui l'est est une quatrieme
    issue, emboitee : l'etiquette commande le signe, l'axe commande la repartition a l'interieur
    de la condition etiquetee. Avec etiquette, gonflement massif sur l'ideologie, le profil
    croise et l'age, et effondrement sur le genre a 0,07 alors que l'etiquette de genre est
    presente et recopiee. Sans etiquette, aucun gonflement sur aucun axe, ideologie comprise
    (a23, a15). [MESURE pour le fait, [HYPOTHESE] pour la cause]
11. **Les prompts de C2 et C3 n'ont jamais ete compares a ceux de `v8` et des agents enquete.**
    Tout l'ecart attribue au modele, 3,9 point dans le regime demographique et 6,4 dans le
    regime questionnaire, peut venir en partie de la formulation. C'est la limite la plus
    serieuse du run (a23, a5 limite 4).

### Ce que la nuit d'analyse avait deja etabli, et qui tient

12. La double distorsion tient hors du GSS et hors du pipeline de Stanford : treize
    configurations de Twin-2K-500 sur treize sont dans le quadrant, inter 1,57 a 3,73 et intra
    0,45 a 0,75, avec un controle de retest humain en (1,004 ; 1,009) (a6).
13. Le correctif qui portait la contribution, le transport de variance a somme constante, ne
    marche pas, et son impossibilite est arithmetique : le ratio de dispersion totale vaut
    0,802 a 0,954 sur les 40 couples mesures et un operateur a somme constante le laisse
    invariant (a7 errata, a20).
14. La metrique du champ est presque aveugle a la structure : moins d'un point d'exactitude,
    0,83 [-1,28 ; -0,38], separe deux conditions dont les gonflements inter groupes different
    d'un facteur 13,5 (a19, a17, a1 errata E1).
15. Le terrain libre s'est reduit trois fois dans la nuit : LifeMem publie deja notre terme
    intra, Garzon et al. publient une correlation intraclasse intra strate, Kim et Lee mesurent
    les deux termes sur le GSS depuis 2023 et Bisbee et al. 2024 les publie avec referent
    humain (a10, a13, a15). Ce qui reste sans equivalent est le plancher de bruit humain par
    reinterrogation, et il repose entierement sur une archive OSF sans licence declaree.
16. Le score normalise d'un meme agent se deplace de dix a treize points selon le seul delai de
    retest et franchit 100 pour cent a quatre ans (a12).

---

## La these, reformulee

**La formulation d'avant.** "Les populations simulees sont mal structurees, trop homogenes
dedans et trop separees dehors ; le correctif ne peut pas etre une dilatation, ce doit etre un
transport de variance a somme constante de l'inter vers l'intra, et aucun papier ne le formule
ainsi." La premiere moitie tient, la seconde tombe, et la nuit lui a ajoute un troisieme terme.

**La formulation a employer desormais, en une phrase.** Les populations simulees ont trois
defauts et non deux : une dispersion interne ecrasee, des ecarts entre groupes gonfles sur les
seuls axes politiquement charges **et seulement quand l'etiquette de groupe est dans l'invite**,
et un deficit de dispersion totale que ni le decodage ni une reallocation ne comblent. La
contribution du projet n'est plus le correctif, c'est la mesure conjointe des trois quantites
rapportee a un plafond humain mesure, et le critere d'evaluation qu'aucun correctif publie ne
satisfait.

**Les six phrases qui la composent, chacune avec son etat au 8 septembre.**

1. **La double distorsion est confirmee sur trois jeux de donnees et deux pipelines.** Quatre
   conditions sur six du paquet OSF sur le GSS (a1), treize configurations sur treize de
   Twin-2K-500 produites par une autre equipe avec GPT-4.1, GPT-4.1-mini et Gemini-Flash-2.5,
   et cinq conditions sur six sur les jeux economiques et le Big Five du meme paquet (a6). Sur
   Twin, les trois mesures ne s'accordent plus, la variance ordinale y donne un intra de 0,06 a
   0,22 : il est interdit d'ecrire "la double distorsion" sans nommer la mesure (a6). **Nos
   propres agents ne valident pas cette phrase en bloc** : C2 est dans le quadrant avec `v8`,
   C3 est dans le quadrant inferieur gauche avec `v6` et `v7`, les deux termes ecrases (a23).
2. **La metrique du champ est presque aveugle a la structure.** Deux conditions du meme papier,
   memes 1 052 participants, memes 169 items, dont l'exactitude ne differe que de 0,83 point
   [-1,28 ; -0,38], ont des gonflements d'ecarts inter groupes qui different d'un facteur 13,5
   avec des intervalles disjoints (a1 errata E1, a19, a17). La demonstration ne depend meme plus
   du paquet de replication : la reconstruction de l'exactitude globale depuis la ligne Gender
   du tableau 5 donne 56,28 pour cent la ou le tableau 8 affiche 58,12, ecart de 1,84 point
   (a14). Le mot "indistinguable" est retire du dossier ; le "-0,07 point statistiquement zero"
   aussi (a19).
3. **L'etiquette ideologique dans l'invite est la cause mesuree du gonflement inter, et elle
   est de premier ordre.** Sur l'archive : `gss_v6` n'a recu ni ideologie ni parti, taux de
   recopie 0,200 et 0,165, `gss_v8` les a recus, 0,961 et 0,994, et le ratio inter sur l'axe
   ideologie passe de 0,34 a 8,51 sans que l'exactitude change de plus d'un point (a19). Sur
   notre pipeline, a modele, temperature, personnes et items constants : C2 avec etiquette a
   8,16 [5,43 ; 15,55], C3 sans etiquette a 0,73 [0,47 ; 0,99], intervalles disjoints (a23).
   Deux archives, deux modeles, deux invites, meme conclusion. C'est le resultat le plus solide
   du dossier.
4. **Le deficit est total, et il est loge dans le conditionnement : ni le decodage, ni le
   transport entre groupes ne le comblent.** Cote decodage : lire la distribution complete rend
   1,4 point sur 34,6 pour C2 et 1,9 sur 32,6 pour C3, la temperature necessaire vaut 6,29 et
   6,27, mesure sur 44 700 appels et deux regimes d'invite (a23, a18). Cote transport : un
   operateur a somme constante laisse invariant le ratio de dispersion totale, qui vaut 0,802 a
   0,954 sur les 40 couples, et le plafond du ratio intra a terme inter nul vaut 0,9364 pour
   les agents composite ; le critere A6 echoue dans les 32 lignes mesurees (a7 errata, a20). La
   famille A de `exploration/09` est fermee, la famille B reste ouverte. La version population
   du meme fait est nouvelle : le modele choisit une modalite pour les trois quarts de la
   population sur la moitie des items, et il en est certain (a23).
5. **Le delai de retest n'est pas controle par la litterature, et il deplace le score normalise
   de dix a treize points sans qu'aucun agent ne change.** 77,79 pour cent a deux semaines,
   69,53 a deux ans, 67,45 a quatre ans sur les memes 118 items ; le score normalise de l'agent
   composite passe de 0,844 a 0,944 puis 0,973 et franchit 1,008 a quatre ans sur les 149 items
   (a12). Le papier de reference ne discute nulle part ce choix, verification faite sur les 86
   pages de la version 3 (a14). A ne pas ecrire : que Stanford aurait choisi un denominateur
   flatteur, c'est l'inverse, deux semaines est le plus severe des trois (a12).
6. **L'axe de segmentation separe les camps de la litterature, mais il ne suffit plus a decrire
   nos donnees.** Les travaux qui segmentent sur un axe politique mesurent un gonflement, ceux
   qui segmentent sur des axes non politiques ne publient pas de terme inter ou concluent a un
   aplatissement depuis une mesure globale ; PSII, le contradicteur suppose, ne mesure jamais
   d'ecart inter groupes sur ses sorties et son introduction ecrit l'inverse de son resume
   (a15). Nos donnees reproduisent le partage a l'interieur de la condition etiquetee, et le
   contredisent hors d'elle : **l'etiquette commande le signe, l'axe commande la repartition a
   l'interieur de la condition etiquetee** (a23). La phrase de synthese de a15 section 7.1 doit
   etre rouverte : les deux mecanismes ne sont pas exclusifs, ils sont emboites.

Sur le vocabulaire : "transport" et "redistribution" sont pris par trois papiers de 2026 dans
trois sens differents. La formulation proposee est "reallocation de variance a total fixe", en
anglais "variance reallocation under a fixed total" (a13, a10).

---

## Ce que le run a tranche

Les six questions que le run devait trancher, avec leur reponse en une ligne. Elles sont celles
de a23 section 3 : le juge, puis les cinq contrastes ecrits par a15 section 8.

| # | question | reponse en une ligne |
|---|---|---|
| 0 | **Le juge : le controle de la vague 2 passe t il a 150 personnes ?** | **Oui, sur l'ideologie, le profil croise et l'age**, 1,11 [0,93 ; 1,41] sur l'axe qui porte l'effet, et sur l'agregat, 1,046 [0,912 ; 1,237] ; non sur la race et l'education, dont l'intervalle contient des valeurs negatives ; le genre est un cas intermediaire a ne pas publier seul (a23 section 3.1). |
| 1 | **Contraste 1, C2 contre C3 par axe : qui commande, l'axe ou l'etiquette ?** | **Les deux, emboites**, et aucune des trois issues de a15 n'est observee : sans etiquette aucun axe ne gonfle, ideologie comprise, 0,73 [0,47 ; 0,99] ; avec etiquette l'ideologie explose a 8,16 [5,43 ; 15,55], le profil croise a 4,88 et l'age a 1,87, pendant que le genre s'effondre a 0,07 alors que son etiquette est presente (a23 section 3.2). |
| 2 | **Contraste 2, argmax contre distribution : le signe change t il ?** | **Non, jamais**, ni sur l'inter, ni sur l'intra, ni sur la mesure de Chen ; chez nous le mode distributionnel rapproche de 1 dans les deux cas, C2 4,769 vers 4,579 et C3 0,607 vers 0,630, la ou Chen trouve l'inverse pour Sonnet, ecart de 4 pour cent, ce que a5 annoncait a temperature 0 (a23 section 3.3). |
| 3 | **Contraste 3, la mesure a la Chen : le contrat est il tenu ?** | **Oui**, `delta eta carre` reste positif pour C2, +0,2960, et negatif pour `v6` et `v7`, -0,0226 et -0,0155 ; il devient negatif pour C3, -0,0104, ce qui est nouveau, et le controle humain vague 2 est a +0,0047 ; seuls le signe et le classement sont comparables a Chen, jamais les valeurs absolues (a23 section 3.4). |
| 4 | **Contraste 4, la temperature est elle isolable comme levier purement intra ?** | **Non, et il faut cesser de l'ecrire** : le profil attendu tient pour C2, intra 0,556 sous la bande 0,620 a 0,872 de Stanford et inter dans la bande, mais il s'inverse pour C3, intra 0,672 dans la bande et inter 0,607 sous la bande ; trois variables changent en meme temps, modele, quantification et invite (a23 section 3.5). |
| 5 | **Contraste 5, le deficit de dispersion totale est il dans le decodage ?** | **Non**, il est confirme et legerement aggrave : 0,654 vers 0,668 pour C2 et 0,674 vers 0,693 pour C3, soit 4,1 et 5,9 pour cent du deficit, temperature necessaire 6,29 et 6,27 ; la famille A de `exploration/09` est fermee sur 44 700 appels et deux regimes d'invite (a23 section 3.6). |

**Un septieme resultat, non prevu, et il derange.** Le critere A6 en version positive : la
deviance moyenne au mode de segment de C2 et de C3 **depasse** celle des humains, 0,409 et
0,429 contre 0,396, et leurs correlations sont parmi les plus basses du tableau, 0,246 pour C2
contre 0,895 pour le controle humain. Toutes les conditions de Stanford sont sous la deviance
humaine, profil attendu d'un ecrasement. Nos agents s'ecartent du stereotype de groupe plus
souvent que les vraies personnes, et pas pour les memes personnes : c'est du bruit, pas de
l'heterogeneite (a23 section 3.7). Le chiffre de la trace partielle, C2 a r = 0,638, n'a pas
tenu ; il tombe a 0,246 sur 150 personnes.

---

## Ce que le projet peut revendiquer

Les trois listes viennent de a13 section 5, mises a jour par a15, a17, a19, a20 et a23.

### (a) Deja fait par d'autres, a ne plus presenter comme neuf

1. Le nom et le diagnostic de la double distorsion. LifeMem l'ecrit dans son resume, avec le nom
   d'identity essentialism et le constat de "stronger within-group compression and between-group
   separation than humans" (a10, a13).
2. La mesure de la dispersion intra groupe des reponses simulees. LifeMem la publie sous le nom
   de within-group pairwise distance, pour neuf methodes, trois modeles et deux jeux de donnees
   (a13). La phrase "aucun papier lu ne publie cette mesure" est retiree du dossier.
3. La mesure conjointe d'un terme inter et d'un terme intra sur le GSS. Kim et Lee, arXiv
   2305.09620 v4, la publient depuis 2023 sur cinq de nos six axes (a13).
4. Les deux termes avec referent humain. Bisbee et al. 2024, Political Analysis, les publie sur
   la polarisation affective, sd ANES 31,4 contre ChatGPT 16,1, ratio 0,513, qui est
   vraisemblablement la source du "0,40 a 0,56" du dossier (a15).
5. Le constat que les agents demographiques sont plus homogenes dans une strate que les agents
   ancres. Garzon, Baron, Grari, Kamphorst, Bernstein et Detyniecki le publient avec une
   correlation intraclasse, sur quatre echelles (a10, a13).
6. La forme d'argument "une statistique agregee identique recouvre deux mecanismes opposes".
   Garzon et al. l'emploient dans leur annexe 7.16 pour l'alpha de Cronbach (a13).
7. Le correctif par ancrage sur des reponses individuelles, occupe par les deux equipes (a13).
8. Un correctif publie de l'identity essentialism existe deja : LifeMem reduit l'ecart intra
   groupe de 22 pour cent, la divergence KL de 30 pour cent (a10).

### (b) Neuf chez nous, une phrase par revendication

Chaque phrase est ecrite pour tenir devant un relecteur qui a lu LifeMem, Garzon, Kim et Lee,
Bisbee et Chen.

1. **Nous mesurons les deux termes comme deux ratios a un referent humain, sur les memes
   donnees, les memes segmentations et les memes items, ce que LifeMem ne fait pas parce qu'il ne
   mesure jamais l'inter, ce que Garzon et al. ne font pas faute de referent humain sur cette
   analyse, ce que Kim et Lee ne font pas parce qu'ils rapportent des nuages de points sans
   ratio, et ce que Bisbee et al. ne font que sur une seule quantite construite, la polarisation
   affective.** (a13, a15)
2. **Nous fournissons le plancher de bruit humain qu'aucun des quatre ne fournit : les memes
   personnes reinterrogees deux semaines plus tard tombent a 0,4 pour cent de (1, 1) sur les
   trois mesures de dispersion, ce qui borne a environ un demi pour cent l'ecart que la methode
   peut fabriquer en l'absence de distorsion reelle, quand les effets rapportes vont de 11 a 36
   pour cent d'ecrasement intra et de 75 a 491 pour cent de gonflement inter.** Le mot "prouve"
   et la phrase "les intervalles contiennent 1" sont retires : l'intervalle intra exclut 1 de
   0,01 et 0,03 pour cent selon la mesure (a13 errata E3, a1 errata E2, a19).
3. **Nous montrons que la metrique d'exactitude du champ est presque aveugle a la structure de la
   population simulee : deux conditions du meme papier, memes 1 052 participants, memes 169
   items, dont l'exactitude ne differe que de 0,83 point [-1,28 ; -0,38], ont des gonflements
   d'ecarts inter groupes qui different d'un facteur 13,5 avec des intervalles disjoints. Un
   point d'exactitude d'un cote, un facteur treize de l'autre.** (a13 errata E1, a19, a17)
4. **Nous corrigeons le biais d'estimation qui inverserait le resultat : sans correction de
   Miller Madow, sans estimateur sans biais de l'indice de Simpson et sans controle par
   permutation des etiquettes de segment, un echantillon fini fabrique un terme inter positif qui
   croit avec le nombre de modalites employees, or les agents en emploient moins que les humains ;
   aucun des travaux voisins ne traite ce biais, et nous montrons de plus qu'un estimateur a
   biais corrige cesse d'etre valide des qu'un post traitement fixe les effectifs conditionnels,
   ce qui exige une nulle de permutation appariee a la structure de l'operateur.** (a13 errata
   E4, a20)
5. **Nous montrons que le sens de la distorsion inter est commande par la presence de
   l'etiquette de groupe dans l'invite, et sa repartition par l'axe de segmentation : sur
   l'archive, l'etiquette ideologique multiplie par vingt cinq le gonflement des ecarts entre
   segments ideologiques, de 0,34 a 8,51, sans changer l'exactitude de plus d'un point ; sur
   notre pipeline, a modele, temperature, personnes et items constants, la meme etiquette fait
   passer le ratio inter de 0,73 [0,47 ; 0,99] a 8,16 [5,43 ; 15,55], intervalles disjoints ; et
   l'ecart entre deux variantes portant la meme etiquette demographique dans le meme paquet
   atteint un facteur 6,9 sur le GSS, 22,8 sur les jeux economiques et 5,7 sur le Big Five.**
   (a13 errata E6, a1, a6, a19, a23)
6. **Nous posons le critere qu'aucun correctif publie ne satisfait : un correctif de l'identity
   essentialism doit etre evalue sur les deux termes et sur leur total apres application, faute
   de quoi on ne peut distinguer une reallocation d'une dilatation, et nous montrons par un
   temoin de dilatation pure que les metriques de LifeMem, intra seul et divergence KL, ne les
   distinguent pas.** (a13, a7, a20)
7. **Nous montrons qu'une chaine de mesure qui ne verifie pas la conformite des sorties a la
   nomenclature de l'enquete inverse le classement de diversite : compte sur les chaines brutes,
   `gss_v8` semble employer 4,48 modalites contre 3,62 aux humains, et une fois appariee a la
   nomenclature, 3,07 contre 3,62 ; le mecanisme est desormais nomme, l'extraction de Stanford
   est une expression reguliere sans appariement a la nomenclature.** (a13, a16)
8. **Nous etablissons qu'un score normalise n'est pas comparable entre protocoles de retest : sur
   les memes 118 items et avec la definition des auteurs, le denominateur vaut 77,79 pour cent a
   deux semaines, 69,53 a deux ans et 67,45 a quatre ans, ce qui deplace le score normalise d'un
   meme agent de 0,844 a 0,973 et le fait franchir 1,008 a quatre ans sur les 149 items, et le
   papier de reference ne discute nulle part ce choix, verification faite sur ses 86 pages.**
   (a12, a14)
9. **Nous mesurons le deficit de dispersion totale et nous l'imputons, ce qu'aucun travail lu ne
   peut faire faute de conserver la distribution complete du modele : sur 44 700 appels et deux
   regimes d'invite, lire la distribution au lieu de l'argmax ne rend que 1,4 point sur 34,6 et
   1,9 sur 32,6, et il faudrait une temperature de 6,29 et 6,27 pour combler le reste, ce qui
   multiplierait par 8,6 l'entropie individuelle.** (a23, a18) [CONFIRME sur traces completes]
10. **Nous mesurons l'ecrasement au niveau de l'appel, ce qu'aucun papier lu ne publie : le
    modele conserve 7,3 a 8,8 pour cent de l'entropie disponible par question, il est certain a
    plus de 0,99 sur 77 a 79 pour cent des appels, et son exactitude reelle dans ce decile vaut
    0,545 pour un ECE de 0,441 ; en version population, une seule modalite couvre plus de 90 pour
    cent des personnes sur 46 items sur 149, contre 13 chez les humains.** (a23, a18, a5)
11. **Nous montrons que l'exces de coherence des repondants synthetiques n'est ni uniforme ni
    toujours positif : il suit la charge identitaire du contenu, alpha 0,872 vers 0,967 sur les
    attitudes politiques et 0,814 vers 0,444 sur 40 decisions d'achat, avec un gonflement maximal
    entre opinion propre et consensus percu, 0,198 vers 0,723.** (a9)
12. **Nous montrons que la valeur des agents de langage est dans les queues et non dans la
    moyenne : quand la vraie reponse est choisie par moins de 10 pour cent des repondants, la
    meilleure baseline statistique en retrouve 3,6 pour cent et l'agent composite 30,7 pour cent,
    en reproduisant 95 pour cent de la masse minoritaire humaine.** (a8)

### (c) A ajouter pour que (b) tienne

Par cout croissant.

1. Reimplementer la within-group pairwise distance de LifeMem sur nos donnees et publier le terme
   inter sur la meme ligne. Quelques dizaines de lignes, aucune donnee nouvelle (a13).
2. Recalculer nos ratios sur la seule segmentation age croise genre, celle de Garzon et al. Une
   heure, `a1-ratios-par-axe.csv` contient deja les deux axes. C'est la reponse la moins chere a
   l'objection la plus previsible (a13 errata E7).
3. Publier l'indice `delta eta carre` de Chen a cote de notre ratio inter, ce sont deux fonctions
   du meme couple de quantites. **Fait pour nos deux conditions** (a15, a18, a23).
4. Recalculer l'ICC(1) de Garzon et al. sur nos huit conditions et publier l'ICC des humains, qui
   est le referent absent de leur papier. Une soiree (a13).
5. Trancher le regime "famille retiree" par C3F, seul test propre. **En cours, partiel a 06 h 20,
   3 h 24 pour le finir** ; l'arithmetique dit deja que la cible de 0,6621 est hors d'atteinte
   (a8 errata E1, a17 objection 1, a19, a23).
6. Traiter `income` comme `polviews` : il reste dans les 149 items, `gss_v6` le recopie a 0,994,
   effet mesure de 0,28 point sur `v6` seulement, **et il porte 25 des 30 rejets de C3** (a19,
   a17 objection 10, a23).
7. Construire une correction pour tests multiples. Elle est absente de tous les rapports, y
   compris de a23, et demande d'abord de fixer la famille d'hypotheses (a19, a17, a20, a23).
8. Lire Bisbee et al. 2024 dans le texte et arXiv 2603.16142 en entier avant redaction (a13,
   a15).
9. Comparer les prompts de C2 et C3 a ceux de `v8` et des agents enquete dans l'archive. C'est la
   limite la plus serieuse du run et elle se leve par une lecture, pas par un calcul (a23, a5).
10. Ecrire aux auteurs de LifeMem pour obtenir leurs sorties d'agents : le depot public contient
    le code mais ni les reponses humaines ni les sorties, et sans elles la revendication 6 reste
    un critere et non un resultat sur LifeMem (a13).
11. Changer le vocabulaire avant qu'un quatrieme papier ne prenne le dernier terme libre (a13,
    a10).

---

## Les chiffres a retenir

Statuts : **confirme** signifie reproduit ou verifie par la relecture adverse ou par un
recalcul independant ; **corrige** signifie que la valeur publiee le 3 ou le 7 septembre a ete
remplacee par celle ci ; **traces completes** signifie mesure le 8 septembre a 05 h 02 sur les
22 350 appels de C2 et les 22 350 de C3, 150 personnes et 149 items ; **non tourne** signifie
un cout projete pour un calcul qui n'a pas eu lieu.

| chiffre | ce qu'il mesure | jeu de donnees | source | statut |
|---|---|---|---|---|
| 0,437 et 5,907, facteur 13,5 | ratio d'ecarts inter groupes, `gss_v7` contre `gss_v8`, 169 items | GSS, paquet OSF | a1, reproduit par a19 | confirme par relecture |
| -0,83 point [-1,28 ; -0,38], t = -3,82 | ecart d'exactitude apparie `v7` contre `v8`, 169 items, n = 1 052 | GSS, paquet OSF | a19 (a17 mesure -0,88) | corrige par errata, remplace -0,07 [-0,52 ; +0,37] |
| 0,34 contre 8,51, facteur 25 | ratio inter sur l'axe ideologie, `gss_v6` contre `gss_v8` | GSS, paquet OSF | a19, a1 errata E4 | confirme par relecture |
| 0,200 et 0,165 contre 0,961 et 0,994 | taux de recopie de `polviews` et `partyid`, `v6` contre `v8` | GSS, paquet OSF | a19, a14 errata E1 | corrige par errata, annule la correction de a14 et de a16 sur a2 |
| 0,64 a 0,89 | ratio de dispersion intra groupe des agents | GSS, paquet OSF | a1 | corrige par errata, remplace le 0,40 a 0,56 de la litterature |
| a 0,4 pour cent de (1, 1) | controle humain vague 2, trois mesures, 1 052 personnes | GSS, paquet OSF | a1 errata E2, a13 errata E3 | corrige par errata, remplace "les intervalles contiennent 1" |
| 13 sur 13, inter 1,57 a 3,73, intra 0,45 a 0,75 | configurations dans le quadrant de la double distorsion | Twin-2K-500 | a6 | confirme par relecture |
| (1,004 ; 1,009) | controle de retest humain sur Twin | Twin-2K-500 | a6 | confirme par relecture |
| 22,8 et 5,7 | facteur entre les deux generations demographiques, inter | jeux economiques et Big Five, paquet OSF | a6 | confirme par relecture |
| 0,802 a 0,954 | ratio de dispersion totale `T`, 40 couples, trois mesures | GSS, paquet OSF | a20 | corrige par errata, remplace le 0,80 a 0,89 de a7 |
| 0,046 / 0,050 / 0,089 | poids `w` du terme inter dans la dispersion humaine, M1 / M2 / M3 | GSS, paquet OSF | a20 | corrige par errata |
| 0,9364 | plafond du ratio intra a terme inter nul, agents composite | GSS, paquet OSF | a20 | corrige par errata, remplace le 0,943 de a7 |
| 4 couples sur 8 | plafond intra au dessus de 1 sous la variance ordinale, 70 items ordinaux | GSS, paquet OSF | a20 | corrige par errata, a17 comptait 5 |
| 2,154 vers 1,053 | ratio inter des agents composite avant et apres transport, Gini Simpson | GSS, paquet OSF | a20 | corrige par errata |
| 0,90 a 3,43 points | cout du transport en exactitude individuelle, 149 items | GSS, paquet OSF | a20 | confirme par relecture |
| 32 lignes sur 32 negatives | echec du critere A6 apres transport, sous M3 | GSS, 70 items ordinaux | a20 | confirme par relecture |
| **0,7915 [0,7763 ; 0,8056]** | plafond humain test retest **de ces 150 personnes** sur 149 items | GSS, run a5 | a23, a5_evaluer | **traces completes** |
| **0,5263 et 0,5817** | exactitude argmax de C2 et de C3, soit 66,5 et 73,5 pour cent du plafond | GSS, run a5 | a23 | **traces completes**, remplace le smoke test 0,544 et 0,656 |
| **-4,64 points [-5,71 ; -3,60]** | ecart apparie C3 moins B1 argmax, 150 personnes, 149 items | GSS, run a5 | a23 | **traces completes** |
| **-1,39 point [-2,42 ; -0,31]** | ecart apparie C3 moins B0 mode | GSS, run a5 | a23 | **traces completes** |
| **65,4 et 67,4 pour cent** | diversite conservee de C2 et de C3, contre 73,1 pour B1 et 89,2 pour les agents composite | GSS, run a5 | a23 | **traces completes** |
| **deux points de front de Pareto** | agents composite et B0 tirage ; C3 domine par quatre methodes, C2 par six | GSS, run a5 | a23 | **traces completes** |
| **0,5541 contre 0,5798** | C3 contre B0 mode sur les 91 items hors des six familles | GSS, run a5 | a23 | **traces completes** |
| **0,654 vers 0,668 et 0,674 vers 0,693** | ratio de dispersion totale, argmax puis tirage, C2 puis C3 | GSS, run a5 | a23, a18 | **traces completes**, remplace le 0,659 vers 0,673 de la trace partielle |
| **6,29 et 6,27** | temperature qu'il faudrait pour amener la dispersion totale a 1, C2 puis C3 | GSS, run a5 | a23, a18 | **traces completes**, remplace le 5,71 de la trace partielle |
| **8,16 [5,43 ; 15,55] contre 8,95 [6,00 ; 16,80] et 0,24 [-0,25 ; 0,66]** | ratio inter axe ideologie, C2 contre `v8` et `v6` | GSS, run a5 | a23 | **traces completes**, remplace le 6,63 contre 7,78 et 0,15 |
| **0,73 [0,47 ; 0,99] contre 2,43 [1,82 ; 3,72]** | ratio inter axe ideologie, C3 contre les agents enquete de Stanford | GSS, run a5 | a23 | **traces completes**, chiffre nouveau |
| **1,11 [0,93 ; 1,41] et 1,046 [0,912 ; 1,237]** | controle vague 2 du terme inter, axe ideologie puis agregat, 150 personnes | GSS, run a5 | a23 | **traces completes**, remplace le 1,167 a intervalle debordant |
| **0,556 [0,527 ; 0,584] et 0,672 [0,657 ; 0,687]** | ratio intra de C2 et de C3, entropie, bande de Stanford 0,620 a 0,872 | GSS, run a5 | a23, a18 | **traces completes** |
| **+0,2960 contre +0,5178 et -0,0226** | `delta eta carre` de Chen, C2 contre `v8` et `v6`, ideologie en trois blocs | GSS, run a5 | a23, a18 | **traces completes**, remplace le +0,269 contre +0,480 et -0,036 |
| **-0,0104** | `delta eta carre` de C3 : ses reponses portent moins de structure ideologique que celles des humains | GSS, run a5 | a23 | **traces completes**, chiffre nouveau |
| **66,4 pour cent contre 49,3** | accord par paires, agents C2 contre humains vague 2, memes 150 personnes | GSS, run a5 | a23, a18, a rapprocher de a0 (66,4 contre 49,5) | **traces completes**, coincidence a zero point sur le premier terme |
| **ECE 0,4410 et 0,3787 ; 0,545 dans le decile a 0,995** | calibration de C2 et de C3 sur 22 350 appels chacune | GSS, run a5 | a23, a18 | **traces completes**, remplace le 0,66 du smoke test |
| **79,3 et 76,8 pour cent** | part des appels a p max superieure a 0,99, C2 puis C3 | GSS, run a5 | a23 | **traces completes** |
| **46 et 43 items sur 149 contre 13** | items ou une seule modalite couvre plus de 90 pour cent des personnes, C2 et C3 contre humains | GSS, run a5 | a23 | **traces completes**, chiffre nouveau |
| **0,246 et 0,673 contre 0,895** | critere A6 positif, correlation de deviance, C2 et C3 contre le controle humain | GSS, run a5 | a23 | **traces completes**, remplace le 0,638 de la trace partielle |
| **0,409 et 0,429 contre 0,396** | deviance moyenne au mode de segment, C2 et C3 contre humains : les deux seules conditions au dessus | GSS, run a5 | a23 | **traces completes** |
| **13 217 et 4 886 appels par heure, 0 et 30 rejets** | debit reel de C2 et de C3, machine seule | GSS, run a5 | a23 | **traces completes** |
| **25 rejets sur 30 portent sur `income`** | perte de masse du scoring par lettre unique au dela de huit modalites, masse descendant a 0,0991 | GSS, run a5 | a23 | **traces completes**, defaut de protocole a corriger |
| **0,6249 contre une cible de 0,6621** | C3 sur les 58 items de famille, contre "B2 famille retiree" : C3F ne peut pas atteindre la cible | GSS, run a5 et a8 | a23, a8 | **traces completes** pour C3, [PROBABLE] pour C3F |
| 77,79 / 69,53 / 67,45 pour cent | consistance test retest humaine a 2 semaines, 2 ans, 4 ans, 118 items | GSS, archive OSF et panels NORC | a12 | confirme par relecture |
| 0,844 vers 0,944 vers 0,973 | score normalise de l'agent composite selon le seul denominateur | GSS, 118 items | a12 | confirme par relecture |
| 1,008 | score normalise de l'agent composite a quatre ans, 149 items | GSS | a12 | confirme par relecture |
| 79,5253 sur 150 items | denominateur publie par les auteurs, jeu d'items exact | GSS, paquet OSF | a19, a12 errata E1 | corrige par errata, a12 ecrivait 177 items |
| 0,5840 contre 0,5655 et 0,5596 | copule gaussienne contre B2 et contre l'agent composite, 70 items ordinaux | GSS | a8 | confirme par relecture |
| 3,6 contre 30,7 pour cent | rappel des cellules minoritaires, B2 contre agent composite | GSS, seuil 10 pour cent | a8 | confirme par relecture |
| k = 25 et k = 100 | k de B2 par validation interne, GSS et Twin ; a2 sous estimait B2 de 0,44 point sur Twin | GSS et Twin-2K-500 | a8 | confirme par relecture |
| 0,797 puis 0,561 puis 0,479 | correlation avantage du modele contre stabilite de l'item : 108 items, hors bloc de prix, au niveau du bloc | Twin-2K-500 | a19, a8 errata E2 | corrige par errata, remplace le 0,80 seul |
| 0,872 vers 0,967 et 0,814 vers 0,444 | alpha de Cronbach humains vers agents, attitudes politiques puis 40 decisions d'achat | Twin-2K-500 | a9 | confirme par relecture |
| 0,198 vers 0,723 | correlation opinion propre contre consensus percu, humains vers agents | Twin-2K-500 | a9 | confirme par relecture |
| 30,9 pour cent, plancher 16,7, exces reel 14,2 points | part de variance du premier facteur de deviance | Twin-2K-500 | a19, a9 errata E3 | corrige par errata, remplace "31 contre un plancher de 0,000" |
| 0,45 a 0,66 et r = 0,275 | taux de deviance des agents rapporte aux humains, et reproduction du classement des personnes | Twin-2K-500 | a9 | confirme par relecture |
| 56,28 contre 58,12, ecart 1,84 | exactitude demographique reconstruite du tableau 5 contre celle affichee au tableau 8 | arXiv 2411.10109 v3 | a14 | confirme par relecture |
| 9,5 points | avantage de l'entretien apres retrait des items extractibles, mesure par les auteurs | arXiv 2411.10109 v3 | a14 | confirme par relecture |
| 0,7 et un seul appel | temperature en dur et nombre d'echantillons dans le code public de Stanford | depot StanfordHCI/genagents | a16 | confirme par relecture |
| 3 505 agents, licence MIT | banque de personas demographiques telechargeable, 30 attributs | depot StanfordHCI/genagents | a16 | confirme par relecture |
| 22 pour cent et 30 pour cent | reduction de l'ecart intra groupe et de la divergence KL par LifeMem | Add Health, Llama-8B | a10 | confirme par relecture |
| 1,3 a 7,7 et 1,4 a 1,6, total +43 a 48 pour cent | effet de l'ancrage chez Garzon et al., inter divise, intra multiplie, total en hausse | SHARE | a13 | reconstruction de lecture, non publiable en l'etat |
| 0,513 | ratio d'ecarts types ChatGPT sur ANES chez Bisbee et al. 2024 | ANES | a15 | confirme par relecture, source probable du 0,40 a 0,56 |
| 16 700 contre 1 759 appels par heure, facteur 9,5 | debit du run local, machine dediee contre deux serveurs | infrastructure | a5 | confirme par relecture |
| 27 515 tokens, 349 s de prefill, 10 h 45 | persona complet de Twin, cout par personne, cout de C3-Twin sur 150 personnes | Twin-2K-500 | a11 | confirme par relecture |
| 2 h 03 | cout de l'extension de C2 a 150 personnes de plus, 22 350 appels | GSS | a21 | **non tourne**, cout projete |
| 3 h 24 | cout de C3F complete au debit reel de 2 556 appels par heure | GSS | a23 | **non tourne**, cout projete au debit mesure |
| 11 h 48 et 13 h 36 | cout de C2 et C3 sur gpt-oss-20b puis sur Qwen3-30B-A3B | GSS | a23, a3 tableau 4.2 | **non tourne**, [ESTIMATION] |

Trois chiffres sont explicitement retires du dossier et ne doivent plus etre repris : le 0,40 a
0,56 comme ratio intra groupe (a10, a15, a9 errata E1), le "-0,07 point, statistiquement zero"
entre `v7` et `v8` (a19, a17), et la phrase "aucun papier lu ne publie cette mesure" (a13, a14
errata E3).

**Regle ajoutee par a23 : aucun chiffre de la trace partielle de a18 ne doit etre repris.** Le
critere A6 de C2 est passe de 0,638 a 0,246, le controle inter agrege de 1,167 a 1,046, la
temperature necessaire de 5,71 a 6,29.

---

## Ce qui reste faux ou fragile

**Objections de a17 restees ouvertes au 8 septembre.**

1. Le regime "famille retiree" de a8 n'est pas apparie : la famille sort du contexte de B2
   seulement, les agents de Stanford gardent leurs items cousins dans l'invite, et la condition
   appariee du papier vaut environ 4 points de moins (a17 objection 1, a8 errata E1). **Etat au
   8 septembre** : l'arithmetique de a23 tranche contre nous sans attendre C3F, C3 vaut 0,6249
   sur ces 58 items et la cible est 0,6621, mais **le chiffre reel de C3F n'existe pas** et la
   comparaison stricte reste a faire. [PROBABLE]
2. Aucune correction pour tests multiples n'existe dans aucun rapport, a23 compris : 32 lignes de
   critere A6, 40 couples de plafond, 36 comparaisons par famille, 12 axes fois conditions fois
   2 mesures. La famille d'hypotheses n'est toujours pas fixee (a17, a19, a20, a23).
3. Le biais residuel de l'estimateur inter n'a pas ete corrige par bootstrap dans a1 : la version
   publiee est declaree borne basse, sans colonne de correction (a17 objection 1.7, a19 point 4).
4. L'agregat des six axes de a1 n'a pas ete rejoue avec l'estimateur corrige, donc l'ecart 1,753
   contre 1,806 n'est pas decompose entre changement de jeu d'items et changement d'estimateur
   (a17 objection 3.4, a20 point 3).
5. Le profil croise comme axe de transport ne couvre que 72,2 pour cent des cellules, la nulle ne
   s'y annule pas et corriger dessus ecrase les axes marginaux (a20, a7 errata E5).
6. Trois defauts internes de a7 restent ouverts : le compte de 24 cellules contre 48, le temoin
   de hasard du critere A6 a 0,167 et non 0,3497, et les quatre manques de sa section 3.8 (a7
   errata, a20 section 0).
7. Les alphas de Cronbach de a9 n'ont pas d'intervalle de confiance, et la correction
   d'attenuation entre items stables et instables n'a pas ete faite (a17 objection 5.4, a19
   points 7 et 8).
8. Deux lignes du tableau de a17 objection 1.1 ne sont pas reproduites par a19, ecart de 0,7 a
   0,8 point sur 177 et 169 items, avec la meme conclusion des deux cotes (a19 point 2).
9. `income` reste dans les 149 items alors que `gss_v6` le recopie a 0,994 et que B1 le recoit en
   attribut ; l'effet mesure est de 0,28 point sur `v6` seulement, mais le perimetre n'a pas ete
   change et il sert a a2, a7, a8, a12 et au run a5 (a17 objection 10, a19).
10. Le compte des victoires par famille de a8 melange des points et des differences, et
    l'inversion de classement des trois mesures sur le terme intra de a1 n'est pas traitee (a17
    objections 4.2 et 1.5).

**Limites propres au run, listees par a23 lui meme.**

- **Les prompts de C2 et C3 n'ont pas ete compares a ceux de `v8` et des agents enquete.** Toute
  la section 2 de a23 attribue au modele un ecart qui peut venir de la formulation. C'est la
  limite la plus serieuse du rapport (a23 point 4, a5 limite 4).
- **Un seul modele, Qwen3-4B-Instruct-2507 en Q4_K_M.** L'absence de gonflement de C3, qui est le
  resultat le plus interessant, peut etre une incapacite du modele plutot qu'une propriete du
  regime sans etiquette. Rien ne separe les deux tant qu'un second modele n'a pas tourne (a23
  point 5).
- **La famille des libertes civiles est un resultat post hoc.** C3 y est nominalement premier des
  douze methodes non humaines a 0,8018, distinguablement au dessus de B1 et de B0 mode, mais la
  famille a ete choisie apres avoir vu les chiffres, sur 36 comparaisons sans correction, et C3
  n'y est distinguable ni de B2 ni des agents de Stanford. A repliquer, pas a annoncer (a23
  sections 1.2 et 6, point 10).
- **Le biais de position n'est pas mesure.** La passe 2 de C3 n'existe pas, sur des items ou une
  seule modalite est predite pour plus de 90 pour cent des personnes dans 43 cas sur 149 (a23
  point 3, a5, a18).
- **Les 30 rejets de C3 n'ont pas ete retires de l'evaluation** : effet estime negligeable, 30
  cellules sur 22 350, non mesure (a23 point 9).
- **Le seuil d'occupation de Miller Madow reste un degre de liberte** sur la voie
  distributionnelle en entropie : inter 132,30 au seuil 1 contre 82,78 au seuil 0 pour C2, et
  33,41 contre -9,91 pour C3. Gini Simpson y est insensible et donne le meme signe et le meme
  classement, mais le choix n'est pas source (a23 point 8, a18 section 2.2).
- **Les intervalles par axe sont des percentiles translates sur l'estimation ponctuelle**, comme
  dans a1 et a18, et non un bootstrap de base (a23 point 7, a19 errata E3).
- **L'extension de C2 a 300 personnes n'a pas tourne** : la question "le controle se resserre t
  il de 150 a 300" n'est pas testee, elle est seulement devenue moins urgente (a23 point 2).

**Limites transversales du dossier.**

- **La licence de l'archive OSF t6g7k est nulle via l'API, donc tous droits reserves.** Reanalyse
  locale seulement, aucune redistribution (a10). C'est le point le plus grave du dossier, parce
  que le seul atout non copiable du projet, le plafond humain test retest, vient entierement de
  ce fichier (a13).
- **Qwen3 ne publie aucune date de coupure**, verifie dans trois sources : il ne peut donc pas
  porter le volet contamination (a3). Les deux modeles a coupure documentee sont Llama 3.1 8B,
  decembre 2023, et gpt-oss-20b, juin 2024.
- **Sur Twin, les trois mesures ne s'accordent plus** : l'entropie dit double distorsion, la
  variance ordinale dit aplatissement des deux termes, intra 0,06 a 0,22. Il est interdit
  d'ecrire "la double distorsion" sans nommer la mesure (a6).
- **Le silhouette de 0,19 n'est pas reproductible en l'etat** : la source ne publie pas son jeu
  d'items, et restreindre aux 57 items attitudinaux du GSS eloigne du chiffre au lieu d'en
  rapprocher (a10, a6).
- **L'ideologie politique n'est pas une variable demographique**, c'est une attitude auto
  declaree, et l'effet principal repose dessus (a1, a15, a23).
- **Le residu de permutation atteint 33 a 40 pour cent sur deux sous ensembles de a6** : ordres
  de grandeur seulement.
- **Le bloc des preferences de prix de Twin porte 37 pour cent des items et 100 pour cent de
  l'avantage du modele**, avec un soupcon de contamination non teste (a8).

**Une limite est levee.** La phrase "150 personnes ne suffisent probablement pas a estimer le
terme inter" tombe en partie : le controle passe a 150 sur l'agregat, sur l'ideologie, sur le
profil croise et sur l'age. Il ne passe pas sur la race ni sur l'education (a23 section 3.1).

---

## Ce qui reste a calculer, par priorite

Sur le Mac M5 32 Gio, un seul `llama-server` a la fois : la regle vaut un facteur 9,5 sur le
debit, mesure (a5 section 4.4).

| rang | chantier | ce qu'il tranche | cout machine | commande ou script |
|---|---|---|---|---|
| 1 | **Un modele plus gros en local sur C2 et C3, gpt-oss-20b puis Qwen3-30B-A3B** | si l'absence de gonflement de C3, l'ECE de 0,44 et la quasi degenerescence sont des proprietes de Qwen3-4B Q4 ou du regime sans etiquette ; c'est la question qui porte le resultat principal (a23, a3) | **11 h 48** sur gpt-oss-20b, **13 h 36** sur Qwen3-30B-A3B pour les deux conditions ; une nuit pour C2 seule [ESTIMATION] | `analyses/a5_agents_locaux_gss.py`, **mais il n'a pas de drapeau de modele** : les constantes `MODELE` et `MODELE_NOM` sont en dur aux lignes 81 et 95, et il faut aussi changer `--suffixe` pour ne pas melanger les traces. Les deux fichiers sont deja installes, `data/modeles/gguf/gpt-oss-20b-MXFP4.gguf` et `Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf`. Prevoir l'edition avant de lancer. |
| 2 | **La correction du scoring au dela de huit modalites** | 25 des 30 rejets de C3 portent sur `income`, a douze modalites et treize lettres, avec une masse sur les lettres descendant a 0,0991 : la regle de scoring par lettre unique n'est pas robuste au dela de sept ou huit modalites (a23 section 0) | zero heure machine, c'est une decision de protocole plus une relecture des traces | deux options exclusives, a trancher avant tout run suivant : retirer `income` des 149 items, ce que a19 suggerait deja pour une autre raison, ou changer de regle de scoring pour les items a plus de huit modalites, ce qui casse la comparabilite avec a2. Le controle 2 de `a5_agents_locaux_gss.py`, section 3, est l'endroit ou la masse est deja enregistree. |
| 3 | **La passe 2 de C3, ordre des modalites inverse** | l'ampleur du biais de position, aujourd'hui inconnue, sur des items ou le modele colle a une modalite dans 43 cas sur 149 (a23, a5 section 6) | environ une nuit sur le GSS ; presque gratuit sur Twin si entrelace sur le meme cache de prefixe | `.venv/bin/python analyses/a5_agents_locaux_gss.py --conditions C3 --passe 2 --fin HH:MM` ; `a5_evaluer.py` detecte la passe 2 seul, moyenne les deux passes au niveau des modalites et rapporte chaque passe separement |
| 4 | **C3F complete, 150 personnes** | la seule reponse propre a l'objection 1 de a17 ; le chiffre attendu est inferieur ou egal a 0,6249, donc sous la cible de 0,6621 (a23 section 6.2) | **3 h 24** au debit reel de 2 556 appels par heure, resumable | `.venv/bin/python analyses/a5_agents_locaux_gss.py --conditions C3 --familles --fin HH:MM` ; la trace en cours, `data/traces/a5-C3F-p1.jsonl`, est reprise automatiquement, cle (condition, passe, pid, item) |
| 5 | **Twin-2K-500, nuit dediee** | la comparaison a information egale avec GPT-4.1-mini, seul argument fort de cette experience ; C3b-Twin et C2-Twin completes en trois heures, puis C3-Twin sur environ 55 personnes (a11 section 6.4) | **7 h**, une nuit entiere, machine libre | `nohup .venv/bin/python analyses/a11_agents_locaux_twin.py --fin 07:30 > data/traces/a11-run.log 2>&1 &` puis `.venv/bin/python analyses/a11_evaluer_twin.py` ; sans `--attendre-a5`, le garde fou refuse de demarrer si un `llama-server` traine |
| 6 | **Llama 3.1 8B pour la contamination** | le seul volet ou une date de coupure documentee est indispensable, decembre 2023 ; Qwen3 ne peut pas le porter, il ne publie aucune coupure (a3) | **10 h 50 a 12 h 10** pour 45 000 appels, plancher non stabilise | meme script que le rang 1, meme edition de constante, sur `data/modeles/gguf/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf` ; le jeu de validation posterieur a la coupure est le barometre CEVIPOF du 4 juin 2026 (PASSATION section 6) |
| 7 | **Extension de C2 a 300 personnes** | elle a perdu son urgence, le controle passe deja a 150 sur les trois axes qui portent l'effet ; elle reste le seul moyen de savoir si l'intervalle se resserre (a23, a21) | **2 h 03** a 11 000 appels par heure, resumable ; la fenetre de cette nuit en couvre une partie jusqu'a 08 h 30 | `.venv/bin/python analyses/a21_extension_c2.py --fin HH:MM >> data/traces/a5-ext.log 2>&1` puis `.venv/bin/python analyses/a21_evaluer_ext.py` |
| 8 | **WVS vague 7** | le seul moyen de reproduire le protocole du silhouette 0,19 et de tester le pays comme axe cache, qui est l'axe reel des facteurs 2,3 et 2,5 (a10, a6, a1) | acces a demander, le jeu est absent de `data/`, cout de calcul non chiffre | aucun script existant ; premiere etape non machine, obtenir l'acces au fichier de la vague 7 et lire sa licence |

**Deux chantiers gratuits qui passent avant tout calcul**, parce qu'ils se font sur les traces
et les fichiers deja produits : la reallocation de l'ICC de Garzon sur nos huit conditions, la
segmentation age croise genre depuis `a1-ratios-par-axe.csv`, et le balayage de temperature sur
C2, qui se recalcule sans un seul appel puisque la distribution complete est deja lue (a18
section 6, a23 rang 2 de sa propre liste).

---

## Questions pour Simon

Douze questions, fusionnees et dedoublonnees a partir des dix neuf rapports, mises a jour par
a23, classees par ce qu'elles debloquent.

### Ce qui debloque la these et le format de publication

1. **C3 ne gonfle rien. Est ce un resultat ou une incapacite ?** C'est la question la plus
   importante du dossier au 8 septembre. Si un modele plus gros dans le meme regime sans
   etiquette gonfle comme les agents enquete de Stanford, alors l'essentialisme identitaire est
   une propriete qui apparait avec la capacite, ce qui est un resultat fort et publiable. S'il
   ne gonfle pas non plus, le gonflement du regime questionnaire est une propriete de la chaine
   de Stanford, invite comprise, et le papier change de cible. Une nuit de calcul tranche.
   Laquelle des deux hypotheses faut il chercher a falsifier en premier ? (a23)
2. **Nos agents sont domines par une regression logistique sur les deux axes du plan. Que fait
   on de ce chiffre dans le papier ?** Le cacher est impossible, un relecteur le refera. Le
   publier affaiblit toute revendication de simulation. La position defendable est que le papier
   ne porte pas sur la performance mais sur la mesure de structure, et que nos agents servent de
   banc a information controlee et non de proposition de simulation. Est ce tenable ? (a23)
3. **La revendication s'est retractee trois fois en une nuit. Est ce encore un papier ?** Apres
   "les LLM ecrasent la variance", puis "la double distorsion" que LifeMem publie dans son resume
   du 20 aout, puis la mesure conjointe des deux termes que Kim et Lee publient depuis 2023 et
   Bisbee et al. depuis 2024, il reste le plafond humain test retest, la dissociation entre
   exactitude et structure a un facteur 13,5, et desormais le contraste a information controlee
   C2 contre C3. Est ce un papier, ou une section de methode dans le papier de quelqu'un
   d'autre ? (a13, a15, a23)
4. **Les trois issues de a15 sont fausses toutes les trois. Faut il republier la question ou
   publier la quatrieme issue ?** Ce qui est observe est un emboitement : l'etiquette commande le
   signe, l'axe commande la repartition a l'interieur de la condition etiquetee. C'est plus vrai
   et moins vendeur que "l'axe de segmentation separe les camps". (a23, a15)
5. **L'axe de segmentation reste la variable centrale, et c'est une attitude auto declaree.** Un
   relecteur de sciences sociales objectera que nous predisons des attitudes a partir d'une
   attitude. Faut il un second axe non attitudinal qui gonfle, religion ou milieu de residence,
   pour tenir ? (a15, a1, a6, a23)
6. **Le critere A6 ayant echoue deux fois pour des raisons independantes, l'une arithmetique et
   l'autre empirique, combien de tentatives avant de declarer close la piste du transport et de
   basculer sur la famille B, le conditionnement ?** La reponse du run pousse dans ce sens : le
   deficit n'est ni dans le decodage, ni dans la repartition entre groupes. (a20, a7, a18, a23)

### Ce qui debloque le plan de calcul

7. **Faut il garder la famille des libertes civiles dans le dossier ?** Elle est le seul endroit
   ou notre agent est en tete des douze methodes non humaines, elle a ete trouvee apres coup, et
   C3 n'y est distinguable ni de B2 ni des agents de Stanford. La garder demande une replication
   preinscrite sur un autre decoupage ; la retirer laisse le rapport sans aucun regime favorable.
   (a23)
8. **Les 25 rejets sur `income` posent une question de protocole.** La regle de scoring par
   lettre unique perd sa masse au dela de sept ou huit modalites. Faut il retirer `income` des
   149 items, comme a19 le suggerait deja pour une autre raison, ou changer de regle de scoring
   pour les items a plus de huit modalites, ce qui casse la comparabilite avec a2 ? (a23, a19)
9. **Twin-2K-500 demande sa propre nuit. Laquelle des quatre sorties prend on ?** Moins de
   personnes, un persona plus court, un modele plus petit, ou une nuit dediee. Le persona complet
   coute 349 secondes de prefill par personne et 10 h 45 pour une seule condition. (a11)
10. **Quel jeu porte le papier ?** Twin-2K-500 donne treize configurations sur treize dans le
    quadrant, un retest humain propre, 2 058 personnes, une licence CC BY 4.0 et deux familles de
    modeles ; le GSS garde la comparabilite avec le papier de Stanford et porte desormais notre
    seul plan a information controlee, mais son paquet n'a aucune licence. Un papier a deux jeux,
    ou un papier Twin avec le GSS en replication ? (a6, a10, a23)

### Ce qui debloque le droit, les contacts et la redaction

11. **Le seul atout non copiable du projet repose sur un fichier sans licence declaree, et le
    precedent le plus proche est co signe par Bernstein et par Kamphorst.** L'archive OSF t6g7k
    renvoie une licence nulle via l'API, donc tous droits reserves : demande t on aux auteurs une
    autorisation d'usage par ecrit, en meme temps que la demande d'adresse institutionnelle ? Et
    faut il ecrire a Kamphorst, a Sciences Po et auteur correspondant, plutot qu'a Stanford, pour
    les trois sujets a soumettre aux auteurs : les deux generations demographiques, les deux
    liens de reproductibilite qui ne contiennent pas ce qu'ils annoncent, et le sens du sigle
    LA ? (a10, a13, a14, a16)
12. **Deux questions de psychologie que le calcul ne tranchera pas, et le vocabulaire.** Existe t
    il un construit nomme pour une propension individuelle a s'ecarter de la position modale de
    son groupe, faiblement transversale mais tres stable dans le temps sur un contenu donne, et
    que dire d'un agent dont la deviance **depasse** celle des humains, 0,409 et 0,429 contre
    0,396, sans etre placee sur les memes personnes, cas qu'aucun papier lu ne decrit ? Quelle
    est la valeur admise de l'effet de faux consensus, sachant que nos humains sont a 0,198 et
    l'agent a 0,723 ? Et sur le vocabulaire : "transport" et "redistribution" sont pris par trois
    papiers de 2026 dans trois sens differents, la proposition est "reallocation de variance a
    total fixe" ; le volet delai de retest doit il porter une proposition de norme, tout score
    normalise declare son delai, son mode de collecte et son traitement des non reponses, et ce
    genre de proposition se publie t il, et ou ? (a9, a23, a13, a10, a12, a14)

---

## Comment reprendre ce matin

### 1. Verifier l'etat des deux calculs qui tournaient

```
cd /Users/amirkellousidhoum/Desktop/Code/Projets/popsim
grep -E "appels|TERMINE" data/traces/a5-familles.log | tail -5
tail -5 data/traces/a5-ext.log
wc -l data/traces/a5-C3F-p1.jsonl data/traces/a5-ext-p1.jsonl
pgrep -fl llama-server
```

C3F devait s'arreter a 06 h 20 sur environ 57 personnes ; l'extension de C2 devait prendre la
suite jusqu'a 08 h 30. **Ne rien lancer tant que `pgrep` renvoie un serveur** : deux serveurs
simultanes coutent un facteur 9,5 sur le debit, mesure (a5 section 4.4).

### 2. Evaluer C3F

`analyses/a5_evaluer.py` traite C3F sans modification : il la detecte seule, la restreint aux
58 items des six familles et recalcule le plafond humain famille par famille (a5 section 6,
`a5_evaluer.py` ligne 350).

```
.venv/bin/python analyses/a5_evaluer.py
```

**La seule comparaison qui compte est C3F contre la ligne "B2 famille retiree" de
`resultats/a8-familles-gss.csv`, a 0,6621, et jamais C3 contre elle.** C3 vaut 0,6249 sur ces
memes 58 items et C3F lui est necessairement inferieur ou egal, l'arithmetique ne pouvant jouer
que dans un sens : la valeur attendue est sous la cible, et le chiffre reel sert a le mesurer,
pas a le decouvrir (a23 section 6.2). Lire aussi le nombre de personnes completes : sous 57, le
chiffre porte un intervalle large et doit etre publie avec.

### 3. Evaluer l'extension de C2

```
.venv/bin/python analyses/a21_evaluer_ext.py --rapide     # essai, 20 s
.venv/bin/python analyses/a21_evaluer_ext.py              # 150, 150 et 300 cote a cote
```

Ce qu'il faut regarder : le controle de la vague 2 se resserre t il en passant de 150 a 300 sur
le genre, la race et l'education. **Si oui**, les ratios inter deviennent publiables sur plus
d'axes. **Si non**, le probleme n'est pas la taille d'echantillon mais l'estimateur, et il faut
soit monter a 400 personnes, soit passer a un estimateur bayesien du type NSB (a21, a18). La
troncature coute des personnes entieres et jamais des items ; le script est resumable et une
relance de jour termine ce qui manque (a21).

### 4. Ou lire quoi, dans l'ordre recommande

| ordre | fichier | ce qu'on y trouve en une ligne |
|---|---|---|
| 1 | `resultats/a23-resultats-du-run.md` | le seul rapport ecrit sur les traces completes : ce que le run detruit, ce qu'il etablit, et les six questions tranchees |
| 2 | ce document, `SYNTHESE-NUIT-2026-09-08.md` | l'etat de la these au 8 septembre, le tableau des chiffres avec leur statut, et le plan de calcul par priorite |
| 3 | `resultats/a19-errata.md` | tous les chiffres corriges de la nuit et les lignes a changer dans les documents de pilotage |
| 4 | `resultats/a17-relecture-adverse.md` | les dix objections les plus graves du dossier, dans l'ordre ou un relecteur les trouvera |
| 5 | `resultats/a18-decomposition-c2-c3.md` | la methode de la decomposition inter et intra, la version distributionnelle et ses deux controles ; ses chiffres sont partiels, ceux de a23 les remplacent |
| 6 | `resultats/a20-transport-de-variance-v2.md` | pourquoi le transport a somme constante ne peut pas marcher, sous les trois mesures |
| 7 | `resultats/a6-double-distorsion-hors-gss.md` | la double distorsion sur Twin-2K-500 et sur deux autres jeux, et le desaccord entre mesures qu'il faut declarer |
| 8 | `resultats/a15-gonflement-ou-aplatissement.md` | la reconciliation de la litterature par l'axe de segmentation, a rouvrir a la lumiere de a23 |
| 9 | `resultats/a13-positionnement-contribution.md` | ce que les quatre travaux voisins publient deja, et les deux paragraphes de related work en anglais |
| 10 | `resultats/a12-delai-de-retest.md` | le second angle propre, le denominateur qui deplace le score de dix a treize points |
| 11 | `resultats/a5-agents-locaux-gss.md` | comment le run a ete construit, le scoring et ses quatre controles, le facteur 9,5 des deux serveurs |
| 12 | `resultats/a11-agents-locaux-twin.md` | ce que coute Twin-2K-500 et la commande de sa nuit dediee, section 6.4 |
| 13 | `JOURNAL-NUIT-2026-09-07.md` | le fil de la nuit heure par heure, y compris les incidents et les decisions d'orchestration |

Les autres rapports, a8, a9, a10, a14, a16 et a21, se lisent a la demande : leurs conclusions
sont reprises dans les tableaux ci dessus avec leur source.

---

## Addendum 06:25, C3F partiel (60 personnes sur 150)

C3F, nos agents C3 prives de la famille entiere de l'item predit, a tourne de 05:02 a 06:20 :
3 498 appels, 60 personnes completes, trace resumable. Sur les 58 items de famille : C3F
0,5617 [0,5365 ; 0,5876] contre C3 0,6249 sur les memes items (a23) et contre la cible
0,6621 de B2 en regime famille retiree (a8, 1 052 personnes). Famille par famille, C3F est
sous C3 partout (-4,7 a -10 points) et sous la modalite majoritaire dans quatre familles sur
six ; diversite conservee 56,6 pour cent. Comparaison indicative, les 60 personnes de C3F ne
sont pas les 150 des autres lignes ; sortie complete dans data/traces/evaluation-c3f.log.
Lecture : le regime "question jamais posee dans ce domaine" n'est pas un terrain ou l'agent
local de 4 milliards gagne, il y perd contre la modalite majoritaire. L'objection 1 de a17 sur
a8 est close dans le sens defavorable au modele de langage, pour ce modele. Reste ouvert, comme
pour C3 : resultat, ou incapacite du petit modele. Pour finir C3F sur 150 personnes :
`.venv/bin/python analyses/a5_agents_locaux_gss.py --conditions C3 --familles --fin 23:59`
(environ 2 h 10 restantes, seul sur la machine).

## Addendum 07:35, extension de C2 a 300 personnes, terminee

L'extension (a21) a fini ses 22 350 appels a 07:29. Sur l'union des 300 personnes, le
controle vague 2 passe : 1,019 en agrege, 1,04 sur l'ideologie, 1,07 sur la race, 1,01 sur
l'education, 0,99 sur le profil croise, 1,09 sur l'age, 0,85 sur le genre (seul axe encore
inexploitable). Les ratios inter de C2 sont publiables sur cinq axes. C2 sur 300 : exactitude
0,5285 [0,5212 ; 0,5355], inter 4,80, intra 0,567, total 0,665 ; ideologie 7,64 contre 8,60
pour v8 et 0,21 pour v6. Les 150 personnes tirees independamment redonnent 6,53 : le
gonflement commande par l'etiquette ideologique se replique sur un second echantillon.
Sortie complete : data/traces/evaluation-ext.log ; tableaux resultats/a21-decomposition.csv
et a21-ratios-par-axe.csv. La limite "150 personnes ne suffisent pas" est levee pour C2.
