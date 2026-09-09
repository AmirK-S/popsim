# P2. Plan de la nuit sur le SCE : la population simulee de menages, cote machine

Page de plan du run simule du **programme C, version menages**, `MOONSHOTS.md` section 3 et
`brainstorm/03-economie-entreprises.md` M4. Le cote humain est fait : `resultats/c1-anticipations-sce.md`, nuit du 8 au 9 septembre 2026, 82 535 observations,
10 974 menages, 70 mois. Cette page decrit le cote simule, et elle est ecrite **avant le premier
appel**, comme `PROTOCOLES-DE-RECHERCHE.md` section 4 l'exige.

**Amir valide cette page en une ligne avant tout appel.** C'est la seule chose qu'il fait lui
meme, et elle se fait avant de voir le moindre chiffre.

Conventions : **[MESURE]** calcule sur nos donnees, **[CONFIRME]** lu dans une source verifiee
avec son adresse, **[PROBABLE]**, **[HYPOTHESE]**.

Mention de source imposee par la licence FRBNY, a reproduire dans toute sortie :
*Source: Survey of Consumer Expectations, (c) 2013-26 Federal Reserve Bank of New York (FRBNY).
The SCE data are available without charge at www.newyorkfed.org and may be used subject to license
terms posted there. FRBNY disclaims any responsibility or legal liability for this analysis and
interpretation of Survey of Consumer Expectations data.*

---

## La question, en une ligne

Une population simulee de menages, a qui l'on donne soit leurs seules demographies soit leur
propre historique d'anticipations, reproduit elle ce que `c1` a mesure chez les vrais menages
americains : un desaccord presque entierement interne aux cohortes, une moitie de ce desaccord
qui appartient aux personnes, et des revisions **deux fois plus petites** que celles d'une
population correctement calibree sur ses marges ?

---

## 1. Le modele, et pourquoi celui la

**Modele principal : `gpt-oss-20b`, MXFP4, coupure publiee juin 2024** [CONFIRME, carte de modele
OpenAI, arXiv 2508.10925, « Our model has a knowledge cutoff of June 2024 », releve dans
`resultats/a3-inference-locale.md` section 2].

**Modele de variation de coupure : `Meta-Llama-3.1-8B-Instruct`, GGUF Q4_K_M, coupure publiee
decembre 2023** [CONFIRME, carte officielle Meta, champ *Data Freshness*,
https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md].

Les deux Qwen sont **exclus de ce run**, et pas parce qu'ils sont mauvais : `a3` a verifie sur
trois sources independantes, carte de modele, rapport technique arXiv 2505.09388 et documentation
officielle, qu'**aucune date de coupure n'est publiee** pour eux [CONFIRME comme absence]. La
regle de `a3` est ecrite et elle ne se negocie pas ici : toute phrase de la forme « cette periode
est posterieure a la coupure du modele » doit citer Llama ou gpt-oss.

**Pourquoi gpt-oss-20b en principal.** Trois raisons, dans cet ordre. Un, sa coupure, juin 2024,
est **anterieure de neuf mois** a la premiere date notee, mars 2025, donc le choc et sa montee
sont hors du corpus, ce qui est la seule contrainte non negociable de `c1`. Deux, elle est
**posterieure a Llama**, donc le modele connait la trajectoire d'inflation jusqu'au milieu de
2024, ce qui est exactement le contexte macroeconomique qu'un menage reel avait en tete en
decembre 2024, et cela rend le test **plus difficile pour nous et plus juste pour le modele** :
un echec ne pourra pas etre impute a l'ignorance du contexte. Trois, R1 a deja fait tourner ce
modele : le lanceur de serveur, le gabarit harmony, les arrets et le registre existent, et `a3`
mesure son debit en configuration reelle.

**Pourquoi garder Llama 3.1 8B.** Deux coupures distantes de six mois donnent **une variation de
la coupure et non un point unique**, ce que `a3` designe comme un atout. Si les deux modeles
rendent le meme verdict, la contamination par memorisation des agregats publies de la SCE est peu
plausible ; s'ils divergent, la divergence est une mesure et pas un bruit.

