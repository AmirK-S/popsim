# a10. Verification des sources de la litterature et veille au 7 septembre 2026

Date : 7 septembre 2026. Auteur : agent de recherche a10. Aucun code execute, aucune
microdonnee manipulee. Toutes les verifications sont documentaires.

**Reponse en une ligne pour l'ensemble du rapport.** Les quatre chiffres repris par le projet
existent bien et sont correctement recopies, mais **aucun des quatre ne mesure la quantite que
a1 mesure** : ni le meme jeu de donnees, ni la meme segmentation, ni la meme distance, ni la
meme unite d'analyse, de sorte que l'ecart entre a1 et la litterature n'est pas une anomalie a
expliquer mais une comparaison qui n'aurait jamais du etre faite ; par ailleurs un correctif
publie le 20 aout 2026, LifeMem, occupe deja une partie du terrain que le projet visait.

---

## Table des sources verifiees

| chiffre repris par le projet | source reelle | statut |
|---|---|---|
| ratio d'ecarts types 0,40 a 0,56 | Ozkan, arXiv 2607.18310 | [CONFIRME], mais mesure differente |
| silhouette 0,19 contre -0,02 | Wang et al., LifeMem, arXiv 2608.19621 | [CONFIRME], attribution d'auteur fausse dans exploration/02 |
| gonflement median 2,3 et 2,5, etendue 1,3 a 4,7 | Chen, Zhu, Zheng, arXiv 2607.26348 | [CONFIRME], segmentation differente |
| 0,622 contre 0,589 et 0,393 contre 0,277 | Chen, Zhu, Zheng, arXiv 2607.26348 | [CONFIRME] |
| "une copule gaussienne egale 37 LLM" | Lukauskas et Sarkauskaite, arXiv 2608.14606 | [CONFIRME sur le fond, formulation a corriger] |

---

# Tache 1. Les quatre chiffres de la litterature

**Verdict en une ligne.** Les quatre chiffres sont authentiques et les identifiants arXiv cites
par exploration/02 sont tous les bons, mais trois erreurs de lecture doivent etre corrigees
dans le dossier : le 0,40 a 0,56 n'est pas un ratio intra groupe, le silhouette de 0,19 n'est
pas de "Ling et al." et ne porte pas sur la segmentation que a1 a testee, et le gonflement de
2,5 sur le WVS est mesure avec le **pays** comme axe de segmentation.

---

## 1.a. Le ratio d'ecarts types de 0,40 a 0,56

**Verdict.** [CONFIRME] Le chiffre existe, il est bien dans la source citee, mais c'est un
**ratio d'ecarts types par item sur l'ensemble de la population**, pas un ratio intra groupe
demographique. Le comparer au 0,64 a 0,89 de a1 est une erreur de categorie.

**Source.** Gurkan Ozkan, *Distribution-First Population Simulation: Collapse, Calibration, and
Recall in Non-WEIRD LLM Persona Modeling*, arXiv 2607.18310, version 1 deposee le 17 juillet
2026 a 15h45 UTC, auteur unique.
[CONFIRME] https://arxiv.org/abs/2607.18310

**C'est bien la source citee par exploration/02.** [CONFIRME] La reference 10 de la
bibliographie de exploration/02 pointe sur `arxiv.org/html/2607.18310`, titre et auteur
concordants.

**Methode, telle que lue dans le texte.**

- **Jeu de donnees.** World Values Survey vague 7, **echantillon Turquie uniquement**, 2 414
  repondants reels. Citation du papier : "From the 2,414 real respondents of the WVS-7 Turkey
  wave we derive ... a deterministic character card." [CONFIRME]
  Un seul pays. L'hypothese de a1 selon laquelle "le WVS est international et ses segments
  demographiques y sont imbriques dans des segments nationaux" **ne s'applique pas a cette
  source** : il n'y a qu'une nation. [CONFIRME]
- **Le GSS n'est pas le support du chiffre.** Le GSS n'intervient que dans un resultat annexe
  de suivi temporel, sur "three attitudes that genuinely shifted between the 2016 and 2022 GSS
  waves". Aucun ratio d'ecarts types GSS n'est publie. [CONFIRME]
- **Mesure exacte.** Le papier ecrit : "kept separate, the SD-ratio (model_SD/human_SD) that
  diagnoses under-dispersion. The headline fidelity_score is 100 fois (1 moins TVD) ; the
  SD-ratio is never folded in." Le ratio est calcule **par item de scenario, ecart type des
  reponses du modele sur ecart type des reponses humaines, toutes personnes confondues**.
  [CONFIRME pour la formule, PROBABLE pour "toutes personnes confondues" : le papier ne dit
  nulle part qu'il conditionne sur un groupe demographique, et il n'y a aucune section de
  segmentation.]
- **Aucune segmentation demographique n'entre dans ce chiffre.** Les personas sont
  individuelles et deterministes, une par repondant. Le papier ne definit pas de segments.
  [CONFIRME par absence]
- **Distance et normalisation.** Aucune. Le ratio est un rapport d'ecarts types sur l'echelle
  de reponse d'origine. Le papier **ne precise pas** le codage numerique des modalites, il
  parle de "discrete options" et de "16 fois 3 scenarios". [limite assumee, le codage n'est pas
  documente dans le papier]
- **Modeles.** Trois familles : GLM-5.2, Qwen3.6-35B, Gemma-4-26B. [CONFIRME]
- **Localisation des valeurs.** Tableau 2. Correspondance modele par modele :
  GLM-5.2 0,46, Qwen3.6-35B 0,56, Gemma-4-26B 0,40. Apres correction par Verbalized Sampling :
  1,26, 1,36, 1,37 respectivement, soit un passage de la sous dispersion a la sur dispersion.
  [CONFIRME]
- **Nombre d'agents.** 40 personnages echantillonnes dans le vivier de 2 414 par unite dans le
  resultat 1, 25 agents par unite sur 48 unites dans le resultat 4. Ce sont des effectifs
  faibles. [CONFIRME]

**Est ce que la methode explique l'ecart avec a1 ?** Oui, entierement, et de quatre facons
independantes. [PROBABLE, raisonnement ci dessous]

1. Ozkan mesure une dispersion **globale par item**, a1 mesure une dispersion **residuelle a
   l'interieur de segments demographiques**. Une population simulee peut avoir un ecart type
   global tres reduit tout en gardant une dispersion intra segment moins reduite, et
   reciproquement. Les deux quantites ne sont pas ordonnees l'une par rapport a l'autre.
2. Ozkan simule des scenarios de choix construits, a1 mesure des items d'enquete du GSS.
3. Ozkan utilise trois modeles ouverts de taille moyenne en configuration persona simple, a1
   mesure les sorties du pipeline de Stanford, dont quatre conditions sur six sont ancrees sur
   des reponses reelles de la personne. Un agent ancre sur cent reponses reelles n'a aucune
   raison de s'effondrer autant qu'un agent persona.
4. Ozkan est mono pays et non WEIRD, a1 est sur un echantillon americain.

