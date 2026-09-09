# 01. Lecture complete : simulation d'individus et de populations, fidelite, ce qui est perdu

Theme 01 de la lecture complete. Methode : `corpus/lecture-complete/00-CONSIGNE.md`. Grille :
`corpus/00-GRILLE.md`. Table de depart : `corpus/01-simulation-individus-populations.md`
(entrees T1.01 a T1.50). These a eprouver : `ARBITRAGE.md`, « une societe simulee a partir
d'etiquettes remplace chaque personne par son groupe ».

Rendu le 8 septembre 2026, au soir.

**Ce que cette session ajoute.** Les cinquante entrees de la table de depart ont ete reprises une
par une, en remontant (`referenced_works` OpenAlex, `/references` Semantic Scholar) et en
descendant (`filter=cites:` et `/citations`) leurs citations. Vingt trois references nouvelles sont
entrees dans la table, dont **seize lues en entier**. Le chantier s'arrete ici parce que les deux
derniers passages de citations sur les papiers les plus recents (Chen 2607.26348, Ku 2607.03091,
LifeMem 2608.19621, Ma 2606.30085) ne rendent plus qu'un ou deux titres deja connus, et parce que
les citations aval de CoMPosT et de Hwang, qui sont les deux racines conceptuelles du theme, ne
ramenent plus que des travaux de personnalisation sans verite terrain de population.

**Trois trouvailles changent le dossier.** Elles sont donnees ici parce qu'elles conditionnent la
lecture de tout ce qui suit.

**1. Le mecanisme central de la these est publie, mesure, et il porte un nom : le budget
d'identite.** Rennard et Xypolopoulos (L1.01, arXiv 2608.23005, aout 2026) mesurent sur 15 vagues
du panel Pew et 21,1 millions de distributions simulees que les sous groupes humains reels se
composent additivement, poids median `(alpha, beta) = (0,95 ; 0,95)`, **total 1,83**, tandis que
les huit modeles testes se placent sur la ligne `alpha + beta = 1`, **total median 0,98**. Une
persona a deux etiquettes se comporte comme une seule. C'est exactement « remplacer la personne par
son groupe », a ceci pres que le papier montre que le modele ne garde meme pas le bon groupe : la
dimension retenue s'accorde avec la dimension humainement dominante dans 53,3 a 57,9 pour cent des
cas contre un plancher de permutation a 50,4 a 52,2. **La these du projet n'est plus vierge. Ce qui
reste vierge, c'est le niveau individuel : Rennard et Xypolopoulos travaillent sur des
distributions de cellules, jamais sur des personnes appariees.**

