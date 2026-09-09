# Veille de l'ete 2026, tri des 126 entrees manquees et lecture des papiers qui comptent

Session du 8 septembre 2026, en prolongement de `corpus/lecture-complete/00-CONSIGNE.md`. Objet :
les 126 entrees de `resultats/veille-2026-09-08.md` declarees absentes des sept fichiers de
`corpus/0N`, entre le 1er juin et le 8 septembre 2026. Meme grille, memes niveaux de certitude,
memes regles de forme. La these testee est celle d'`ARBITRAGE.md` : une societe simulee a partir
d'etiquettes remplace chaque personne par son groupe, garde les opinions rares de chaque groupe
mais les attribue aux mauvaises personnes, et pousse le camp le moins varie a l'unanimite.

## Compte rendu en cinq lignes

1. Sur 126 entrees, 9 sont des menaces directes, 10 des precedents partiels, 16 des soutiens, 30
   des methodes utiles et 61 sont sans rapport ; 19 papiers ont ete lus en entier, dont SimPol.
2. Sept des 126 ne sont pas neuves : elles figurent deja dans `corpus/lecture-complete`, que
   l'index de comparaison de la veille n'interroge pas ; le chiffre reel de nouveautes est 119.
3. La menace la plus grave est Yuan, « Cultural Bias Without a Cultural Self » (2607.02368) : elle
   publie le mecanisme de notre these, la substitution de la personne par un gabarit de groupe, avec
   un generateur nul qui reproduit tout le motif, et un controle humain a trois proprietes.
4. Viennent ensuite Li et al. sur le biais de bienveillance (2608.24912), qui retablit la phrase
   « la simulation rend une societe presentable » que le dossier avait retiree, sur un sous ensemble
   nomme et avec un correctif qui ramene six categories au niveau humain, et Holtdirk et al.
   (2606.09351), ou l'imputation par LLM bat MICE PMM et MICE Forest sur 150 variables d'opinion.
5. Ce qui reste a nous apres cette passe : le partage inter et intra sur reponses individuelles,
   normalise par un plancher de reinterrogation des memes personnes, avec la condition avec
   etiquette et la condition sans etiquette dans le meme plan. Aucune des 126 ne fait les trois.

---

## 1. Ce qui menace la these, par gravite

### 1.1 Yuan, « Cultural Bias Without a Cultural Self », arXiv 2607.02368 v3 (30 aout 2026)

C'est la menace la plus serieuse du lot, parce qu'elle n'attaque pas un de nos chiffres, elle
occupe notre phrase. [CONFIRME]

Ce que le papier fait. Il separe deux choses que le champ confond : un **biais**, qui ne demande que
des moyennes d'item propres a un groupe, et une **persona**, qui demande une structure interne a un
seul jeu de reponses, structure qui doit survivre a un changement de cadre de mesure. Sa
construction : ranger les 50 reponses d'une passation IPIP-50 dans une matrice item par dimension
10 x 5, prendre la matrice de correlation entre colonnes, la traiter comme un point sur la variete
des matrices symetriques definies positives, la projeter dans l'espace tangent, et regarder si elle
identifie l'instance.