**Une precision d'honnetete, recopiee de `a3` et non adoucie.** Une coupure publiee n'est pas une
coupure verifiee. Meta et OpenAI annoncent une date, personne ne l'a auditee. Le controle
empirique reste a faire : le denombrement par infini-gramme des agregats publies de la SCE pour
les mois notes est joint comme variable de controle, et non comme preuve.

---

## 2. Les cohortes et les mois

**Six cohortes**, les six cellules pleines les plus peuplees du perimetre de `c1`, qui portent a
elles seules **48 pour cent** des observations [MESURE, c1 section « ce que le run simule devra
montrer »] :

| cohorte age x diplome x revenu |
|---|
| 40 a 60 x diplome x plus de 100 k |
| moins de 40 x diplome x plus de 100 k |
| moins de 40 x diplome x 50 a 100 k |
| 40 a 60 x diplome x 50 a 100 k |
| plus de 60 x quelques annees x moins de 50 k |
| plus de 60 x diplome x 50 a 100 k |

**Cent menages tires par cohorte, soit 600 agents**, chacun apparie a un menage reel du panel et
portant son historique reel. Tirage par graine fixee et journalisee, sans remise, parmi les
menages presents sur les sept mois du perimetre.

**Les mois.** Deux fenetres, definies par la regle de `c1` et par elle seule.

| fenetre | mois | role |
|---|---|---|
| **contexte** | decembre 2024, janvier 2025, fevrier 2025 | historique donne a l'agent en regime C3, jamais note |
| **notee** | **mars, avril, mai, juin 2025** | quatre mois notes, un appel par agent et par mois |

Cette fenetre notee est choisie pour contenir **les deux regles de choc de `c1` a la fois**, ce
qui est la seule facon de ne pas rejouer l'arbitrage apres coup :

- la **regle primaire**, plus grand saut mensuel de la moyenne en valeur absolue, designe
  **juin 2025**, saut de **moins 0,62 point**, qui est le **retournement** [MESURE, c1 4.3] ;
- la **regle secondaire**, plus grand saut de l'ecart interquartile, designe **avril 2025**, saut
  de **plus 0,72 point** [MESURE, c1 4.3] ;
- et **la montee depuis decembre 2024** vaut **plus 1,17 point** cumules jusqu'en avril, faite en
  trois mois dont aucun ne bat isolement le retournement de juin. C'est la lecon de methode de
  `c1` : une regle de saut mensuel maximal ne trouve pas un episode qui dure un trimestre, elle
  trouve sa fin.

**Toutes les quantites du run sont donc rendues sous les deux regles**, la primaire portant le
verdict, la secondaire publiee entierement a cote et jamais substituee. C'est le traitement exact
que `c1` applique au cote humain.

**Ce que l'agent ne recoit jamais** : la moyenne du mois cible, la marginale de sa cohorte au mois
cible, aucun agregat publie de la SCE, aucune date posterieure a la fenetre de contexte presentee
comme connue.

---

## 3. Les conditions

Trois conditions appelees, quatre adversaires a zero appel.

### Conditions appelees

| code | ce que l'agent recoit | ce qu'elle teste |
|---|---|---|
| **C2** | l'etiquette de cohorte seule : age, diplome, revenu, region, numeratie. Aucune reponse du menage. | ce qu'un gabarit demographique peut rendre |
| **C3** | tout ce que C2 recoit, **plus ses propres anticipations des trois mois de contexte**, en clair, plus le mois courant | ce que l'historique de la personne ajoute |
| **DESC** | aucune incarnation : le modele **decrit la distribution de la cohorte** pour le mois cible | la voie description de `a27`, l'adversaire bon marche que M4 designe |

### Adversaires a zero appel, calcules sur les memes menages et les memes mois

| code | definition | ce qu'il coute |
|---|---|---|
| **P** | persistance : la valeur du mois precedent | une ligne de code |
| **D** | les cinq demographies seules, foret hors pli | quelques secondes |
| **T1** | la moyenne de la cohorte, estimee hors pli | quelques secondes |
| **TIRAGE** | **le controle statistique par tirage** : chaque menage recoit a chaque mois une valeur tiree dans la loi empirique de sa cohorte a ce mois. Les deux marginales et la derive par cohorte sont conservees, l'appariement des personnes est detruit. | 50 replicats, quelques minutes |