**Ce qu'il faut refaire chez nous pour comparer a armes egales.** Rien, et c'est le point
important. Il n'y a pas de comparaison a armes egales possible entre ce chiffre et le notre,
parce que ce ne sont pas les memes grandeurs. La bonne decision est de **retirer la fourchette
0,40 a 0,56 de la these du projet** telle qu'elle est formulee dans PASSATION.md section 5 et
CONTEXTE.md, et de la remplacer par une phrase du type : "la dispersion globale par item des
populations simulees tombe a 0,40 a 0,56 de la dispersion humaine sur le WVS Turquie chez
Ozkan 2026 ; la dispersion residuelle a l'interieur des segments demographiques tombe a 0,64 a
0,89 sur le GSS dans notre mesure ; ce sont deux quantites differentes et elles se lisent
ensemble". Si l'on veut malgre tout un chiffre comparable a Ozkan, il faut calculer chez nous
le ratio d'ecarts types global par item, ce que a1 a deja sous la main sous le nom de "mesure
globale de dispersion" a 0,80 a 0,90 en section 9, mais sur trois mesures de dispersion et non
sur l'ecart type d'un codage ordinal. [HYPOTHESE sur la comparabilite de ces 0,80 a 0,90 avec
le 0,40 a 0,56, elle depend du codage employe par Ozkan, qui n'est pas documente]

---

## 1.b. Le score de silhouette 0,19 contre -0,02

**Verdict.** [CONFIRME] Le chiffre existe et est exactement celui annonce, mais **exploration/02
attribue le papier au mauvais auteur**, et la methode reelle valide l'hypothese 3 de a1
(distance euclidienne sur codage ordinal standardise) tout en invalidant la lettre de
l'hypothese 1 (le pays n'est pas une etiquette de segmentation, mais il est dans l'invite de
l'agent et l'echantillon est international).

**Source.** Hexi Wang, Yujia Zhou, Bangde Du, Weihang Su, Xinyuan Cao, Qingyi Pan, Qingyao Ai,
Yueyue Wu, Min Zhang, Yiqun Liu, *Mitigating Identity Essentialism in LLM Agents with
Longitudinal Life Trajectories*, arXiv 2608.19621. Version 1 le 20 aout 2026, version 2 le 21
aout 2026, qui est la version courante.
[CONFIRME] https://arxiv.org/abs/2608.19621

**Correction a porter au dossier.** exploration/02 cite ce papier huit fois sous le nom
"Ling et al." (lignes 237, 604, 651, 1116, 1457, 1662 notamment). **Aucun auteur ne s'appelle
Ling.** Le premier auteur est Hexi Wang. La reference 13b de la bibliographie doit etre
corrigee. [CONFIRME par la page arXiv]

**Methode, telle que lue dans le texte.**

- **Jeu de donnees du chiffre.** World Values Survey vague 7. Citation : "We use Wave 7 of the
  World Values Survey (WVS) and randomly sample 2,000 respondents with seed 42." [CONFIRME]
- **Echantillon international, non restreint a un pays.** Les 2 000 repondants sont tires dans
  l'ensemble des pays de la vague 7. [CONFIRME]
- **Ce n'est pas le jeu de donnees principal du papier.** Le silhouette apparait dans l'analyse
  de motivation, pas dans les tableaux de resultats. Les experiences principales de LifeMem
  portent sur **Add Health, 100 repondants, 6 vagues** et **Understanding Society, 100
  repondants, 15 vagues**. [CONFIRME]
- **Segmentation.** **Trois groupes de statut socio economique**, tertiles d'un score composite
  construit sur quatre variables : classe sociale subjective, situation economique du menage,
  niveau d'education, groupe de revenu. Citation : les repondants sont "divided into low-,
  middle-, and high-SES groups according to the tertiles". [CONFIRME]
- **Le pays n'est pas une etiquette de grappe.** Aucune mention du pays comme variable de
  clustering ou de controle dans cette analyse. [CONFIRME par absence dans la section lue]
- **Mais le pays est dans l'invite de l'agent.** Le gabarit d'invite est : "You are <gender>.
  You are aged <age>. You live in <country> ... Your income is in income group <income group>."
  Les attributs viennent des questions Q260 a Q290 de la section demographique du WVS.
  [CONFIRME]
- **Distance.** **Euclidienne sur l'espace de reponse standardise.** Citation : "Silhouette
  scores are computed in the standardized response space before PCA projection ; PCA is used
  only for visualization." Et : "Each question dimension is standardized before dimensionality
  reduction." Les items sont codes en entiers ordinaux, exemple donne par le papier : groupe de
  revenu 1 pour le plus bas, 10 pour le plus haut. [CONFIRME]
- **Modele.** **Llama-3.1-8B-Instruct uniquement**, un agent par repondant, soit 2 000 agents.
  [CONFIRME]
- **Citation exacte du resultat.** "Human responses are broadly dispersed and substantially
  overlap across SES groups, resulting in a silhouette score of S = -0.02. In contrast, agent
  responses form more compact within-group clusters and show clearer separation between SES
  groups, resulting in S = 0.19." [CONFIRME]
- **Aucun silhouette n'est publie apres correction par LifeMem.** La metrique ne sert que de
  diagnostic d'ouverture. [CONFIRME]

**Est ce que la methode explique l'ecart avec a1 ?** Oui, sur cinq points, et le desaccord
disparait completement une fois les cinq empiles. [PROBABLE, raisonnement]

1. **La distance n'est pas la meme.** a1 emploie l'appariement simple, soit du Gower purement
   categoriel. La source emploie l'euclidienne sur des entiers ordinaux standardises. C'est
   exactement l'hypothese 3 de a1 section 5, et elle est **confirmee**. La standardisation par
   item donne un poids egal a chaque item, et l'euclidienne sur ordinal cree de la structure la
   ou l'appariement simple n'en voit pas.
2. **La segmentation n'est pas la meme.** SES en trois tertiles, aucune des six partitions de
   a1. Le plus proche que a1 possede est l'education, sur laquelle a1 mesure -0,007 chez les
   humains et -0,001 a -0,056 chez les agents. Le SES composite d'un jeu international est une
   variable beaucoup plus separante que l'education americaine seule.
3. **L'echantillon est international.** Meme sans le pays comme etiquette, un agent a qui l'on
   dit "You live in <country>" produit des reponses fortement determinees par le pays, et le
   SES est correle au pays dans la vague 7. La separation par SES capte donc une part de la
   separation par pays. L'hypothese 1 de a1 est **partiellement confirmee** : ce n'est pas la
   segmentation qui contient le pays, c'est l'invite.
4. **Le modele n'est pas le meme.** Llama-3.1-8B-Instruct en persona demographique pure,
   contre le pipeline de Stanford, dont la plupart des conditions sont ancrees sur des reponses
   reelles. Chen et al. (voir 1.c) montrent que Llama-8B est le modele qui gonfle le plus.
5. **Le jeu d'items n'est pas identifiable.** [limite assumee] Le papier **ne dit pas** quelles
   questions du WVS forment l'espace de reponse sur lequel le silhouette est calcule. Il precise
   seulement que "For both human respondents and their corresponding agents, the survey answers
   are converted into response vectors" et que "human and agent responses follow the same
   response labeling, processing, standardization, PCA, and visualization procedure". C'est un
   defaut de reproductibilite de la source, pas de notre lecture.

**Ce qu'il faut refaire chez nous pour comparer a armes egales.** Le test decisif de a1 section
5 doit etre **reecrit**. Il ne s'agit plus de "recalculer le silhouette sur le WVS avec et sans
le pays", puisque le pays n'est pas dans la segmentation source. Le protocole comparable est :