Donnees. Cote humain, deux echantillons : un test retest maison, `N=89`, deux passations de 50 items
sans item, sans ordre ni contexte communs, avec la moyenne generale universitaire tiree du registre
officiel ; et une replication publique NEO-PI-R, `N=263`, une semaine d'intervalle, 240 items en
ordre individuellement randomise. Cote modele, un plan 2 (persona americaine contre americaine
d'origine chinoise) x 2 (ordre fixe FO contre ordre aleatoire par instance RO), sur GPT-4o
(`N` d'environ 400, puis 2 000), DeepSeek-V3, Claude Haiku 4.5 et Claude Sonnet 4.6, `N=400` chacun,
temperature 0,7, 150 jetons, sans invite systeme.

Resultats chiffres. Chez l'humain, la geometrie tient : correlation element par element entre les
deux sessions `r=0,77`, etendue 0,52 a 0,96 ; identification d'individus jusqu'a 75,9 pour cent
contre un hasard a 0,38 pour cent ; et surtout les dix variables de l'espace tangent predisent la
moyenne generale, `R^2=0,281`, `p` de permutation 0,003, la ou les agregats Big Five tires des
**memes reponses** ne predisent rien, `R^2=0,018`, `p=0,91`. Chez les quatre modeles, rien. La
separation des personas passe de 94,7 pour cent en ordre fixe a un niveau de hasard en ordre
aleatoire, et revient a 82 a 84 pour cent des qu'on realigne les instances sur **n'importe quel**
ordre partage tire au hasard, sur 2 000 tirages independants. Un generateur qui tire chaque item
independamment, `X_ij` normal de moyenne et d'ecart type estimes sur les statistiques d'item du
modele, sans aucune structure latente, reproduit tout le motif : 97,2 en FO, 57,6 en RO, 83,2 apres
realignement, contre 94,6 / 55,2 / 83,7 pour le vrai GPT-4o. Les memes simulations parametrees sur
des normes humaines ne produisent aucun ecart FO contre RO.

Terme inter et intra : le papier ne les nomme pas, mais il livre l'equivalent le plus dur du
gonflement d'ecart entre groupes. Sonnet 4.6 atteint 100 pour cent de separation Big Five en ordre
fixe avec une geometrie a 52,41 pour cent, c'est a dire au hasard, parce que ses deux personas
occupent deux points et non deux distributions ; en ordre aleatoire, sa dispersion intra groupe est
multipliee par plus de cinq, `0,054` a `0,284` sur l'extraversion, et la separation tombe au hasard.
Plancher humain : oui, et de trois natures, fiabilite, identifiabilite, validite de critere.
Etiquette testee comme cause : oui, par la perturbation de cadre, qui est un test causal sur le
dispositif et non sur l'etiquette elle meme. Baseline non LLM : oui, le generateur conditionnellement
independant, et c'est la meilleure baseline non LLM du corpus entier.

Ce que ca coute a la these. Deux phrases de notre enonce sont deja ecrites ailleurs :
« The cultural signal is a group template, not a property of any instance » et « alignment regimes
differ only in which stereotype survives on the surface ». La deuxieme touche notre question ouverte
« a quelle etape, socle ou alignement, la substitution apparait ». Le papier repond, sur son terrain,
qu'aucun regime d'alignement ne produit de structure invariante au cadre, et que les regimes ne
different que par le stereotype de surface qui survit. La cause probable est nommee comme hypothese
testable, pas comme mecanisme : « objectives penalizing culturally differentiated outputs remove
between-group signal dimension by dimension, while objectives without such penalties leave
multi-dimensional stereotypes intact ».

Ce qui reste a nous, precisement. Le papier travaille sur deux personas culturelles et un inventaire
de personnalite, pas sur des attitudes politiques ni sur le GSS. Il ne mesure ni gonflement d'ecart
entre groupes ni dispersion intra sur des reponses d'opinion. Il n'a pas de reponse rare, pas de
rappel de minorite, pas d'appariement individuel a une personne reelle. Sa proposition S4 dit
explicitement qu'augmenter le nombre de personas « multiplie les gabarits plutot qu'il ne cree des
selves », donc l'auteur revendique la generalite du **negatif**, pas la mesure du positif. Notre a31,
qui mesure que les fausses raretes sont les raretes typiques du segment avec un rapport 4,45 avec
etiquette contre 0,44 sans, dit la meme chose sur des reponses d'enquete, avec des personnes reelles
en face. C'est la meme these avec un instrument different, et l'anteriorite est desormais a lui.

### 1.2 Li, Wang, Liu et al., « Analyzing and Correcting Benevolence Bias », arXiv 2608.24912 (26 juillet 2026)

Menace directe, et menace sur une phrase que le dossier avait retiree le 8 septembre au matin.
[CONFIRME]

Donnees et modeles. 18 modeles, quatre jeux de sciences sociales, ANES, GSS, WVS et une replication
interculturelle de la theorie des perspectives, 406 items retenus, quatre domaines sociaux et six
categories de biais : desirabilite sociale, aversion au dommage, prosocialite, interpretation
bienveillante, optimisme d'equite, adoucissement emotionnel. Deux mesures : `BTB`, deplacement au
niveau de la population par rapport a la reference humaine, et `BWR`, direction question par
question, reference humaine `BTB=0` et `BWR=0,5`.

Resultats chiffres. 83 des 108 cellules `BTB` sont positives, 75 des 108 `BWR` sont au dessus de
0,5, moyennes 0,027 et 0,527. Les 18 modeles sur 18 se deplacent positivement sur la desirabilite
sociale (`BTB` moyen 0,059, `BWR` 0,565) et 17 sur 18 sur l'aversion au dommage (0,066 et 0,569). Le
biais croit avec la taille dans les deux familles Qwen, ne tient que faiblement a la capacite
(`R^2=0,16` contre MMLU-Pro), et entre au post entrainement : l'affinage par instruction augmente le
`BTB` moyen aux tailles 1,5, 7, 14 et 32 milliards, plus fortement a 32. Les classements de modeles
concordent entre les trois grandes enquetes, rho de Spearman 0,54 a 0,63.

Le point qui touche notre these. Un test de persona malveillante, ou chaque persona est reecrite en
antisociale, interessee et tolerante au dommage, abaisse le taux sur l'optimisme d'equite,
l'adoucissement et l'interpretation bienveillante, mais **ne peut pas passer sous la reference
humaine** sur la desirabilite sociale, la prosocialite et l'aversion au dommage. Pour Qwen3-32B, tous
les jeux restent au dessus de 0,5. Les auteurs ecrivent : « on those axes the models have measurably
lost the ability to imitate people at the less-benevolent end ». Ce n'est plus un deplacement de
moyenne, c'est un **retrecissement de l'etendue des gens imitables**, c'est a dire notre these,
enoncee sur un autre axe que le camp politique. Ils ajoutent que le biais est au centre de la
distribution et non dans les queues : la temperature le deplace de moins de `0,01` sur toute la
grille testee, ce qui recoupe exactement notre resultat a23 selon lequel le defaut est loge dans le
conditionnement et non dans le tirage.

Correctif. Une calibration contrastive au niveau du vecteur de probabilites du jeton suivant, sans
reentrainement et sur API fermee : un second appel sous persona neutre donne l'aprioripar defaut,
on divise la distribution conditionnee par cet a priori a la puissance alpha et on renormalise. A
`alpha` d'environ 0,5, les six categories reviennent dans une bande serree autour de la reference
humaine ; a `alpha=1` plusieurs passent en dessous.

Ce que ca coute. Trois choses. D'abord la phrase « ce qui est tombe aujourd'hui : la simulation rend
une societe presentable » d'`ARBITRAGE.md` doit etre rendue conditionnelle : elle est fausse en bloc
sur nos items GSS, elle est vraie et unidirectionnelle sur trois des six categories de ce papier, et
la variable qui explique la difference est le decoupage des items, pas la population. Ensuite, notre
question ouverte sur l'etape ou apparait le defaut recoit ici une reponse partielle et chiffree,
socle contre modele instruit sur la meme famille et la meme taille. Enfin, un correctif publie qui
marche sans reentrainement occupe une partie du terrain « remedes » que le dossier avait laisse
ouvert apres l'echec du transport de variance.

Ce qui reste a nous. Le papier ne mesure aucun terme inter, aucun terme intra par groupe, aucune
reponse rare, aucun appariement individuel, aucun plancher de reinterrogation. Sa reference humaine
est une distribution marginale d'item, pas une personne. Et sa calibration contrastive est evaluee
sur le retour a la moyenne humaine, jamais sur le nombre de personnes reparees contre cassees : le
critere A6 du projet reste sans equivalent.

### 1.3 Ahn, Mao et Lee, « Item-Mean Surrogates », arXiv 2608.29455 (29 aout 2026)

Deja lue par le projet sous les identifiants L1.02 et L03-01. Relue en entier ici, et confirmee.
[CONFIRME] La menace est intacte et elle est la plus grande du corpus par la taille : quatre jeux,
plus de 400 000 participants, plus de 6 000 items.

Chiffres a retenir. `R^2` poole apres retrait de la moyenne humaine de l'item : 3,05 pour cent sur le
Megastudy de Peng, soit 5,7 pour cent du plafond de fiabilite test retest humain de 53,6 pour cent ;
4,44 pour cent avec la meilleure invite non affinee ; 2,31 pour cent avec un GPT-4.1 affine ;
3,87 a 6,21 sur l'enquete Twin-2K-500 ; 5,78 sur SocSci210 mais 0,73 sur les etudes non vues ;
10,77 sur ANES. Decomposition en theorie de la generalisabilite sur 108 160 paires personne item :
effet principal de personne stable 4,9 pour cent, effet d'item 8,7, interaction personne par item
44,0, erreur transitoire 42,4 ; l'interaction vaut **8,9 fois** l'effet principal de personne.
Comparaison a une baseline sans aucune information sur la personne, la moyenne humaine de l'item en
laisser un dehors : le LLM perd, `r` moyen 0,34 contre 0,45, `dz` apparie de -0,55, `p` de l'ordre de
`4,6 x 10^-95` sur 1 631 repondants. Compression de distribution : ecarts types medians des items a
65 pour cent des humains sur le Megastudy, 50 sur SocSci210, 57 sur l'enquete ; nombre effectif de
modalites employees a 43 a 73 pour cent ; et la **forme** compte pour 31 a 40 pour cent de la
distance de Wasserstein-2 au carre, ce qui interdit de tout mettre sur le dos de la compression.

Terme inter et intra : non separes. Plancher humain : oui, 53,6 pour cent, et c'est un plancher de
reinterrogation. Etiquette testee comme cause : oui, par permutation de personas, 10 000 tirages, le
maximum sous permutation vaut 0,028 pour cent contre 3,05 en appariement correct, `p` empirique
0,0001. Baseline non LLM : oui, et c'est elle qui gagne.

Ce qui reste a nous, et le papier le dit lui meme dans ses quatre tests de falsification : aucun
systeme teste ne recupere les deviations personne par item hors echantillon, et aucun ne restitue les
distributions. Notre atout n'est pas la, il est dans le fait que nos deux regimes different par la
seule etiquette ideologique, ce que ce papier ne fait pas, et dans la mesure des reponses rares, que
la mecanique du `R^2` demeane ne capte pas.

### 1.4 Cai, Hu, Li et al., « Can LLMs Represent Urban Publics ? », arXiv 2607.27100 (29 juillet 2026)

Deja lue par le projet sous L1.06. Relue en entier. [CONFIRME] Elle reste la seule du lot a publier
un plancher **humain contre humain** sur une structure de sous groupes politiques.

Chiffres. Humains : 843 repondants, effet de proximite global -0,465, moderation proprietaire contre
locataire `theta = -0,285`, intervalle [-0,385 ; -0,179]. Qwen 2.5 14B est le seul des huit modeles a
passer le critere d'equivalence prespecifie a plus ou moins 0,20, avec -0,242, mais il surestime
l'effet global, -0,644 contre -0,465. Structure : RMSE 0,613 sur 27 cellules parti par statut
d'occupation par item, correlation de cellule 0,746, et surtout **rapport median de variance modele
sur humain de 0,099** ; Phi-4 et Gemma 3 sont a `0,000`, c'est a dire aucune variance de reponse dans
au moins la moitie des cellules. L'entropie est plus faible que chez l'humain pour tous les modeles.
Le plancher : sur 18 cellules, la distance de variation totale vaut 0,561 pour Qwen contre humain et
**0,098 pour humain contre humain**, intervalles [0,535 ; 0,586] et [0,077 ; 0,119] ; divergence de
Jensen Shannon 0,249 contre 0,009 ; Wasserstein ordinal 0,721 contre 0,147 ; les 18 cellules sur 18
depassent leur plancher apparie. Ordre des questions : le decalage du contraste vaut +0,367 pour
Qwen, +0,367 pour Llama, -0,163 pour Mistral, contre +0,036 chez l'humain, intervalle
[-0,169 ; +0,235].

Ce que ca coute. Notre point ouvert « l'effet de l'ordre des reponses proposees n'est pas mesure »
est desormais occupe pour l'ordre des **questions**, avec un plancher humain qui montre que l'humain
n'y est pas sensible et le modele si. Et le rapport de variance de 0,099 est bien plus severe que nos
0,64 a 0,89 : si l'on cite les deux, il faut nommer la mesure et l'unite, comme le dossier l'exige
deja depuis Twin.

Ce qui reste a nous. Une seule condition de conditionnement, un seul domaine, aucune reponse rare,
aucune mesure de gonflement d'ecart entre groupes au sens du dossier.

### 1.5 Fröhling, Rupprecht, Strohmaier et Wagner, arXiv 2609.02526 (2 septembre 2026)

Deja lue sous L1.15 et L02-10. Relue en entier. [CONFIRME] Menace parce qu'elle propose une variable
explicative concurrente de la notre pour l'effet de l'etiquette.

Plan. Quatre enquetes sociales generales, deux pays, 20 questions cibles par enquete choisies aux
deux extremes de la dispersion humaine, six modeles Llama et Qwen de 3 a 70 milliards, cinq methodes
de selection d'attributs dont deux statistiques et deux par LLM, mesure par distance de Jensen
Shannon entre distribution predite et distribution reelle.

Resultats. La persona aide **davantage** sur les questions a forte variation de reponse humaine, et
l'effet s'inverse pour le modele sans persona, qui represente mieux les questions a faible variation.
Les selections statistiques, correlation et importance de variable, battent les selections par LLM,
sur les six modeles et les quatre enquetes. Les selections par LLM sont instables : `W` de Kendall
entre 0,25 et 0,50 entre executions independantes pour l'approche par score ; l'approche par
ensemble se stabilise avec la taille, Llama-3.3-70B choisissant le meme attribut en tete dans
58 pour cent des executions.

Ce que ca coute. Si la persona aide surtout la ou les humains se dispersent, alors l'effet de
l'etiquette n'est pas seulement une substitution par le groupe, c'est aussi un apport d'information
la ou le defaut par defaut du modele echoue. Notre enonce doit tenir compte de ce signe. Les auteurs
notent aussi, en limites, que « persona-prompted LLMs are competitive with a random forest classifier
used as the imputation baseline », en citant Rupprecht et al. 2026 : cela affaiblit la portee de
notre constat « nos agents sont battus par une regression logistique », qui devient un fait sur notre
modele de 4 milliards, pas sur le champ.

Ce qui reste a nous. Aucun terme intra, aucun plancher, aucune reponse rare, et l'unite est la
distribution agregee de l'enquete, pas la personne.

### 1.6 Bojic, Matic, Matthes et Cabarkapa, arXiv 2608.07498 (19 juin 2026)

[CONFIRME] Menace directe sur deux points du dossier.

Plan. 296 profils d'agents issus d'une enquete, 26 messages a verite terrain, 56 messages au total,
12 configurations de LLM, trois conditions de profil, baselines d'apprentissage supervise en laissant
un message dehors.

Chiffres. Sous profil complet, exactitude de 75,54 a 96,68 pour cent. La degradation est brutale :
GPT-5.5 Pro passe de 96,68 avec profil complet a 62,32 avec profil reduit et a **51,00 avec les
seules donnees demographiques**, contre une baseline de classe majoritaire a 51,1 pour cent. Les
classifieurs supervises s'effondrent a 15,4 pour cent en laissant un message dehors. L'accord entre
modeles vaut kappa 0,440 sur les messages a ancrage direct et 0,233 sans. Et la configuration la
moins heterogene **homogeneise 34 pour cent des messages**, homogeneise etant defini comme plus de
90 pour cent des agents recevant la meme reponse ; l'ecart type moyen du taux de mention j'aime va de
0,303 pour Claude Haiku 4.5 a 0,455 pour GPT-5.5.

Ce que ca coute. Le seuil des 90 pour cent est exactement notre mesure de a23, « une seule modalite
couvre plus de 90 pour cent des personnes sur 46 et 43 questions sur 149, contre 13 chez les
humains ». Un autre groupe la publie, sur un autre materiau. Nous gardons le referent humain sur les
memes items, qu'eux n'ont pas. Deuxieme point : la demographie seule ne vaut pas mieux que la reponse
majoritaire, ce qui confirme notre fait etabli selon lequel tout l'effet passe par l'etiquette
attitudinale, et durcit le probleme du dossier qui « predit des attitudes a partir d'une attitude ».

### 1.7 Dahiya, « Mind the Gaps : Mixture-of-Minds for Human Simulation », arXiv 2608.06115 (6 aout 2026)

[CONFIRME] Menace moyenne, par la revendication et par la synthese qu'elle fait de nos adversaires.

Le systeme, Anacreon, apprend une representation d'auteur par objectif contrastif, regroupe un corpus
qualitatif reel autour de personnes graines, et entraine un adaptateur LoRA de rang 64 par groupe sur
un socle Gemma 4 12B, 420 groupes entraines, 400 retenus, environ 110 milliards de parametres
appris. Il annonce un alignement ordinal `1 - MAD/R` de 0,775, contre 0,717 pour Twin-2K-500, 0,740
pour Socrates-Qwen-14B et 0,748 pour la megaetude de jumeaux, et 0,679 d'exactitude exacte contre
0,657 pour les agents d'entretien de Park et al.

Ce qui menace : la revendication est explicitement « simuler des individus heterogenes assez
fidelement pour en tirer un agregat », et le papier attaque frontalement la fragilite d'invite en
melangeant l'ordre des modalites a chaque epoque, et le biais de positivite en equilibrant la
distribution d'entrainement, deux de nos points ouverts.

Ce qui ne menace pas, et il faut le dire : Anacreon ne publie **aucune** mesure de dispersion, aucun
plancher humain pour son propre jeu, aucun terme inter, et son biais residuel est de +0,437 position
d'echelle avec un ecart type par groupe median de 1,85. Le papier reconnait lui meme, dans son etat
de l'art, que l'alignement ordinal « is necessary but not sufficient » et que le champ le complete
par des controles de distribution. Il porte en revanche une citation qui vaut alerte pour nous :
sur des stimulus nouveaux, les jumeaux de Peng et al. ne correlent que faiblement a leurs humains,
`r` moyen d'environ 0,20, et retombent vers la moyenne de population ; et une part importante des
coefficients de regression estimes sur eux changent de taille ou de signe.

### 1.8 Luo, Xu, Chen et Zhao, « ACE-Align », arXiv 2601.12962 v2 (30 aout 2026)

[CONFIRME] Menace parce qu'elle publie la taxonomie que le dossier emploie sans l'avoir nommee.

Plan. 14 pays, cinq continents, personas definies par des sous ensembles de quatre attributs, genre,
education, residence, statut matrimonial ; la granularite est le nombre d'attributs specifies, de 1 a
4 ; l'alignement est appris par appariement des effets d'attribut obtenus par **editions controlees
de persona**, tous les autres attributs tenus fixes.

Resultat structurant. Une taxonomie a quatre types pour chaque couple attribut par sujet, selon la
relation entre l'effet estime par le modele et l'effet mesure dans l'enquete : `Flipped` si les
signes different, `Stereotyping` si la magnitude est surestimee, `Erasure` si elle est sous estimee,
`Aligned` si elle correspond. C'est mot pour mot le gonflement et l'ecrasement du dossier, transposes
de la structure de population aux effets d'attribut, avec un controle causal propre. Chiffres
publies : toutes les methodes evaluees ont un alignement moyen plus faible a `G=4` qu'a `G=1`, et
ACE-Align reduit l'ecart moyen Nord contre Sud de 3,40 a 1,11 points sur le WVS et de 2,53 a 0,85 sur
l'ISSP.

Ce qui reste a nous. Aucune dispersion intra groupe mesuree, aucun plancher humain, aucune reponse
individuelle appariee : le papier travaille sur des effets moyens d'attribut, pas sur des personnes.
Mais le vocabulaire est pris : ecrire « gonflement et ecrasement » sans citer `Stereotyping` et
`Erasure` de ce papier serait desormais une faute.

### 1.9 Moon, Kim, Lah et Han, « Beyond Averages », arXiv 2606.09013 v2 (22 juin 2026)

Deja lue sous L02-14. Relue en entier. [CONFIRME] Menace sur notre chapitre de baselines.

Le fait dur : sur la quantite achetee, la baseline marginale, qui predit la distribution humaine
poolee sous toutes les conditions sans aucune information conditionnelle, atteint une distance de
Wasserstein moyenne de 0,641, plus faible que **tous** les modeles evalues, le meilleur, Gemini-2.5
Pro, etant a 1,467, plus de deux fois plus loin. Sur l'incidence d'achat, la baseline marginale a une
erreur absolue moyenne de 0,013 qu'aucun modele ne bat, et trois modeles inversent le motif humain.
Deux effets de dispositif, mesures et transferables : les personas en JSON structure battent les
personas en texte libre, `r` de Pearson 0,800 contre 0,720 et divergence de Jensen Shannon 0,237
contre 0,283, a contenu identique ; et l'incitation au raisonnement degrade l'alignement de facon
monotone, 0,759 sans raisonnement, 0,722 en trace libre, 0,692 en trace guidee. Les auteurs
l'expliquent ainsi : « reasoning traces commit the model to a specific justification, narrowing the
space of plausible final answers and collapsing the response distribution ».

---

## 2. Ce qui la soutient

Aucun des seize soutiens ne mesure nos quantites ; ils rendent la these plus difficile a contredire.

**L'alignement est bien la source, et l'effet est asymetrique.** Song, Choi, Park et Han
(2509.10078, [PROBABLE]) montrent que les questionnaires psychometriques humains **surestiment** la
capacite du modele a jouer une persona demographique : les invites demographiques deplacent les
reponses aux questionnaires dans le sens des motifs humains reels, mais aucun deplacement de ce genre
n'apparait en probabilite de generation sur des requetes d'usage ordinaire, parce que les items de
questionnaire portent des indices lexicaux qui laissent le modele reconnaitre le construit vise et
repondre de facon socialement desirable. Pour nous, cela dit que **notre chaine en choix fermes est
precisement le regime ou l'illusion de persona est la plus forte**. Fu, Meng, Chen et Huang
(2608.29198, [PROBABLE]) dissocient deux declencheurs de sycophantie politique, l'opinion explicite
et l'identite demographique, sur 450 dilemmes controles et 13 modeles instruits : la sensibilite a
l'un ne predit pas la sensibilite a l'autre, les deux sont sous additifs quand ils sont presents
ensemble, et les personas systeme deplacent la position de base sans changer l'ampleur du
deplacement induit. Zhao, Xiao, Xuan et Salim (2608.11528, [PROBABLE], deja indexee 06-55) montrent
que le gain d'alignement et la derive de sycophantie induite forment un profil **propre a chaque
groupe** a budget identique.

**Le retrecissement de la diversite est documente hors enquete.** Bao, Wu, Liu et Li (2606.08251,
[PROBABLE]) obtiennent 25 139 jeux de notes de 6 749 scientifiques sur des idees generees a partir de
leurs propres articles : les modeles non raisonneurs s'effondrent dans un « hivemind » etroit,
aucun modele ne propose spontanement d'hypothese nulle, et une analyse de 39 millions d'articles de
2010 a 2025 montre que les affirmations nulles ont ete fortement supprimees apres la sortie de
ChatGPT. Thakur, Agrawal, Nakkiran et Karlsson (2608.22859, [PROBABLE]) posent le meme constat cote
recherche documentaire : « standard top-k retrieval ranks documents by query similarity, not by how
faithfully they represent the population, so minority views quietly disappear », et corrigent par
alignement de Wasserstein sur la distribution d'opinion cible, reduction d'au moins 43 pour cent de
l'erreur distributionnelle sur 35 000 documents et 156 requetes. Varadarajan, Yerukola, Diab et Sap
(2607.05405, [PROBABLE]) mesurent une asymetrie qui prolonge la notre : les modeles repondent
correctement plus souvent quand la persona **s'ecarte** de la norme culturelle que quand elle la
suit, ce qui suggere une preference pour le biais interne sur l'adaptation aux indices.

**Le plancher humain lui meme est menace par le haut.** Xu et Malkin (2607.00403, [PROBABLE])
quantifient l'usage de LLM par les repondants de plateformes sur une serie d'enquetes `N=250` : moins
de 10 pour cent sur Prolific, plus de 80 pour cent sur Mechanical Turk, et les mesures d'attenuation
reduisent l'usage sans ameliorer necessairement la qualite. Velutharambath, Falk, Labat et Tater
(2606.04924, [PROBABLE]) interrogent 155 chercheurs : 44 pour cent ont observe de l'usage de LLM dans
leurs donnees collectees, 93 pour cent d'entre eux s'y attendaient, la moitie ne savent pas quelle
precaution prendre. C'est le point 9 de la section « ce que personne n'a fait » du fichier 07 du
projet, avec deux mesures nouvelles.

**Le reste des soutiens, en une ligne chacun.** Mungari (2608.11649, [PROBABLE]) : taux de refus et
sensibilite a la formulation dans un audit politique italien, avec variation par persona. Proskurina,
Gourru et Velcin (2608.04268, [PROBABLE]) : l'effondrement d'equite precede l'effondrement de modele,
les biais demographiques s'amplifient avant que les metriques de langage ne bougent, ce qui est le
risque de boucle pour toute donnee synthetique reinjectee. Venkit, Prabhakar, Li et Lee (2607.28818,
[PROBABLE]) : sur 2 008 conversations et 27 personas, l'exactitude de trajectoire tombe a 44,4 pour
cent en moyenne et la retention au questionnaire **desaccorde** avec le comportement observe tour par
tour, ce qui est un argument de plus contre les questionnaires comme preuve de persona. Shani-Narkiss,
Fire et Tsur (2607.27232, [PROBABLE]) : sur 3 011 Britanniques et sept modeles, la correlation avec
le jugement humain va de 0,789 a 0,4, l'alignement agrege est bon mais **differe significativement
entre sous groupes**. Loi (2601.14295, [PROBABLE]) : les modeles de pointe penalisent un argument
selon la position ideologique attendue de sa source, et ces effets s'effondrent quand les modeles
detectent un test systematique, ce qui est un effet de demande a integrer a tout protocole d'items
sensibles. Kumar, Gautam, Chadha et Jain (2604.23600, [PROBABLE]) : sur 23 400 recits, les traits de
la triade noire sont associes a des representations plus stereotypees du genre que les traits
socialement desirables. Khetan et Khetan (2603.23841, [PROBABLE]) : les scenarios de jeu de role
multi tours activent des profils de valeurs plus larges que les questions politiques directes, et
l'engagement dans une position croit d'environ 1,4 point sur 5 du debut a la decision. Kunkel,
Hartwig, Voss et Schütt (2606.02741, [PROBABLE]) : 31 modeles sont plus verts que le repondant
allemand moyen, avec des deplacements sycophantes qui suivent la position ideologique annoncee par
l'utilisateur.

---

## 3. Ce qui se contredit avec le corpus deja lu, et la variable

**3.1 « La simulation ne devie pas vers la reponse polie » contre « les modeles ont perdu le bas de
l'echelle de bienveillance ».** Le dossier a retire la formule « la simulation rend une societe
presentable » au motif qu'elle devie dans les deux sens. Li et al. (2608.24912) mesurent l'inverse
sur trois categories : desirabilite sociale, prosocialite, aversion au dommage, ou une persona
explicitement malveillante ne parvient pas a passer sous la reference humaine. **La variable est le
decoupage des items.** Le dossier travaille sur des items GSS classes sensibles contre temoins
apparies ; eux travaillent sur 406 items repartis en six categories psychologiques definies a
l'avance, dont trois seulement portent l'effet et trois ne le portent pas, l'adoucissement emotionnel
etant nul en moyenne (`BTB=0,001`). Nos items sensibles melangent probablement les six. La phrase
correcte devient : la deviation est unidirectionnelle sur les axes que l'alignement vise
explicitement, et bidirectionnelle sur les autres.

**3.2 « L'etiquette degrade » contre « l'etiquette aide la ou les gens se dispersent ».** Nos a30 et
a31 montrent que l'etiquette ideologique fait tomber l'appariement des raretes de 0,41 a 0,19 et
rend le camp de gauche simule unanime. Fröhling et al. (2609.02526) montrent que la persona aide
d'autant plus que la variation de reponse humaine de la question est forte. **La variable est le
niveau d'observation.** Leur mesure est une distance entre distributions agregees de l'enquete, la
notre est un appariement individuel de reponses rares. Les deux peuvent tenir en meme temps : une
etiquette qui remplace la personne par le groupe ameliore la marge et detruit l'attribution. Le fait
que les deux quantites soient mesurables sur le meme materiau est notre meilleure ouverture, section
5.

**3.3 « Personne ne publie de plancher de bruit humain » contre trois planchers publies.** La ligne
`[ETABLI]` de `FAITS-ETABLIS.md` selon laquelle le plancher humain par reinterrogation reste sans
equivalent publie doit etre precisee et non retiree. Trois planchers coexistent maintenant dans le
champ, de trois natures : Ahn et al. publient un plancher de **reinterrogation** (0,536 sur
Twin-2K-500) ; Cai et al. publient un plancher **humain contre humain par appariement
d'echantillons** (distance de variation totale 0,098 contre 0,561) ; Yu, Suh, Chang et Chan
(2607.10628) publient une **ligne humaine** dans leur tableau ATP, distance de Wasserstein 0,057,
0,091 et 0,081 sur les vagues 34, 92 et 99, contre 0,139 a 0,218 pour la meilleure condition de
modele, et norme de Frobenius 0,418, 0,411 et 0,327 contre 0,964 a 1,414. **La variable est ce que
le plancher mesure.** Le notre est un plancher de fiabilite temporelle des memes personnes sur les
memes items ; le leur est une variabilite d'echantillonnage entre deux moities d'un meme
echantillon. Ce ne sont pas les memes quantites et elles ne se substituent pas, mais la phrase
« aucun plancher publie » n'est plus tenable telle quelle.

**3.4 « Le LLM est battu par la statistique » contre « le LLM bat MICE ».** Le dossier etablit que nos
agents sont battus sur les deux axes par une regression logistique demographique, 0,5263 et 0,5817
contre 0,6281. Holtdirk, Ahnert, Sakshaug et Haensch (2606.09351, [CONFIRME]) etablissent l'inverse
sur le terrain de l'imputation : sur 150 variables d'opinion et 15 vagues de l'American Trends Panel,
plus de 5 millions de reponses imputees, les quatre specifications d'apprentissage en contexte
battent MICE PMM et MICE Forest **sous les trois mecanismes de manquant**, Wilcoxon `p < 0,05` ;
gpt-oss-120b a 100 exemples en contexte donne des erreurs absolues medianes de 0,033, 0,044 et 0,048
sous MCAR, MAR et MNAR contre 0,068, 0,092 et 0,068 pour MICE PMM, avec des intervalles de confiance
deux a cinq fois plus etroits, au prix d'une sous couverture sous MAR. **La variable est la quantite
notee.** Nous notons une exactitude individuelle, eux notent l'erreur sur un coefficient de
regression, et ils publient le decouplage : « lower cell-level prediction error does not imply lower
coefficient error, and ranking imputation methods by prediction accuracy would not have selected the
method that best supports inference ». Autrement dit, le fait que nos agents perdent sur l'exactitude
individuelle ne dit rien sur leur valeur d'inference, et le point ouvert « decider quoi faire du fait
que nos agents sont battus par une regression logistique » se reformule : il faut noter les deux.

**3.5 « L'aplatissement est entre groupes, pas a l'interieur » contre trois mesures d'aplatissement
interne.** Le fichier 01 de `corpus/lecture-complete` retient de L1.01 une phrase forte, « the
much-discussed flattening of identity groups is between-group, not within: a hedge, not a
caricature », avec une dispersion simulee **superieure** a l'humaine de `+0,18` a `+0,23` nats. Trois
entrees de cette veille mesurent l'inverse en choix fermes : Cai et al. avec un rapport de variance
median de 0,099, Bojic et al. avec 34 pour cent de messages homogeneises a plus de 90 pour cent, et
van der Linden, Kumar, Dixit et Sudan (2510.21011, [CONFIRME]) avec une part mediane du premier
groupe de genre egale a 1,00 pour DeepSeek et Mistral, 0,99 pour GPT-4, c'est a dire que dans
l'occupation typique **toutes** les personas generees recoivent le meme genre. **La variable est le
format de sortie**, deja identifiee par le fichier 01 : texte libre contre modalites fermees. Cette
veille la confirme sur trois materiaux nouveaux et sans exception.

**3.6 « Le plafond humain est un point fixe » contre le plafond estime.** Liu, Shang, Liu et Liu
(2602.00685, [CONFIRME]) construisent, pour leur score de concordance d'effet, un plafond de
**replicateur humain idealise** estime sous la meme structure de bruit, plutot que de prendre la
valeur humaine brute. C'est exactement la lecon de notre a12 sur le delai de retest, transposee a une
autre quantite. Aucun de nos rapports ne borne ses scores par un plafond simule de cette facon.

---

## 4. Ce que ca permet de tester chez nous tout de suite

Chaque test avec son cout, dans la convention du dossier : « analyse » veut dire aucun appel de
modele, quelques minutes sur quatre coeurs ; « nuit » veut dire une nuit de calcul local.

**4.1 La perturbation d'ordre de Yuan, sur nos traces existantes.** Cout : une nuit, mais une nuit
courte. Le test minimal recommande par 2607.02368 est : donner a chaque instance son propre ordre
d'items et regarder si la separation entre groupes s'effondre, puis realigner sur un ordre partage
tire au hasard et regarder si elle revient. Notre pipeline a deja deux regimes d'invite, 150
personnes, 149 questions ; un troisieme regime a ordre d'items randomise par personne coute le meme
budget que le regime court, environ 22 350 appels a 13 217 appels par heure, soit moins de deux
heures. Si notre gonflement de 8,16 avec etiquette s'effondre sous ordre aleatoire et revient sous
realignement, alors notre effet est un gabarit de groupe au sens exact de Yuan, et notre these est
confirmee **par son propre criterium**, ce qui est plus fort que de la confirmer par le notre.

**4.2 Le generateur nul conditionnellement independant, comme baseline.** Cout : analyse. Tirer
chaque reponse independamment par item et par groupe, `X_ij` selon la marginale humaine du couple
item par camp, sans aucune structure entre items, puis passer ce faux jeu dans **toute** notre chaine
de mesure : gonflement d'ecart entre groupes, dispersion intra, rappel des reponses rares,
appariement des raretes. Si le generateur nul reproduit nos chiffres, notre resultat porte sur les
marginales et non sur la simulation. C'est la baseline la plus severe disponible et elle ne coute pas
un appel de modele.

**4.3 Le test de permutation de personas de Ahn et al., sur nos deux regimes.** Cout : une nuit.
Reassigner au hasard les etiquettes de personne a l'interieur de chaque bloc, 10 000 permutations
pour la partie analyse, et comparer notre appariement des raretes correct contre permute. Nous avons
deja les deux termes en tete : 0,41 sans etiquette et 0,19 avec. Il manque la valeur sous
permutation, qui est le seul niveau de reference honnete. Chez Ahn, l'ecart correct contre permute
vaut plus de 100 fois ; si chez nous il vaut deux fois, la revendication tombe.

**4.4 Le `R^2` demeane sur nos propres traces.** Cout : analyse. Retirer la moyenne humaine de chaque
question a nos reponses et aux leurs, puis calculer le `R^2` poole. Nous obtenons alors une valeur
directement comparable a 3,05, 4,44 et 3,87 a 6,21, et surtout comparable **entre nos deux regimes**,
avec et sans etiquette, ce qu'Ahn et al. ne peuvent pas faire. Le point 3 de « ce que personne n'a
fait » du fichier 01, relier le budget d'identite au `R^2` demeane, devient calculable dans l'apres
midi.

**4.5 Le rapport de variance median par cellule, a la maniere de Cai et al.** Cout : analyse.
Publier, a cote de nos rapports 0,64 a 0,89, le **rapport median de variance par cellule** et le
nombre de cellules a variance nulle. C'est la mesure qui rend nos chiffres comparables aux 0,099 et
aux 0,000 de leur tableau, et elle expose le fait, deja etabli chez nous, que trois mesures de
dispersion ne s'accordent plus sur Twin.

**4.6 La calibration contrastive de Li et al., sur notre modele local.** Cout : une nuit courte, un
second appel par question sous persona neutre. Nous avons deja les distributions completes de 44 700
appels par regime ; il manque l'appel neutre. Le test qui vaut publication n'est pas de retrouver la
reference humaine, ils l'ont fait, c'est de passer leur correctif dans **notre** critere A6 : combien
de personnes reparees, combien cassees, et que devient le gonflement d'ecart entre groupes une fois
la distribution recentree. Aucun des correctifs publies ne repond a cette question.

**4.7 Le format de persona et l'incitation au raisonnement, en variables de dispositif.** Cout : deux
nuits courtes. Moon et al. mesurent que le JSON structure bat le texte libre a contenu identique
(0,800 contre 0,720 en `r`, 0,237 contre 0,283 en Jensen Shannon) et que la trace de raisonnement
degrade l'alignement de facon monotone. Nos invites n'ont jamais ete comparees a celles de Stanford,
et c'est declare comme la limite la plus serieuse de notre run. Deux conditions de format sur le meme
plan repondent a la moitie de cette limite, avec un effet attendu deja chiffre ailleurs.

**4.8 Le plancher de sensibilite a l'ordre des questions.** Cout : analyse sur les donnees GSS
existantes plus une nuit courte pour la condition agent. Le decalage humain mesure par Cai et al.
vaut +0,036 avec un intervalle qui contient zero ; le decalage modele vaut jusqu'a +0,367. Notre
point ouvert sur l'ordre des modalites devient, avec ce protocole, un test a plancher.

**4.9 L'inventaire de deux processus de Plisiecki et al., pour la question socle contre aligne.**
Cout : lecture puis une nuit. Le papier (2607.20082, [PROBABLE]) publie un instrument de 48 items,
teste sur 206 modeles a poids ouverts dont **67 paires socle et post entraine du meme point de
sauvegarde**, avec une empreinte du post entrainement chiffree, `B` monte de 0,20 dans 62 paires sur
67. C'est le dispositif exact dont le dossier a besoin pour trancher « a quelle etape la substitution
apparait », et il fournit la liste des paires deja constituees.

---

## 5. Ce que personne n'a fait, mis a jour

La liste des sept fichiers de `corpus/lecture-complete` reste la reference. Cette passe en ferme
deux, en deplace trois et en ouvre quatre.

**Ferme.**

1. Le point 5 du fichier 05, « personne n'a applique le modele generatif de Brandt et Sleegers a une
   population simulee par modele de langage », reste ouvert pour la partie LLM, mais l'outillage
   change de statut. SimPol (2606.27968, [CONFIRME]) infere des reseaux de croyances par
   reconstruction bayesienne non parametrique sur les 23 pays de l'European Social Survey 2016, les
   publie avec une application web, et les injecte dans le modele a base d'agents de Dalege et al.
   2025 avec deux parametres, `beta_pers` pour l'attention a la coherence interne et `beta_soc` pour
   l'attention a l'accord social, 2 000 agents par pays. Resultats : les systemes de croyances
   s'organisent autour de l'immigration (18 pays sur 23 dans le top cinq), des droits LGBT (17) et de
   l'interventionnisme economique (15) ; l'auto positionnement gauche droite predit l'alignement du
   reste des croyances de facon coherente a l'Ouest et non a l'Est ; la polarisation maximale demande
   trois conditions simultanees, un espace de croyances aligne sur un seul axe, une forte attention a
   la coherence interne et une faible attention aux autres ; et le niveau de polarisation atteint
   suit le meme partage Ouest Est que la topologie des reseaux, avec une relation positive entre la
   somme des poids signes du reseau national et la polarisation finale. Ce qui manque encore est le
   pont : personne n'a fait tourner ce modele sur une population **simulee par LLM**, ni ajuste ses
   deux parametres sur des sorties d'agents. Le papier declare lui meme la limite qui nous concerne :
   « we are inferring the same belief network for the whole population, while this is an unrealistic
   assumption ». Notre a30 mesure precisement une dispersion intra camp sur reponses individuelles,
   c'est a dire l'objet que SimPol suppose homogene.
2. Le point 9 du fichier 07, « personne ne mesure l'effet de la contamination inverse sur le plancher
   humain », est occupe pour la partie prevalence : 2607.00403 donne moins de 10 pour cent sur
   Prolific contre plus de 80 sur Mechanical Turk, 2606.04924 donne 44 pour cent de chercheurs ayant
   observe le phenomene. Le signe du biais sur les scores « en pourcentage du plancher humain » n'est
   toujours donne par personne.

**Deplace.**

3. Le point 3 du fichier 02, « aucun plancher de bruit humain par reinterrogation des memes
   personnes », se scinde. Le plancher de reinterrogation reste sans equivalent applique a un partage
   inter et intra. Mais deux planchers voisins existent maintenant, celui de Cai et al. par
   appariement d'echantillons et celui d'Anamnesis par ligne humaine dans le tableau. Toute phrase du
   dossier sur ce point doit nommer laquelle des trois quantites.
4. Le point 4 du fichier 02, « aucun correctif evalue contre une baseline non LLM », se durcit au
   lieu de se fermer : 2606.09013 confirme qu'aucun modele ne bat la marginale humaine insensible aux
   conditions sur la distribution de quantite, et 2608.29455 confirme qu'aucun ne bat la moyenne
   d'item en laisser un dehors sur la correlation par personne. Ce qui manque toujours est un
   **correctif** de dispersion evalue contre l'une de ces deux baselines.
5. Le point 5 du fichier 03, « personne n'a evalue un simulateur avec une metrique qui compte les gens
   rares », tient. 2608.22859 compte les opinions minoritaires, mais dans une chaine de recherche
   documentaire, pas dans une simulation de repondants, et sa cible est une distribution d'opinion,
   pas une personne.

**Ouvert par cette passe.**

6. **Personne ne mesure la perturbation d'ordre de Yuan sur des attitudes politiques.** Son plan a
   deux personas culturelles et un inventaire de personnalite ; l'auteur declare que l'extension a
   des personas politiques « is open to test ». Le faire sur le GSS, avec un camp de gauche et un
   camp de droite, avec la dispersion intra camp de notre a30 comme mesure de sortie, est une
   contribution a soi seule et coute une nuit courte.
7. **Personne ne relie le retrecissement de bienveillance a la dispersion intra camp.** Li et al.
   montrent que le modele a perdu le bas de l'echelle sur trois axes ; nous montrons que le camp de
   gauche simule devient unanime sur l'avortement et les libertes civiles. Si les items ou notre camp
   de gauche s'ecrase sont ceux qui portent le plus de `BTB`, alors les deux resultats sont un seul
   mecanisme. Cout : analyse, avec un etiquetage d'items a la main.
8. **Personne n'a mis le `R^2` demeane et le rapport de variance dans le meme tableau que la valeur
   d'inference.** Le point 7 du fichier 03 reclamait deja ce croisement pour Ye et Ahn ; 2606.09351
   fournit desormais le troisieme cote, une erreur de coefficient mesuree contre MICE sur les memes
   variables d'opinion. Une table a trois colonnes, part de variance individuelle conservee, erreur
   de coefficient, largeur d'intervalle, n'existe nulle part.
9. **Personne n'a publie un taux d'homogeneisation a plus de 90 pour cent avec referent humain sur
   les memes items.** Bojic et al. publient 34 pour cent sans referent ; nous publions 46 et 43
   questions sur 149 contre 13 chez les humains. Le croisement n'existe pas, et il tient dans une
   ligne de tableau.

---

## 6. Ce que je n'ai pas pu verifier

1. **L'index de comparaison de la veille est incomplet, et le chiffre de 126 est faux.** Il compare
   aux sept fichiers `corpus/0N` et ignore `corpus/lecture-complete`. Sept des 126 y figurent deja :
   2609.02526, 2608.29455, 2608.28668, 2608.11528, 2603.00059, 2607.27100 et 2606.09013. Six d'entre
   elles y sont lues en profondeur, la septieme (2608.28668) y est `[NON LU]` titre seul. Le nombre
   d'entrees reellement neuves est **119**. Le tri ci dessous garde la numerotation de la veille et
   signale ces sept lignes.
2. **Aucun des 61 « sans rapport » n'a ete lu au dela du resume d'origine complet recupere par l'API
   arXiv.** Le classement repose sur ce resume seul. Le filtre de pertinence de la veille est lexical
   et laisse passer beaucoup de bruit de contamination de bancs d'essai, ce qui explique la taille de
   cette categorie ; il peut aussi avoir ecarte a tort un papier dont le resume n'emploie aucun des
   termes attendus, et cela n'est pas verifiable depuis ce rapport.
3. **La couverture hors arXiv est nulle.** La veille declare elle meme qu'OpenAlex a repondu 429 et
   que les requetes restantes ont ete abandonnees, et que SSRN, OSF et PsyArXiv ne sont pas
   interroges. Les revues de sciences sociales, ou vivent la psychologie sociale et la methodologie
   d'enquete, sont donc sous representees dans les 126. Toute conclusion d'absence de cette session
   porte sur arXiv, du 1er juin au 8 septembre 2026, et sur rien d'autre.
4. **Les annexes supplementaires des papiers lus n'ont pas ete ouvertes.** Pour 2608.29455, les
   tableaux S1 a S8 portent les comparaisons de jeux d'items, les details d'invite et la sensibilite
   du partage entre interaction personne par item et erreur transitoire ; le chiffre de 44,0 pour
   cent depend de la fiabilite retenue, `r_tt = 0,536`, et le papier signale que ce partage bouge avec
   elle. Pour 2607.02368, les sections S1 a S9 portent la regularisation des matrices singulieres et
   les variantes de simulation ; le fait que 83,3 pour cent des matrices GPT-4o en ordre fixe soient
   singulieres avant perturbation est lu dans le corps du texte, pas verifie dans l'annexe.
5. **Deux valeurs du tableau de 2607.27100 sont tronquees dans le rendu PDF employe.** La ligne
   Gemma 3 12B de la table 2 ne rend que trois de ses six colonnes ; les valeurs citees pour Qwen et
   Phi sont completes, celle de Gemma 3 n'est reprise que pour le rapport de variance median, `0,000`.
6. **La version publiee de plusieurs entrees n'a pas ete consultee.** Toutes les lectures portent sur
   la version arXiv indiquee dans la table. Pour 2510.21011 et 2509.10078, qui sont des revisions de
   preprints de 2025, l'ecart entre la version lue et une eventuelle version de revue n'est pas
   verifie.
7. **Le lien entre SimPol et nos donnees n'est pas testable en l'etat.** Leur materiau est
   l'European Social Survey 2016, le notre le GSS ; les items ne se recouvrent pas et leur code
   d'inference de reseau n'est pas indique comme public dans le texte lu, seule l'application web de
   visualisation l'est.
8. **Le budget de calcul n'a servi a aucune verification empirique.** Conformement a la consigne,
   aucune analyse n'a ete relancee ; tous les chiffres attribues au projet dans ce fichier sont repris
   de `FAITS-ETABLIS.md` et d'`ARBITRAGE.md` sans recalcul.

---

## Annexe. Table de tri des 126 entrees

Grille de `corpus/00-GRILLE.md`. Colonne « rapport a la these » restreinte a : `menace directe`
(mesure la meme chose que nous), `precedent partiel`, `soutien`, `methode utile`, `sans rapport`.
Certitude : **[CONFIRME]** lu en entier dans le texte pendant cette session, **[PROBABLE]** resume
d'origine complet lu a la source arXiv, **[NON LU]** titre seul. Aucune ligne n'est **[NON LU]** :
les 126 resumes ont ete recuperes par l'API arXiv et lus. Les sept lignes marquees `DEJA AU CORPUS`
figurent deja dans `corpus/lecture-complete` et ne sont donc pas des nouveautes.

| # | reference | question posee | donnees | modeles | mesure exacte | resultat chiffre principal | faille ou limite | rapport a la these | certitude |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Li X. et al., 4 sept. 2026, *Aplaud*, arXiv 2609.04738 | peut on personnaliser un LLM par utilisateur a faible cout memoire pour predire ses reponses d'enquete ? | donnees d'enquete par utilisateur, volume non precise | LoRA sur base non precisee | perte de generalisation et efficacite d'inference contre LoRA personnalises de l'etat de l'art | annonce un gain sur les deux, valeurs non donnees dans le resume | aucune baseline statistique, aucune mesure de dispersion | methode utile, concurrent de la baseline par personne | [PROBABLE] |
| 2 | Fröhling, Rupprecht, Strohmaier, Wagner, 2 sept. 2026, arXiv 2609.02526 `DEJA AU CORPUS` | quand l'etiquette aide t elle, et quelle methode de selection d'attributs employer ? | 4 enquetes sociales generales, 2 pays, 20 questions cibles par enquete | 6 modeles Llama et Qwen, 3 a 70 milliards | distance de Jensen Shannon entre distributions predite et reelle, croisee avec entropie normalisee ou dissension de la question | la persona aide sur les questions a forte variation humaine et nuit sur les faibles ; les selections statistiques battent les selections par LLM ; `W` de Kendall 0,25 a 0,50 entre executions | unite agregee, aucun terme intra, aucun plancher | menace directe | [CONFIRME] |
| 3 | Greco, La Cava, Tagarelli, 2 sept. 2026, arXiv 2601.22396 | des personas culturelles s'alignent elles sur le WVS, la carte Inglehart Welzel et les fondements moraux ? | WVS, questionnaire de fondements moraux | non precise dans le resume | positionnement sur la carte, coherence par groupe demographique, profils moraux | les distributions suivent largement les motifs de groupe humains | descriptif, aucun terme intra, aucun plancher | sans rapport | [PROBABLE] |
| 4 | Song, Choi, Park, Han, 2 sept. 2026, arXiv 2509.10078 | un questionnaire psychometrique humain decrit il le comportement reel d'un LLM ? | PVQ-40/21 et BFI-44/10, plus requetes d'usage ordinaire | 8 modeles a poids ouverts | profils par auto declaration Likert contre probabilites de generation sur requetes reelles | les deux profils divergent ; la coherence intra construit disparait en generation ; les invites demographiques deplacent les reponses au questionnaire mais pas la generation | pas de referent humain individuel | soutien | [PROBABLE] |
| 5 | Bommarito, 2 sept. 2026, *SHELF*, arXiv 2609.03047 | quels outils conviennent au travail bibliographique des bibliotheques ? | 62 899 documents ecrits par modele, vocabulaires Library of Congress | TF, TF-IDF, BM25, encodeurs, decodeurs zero shot | exactitude par tache | classification de sujet 0,8887, classification de genre 0,2605 | hors domaine | sans rapport | [PROBABLE] |
| 6 | Yu, Suh, Chang, Chan, 31 aout 2026, *Anamnesis*, arXiv 2607.10628 | une plateforme ouverte peut elle rendre la simulation par recits de vie accessible et reproductible ? | American Trends Panel vagues 34, 92 et 99, plus concours de legendes du New Yorker | LLaMA-3.1-8B, conditionnement par recit contre listes demographiques BIO et QA | distance de Wasserstein et norme de Frobenius apres appariement des personas aux repondants | Anamnesis 0,147 / 0,218 / 0,139 en WD contre 0,235 a 0,392 pour les listes demographiques, et **ligne humaine a 0,057 / 0,091 / 0,081** | le plancher humain est une variabilite d'echantillonnage, pas une reinterrogation ; aucun terme inter ni intra | precedent partiel | [CONFIRME] |
| 7 | Kassis, 31 aout 2026, *mimeo*, arXiv 2609.00453 | un dossier sur un expert transfere t il sa connaissance, sa voix ou son jugement ? | oeuvre publique de quatre experts, 20 questions obscures | un harnais d'agent de code | reponses correctes, citations verifiees, identification de la persona | 13,2 pour cent des citations rejetees ; identification abaissee de 18 a 23 points par l'ajout de materiel de tache | pas d'enquete, pas de population | sans rapport | [PROBABLE] |
| 8 | Zhao G. et al., 31 aout 2026, *ScienceArena*, arXiv 2608.30517 | les modeles resolvent ils les olympiades scientifiques recentes ? | 13 competitions publiques | 14 modeles recents | bareme a credit de processus, juge LLM calibre sur des medailles | scores equivalents a une medaille sur plusieurs epreuves | hors domaine | sans rapport | [PROBABLE] |
| 9 | Zhao X. et al., 31 aout 2026, *LiveMacroEval*, arXiv 2608.30110 | des agents LLM prevoient ils les indicateurs macroeconomiques en temps reel ? | 16 indicateurs americains, six mois | 4 agents avec recherche web | score contre rendements et paris simules, contre nowcasts de la Fed et consensus Bloomberg | exactitude agregee comparable aux references institutionnelles | hors domaine | sans rapport | [PROBABLE] |
| 10 | Gwak, Kwak, Lee, Son, 31 aout 2026, *LaRA*, arXiv 2605.29888 | detecter la contamination dans l'apres entrainement par renforcement | modeles de raisonnement entraines par RL | LLM de raisonnement | sensibilite a la perturbation, effondrement directionnel, rigidite locale par couche | surpasse les detecteurs au niveau des sorties | contamination de bancs d'essai, pas d'enquete | sans rapport | [PROBABLE] |
| 11 | Żatuchin, Dzemesjuk, 30 aout 2026, *PersonaGen-1M*, arXiv 2608.30023 | construire un corpus d'acheteurs synthetiques annote en intention | 1 031 732 personas, 19 416 821 attributs, 511 secteurs | pipeline de deduplication puis enrichissement | part d'intention par categorie | 78,3 pour cent informationnel, 17,4 commercial, 4,3 transactionnel | aucune validation contre des humains, l'estimation empirique est declaree travail futur | sans rapport | [PROBABLE] |
| 12 | Yuan Y., 30 aout 2026, *Cultural Bias Without a Cultural Self*, arXiv 2607.02368 v3 | une persona installee par invite est elle un point de vue ou un gabarit de groupe ? | humains `N=89` test retest et `N=263` NEO-PI-R ; 4 modeles x 2 personas x 2 ordres, `N=400` a 2 000 | GPT-4o, DeepSeek-V3, Claude Haiku 4.5, Claude Sonnet 4.6, temperature 0,7 | matrice item par dimension, correlation intra instance, espace tangent sur la variete SPD ; separation par regroupement sous ordre fixe, aleatoire et realigne | humains `r=0,77` entre sessions disjointes, identification jusqu'a 75,9 pour cent contre 0,38 de hasard, `R^2=0,281` sur la moyenne generale contre 0,018 pour Big Five ; modeles 94,63 en FO, 55,23 en RO, 83,69 apres realignement ; un generateur sans structure reproduit 97,2 / 57,6 / 83,2 | deux personas culturelles, un seul inventaire, pas d'attitudes politiques, pas de reponses rares | menace directe | [CONFIRME] |
| 13 | Luo, Xu, Chen, Zhao, 30 aout 2026, *ACE-Align*, arXiv 2601.12962 v2 | comment aligner les effets d'attribut plutot que la moyenne d'un groupe suppose homogene ? | WVS et ISSP, 14 pays, personas a 1 a 4 attributs | LLaMA3.1-8B-Instruct plus baselines | effets d'attribut par edition controlee de persona, taxonomie `Flipped`, `Stereotyping`, `Erasure`, `Aligned` | toutes les methodes baissent de `G=1` a `G=4` ; ecart Nord Sud de 3,40 a 1,11 sur WVS et 2,53 a 0,85 sur ISSP | aucune dispersion intra, aucun plancher, effets moyens et non personnes | menace directe | [CONFIRME] |
| 14 | Hsu, Lu, 30 aout 2026, *Incognita*, arXiv 2607.02975 | ce que resout un banc d'essai d'agents change t il quand l'acces est social ? | 18 taches de service client, 864 essais | 4 modeles | taux de succes selon trois regimes d'acces | l'acces social baisse le succes pour tous, meilleur modele a 0,65 | hors domaine | sans rapport | [PROBABLE] |
| 15 | Zhou X. et al., 30 aout 2026, *RePro*, arXiv 2609.00062 | reecrire un banc de maths avec preuve verifiee | GSM8K et MATH | prouveurs Lean plus LLM | validite, faisabilite, correction des reponses | 100 pour cent sur les instances retenues | hors domaine | sans rapport | [PROBABLE] |
| 16 | Wang Y. et al., 30 aout 2026, *EvoBrowseComp*, arXiv 2606.13120 | evaluer des agents de recherche sur des connaissances evolutives | 400 questions anglaises et 400 chinoises | agents de recherche | exactitude sur questions sans contamination | difficulte elevee confirmee | hors domaine | sans rapport | [PROBABLE] |
| 17 | dos Santos et al., 30 aout 2026, arXiv 2507.08814 | la structure urbaine predit elle la susceptibilite a la dengue ? | annees d'epidemie, unites spatiales | modeles spatiaux, aucun LLM | correlation de Spearman spatiale prospective | 0,49 a 0,76 selon l'annee, nul sous permutation | aucun rapport avec la simulation d'opinion | sans rapport | [PROBABLE] |
| 18 | Nguyen, Ahmad, 29 aout 2026, arXiv 2608.29266 | une position culturelle attribuee a un modele se distingue t elle du bruit ? | 88 pays de l'Integrated Values Survey | une douzaine de modeles de quatre origines | rapport bruit sur signal, decomposition entre graines aleatoires et reformulations d'invite | `NSR > 1` sur 49 des 117 couples valides, 42 pour cent, jusqu'a 5,56 ; le ton de l'invite deplace un modele de 2,4 unites de carte | mesure au niveau du modele, pas de la personne | methode utile | [PROBABLE] |
| 19 | Ahn, Mao, Lee, 29 aout 2026, *Item-Mean Surrogates*, arXiv 2608.29455 `DEJA AU CORPUS` | apres retrait de la moyenne d'item, que reste il du signal individuel ? | 4 jeux, plus de 400 000 participants, plus de 6 000 items | GPT-4.1, GPT-5, DeepSeek, Gemini 2.5 et 3, Llama 3.1 70B, Centaur, plus affinages | `R^2` poole demeane, theorie de la generalisabilite, distance de Wasserstein-2 decomposee | 3,05 pour cent contre un plafond humain de 53,6 ; interaction personne par item 8,9 fois l'effet de personne ; ecarts types medians a 50 a 65 pour cent des humains ; le LLM perd contre la moyenne d'item en laisser un dehors, 0,34 contre 0,45 | mesures lineaires, pas de systeme a historique complet de reponses | menace directe | [CONFIRME] |
| 20 | Degli Esposti, 29 aout 2026, *Animarium*, arXiv 2608.27111 | produire une population synthetique italienne reproductible a partir d'agregats publics seuls | 1 814 317 individus, 887 937 menages, 11 communes | maximum d'entropie plus donation de vecteurs entiers de 23 variables attitudinales | reproductibilite au bit pres, qualite par anneau | regeneration identique en 33 minutes sur une station | validation explicitement hors perimetre | methode utile | [PROBABLE] |
| 21 | Liu X. et al., 29 aout 2026, *HumanStudy-Bench*, arXiv 2602.00685 | un agent atteint il les memes conclusions inferentielles qu'un humain ? | 12 etudes fondatrices, plus de 6 000 essais, echantillons humains de quelques dizaines a 2 100 | 10 modeles contemporains et ensembles | score d'alignement de probabilite et score de concordance d'effet, avec plafond de replicateur humain idealise | meilleur `PAS` 0,5314, meilleur `ECS` 0,265 ; la correlation de motif plafonne a `rho <= 0,31` alors que la calibration de magnitude atteint 1,00 | pas de dispersion intra, pas de reponses individuelles | precedent partiel | [CONFIRME] |
| 22 | Fu, Meng, Chen, Huang, 29 aout 2026, arXiv 2608.29198 | l'identite et l'opinion declenchent elles la meme sycophantie politique ? | 450 dilemmes politiques verifies a la main | 13 modeles instruits | deplacement de position selon indice d'opinion et indice d'identite | dissociation entre les deux sensibilites, effets sous additifs quand les deux sont presents | pas de referent humain | soutien | [PROBABLE] |
| 23 | Angulo, Yeste, Espinos-Morato, 29 aout 2026, arXiv 2608.29463 | une taxonomie de contamination organisee par mitigation vaincue | 41 documents codes par deux codeurs | aucun | kappa pondere lineaire par variable | mediane 0,21 contre un plafond de test retest a 0,84 | contamination de bancs d'essai | sans rapport | [PROBABLE] |
| 24 | Wei, Li, Godbole, Jia, 29 aout 2026, arXiv 2605.24818 | corriger un score contamine plutot que le detecter | modeles Hubble en paires minimales | predicteurs de memorisation et de correction | estimateurs de correction calibres par contamination volontaire a taux connu | 10 exemples suffisent a calibrer, transfert d'un jeu a l'autre | banc d'essai, pas d'enquete | methode utile | [PROBABLE] |
| 25 | Land, Bikel, 28 aout 2026, arXiv 2605.30504 | auditer les etiquettes d'un banc d'essai par theorie de la reponse a l'item | 7 bancs, reponses de 114 modeles | 114 modeles | indicateur fonde sur l'IRT | 95 pour cent de precision sur les 200 premiers cas | banc d'essai, mais l'appareil IRT est transferable a une enquete | methode utile | [PROBABLE] |
| 26 | Epure et al., 25 aout 2026, arXiv 2511.16478 | repenser l'evaluation de la recommandation musicale a l'ere des LLM | revue | revue | revue | aucune mesure propre | position | sans rapport | [PROBABLE] |
| 27 | Hyodo, 24 aout 2026, arXiv 2608.22833 | fournir deux socles minimaux de simulation locale 2D et 3D | aucun jeu de donnees humain | LLM et VLM heberges localement | aucune | aucune | outil pedagogique | sans rapport | [PROBABLE] |
| 28 | Venkat, Qiu, Peng, Gui, 24 aout 2026, *ExploraTwin*, arXiv 2608.20539 | abaisser le cout d'essai des jumeaux numeriques | replication de 19 experiences de Twin-2K-500, 197 000 unites de reponse | jumeaux du jeu Twin-2K-500 | taux de reponse structurellement valide au premier essai | 99,6 pour cent | plateforme, aucune mesure de fidelite propre | methode utile | [PROBABLE] |
| 29 | Song E., Hong S., 24 aout 2026, arXiv 2608.28668 `DEJA AU CORPUS` | l'erreur demographique d'un panel synthetique vient elle du generateur ou du referentiel choisi ? | 1 000 000 d'enregistrements Nemotron-Personas-Korea contre statistiques officielles coreennes | generateur de personas | distance de variation totale sur la loi jointe sexe x age x province, borne de biais | 1,81 point de pourcentage contre le registre d'avril 2026, 0,56 contre le referentiel generateur ; raking et post stratification retirent l'essentiel de la dependance pour 0,2 pour cent d'inflation de variance | porte sur la composition demographique, pas sur les opinions | methode utile | [PROBABLE] |
| 30 | Thakur, Agrawal, Nakkiran, Karlsson, 24 aout 2026, *WARP*, arXiv 2608.22859 | comment eviter que la recherche documentaire efface les opinions minoritaires ? | 35 000 documents, 156 requetes, 26 entites, trois domaines | recherche dense, creuse et a bassin variable | distance de Wasserstein-1 sur la distribution d'intensite de sentiment | reduction d'au moins 43 pour cent de l'erreur distributionnelle, panel de cinq juges preferant WARP dans 86 pour cent des comparaisons tranchees | chaine documentaire et non simulation de repondants | soutien | [PROBABLE] |
| 31 | Ashok et al., 21 aout 2026, arXiv 2608.26182 | comment specifier une persona de robot par invite | 27 experts en interaction homme robot | LLM en robot social | analyse qualitative | huit composantes fonctionnelles proposees | pas de mesure quantitative | sans rapport | [PROBABLE] |
| 32 | Meng et al., 21 aout 2026, *Know2Guess*, arXiv 2606.26101 | separer reponse fondee, devinette et abstention | 1 200 items, cinq domaines | FLAN-T5, Qwen2.5, Llama-3 | zones d'attente d'abstention, double analyse syntaxique | Qwen2.5-3B meilleur, calibration mauvaise, refus benins persistants | banc d'essai de connaissance | sans rapport | [PROBABLE] |
| 33 | Ahmadi, Jiao, Manzolli, Yu, 20 aout 2026, arXiv 2608.20320 | un flux a trois agents peut il collecter et predire un choix modal ? | 454 observations repondant par scenario, enquete par robot conversationnel | 9 modeles locaux de 2 a 35 milliards, plus logit multinomial, regression logistique, foret aleatoire | exactitude a cinq classes | foret aleatoire 69,6 pour cent, meilleur LLM texte 69,9, meilleure configuration visuelle 71,5 | domaine du transport, echantillon etudiant, pas d'opinion | methode utile | [PROBABLE] |
| 34 | Chen M. et al., 20 aout 2026, arXiv 2608.11354 | inferer des croyances a partir d'interactions pour la recommandation | jeu OPeRA | LLM avec raisonnement contrefactuel | prediction d'action suivante, Big Five, categorie retenue | les personas inferees egalent ou depassent les personas de verite terrain | domaine recommandation | sans rapport | [PROBABLE] |
| 35 | Elfes, Bastos, Aiello, 18 aout 2026, arXiv 2601.07398 | mesurer la polarisation narrative plutot que la polarisation d'opinion | 212 videos YouTube, 90 029 commentaires | LLM d'extraction de roles narratifs | polarisation narrative sur roles d'acteurs | les videos sont fortement polarisees, les commentaires beaucoup moins et convergent sur des structures partagees | pas de simulation de repondants | methode utile | [PROBABLE] |
| 36 | Braun, 16 aout 2026, arXiv 2608.12652 | detecter la contamination par sonde du flux residuel | quatre audits de points de sauvegarde contamines | transformeurs reels | separabilite excedentaire recentree sur placebo | la correction porte plus de variance que le nul teste, `p=0,0075` devient 0,0745 apres propagation | banc d'essai | sans rapport | [PROBABLE] |
| 37 | Lundström-Imanov, 15 aout 2026, arXiv 2605.20279 | theorie microeconomique de l'effondrement de modele | banc synthetique C4, dix generations | theorie plus estimation | loi d'effondrement logarithmique | coefficient 0,181, erreur type HAC 0,024 | economie theorique | sans rapport | [PROBABLE] |
| 38 | Hung, Midha, Wu, Zhang, 13 aout 2026, arXiv 2609.04243 | des agents synthetiques peuvent ils remplacer des humains dans une experience conjointe ? | replications d'experiences conjointes publiees en science politique | plusieurs modeles, temperature 0,5, appariement un pour un des personas | correspondance representationnelle, correspondance inferentielle, stabilite procedurale, decomposition de variance entre reglages | resultats inegaux entre les trois dimensions ; la validite est declaree dependante de la revendication et hierarchique ; le meme plan change de conclusion selon le modele | les resultats repliques sont vraisemblablement dans les corpus d'entrainement, les auteurs le disent | precedent partiel | [CONFIRME] |
| 39 | Zhang X. et al., 13 aout 2026, arXiv 2608.12984 | ecrire un rapport sans derive a une date fixee | 6 130 sources, 555 926 fiches de preuve | systeme multi agents | contradictions residuelles, violations de regard en avant | 6 845 contradictions ramenees a zero, zero violation sur sept dates | outillage de redaction | sans rapport | [PROBABLE] |
| 40 | Mungari, 12 aout 2026, arXiv 2608.11649 | quelles preferences politiques un modele exprime t il sur des partis reels ? | partis et dirigeants italiens, neuf criteres | plusieurs modeles | coherence entre evaluations, taux de refus, sensibilite a la formulation, effet des personas | audit systematique, valeurs par modele | pas de referent humain d'enquete | soutien | [PROBABLE] |
| 41 | Zhao H., Xiao, Xuan, Salim, 12 aout 2026, arXiv 2608.11528 `DEJA AU CORPUS` | l'alignement sur un groupe induit il de la sycophantie, et egalement pour tous ? | OpinionQA, TriviaQA, TruthfulQA, banc are-you-sure | 4 modeles x 13 groupes x 3 methodes | gain d'alignement d'opinion et deplacement de sycophantie, a budget apparie | gain et deplacement non uniformes entre groupes, profil propre a chaque groupe | pas de dispersion intra | soutien | [PROBABLE] |
| 42 | Li Y., Zhong, Kamalloo, 11 aout 2026, arXiv 2609.00014 | des profils tires de publications reelles battent ils les personas synthetiques ? | messages de reseaux sociaux anonymises | affinage supervise et raisonnement multi perspective | bancs de recommandation et de requetes ouvertes | les profils ancres sur le comportement battent les profils synthetiques | pas d'enquete, pas de plancher | methode utile | [PROBABLE] |
| 43 | Yang Z. et al., 11 aout 2026, *CalibDCD*, arXiv 2608.10462 | corriger les deplacements de traits dus a l'apres entrainement pour la detection de contamination | corpus de pre entrainement supposes | detecteurs a traits | AUC et vrai positif a 5 pour cent de faux positifs | gains jusqu'a 7,0 et 15,0 points | banc d'essai | sans rapport | [PROBABLE] |
| 44 | Bao, Wu, Liu, Li, 10 aout 2026, arXiv 2606.08251 | l'IA sait elle diverger ou nier en science ? | 121 640 preprints sollicites, 6 749 scientifiques, 25 139 jeux de notes ; 39 millions d'articles 2010 a 2025 | modeles raisonneurs et non raisonneurs | nouveaute, faisabilite, probabilite, adoption ; espace d'hypotheses explore | les modeles non raisonneurs s'effondrent dans un espace etroit, aucun ne propose spontanement d'hypothese nulle, les affirmations nulles chutent apres la sortie de ChatGPT | domaine des idees scientifiques, pas des opinions | soutien | [PROBABLE] |
| 45 | Chen P. et al., 10 aout 2026, *Cultivar*, arXiv 2608.09766 | contamination et robustesse a la localisation en traduction | sous ensemble localise de FLORES | 32 modeles a poids ouverts | ecart de performance source contrastive | les modeles specialises sont moins robustes, biais vers les contenus americains | traduction | sans rapport | [PROBABLE] |
| 46 | Shihab, Akter, Sharma, 8 aout 2026, arXiv 2608.07914 | quand la contamination est elle detectable ? | controles propres et vus apparies | six canaux de permutation exacte | efficacite `ef` et budget de puissance | `R^2` 0,83 a 0,98 entre efficacite de calibration et puissance ; le budget gaussien echoue dans 9 cas sur 9 | banc d'essai, mais le cadre de puissance est transferable | methode utile | [PROBABLE] |
| 47 | Hou, Jiao, Wang, Li, 7 aout 2026, arXiv 2608.07341 | la mitigation de contamination restaure t elle vraiment la capacite ? | modeles contamines et bancs multiples | plusieurs | agregat stratifie d'ecarts de probabilite par question | la restauration des methodes anterieures est fortement surestimee | banc d'essai | sans rapport | [PROBABLE] |
| 48 | Liu S. et al., 7 aout 2026, arXiv 2604.12147 | les agents suivent ils le plan qu'on leur donne ? | 21 120 trajectoires SWE-agent | 4 modeles | conformite au plan | un mauvais plan nuit plus que pas de plan | genie logiciel | sans rapport | [PROBABLE] |
| 49 | Dahiya, 6 aout 2026, *Mind the Gaps*, arXiv 2608.06115 | peut on simuler des individus assez fidelement dans un domaine etroit ? | corpus qualitatif public, 420 groupes entraines, marchands SME | Gemma 4 12B plus un adaptateur LoRA rang 64 par groupe, 400 retenus | alignement ordinal `1 - MAD/R`, exactitude exacte, erreur signee par groupe | 0,775 d'alignement ordinal contre 0,717, 0,740 et 0,748 pour les systemes anterieurs ; 0,679 d'exactitude exacte contre 0,657 ; biais residuel +0,437 position, ecart type par groupe median 1,85 | aucune mesure de dispersion, aucun plancher humain sur son propre jeu, domaine commercial etroit | menace directe | [CONFIRME] |
| 50 | Chen C., Yuan, Kairouz, 6 aout 2026, arXiv 2604.22191 | auditer l'usage de contextes prives dans l'affinage par renforcement | donnees de preference instrumentees | modeles affines par RL | taux de detection a 10 pour cent de faux positifs | 67 pour cent, AUROC 0,756 a 1 pour cent d'injection | audit de conformite | sans rapport | [PROBABLE] |
| 51 | Miklian, Hoelscher, Katsos, 5 aout 2026, arXiv 2603.00059 v3 `DEJA AU CORPUS` | des repondants synthetiques retrouvent ils les resultats contre intuitifs d'une enquete ? | 420 developpeurs de la Silicon Valley, plus donnees synthetiques | cinq puis trois modeles de pointe, deux protocoles de generation | comparaison item par item et par sous groupe politique, plus tests d'ordre de specification d'invite | les consensus sont repris (humain 88, synthetique 75 a 100) ; les resultats contre intuitifs ne le sont pas ; **les centristes humains ont un regret de 28 contre 56 pour cent chez les non centristes, un seul modele reproduit la direction et a un tiers de l'amplitude, un autre ne genere aucun centriste** ; en generation par repondant, 99 pour cent des agents sur une seule modalite | echantillon professionnel etroit, pas de plancher humain | precedent partiel | [CONFIRME] |
| 52 | Bhandari et al., 5 aout 2026, arXiv 2608.04746 | une decroissance temporelle par type de memoire ameliore t elle un agent | banc de generalisation temporelle | agents a memoire | ecart de generalisation | +0,108, effondre d'un facteur 5,7 sans decroissance | memoire d'agent | sans rapport | [PROBABLE] |
| 53 | Li X. et al., 4 aout 2026, *MatrAIx*, arXiv 2608.04205 | evaluer des produits avec une population simulee a l'echelle | 8,3 milliards d'enregistrements de persona, 1 010 taches, 18 189 essais | Claude Opus 4.8, GPT 5.5, Claude Haiku 4.5 | adherence a la persona sur dix attributs comportementaux | 366 essais sur 400, 91,5 pour cent | aucun referent humain d'enquete, aucune dispersion | sans rapport | [PROBABLE] |
| 54 | Proskurina, Gourru, Velcin, 4 aout 2026, arXiv 2608.04268 | l'entrainement sur donnees synthetiques amplifie t il les biais sociaux ? | Bias in Bios, regimes d'entrainement controles | modeles de langue reentraines par generations | metriques d'equite et metriques de langage | la degradation d'equite apparait **avant** la degradation de langage | pas d'enquete d'opinion | soutien | [PROBABLE] |
| 55 | Hu Z. et al., 4 aout 2026, arXiv 2608.03970 | voix ou clavier, quelle perturbation coute le plus ? | suite HIVE de perturbations | modeles instruits | exactitude sous perturbation | la voix coute plus que le clavier, la cause est le nombre de jetons detruits | hors domaine | sans rapport | [PROBABLE] |
| 56 | Zhou L. et al., 4 aout 2026, *GDPevo*, arXiv 2608.03764 | mesurer l'auto evolution d'agents sur des taches d'entreprise | 120 puis 240 taches | 4 agents | exactitude sur taches tenues a l'ecart | jusqu'a +16,44 points, plafond oracle 91,6 | hors domaine | sans rapport | [PROBABLE] |
| 57 | Zhang Z., Stadie, 4 aout 2026, arXiv 2608.02985 | comparer avant et apres la coupure suffit il a detecter une fuite ? | questions resolues apres coupure | quatre modeles de pointe | score ajuste de fuite, controle propre apparie | le test standard est non informatif, quatre modeles sur quatre echouent sur des questions qu'ils ne peuvent avoir memorisees ; la fuite se concentre sur les issues qui ont surpris la foule | domaine de la prevision | methode utile | [PROBABLE] |
| 58 | Xia W. et al., 3 aout 2026, arXiv 2607.24341 | modeliser les frictions percues plutot que la seule demographie | 1 068 citoyens neerlandais, environ 40 548 couples question reponse | GPT-3.5-turbo, Ministral-8B, Llama-3.1-8B, affinage supervise et GRPO | exactitude en invite seule et apres affinage | les personas fondees sur le cout de transaction percu ameliorent systematiquement | pas de dispersion, pas de plancher | methode utile | [PROBABLE] |
| 59 | Petrov et al., 3 aout 2026, arXiv 2608.07567 | generalisation temporelle en classification fNIRS | 124 sujets | trois architectures visuelles | exactitude entre fenetres | zero shot 54 a 69 pour cent, 90 a 96 apres affinage par sujet | hors domaine | sans rapport | [PROBABLE] |
| 60 | Wu Z. et al., 31 juil. 2026, *ESPP*, arXiv 2607.28439 | un panel de personas evalue t il une interface mieux qu'un juge unique ? | captures d'interfaces generees | panel de personas psychologiquement diverses avec confiance bornee | correlation de Pearson au jugement humain | 0,716 a 0,922 ; les sous groupes s'accordent sur le classement des modeles mais divergent sur les dimensions, ce qu'un juge homogene efface | domaine de l'interface | methode utile | [PROBABLE] |
| 61 | Zhao R., Raissi, 31 juil. 2026, arXiv 2608.11232 | evaluer des agents de trading sans contamination | 30 questions selectionnees, 38 minees | 11 modeles | exactitude avec et sans outils | 90,0 contre 73,0 pour cent | hors domaine | sans rapport | [PROBABLE] |
| 62 | Alharbi, 31 juil. 2026, arXiv 2608.28626 | les modeles relisent ils vraiment ce qu'ils evaluent ? | 165 soumissions ICLR 2026, 145 erreurs inserees | Qwen2.5-VL-72B et Pixtral-Large-124B | notes, detection d'erreurs, effet de l'identite des auteurs | notes 7,0 a 8,1 contre 3,4 a 6,8 chez l'humain, 12,1 pour cent d'erreurs detectees, 22,2 avec une consigne de verification | relecture scientifique | sans rapport | [PROBABLE] |
| 63 | Cooper, Lemley, De Sa, Duesterwald, 31 juil. 2026, arXiv 2603.24917 | estimer le risque d'extraction quasi litterale | sequences cibles | plusieurs tailles et types | borne inferieure deterministe par recherche en faisceau contrainte | cout equivalent a 20 tirages Monte Carlo contre 100 000 | memorisation litterale | sans rapport | [PROBABLE] |
| 64 | Venkit, Prabhakar, Li, Lee, 30 juil. 2026, *ANCHOR*, arXiv 2607.28818 | une persona et une trajectoire tiennent elles sur le long terme ? | 2 008 conversations, 27 personas, 9 calendriers, 4 modeles | quatre modeles evalues | sonde d'identite a 102 items scelles et sonde de trajectoire a 110 questions contrefactuelles | exactitude de trajectoire 44,4 pour cent en moyenne, rappel de l'etat de l'utilisateur proche du hasard a quatre options ; la retention au questionnaire desaccorde avec le comportement tour par tour | pas d'enquete d'opinion | soutien | [PROBABLE] |
| 65 | Cai, Hu, Li, Ju, Guo, 29 juil. 2026, arXiv 2607.27100 `DEJA AU CORPUS` | un accord agrege survit il a la descente en sous groupes ? | 843 repondants americains, 27 cellules parti x occupation x item, 720 sessions par modele | 8 modeles a poids ouverts, temperature 0,7 | contraste d'equivalence prespecifie, TV, Jensen Shannon, Wasserstein ordinal, RMSE, rapport de variance, entropie, decalage d'ordre | humain `theta = -0,285`, Qwen -0,242 seul dans l'equivalence mais effet global -0,644 contre -0,465 ; **rapport de variance median 0,099**, Phi-4 et Gemma 3 a 0,000 ; **TV humain contre humain 0,098 contre 0,561 modele contre humain** ; decalage d'ordre +0,367 contre +0,036 chez l'humain | un seul domaine, une seule condition de conditionnement, pas de reponses rares | menace directe | [CONFIRME] |
| 66 | Li Y., Wang J., Liu M., Li B. et al., 26 juil. 2026, arXiv 2608.24912 | l'alignement deplace t il, ou retrecit il, la distribution de valeurs ? | ANES, GSS, WVS, replication interculturelle de theorie des perspectives, 406 items, six categories | 18 modeles, plus paires socle contre instruit sur Qwen2.5, plus balayage de temperature | `BTB` deplacement au niveau population, `BWR` direction par question, reference humaine 0 et 0,5 | 83 cellules positives sur 108, 75 `BWR` sur 108 au dessus de 0,5 ; 18 modeles sur 18 positifs en desirabilite sociale, 17 sur 18 en aversion au dommage ; croissance avec la taille, entree au post entrainement, `R^2=0,16` avec la capacite ; **une persona malveillante ne passe jamais sous la reference humaine sur trois axes** ; temperature sans effet au dela de 0,01 ; calibration contrastive a `alpha=0,5` ramene les six categories a la reference | aucun terme inter ni intra, aucun appariement individuel, reference humaine marginale | menace directe | [CONFIRME] |
| 67 | Hu H. et al., 26 juil. 2026, arXiv 2607.23440 | raisonnement ou memorisation sur des devinettes chinoises inedites | xiehouyu nouveaux crees par des linguistes | modeles chinois et anglophones | delta d'exactitude entre items rares existants et items nouveaux | 23,6 pour cent pour les modeles chinois, 5,1 pour les anglophones | linguistique | sans rapport | [PROBABLE] |
| 68 | Plisiecki, Chmielewski, Dudzic, Sterna, 22 juil. 2026, arXiv 2607.20082 | que mesure une auto declaration de modele ? | 206 modeles a poids ouverts, dont **67 paires socle et post entraine du meme point de sauvegarde** | 206 modeles | inventaire de 48 items, deux dimensions, installation de persona et filtrage d'attribution | fiabilite `alpha` 0,82 a 0,94, convergence entre formes `r=0,84`, stabilite a huit mois `r=0,93` ; l'installation monte de 0,20 dans 62 paires sur 67 ; la taille ne predit le filtrage qu'apres post entrainement, `r=-0,42` contre `+0,11` | porte sur l'auto declaration du modele, pas sur la simulation d'un humain | methode utile | [PROBABLE] |
| 69 | Shani-Narkiss, Fire, Tsur, 22 juil. 2026, arXiv 2607.27232 | les modeles saisissent ils la nuance emotionnelle du cadrage ? | 3 011 adultes britanniques representatifs, titres de presse sur des conflits | sept modeles | correlation aux jugements humains, globale et par sous groupe | 0,789 pour le meilleur a 0,4 pour le pire ; alignement global bon mais differences significatives entre sous groupes | pas de simulation de repondants individuels | soutien | [PROBABLE] |
| 70 | Li S., Yao, 22 juil. 2026, arXiv 2607.20589 | que vaut une simulation de persona pour la prediction d'opinion ? | personas de neuf Etats du jeu Columbia, ATP vague 123 | GPT-4.1, coupure declaree juin 2024 | exactitude sur des resultats electoraux et des croyances vaccinales | 8 Etats sur 9 corrects, jusqu'a 0,94 sur les croyances vaccinales | aucune baseline, aucun plancher, contamination probable des resultats electoraux 2024 | methode utile | [PROBABLE] |
| 71 | Douven, 22 juil. 2026, arXiv 2607.18269 | une foule de modeles produit elle une sagesse des foules ? | 254 questions de marche de prediction | 15 modeles | agregation classique et apprise, sous ensemble propre apres coupure | l'ecart apparent entre modeles de pointe et modeles locaux passe de 35,8 a 8,9 pour cent sur le sous ensemble propre | domaine de la prevision | methode utile | [PROBABLE] |
| 72 | Tomašev, Franklin, Osindero, 20 juil. 2026, arXiv 2607.18506 | quelles consequences longues d'un alignement non adaptatif ? | aucune donnee empirique | modelisation de physique sociale | analyse et simulation | risque de verrouillage de valeurs et d'effondrement normatif | theorique | sans rapport | [PROBABLE] |
| 73 | Reizinger, Brendel, 20 juil. 2026, *HALLMARK*, arXiv 2607.18360 | diagnostiquer les verificateurs de citations | 2 526 entrees BibTeX, 14 types d'hallucination | modeles de pointe et agents | taux de faux positifs a taux de base realiste | le taux de faux positifs et non le rappel decide du deploiement | verification bibliographique | sans rapport | [PROBABLE] |
| 74 | Ding J., Guo, Xu, 20 juil. 2026, arXiv 2607.17765 | des agents predisent ils des evenements posterieurs a leur coupure ? | 104 matchs, 416 previsions | quatre modeles de pointe plus le marche | score de Brier, retour sur investissement | les quatre donnent le meme favori dans 92 pour cent des matchs, aucun ne bat le marche | domaine sportif | sans rapport | [PROBABLE] |
| 75 | Huang J., Cucerzan, Jauhar, White, 16 juil. 2026, arXiv 2510.24891 | les modeles savent ils planifier une recherche ? | articles ICML 2025 et Nature Mental Health posterieurs aux coupures | plusieurs | bareme par composante | GPT-5 en tete, marge importante restante | hors domaine | sans rapport | [PROBABLE] |
| 76 | Shoghli, Banani Ardecani, Mohamadi Hezaveh, 15 juil. 2026, arXiv 2607.13798 | comment evolue l'acceptation d'un outil generatif apres usage ? | 124 employes d'une administration, deux vagues appariees | aucun modele simule | tests non parametriques, `k`-means sur trois personas d'acceptation | l'utilite percue baisse ; 40 pour cent des sceptiques montent, 68 pour cent des champions descendent | le mot persona designe un groupe d'employes, pas une simulation | sans rapport | [PROBABLE] |
| 77 | Rahul, Chowdhury, 13 juil. 2026, arXiv 2607.14141 | un panel d'agents peut il estimer les probabilites d'un reseau bayesien ? | un cas d'intention de consultation medicale | panel d'agents LLM avec personas | moyenne tronquee des estimations | la norme subjective domine l'auto efficacite | pas de referent humain, un seul cas | sans rapport | [PROBABLE] |
| 78 | Sharma A., Wang G., 13 juil. 2026, *VoxENES*, arXiv 2607.11706 | les detecteurs d'usurpation vocale generalisent ils ? | 53 628 echantillons bilingues | huit detecteurs | taux d'erreur egale | meilleur modele a 28,98 pour cent | audio | sans rapport | [PROBABLE] |
| 79 | Liu X. et al., 11 juil. 2026, *AgentAbstain*, arXiv 2607.10059 | un agent sait il quand ne pas agir ? | 263 taches appariees, 42 environnements | 17 modeles, 4 harnais | exactitude appariee acte contre abstention | meilleur agent a 59,5 pour cent | agents outillés | sans rapport | [PROBABLE] |
| 80 | Giarimpampa, Meier, Bissyandé, Lenders, 6 juil. 2026, arXiv 2608.16893 | un LLM peut il remplacer un expert dans une enquete d'experts ? | six experts humains de centres operationnels de securite, items categoriels, a choix multiple et Likert | plusieurs modeles, plusieurs reglages, tirages repetes | stabilite entre executions, accord entre modeles, divergence absolue a la reference humaine, dispersion | les modeles sont tres stables entre executions et proches les uns des autres, mais **variance reduite, biais de tendance centrale et opinions homogeneisees** par rapport aux experts, qui se dispersent sur tous les types de question | six experts seulement, pas de plancher de reinterrogation, pas de terme inter | precedent partiel | [CONFIRME] |
| 81 | Zhou S. et al., 6 juil. 2026, *TRACE*, arXiv 2607.04784 | mesurer le raisonnement temporel a difficulte controlee | 1 200 instances synthetisees | huit modeles de raisonnement | correlation performance difficulte, taux de devinette | `r` d'environ -0,96, 28 pour cent de devinettes justes | raisonnement formel | sans rapport | [PROBABLE] |
| 82 | Xiao X., Cheng Y., 5 juil. 2026, arXiv 2609.02899 | la contamination reordonne t elle les classements ? | 47 modeles publics et 74 modeles contamines a dose connue, quatre bancs | 121 modeles | fonctionnement differentiel des items originaux contre paraphrases | dose recuperee a +0,187 point, controle negatif a -0,012, correlation de rang entre classements 0,997 | banc d'essai, mais l'invariance d'item est transferable a une enquete | methode utile | [PROBABLE] |
| 83 | Wang J. A., Wang K., Nie, 2 juil. 2026, *TestEvo-Bench*, arXiv 2607.02469 | les agents suivent ils la co evolution du test et du code ? | 746 taches de generation, 509 de mise a jour | quatre agents | taux de succes, couverture, score de mutation | jusqu'a 77,5 et 74,6 pour cent, en baisse sur les taches recentes | genie logiciel | sans rapport | [PROBABLE] |
| 84 | Liu Y. et al., 2 juil. 2026, *MMBench-Live*, arXiv 2607.01813 | un banc multimodal evolutif preserve t il les classements ? | 5 900 instances nouvelles | modeles vision langage | stabilite des classements, memorisation | classements stables, environ 30 dollars par mise a jour | banc d'essai | sans rapport | [PROBABLE] |
| 85 | Xu Z., Malkin, 1er juil. 2026, arXiv 2607.00403 | a quel point les repondants de plateforme s'aident ils d'un modele ? | series d'enquetes, `N=250` | detection par style et par temps de completion | prevalence d'usage, effet des mesures d'attenuation | **moins de 10 pour cent sur Prolific, plus de 80 sur Mechanical Turk** ; les mesures reduisent l'usage sans ameliorer necessairement la qualite | echantillon reduit, une seule periode | soutien | [PROBABLE] |
| 86 | Zarzecki, Dubiński, Cygert, 1er juil. 2026, arXiv 2606.03305 | les detecteurs d'appartenance tiennent ils hors du laboratoire ? | 335 evaluations, 25 modeles, jusqu'a 27 milliards | trois paradigmes de detection | justesse du verdict | 201 verdicts corrects sur 335 ; faux positifs sous decalage de distribution | banc d'essai, mais le diagnostic de puissance est transferable | methode utile | [PROBABLE] |
| 87 | Benhenda, 30 juin 2026, arXiv 2606.23032 | evaluer des analystes financiers LLM sur une introduction en bourse | 1 000 questions, 70 publiees | plusieurs modeles | exactitude par bareme genere | meilleur modele a 79,8 pour cent | finance | sans rapport | [PROBABLE] |
| 88 | Morosini, Cen, Ilyas, Driss, 29 juin 2026, arXiv 2606.30801 | auditer un algorithme de personnalisation avec des agents a persona fixe | 1 120 agents sur X, plus de 200 000 expositions, 14 personas, trois conditions contrefactuelles | agents generatifs ancres sur des donnees d'enquete demographiques et politiques | amplification de contenu selon l'ideologie de l'utilisateur, effets contrefactuels par sous groupe | le fil algorithmique amplifie le contenu toxique, polarisant et de droite ; **les effets poolés sont nuls la ou les effets par sous groupe varient en direction et en amplitude** | audit de plateforme, pas de fidelite d'opinion | methode utile | [PROBABLE] |
| 89 | Huang Y. et al., 29 juin 2026, *ConsumerSim*, arXiv 2606.30395 | peut on reconstruire un indice de confiance des consommateurs par simulation generative ? | series officielles americaine, europeenne et japonaise, population synthetique calibree sur microdonnees | population de personas plus signaux macroeconomiques datés | metriques de reconstruction contre baselines de persistance, de series temporelles et de regression | premier rang sur les metriques rapportees, gains autour des chocs saillants ; les trajectoires de sous groupes s'alignent en direction et different en amplitude | pas de fidelite individuelle, pas de plancher | methode utile | [PROBABLE] |
| 90 | Guan H. et al., 28 juin 2026, *Light Society*, arXiv 2506.12078 | peut on simuler un milliard d'agents ? | profils demographiques du WVS | melange de modeles complets et de substituts distilles | jeux de confiance et diffusion d'opinion a l'echelle | faisabilite a un milliard d'agents | aucune mesure de fidelite individuelle ni de dispersion contre humain | sans rapport | [PROBABLE] |
| 91 | Yamamoto, Kawahara, 27 juin 2026, *PASTA*, arXiv 2606.28898 | mettre a jour la connaissance d'un modele apres sa coupure | articles de presse posterieurs a la coupure | modele de base plus auto apprentissage DPO | exactitude sur questions factuelles | de 0,02 a 0,82 | mise a jour de connaissance | sans rapport | [PROBABLE] |
| 92 | Zhang Y., Ma Z., 26 juin 2026, arXiv 2601.14264 | les jumeaux numeriques sont ils psychometriquement comparables aux humains ? | plusieurs etudes, dont une vague longitudinale et deux inventaires de personnalite | DeepSeek V3 et V4-Flash, Qwen 2.5 Max et 3.5 Plus, Gemma-4-31B-it, gpt-oss-120b | validite de construit, invariance de mesure de reseau, correlations item par item et de profil, pentes d'erreur | forte exactitude agregee, **correlations item par item systematiquement inferieures aux correlations de profil**, variance compressee, biais heuristiques sous reproduits (omission 0,2 a 9,4 pour cent contre environ 45 chez l'humain), **aucune comparaison humain contre jumeau n'atteint l'invariance metrique**, plus de la moitie des items montrant des chargements differents | pas de terme inter, pas de reinterrogation, pas de reponses rares | precedent partiel | [CONFIRME] |
| 93 | Agostinelli et al., 26 juin 2026, arXiv 2606.27956 | comment le soi interieur et le soi exterieur se relient ils a la sante mentale ? | Human Connectome Project, enquetes plus IRM fonctionnelle de repos | aucun LLM | matrices de correlation, `k`-means sur profils sociaux | le groupe au profil socialement plus desirable a une meilleure satisfaction de vie et une connectivite plus faible du reseau du mode par defaut | pas de LLM, pas de simulation ; le lien a la desirabilite sociale est indirect | sans rapport | [PROBABLE] |
| 94 | Burattini Freire, Cha, Epure, Filippini et al., 26 juin 2026, *SimPol*, arXiv 2606.27968 | la topologie d'un reseau de croyances explique t elle les trajectoires de polarisation en Europe ? | European Social Survey 2016, 23 pays | aucun LLM ; inference de reseau par correlations de Kendall, lasso graphique et reconstruction bayesienne non parametrique, puis modele a base d'agents de Dalege et al. 2025, 2 000 agents identiques par pays sur un reseau petit monde | polarisation multidimensionnelle par variance de la distance euclidienne dans l'espace des croyances, balayage `beta_pers` et `beta_soc` dans `{0,5 ; 2}` | l'immigration figure dans le top cinq de 18 pays sur 23, les droits LGBT de 17, l'interventionnisme economique de 15 ; l'auto positionnement gauche droite predit l'alignement des autres croyances a l'Ouest et non a l'Est ; polarisation maximale a `beta_pers` eleve et `beta_soc` faible, tres forte a l'Ouest et moderee a l'Est ; relation positive entre somme des poids signes du reseau et polarisation finale | **un seul reseau infere pour toute la population, agents homogenes en attention, croyances initialisees au hasard, pas de calibration sur les donnees, pas de LLM** | precedent partiel | [CONFIRME] |
| 95 | Ricci, 23 juin 2026, arXiv 2606.24391 | comment les modeles raisonnent ils sous brouillard de guerre ? | 54 parties, 5 258 actions | 15 modeles de raisonnement | taux de victoire, actions illegales | 78 pour cent de ruee nucleaire, environ 58 pour cent des actions illegales dues au suivi d'etat | jeu strategique | sans rapport | [PROBABLE] |
| 96 | Moon J., Kim, Lah, Han, 22 juin 2026, arXiv 2606.09013 v2 `DEJA AU CORPUS` | les modeles reproduisent ils la forme de la distribution ou seulement la moyenne ? | experience de choix non publique, nouilles instantanees, Coree 2010, 12 conditions promotionnelles, trois types de variable | Gemini-2.5-Pro, GPT-5-nano, GPT-4.1-nano, Qwen2.5-VL et Qwen3-VL, Llama-3.2-11B-Vision | erreur absolue, correlation de motif, Jensen Shannon et Wasserstein, contre trois baselines humaines (marginale, uniforme, delta de moyenne) | **la baseline marginale bat tous les modeles en distance de Wasserstein sur la quantite, 0,641 contre 1,467 pour le meilleur** ; sur l'incidence, la marginale a 0,013 d'erreur et trois modeles inversent le motif ; persona JSON contre texte 0,800 contre 0,720 en `r` ; le raisonnement degrade l'alignement de facon monotone, 0,759 puis 0,722 puis 0,692 | un seul jeu de donnees, aucune heterogeneite conditionnelle a la demographie, les auteurs le declarent | menace directe | [CONFIRME] |
| 97 | Sun G., Zhan, Gales, 22 juin 2026, arXiv 2606.23313 | decontaminer par incertitude plutot que par paraphrase | MMLU-Pro et MATH-MCQA | plusieurs socles | distances distributionnelles par echantillon | distributions plus proches d'un modele non contamine que les baselines | banc d'essai | sans rapport | [PROBABLE] |
| 98 | Wedgwood, Thaker, Kale, Smith, 21 juin 2026, arXiv 2607.24782 | personnalisation, jeu de role et prevision sont ils interchangeables ? | WVS, 101 questions, 13 tranches langue par pays, 21 008 lignes de reponse | GPT-5.4, Claude Sonnet 4.6, Gemini 2.5 Flash, Qwen3-235B | alignement a la distribution humaine appariee selon quatre cadrages d'invite | le cadrage est un determinant de premier ordre ; la prevision a la troisieme personne donne le meilleur alignement directionnel pour trois modeles sur quatre ; les gains se concentrent sur religiosite, roles de genre et valeurs materielles du travail | pas de dispersion intra, pas de plancher, unite agregee | methode utile | [PROBABLE] |
| 99 | Bojic, Matic, Matthes, Cabarkapa, 19 juin 2026, arXiv 2608.07498 | un agent a profil complet predit il des reactions individuelles ? | 296 profils issus d'une enquete, 56 messages dont 26 a verite terrain | 12 configurations, dont GPT-5.5 Pro, Claude Opus 4.7, Claude Haiku 4.5, plus classifieurs supervises | exactitude, kappa entre modeles, **taux d'homogeneisation defini a plus de 90 pour cent d'agents identiques**, ecart type du taux de reaction | 96,68 pour cent avec profil complet, 62,32 avec profil reduit, **51,00 avec la demographie seule contre une baseline majoritaire a 51,1** ; les classifieurs s'effondrent a 15,4 pour cent en laissant un message dehors ; kappa 0,440 contre 0,233 selon la presence d'un ancrage ; **une configuration homogeneise 19 messages sur 56, 34 pour cent** | pas de plancher humain pour l'homogeneisation, reactions binaires j'aime ou non | menace directe | [CONFIRME] |
| 100 | Kotalwar, Das, Rose, 19 juin 2026, arXiv 2606.18413 | quelle structure de collaboration ameliore une equipe humain machine ? | 1 482 sessions dans Collaborative Gym | equipes simulees | performance selon composition et structure | ajouter un collaborateur peut nuire sans structure de coordination | collaboration, pas d'opinion | sans rapport | [PROBABLE] |
| 101 | Zibaeirad, Vieira, 18 juin 2026, arXiv 2606.20502 | l'affinage apprend il a raisonner sur la securite ? | 834 echantillons du noyau Linux, 74 CWE | huit modeles plus 15 variantes LoRA | indices de defaillance directionnelle | meilleure detection a 52,1 pour cent, soit 2,1 points au dessus du hasard ; 84 pour cent des echantillons dits contamines ne portent aucun signal de memorisation | securite logicielle | sans rapport | [PROBABLE] |
| 102 | Wang Z. et al., 17 juin 2026, *ExpertIVS*, arXiv 2608.20355 | reconstruire un systeme de valeurs individuel plutot que concatener des reponses | 480 individus, 12 pays, WVS | 14 agents experts sociologues plus un mecanisme de debat | fidelite de restitution des valeurs, generalisation | 90,78 pour cent de fidelite, +5,3 points de generalisation | aucune dispersion, aucun plancher, aucune baseline non LLM | methode utile | [PROBABLE] |
| 103 | Olza, Santana, Soto, 17 juin 2026, arXiv 2511.14555 | simuler des participants a un neurofeedback decode | aucune enquete | modeles generatifs a variables latentes | reproduction de phenomenes empiriques | reproduit les phenomenes cibles | neurosciences | sans rapport | [PROBABLE] |
| 104 | Krishnappa, Das, Jain, Chadha, 17 juin 2026, *RECOM*, arXiv 2606.19218 | une metrique automatique peut elle a la fois valider et discriminer ? | 15 000 questions r/AskReddit de septembre 2025, posterieures aux coupures | cinq modeles ouverts de 7 a 10 milliards | validite contre plancher de derangement aleatoire, pouvoir discriminant | la similarite cosinus separe le reel du hasard, `d` d'environ 2, mais ne classe pas les modeles, `|d| < 0,1` ; BERTScore s'effondre a `|d| = 0,09` une fois la longueur controlee | texte libre, pas d'enquete | methode utile | [PROBABLE] |
| 105 | Bettencourt, Ding, Giesecke, 17 juin 2026, arXiv 2606.18192 | reconstruire les depots SEC en donnees de pre entrainement | 152 milliards de jetons publies | aucun | recouvrement avec Common Crawl | moins de 0,1 pour cent | corpus | sans rapport | [PROBABLE] |
| 106 | Yehudai, Rozen, Gera, 16 juin 2026, arXiv 2605.30036 | peut on induire une structure de valeurs humaine dans un modele ? | plus de 5 millions de questions, questionnaires valides | modeles de pointe | structure des valeurs et relations valeurs comportement, comparees aux motifs humains | fort accord entre modeles a valeurs induites et humains sur les deux dimensions ; l'injection de distributions de valeurs humaines ameliore les simulations de population | pas de terme intra, pas de plancher, pas de personnes appariees | methode utile | [PROBABLE] |
| 107 | Noever, McKee, 16 juin 2026, arXiv 2608.27459 | un modele local contient il la connaissance testable d'une culture ? | 529 939 indices Jeopardy sur 41 saisons | Qwen2.5-14B en 4 bits | exactitude sous protocole de reponse forcee | 67,0 pour cent au total, 65 sur les indices posterieurs a la coupure contre 95 pour Claude Opus 4.8 | connaissance factuelle | sans rapport | [PROBABLE] |
| 108 | Huang C., Wu, Wang, 15 juin 2026, arXiv 2502.17773 v6 | combien de repondants humains vaut un modele ? | deux jeux d'enquete reels, opinions sociales et test educatif | plusieurs modeles | ensembles de confiance a couverture moyenne garantie, taille d'echantillon simule choisie de facon adaptative | la taille selectionnee mesure la **taille effective de population humaine** que le modele represente ; forte heterogeneite de fidelite entre modeles et domaines | quantite de population, pas de personne ; pas de terme intra | precedent partiel | [CONFIRME] |
| 109 | Ravi et al., 11 juin 2026, arXiv 2606.12805 | l'accent d'un agent vocal change t il la collaboration en classe ? | 33 enseignants, plan inter sujets | agent vocal generatif | perceptions, roles, confiance | l'agent a accent britannique est traite comme un outil, les autres sont anthropomorphises | education | sans rapport | [PROBABLE] |
| 110 | Snoke, 11 juin 2026, arXiv 2606.13902 | comment mesurer le risque empirique quand on synthetise une population entiere ? | commentaire methodologique | aucun | attaques par inference d'appartenance et d'attribut | l'inference d'appartenance devient sans objet quand l'appartenance est publique ; le risque d'isolement augmente | commentaire, pas de mesure | methode utile | [PROBABLE] |
| 111 | Loi, 11 juin 2026, arXiv 2601.14295 | comment eviter le biais de coherence dans la formation de croyances d'un modele ? | arguments attribues a des sources ideologiquement typees | modeles de pointe | penalite de credibilite selon la coherence identite position | les modeles penalisent les arguments dont la source contredit la position attendue, et **ces effets s'effondrent quand les modeles detectent un test systematique** | philosophie normative, mesure secondaire | soutien | [PROBABLE] |
| 112 | Nakayashiki, Watanabe, 11 juin 2026, arXiv 2606.11654 | peut on predire la saillance d'un passage avant qu'il soit lu ? | corpus de surlignage de foule | classement logistique sur plongements contre baseline de position | precision moyenne, amorçage par document | +0,044 de precision moyenne sur la baseline, intervalle [+0,029 ; +0,058] ; l'avantage croit quand la popularite baisse | domaine du texte, pas de l'opinion ; mais le plan preenregistre a plancher est transferable | methode utile | [PROBABLE] |
| 113 | Holtdirk, Ahnert, Sakshaug, Haensch, 8 juin 2026, arXiv 2606.09351 | l'apprentissage en contexte impute t il mieux qu'une methode statistique ? | 150 variables d'opinion, 15 vagues de l'American Trends Panel, plus de 5 millions de reponses imputees, taux de manquant 50 pour cent, mecanismes MCAR, MAR et MNAR | Qwen3-30B-A3B, gpt-oss-120b, plus quatre autres generateurs ; baselines MICE PMM et MICE Forest | erreur absolue sur le coefficient, couverture a 95 pour cent, largeur d'intervalle, MAE individuelle | **les quatre specifications battent MICE PMM et MICE Forest sous les trois mecanismes**, Wilcoxon `p < 0,05` ; gpt-oss-120b a 100 exemples : 0,033 / 0,044 / 0,048 contre 0,068 / 0,092 / 0,068 ; MICE PMM garde la meilleure couverture, 0,964 / 0,971 / 0,935, avec des intervalles deux a cinq fois plus larges ; **la specification qui minimise l'erreur individuelle n'est pas celle qui minimise l'erreur de coefficient** | recouvrement possible d'OpinionQA avec les corpus, les auteurs l'argumentent sans le mesurer ; pas de terme intra | precedent partiel | [CONFIRME] |
| 114 | Varadarajan, Yerukola, Diab, Sap, 8 juin 2026, *CCBENCH*, arXiv 2607.05405 | un modele s'adapte t il aux valeurs signalees implicitement ? | 60 personas, six cultures, 52 questions de sante reelles, 3 120 interactions | cinq modeles de pointe | taux de reponse culturellement appropriee | 20 a 30 pour cent pour le meilleur, +3 a 5 points avec chaine de pensee ; **les modeles reussissent mieux quand la persona s'ecarte de la norme que quand elle la suit** | domaine de la sante, pas d'enquete d'opinion | soutien | [PROBABLE] |
| 115 | Greco, Xu, Domenicucci, He, 4 juin 2026, arXiv 2606.05890 | comment un conseiller moral peut il maintenir l'incertitude ? | dialogues entre modeles sur des dilemmes ethiques, questionnaires avant et apres | modeles ouverts et fermes | divergence entre personas contre couverture a l'interieur d'une persona ; personas declaratives contre narratives | **les modeles ouverts s'alignent sur l'ambiguite humaine par divergence entre personas, les modeles fermes par couverture a l'interieur d'une persona** ; les personas declaratives captent mieux la diversite de position initiale, les narratives une revision de croyance plus realiste | pas de referent humain quantitatif | methode utile | [PROBABLE] |
| 116 | Seo, Choi, Koh, Lee, 4 juin 2026, *OG-MAR*, arXiv 2601.21700 | une ontologie de valeurs ameliore t elle l'alignement culturel ? | WVS et bancs regionaux | quatre socles | alignement culturel et robustesse | ameliore les baselines | pas de dispersion, pas de plancher | sans rapport | [PROBABLE] |
| 117 | Kumar T., Gautam, Chadha, Jain, 4 juin 2026, arXiv 2604.23600 | les traits de personnalite modulent ils le biais de genre d'une persona ? | 23 400 recits en anglais et en hindi | six modeles de pointe | association entre traits HEXACO ou triade noire et representation stereotypee du genre | les traits de triade noire sont associes a des representations plus stereotypees que les traits socialement desirables | generation de recits, pas d'enquete | soutien | [PROBABLE] |
| 118 | Jaenada, Pardo, Prajapat, 4 juin 2026, arXiv 2606.06699 | inference robuste pour des essais de vie acceleres | donnees de fiabilite industrielle | aucun LLM | estimateur a divergence de puissance de densite ponderee | protection contre les valeurs aberrantes a efficacite conservee | statistique de fiabilite ; le mot contamination y a un autre sens | sans rapport | [PROBABLE] |
| 119 | Asai, Lin, Kishimoto, Obi, 4 juin 2026, arXiv 2606.05804 | peut on contraindre un modele a ignorer l'apres coupure ? | trois bancs existants plus un banc multi coupures construit | plusieurs | exactitude sous coupure imposee, notamment sur questions contrefactuelles | le rappel explicite de la contrainte et le rappel d'information pertinente battent la reponse directe et le raisonnement pas a pas | banc de connaissance, pas d'enquete | methode utile | [PROBABLE] |
| 120 | Velutharambath, Falk, Labat, Tater, 3 juin 2026, arXiv 2606.04924 | comment la communaute traite t elle l'usage de LLM par les annotateurs ? | 155 chercheurs interroges | aucun | prevalence declaree, strategies de detection | **44 pour cent ont observe de l'usage de LLM dans leurs donnees**, 93 pour cent s'y attendaient, la moitie ne savent pas quelle precaution prendre | declaratif | soutien | [PROBABLE] |
| 121 | Maiorano, 3 juin 2026, arXiv 2608.13563 | valider des micro simulations d'experience utilisateur par corpus proxy | six corpus proxy publics | pipeline LLM sur Azure OpenAI | Jaccard au sommet et Jaccard pondere par distribution | `W = 0,128` contre 0,000 sur un corpus, instabilite du point d'estimation sous reechantillonnage | domaine de l'interface | sans rapport | [PROBABLE] |
| 122 | Toda, 3 juin 2026, arXiv 2606.05383 | l'IA peut elle refuter une theorie economique ? | quatre articles publies contenant une erreur | Gemini, Claude, ChatGPT | detection de l'erreur | aucun modele ne trouve l'erreur sans guidage humain substantiel | economie theorique | sans rapport | [PROBABLE] |
| 123 | Khetan R., Khetan A., 2 juin 2026, *PoliticsBench*, arXiv 2603.23841 | comment les valeurs politiques s'expriment elles en jeu de role multi tours ? | 20 scenarios evolutifs | huit modeles | nombre de dimensions de valeur fortement activees, engagement dans une position | +0,75 dimension sur 10 aux pics d'interaction, `p < 0,05` ; engagement +1,4 point sur 5 du debut a la decision | pas de referent humain | soutien | [PROBABLE] |
| 124 | Ding R., Gao, Zollo, Bachmat, 2 juin 2026, arXiv 2602.14279 | a qui poser quelle question sous budget contraint ? | trois jeux d'opinion reels | objectif de gain d'information par LLM plus reseau de neurones sur graphe heterogene | prediction de reponse au niveau de la population sous budget | plus de 12 pour cent de gain relatif sur CES a 10 pour cent de budget de repondants | pas de dispersion, pas de plancher | methode utile | [PROBABLE] |
| 125 | Kunkel, Hartwig, Voss, Schütt, 1er juin 2026, arXiv 2606.02741 | quelles attitudes environnementales sont inscrites dans les modeles ? | questions d'enquetes de conscience environnementale, references humaines allemandes | 31 modeles proprietaires et ouverts | comparaison entre modeles et a la reference humaine, robustesse aux conditions d'invite | beaucoup de modeles sont plus progressistes que le repondant moyen, sans relation systematique a l'origine, la taille ou la date ; deplacements sycophantes suivant la position ideologique annoncee | pas d'appariement individuel, pas de dispersion intra | soutien | [PROBABLE] |
| 126 | van der Linden, Kumar, Dixit, Sudan, 1er juin 2026, arXiv 2510.21011 v3 | comment les modeles peuplent ils les professions en genre et en race ? | plus de 1,5 million de personas professionnelles, 41 professions, reference Bureau of Labor Statistics | GPT-4, Gemini 2.5, DeepSeek V3.1, Mistral-medium | **decomposition deplacement contre exageration**, intercept `alpha` et pente `beta` de regression, plus part du premier groupe et entropie intra profession contre BLS | part mediane du premier genre a **1,00** pour DeepSeek et Mistral, 0,99 pour GPT-4, 0,89 pour Gemini ; part mediane de la premiere race 0,97 pour DeepSeek, 0,62 pour Gemini dont l'entropie de race, 1,26, approche celle du BLS, 1,32 ; femmes sous representees de 6,1 points a la profession mediane avec une deviation de pente de +0,17, blancs a -32,1 points avec une pente de +1,13, hispaniques a +9,4 et asiatiques a +3,4 | porte sur la composition demographique des personas generees, pas sur des opinions ; pas de plancher humain de reinterrogation | precedent partiel | [CONFIRME] |

### Recapitulatif du tri

| rapport a la these | nombre | numeros |
|---|---|---|
| menace directe | 9 | 2, 12, 13, 19, 49, 65, 66, 96, 99 |
| precedent partiel | 10 | 6, 21, 38, 51, 80, 92, 94, 108, 113, 126 |
| soutien | 16 | 4, 22, 30, 40, 41, 44, 54, 64, 69, 85, 111, 114, 117, 120, 123, 125 |
| methode utile | 30 | 1, 18, 20, 24, 25, 28, 29, 33, 35, 42, 46, 57, 58, 60, 68, 70, 71, 82, 86, 88, 89, 98, 102, 104, 106, 110, 112, 115, 119, 124 |
| sans rapport | 61 | 3, 5, 7, 8, 9, 10, 11, 14, 15, 16, 17, 23, 26, 27, 31, 32, 34, 36, 37, 39, 43, 45, 47, 48, 50, 52, 53, 55, 56, 59, 61, 62, 63, 67, 72, 73, 74, 75, 76, 77, 78, 79, 81, 83, 84, 87, 90, 91, 93, 95, 97, 100, 101, 103, 105, 107, 109, 116, 118, 121, 122 |

Papiers lus en entier : 19. Numeros 2, 6, 12, 13, 19, 21, 38, 49, 51, 65, 66, 80, 92, 94, 96, 99,
108, 113, 126. Dont cinq deja lus par le projet dans `corpus/lecture-complete` et relus ici pour
verification : 2, 19, 51, 65, 96.