**TIRAGE est le controle qui porte le resultat neuf de `c1`**, et il faut le dire en clair : il
n'est pas un temoin de nullite, il est la **population correctement calibree sur ses marges**, et
il fait bouger ses menages **deux fois trop** entre deux mois. C'est contre lui que se lit
l'ampleur des revisions de la population simulee.

---

## 4. Les quantites a rendre, avec la cible humaine en face

Cinq nombres, tous sur `infl1`, tous deja mesures chez les humains
[MESURE, `c1-cibles-jumeau.csv`].

| quantite | cible humaine | ce qu'un echec veut dire |
|---|---|---|
| **part inter cohortes** | **0,019**, mediane mensuelle, maximum 0,048 sur 70 mois | une valeur proche de 1 dit que la population simulee a mis tout son desaccord entre les cohortes, ce qui est la signature du gabarit ; une valeur proche de 0,019 est la seule facon de rendre a une banque centrale ce qu'elle n'a pas deja |
| **part stable** | **0,525**, IC [0,510 ; 0,539], a lire entre le retest a un mois 0,659 et le retest a onze mois 0,280 | une valeur proche de 0 dit que la simulation tire un menage neuf a chaque mois ; une valeur proche de 1 dit qu'elle a fige la personne et n'a plus de revision |
| **chute sous permutation intra cohorte**, anticipation du mois suivant | **superieure a 0,639** pour egaler l'historique du menage, **superieure a 0,615** pour battre la persistance seule ; **0,034** est ce que rendent les demographies seules ; **0,000** est le temoin de cohorte a plein echantillon | sous 0,615 la branche jumeaux ferme ; sous 0,034 la simulation ne fait pas mieux que cinq demographies ; a 0,000 exactement, c'est un bug et pas un resultat |
| **rapport d'ampleur des revisions contre son propre nul a derive** | **0,43**, plage de 0,427 a 0,554 sur les neuf variables ; **1,00 est la valeur d'une population sans appariement des personnes** | un rapport de 1,00 dit que la population simulee bouge deux fois trop, comme TIRAGE, donc qu'elle n'a pas de personnes dedans |
| **chute sur qui revise au choc** | **0,287** pour l'historique complet, dont **0,140** pour la seule volatilite passee ; les demographies seules rendent **moins 0,032**, a lire comme nul | c'est le transport du resultat de `i1` a une variable continue et a un choc macroeconomique |

**La barre, ecrite ici et non apres.** Une population simulee de menages, evaluee sur les memes
mois, les memes cohortes et la meme permutation, doit atteindre une chute superieure a **0,639**
pour egaler l'historique du menage et superieure a **0,615** pour battre la persistance, qui coute
zero appel ; elle doit reproduire une part inter cohortes de **0,019** et non de 1, une part
stable de **0,525** et non de 0, et un rapport d'ampleur de **0,43** et non de 1,00.

**La question qui commande le run, tranchee ici.** `c1` question 1 demande contre quel adversaire
le jumeau est note, puisque la persistance capte **96 pour cent** de ce que la foret va chercher.
Reponse retenue : **le jumeau est note sur ce qu'il ajoute a `P`, la partie residuelle**, la chute
complete etant publiee a cote et jamais a la place. Un jumeau qui bat la persistance de deux
centiemes aura battu la persistance, et cela ne voudra rien dire ; il faut l'avoir ecrit avant.

**Les quatre variables secondaires**, rendues avec les memes quantites et les memes cibles :
`infl3` (part inter 0,011, part stable 0,495, chute `P` 0,582), `infl1_point` (0,054 ; 0,465 ;
0,560), `infl1_var` (**0,119** ; 0,616 ; 0,614) et `perte_emploi` (0,010 ; 0,559 ; 0,689).
`infl1_var` merite une ligne a part : c'est la **seule** variable ou la cohorte explique une part
non negligeable du desaccord, 0,119 en mediane et 0,198 au maximum, en hausse continue depuis
2020, et c'est le seul endroit du dossier ou un gabarit de cohorte a quelque chose a rendre. Si la
population simulee doit reussir quelque part, c'est la.

---

## 5. Les appels et les heures