1. Refaire le silhouette **sur le GSS d'abord**, avec la distance euclidienne sur codage
   ordinal standardise, et non avec l'appariement simple. C'est gratuit, c'est immediat, et
   c'est le seul des trois tests de a1 qui ne demande aucune donnee nouvelle. Si le silhouette
   monte fortement, la question du jeu de donnees devient secondaire.
2. Construire chez nous un axe de segmentation **SES composite en tertiles** sur le GSS, a
   partir de l'education, du revenu et de la classe sociale subjective si elle existe dans le
   fichier. C'est l'axe le plus proche de la source.
3. Seulement ensuite, si l'ecart persiste, aller chercher le WVS vague 7. Et dans ce cas, le
   comparateur honnete est un agent Llama-8B en persona demographique pure, pas les conditions
   ancrees de Stanford.

**Un point a garder pour le papier.** La remarque de a1 selon laquelle le silhouette est
lui meme une mesure globale, donc sujette au defaut qu'il est cense reveler, reste valable et
se renforce : la source elle meme n'a pas ose republier ce silhouette apres correction.

---

## 1.c. Le facteur median de gonflement 2,3 et 2,5, etendue 1,3 a 4,7

**Verdict.** [CONFIRME] Les chiffres sont exacts au dixieme pres, mais **sur le WVS l'axe de
segmentation est le pays**, ce qui change entierement la lecture, et l'etendue reelle est de
1,3 a 4,1 sur le GSS et de 2,0 a 4,7 sur le WVS, pas "1,3 a 4,7" comme le raccourci de
PASSATION.md et de CONTEXTE.md le laisse croire.

**Source.** Zihan Chen, Di Zhu, Lei Nico Zheng, *When Synthetic Users Fail: A Cross-Domain
Benchmark of LLM-Simulated Human Survey Responses*, arXiv 2607.26348, version 1 du 28 juillet
2026 a 23h43 UTC.
[CONFIRME] https://arxiv.org/abs/2607.26348

**C'est bien la source citee par exploration/02**, reference 13a. Titre, auteurs et date
concordent au jour pres. [CONFIRME]

**Methode, telle que lue dans le texte.**

- **Definition.** Ecart entre segments : "max_g p_g moins min_g p_g", ou p_g est "the fraction
  of segment g on the high end of the answer scale". Facteur de gonflement :
  "gap_model / gap_human". [CONFIRME]
- **Codage.** Les valeurs d'echelle d'origine, sans renormalisation en 0 a 1. Le gonflement
  porte donc sur une **proportion**, pas sur une distance dans un espace multivarie. Ce n'est
  pas la meme grandeur que la composante de variance inter groupes que a1 calcule.
  [CONFIRME pour le codage, PROBABLE pour la conclusion sur la non equivalence]
- **Medianes.** "median gap is 2.3 times the true human gap on GSS and 2.5 times on WVS", pour
  Sonnet en reponse unique. [CONFIRME]
- **Etendue.** "medians 1.3 to 4.1 times on GSS, 2.0 to 4.7 times on WVS" sur l'ensemble des
  modeles. Haiku et Llama-70B occupent le haut de la fourchette. [CONFIRME]