**2. Le denominateur du probleme est publie lui aussi, avec plancher humain.** Ahn, Mao et Lee
(L1.02, arXiv 2608.29455) retirent la moyenne humaine de chaque item et mesurent ce qui reste :
`R^2` demeane de **3,05 pour cent** contre un plafond de fiabilite test retest de **53,6 pour
cent**, soit **5,7 pour cent du plafond**. Et le LLM perd contre la moyenne des autres repondants :
`r` moyen par personne 0,34 contre 0,45 pour un simple `leave-one-out` sur la moyenne d'item
(`dz = -0,55`, `p` de l'ordre de `4,6e-95`). C'est la premiere fois que le champ publie une
exactitude individuelle **et** un plancher de fiabilite **et** un plancher trivial dans le meme
tableau. Le point 3 de « Ce que personne n'a fait » de la table de depart est donc a reecrire.

**3. Un resultat de L1.01 contredit frontalement la partie « caricature » du dossier.** Sur les
memes cellules, les distributions simulees sont **plus dispersees** que les humaines a toutes les
profondeurs, `delta H = +0,18 a +0,23` nats, et les auteurs ecrivent : « the much-discussed
"flattening" of identity groups is between-group, not within: a hedge, not a caricature ». Cela
s'oppose a Wang, Morgenstern et Dickerson (T1.10), a Cheng, Piccardi et Yang (L1.04) et a la
robustesse du biais d'homogeneite de L1.20. La variable qui explique la contradiction est
identifiee en section « Ce qui se contredit » : c'est **le format de sortie**, texte libre contre
distribution fermee. Cela vaut directement pour nous, dont toute la chaine est en choix fermes.

---

## Table etendue

Convention de certitude inchangee. **[CONFIRME]** : methode et resultats lus dans le texte au cours
de cette session. **[PROBABLE]** : resume lu a la source primaire. **[NON LU]** : titre seulement.
Colonne « trouve par » : `table initiale` (deja dans corpus/01), `citation amont` (reference d'une
entree confirmee), `citation aval` (papier citant une entree confirmee), `citation aval niveau 2`.

| id | reference | question posee | donnees | modeles | mesure exacte | resultat chiffre principal | faille ou limite | rapport a la these | trouve par | certitude |
|---|---|---|---|---|---|---|---|---|---|---|
| L1.01 | Rennard (MIT), Xypolopoulos (Polytechnique), 24 aout 2026, « Large language models simulate intersectional synthetic identities with a budget of one to two dimensions », arXiv 2608.23005 | un modele a qui l'on donne deux ou trois etiquettes conditionne t il sur toutes, ou en jette t il ? | **15 vagues du Pew American Trends Panel W26 a W92, 2017 a 2021**, 67 a 128 questions fermees et 2 524 a 10 221 repondants par vague ; toutes cellules a `n >= 20` sur 7 dimensions ; 31 profils a un trait, 405 a deux, 1 355 a trois ; **15,7 millions de distributions simulees en pipeline principal, 21,1 millions au total** | GPT-4o, GPT-4o-mini, GPT-5.5, Claude Haiku 4.5, Claude Sonnet 5, Gemma-2-9B, Mistral-7B, Llama-3.1-8B ; temperature 0,7 ; le modele repartit 1 000 repondants hypothetiques sur les options | **contest de composition** : le biais de paire `e_AB = p_chapeau_AB - p_AB` est il mieux explique par la somme `e_A + e_B` ou par le meilleur biais simple, en cosinus ; **decomposition par moindres carres** du vecteur realise en `alpha` fois A plus `beta` fois B ; **index de collapse recalibre** entre deux bornes construites sur le bruit run a run du modele lui meme | **le meilleur trait simple gagne dans 78,4 pour cent [77,8 ; 79,0] des cellules pour GPT-4o-mini, 75,3 a 81,2 chez les sept autres, dont 79,1 pour GPT-5.5 et 77,8 pour Claude Sonnet 5** ; index auto calibre 0,83 a 0,95, soit six septiemes du chemin vers l'effondrement pur. **Budget : humains `(0,95 ; 0,95)`, total median 1,83 ; modeles sur la ligne `alpha + beta = 1`, total median 0,98 (0,91 a 1,03), part dominante mediane 0,88, 63 pour cent des cellules au dessus de 0,75.** Profondeur 3 : l'additif complet ne gagne que 7,8 a 10,0 pour cent, index 0,92 a 0,98. Contest en espace de steering sur cellules identiques : **humains 44,4 pour cent de 236 752 cellules contre un plafond de 49,3, soit 90 pour cent de leur plafond ; GPT-4o-mini 9,3 contre son plafond de 29,7, soit 31 pour cent** | l'unite est la cellule demographique, **jamais l'individu** ; un seul pays, une seule langue, une seule famille d'instruments ; les statistiques de composition sont internes a la geometrie du modele | **soutient, et c'est le precedent le plus proche jamais trouve.** Le mecanisme « le groupe remplace la personne » est publie, mesure sur 21 millions de distributions et stable sur huit architectures et deux generations. Notre espace restant est le **niveau individuel apparie** et le **plancher test retest**, qui manquent tous deux ici | citation aval de T1.10 | [CONFIRME] |
| L1.01b | idem, resultats secondaires | quelle etiquette le modele garde t il, et l'exactitude progresse t elle avec la profondeur ? | idem | idem, plus contrastes base contre instruct sur Llama-3.1-8B et Mistral-7B | accord entre le trait retenu et le trait humainement dominant, contre un plancher de permutation ; ecarts `keep rate moins human dominance` par dimension et par valeur ; plancher de bruit d'echantillonnage par **demi echantillons** de la meme cellule | **accord 53,3 a 57,9 pour cent contre un plancher de 50,4 a 52,2 : 3 a 7 points au dessus du hasard.** Sur retenu moins dominant : **race moins 9,5 points, religion moins 5,0, genre plus 12,5, revenu plus 3,0** ; race sous retenue dans les six modeles de generation precedente, moins 8,3 a moins 10,6, **sur les 15 themes y compris la vague consacree aux questions raciales, moins 11,4**. Au niveau des valeurs : **moins 19 a moins 23 points pour les repondants noirs, hispaniques, asiatiques, metis, athees et juifs, plus 16 pour les blancs, plus 4 a plus 6 pour protestants et catholiques**. Plancher de bruit humain (TV demi echantillons) 0,079 / 0,120 / 0,147 aux profondeurs 1 / 2 / 3 ; erreur GPT-4o-mini 0,212 / 0,238 / 0,269, soit 1,8 a 2,7 fois le plancher et jusqu'a 4 fois pour le plus faible. **La regle additive appliquee aux vrais traits simples atteint 0,062 de TV moyenne en profondeur 2, sous le plancher humain et au quart de l'erreur du modele** | la suppression est mesuree en espace de biais, pas en espace de decision ; les auteurs ne testent pas la lecture par log probabilites sur les huit modeles | **soutient, et localise la faute.** Deux defauts distincts et cumulatifs : la **mauvaise calibration du trait simple**, qui porte toute l'erreur d'exactitude, et **l'echec de composition**, qui est structurel et sans cout d'exactitude sous la calibration actuelle. C'est la distinction que notre plan exactitude contre diversite doit reprendre | citation aval de T1.10 | [CONFIRME] |
| L1.01c | idem, contre expertises | l'effondrement vient il du format de sortie, de l'alignement, ou de la memorisation ? | idem, plus trois paradigmes d'elicitation et deux checkpoints de base | idem | taux de victoire du meilleur trait simple sous trois lectures : repartition agregee de 1 000 repondants, **echantillonnage individuel** a temperature 1,0 sur 100 personas par cellule, et **lecture par log probabilites** sans echantillonnage ; contraste base contre instruct contre gabarit de chat | **le taux reste dans 75,3 a 83,4 pour cent dans chaque case (modele x paradigme), cinq familles.** Base contre instruct sur Llama-3.1-8B : deficit de race deja a **moins 10,8 points dans le modele de base**, deplacement par l'ajustement des poids **plus 0,6 [moins 3,5 ; plus 4,7]**, par le gabarit de chat **0,0**, contre un plan capable de detecter 5,9 points ; religion moins 5,3, deplacements moins 0,6 et moins 0,4 contre une capacite de 2,7. Mistral-7B replique : race moins 7,3, religion moins 3,6. Memorisation ecartee par quatre arguments dont la stratification en terciles d'exactitude des traits parents : **78,5 / 78,0 / 78,7 pour cent, plat** | les deux familles decomposables sont petites ; aucune affirmation n'est faite sur les modeles fermes | **soutient, et deplace la cible.** L'effondrement n'est ni un artefact d'invite, ni un effet de l'alignement, ni de la recuperation : il est **en amont du post entrainement**. Cela contredit l'hypothese repandue, chez nous comprise, que le RLHF est le coupable | citation aval de T1.10 | [CONFIRME] |
| L1.02 | Ahn (Georgia), Mao (MIT Sloan), Lee (Boston University), 29 aout 2026, « Item-Mean Surrogates : Why Richer Persona Data Fail to Improve LLMs as Human Surrogates », arXiv 2608.29455, preenregistre en fevrier 2026 | ce que le LLM predit d'une personne est il autre chose que la moyenne de l'item ? | **quatre jeux, plus de 400 000 participants et plus de 6 000 items** : Megastudy de Peng et al. (1 784 repondants, 160 items, 18 etudes retenues, 133 items et 108 160 paires en analyse POMP), SocSci210 (plus de 400 000 repondants, 5 998 resultats, 210 etudes), enquete Twin-2K-500 (2 058 repondants, 126 items), ANES (4 270 repondants, 11 variables) | GPT-4.1 et variantes, plus un GPT-4.1 ajuste et Socrates-Qwen2.5-14B | **`R^2` demeane** : correlation au carre entre l'ecart humain a la moyenne de l'item et l'ecart LLM a la meme moyenne ; **decomposition de theorie de la generalisabilite** de l'erreur de prediction ; **baseline `leave-one-out` de moyenne d'item** ; permutation de personas | **`R^2` demeane 3,05 pour cent contre un plafond test retest de 53,6, soit 5,7 pour cent du plafond** ; meilleure invite non ajustee 4,44 pour cent. **Le LLM perd contre la moyenne des autres repondants : `r` moyen 0,34 contre 0,45, `dz = -0,55`, `p` de l'ordre de `4,6e-95`, sur 1 631 repondants.** Decomposition : effet principal de personne **4,9 pour cent**, effet d'item 8,7, residu 86,4, dont **interaction personne x item stable 44,0 pour cent et erreur transitoire 42,4** ; l'interaction vaut **8,9 fois** l'effet principal de personne. Ajustement fin : GPT-4.1 tombe a 2,31 ; Socrates 7,57 sur les etudes vues et **0,73 sur les etudes tenues a l'ecart**. ANES 10,77. Permutation : correct 3,05 contre un maximum de 0,028 sur 10 000 permutations. Ecarts types medians a **65 pour cent (Megastudy), 50 (SocSci210), 57 (enquete)** de l'humain ; categories effectivement utilisees 43 a 73 pour cent ; **la forme pese 31,4 a 59,4 pour cent de la distance de Wasserstein 2 au carre** | le plafond de 53,6 pour cent vient de Twin-2K-500 et sert de reference descriptive commune aux quatre jeux, ce que les auteurs signalent ; l'ANES est a quatre items | **soutient tres fortement, et prend une partie de notre place.** Le mot du papier, « item-mean surrogacy », dit la meme chose que « la personne remplacee par son groupe » avec un groupe plus grand encore : la population entiere. Il publie exactitude, dispersion, forme, plancher humain et plancher trivial dans le meme tableau. **Ce qu'il ne fait pas : aucune segmentation demographique, donc aucun terme inter groupes** | citation amont de T1.12, citation aval de T1.16 | [CONFIRME] |
| L1.03 | Xie, Li, Lu, Xiao, Shi, Huang, Wang, « Evaluating the statistical realism of LLM-generated social science data », **PNAS 123, e2538145123 (2026)**, DOI 10.1073/pnas.2538145123 | les donnees generees reproduisent elles les moments statistiques d'une population reelle ? | **sept enquetes** : NLSY, CFPS, Add Health, Understanding Society (longitudinales), recensement des Etats Unis, CPS-ASEC, GSS (transversales) ; 1 000 cas tires par jeu ; six domaines | **15 LLM**, de GPT-3.5-Turbo a GPT-5, plus Qwen et DeepSeek-V3 ; conditionnement sur les variables demographiques reelles de la personne | **taux de reussite** : part des iterations de bootstrap ou le test ne distingue pas la statistique simulee de la reelle a 0,05, sur cinq familles de motifs (distributions univariees, associations bivariees, prediction multivariee, distributions de sequences d'evenements de vie, associations de ces sequences) | **taux de reussite generalement sous 0,5** ; les types 1 et 4 sont les plus bas, **le type 4 (sequences de vie) est proche de zero**. **Tous les modeles produisent une entropie systematiquement inferieure a celle du reel**, sur les variables categorielles comme sur les sequences. Cramer's V simules gonfles, avec **une grappe de paires au dessus de 0,6 et certaines approchant 0,8 voire 1**. Sur le NLSY avec Gemini-2.5-Flash, le `R^2` d'une regression du log du revenu moyen de 30 a 40 ans sur race, genre et diplome **approche 0,6 en simule contre moins de 0,1 en reel**. **Aucune amelioration de generation en generation, de GPT-3.5-Turbo a GPT-5** ; **aucune relation coherente avec la temperature** ; un ajustement de domaine sur 1 000 enregistrements CPS-ASEC de 1970 ameliore le realisme | conditionnement volontairement pauvre, « sparse conditioning », que les auteurs presentent comme la limite du cadre ; aucun niveau individuel apparie | **soutient, et donne le chiffre le plus citable du corpus pour l'essentialisme.** Un facteur six sur la part de variance du revenu expliquee par trois etiquettes, dans PNAS, avec 15 modeles et 7 enquetes. C'est le pendant du facteur quarante sur l'eta carre de Chen et al. (T1.32), sur un autre outcome et une autre revue | citation amont de L1.02 | [CONFIRME] |
| L1.04 | Cheng, Piccardi, Yang, EMNLP 2023, « CoMPosT : Characterizing and Evaluating Caricature in LLM Simulations », arXiv 2310.11501 | comment mesurer la caricature dans une simulation en texte libre ? | 15 personas (5 origines, 3 genres, 3 ideologies, 3 ages, plus « person »), 30 paires de themes tirees des questions les plus clivantes d'OpinionQA, trois contextes (forum, entretien, Twitter) | GPT-4 principalement, plus des modeles anterieurs | **caricature = individuation x exageration** ; individuation : exactitude d'un classifieur (foret aleatoire sur plongements SBERT) qui separe la simulation de la simulation a persona par defaut ; exageration : cosinus normalise de la sortie a un **axe semantique persona contre theme** construit par la methode Fightin' Words | **toutes les personas sont individuables** : score moyen superieur a 0,5 partout, **superieur a 0,95 pour chacune en contexte d'entretien**. Exageration maximale pour **non binaire, noir, hispanique, moyen oriental et conservateur** ; **minimale pour asiatique et femme**, que les auteurs lisent comme des defauts implicites du modele. Les themes generaux et non controverses caricaturent plus que les themes specifiques et controverses, et la caricature decroit continument quand la specificite du theme augmente | aucune verite terrain humaine ; mesure purement textuelle, non transposable a un questionnaire ferme ; les auteurs reconnaissent qu'un texte peut etre stereotype sans etre caricatural a leur sens, exemple donne des reponses « femme » sur le menage | **soutient le vocabulaire, et pose le piege.** C'est la source du mot « caricature » que L1.01 conteste. La contradiction n'est pas sur les faits, elle est sur le format de sortie : voir « Ce qui se contredit » | citation amont de L1.01 | [CONFIRME] |
| L1.05 | Hwang, Majumder, Tandon, Findings of EMNLP 2023, « Aligning Language Models to User Opinions », arXiv 2305.14929 | l'opinion d'une personne et ses etiquettes se predisent elles l'une l'autre ? | American Trends Panel de Pew, 15 themes, 100 utilisateurs par theme ; 8 variables demographiques, l'ideologie, et les opinions passees du meme utilisateur | text-davinci-003, zero shot | **kappa de Cohen entre paires d'utilisateurs partageant les memes demographies** ; part des paires a opinions proches qui ont des ideologies differentes ; exactitude de QA en correspondance exacte et en correspondance regroupee | **entre deux personnes de memes demographies, l'accord sur les opinions implicites tourne autour de 0,4 a 0,5 de kappa.** Parmi les paires qui partagent une opinion, **60 a 83 pour cent ont des ideologies differentes** selon le theme (81 sur les armes, 82 sur l'automatisation, 83 sur la vie privee, 70 sur la race). Exactitude : sans persona 0,43 / 0,62 ; **demographies plus ideologie 0,47 / 0,65** ; **les 8 opinions passees les plus pertinentes seules 0,52 / 0,68** ; tout combine 0,54 / 0,70 | modele de 2022, 100 utilisateurs par theme, une seule enquete ; les « opinions passees » viennent de la meme enquete, donc fuite partielle | **soutient, et c'est l'anteriorite conceptuelle la plus ancienne trouvee.** Publie en 2023 : « the opinions of a user and their demographics and ideologies are not mutual predictors ». **Huit reponses propres a la personne valent 5 points de plus que toutes ses etiquettes reunies.** La litterature de 2026 mesure cela sous d'autres noms sans jamais citer ce resultat comme sa source | citation amont de L1.01 | [CONFIRME] |
| L1.06 | anonyme (huit modeles ouverts), 27 juillet 2026, « Can Large Language Models Represent Urban Publics ? », arXiv 2607.27100 | un accord sur un contraste agrege survit il a la descente en sous groupes ? | experience d'enquete sur le logement abordable aux Etats Unis, **843 repondants humains**, 27 cellules parti x statut d'occupation x item, deux ordres de questions randomises, 720 sessions par modele | Qwen 2.5 14B et 7B, Phi-4 14B, Gemma 3 12B, Gemma 2 9B, Llama 3.1 8B, OLMo 2 7B, Mistral 7B | contraste proprietaire contre locataire de l'effet de proximite, avec **critere d'equivalence prespecifie a plus ou moins 0,20** ; puis TV, Jensen Shannon, Wasserstein ordinal, RMSE, correlation de cellule, **rapport median de variance modele sur humain**, ecart d'entropie ; **et un plancher humain humain obtenu en comparant deux echantillons humains apparies** | humains `theta = -0,285` [-0,385 ; -0,179] ; **seul Qwen 2.5 14B passe l'equivalence, -0,242**, mais son effet global est -0,644 contre -0,465. Au niveau des sous groupes il **attenue les republicains (-0,044 contre -0,335) et exagere les independants (-0,500 contre -0,326)**, deux erreurs qui s'annulent dans la moyenne. RMSE 0,613 sur 27 cellules. **Rapport median de variance 0,099 pour Qwen ; 0,000 pour Phi-4, Gemma 3 et OLMo 2, ce qui signifie aucune variance de reponse dans au moins la moitie des cellules.** Entropie inferieure a l'humaine pour les huit modeles, ecart -0,362 a -0,728. **Plancher humain humain : TV 0,098 contre 0,561 pour Qwen ; JS 0,009 contre 0,249 ; Wasserstein ordinal 0,147 contre 0,721, et les 18 cellules depassent leur plancher.** L'ordre des questions deplace `theta` de +0,367 chez Qwen contre +0,036 non significatif chez les humains | un seul domaine, huit modeles ouverts seulement, pas de modele proprietaire ; effectifs de cellule modestes | **soutient, et fournit le plancher humain de dispersion que le corpus n'avait pas.** C'est **la seule entree du corpus qui publie une distance humain humain a cote d'une distance humain modele sur les memes cellules**. Le rapport median de variance a 0,000 est le chiffre le plus dur du champ | citation aval de T1.10 | [CONFIRME] |
| L1.07 | anonyme, 3 aout 2026, « Emulate or Estimate ? The Divergent Strengths of Base and Post-Trained Language Models for Opinion Simulation », arXiv 2608.03044 | l'ecart inter groupes est il ecrase ou exagere, et de quoi cela depend il ? | 59 items a quatre options de la vague 54 du Pew American Trends Panel ; sept conditions dont une marginale non conditionnee et six groupes (democrate, republicain, tres liberal, tres conservateur, haut revenu, protestant) | **trois paires base et post entrainee appariees** : Qwen3-14B, Olmo-3-7B, Olmo-3-32B ; plus Claude Opus 4.6 en reference d'estimation | TV et Wasserstein contre la verite humaine, dans deux paradigmes : **emulation** (le modele genere des reponses qui s'agregent) et **estimation** (le modele donne directement la distribution) ; **correlation de Spearman entre les distances TV par paires de groupes chez le modele et chez l'humain**, et **rapport moyen des ecarts inter groupes** | emulation : les bases battent leurs versions post entrainees dans **les sept conditions et les six modeles** (Qwen3-14B 0,263 contre 0,458 en TV ; Olmo-3-7B 0,248 contre 0,372 ; Olmo-3-32B 0,274 contre 0,427). **Structure demographique : les bases suivent la structure humaine, `rho` 0,607 a 0,754, tous `p < 0,02`, en compressant les ecarts inter groupes a environ 70 pour cent (0,664 a 0,704) ; les post entrainees suivent moins bien, `rho` 0,350 a 0,593, et exagerent les ecarts d'environ 2 fois (2,014 a 2,242).** Sorties post entrainees 8,0 a 14,0 fois plus semblables au niveau des bigrammes. En estimation, les post entrainees gagnent et Claude Opus 4.6 domine (TV 0,142) | 59 items, un seul theme economique, six groupes ; les paires ne couvrent que deux familles | **soutient, et donne LA variable explicative du desaccord inter groupes du champ.** Compression a 0,70 chez les bases, gonflement a 2,0 chez les alignees, sur les memes items et les memes groupes. Notre resultat « l'etiquette aggrave » est donc **conditionne au post entrainement**, ce que notre comparaison base contre aligne (option C de l'arbitrage) peut trancher | citation aval de T1.13 | [CONFIRME] |
| L1.08 | anonyme, ICLR 2026, « SimBench », arXiv 2510.17516 | quelle est la fidelite de simulation, mesuree une fois pour toutes, et que fait l'alignement ? | **20 jeux harmonises**, d'OpinionQA et Afrobarometer a MoralMachine, Choices13k, Jester et des echelles de machiavelisme et de croyances conspirationnistes ; deux volets, population generale et groupes | **45 modeles**, dont 13 paires base et instruct appariees, plus les modeles Centaur | score `S` de 0 a 100 : reduction de la TV a la verite humaine par rapport a une baseline uniforme, moyennee ; puis `delta S` entre condition groupee et non groupee | meilleur modele **Claude-3.7-Sonnet 40,80 sur 100**, DeepSeek-R1 34,52, Qwen2.5-32B base 12,27 ; **dix modeles sur 45 sont sous 0**, donc plus loin de l'humain que l'uniforme. Le calcul a l'inference n'apporte rien (o4-mini 27,77 vers 28,99 ; Claude 40,80 vers 39,46 ; GPT-4.1 34,55 vers 33,11). **Arbitrage alignement simulation : la difference instruct moins base contre l'entropie de la reponse humaine donne `r = -0,942`, jusqu'a plus 40 points de gain en consensus et un passage sous zero vers une entropie de 0,8** ; mediation causale, effet direct **plus 6,46**, effet indirect par la baisse d'entropie **moins 1,74**. **Conditionner sur un groupe degrade tous les modeles : `delta S` de -1,27 a -4,61 ; par dimension, religiosite -9,91 plus ou moins 1,59, affiliation politique -4,97, religion -4,83, revenu -4,51** | le score reste relatif a l'uniforme, donc dependant de l'entropie des jeux ; agrege 20 jeux tres heterogenes | **soutient sur deux points.** L'arbitrage alignement simulation est mesure avec une mediation, ce qui explique les resultats opposes de T1.09 et T1.04. Et **l'etiquette demographique degrade la simulation dans les cinq modeles testes, le plus fortement sur la religion et la politique**, exactement les deux dimensions que L1.01 montre supprimees | citation aval de T1.10 | [CONFIRME] |
| L1.09 | anonyme, 20 juillet 2026, « More Is Not More : What Matters for Diversity in LLM Opinions ? », arXiv 2607.20429 | qu'est ce qui, dans une persona, produit reellement de la diversite ? | 100 questions ouvertes d'utilisateurs reels ; plan factoriel **5 profondeurs de persona x 3 architectures** plus quatre astuces a bas cout | 7 modeles | dispersion intra condition (`alpha`, distance moyenne par paires sur plongements) et complementarite inter conditions (`beta`, taux de categories d'opinion non couvertes) | **la premiere marche de la persona capte l'essentiel du gain ; ajouter environ 60 mots de detail demographique apporte en moyenne plus 0,004 de MPD.** Une description de role d'une phrase vaut **2,5 fois** le meilleur des trucs a bas cout. Temperature et consignes de diversite : effets negligeables. **La largeur du vivier bat la profondeur** : passer de 5 a 20 personas donne peu en `alpha` mais entre quatre groupes tires au hasard le taux de categories non partagees atteint 59 a 82 pour cent. Deux architectures differentes couvrent des regions d'opinion largement disjointes, taux moyen de non recouvrement 79 pour cent contre un plancher de partition aleatoire a 29 | texte libre, pas de verite terrain d'enquete ; la diversite mesuree est semantique, pas distributionnelle | **soutient, et corrige une intuition du projet.** Ce qui cree de la diversite n'est pas le contenu de l'etiquette, c'est **le fait qu'il y ait une etiquette differente d'un appel a l'autre**. Corollaire direct : notre condition sans etiquette n'est pas une condition « sans persona », c'est une condition sans differenciation, et la comparaison doit en tenir compte | citation aval de T1.10 | [CONFIRME] |
| L1.10 | anonyme, 20 mars 2026, « Characterizing the ability of LLMs to recapitulate Americans' distributional responses to public opinion polling questions », arXiv 2603.20229 | vaut il mieux interroger mille personas ou demander la distribution une fois ? | Cooperative Election Study 2022, environ 60 000 adultes, **84 questions** de politique publique, 1 680 combinaisons question x demographie | GPT-4o-mini, quatre gabarits d'invite, 20 repetitions | difference de moyenne, **difference d'ecart type**, et distance de Wasserstein normalisee, entre la distribution humaine et la distribution predite, pour chaque combinaison | **le cadre « distribution directe » bat le cadre « individu unique » sur 1 299 des 1 680 distributions (77,3 pour cent), avec un Wasserstein inferieur de 0,107 en moyenne [0,100 ; 0,113]**, et une moyenne plus juste dans 1 222 sur 1 680 (72,7 pour cent), de 10,4 points de l'etendue de reponse. **Sur les ecarts types, la voie distributionnelle reproduit la dispersion humaine tandis que la voie individuelle surestime systematiquement l'homogeneite.** La performance de la voie distributionnelle varie de facon predictible selon la demographie et la question, ce qui permet d'anticiper l'erreur avant l'appel | un seul modele, un seul jeu ; les non binaires sont ecartes, 0,73 pour cent de l'echantillon | **soutient, et boucle une serie de quatre.** Sun (T1.11), Ozkan (T1.33), Meister (T1.15) et ce papier arrivent au meme endroit par quatre chemins. Et celui ci **attribue l'ecrasement a la voie d'interrogation individuelle, pas au modele** : le meme GPT-4o-mini reproduit la dispersion quand on lui demande la distribution | citation aval de T1.13 | [CONFIRME] |
| L1.11 | Entropy 27(9) 923, 2025, « Simulating Public Opinion : Comparing Distributional and Individual-Level Predictions from LLMs and Random Forests », DOI 10.3390/e27090923, CC BY | l'ecrasement est il propre au modele de langage ou propre a la prediction ? | ANES 2020, echantillon pre electoral ; **25 variables de fond reparties en trois groupes, demographique (D), attitudinal et politique (A), valeurs morales et sociales (M)** ; 10 themes d'opinion ; validation croisee 3 blocs, bootstrap 1 000 | Gemma3 12B et Qwen2.5 14B en zero shot ; **foret aleatoire supervisee sur les memes variables**, plus baselines aleatoire et constante | F1 et Cramer's V au niveau individuel, distance de Jensen Shannon au niveau distributionnel, **les deux modeles evalues sur exactement les memes blocs de validation** | contre les baselines naives, le LLM domine partout (climat : F1 0,59 contre 0,36 aleatoire et 0,41 constante ; JSD 0,21 contre 0,29 et 0,51 ; Cramer's V 0,41 contre 0,04). **Face a la foret aleatoire, chacun a son terrain : le LLM a un JSD significativement meilleur sur 6 themes sur 10** (toxicomanie plus 0,18, roles de genre plus 0,18, assurance sante plus 0,12) ; **la foret a un F1 egal ou meilleur sur la plupart des themes**, jusqu'a 0,08 de plus sur la regulation des armes, et un Cramer's V nettement superieur sur les armes (0,19) et la diversite raciale (0,17). **Les meilleurs blocs de variables du LLM sont A ou M ou A+M, presque jamais D seul** | 10 themes, deux modeles ouverts moyens ; l'ANES 2020 est probablement dans les corpus | **soutient, et repond directement au point 2 de « Ce que personne n'a fait ».** L'ecrasement n'est pas uniformement une propriete de la prediction : **le LLM tient mieux la distribution, la foret tient mieux l'individu et l'association.** C'est l'inverse exact de la lecture de Ku et al. (T1.31) et cela merite d'etre pose cote a cote | citation aval de L1.04 | [CONFIRME] |
| L1.12 | Chang et al. (dépôt `schang-lab/gems`), 2 novembre 2025, « Graph-Based Alternatives to LLMs for Human Simulation » (GEMS), arXiv 2511.02135 | un LLM est il necessaire pour predire une reponse fermee ? | **OpinionQA** (76 000 individus, 500 questions), **Twin-2K** (2 000 individus, batterie de 150 items), **Dunning-Kruger** (3 000 individus, 20 questions) ; trois regimes : imputation, individus inedits, questions inedites | reseau de neurones sur graphe heterogene individus x choix (RGCN, GAT, SAGE) contre LLaMA-2-7B, Mistral-7B, Qwen3-8B en zero shot, few shot, chaine de pensee agentique, SFT et few shot ajuste | exactitude en correspondance exacte, moyennee sur trois partitions, **avec le plafond test retest humain de Twin-2K a 81,72 pour cent affiche dans la table** | imputation : **GEMS (SAGE) 57,00 sur OpinionQA, 66,62 sur Twin-2K, 57,89 sur Dunning-Kruger**, contre le meilleur LLM (ajustement plus 8 exemples) a 56,76 / 66,36 / 57,21 et le hasard a 27,87 / 35,05 / 20,00. Individus inedits : GEMS 50,73 / 62,50 / 57,07 contre SFT 50,56 / 61,85 / 56,66. **Le tout avec environ mille fois moins de parametres et jusqu'a cent fois plus vite**, et sans utiliser le texte des questions | le regime d'imputation donne au graphe 40 pour cent des reponses de la personne cible, ce qui n'est pas comparable a un conditionnement par etiquettes seules ; le gain sur individus inedits est faible | **soutient une menace deja connue, avec un troisieme instrument.** Apres la regression logistique de Chen (T1.32) et la foret aleatoire de Ku (T1.31), un GNN. **Sur Twin-2K, la meilleure exactitude publiee, 66,62, laisse encore 15 points jusqu'au plafond humain de 81,72.** Toute exactitude individuelle publiee sans baseline structurelle est desormais indefendable | citation aval de T1.13 | [CONFIRME] |
| L1.13 | anonyme, 28 juillet 2026, « Correcting Mode Collapse in Silicon Sampling with Semantic Similarity Rating », arXiv 2607.28550 | l'ecrasement de variance vient il de l'incapacite du modele a produire des nombres ? | ANES 2016 en apprentissage et **ANES 2020 en test, 6 630 personas apres le nettoyage de Bisbee et al.** ; thermometres de sentiment sur quatre cibles | Claude Sonnet 5, DeepSeek V4 Flash, GPT-5.4 Mini | divergence KL entre distribution reelle et synthetique, et comparaison des ecarts types cellule par cellule ; **une seule temperature globale `T` apprise** | **KL en sortie numerique brute : 0,61 (DeepSeek), 1,34 (GPT), 1,97 (Claude). Avec la notation par similarite semantique du texte : 0,13 / 0,11 / 0,07 en 2016, et 0,11 / 0,07 / 0,08 en 2020 avec le parametre appris sur 2016.** Le parametre vaut `T = 0,2`, donc faible, et la KL croit de facon monotone quand `T` augmente : la methode n'aplatit pas vers l'uniforme. **En revanche le biais de position n'est pas corrige** : les democrates synthetiques notent toujours les conservateurs plus bas que les democrates reels | domaine restreint aux echelles thermometriques ; trois modeles ; le parametre est ajuste sur de la donnee reelle, donc la methode n'est pas gratuite | **soutient une distinction que le projet doit faire.** L'ecrasement de dispersion et le biais de groupe sont **deux defauts separables** : le premier tombe d'un facteur cinq a vingt avec un seul parametre, le second ne bouge pas. Notre chaine de scoring par lettre unique est exactement la « sortie numerique brute » que ce papier accuse | citation aval de T1.13 | [CONFIRME] |
| L1.14 | anonyme, 24 avril 2026, v3 du 2 septembre 2026, « Statistical realism is not evidence that LLMs can estimate treatment effects in social science experiments », arXiv 2604.02458 | un echantillon synthetique realiste donne t il de bons effets de traitement ? | experience transnationale, **59 508 participants, 62 pays, 11 interventions** ; deux replications supplementaires sur 12 et 27 pays, 20 785 participants | trois LLM | mesure conjointe, sur les memes reponses simulees, du **realisme statistique** (MAE sur les distributions de reponse) et de **l'exactitude d'effet de traitement** (erreur d'ATE) | **correlation de Spearman entre realisme et exactitude d'effet : `rho = 0,10`.** Quand on s'en sert pour choisir un modele, la relation s'inverse : **`rho = -0,52`, `p = 0,027`, IC 95 pour cent [-0,79 ; -0,07]** : optimiser le realisme degrade l'effet. La divergence est plus grande pour les resultats comportementaux, ou les modeles semblent extrapoler le comportement a partir de motifs attitudinaux ; dans les donnees humaines croyance et action sont faiblement liees (`r = 0,12` sur les reponses, `-0,15` sur les ATE) et les modeles resserrent ce lien | un seul domaine experimental, trois modeles ; le realisme est mesure par une MAE de distribution, pas par une mesure de structure | **contredit et clarifie.** Le champ traite implicitement realisme et validite causale comme un seul objet. Ils ne correlent pas. **Cela s'applique a nous : notre C2ST, notre ratio de dispersion et notre exactitude individuelle sont trois cibles distinctes, et bien faire sur l'une ne certifie rien sur les autres** | citation aval de T1.17 | [CONFIRME] |
| L1.15 | anonyme, 2 septembre 2026, « When Persona Attributes Improve Population Alignment in Large Language Models », arXiv 2609.02526 | quand une etiquette aide t elle, et laquelle choisir ? | **quatre enquetes sociales generales, deux pays**, 20 taches de prediction par enquete | 6 LLM (familles Llama et Qwen, 3B a 70B) | alignement entre distribution predite et distribution humaine, croise avec la **variation de reponse humaine** de la question cible, mesuree par entropie normalisee (nominal) ou dissension (ordinal) ; cinq methodes de selection d'attributs, dont deux statistiques et deux par LLM | **la persona aide davantage sur les questions a forte variation de reponse humaine, et pour la condition sans persona la relation s'inverse : le modele est meilleur sur les questions a faible variation.** Selection d'attributs : **les methodes statistiques (correlation, importance de variable) battent les selections faites par le LLM lui meme**, qui sont en outre instables ; le plus gros Llama ne reselectionne le meme attribut principal que dans environ 60 pour cent des tirages | pas de niveau individuel ; l'alignement est distributionnel | **soutient, et donne le moderateur.** La variation de reponse humaine est la variable qui reconcilie les resultats contradictoires du champ sur la persona. Et **le modele ne sait pas choisir ses propres etiquettes** : c'est une preuve supplementaire, par une autre voie, du « choix quasi aveugle » de L1.01 | citation aval de T1.10 | [CONFIRME] |
| L1.16 | tutoriel Evans, Leckie, Merlo, Subramanian, SSM Population Health 27, 101664 (2024), CC BY-NC-ND ; cadre pose par Merlo, Social Science & Medicine 203, 74 a 80 (2018) et Evans, Williams, Onnela, Subramanian, ibid. 203, 64 a 73 (2018) | **combien de la variation individuelle se trouve entre les strates identitaires ?** | epidemiologie sociale ; illustration sur 33 000 individus et **384 strates** (2 genres x 3 origines x 4 diplomes x 4 revenus x 4 ages) | modeles multiniveaux lineaires et logistiques, effets aleatoires de strate | **VPC**, part de la variance individuelle totale qui est entre strates ; **PCV**, part de la variance inter strates expliquee par les effets principaux additifs ; **AUC comme mesure de la `discriminatory accuracy` de la strate** | **VPC 9,4 pour cent en lineaire et 10,7 en logistique dans l'illustration, presente comme « a relatively large amount of clustering ».** Reference du domaine citee par les auteurs : « most studies using multilevel models to examine individuals nested in neighborhoods, schools, or workplaces will often see VPCs less than 5%, and they rarely exceed 10% ». Formulation exacte du sens : « Hypothetically, if the VPC were 100%, then knowing the stratum average would tell us the [outcome] of every individual in the stratum » | domaine sante, outcome continu ou binaire, pas une opinion ; l'illustration est sur donnees simulees | **soutient le cadrage, et fournit l'ancrage non informatique qui manquait.** La litterature qui mesure depuis vingt ans « ce que l'etiquette permet de deviner d'une personne » a un nom, une metrique et un ordre de grandeur : **moins de 10 pour cent**. Une simulation qui remplace la personne par sa strate se comporte comme si le VPC valait 100. C'est la formulation la plus economique de la these du projet, et elle est citable hors informatique | citation amont de L1.01 | [CONFIRME] |
| L1.17 | Liu, Diab, Fried, Findings of ACL 2024, « Evaluating Large Language Model Biases in Persona-Steered Generation », arXiv 2405.20253 | une persona incongrue est elle plus dure a tenir ? | personas a plusieurs traits dont un rend les autres moins probables dans les donnees d'enquete humaines ; generation en texte libre | plusieurs LLM, dont des versions RLHF | steerabilite vers la position cible, diversite des vues exprimees | **les modeles sont 9,7 pour cent moins steerables vers les personas incongrues que congrues**, et produisent parfois la position stereotypee de la demographie plutot que la position demandee. **Les modeles RLHF sont plus steerables, en particulier vers les positions associees aux liberaux et aux femmes, mais presentent des vues significativement moins diverses.** La variance de steerabilite n'est pas predictible depuis une evaluation a choix multiples | texte libre ; pas de verite terrain d'enquete appariee | **soutient, et contredit L1.01 sur un point precis.** Ici la persona contre stereotypique coute 9,7 points ; L1.01, apres correction du bruit de la verite terrain, ne trouve aucune penalite contre stereotypique. Voir « Ce qui se contredit » | citation amont de L1.01 | [PROBABLE] |
| L1.18 | Orlikowski et al., 2025, « Beyond Demographics : Fine-tuning Large Language Models to Predict Individuals' Subjective Text Perceptions », arXiv 2502.20897 | un modele entraine apprend il le lien etiquette vers opinion, ou la personne ? | cinq taches d'annotation subjective avec sociodemographies standardisees | LLM ajustes | exactitude d'annotation sous invite sociodemographique, avant et apres ajustement, avec decomposition entre apprentissage du comportement propre a l'annotateur et apprentissage de motifs sociodemographiques | l'ajustement ameliore bien l'invite sociodemographique, **mais le gain vient essentiellement de l'apprentissage du comportement propre a l'annotateur, pas de motifs sociodemographiques** ; conclusion des auteurs : « models learn little meaningful connection between sociodemographics and annotation » | annotation de texte, pas enquete d'opinion ; taille des jeux non lue | **soutient tres directement.** Meme conclusion que Hwang (L1.05) onze ans de modeles plus tard, obtenue par ajustement plutot que par invite : **l'information qui predit est celle de la personne, pas celle du groupe** | citation aval de L1.04 | [PROBABLE] |
| L1.19 | anonyme, 19 avril 2026, « LLM Agents Predict Social Media Reactions but Do Not Outperform Text Classifiers », arXiv 2604.19787 | un agent a persona bat il un classifieur de texte ordinaire ? | **1 511 participants serbes, plus de 120 000 combinaisons agent x persona** | 27 LLM | exactitude globale ; puis choix force binaire avec **coefficient de correlation de Matthews**, corrige du hasard | agents 70,7 pour cent d'exactitude globale, avec **13 points d'ecart entre modeles** ; en choix force, **MCC des agents 0,29 contre 0,36 pour un classifieur supervise TF-IDF** | reactions de reseau social, pas reponses d'enquete ; un seul pays | **contredit un usage.** Quatrieme baseline non LLM qui tient ou bat les agents, apres regression logistique, foret aleatoire et GNN. La liste devient un argument a elle seule | citation aval de L1.04 | [PROBABLE] |
| L1.20 | anonyme, v3 du 2 janvier 2025 revise 2026, « How Robust Is Homogeneity Bias in LLMs ? », arXiv 2501.02211 | l'homogeneisation des groupes marginalises est elle stable ? | portraits generes en texte libre ; **grille 5 x 5 de temperature et `top-p`** ; deux facons de signaler l'identite, etiquette explicite et nom typé | **sept modeles ouverts instruits, 7 a 20 milliards de parametres** | similarite interne des portraits d'un groupe, comparee entre groupes | **dans six modeles sur sept, les Hispaniques et les Asiatiques americains sont depeints comme significativement plus homogenes que les blancs, a la configuration par defaut, et l'effet reste positif en moyenne a toutes les temperatures et tous les `top-p` testes.** Les signaux afro americain et de genre varient de direction selon le modele | texte libre uniquement ; pas de verite terrain humaine | **soutient la partie « caricature » et contredit L1.01.** Une homogeneisation intra groupe robuste sur 25 configurations de decodage et sept modeles, la ou L1.01 mesure l'inverse. Format de sortie, encore | citation aval de L1.04 | [PROBABLE] |
| L1.21 | Sen, Lutz, Rogers, Garcia, Strohmaier, 2 novembre 2025, « Missing the Margins : A Systematic Literature Review on the Demographic Representativeness of LLMs », arXiv 2511.01864 | que vaut la litterature qui conclut a la representativite ? | **211 articles** codes | aucun | part des articles concluant positivement qui evaluent effectivement plusieurs categories demographiques et des sous categories | **29 pour cent des etudes concluent positivement ; parmi elles, 30 pour cent n'evaluent pas plusieurs categories ou sous categories ; 35 et 47 pour cent ne precisent meme pas les sous categories pour le genre et pour la race ; moins de la moitie de celles qui les precisent incluent des groupes marginalises ; plus d'un tiers ne definissent pas la population cible** | revue, sans mesure propre | **soutient le cadrage, et donne le chiffre de contexte.** Le champ surestime sa propre representativite, et l'erreur se concentre exactement la ou notre these porte, sur les sous categories et les marges | citation aval de T1.13 | [PROBABLE] |
| L1.22 | anonyme, 6 avril 2026, « Restoring Heterogeneity in LLM-based Social Simulation : An Audience Segmentation Approach », arXiv 2604.06663 | une segmentation plus fine restaure t elle l'heterogeneite ? | enquete d'opinion climatique aux Etats Unis ; six configurations de segmentation, trois logiques de selection d'identifiants (theorique, guidee par les donnees, par l'instrument) | Llama 3.1-70B et Mixtral 8x22B | cadre a trois dimensions : fidelite **distributionnelle**, **structurelle** et **predictive** | **la granularite ne produit pas d'amelioration coherente** : un enrichissement modere peut aider, une extension supplementaire n'aide pas de facon fiable et peut degrader la fidelite structurelle et predictive. Les configurations compactes egalent ou battent souvent les completes. **La logique de selection determine quelle dimension progresse** : par l'instrument pour la forme distributionnelle, par les donnees pour la structure inter groupes. **Aucune configuration ne domine sur les trois dimensions, et un gain sur une dimension peut coincider avec une perte sur une autre** | un seul domaine, deux modeles ouverts | **soutient, et confirme l'antagonisme.** Troisieme papier apres Kolluri (T1.21) et Krsteski (T1.24) a montrer que les dimensions de fidelite se contrarient, ici sur trois axes explicitement nommes | citation aval de T1.10 | [PROBABLE] |
| L1.23 | anonyme, 28 juin 2026, « Beyond the Mean : Three-Axis Fidelity for Aligning LLM-Based Survey Simulators from Small Pilot Data », arXiv 2606.28963 | un petit echantillon pilote suffit il a recuperer la population ? | enquete sur la desinformation COVID-19 | trois familles d'approches : invite, rectification, ajustement fin | decomposition en fidelite **structurelle**, **marginale** et **individuelle** | **l'ajustement fin sur un petit echantillon pilote offre l'equilibre le plus favorable sur les trois axes, mais les niveaux atteints varient selon les sous echantillons, ce qui menace l'alignement pluraliste** ; constat de depart : marges biaisees, variance mal calibree, relations predicteur vers resultat **attenuees** | un seul domaine ; pas de plancher humain | **soutient, avec une nuance rare.** « predictor-outcome relationships are attenuated » va dans le sens **inverse** du gonflement inter groupes de Chen (T1.32) et de Xie (L1.03). La direction depend donc du regime, ce que la section « Ce qui se contredit » explicite | citation aval de T1.10 | [PROBABLE] |
| L1.24 | anonyme, 28 aout 2026, « Benchmarking large language model agent societies against human behavioural distributions » (SILICA), arXiv 2608.28182 | une societe d'agents reproduit elle une distribution comportementale humaine ? | cinq environnements avec ancrages humains publies, plus des perturbations qui laissent les regles inchangees et des variantes dont les gains pointent a l'oppose du resultat memorise | **douze modeles a poids ouverts**, sur une seule carte graphique grand public | equivalence a l'ancrage humain, sensibilite aux perturbations de presentation, et test de memorisation par inversion des gains | **l'accord avec les donnees humaines se limite aux points de depart** : la contribution du premier tour dans le bien public tombe dans la marge d'equivalence pour huit modeles sur onze, **aucun ne reproduit l'etat final ni le couloir humain de cooperation**. **Inverser l'ordre de deux actions coute 58 points de cooperation a un modele.** Un seul modele, le seul entraine au raisonnement, place son seuil d'acceptation la ou l'incitation l'exige ; deux le deplacent partiellement, deux dans le mauvais sens, trois n'en acquierent jamais | jeux economiques, pas enquete d'opinion ; modeles ouverts uniquement | **soutient une dette de methode.** La sensibilite a la presentation (58 points sur un simple echange d'ordre) est du meme ordre que le facteur 3,6 de Cummins (T1.20) et que le decalage d'ordre de +0,367 de L1.06. **Trois papiers independants : sans courbe de specification, un chiffre de simulation n'est pas un chiffre** | citation aval de T1.10 | [PROBABLE] |
| L1.25 | anonyme, 26 juillet 2026, « Human diversity fuels collective creativity that large language models cannot simulate or sustain », arXiv 2607.26899 | une population simulee peut elle remplacer la diversite d'une population reelle ? | experience preenregistree de metaphores creatives, redacteurs anglophones natifs (L1) et non natifs (L2), trois conditions (sans IA, ideation par IA, raffinement par IA) ; puis simulation du vivier complet par personas construites sur les vrais parcours des participants | trois familles de modeles, invite en langue maternelle, temperatures elevees | diversite collective du vivier d'idees | **tout vivier simule tombe sous tout vivier humain** ; pousser les modeles plus loin ne cree de la diversite qu'au prix de texte degenere. L'ideation par IA comprime la diversite collective pour tous et **efface l'avantage des redacteurs L2**, alors que le raffinement par IA le preserve | domaine creatif, pas opinion ; personas construites, pas jumeaux valides | **soutient, sur un troisieme terrain.** Apres les attitudes (T1.34) et les gouts (T1.29), la creativite. Et le detail interessant pour nous : **c'est l'avantage du groupe minoritaire qui disparait en premier** | citation aval de T1.10 | [PROBABLE] |
| L1.26 | Beck, Schuff, Lauscher, Gurevych, EACL 2024, « Sensitivity, Performance, Robustness : Deconstructing the Effect of Sociodemographic Prompting », arXiv 2309.07034 | l'invite sociodemographique marche t elle, et quand ? | **sept jeux de donnees**, taches subjectives de NLP | **six familles de modeles instruits** | sensibilite (le profil change t il la sortie), performance, robustesse a la formulation du profil | l'information sociodemographique **affecte** les predictions et peut aider en zero shot, **mais les resultats varient largement selon le type, la taille et le jeu, et sont soumis a une forte variance selon la formulation du profil** | annotation, pas enquete ; modeles de 2023 | **soutient le cadrage, comme anteriorite.** C'est le premier constat systematique que l'effet d'une etiquette depend plus de la formulation que de l'etiquette. Cite en amont par L1.01 | citation amont de L1.01 | [PROBABLE] |
| L1.27 | anonyme, 15 novembre 2025, « Two-Faced Social Agents : Context Collapse in Role-Conditioned Large Language Models », arXiv 2511.15573 | une persona socio economique tient elle sous charge cognitive ? | 15 conditions de role, trois scenarios : items de mathematiques SAT et taches de preference affective | GPT-5, Claude Sonnet 4.5, Gemini 2.5 Flash | PERMANOVA sur les reponses par condition de role, plus tailles d'effet | **GPT-5 montre un effondrement contextuel complet et adopte une identite unique, `p = 1,000`, `R^2 = 0,0004`** ; Gemini 2.5 Flash partiel (`p = 0,120`, `R^2 = 0,0020`) ; Claude Sonnet 4.5 garde une variation mesurable mais limitee (`R^2 = 0,0043`) **avec une relation statut socio economique et performance inversee**, les personas a faible statut faisant mieux. En revanche **tous les modeles gardent une preference affective conditionnee au role, `d` moyen 0,52 a 0,58**, contre une separation quasi nulle en mathematiques | trois modeles, un domaine cognitif etroit | **soutient, et donne une precision utile.** La persona survit sur la preference et meurt sur la performance : l'effondrement est **dependant de la tache**, pas global. Nos items GSS sont du cote preference, donc du cote ou la persona tient encore | citation aval de T1.13 | [PROBABLE] |
| L1.28 | anonyme, 16 juillet 2025, « The Prompt Makes the Person(a) », arXiv 2507.16076 | la formulation de la persona change t elle qui est bien simule ? | **15 groupes demographiques croises**, taches ouvertes et fermees | cinq LLM ouverts | alignement et stereotypie selon le format d'adoption de role et la strategie d'amorcage demographique | **les modeles peinent a simuler les groupes marginalises, mais le format compte** : un format d'entretien et un amorcage par le prenom **reduisent la stereotypie et ameliorent l'alignement**. Resultat inattendu : **OLMo-2-7B fait mieux que Llama-3.3-70B** | pas de verite terrain individuelle appariee | **soutient, et donne un levier a cout nul.** L'amorcage par prenom plutot que par etiquette explicite est exactement le « temoin negatif sans essentialisation » de Wang, Morgenstern et Dickerson (T1.10), teste ici sur 15 groupes | citation aval de L1.04 | [PROBABLE] |
| L1.29 | Wu, Lin, Qiu et al., 2 mars 2026, « The Personality Trap : How LLMs Embed Bias When Generating Human-Like Personas », arXiv 2602.03334 | quelles personnes le modele invente t il quand on le laisse faire ? | populations synthetiques generees a partir de reponses a des questionnaires de personnalite | cinq LLM | representativite sociodemographique des personas generees, et alignement aux traits vises | les modeles reproduisent les correlations connues entre personnalite et sociodemographie **mais presentent tous un biais WEIRD prononce**, favorisant des individus jeunes, diplomes, blancs, heterosexuels, occidentaux, centristes ou progressistes, seculiers ou chretiens. **Quand on maximise le psychoticisme, plusieurs modeles surrepresentent les identites non binaires et LGBTQ+** | pas de verite terrain de population | **soutient, et donne l'exemple le plus net d'essentialisme residuel.** Une association pathologisante apparait quand on pousse une dimension de personnalite : l'etiquette de groupe est attachee a une valeur clinique | citation aval de T1.10 | [PROBABLE] |
| L1.30 | Wang, Fu, Yao et al., 21 mars 2025, « LLM Generated Persona is a Promise with a Catch », arXiv 2503.16527 | les personas generees par LLM sont elles utilisables a grande echelle ? | **environ un million de personas generees, publiees** ; previsions d'election presidentielle et enquetes d'opinion generales aux Etats Unis | plusieurs LLM | ecart aux resultats reels des simulations fondees sur ces personas | les techniques ad hoc de generation de personas produisent des **biais systematiques** qui menent a des **deviations significatives des resultats reels** ; les auteurs appellent a une science de la generation de personas | pas de chiffres lus dans le corps ; jeu de personas public | **soutient le cadrage, et fournit une ressource.** Un million de personas publiques permet de tester un pipeline sans en generer | citation aval de T1.14 | [PROBABLE] |
| L1.31 | anonyme, 12 juin 2026, « Marginal Alignment Does Not Guarantee Joint-Distribution Fidelity », arXiv 2606.12433 | des marges justes garantissent elles une structure jointe juste ? | **NVIDIA Nemotron-Personas-Korea, un million de personas synthetiques coreennes** ; references officielles KOSIS et KEIS ; replication sur une autre locale | jeu de personas synthetiques, pas un modele | **Independence-Assumption Footprint** : pour chaque combinaison d'attributs que la fiche du jeu declare traitee comme independante, comparaison de la jointe synthetique a une jointe officielle | le jeu **s'aligne sur les marges KOSIS et echoue sur trois jointes** : la distribution filiere x profession contre l'univers des diplomes KEIS presente un fort desaccord conditionnel ; le profil d'age du service militaire est institutionnellement incoherent ; **la representation feminine dans les professions a dominante masculine est fortement aplatie vers la parite** | audit d'un jeu de donnees, pas d'un simulateur ; un pays | **soutient la mesure de structure.** Quatrieme instrument apres le Cramer's V de Ma (T1.29), le Rand ajuste de Jia (T1.26) et le C2ST de Marciaga (T1.30). Et le motif d'echec est nomme : **aplatissement vers la parite**, c'est a dire vers une independance des attributs que le reel n'a pas | citation aval de L1.04 | [PROBABLE] |
| L1.32 | anonyme, 21 novembre 2025, « Can Finetuning LLMs on Small Human Samples Increase Heterogeneity, Alignment, and Belief-Action Coherence ? », arXiv 2511.21218 | un pilote humain suffit il a rendre le simule utilisable en inference ? | experience comportementale sur la divulgation d'information | LLM de base et ajuste sur un petit sous ensemble humain | divergence distributionnelle, alignement par sous groupe, coherence croyance action, **recuperation des coefficients de regression de l'etude originale** | l'ajustement sur un petit echantillon humain **ameliore substantiellement l'heterogeneite, l'alignement et la coherence croyance action** par rapport au modele de base. **Mais meme le meilleur modele ajuste ne reproduit pas les coefficients de regression de l'etude originale** | un seul domaine, une seule experience | **soutient la reorientation, et pose la limite exacte.** A rapprocher de Krsteski (T1.24) : cent repondants suffisent a ramener un biais sous 5 pour cent, et pourtant **cela ne suffit pas pour une analyse inferentielle formelle**. Le message operationnel du projet doit se tenir a l'estimation, pas a l'inference | citation aval de T1.12 | [PROBABLE] |
| L1.33 | anonyme, 24 juillet 2026, « Reason-Mediated Behavioral Models for Auditing LLM Social Simulators », arXiv 2607.24649 | le simulateur atteint il la bonne reponse par le bon chemin ? | test de concept sur creme solaire, **94 personnes**, trois concepts chacune, avec justifications ouvertes ecrites | LLM | codage des justifications en etats de raison signes ; le raisonnement humain ameliore t il la prediction hors echantillon, et le LLM retrouve t il le meme etat sans voir la justification ni le resultat | **les raisons humaines ameliorent substantiellement la prediction hors echantillon de l'intention d'achat ; les raisons simulees par LLM sont fragiles : plausibles, mais elles repetent souvent l'argumentaire du produit au lieu de retrouver le chemin d'acceptation ou de refus du repondant** | 94 personnes, un domaine commercial | **soutient, et propose un audit reutilisable.** Un simulateur peut donner la bonne reponse par la mauvaise raison. C'est la version « chemin » de notre resultat a31 sur les fausses raretes, qui sont les raretes typiques du segment et non celles de la personne | citation aval de T1.10 | [PROBABLE] |

---

## Comment ca fonctionne

### Le mecanisme central : le conditionnement demographique a un budget, et il vaut une etiquette

La question qui organise tout le theme n'est pas « le modele est il precis », c'est « que fait il
d'une information d'identite ». Rennard et Xypolopoulos y repondent par une mesure qui n'existait
pas (L1.01). L'idee de leur dispositif merite d'etre reprise ici parce qu'elle est reutilisable :
plutot que de comparer une sortie a deux etiquettes a sa cible, ils comparent **son erreur** a
l'erreur que le modele fait deja quand il ne recoit qu'une des deux. Le biais d'un trait simple est
une signature reproductible, un tampon que le modele appose chaque fois que ce trait entre dans
l'invite. Si le modele conditionne vraiment sur les deux, il appose les deux tampons et le biais de
la paire ressemble a leur somme. S'il en jette un, il n'appose qu'un tampon. C'est un test qui ne
demande aucune donnee nouvelle et qui, decisif, ne depend pas de savoir si le modele est bon.

Le resultat est que le meilleur trait simple explique le biais de la paire dans 75,3 a 81,2 pour
cent des cellules selon le modele, contre des bornes de calibration construites sur le bruit propre
du modele qui placent l'additivite pure a environ 40 pour cent et l'effondrement pur a environ 84.
Recale entre ces deux bornes, l'index d'effondrement vaut 0,83 a 0,95 : six septiemes du chemin
vers l'effondrement. La decomposition par moindres carres donne la meme chose sans contest :
les sous groupes humains se placent sur `(0,95 ; 0,95)`, poids total 1,83, les huit modeles se
placent sur la ligne `alpha + beta = 1`, poids total median 0,98, avec une part dominante mediane
de 0,88. Le modele depense une identite. Les gens en depensent deux.

Deux verifications rendent ce resultat difficile a contester et il faut les nommer, parce qu'elles
manquent partout ailleurs. D'abord, **la cible est validee comme propriete et non supposee** : les
sous groupes reels composent bien additivement, ils atteignent 44,4 pour cent sur 236 752 cellules
contre un plafond attingible de 49,3, soit 90 pour cent de leur plafond, la ou GPT-4o-mini atteint
9,3 contre son propre plafond de 29,7, soit 31 pour cent. Ensuite, **l'exces de distinction reelle
est mesure et il n'existe pas** : les paires humaines ne portent aucun surplus emergent, ce qui
interdit l'objection « les modeles echouent a une tache que les populations reelles ne font pas
non plus ». Le modele echoue a l'addition simple.

La lecture la plus utile pour nous n'est pourtant pas celle la. C'est la separation, faite par les
auteurs, entre **deux defauts qui se cumulent**. La regle additive appliquee aux **vraies**
distributions de traits simples atteint 0,062 de distance de variation totale en profondeur 2, soit
sous le plancher de bruit d'echantillonnage humain de 0,120 et au quart de l'erreur native du
modele a 0,238. Autrement dit, la composition n'est pas le probleme d'exactitude ; l'erreur vit
entierement dans les distributions a un trait, qui sont mal calibrees avant meme d'etre combinees.
Sous la calibration actuelle, l'effondrement **ne coute presque rien en exactitude**. Sa portee est
representationnelle : quelle identite est effacee.

Et la reponse a cette derniere question est le second resultat du papier. Le trait retenu s'accorde
avec le trait humainement dominant dans 53,3 a 57,9 pour cent des cas, contre un plancher de
permutation a 50,4 a 52,2 : trois a sept points au dessus du hasard. Le residu est un a priori fixe
et invariant au theme : genre sur retenu de 12,5 points par rapport a ce que le reel justifie,
revenu de 3,0 ; **race sous retenue de 9,5 points, religion de 5,0**, la race l'etant dans les six
modeles de generation precedente et **sur les quinze themes, y compris la vague consacree aux
questions raciales, ou l'ecart vaut moins 11,4**. Au niveau des valeurs, l'ecart se creuse : moins
19 a moins 23 points pour les repondants noirs, hispaniques, asiatiques, metis, athees et juifs,
**plus 16 pour les blancs**. La « suppression de la race » est concretement le rejet des identites
minoritaires et la sur retention de la majoritaire.

Ce mecanisme s'articule exactement avec ce que le corpus de depart avait deja. Le 1,35 pour cent
contre 41 a 83 de GlobalOpinionQA (T1.06), l'effondrement du groupe des independants purs chez
Argyle (T1.01), la KL de 0,6317 chez les repondants noirs contre 0,2465 chez les blancs de Sun
(T1.11), les 23,3 pour cent sur la souverainete chez Ku (T1.31) : ce sont des symptomes locaux du
meme phenomene, mesure ici globalement. Et la formulation de la direction de these validee par Amir,
« la position n'est pas deductible de l'etiquette », trouve son revers : **le modele, lui, agit
comme si elle l'etait, et il choisit mal l'etiquette.**

### La contre partie : l'information qui predit une personne n'est pas une information de groupe

Le second mecanisme etabli est plus ancien et beaucoup moins cite. Hwang, Majumder et Tandon
l'ecrivent en 2023 (L1.05) : entre deux personnes qui partagent les memes demographies, l'accord
sur les opinions implicites tourne autour de 0,4 a 0,5 de kappa ; parmi les paires qui partagent
une opinion, 60 a 83 pour cent ont des ideologies differentes. Leur table d'exactitude est le
resultat operationnel : sans persona 0,43, avec demographies et ideologie 0,47, avec **les huit
opinions passees les plus pertinentes de la personne, seules, 0,52**. Huit reponses propres a
l'individu valent cinq points de plus que toutes ses etiquettes reunies, et le total avec les deux
n'ajoute que deux points de plus.

Orlikowski et al. (L1.18) retrouvent la meme chose par une autre voie et avec un instrument plus
severe : l'ajustement fin ameliore bien l'invite sociodemographique, mais le gain vient de
l'apprentissage du comportement propre a chaque annotateur, pas de motifs sociodemographiques ;
« models learn little meaningful connection between sociodemographics and annotation ». Cao et al.
(T1.25), Garzon et al. (T1.27), Li et Conrad (T1.40), Kinzinger et Hartmann (T1.28), Park et al.
(T1.13) disent tous la meme chose du cote positif, avec des gains de 8 a 29 points selon la
metrique. Et la fidelite de l'ancrage individuel se paie ailleurs, ce qui est le point que la
section suivante developpe.

L'ancrage non informatique de ce mecanisme etait le trou du dossier, et il existe. La litterature
de l'analyse multiniveau de l'heterogeneite individuelle et de la precision discriminante, MAIHDA
(L1.16), mesure depuis dix ans exactement cette quantite : le **coefficient de partition de
variance**, part de la variance individuelle totale qui se trouve entre strates identitaires. Le
tutoriel de reference le pose sans ambiguite : « Hypothetically, if the VPC were 100%, then knowing
the stratum average would tell us the [outcome] of every individual in the stratum ». Et l'ordre de
grandeur reel : « most studies using multilevel models to examine individuals nested in
neighborhoods, schools, or workplaces will often see VPCs less than 5%, and they rarely exceed
10% ». Leur propre illustration, sur 384 strates croisant genre, origine, diplome, revenu et age,
donne 9,4 pour cent en lineaire et 10,7 en logistique, et ils la qualifient de « relativement
importante ».

Voila la phrase du projet, en une ligne et hors informatique : **dans une population reelle,
l'etiquette explique moins d'un dixieme de la variation individuelle ; une simulation qui remplace
la personne par son groupe se comporte comme si elle en expliquait la totalite.** Xie et al. dans
PNAS (L1.03) en donnent la mesure directe : le `R^2` d'une regression du revenu sur race, genre et
diplome approche 0,6 dans les donnees simulees contre moins de 0,1 dans le NLSY reel. Chen et al.
(T1.32) avaient le meme fait sur un eta carre et un facteur quarante ; Xie et al. l'ont dans PNAS,
sur 15 modeles et 7 enquetes.

### La decomposition qui manquait : ce que la persona peut encoder, et ce qu'elle ne peut pas

Ahn, Mao et Lee (L1.02) fournissent l'explication mecanique de pourquoi enrichir une persona ne
marche pas, et c'est le resultat le plus important de la session apres L1.01. Leur geste est
simple : retirer la moyenne humaine de chaque item des deux cotes, humain et modele, et regarder ce
qui correle encore. Il reste 3,05 pour cent, contre un plafond de fiabilite test retest de 53,6.
Le modele suit tres bien la moyenne d'item, `r = 0,777` sur 133 items, et presque rien d'autre.
Le nom qu'ils donnent a cela, « item-mean surrogacy », est la version maximale de la these :
la personne n'est pas remplacee par son groupe demographique, elle est remplacee par **la
population entiere**.

La preuve que cela n'est pas un artefact de mesure vient d'une decomposition de theorie de la
generalisabilite. L'erreur de prediction se repartit en effet principal de personne 4,9 pour cent,
effet d'item 8,7, residu 86,4 ; en scindant le residu par la fiabilite test retest, l'interaction
stable personne x item vaut 44,0 pour cent et l'erreur transitoire 42,4. **L'interaction vaut 8,9
fois l'effet principal de personne.** Le signal manquant n'est donc pas « qui est cette personne
en moyenne », qu'une persona peut encoder ; c'est « comment cette personne s'ecarte de la moyenne
sur cet item precis », qu'une persona ne peut par construction pas encoder, puisqu'elle est fixe
d'un item a l'autre. C'est la raison pour laquelle Park et al. gagnent un point pour deux heures
d'entretien (T1.13) et Ye, Deng et Candogan 1,91 point pour une refonte complete de la
representation (T1.35). **La marge n'est pas dans l'entree parce que l'entree est du mauvais type.**

Trois controles verrouillent l'interpretation. La permutation de personas : l'appariement correct
donne 3,05 pour cent contre un maximum de 0,028 sur dix mille permutations, donc le signal existe,
il est simplement minuscule. L'ajustement fin ne le sauve pas : GPT-4.1 ajuste tombe a 2,31, et
Socrates-Qwen atteint 7,57 sur les etudes vues et **0,73 sur les etudes tenues a l'ecart**, ce qui
signifie qu'il a appris des motifs propres aux etudes et non des ecarts propres aux personnes. Et
le plancher trivial est humiliant : le LLM perd contre la moyenne des **autres** repondants au meme
item, `r` moyen 0,34 contre 0,45.

### Ce qui est perdu, revu a la lumiere du plancher humain

La table de depart distinguait quatre pertes. Cette session en confirme trois, en precise une, et
en ajoute une cinquieme.

**La dispersion, avec pour la premiere fois un plancher humain sur la meme mesure.** Le travail sur
le logement abordable (L1.06) compare, sur les memes cellules, la distance entre le modele et les
humains et la distance entre **deux echantillons humains apparies** : TV 0,561 contre 0,098,
Jensen Shannon 0,249 contre 0,009, Wasserstein ordinal 0,721 contre 0,147, et les dix huit cellules
depassent leur plancher. C'est la reponse a l'objection permanente « peut etre que les humains
aussi different d'eux memes ». Ils different cinq a vingt sept fois moins. Et le rapport median de
variance modele sur humain vaut 0,099 pour le meilleur modele et **0,000 pour trois des huit**,
ce qui signifie litteralement aucune variance de reponse dans au moins la moitie des cellules.
Ahn, Mao et Lee ajoutent la mesure sur quatre jeux : ecarts types medians a 65, 50 et 57 pour cent
de l'humain, categories effectivement utilisees a 43 a 73 pour cent.

**La forme, qui n'est pas reductible a la dispersion.** Zhou et al. (T1.19) avaient la
gaussianisation. Ahn, Mao et Lee la chiffrent proprement : en decomposant la distance de
Wasserstein 2 au carre en position, echelle et forme, **la forme pese 30,9 a 59,4 pour cent selon
le jeu**, et un recalage lineaire moyenne variance ne peut pas l'enlever. Cela veut dire qu'un
correctif de type dilatation, comme le Verbalized Sampling d'Ozkan (T1.33), s'attaque au tiers du
probleme au mieux.

**La structure jointe.** Xie et al. (L1.03) ajoutent la mesure la plus large : sur sept enquetes et
quinze modeles, l'entropie simulee est systematiquement inferieure a la reelle, les Cramer's V
sont gonfles avec une grappe de paires au dessus de 0,6 et certaines approchant 1, et les
distributions de sequences d'evenements de vie s'effondrent vers une trajectoire normative, avec
des taux de reussite proches de zero. L'audit de Nemotron-Personas-Korea (L1.31) montre la meme
chose sur un jeu de personas plutot que sur un simulateur : marges justes, trois jointes fausses,
et la representation feminine dans les professions a dominante masculine **aplatie vers la parite**,
c'est a dire vers une independance des attributs que le reel n'a pas.

**Les minorites, avec un mecanisme cette fois.** La table de depart notait que les groupes perdus
ne sont pas les plus petits mais ceux dont la position n'est pas deductible de l'etiquette. L1.01
ajoute une couche : ce sont aussi les groupes dont l'etiquette est **jetee la premiere**. Et L1.08
le confirme au niveau benchmark : conditionner sur un groupe degrade la simulation pour les cinq
modeles testes, `delta S` de moins 1,27 a moins 4,61, et le pire est la religiosite a moins 9,91
puis l'affiliation politique a moins 4,97. Ce sont exactement les deux dimensions que L1.01 montre
supprimees dans la composition.

**Le chemin, cinquieme perte, jamais nommee dans la table de depart.** L1.33 montre sur 94 personnes
que les raisons humaines ecrites ameliorent substantiellement la prediction hors echantillon de
l'intention d'achat, tandis que les raisons simulees sont plausibles mais reprennent l'argumentaire
du produit au lieu de retrouver le chemin d'acceptation de la personne. C'est la forme generale de
notre resultat a31 : la fausse rarete attribuee est la rarete typique du segment et non celle de la
personne. Une simulation peut avoir raison par le mauvais chemin, et rien dans les metriques de
sortie ne le voit.

### Les remedes publies, et ce qu'ils corrigent reellement

Quatre familles de correctifs existent maintenant, et il vaut la peine de les separer par ce
qu'elles reparent.

**Renoncer a l'individu repare la distribution.** Sun et al. (T1.11), Meister et al. (T1.15) et
Ozkan (T1.33) l'avaient etabli ; le travail sur le Cooperative Election Study (L1.10) le mesure a
grande echelle et, surtout, l'attribue : sur 1 680 combinaisons question x demographie, demander la
distribution directement bat interroger des personas dans 77,3 pour cent des cas, avec un
Wasserstein inferieur de 0,107, et **la voie individuelle surestime systematiquement l'homogeneite
tandis que la voie distributionnelle reproduit les ecarts types humains**. Le meme modele, le meme
jour. L'ecrasement de dispersion n'est donc pas une propriete du modele, c'est une propriete du
protocole d'interrogation individuel.

**Changer le format de sortie repare la dispersion mais pas le biais.** La notation par similarite
semantique (L1.13) fait tomber la divergence KL de 0,61 a 0,13, de 1,34 a 0,11 et de 1,97 a 0,07
selon le modele, avec un seul parametre global appris, qui generalise de l'ANES 2016 a l'ANES 2020.
Mais les auteurs sont explicites : le biais de position, les democrates synthetiques qui notent les
conservateurs trop bas, n'est pas corrige. **Dispersion et biais de groupe sont deux defauts
separables, et un correctif de dispersion ne touche pas au second.**

**Choisir le bon substrat repare la structure inter groupes, et c'est le resultat le plus important
pour la these du projet.** Le travail sur base contre post entraine (L1.07) apparie trois familles
et mesure, sur les memes 59 items et les memes six groupes, la correlation entre les distances
inter groupes du modele et celles des humains, plus le rapport moyen d'amplitude. **Les modeles de
base suivent la structure humaine, `rho` de 0,607 a 0,754, en comprimant les ecarts a environ 70
pour cent ; les modeles post entraines la suivent moins bien, `rho` de 0,350 a 0,593, et exagerent
les ecarts d'environ deux fois.** Le sens de la distorsion inter groupes n'est donc pas une
propriete des modeles de langage, c'est une propriete du post entrainement. SimBench (L1.08) donne
le mecanisme general par mediation causale : l'ajustement par instruction a un effet direct positif
de plus 6,46 sur la simulation et un effet indirect negatif de moins 1,74 passant par la reduction
d'entropie, et la difference instruct moins base contre l'entropie humaine donne `r = -0,942`, en
faveur du base des que l'entropie humaine depasse environ 0,8.

**Ajouter de l'information de personne repare l'individu, et sature.** C'est le mecanisme deja
etabli. La nouveaute de cette session est qu'on sait pourquoi il sature (L1.02, interaction
personne x item) et que la profondeur de la persona n'est pas ce qui produit la diversite (L1.09,
environ 60 mots de detail demographique valent plus 0,004 de dispersion moyenne, alors qu'une seule
phrase de role vaut 2,5 fois le meilleur des trucs a bas cout). **Ce qui cree de la diversite, c'est
qu'il y ait une identite differente d'un appel a l'autre, pas ce qu'elle contient.**

### Le mur des baselines, qui s'est epaissi

La table de depart avait deux baselines qui battent ou egalent les LLM : la regression logistique
de Chen et al. (T1.32) et la foret aleatoire de Ku et al. (T1.31). Trois s'ajoutent. Un reseau de
neurones sur graphe (L1.12) egale ou depasse la meilleure methode LLM sur trois jeux et trois
regimes, avec environ mille fois moins de parametres, et sans utiliser le texte des questions ;
sur Twin-2K il atteint 66,62 pour cent la ou le plafond test retest humain est a 81,72. Un
classifieur TF-IDF (L1.19) obtient un MCC de 0,36 contre 0,29 pour les agents, sur plus de
120 000 combinaisons. Et la modalite majoritaire de Li, Li et Qiu (T1.39) reste la baseline la plus
humiliante du corpus.

Mais un papier renverse partiellement la table, et il faut le lire attentivement parce qu'il
repond a la question 2 de notre propre liste d'absences. L'article d'Entropy (L1.11) fait courir
un LLM et une foret aleatoire **sur les memes blocs de validation croisee**, avec les memes
variables, sur dix themes de l'ANES 2020. **Le LLM a un Jensen Shannon significativement meilleur
sur six themes sur dix ; la foret a un F1 egal ou meilleur sur la plupart, et un Cramer's V
nettement superieur sur deux.** L'ecrasement n'est donc pas uniformement une propriete de tout
predicteur : chacun perd quelque chose de different. Le LLM tient la distribution, la statistique
tient l'individu et l'association. C'est exactement le renversement qu'annoncait le point 2 de
`ARBITRAGE.md` sur les minorites d'opinion, et cela le renforce plutot que cela ne le contredit.

---

## Ce qui se contredit

**1. La simulation ecrase t elle la variance intra groupe, ou la gonfle t elle ?**
Wang, Morgenstern et Dickerson (T1.10) trouvent que « nearly every single model and identity group
across each metric has less diverse LLM responses compared to human responses ». Le biais
d'homogeneite (L1.20) est positif dans six modeles sur sept pour les Hispaniques et les Asiatiques,
et il tient sur une grille de vingt cinq configurations de decodage. LifeMem (T1.38) mesure une
distance intra groupe trop faible. Et Rennard et Xypolopoulos mesurent l'inverse : `delta H = +0,18
a +0,23` nats, les distributions simulees sont **plus** dispersees, et ils ecrivent que
l'aplatissement des groupes d'identite « is between-group, not within: a hedge, not a caricature ».

**La variable explicative est le format de sortie.** Les mesures qui trouvent une compression intra
groupe portent toutes sur du **texte libre** : portraits generes, reponses ouvertes, recits. Celles
qui trouvent une dispersion excessive portent sur une **distribution fermee demandee au modele**.
En texte libre, un modele produit des variantes lexicales d'un meme contenu, ce qui donne une faible
diversite semantique ; en distribution fermee, un modele instruit qui ne sait pas produit une
repartition prudente sur les options, ce qui donne une entropie elevee. Ce ne sont pas les memes
objets. Consequence pour nous, et elle est operationnelle : **notre chaine est en choix fermes, donc
c'est le regime de L1.01, pas celui de T1.10.** Un exces d'entropie intra groupe est possible chez
nous en meme temps qu'un exces d'ecart inter groupes, et les deux doivent etre mesures separement.

**2. Les ecarts inter groupes sont ils comprimes ou exageres ?**
Le corpus de depart tenait deja les deux affirmations, entre PSII (T1.37) et LifeMem (T1.38), et
la table les reconciliait en montrant qu'aucun des deux ne mesurait un ecart entre moyennes de
groupes. Cette session ajoute deux entrees qui mesurent, elles, exactement cela, et elles se
contredisent : L1.07 mesure une compression a 0,664 a 0,704 chez les modeles de base et un
gonflement a 2,014 a 2,242 chez les post entraines. L1.23 rapporte des relations predicteur vers
resultat **attenuees**. Chen et al. (T1.32) et Xie et al. (L1.03) mesurent des gonflements de
facteur 2,3 a 40.

**La variable explicative est le post entrainement**, et le tableau de L1.07 la donne sur des
paires appariees, ce qui est la seule facon propre de l'etablir. Deuxieme variable, secondaire :
la quantite mesuree. Un « gonflement » sur une difference de proportions (Chen), sur un eta carre
(Chen), sur un `R^2` (Xie) et sur une distance TV entre groupes (L1.07) ne sont pas la meme
quantite. **Pour nous, cela transforme l'option C de l'arbitrage en test decisif et non en
supplement** : si le gonflement inter groupes est un effet de l'alignement, un modele de base doit
le faire disparaitre ou en changer le signe.

**3. Les personas contre stereotypiques sont elles plus dures a simuler ?**
Liu, Diab et Fried (L1.17) mesurent 9,7 pour cent de steerabilite en moins vers les personas
incongrues. CoMPosT (L1.04) trouve les plus forts scores de caricature sur les personas non
binaires, noires, hispaniques et moyen orientales. Rennard et Xypolopoulos ne trouvent **aucune**
penalite contre stereotypique, et meme un residu de signe oppose (`rho = +0,13`, `p = 0,01`), et
une relation plate en restreignant aux cellules a `n >= 100` (`rho = +0,04`, non significatif).

**La variable explicative est le bruit de la verite terrain, et elle est demontree, pas
supposee.** Les profils rares ont de petites cellules humaines, les petites cellules ont une verite
terrain bruitee, et le bruit se lit comme une erreur du modele. Les auteurs montrent la
decomposition sur un cas : l'erreur brute de 0,277 du profil republicain athee se decompose en
0,178 d'erreur reelle, **sous la moyenne des profils typiques**, plus 0,099 de bruit. Leur
avertissement est cite tel quel : « audits that do not control ground-truth cell size will
rediscover a spurious counter-stereotypical effect, as our own raw data did before correction ».
La seconde variable est de nouveau le format : L1.17 et L1.04 travaillent en texte libre, ou le
mot « steerabilite » designe autre chose qu'une distance de distribution. **Chez nous, cela
s'applique tel quel a la comparaison des reponses rares : une cellule de repondants rares est
petite, et il faut un plancher de bruit d'echantillonnage avant de conclure quoi que ce soit sur
une penalite propre aux gens atypiques.**

**4. L'ecrasement est il propre au modele de langage ou propre a la prediction ?**
Ku et al. (T1.31) donnent un rapport de variance de 0,72 pour une foret aleatoire contre 0,67 a
0,85 pour trois LLM, ce qui suggere que tout predicteur ecrase. L'article d'Entropy (L1.11), sur
les memes blocs de validation, trouve que **le LLM tient mieux la distribution et la foret tient
mieux l'individu**. Et le travail sur le Cooperative Election Study (L1.10) montre que le meme
modele ecrase ou n'ecrase pas selon qu'on l'interroge individu par individu ou en une fois.

**La variable explicative est le niveau auquel la quantite est definie.** Ku mesure un rapport de
variance sur des reponses individuelles simulees ; L1.11 mesure une divergence de distribution
agregee. Un predicteur statistique qui minimise une perte quadratique ecrase mecaniquement la
variance individuelle **et** la variance agregee ; un LLM interroge en distribution ne fait ni
l'un ni l'autre, et interroge en individu fait les deux. Il n'y a donc pas une reponse, il y en a
deux, et la table de depart avait raison de dire que sans baseline supervisee dans le meme plan
notre resultat n'est pas attribuable. **La nouveaute est qu'il faut deux baselines, une par
niveau**, et que L1.11 fournit le protocole exact, blocs de validation partages et bootstrap sur
les paires prediction, verite.

**5. Le realisme statistique certifie t il la validite ?**
Le champ le suppose. L1.14 le mesure et trouve `rho = 0,10` entre realisme et exactitude d'effet
de traitement, et `rho = -0,52` quand on s'en sert pour choisir un modele. **Variable explicative :
la structure d'erreur.** Les erreurs de distribution et les erreurs d'effet ne vivent pas dans le
meme espace, et l'ecart est plus grand pour les resultats comportementaux, ou les modeles semblent
extrapoler le comportement depuis des motifs attitudinaux alors que chez les humains croyance et
action sont faiblement liees (`r = 0,12`). Pour nous : **le C2ST, le ratio de dispersion et
l'exactitude individuelle sont trois cibles distinctes, et le dossier ne doit jamais presenter
l'une comme une preuve pour l'autre.**

---

## Ce que ca permet de tester chez nous tout de suite

Les couts sont donnes en temps de calcul et en appels de modele. Les tests 1 a 5 n'en demandent
aucun.

**1. Le contest de composition de L1.01, applique a nos huit conditions.** Nous avons des
conditions avec etiquette et sans etiquette sur les memes items du GSS. Le test consiste a
construire, pour chaque etiquette prise seule, le vecteur de biais `p_chapeau - p` sur les cellules
correspondantes, puis a demander si le biais d'une cellule a deux etiquettes ressemble davantage a
la somme des deux biais simples ou au meilleur des deux, en cosinus. **Cout : aucun appel de
modele, une lecture de nos sorties existantes.** Il faut ajouter les deux garde fous que le papier
impose et que personne d'autre ne pose : des bornes de calibration construites sur notre propre
bruit run a run, et un plancher nul obtenu en tirant une dimension sans rapport, qui atteint chez
eux un cosinus median de 0,84. **Interet pour la these : si notre index d'effondrement est du meme
ordre que le leur, la these est confirmee sur un troisieme jeu ; s'il differe, la difference est
elle meme le resultat, parce que nos cellules sont adossees a des individus reels et les leurs
non.**

**2. Le `R^2` demeane de L1.02, sur le paquet OSF t6g7k et sur nos agents locaux.** Retirer la
moyenne humaine de chaque item des deux cotes, correler ce qui reste, et diviser par la fiabilite
test retest de la vague 2 que nous avons deja. **Cout : aucun appel de modele.** C'est le test le
plus rentable de la liste. Nous sommes le seul projet a disposer, sur les memes personnes, d'une
exactitude d'agent, d'une re interrogation a deux semaines et de conditions avec et sans etiquette.
Ahn, Mao et Lee ont l'exactitude et le plafond, mais aucune segmentation. **Le chiffre qu'aucun
papier ne possede est le `R^2` demeane des agents avec etiquette contre celui des agents sans
etiquette, chacun normalise par le meme plancher humain.** Si l'etiquette ne change pas le `R^2`
demeane alors qu'elle change l'exactitude brute, alors l'etiquette n'ajoute que de la moyenne de
groupe, ce qui est la these, demontree.

**3. Le plancher humain humain de L1.06, sur nos propres distances.** Toutes nos distances au reel
doivent etre accompagnees d'une distance obtenue entre deux moities de l'echantillon humain, ou
entre la vague 1 et la vague 2 des memes personnes. **Cout : aucun appel de modele.** Chez eux,
TV humain humain 0,098 contre 0,561 pour le meilleur modele. Notre controle vague 2 a
(1,003 ; 1,004) est deja de cette famille ; le geste consiste a l'appliquer a **chaque** metrique
publiee, pas seulement au ratio de dispersion.

**4. La decomposition de Wasserstein 2 en position, echelle et forme, sur nos huit conditions.**
Trois termes non negatifs qui somment a la distance au carre. **Cout : aucun appel de modele,
quelques dizaines de lignes.** Chez Ahn, Mao et Lee la forme pese 30,9 a 59,4 pour cent selon le
jeu. Si la forme pese autant chez nous, alors tout correctif de dilatation, y compris le Verbalized
Sampling d'Ozkan, plafonne mecaniquement, et nous pouvons le dire avec un chiffre.

**5. Le plancher de bruit de cellule avant toute conclusion sur les reponses rares.** Le resultat le
plus net de `ARBITRAGE.md` porte sur les reponses que moins d'une personne sur dix donne, donc sur
de petites cellules. L1.01 demontre que l'absence de ce controle fabrique un effet contre
stereotypique la ou il n'y en a pas. Le geste : couper l'echantillon humain en deux moities
aleatoires, calculer la distance entre les deux, et soustraire ce plancher de chaque erreur avant
de comparer les groupes. **Cout : aucun appel de modele.** C'est aussi la contre expertise
obligatoire de notre propre resultat sur les fausses raretes.

**6. La condition « distribution directe » contre nos personas, sur les memes items.** L1.10 montre
un gain de 0,107 de Wasserstein normalise pour la voie distributionnelle sur 77,3 pour cent de
1 680 combinaisons, avec le meme modele. **Cout : un appel par question et par cellule, donc de
l'ordre de quelques centaines d'appels, une soiree.** Si la voie distributionnelle reproduit la
dispersion humaine sur nos items la ou nos personas l'ecrasent, alors la partie « ecrasement » de
notre resultat est un enonce sur le protocole et non sur le modele, et il faut le dire ainsi.

**7. Le contraste base contre aligne, avec la mesure d'ecart inter groupes de L1.07.** C'est
l'option C de l'arbitrage, et cette session la rend decisive plutot que facultative. Le protocole
exact est publie : correlation de Spearman entre les distances par paires de groupes chez le
modele et chez les humains, plus rapport moyen d'amplitude. **Cout : une nuit de calcul, deux
familles a poids ouverts en versions base et instruct.** Chez eux, 0,70 en base contre 2,0 en
aligne. **Si notre gonflement inter groupes disparait ou change de signe sur le modele de base,
alors la phrase a defendre devient « une societe simulee par un modele aligne remplace chaque
personne par son groupe », ce qui est plus precis et plus interessant que la version actuelle.**

**8. L'amorcage par prenom contre l'etiquette explicite, sur nos items.** L1.28 montre qu'un format
d'entretien et un amorcage par prenom reduisent la stereotypie sur 15 groupes ; T1.10 avait montre
que des personas aleatoires atteignent une couverture egale ou superieure sans essentialiser.
**Cout : une reexecution de la condition avec etiquette, meme volume d'appels que l'original.**
C'est le temoin negatif qui manque a notre plan : si le prenom donne l'exactitude de l'etiquette
sans le gonflement inter groupes, nous avons un remede a publier et pas seulement un diagnostic.

**9. La comparaison a deux niveaux du protocole de L1.11.** Faire courir nos deux baselines B0 et
B1 et nos agents **sur les memes blocs de validation croisee**, et publier F1, Cramer's V et
Jensen Shannon cote a cote, avec un bootstrap sur les paires prediction, verite. **Cout : aucun
appel de modele si les predictions sont deja stockees.** C'est la table qui repond a la question
« l'ecrasement est il propre au LLM », et l'article d'Entropy montre que la reponse depend du
niveau, donc que la table a deux niveaux est le livrable, pas une seule ligne.

---

## Ce que personne n'a fait

Les constats d'absence de la table de depart sont revus a la baisse par cette session, parce que
trois d'entre eux sont maintenant occupes. Ce qui suit est la liste corrigee, avec la reserve
d'usage : une recherche par absence n'est pas une preuve d'absence.

1. **Personne ne mesure un ecrasement de dispersion normalise par un plancher humain avec, dans le
   meme plan, une condition avec etiquette et une condition sans etiquette.** L1.06 a le plancher
   humain humain mais une seule condition de conditionnement. L1.01 a les deux conditions mais
   aucun plancher de fiabilite temporelle. L1.02 a le plancher de fiabilite mais aucune
   segmentation. **Le croisement des trois est vide, et c'est exactement notre paquet OSF.**

2. **Personne ne mesure le budget d'identite de L1.01 sur des individus apparies.** Rennard et
   Xypolopoulos travaillent sur des cellules demographiques et le disent : leur additivite est
   « operationalised deliberately conservatively, at the level of ATP closed-form marginal opinion
   distributions ». La question « une persona a deux etiquettes predit elle une **personne** comme
   la somme de ses deux etiquettes, ou comme une seule » n'a pas de reponse publiee. Twin-2K-500 et
   l'archive t6g7k la rendent calculable.

3. **Personne ne relie le budget d'identite au `R^2` demeane.** Ce sont deux mesures du meme fait,
   parues a cinq jours d'intervalle, par deux equipes qui ne se citent pas. L1.01 dit que le
   modele garde une etiquette sur deux ; L1.02 dit que ce que le modele garde d'une personne, c'est
   la moyenne de l'item. Si les deux sont vrais, alors **le trait retenu par le modele est celui
   qui deplace le moins la reponse par rapport a la moyenne d'item**, ce qui est une prediction
   testable et que personne n'a formulee.

4. **Personne ne mesure la dispersion avec le plancher humain sur autre chose qu'un domaine.**
   L1.06 le fait sur le logement abordable, dans une seule experience. Aucun panel longitudinal
   n'a servi a construire un plancher de dispersion, alors que le LISS, le SOEP, Add Health et
   Understanding Society sont tous utilises dans ce corpus (T1.26, T1.28, T1.38) et tous
   longitudinaux. **L'absence est reconnue par ecrit par Garzon et al. : « We did not assess this
   reliability but relied on a single set of pre-existing answers ».**

5. **Personne ne teste le classifieur synthetique contre reel comme critere de fidelite de
   population, sauf Marciaga et al.** Le constat de la table de depart tient apres cette session :
   sur soixante treize entrees, un seul travail rapporte un Classifier Two-Sample Test. Le
   dispositif est de quinze lignes et il fait tomber ensemble les marges, la structure et la
   dispersion.

6. **Personne n'articule les deux formats de sortie sur les memes personnes.** La contradiction 1
   ci dessus est resolue par une hypothese, pas par une experience. Aucun travail ne demande, aux
   memes personas et sur les memes items, une reponse en texte libre **et** une distribution
   fermee, pour verifier que la dispersion intra groupe change de signe entre les deux. C'est
   faisable, c'est bon marche, et cela reconcilierait une contradiction que le champ traine depuis
   trois ans.

7. **Personne ne publie de courbe de specification sur une mesure de dispersion.** Cummins (T1.20)
   en publie une sur des correlations, SILICA (L1.24) montre qu'un simple echange d'ordre coute
   58 points de cooperation, L1.06 montre un decalage d'ordre de +0,367 sur le contraste principal.
   Aucun des trois ne fait courir la variation de pipeline sur un ratio de variance ou une entropie.
   **Sans cela, aucun chiffre de dispersion publie n'est defendable en relecture, y compris les
   notres.**

8. **Personne ne relie la « discriminatory accuracy » de la litterature MAIHDA a la simulation par
   LLM.** Aucun des soixante treize travaux ne cite Merlo ni Evans, sauf L1.01 qui les cite en
   passant pour justifier son hypothese d'additivite. Or c'est la litterature qui a le mot, la
   metrique et vingt ans de valeurs de reference sur la question exacte que le champ redecouvre.
   **Poser nos resultats en VPC et en AUC de strate, plutot qu'en ratio maison, rendrait le
   dossier lisible par les epidemiologistes sociaux et les sociologues quantitatifs, qui sont un
   public plus large que celui de l'apprentissage automatique.**

---

## Ce que je n'ai pas pu verifier

1. **Les annexes de L1.01.** Les Extended Data figures 1 a 7 et les tables 1 a 3 sont dans le PDF
   mais leur mise en page est reconstruite par `pdftotext -layout`, avec des figures dont le texte
   se melange aux axes. Les chiffres cites ici viennent tous du corps du texte, jamais d'une
   lecture de figure. **Les valeurs `delta H = +0,18 a +0,23` nats et la distinctivite 0,0082 vers
   0,0147 vers 0,0204 sont dans le corps ; leur decomposition par modele est en Extended Data et
   n'a pas ete verifiee.**

2. **Le detail des tables S1 a S6 de L1.02.** Le corps du papier et une partie du materiel
   supplementaire ont ete lus. La classification de la litterature en 63 papiers, 53 partisans, 44
   partisans empiriques dont 33 agreges seulement, vient du corps du texte. **La table S1b, qui
   detaille papier par papier, n'a ete lue que par extraits ; les lignes citees ici, Kim et al.
   2024, Cui et al. 2025 et Maier et al. 2025, viennent de ces extraits.**

3. **Les figures 2 a 4 de L1.03 (PNAS).** Le texte lu via PubMed Central donne les enonces mais les
   valeurs numeriques des boites a moustaches ne sont pas dans le texte. **Le `R^2` d'environ 0,6
   contre moins de 0,1 pour le revenu, les Cramer's V au dessus de 0,6 et approchant 1, et
   l'entropie systematiquement inferieure sont tous des enonces textuels, pas des lectures de
   figure. Aucune valeur de taux de reussite par modele n'est reprise ici, parce qu'elles ne sont
   que dans la carte de chaleur de la figure 2.**

4. **Le modele employé par L1.02 pour la ligne principale.** Le texte parle de « the LLM » et de
   variantes de modeles sans nommer le modele principal a l'endroit ou le 3,05 pour cent est donne.
   La ligne « Fine-tuned GPT-4.1 » indique une famille, pas la ligne de base. **A relire avant
   citation externe.**

5. **La version publiee de L1.03.** L'article PNAS est en libre acces via PubMed Central mais le
   texte de la version editeur n'a pas ete compare a celui du depot. Les auteurs sont listes deux
   fois dans OpenAlex, ce qui suggere une notice dedoublee ; **la liste d'auteurs donnee ici est
   celle d'OpenAlex et n'a pas ete verifiee sur la page de l'editeur, qui renvoie un 403.**

6. **Le corps de L1.17, L1.18, L1.19, L1.20, L1.21, L1.22, L1.23, L1.24, L1.25, L1.26, L1.27,
   L1.28, L1.29, L1.30, L1.31, L1.32 et L1.33.** Ces seize entrees sont classees [PROBABLE] :
   resume lu a la source primaire, arXiv ou notice d'editeur, corps non ouvert. **Les chiffres qui
   y figurent viennent tous du resume, ou ils sont donnes explicitement par les auteurs. Aucun
   n'est extrait d'un tableau non lu.**

7. **Merlo 2018 et Evans et al. 2018.** Les deux articles fondateurs de MAIHDA sont derriere le
   paywall Elsevier de Social Science & Medicine ; seul le tutoriel de 2024 en libre acces a ete lu
   integralement. **La phrase de reference sur les VPC inferieurs a 5 pour cent est citee dans le
   tutoriel comme venant de Subramanian et O'Malley 2010, que je n'ai pas ouvert.** Avant tout
   usage externe, remonter a la source.

8. **L'exhaustivite.** Les recherches se sont appuyees sur les API OpenAlex et Semantic Scholar,
   sans cle, et sur arXiv. Semantic Scholar a renvoye un `429` a mi parcours, ce qui a impose de
   passer par arXiv pour une partie des resumes ; **il est possible que des citations aval de
   Toubia et al. et de Peng et al. aient ete tronquees a la centaine de resultats.** Le budget de
   recherche web de la session etait epuise a l'ouverture, donc aucune recherche par mots cles
   generale n'a pu etre lancee : tout ce qui figure ici a ete atteint par le graphe de citations.
   Les actes de conference non deposes sur arXiv, SSRN et les revues de sociologie quantitative
   n'ont pas ete balayes.

9. **Le lien entre L1.01 et L1.02.** L'hypothese formulee au point 3 de « Ce que personne n'a fait »,
   selon laquelle le trait retenu serait celui qui deplace le moins la reponse par rapport a la
   moyenne d'item, est **une conjecture de ma part**. Ni l'un ni l'autre papier ne la formule, et
   je ne l'ai pas testee.