| bloc | calcul | appels |
|---|---|---|
| `infl1`, principal | 600 agents x 4 mois x 2 regimes (C2, C3) | **4 800** |
| quatre variables secondaires | 4 x 4 800 | **19 200** |
| voie description, DESC | 6 cohortes x 4 mois x 5 variables | **120** |
| **sous total gpt-oss-20b** | | **24 120** |
| bras de coupure, Llama 3.1 8B, `infl1` seul | 600 x 4 x 2 | **4 800** |
| **total** | | **28 920** |

Debits mesures par `a3` en configuration reelle, prefixes de persona compris : gpt-oss-20b
**7 212 appels par heure**, Llama-3.1-8B sous llama.cpp **6 384 appels par heure** [MESURE, a3
section 5.1].

| bloc | duree |
|---|---|
| 24 120 appels sur gpt-oss-20b | **3 h 21** |
| 4 800 appels sur Llama 3.1 8B | **0 h 45** |
| **total machine** | **4 h 06** |
| marge pour le chargement des serveurs, les prefixes C3 plus longs, les relances | + 1 a 2 h |
| **a annoncer** | **une nuit, 4 a 6 heures** |

Les adversaires a zero appel, `P`, `D`, `T1` et TIRAGE avec ses 50 replicats, tiennent en quelques
minutes sur quatre coeurs, hors du chemin critique.

**Parse.** Une seule ligne non vide, un nombre entre moins 50 et plus 50 avec au plus une
decimale, rien d'autre. **Une relance et une seule, sans aucun chiffre d'exemple** : R1 a mesure
que sur 13 relances, **11 recopient l'exemple chiffre a la virgule pres** chez Qwen3-4B, taux de
0,846 [MESURE, r1 section 4.1]. C'est la correction que `a46` a deja inscrite dans son plan et
elle est reprise ici sans discussion.

---

## 6. Les criteres de chute, ecrits avant

Six criteres. Chacun commande sans debat le jour venu.

1. **Plus de 25 pour cent de rejets de parse pour un modele sur une variable** : cette variable
   sort pour ce modele, et le taux est publie.
2. **Valeur constante d'un agent a l'autre a l'interieur d'une cohorte**, ecart type intra cohorte
   sous 0,1 point : le modele rend une etiquette et pas des personnes ; le run est un run de
   gabarit et se publie comme tel.
3. **C3 ne bat pas `P` sur la chute**, c'est a dire chute inferieure a 0,615 : **la branche jumeaux
   du programme C version menages ferme**, et le banc devient un banc de statistique, comme
   `MOONSHOTS.md` l'ecrit deja.
4. **C2 fait aussi bien que C3**, ecart de chute inferieur a 0,02 : le regime a etiquette suffit,
   et le dossier a trouve un **contre exemple a `a44`**, ce qui vaudrait d'etre publie tel quel et
   n'est pas un echec.
5. **Part inter cohortes de la population simulee superieure a 0,15**, c'est a dire huit fois la
   valeur humaine : la simulation fabrique du desaccord entre cohortes la ou les humains n'en ont
   pas, et aucune de ses autres quantites n'est interpretable.
6. **Contamination** : si la valeur mediane rendue par un modele pour un mois note tombe a moins de
   0,1 point de l'agregat publie de la SCE pour ce mois, sur plus de deux des quatre mois, la
   variable est declaree suspecte de recitation et sort du verdict, le denombrement par
   infini-gramme etant joint.

**Ce qui n'est pas un critere de chute et qu'il ne faut pas confondre.** Un echec de la
population simulee a battre la persistance **n'invalide pas le run** : c'est le resultat que `i1`
et `c1` rendent probable, il ferme une branche, il se publie, et il interdit de vendre du ciblage
individuel. Le run est concu pour que le non vaille le oui.

---

## 7. Ce que chaque issue voudrait dire pour une banque centrale

Quatre issues, et les quatre se publient.

**Issue 1. C3 reproduit 0,019, 0,525 et 0,43, et bat `P` sur la partie residuelle.** Une population
simulee de menages porte le **desaccord par cohorte**, qui est deja une variable de politique
monetaire, et elle le porte au niveau de la personne et non de la moyenne. Une banque centrale
peut alors simuler une population de menages pour une question qu'elle ne peut pas poser a son
panel : une annonce, un scenario tarifaire, un changement de communication, teste avant d'etre
subi. C'est l'issue qui justifie un achat, et c'est la moins probable au vu de `c1`.