- **Segmentation.** [CONFIRME, et c'est le point decisif] **Sur le GSS l'axe principal est
  l'opinion politique ("political views"), sur le WVS c'est le pays ("country").** Les segments
  sont definis par paire (question, axe demographique).
- **Donnees.** GSS vagues 2016 a 2024, 14 704 repondants, 85 898 paires (repondant, question)
  sur **10 questions** d'attitude. WVS vague 7, **63 pays**, 91 774 repondants, 1 426 473
  paires sur **16 questions**, presentees comme reprenant le jeu de sondes de WorldValuesBench.
  [CONFIRME pour les effectifs. limite : le depot WorldValuesBench annonce 36 questions de
  valeurs, la source annonce 16 ; je n'ai pas pu reconcilier les deux chiffres.]
- **Modeles.** Claude Haiku 4.5, Claude Sonnet 4.6, Llama-3.1-8B, Llama-3.3-70B. [CONFIRME]
- **Ce que le modele recoit.** Uniquement des attributs demographiques, **aucune reponse
  anterieure de la personne**. GSS : age, sexe, race, diplome le plus eleve, region, opinions
  politiques, identification partisane. WVS : tranche d'age, sexe, niveau d'education, type
  d'habitat, pays. [CONFIRME]

**Est ce que la methode explique l'ecart avec a1 ?** Il n'y a pas vraiment d'ecart a expliquer,
et c'est plutot une convergence. a1 mesure des gonflements de 1,8 a 5,9 selon la condition,
mediane item par item de 1,24 a 2,18. Chen et al. mesurent 1,3 a 4,7 selon le modele. Les
fourchettes se recouvrent largement. [PROBABLE]

Trois differences de methode restent a signaler avant toute mise en regard chiffree.

1. **Le gonflement de Chen porte sur une proportion "haut de l'echelle" par question**, celui
   de a1 sur une composante de variance inter groupes agregee sur 169 items et 6 axes. Le
   premier est un ratio de differences de proportions, le second un ratio de variances.
2. **Sur le WVS, le pays est l'axe.** Un facteur 2,5 signifie ici que le modele caricature les
   differences entre nations. Cela ne dit rien du gonflement entre segments demographiques a
   l'interieur d'un pays. Ce chiffre ne doit donc **pas** etre presente comme "le gonflement
   inter groupes demographiques sur le WVS" dans le dossier.
3. **Chen n'evalue que des agents demographiques purs.** a1 evalue en plus quatre conditions
   ancrees, et c'est justement la ou a1 apporte quelque chose que Chen n'a pas.

**Ce qu'il faut refaire chez nous pour comparer a armes egales.** Ajouter au script a1 une
mesure secondaire "a la Chen" : pour chaque item et chaque axe, la difference max moins min de
la proportion de repondants dans le haut de l'echelle, chez les humains et chez les agents,
puis la mediane du rapport. C'est quelques lignes, cela ne demande aucune donnee nouvelle, et
cela produit le seul chiffre directement comparable a 2,3 sur le GSS. Sans cela, le dossier
juxtapose deux grandeurs differentes sous le meme mot.

---

## 1.d. La regression logistique 0,622 contre 0,589, et la copule gaussienne

**Verdict.** [CONFIRME] Les quatre nombres sont exacts et proviennent du tableau 2 de Chen,
Zhu et Zheng. En revanche la formule "une copule gaussienne egale 37 LLM" de PASSATION.md est
**inexacte dans le detail** : sur le score agrege, le meilleur des 37 modeles bat la copule de
0,02 point ; c'est sur les composantes de correlation et de mediation que la copule bat tous
les modeles.

### Le tableau des baselines, verifie

**Source.** Chen, Zhu, Zheng, arXiv 2607.26348, tableau 2.
[CONFIRME] https://arxiv.org/abs/2607.26348

| predicteur | GSS | WVS |
|---|---|---|
| marginale de question | 0,568 | 0,348 |
| lookup demographique | 0,589 | 0,388 |
| **regression logistique multinomiale** | **0,622** | **0,393** |
| foret aleatoire | 0,583 | 0,366 |
| **meilleur LLM (Sonnet, style C)** | **0,589** | **0,277** |

[CONFIRME] Les chiffres du tableau 2.7.1 de exploration/02, lignes 697 a 701, sont exacts et
n'ont pas ete deformes. Le "devinette aleatoire" n'est pas publie par cette source.

**Details de methode qui manquaient au dossier.**

- **Metrique.** Exactitude en correspondance exacte, "the fraction of individuals whose exact
  answer the model predicts correctly". Ce n'est ni une correlation ni une aire sous courbe.
  [CONFIRME]
- **Protocole.** Un seul partage, pas de validation croisee. Les baselines sont "fit on a
  held-out 50% split of the in-scope pool (assigned by a hash of the respondent id) and
  evaluated on the evaluation-sample rows, which come from the other split". [CONFIRME]
- **Variables.** La regression logistique multinomiale utilise **exactement les memes
  demographies que celles donnees au modele dans l'invite**, encodees en one hot, ajustee
  question par question. C'est ce qui rend la comparaison honnete. [CONFIRME]
- **Style A contre style C.** Style A : le modele rend une seule reponse. Style C : le modele
  rend une probabilite par modalite, en JSON. Le meilleur LLM sur les deux jeux est Sonnet en
  style C. [CONFIRME]
- **Le modele ne recoit aucune reponse anterieure de la personne.** [CONFIRME] C'est le point
  qui delimite la portee de la menace, exactement comme PASSATION.md le dit deja.

### La copule gaussienne

**Source.** Mantas Lukauskas, Viktorija Sarkauskaite, *Plausible but Not Valid: A Psychometric
Audit of LLMs as Synthetic Survey Respondents*, arXiv 2608.14606, 50 pages, 9 figures, declare
en cours de relecture.
[CONFIRME] https://arxiv.org/abs/2608.14606

- **Score PSS.** Copule gaussienne 0,688. Meilleur LLM, gpt-5.4-mini, 0,714. Plafond humain sur
  echantillon retenu 0,825. Citation : "the best LLM barely beats a Gaussian copula with no
  language model at all ... overall copula PSS 0.69 vs. best-LLM 0.71, both far below the 0.825
  ceiling". [CONFIRME]
- **La ou la copule gagne vraiment.** "the Gaussian-copula and MVN baselines outperform every
  LLM : c = 0.95, r = 0.99 for the copula vs. c = 0.52, r = 0.94 for the best LLM". C'est sur
  la structure de correlation inter items et sur la mediation. [CONFIRME]
- **Composition du PSS.** Somme ponderee de six composantes, poids par defaut (0,25 ; 0,25 ;
  0,20 ; 0,20 ; 0,10) sur distribution, correlation, fiabilite, mediation, effets
  demographiques, fidelite au niveau du construit. [CONFIRME]
- **Le ratio d'ecarts types intra item.** Il est **nomme** comme metrique cle, "The SD ratio is
  reported separately because the most common LLM failure mode is range restriction", mais
  **aucune valeur numerique n'a pu etre extraite**. [limite assumee] La ligne de exploration/02
  qui dit "le papier ne publie pas un chiffre unique" est donc correcte et prudente.
- **Donnees.** 263 salaries lituaniens, 68 items, 12 sous echelles, instruments IWPQ, ATC de
  Dunham, UWES-17, plus une echelle auxiliaire. 37 modeles. Environ 65 000 questionnaires
  synthetiques valides en JSON. [CONFIRME]
- **Anomalie a signaler.** La page HTML affiche "arXiv:2608.14606v1 [cs.CY] 06 Jul 2026". Un
  identifiant en 2608 correspond a aout 2026, pas a juillet. L'un des deux elements est
  incoherent. Cela n'affecte aucun chiffre, mais **la date de depot exacte n'est pas etablie**
  et ne doit pas etre citee au jour pres. [limite assumee]

**Correction a porter au dossier.** Remplacer "une copule gaussienne egale 37 LLM" par : "sur
un audit psychometrique de 37 modeles, une copule gaussienne sans aucun modele de langage
atteint un score composite de 0,688 contre 0,714 pour le meilleur modele, et **surpasse les 37
modeles** sur la reproduction de la structure de correlation inter items, r = 0,99 contre 0,94".
C'est plus long, c'est verifiable, et c'est plus dur a attaquer.

**Ce qu'il faut refaire chez nous pour comparer a armes egales.** Rien de neuf du cote de la
menace : a2 a deja construit les baselines. Le seul ajustement utile est de s'assurer que notre
regression logistique est ajustee **question par question** sur les **memes** attributs que ceux
donnes au modele, avec un partage 50 pour cent par hachage de l'identifiant, et que la metrique
rapportee est bien la correspondance exacte. Sinon la comparaison a 0,622 ne tient pas.

---

# Tache 2. Acces aux donnees et licences

**Verdict en une ligne.** Le WVS vague 7 est gratuit mais exige un formulaire et interdit la
redistribution, aucun miroir libre ne contient les reponses individuelles brutes, le GSS est
libre d'acces mais sans licence explicite de redistribution, et **l'archive OSF t6g7k ne
declare aucune licence**, ce qui vaut tous droits reserves par defaut.

---

## 2.a. World Values Survey vague 7

**Acces.** [CONFIRME] Gratuit, sans paiement, mais conditionne a un formulaire. Le parcours est
worldvaluessurvey.org, puis "Data and Documentation", puis "Data Download", puis l'onglet de la
vague 7. Le tutoriel public de Garcia-Vavilla decrit la procedure : "you will be asked to share
information on yourself and intended data usage", avec un champ "FILE USAGE" a renseigner.
https://github.com/maugavilla/well_hello_stats/blob/main/tutorials/2_1_download_WVS.md

**Formats.** csv, R, SAS, Stata, SPSS, livres en archive zip. [CONFIRME, meme source]

**Contenu.** Vague 7, 2017 a 2022, 64 pays et societes, plus de 80 000 repondants selon la
presentation officielle. Les sources secondaires donnent 94 728 participants et 290 questions
communes. [PROBABLE, les deux chiffres circulent selon la version du fichier, v3.0.0 ou
anterieure]

**Redistribution.** [CONFIRME, par preuve indirecte forte] Le depot WorldValuesBench, qui est un
benchmark academique construit sur cette vague, ecrit dans son README : "Due to licensing
issues, we can't distribute the raw data", et renvoie l'utilisateur au formulaire officiel.
https://github.com/Demon702/WorldValuesBench
C'est la meilleure preuve disponible que la licence WVS interdit la redistribution des
microdonnees.

**Usage en local.** [PROBABLE] Rien dans ce qui a ete lu n'interdit le traitement local. La
contrainte porte sur la redistribution, pas sur le calcul. La contrainte 3 de PASSATION.md,
pipeline en local, reste donc suffisante.

**Je n'ai pas pu lire le texte integral des "conditions of use".** [limite assumee] Le site
worldvaluessurvey.org sert ses pages via des appels JavaScript, et les trois URL essayees
renvoient uniquement le squelette de navigation. Le texte des conditions se trouve derriere le
formulaire de telechargement, qui n'est pas accessible sans le remplir. **Avant tout usage
publie, quelqu'un doit remplir le formulaire et lire le texte a ce moment la.**

**Miroir libre : la reponse est non, pour ce dont le projet a besoin.**

| candidat | contenu | licence | utilisable pour le test silhouette ? |
|---|---|---|---|
| Anthropic/llm_global_opinions (GlobalOpinionQA) | 2 556 questions issues du WVS et du Pew Global Attitudes, **distributions agregees par pays uniquement**, pas de microdonnee | cc-by-nc-sa-4.0 | **Non**, il n'y a pas d'individus |
| 3ebdola/wvs2persona | 96 020 fiches persona en anglais, une par repondant de la vague 7, 66 sous ensembles pays | **aucune licence declaree sur la page** | **Partiellement**, voir ci dessous |
| WorldValuesBench | code et protocole, pas les donnees | sans objet | Non |
| GESIS ZA7505 | miroir institutionnel du fichier cross national | non verifiee | inconnu |

[CONFIRME] pour GlobalOpinionQA : https://huggingface.co/datasets/Anthropic/llm_global_opinions
Le jeu contient trois champs, la question, la distribution de reponses indexee par pays, et les
modalites. La carte precise que les auteurs "recognize the limitations in using this dataset to
evaluate LLMs, as they were not specifically designed for this purpose". **Il ne permet aucun
calcul au niveau individuel**, donc ni silhouette, ni decomposition inter et intra. Il ne
remplace pas le WVS pour ce projet.

[CONFIRME] pour wvs2persona : https://huggingface.co/datasets/3ebdola/wvs2persona
Chaque enregistrement contient deux champs seulement, `persona_id` et `persona`, ce dernier
etant "a full English persona description grounded in the respondent's WVS Wave 7 core-variable
responses", soit un rendu en langue naturelle deterministe des reponses decodees. **Les
reponses brutes ne sont pas presentes en tant que telles.** Il faudrait les re extraire du
texte, ce qui est faisable mais fragile. Et la page **ne declare aucune licence**, ce qui est
un probleme en soi puisque la source amont interdit la redistribution.

[non verifie] GESIS. La page search.gesis.org/research_data/ZA7505 renvoie un HTTP 403 aux
outils automatiques. C'est probablement le miroir le plus propre juridiquement, avec une classe
d'acces explicite, mais **je n'ai pas pu lire ses conditions**. A ouvrir dans un navigateur.

---

## 2.b. L'archive OSF t6g7k

**Verdict.** [CONFIRME] **Aucune licence n'est declaree.** Le point ouvert de
data/PROVENANCE.md est tranche, et la reponse est defavorable.

**Preuve.** Interrogation de l'API publique OSF, https://api.osf.io/v2/nodes/t6g7k/ :

- `title` : "LLM Agents Grounded in Self-Reports Enable General-Purpose Simulation of
  Individuals"
- `description` : "Replication materials for: LLM Agents Grounded in Self-Reports Enable
  General-Purpose Simulation of Individuals"
- `date_created` : 2026-04-21T10:11:34 UTC
- `date_modified` : 2026-04-21T10:13:07 UTC
- `public` : true
- `node_license` : **null**
- licence embarquee : absente

[CONFIRME] https://api.osf.io/v2/nodes/t6g7k/

**Ce que cela veut dire.** Sur OSF, un projet public sans champ de licence n'accorde aucune
permission explicite. Public veut dire consultable, pas reutilisable. Le regime par defaut est
donc le droit d'auteur ordinaire, tous droits reserves. [PROBABLE, c'est la lecture standard
de l'absence de licence, mais ce n'est pas un avis juridique.]

**Consequences pratiques pour le projet.**

1. **Telecharger et analyser en local : sans probleme identifie.** Le fichier est publie
   volontairement comme materiel de replication, l'usage de replication est manifestement celui
   auquel il est destine. [PROBABLE]
2. **Versionner ou redistribuer : non.** La regle 5 de PASSATION.md tient, et elle est
   maintenant justifiee par une preuve et non par une prudence generale.
3. **Publier des chiffres agreges derives : oui.** C'est un resultat, pas une redistribution de
   donnees. [PROBABLE]
4. **Publier une trace d'execution contenant les reponses individuelles : non**, et le point de
   droit laisse ouvert dans PASSATION.md section 8 doit se resoudre par la position par defaut
   deja retenue, trace expurgee et renvoi par identifiant.
5. **Une demande ecrite aux auteurs reglerait la question en une phrase.** C'est la seule action
   utile ici, et elle croise la demarche MIT deja prevue.

---

## 2.c. Le General Social Survey sous jacent

**Verdict.** [CONFIRME] Acces libre et gratuit, citation obligatoire, aucune licence de
redistribution explicite trouvee, et une clause de copyright NORC sur les contenus du site.

- **Gratuite et acces.** Le GSS est distribue gratuitement par NORC, et aussi par SDA a
  Berkeley, par iPoll du Roper Center et par ICPSR pour les institutions membres. [CONFIRME]
  https://gss.norc.org/us/en/gss/faq.html
- **Citation exigee.** Forme recommandee : "Davern, Michael ; Bautista, Rene ; Freese, Jeremy ;
  Herd, Pamela ; and Morgan, Stephen L. ; General Social Survey 1972-2024", NORC editeur.
  [CONFIRME]
- **Redistribution.** La FAQ **ne traite pas** la redistribution. La page Terms and Conditions
  de NORC contient en revanche une clause generale : les contenus des sites NORC sont proteges
  et aucune partie ne peut etre reproduite, stockee ou transmise sans consentement ecrit
  expres. [PROBABLE, la clause est generale au site et sa portee sur les fichiers de donnees
  n'est pas explicite]
  https://gss.norc.org/terms-and-conditions.html
- **Le codebook, lui, est sous une permission de type MIT**, "permission to any person
  obtaining a copy ... to use, copy, modify, merge, publish, and distribute". Cela ne couvre
  que le codebook. [PROBABLE, lu via extrait de recherche, non verifie sur le PDF]
- **Consequence.** Le GSS ne pose aucun probleme d'usage. Il ne faut simplement pas versionner
  les fichiers. Position identique a celle deja adoptee.

**Ce que je n'ai pas verifie.** Le texte integral de la page Terms and Conditions de NORC, et
la question de savoir si les fichiers de microdonnees GSS relevent d'un regime distinct de
celui du site. [limite assumee]

---

# Tache 3. Veille depuis le 3 septembre 2026

**Verdict en une ligne.** Aucune equipe n'a publie la decomposition inter et intra de la
variance des populations simulees que le projet vise, la contribution reste libre, **mais un
correctif publie le 20 aout 2026, LifeMem, occupe deja le voisinage immediat et publie des
reductions d'ecart intra groupe de 22 pour cent**, ce qui oblige a repositionner la
contribution 3 de PASSATION.md.

---

## 3.a. La menace principale, LifeMem, deja publie

**arXiv 2608.19621, 20 et 21 aout 2026, Wang et al.**
https://arxiv.org/abs/2608.19621

C'est le meme papier que celui de la tache 1.b. Il faut le relire non plus comme une source de
chiffre, mais comme un concurrent direct.

- Il **nomme** le probleme : "identity essentialism : demographic labels can encourage models
  to treat group-average tendencies as individual traits". [CONFIRME]
- Il **constate** le double phenomene : les agents montrent "stronger within-group compression
  and between-group separation than humans". [CONFIRME]
- Il **propose un correctif** : LifeMem, combinaison d'une recherche d'evenements de vie
  structuree et d'une memoire parametrique propre a l'agent.
- Il **mesure** avec quatre metriques, dont deux qui recouvrent les notres : divergence KL,
  **ecart de distance moyenne intra groupe entre humains et agents**, ecart d'entropie
  normalisee, divergence JS des transitions.
- Il **publie des gains** : sur Llama-8B et Add Health, KL de 5,83 a 4,06 soit 30 pour cent,
  ecart intra groupe de 0,296 a 0,231 soit 22 pour cent, ecart d'entropie de 0,395 a 0,321 soit
  19 pour cent. [CONFIRME]

**Ce qui reste libre pour popsim, et c'est etroit.**

1. LifeMem **ne mesure pas** le terme inter groupes apres correction. Aucun silhouette n'est
   republie, aucun facteur de gonflement. On ne sait donc pas si LifeMem a transporte de la
   variance ou simplement dilate les deux termes. **C'est exactement la question que a1 pose et
   que personne ne repond.** [CONFIRME par absence dans le papier]
2. LifeMem **ne formule pas** la contrainte de somme constante. Le papier decrit son mecanisme
   comme "encoding heterogeneous life experiences into differentiated parametric states", donc
   un ajout de personnalisation, pas une redistribution. [CONFIRME]
3. LifeMem exige des **trajectoires de vie longitudinales**, Add Health sur 6 vagues et
   Understanding Society sur 15 vagues, sur 100 repondants seulement. Le budget de donnees est
   lourd et l'echantillon minuscule.

**Ce qu'il faut faire, ce soir.** Ajouter LifeMem a la section "travaux voisins" du dossier avec
sa vraie attribution, et reformuler la contribution 3 de PASSATION.md en : "mesurer conjointement
les deux termes avant et apres correction, et montrer qu'aucun correctif publie, LifeMem
compris, ne demontre un transport a somme constante parce qu'aucun ne mesure les deux termes
apres son propre correctif". C'est une contribution plus modeste que "aucun precedent trouve",
mais elle est vraie et elle est defendable.

## 3.b. Autres items depuis le 20 aout 2026

Classement par menace decroissante pour la these.

| date | reference | contenu | effet sur la these |
|---|---|---|---|
| 20 aout 2026 | arXiv 2608.19621, LifeMem, Wang et al. https://arxiv.org/abs/2608.19621 | correctif de l'identity essentialism par trajectoires de vie, ecart intra groupe reduit de 22 pour cent | **deja fait par d'autres, partiellement.** Le voisinage est occupe. Voir 3.a |
| 24 aout 2026 | arXiv 2608.23005, Rennard et Xypolopoulos, *Large language models simulate intersectional synthetic identities with a budget of one to two dimensions* https://arxiv.org/abs/2608.23005 | Pew American Trends Panel, 15 vagues, 8 modeles, 21 millions de distributions simulees. Un seul attribut explique mieux la reponse d'une persona a deux attributs que leur combinaison additive dans 75 a 82 pour cent des sous groupes. Les vrais repondants gagnent 2,5 fois en distinctivite quand les identites se croisent, les agents non. Aucun correctif propose. | **renforce fortement.** C'est de l'identity essentialism mesure sur l'intersectionnalite, et cela donne un mecanisme : le modele jette la race et la religion, qui sont les vrais moteurs. Nouvel argument pour la these, et nouvelle source a citer |
| 23 aout 2026 | arXiv 2608.22438, *When Persona Simulations Are Informative: Graph-Structured Signals for Pluralistic Opinion Sensing* | metrique de diagnostic : la reponse de la persona reflete elle un vrai conditionnement | **concurrence sur la metrique.** A lire avant de proposer une metrique standard |
| 20 aout 2026 | arXiv 2608.20539 v2, *ExploraTwin, a Non-Profit Research Platform for Digital Twin Simulations* | plateforme ouverte de simulation d'enquete par jumeaux numeriques, formats standardises | neutre, potentiellement utile comme infrastructure gratuite |
| 14 aout 2026 | arXiv 2608.14079, *The conditional superiority of fast silicon sampling* | les modes rapides de silicon sampling conservent ils la fidelite | a lire, effet inconnu |
| 1er septembre 2026 | arXiv 2609.00565, Zhang, Xu, Zhang, *Aligned but Flattened: Analyzing the Trade-off between Cultural Alignment and Diversity in LLMs* https://arxiv.org/abs/2609.00565 | WVS, six modeles. "the pursuit of cultural alignment consistently incurs an acute expense of diversity, leading to severe cultural flattening". Aucun correctif, appel a de futurs objectifs d'alignement preservant le pluralisme | **renforce.** Documente un arbitrage alignement contre diversite, ce qui est une facon differente de dire "somme constante". A citer a l'appui du corollaire de transport |
| 1er septembre 2026 | arXiv 2609.01038, *Data-Driven Persona-Conditioned Agents for A/B Test Simulation* | agents ancres sur des donnees comportementales, exactitude directionnelle 0,75 a 0,90 sur des tests A/B | neutre, terrain commercial |
| 3 septembre 2026 | arXiv 2609.04485, Czolgowski et Iyasele, *Cultural Misalignment in Large Language Models: Detection, Measurement, and Mitigation Through Targeted Fine-Tuning* https://arxiv.org/abs/2609.04485 | WVS vague 7, 63 personas, 3 pays, 3 modeles ouverts, distance de Wasserstein normalisee. LoRA sur 5 personas defaillantes, moins de 1 200 paires, moins de 15 minutes sur un GPU, reduction du biais de 16,8 pour cent sur Bielik-11B. Aucun modele ne favorise son pays d'origine. | **attention au vocabulaire.** Le papier ecrit "fine-tuning redistributes rather than removes bias : Bielik's worst-case personas swap entirely from American to Chinese elderly, with zero overlap". Le mot "redistribue" est deja pris, mais il designe un deplacement entre personas, pas un transport inter vers intra. Ce n'est pas notre contribution, c'est une collision de vocabulaire a anticiper en relecture |
| 4 septembre 2026 | arXiv 2609.05018, *How a Chatbot's Response Style Shapes a Classroom* | simulation multi agents d'eleves | hors sujet |

## 3.c. Un precedent anterieur qui n'etait pas dans le dossier, et qui compte

**arXiv 2605.16303, 24 avril 2026, Garzon, Baron, Grari, Kamphorst, Bernstein, Detyniecki,
*From Demographics to Survey Anchors: Evaluating LLM Agents for Modeling Retirement Attitudes***
https://arxiv.org/abs/2605.16303

- **Ce papier contient une sous section intitulee "Within-stratum intraclass correlation"**,
  c'est a dire une correlation intraclasse a effets aleatoires calculee a l'interieur des strates
  demographiques, chez les agents et chez les humains. [CONFIRME, le titre de sous section est
  present dans la version HTML]
- Il rapporte que les agents demographiques presentent une correlation intraclasse
  systematiquement superieure a celle des agents ancres sur des reponses d'enquete, autrement
  dit que les agents ancres varient davantage a l'interieur d'une strate, comme les vrais
  humains. [PROBABLE, extrait de recherche concordant, valeurs numeriques non lues]
- Il documente le biais de tendance centrale : "Demographics-only agents ... exhibited
  central-tendency bias, skewing answers toward population means and under-represent the
  variance and tails of the distribution", et une compression severe, ecarts types de 0,16 a
  0,28 sur une echelle de 1 a 7. [CONFIRME]
- **Jonne Kamphorst et Michael Bernstein sont co-auteurs**, donc c'est la meme equipe que le
  papier de reference du projet. Le jeu de donnees est SHARE, sur les attitudes envers la
  retraite. [CONFIRME]

**Pourquoi cela compte.** Une correlation intraclasse est le complement direct d'une
decomposition inter et intra. Ce papier est donc le precedent le plus proche du chantier 1 de
PASSATION.md, il vient de l'equipe meme du papier de reference, et il n'apparait nulle part dans
exploration/02. La contribution du projet reste distincte, parce que ce papier ne mesure pas le
terme inter et ne formule pas de contrainte de somme, mais **le dossier ne peut plus dire
"aucun precedent trouve"** sans le citer. [PROBABLE, sous reserve de lecture du PDF complet]

## 3.d. Mises a jour des papiers suivis

- **arXiv 2411.10109.** [CONFIRME] Toujours en **version 3**, pas de version 4. Historique :
  v1 le 15 novembre 2024, v2 le 22 avril 2026, v3 le 28 juin 2026. Titre courant inchange,
  *LLM Agents Grounded in Self-Reports Enable General-Purpose Simulation of Individuals*. Liste
  d'auteurs relevee : Joon Sung Park, Carolyn Q. Zou, Jonne Kamphorst, Niles Egan, Aaron Shaw,
  Benjamin Mako Hill, Carrie Cai, Meredith Ringel Morris, Percy Liang, Robb Willer, Michael S.
  Bernstein. https://arxiv.org/abs/2411.10109
- **arXiv 2505.17479, Twin-2K-500.** [CONFIRME] Toujours en **version 1**, deposee le 23 mai
  2025. Aucune mise a jour. Auteurs : Olivier Toubia, George Z. Gui, Tianyi Peng, Daniel J.
  Merlau, Ang Li, Haozhe Chen. https://arxiv.org/abs/2505.17479
- **arXiv 2607.26348, Chen et al.** version 1 uniquement, 28 juillet 2026.
- **arXiv 2607.18310, Ozkan.** version 1 uniquement, 17 juillet 2026.
- **arXiv 2608.19621, LifeMem.** version 2, 21 aout 2026.

## 3.e. Actualite des societes

- **Simile.** [CONFIRME] Rien de nouveau depuis le 30 juillet 2026. La serie B de 200 millions
  de dollars a 2 milliards de valorisation est menee par **Greenoaks**, avec Index, Hanabi,
  Bain Capital Ventures, A*, Factory, Definition et **CVS Health Ventures**. Chiffres de
  traction relayes : revenus multiplies par 5 en 5 mois, plus de 50 salaries, dizaines de
  millions de simulations, clients CVS Health, Deloitte, Gallup, Wealthfront.
  https://techcrunch.com/2026/07/30/synthetic-user-startup-simile-raises-200m-at-2b-valuation-5-months-after-100m-series-a/
  **Nouvelle source non presente dans exploration/03** : un podcast Sequoia, *Simulating Humans
  at Scale: Simile's Joon Sung Park*, https://sequoiacap.com/podcast/simulating-humans-at-scale-similes-joon-sung-park
  Non ecoute. [non verifie sur le contenu]
- **Aaru.** [CONFIRME] Serie A multi tranches menee par Redpoint Ventures, valorisation
  affichee 1 milliard de dollars, 88 millions de dollars leves au total. Partenariat annonce en
  aout 2026 avec **Interpublic**, pour l'optimisation de campagnes en temps reel.
  https://www.mrweb.com/drno/news39165.htm
  Ce partenariat n'est pas dans exploration/03.
- **Electric Twin.** [PROBABLE] 31,5 millions de dollars leves, fondee en 2023, siege a Londres.
  Aucune actualite posterieure trouvee. Source secondaire Tracxn, non primaire.

## 3.f. Le point qui devait etre tranche ce soir

**Question posee : quelqu'un a t il publie une decomposition inter et intra de la variance des
populations simulees, ou un correctif qui reduit les ecarts inter groupes ?**

**Reponse, decomposition : non.** [CONFIRME par recherche, avec la reserve d'usage sur les
recherches par absence] Trois requetes distinctes sur l'API arXiv, sur "between-group" et
"within-group" avec "language model", sur "variance decomposition" avec "LLM", et sur
l'intraclasse avec les repondants simules, ne ramenent aucun papier qui publie les deux ratios
ensemble pour des populations simulees. Le plus proche est 2605.16303, qui publie une
correlation intraclasse intra strate sans le terme inter, et LifeMem, qui publie un ecart intra
groupe sans le terme inter apres correction.

**Reponse, correctif reduisant les ecarts inter groupes : non, mais il s'en faut de peu.**
LifeMem reduit la compression intra groupe de 22 pour cent et se donne explicitement pour but de
corriger l'identity essentialism, qui est la cause commune des deux termes. Il est tres probable
que la prochaine version de ce papier, ou un papier concurrent, publie le terme inter. **La
fenetre est ouverte et elle est courte.** [HYPOTHESE]

**Ce que cela implique concretement.** Le chantier 1 de PASSATION.md, la figure de la double
distorsion, garde toute sa valeur et devient **plus** urgent, pas moins. Le chantier 3, le
retrecissement calibre des ecarts inter groupes, doit changer d'argumentaire : il ne peut plus
se vendre comme "aucun precedent", il doit se vendre comme "le seul correctif qui mesure les
deux termes et se contraint a somme constante, la ou LifeMem n'en mesure qu'un".

---

# Tache 4. La reference Nature

**Verdict en une ligne.** Le papier Nature d'Ashokkumar et al. est confirme, reference complete
etablie, et **aucun travail Nature, Nature Human Behaviour ou Nature Medicine de simulation de
populations par LLM en psychiatrie n'a ete trouve** ; la mention de Simon reste sans referent
identifie.

## 4.a. Ashokkumar, Hewitt, Ghezae, Willer

[CONFIRME] Ashwini Ashokkumar, Luke Hewitt, Isaias Ghezae, Robb Willer, *Large language models
can predict the results of social science experiments*, **Nature, volume 656, pages 115 a 122,
2026**, DOI s41586-026-10742-x.
https://www.nature.com/articles/s41586-026-10742-x
Indexation PubMed : https://pubmed.ncbi.nlm.nih.gov/42420458/

Contenu verifie : archive de 70 experiences d'enquete pre enregistrees et nationalement
representatives aux Etats Unis, 469 effets experimentaux, 119 330 participants. Le modele
simule des echantillons representatifs, les effets de traitement sont deduits par comparaison
des reponses simulees entre conditions. **r = 0,85** entre predictions et effets reels, egalant
ou depassant les previsions humaines agregees. Les auteurs signalent que les modeles
**surestiment les tailles d'effet**. [CONFIRME]

Ce dernier point est directement utile au projet : la surestimation des tailles d'effet dans
Nature 656 est la meme famille de defaut que le gonflement inter groupes de Chen et al.
[PROBABLE, rapprochement de ma part, aucun des deux papiers ne fait le lien]

**Note de contexte, non demandee mais utile.** Nature a publie en 2026 un editorial
d'accompagnement, *Judicious use of LLMs could speed up progress in the social sciences*,
https://www.nature.com/articles/d41586-026-01875-0 [CONFIRME sur l'existence, contenu non lu]

## 4.b. Y a t il un equivalent en psychiatrie dans Nature ?

**Non trouve.** [CONFIRME par recherche] La conclusion de exploration/02, point 13 de "ce que je
n'ai pas pu verifier", est maintenue apres une seconde recherche independante.

Ce qui a ete examine et ecarte, avec la raison.

| candidat | reference | pourquoi ce n'est pas le referent |
|---|---|---|
| DT-GPT, jumeaux numeriques de patients | *Large language models forecast patient health trajectories enabling digital twins*, **npj Digital Medicine**, 2025, https://www.nature.com/articles/s41746-025-02004-3 | C'est bien un jumeau numerique de patient par LLM, mais dans **npj Digital Medicine**, pas Nature. Domaines evalues : cancer du poumon non a petites cellules, soins intensifs, Alzheimer. **Pas de psychiatrie.** C'est le candidat le plus proche |
| Revue systematique assistee par LLM | **Nature Medicine**, 2026, https://www.nature.com/articles/s41591-026-04229-5 | C'est une revue de 4 609 etudes, pas une simulation de population |
| Manifestations psychiatriques en depression et anxiete | **npj Mental Health Research**, 2025, https://www.nature.com/articles/s44184-025-00175-1 | LLM d'extraction clinique, aucune simulation de population |
| Jumeaux numeriques en sante mentale | *Blocking the Reflection: Milestones and Hurdles for Digital Twins in Mental Health*, https://pubmed.ncbi.nlm.nih.gov/41856487/ | Article de position, journal non Nature, aucun resultat empirique de simulation |
| Centaur | Nature 2025 | Psychologie cognitive, pas psychiatrie. Deja identifie par exploration/02 |

**Hypothese sur ce que Simon avait en tete, a lui poser directement.** [HYPOTHESE] Trois
possibilites, par ordre de plausibilite : Simon pensait a Ashokkumar et al. et a dit
"psychiatrie" pour "sciences du comportement" ; ou il pensait a DT-GPT et a dit "Nature" pour
"un journal du groupe Nature", ce qui est un raccourci tres courant ; ou il pense a un travail
non publie ou en preprint dont il a eu connaissance par son reseau MIT. **Aucune de ces trois
n'est verifiable sans lui.** Il ne faut pas continuer a chercher, il faut poser la question.

---

# Ce que je n'ai pas pu verifier

1. **Le texte integral des conditions d'utilisation du World Values Survey.** Le site sert ses
   pages en JavaScript et le texte se trouve derriere le formulaire de telechargement. Trois
   URL essayees, aucune n'a rendu le texte. Il faut remplir le formulaire une fois et lire a ce
   moment la.
2. **La page GESIS ZA7505**, qui est probablement le miroir institutionnel le plus propre
   juridiquement, renvoie un HTTP 403 aux outils automatiques. Sa classe d'acces et ses
   conditions restent inconnues.
3. **Le codage numerique des modalites chez Ozkan.** Le papier parle de "discrete options" et de
   "16 fois 3 scenarios" sans jamais dire comment il transforme une modalite en nombre pour
   calculer un ecart type. Sans cela, la comparabilite avec notre mesure globale de dispersion
   n'est pas etablissable.
4. **Le jeu d'items exact du silhouette de LifeMem.** Le papier ne dit pas quelles questions du
   WVS forment l'espace de reponse. C'est un defaut de reproductibilite de la source. Il rend le
   chiffre de 0,19 non reproductible en l'etat, meme avec le WVS en main.
5. **Les valeurs numeriques du ratio d'ecarts types intra item chez Lukauskas et Sarkauskaite.**
   La metrique est nommee et justifiee, aucune valeur n'a pu etre extraite.
6. **La date de depot exacte de arXiv 2608.14606.** La page affiche un identifiant en 2608 et
   une date au 6 juillet 2026, ce qui est incoherent. Ne pas citer la date au jour pres.
7. **Le nombre de questions WVS chez Chen et al.** Le papier annonce 16 questions et declare
   reprendre le jeu de sondes de WorldValuesBench, dont le depot annonce 36 questions de
   valeurs. Je n'ai pas reconcilie les deux.
8. **Les valeurs numeriques de la correlation intraclasse de arXiv 2605.16303.** La sous section
   existe, les valeurs n'ont pas ete extraites. Ce papier merite une lecture complete du PDF, il
   est le precedent le plus proche du chantier 1.
9. **Le contenu du podcast Sequoia sur Simile** et de l'editorial Nature d'accompagnement. Non
   ecoute, non lu.
10. **Tous les chiffres de cette note issus des versions HTML d'arXiv** ont ete lus par un outil
    de lecture automatique. Les citations entre guillemets sont fiables, les tableaux
    reconstitues le sont moins. Avant citation dans un dossier MIT, les tableaux 2 de Ozkan et
    de Chen doivent etre relus sur le PDF.
11. **Une recherche par absence n'est pas une preuve d'absence.** L'affirmation "personne n'a
    publie la decomposition inter et intra" repose sur trois requetes sur l'API arXiv et deux
    recherches web. Elle ne couvre ni les actes de conference non deposes sur arXiv, ni les
    revues de sociologie quantitative, ni les preprints SSRN.

---

# Questions ouvertes pour Simon

1. **La these du projet contient un chiffre qui ne mesure pas ce qu'elle dit.** Le 0,40 a 0,56
   est un ratio d'ecarts types global par item sur un echantillon turc, pas un ratio intra
   groupe. Notre mesure intra groupe est 0,64 a 0,89. Acceptes tu que la these soit reecrite
   avec nos chiffres et que celui de la litterature devienne une note de bas de page ?
2. **Le silhouette de 0,19 est calcule sur une segmentation par statut socio economique en
   tertiles, avec une distance euclidienne, sur un echantillon international, avec
   Llama-3.1-8B.** Rien de tout cela ne correspond a ce que nous mesurons. Faut il reproduire
   leur protocole a l'identique, ce qui coute l'acces au WVS, ou abandonner le silhouette comme
   metrique du projet au motif qu'il agrege et donc masque, ce que a1 argumente deja ?
3. **LifeMem, arXiv 2608.19621, publie le 20 aout, corrige deja l'identity essentialism et
   annonce 22 pour cent de reduction de l'ecart intra groupe.** Il ne mesure pas le terme inter
   apres correction, ce qui laisse notre angle ouvert, mais l'espace se referme. Faut il
   accelerer le chantier 1 pour deposer une mesure avant que quelqu'un ne publie le terme
   manquant, ou considerer que la mesure seule ne suffit plus et qu'il faut le correctif dans le
   meme papier ?
4. **Le precedent le plus proche du chantier 1 vient de l'equipe de Bernstein et Kamphorst
   elle meme**, arXiv 2605.16303, avec une correlation intraclasse intra strate sur les
   attitudes envers la retraite. Cela change t il la strategie de contact avec le MIT et avec
   les auteurs de Stanford, sachant que le sujet les interesse deja ?
5. **L'archive OSF t6g7k n'a aucune licence declaree.** Public ne vaut pas reutilisable.
   Acceptes tu qu'on demande par ecrit aux auteurs une autorisation d'usage, en meme temps que
   la demande d'adresse institutionnelle, plutot que de rester sur une prudence par defaut ?
6. **La reference Nature en psychiatrie n'existe pas dans ce que je trouve.** Le seul jumeau
   numerique de patient par LLM est DT-GPT, publie dans npj Digital Medicine en 2025, sur le
   cancer du poumon, les soins intensifs et Alzheimer, pas en psychiatrie. Est ce que tu penses
   a autre chose, ou est ce le raccourci "un journal du groupe Nature" ?
7. **Question de vocabulaire.** Un papier du 3 septembre, arXiv 2609.04485, emploie deja le mot
   "redistribue" pour designer un deplacement de biais entre personas apres fine tuning. Notre
   "transport de variance a somme constante" risque d'etre confondu avec cela en relecture.
   Faut il changer le nom maintenant ?