**Issue 2. C3 reproduit les trois quantites de forme mais n'ajoute rien a `P`.** La population
simulee est un **generateur de populations synthetiques honnete** : elle rend une dispersion
realiste, une stabilite realiste et une ampleur de revision realiste, et elle ne predit personne.
Pour une banque centrale, c'est un outil de scenario agrege, pas un outil de ciblage. Le livrable
est une norme de qualite : **trois nombres a exiger d'un fournisseur de population synthetique**,
0,019, 0,525 et 0,43, avant d'en acheter une.

**Issue 3. C2 fait aussi bien que C3.** L'etiquette suffit, donc l'historique de la personne
n'apporte rien, donc la population simulee est un gabarit de cohorte deguise. Pour une banque
centrale, la lecon est directe et couteuse pour les vendeurs : **une population synthetique qui
n'a pas recu les reponses anterieures des menages rend la moyenne de cohorte qu'elle avait
deja**, et 98 pour cent du desaccord qu'elle cherche est perdu.

**Issue 4. La population simulee rend un rapport d'ampleur proche de 1,00.** C'est l'issue la plus
instructive et la plus severe. Elle dit que la population simulee **bouge deux fois trop**, comme
une population dont chaque menage est retire au hasard dans la loi de sa cohorte a chaque mois.
Une banque centrale qui s'en servirait pour evaluer la volatilite des anticipations, la vitesse
d'ancrage ou la reaction a une annonce **surestimerait systematiquement la reactivite des
menages**, et donc l'effet de sa propre communication. Ce rapport coute zero appel, il se calcule
sur n'importe quelle population simulee avec le meme code, et c'est le candidat le plus serieux au
titre de **quantite de verdict du dossier** : la question ouverte 3 de `c1` demande de trancher,
et ce run est le premier endroit ou il sera calcule sur une population simulee.

**Ce qu'aucune issue ne permettra de dire.** Rien sur la direction des revisions au niveau
individuel : `c1` mesure que la direction est integralement portee par le retour a la moyenne sur
la valeur precedente, chute de **0,150** pour le niveau d'avant seul contre **0,124** pour
l'historique complet [MESURE, c1 6.2]. Rien sur la population americaine : les champs de
ponderation existent et ne sont pas utilises, toutes les quantites sont des quantites
d'echantillon. Rien sur l'origine du choc : que la montee de janvier a avril 2025 soit l'effet des
annonces tarifaires est une hypothese, aucune donnee externe n'a ete consultee [HYPOTHESE, c1].

---

## 8. Ce qui est fige avant le run, et ce qui reste ouvert

**Fige ici** : les six cohortes, les 600 menages et leur graine, les deux fenetres de mois, les
deux regles de choc et le fait que les deux sont publiees, les trois conditions appelees et les
quatre adversaires, les cinq quantites et leurs cibles, la notation sur la partie residuelle de
`P`, les six criteres de chute, le parse et l'unique relance sans exemple chiffre, les deux
modeles et leurs coupures.

**Reste ouvert, et a trancher par Amir dans sa ligne de validation** : faut il **ouvrir le fichier
2013-2016** de la SCE, qui ajoute 43 mois et 8 735 menages et ne sert a rien pour le choc de 2025,
mais donnerait douze ans de trajectoire de dispersion et l'episode de 2015-2016 comme second point
hors crise (`c1` question 6) ? Ce run n'en a pas besoin ; la reponse peut etre non sans rien
coder.

## 9. Rejouer

```
cd /Users/amirkellousidhoum/Desktop/Code/Projets/popsim

# les adversaires a zero appel, deja ecrits, sur les memes menages et les memes mois
.venv/bin/python analyses/c1_cibles.py

# le run simule, seul script de ce plan qui appelle un modele
# (a ecrire ; il importe de r1_oracle_camps le lanceur de serveur, les gabarits,
#  les arrets et le registre des modeles, comme a46_run_composition.py le fait deja)
```

**Aucun script existant ne doit etre modifie. Tout ce qui est produit porte le prefixe `p2`.**
