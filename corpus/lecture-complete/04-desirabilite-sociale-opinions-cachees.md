# Theme 04, lecture complete : ce que les gens ne disent pas, et ce que les modeles en font

Consigne : `corpus/lecture-complete/00-CONSIGNE.md`. Grille : `corpus/00-GRILLE.md`.
Table initiale : `corpus/04-desirabilite-sociale-opinions-cachees.md` (50 references, ids 04-01 a 04-50).
Resultats de reference : `resultats/a25-items-sensibles-au-mode.md`, `resultats/a28-trois-tests-decisifs.md`
section 1, `ARBITRAGE.md`.

Lecture faite le 8 septembre 2026 au soir. Le budget de recherche web etait epuise a l'ouverture de
la session ; tout ce qui suit a donc ete trouve par remontee et descente de citations sur OpenAlex et
Semantic Scholar, par exploration directe des depots de NORC, et par l'API arXiv. C'est une
contrainte qui s'est revelee heureuse : elle a force l'ouverture du catalogue des rapports
methodologiques du GSS, qui est la principale nouveaute de cette lecture.

Certitude : [CONFIRME] lu dans le texte, [PROBABLE] resume ou source secondaire, [NON LU] titre seul.

**Ce que cette lecture ajoute en une phrase.** L'ampleur par item que `a25` declarait introuvable
existe, mais elle n'existe pas la ou nous la cherchions : NORC ne la publie pas dans sa note de mode
de 2022, il la publie ailleurs, dans ses rapports methodologiques MR099, MR086, MR010 et MR141, et
la litterature economique vient de la rassembler pour les comportements dans un atlas publie en juin
2025 ; et cette ampleur, une fois lue, contredit sur trois points le protocole de `a25`.

**26 references nouvelles**, dont **11 lues en entier**.

---

## Table etendue

Colonne « trouve par » : `table initiale` (deja dans `corpus/04`), `citation aval` (descente depuis
une reference confirmee), `citation amont` (remontee), `depot NORC` (catalogue des rapports
methodologiques du GSS), `arXiv` (listage de l'API).

| id | reference | question posee | donnees | modeles | mesure exacte | resultat chiffre principal | faille ou limite | rapport a la these | trouve par | certitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L04-01 | Smith, T. W. et Dennis, J. M. (2004), *Comparing the Knowledge Networks Web-Enabled Panel and the In-Person 2002 General Social Survey: Experiments with Mode, Format, and Question Wordings*, GSS Methodological Report No. 99, NORC, mars 2004 | que fait le passage du face a face au web sur les items de depenses du GSS, item par item | GSS 2002 en face a face, N = 2 765, taux de reponse 70,1 pour cent ; panel Knowledge Networks 2002, N = 1 655, taux de reponse d'environ 13 pour cent ; 17 items de depenses, poses en premier des deux cotes pour neutraliser le contexte | sans objet | distributions « trop / juste / pas assez » par item et par mode, don't know retires ; quatre formats de don't know cote web | **ecart moyen de 3,9 points sur 17 items, 6 comparaisons significatives sur 17**. Les cinq gros ecarts : depenses pour les Noirs **13,8 points** de « trop » en plus sur le web (18,3 contre 32,1 pour cent) et 9,7 points de « pas assez » en moins (32,7 contre 23,0) ; welfare 9,7 points ; aide etrangere 8,5 points ; toxicomanie 7,0 points ; grandes villes 6,3 points. Niveaux de don't know : GSS 3,4 pour cent, KNS-A 3,2, KNS-C 10,6, KNS-D 11,0, **KNS-B 16,2** ; par item le DK va de 0,9 pour cent (education) a 10,5 (villes). Sur 49 items d'opinion, les DK passent de 4,4 pour cent en 1998 et 2000 a 2,6 pour cent en 2002 avec le passage du papier au CAPI | panel de volontaires recrutes par RDD, taux de reponse de 13 pour cent contre 70 ; selection et mesure confondues ; un seul jeu de 17 items | **la piece qui manquait a `a25`.** Elle donne une ampleur de mode continue, item par item, sur exactement la famille `nat*` que `a25` traite par une regle uniforme. Et elle contredit le pole retenu : voir L04-01 dans « ce qui se contredit » | depot NORC | [CONFIRME] |
| L04-02 | Smith, T. W. (1995), *The Impact of the Presence of Others on a Respondent's Answers to Questions*, GSS Methodological Report No. 86, NORC, decembre 1995 | la presence d'un tiers pendant l'entretien change t elle les reponses | GSS, N = 849 pour le volet conjoint ; items de sexualite, de religion, d'evaluation de soi et d'evaluation d'autrui | regressions bivariees puis avec controles de taille du menage, age, education, race, statut marital | associations entre presence d'un tiers et distribution des reponses | un tiers est present dans **37 a 57 pour cent** des entretiens nationaux en face a face, en baisse de 55 a 57 pour cent en 1966 a 1972 vers 37 pour cent en 1994 ; protocoles stricts : presence du conjoint ramenee a 6 a 11 pour cent. **Aucune difference significative associee a la presence du conjoint.** Presence de quelqu'un : **3 associations sur 13** significatives, et une seule survit aux controles, la sante auto declaree (**29 pour cent d'« excellente » avec quelqu'un contre 34 pour cent seul** ; 35, 31 et 23,5 pour cent pour 0, 1 et 2 personnes et plus) | echantillon modeste, un seul item auto administre (`evstray`), puissance faible ; Aquilino 1993 trouve des effets avec N jusqu'a 6 882 | **contredit frontalement 04-14.** Le moderateur le plus puissant de la meta analyse de Gnambs et Kaspar, la presence d'un tiers, est nul sur les items d'attitude du GSS. La variable qui explique : Gnambs mesure des comportements honteux auto administres, Smith mesure des attitudes dites a voix haute | depot NORC | [CONFIRME] |
| L04-03 | Sparkman, R., Wells, B. M., Norling-Ruggles, A., Schapiro, B. et Bautista, R. (2024), *The Effect of Question Presentation in Web-based Surveys: Two Experiments from the General Social Survey*, GSS Methodological Report No. 141, septembre 2024 | qu'arrive t il aux reponses du GSS quand la modalite « volontaire » (il depend, ca reste, ne sais pas) devient visible sur le web | GSS 2021 et 2022, deux experiences randomisees : grille contre item isole ; modalite volontaire affichee (`-V`) contre retiree (`-NV`) | sans objet | proportions par modalite et par condition, poids WTSSNRPS, correction de Bonferroni pour 38 comparaisons (seuil 0,0013) | **la grille ne change presque rien** : un seul item significatif en 2021, aucun en 2022, et rien ne survit a la correction. **La modalite volontaire change tout** : significatif pour presque tous les items, en 2021 et en 2022, et la plupart survivent a Bonferroni. Ampleur par item, part prenant la modalite volontaire en 2022 : `aged` « ca depend » **62,8 pour cent**, `divlaw` « ca reste » 54,1, `helpful` 44,9, `getahead` 43,8, `fair` 43,3, `courts` 41,0, `trust` 39,2, `fucitzn` 27,6, `postlife` 26,1, `uswary` 20,6, `prayer` 18,2, `reliten` 16,2, `grass` 15,8, `fepol` 14,3, `kidssolv` 10,8, `bible` 10,1, `racopen` 9,9, `discaffw` 7,3, `uscitizn` 3,0 et **0,8**. Effet en cascade : `aged` « bonne idee » passe de 66,9 a 25,5 pour cent, soit **41 points** | l'experience est propre mais elle porte sur des items en partie hors de nos 149 ; les conditions melangent web et modes anterieurs pour la comparaison a 2018 | **une ampleur continue par item, mesuree sur le GSS en 2021 et 2022, sur une echelle de 0,8 a 62,8.** Ce n'est pas de la desirabilite, c'est de la conception d'item, et c'est un confondant direct pour `a25` : plusieurs de ces items sont dans nos 65 temoins negatifs | depot NORC | [CONFIRME] |
| L04-04 | NORC (2022), *2021 GSS Cross-section Methodological Primer* | qu'est ce qui a change dans le GSS 2021 | GSS 2021, echantillon par adresse, push to web | sans objet | sans objet | trois ruptures : courrier au lieu d'enqueteur, tirage par « anniversaire le plus recent » au lieu d'aleatoire dans le menage, questionnaire en ligne. Et surtout, pour nous : **« attitude and opinion questions [...] did not show 'Don't know' responses »**, alors que les questions factuelles les gardaient ; une modalite « skipped on web » remplace le refus. Sous representation des moins de 30 ans, des non diplomes du secondaire et des repondants noirs | note descriptive, aucun chiffre d'ecart | **les humains du GSS 2021 etaient, sur les attitudes, en choix force exactement comme nos agents.** Toute comparaison qui oppose 2018 (don't know disponible) et 2021 (don't know retire) melange desirabilite et format. C'est aussi le seul point ou l'humain et l'agent sont dans le meme regime | depot NORC | [CONFIRME] |
| L04-05 | Schapiro, B. (2026), *Recent Changes in GSS Questions on Religion*, GSS Methodological Report No. 145, mars 2026 | la chute de la religiosite mesuree sur le web est elle un effet de mode ou un effet de conception | GSS 2012 a 2024, RELIG / DENOM / OTHER, par mode, non pondere | sans objet | distributions d'affiliation par mode et par annee | 2022, face a face contre web : protestants **45,4 contre 36,1 pour cent** (9,3 points), sans religion **24,3 contre 32,7 pour cent** (8,4 points), catholiques 20,9 contre 21,4. Le web est **plus stable dans le temps** que le face a face, ce qui est l'inverse de ce qu'on attendrait d'un effet de selection pur. NORC impute une part a un artefact de conception : **« Differential stimulus between the web and face-to-face (FTF) modes also heightened these differences »**, l'ecran web affichant la liste des religions alors qu'aucune carte n'etait remise en face a face. Avant le passage au web, un peu plus d'un repondant sur cinq finissait en reponse ouverte a RELIG | non pondere, pas de decomposition selection / mesure, chevauchement avec le choc de la periode 2020 a 2022 | **la chute de la religiosite sur le web du GSS n'est pas etablie comme un effet de desirabilite.** Or `attend`, `pray`, `reborn`, `savesoul` portent quatre des dix poles de desirabilite de `a25`, dont les quatre marques [CONFIRME] d'apres NORC. La source elle meme se retracte partiellement | depot NORC | [CONFIRME] |
| L04-06 | Smith, T. W. (1981), « Qualifications to generalized absolutes: 'approval of hitting' questions on the GSS », GSS Methodological Report No. 10, repris dans *Public Opinion Quarterly* 45, 224 a 230 | quand un repondant du GSS dit « non » a l'approbation de coups portes par la police, que veut il dire | GSS 1976 et 1978, question generale « any situations you can imagine » suivie de quatre situations concretes pour la police et cinq pour un homme adulte | echelle de Guttman, gammas | part des « non » a la question generale qui approuvent au moins une situation concrete | **86 pour cent** de ceux qui desapprouvent en general approuvent au moins une situation de coups portes par la police, avec **1,52 situation approuvee en moyenne** ; **83,7 pour cent** et 1,82 pour l'homme adulte. L'asymetrie est totale : seuls **1,1 pour cent** des « oui » a la question generale n'approuvent aucune situation, et 2,4 pour cent pour l'homme adulte. Dans une echelle de Guttman, l'item general n'est pas le plus difficile, il tombe au milieu. Les contradicteurs ont moins d'education (gamma passant de 0,289 a 0,683 selon le nombre de situations approuvees), sont plus souvent des femmes et des non blancs, et sont **moins** punitifs sur les autres items | donnees de 1976 et 1978 ; le contredit peut venir de la reponse situationnelle et non de la reponse generale, l'auteur en discute | **c'est la reference decisive pour l'item qui porte le resultat de la section 4 de `a25`.** Quand nos agents locaux font approuver la violence policiere a 71 et 50 personnes sur 150 la ou 9 humains l'approuvent, le « 9 » est le chiffre d'une question absolue dont NORC etablit que 86 pour cent des « non » se contredisent des qu'on pose une situation. L'agent n'est pas forcement plus dur, il peut lire l'item comme une question situationnelle | depot NORC | [CONFIRME] |
| L04-07 | Smith, T. W. (s. d.), *Discrepancies in Past Presidential Vote*, GSS Methodological Report No. 21, NORC | de combien le vote declare est il gonfle sur le GSS | GSS, CPS, etudes electorales du Michigan, resultats officiels | sans objet | ecart entre participation declaree et participation calculee sur les resultats | le vote declare du GSS est superieur d'**environ 10 points** aux estimations tirees des resultats ; le CPS est **3 a 7 points en dessous du GSS**, avec deux causes creditees : taux de reponse de 96 pour cent contre 75 pour cent, et surtout usage d'informants pour les autres membres du menage, ce qui « probably reduces the percent voting by lessening the social desirability bias ». Sur le choix de candidat, ecart absolu moyen de **3,3 points** pour le GSS et 3,1 pour le Michigan ; **le GSS estime toujours la part democrate plus haut que le Michigan, de 4,2 points en moyenne** | rapport ancien, elections des annees 1970 et 1980 ; validation individuelle absente | ampleur de la sur declaration de vote propre au GSS, distincte du 15,8 points du CCES de 04-20. Et un effet de maison sur le choix de candidat, 4,2 points vers le democrate, qui est un confondant a part entiere pour `pres16` et `if16who` | depot NORC | [PROBABLE] |
| L04-08 | Sparkman, R., Barari, S., Schapiro, B. et Bautista, R. (2026), *Leveraging Large Language Models to Code Open-Ended Responses in the General Social Survey*, GSS Methodological Report No. 150, juillet 2026 | un LLM code t il les reponses ouvertes du GSS aussi bien qu'un codeur expert | questionnaire de suivi du GSS 2024 ; deux domaines, composition du menage (factuel) et probleme le plus important du pays (attitudinal) ; verite terrain = **auto classification par le repondant lui meme** | GPT-5, GPT-5-Mini, Claude Sonnet 4.5, plus un codeur expert humain | exactitude par categorie, deux strategies de prompt | sur l'attitudinal, **codeur expert 63 pour cent, GPT-5 64 a 65 pour cent, GPT-5-Mini 65, Claude Sonnet 4.5 58 a 61**. Le factuel est mieux code que l'attitudinal par tout le monde. Par categorie, l'ecart est enorme : « aucune de ces categories » 88 a 93 pour cent, economie 59 a 68, immigration 51 a 52, sante 45 a 56, education 26 a 31, **terrorisme 14 a 18**. Ajouter les demographies du repondant au prompt **ameliore une categorie de 33 points et en degrade d'autres de 11,8 points**, et produit davantage d'erreurs de format ; ajouter la tendance historique 2010 et 2021 apporte moins de 4 points et degrade ailleurs | tache de codage, pas de simulation ; la verite terrain est l'auto classification, elle meme faillible | premiere trace officielle de NORC sur les LLM. Deux points pour nous : le contexte demographique dans le prompt **aide parfois et nuit souvent**, ce qui recoupe l'effet de l'etiquette mesure en a31 ; et la difficulte est portee par la categorie, pas par le codeur | depot NORC | [CONFIRME] |
| L04-09 | Bursztyn, L., Haaland, I. K., Rover, N. et Roth, C. (2025), « The Social Desirability Atlas », NBER Working Paper 33920, juin 2025 | ou la desirabilite sociale mord elle, et de combien, quand on dispose d'une verite terrain individuelle | synthese restreinte aux etudes qui apparient declaration et registre au niveau de l'individu, six domaines : delinquance, economie, education, sante, moralite, vote | sans objet | taux de faux positifs et de faux negatifs par etude ; rapport « prevalence declaree sur prevalence reelle » | trois sources distinctes de biais posees en cadre : **couts materiels, image sociale, image de soi**. Sur les comportements indesirables, les faux negatifs sont « several orders of magnitude » au dessus des faux positifs, et l'inverse pour les comportements desirables. Fraude fiscale des entreprises en Ouganda : **faux negatif de 85 pour cent** ; fraude sociale, evasion fiscale et triche : declarations **plus de 50 pour cent en dessous** du reel. Vote, Norvege, registres administratifs sur cinq decennies : **96 pour cent d'accord** entre declaration et registre, sur declaration bien plus frequente que sous declaration ; experience de mode 2019 : **sur declaration 4,2 pour cent au telephone contre 2,8 pour cent sur le web**, sous declaration a 0,3 pour cent dans les deux modes. Reponse randomisee : la meta analyse de Lensvelt-Mulders donne **plus 11 points** de prevalence declaree, mais contre verite terrain individuelle le rapport estime sur reel est erratique et va jusqu'au negatif. Moins de 23 pour cent des repondants font confiance a l'anonymat de la RRT alors que plus de 79 pour cent declarent avoir compris les instructions | tout le corpus retenu porte sur des **comportements** verifiables ; les attitudes en sont absentes par construction, les auteurs le disent | **c'est le score continu par domaine que `a25` a fabrique a la main dans son S2, mais construit sur verite terrain individuelle.** Il remplace avantageusement les valeurs [HYPOTHESE] du tableau S2 de a28 section 1.5. Et il donne le cadre a trois sources qui tranche le cas LLM : un agent n'a ni cout materiel ni image sociale, il ne peut avoir qu'une image de soi installee par l'alignement | citation aval de 04-11 | [CONFIRME] |
| L04-10 | Bullock, J. G., Gerber, A. S., Hill, S. J. et Huber, G. A. (2015), « Partisan bias in factual beliefs about politics », *Quarterly Journal of Political Science* 10(4), 519 a 578 ; version NBER w19080 | l'ecart partisan sur les faits est il une croyance ou une declaration de loyaute | deux experiences : YouGov, 626 assignes, 419 analyses ; MTurk, 1 506 recrutes, groupes de 156 en controle, 534 payes pour la reponse exacte, 660 payes pour l'exacte et pour « je ne sais pas », 795 analyses | sans objet | ecart democrate contre republicain sur des questions factuelles, avec et sans incitation monetaire | payer pour la reponse exacte reduit l'ecart partisan de **55 a 60 pour cent** ; il ne reste **que 40 pour cent** de l'ecart initial. Ajouter un paiement pour « je ne sais pas » retire **20 points de plus** et laisse **environ 20 pour cent** de l'ecart de depart. Les auteurs en concluent que **la moitie de l'ecart restant vient de gens qui ignorent la reponse et savent qu'ils l'ignorent**. Sur un item, l'ecart passe de 0,9 a 0,4 puis a 0,2 point de pourcentage. Reductions de 56 pour cent des 10 cents, effets non monotones selon le montant | echantillons YouGov et MTurk ; incitations faibles ; ne dit rien des attitudes, seulement des faits verifiables | c'est l'ampleur de la « declaration de loyaute » : **la moitie a 80 pour cent de ce qu'on prend pour une croyance partisane est un acte d'expression**. C'est le pont demande : un humain qui joue son groupe produit une reponse qui n'est pas sa croyance, exactement comme un agent conditionne par une etiquette | citation aval, litterature de l'expressive responding | [CONFIRME] |
| L04-11 | Prior, M., Sood, G. et Khanna, K. (2015), « You cannot be serious: the impact of accuracy incentives on partisan bias in reports of economic perceptions », *QJPS* 10(4), 489 a 518 | meme question sur les perceptions economiques | deux enquetes sur echantillons nationalement representatifs | sans objet | ecart partisan sur les conditions economiques, avec incitation monetaire et avec appel a l'exactitude a l'ecran | les deux traitements reduisent significativement l'ecart partisan. Formulation des auteurs : **« Many partisans interpret factual questions about economic conditions as opinion questions, unless motivated to see them otherwise »**, et les conditions d'enquete ordinaires livrent « a mix of what partisans know about the economy, and what they would like to be true » | texte integral sous paywall nowpublishers, refus 403 le 8 septembre 2026 ; l'ampleur exacte de la reduction n'a pas ete lue | replique L04-10 sur un autre objet. La phrase clef pour nous : le repondant humain **change de regime de reponse** selon ce qu'il croit qu'on lui demande, ce qui est exactement le mecanisme mesure chez GPT-4 par 04-32 | citation aval | [PROBABLE] |
| L04-12 | Schaffner, B. F. et Luks, S. (2018), « Misinformation or expressive responding? What an inauguration crowd can tell us about the source of political misinformation in surveys », *POQ* 82(1), 135 a 147 | les fausses croyances partisanes sont elles crues ou declarees | enquete americaine, deux photographies de foules d'investiture, Trump 2017 et Obama 2009 | sans objet | part repondant faux a une question dont la reponse est visuellement evidente | **« We find clear evidence of expressive responding »**, et le comportement est **plus frequent chez les partisans les plus interesses par la politique** | non OA, pourcentages exacts non lus ; item unique | l'existence meme du phenomene est etablie sur un item ou aucune croyance sincere n'est possible. Aucun chiffre n'est repris ici | citation aval | [PROBABLE] |
| L04-13 | Graham, M. H. (2022), « The Big Lie: expressive responding and misperceptions in the United States », *Journal of Experimental Political Science* | l'adhesion republicaine aux fausses croyances electorales de 2020 est elle expressive | enquetes bien dimensionnees de republicains et d'independants | sans objet | effet de traitements encourageant l'exactitude | **les traitements d'exactitude sont inefficaces et « can in some cases even backfire »** ; l'auteur conclut que l'adhesion est sincerement tenue | un seul objet, tres charge ; pas de verite terrain individuelle | contredit L04-10 et L04-12 sur le meme mecanisme. Voir « ce qui se contredit » | citation aval | [PROBABLE] |
| L04-14 | Malka, A. et Adelman, M. (2022), « Expressive survey responding: a closer look at the evidence and its implications for American democracy », *Perspectives on Politics* 20(4), 1198 a 1209 | que vaut au juste la preuve de la reponse expressive | revue de la litterature et des commentaires | sans objet | sans objet | deux conclusions : **« evidence for insincere expressive responding on divisive political matters is limited and ambiguous »** ; et quand une manipulation reduit la declaration de croyances congruentes, c'est souvent parce que ces croyances sont **« flexible and interchangeable ways of justifying the largely stable allegiances that guide political behavior »**. Les auteurs proposent de traiter la valeur expressive comme un trait central du contexte politique americain et non comme un artefact de methode | revue argumentee, pas de meta analyse ; texte integral non atteint, Cambridge en erreur 500 et 403 le 8 septembre 2026 | **avertissement direct sur le pont que nous voulons construire.** Si l'expressive responding est « la vraie attitude, exprimee par un autre moyen », alors l'analogie « humain qui joue son groupe egale agent a etiquette » perd son tranchant : ce n'est pas de la simulation, c'est de l'allegeance | citation aval | [PROBABLE] |
| L04-15 | Cohen, G. L. (2003), « Party over policy: the dominating impact of group influence on political beliefs », *JPSP* 85(5), 808 a 822 | de quoi depend l'attitude declaree sur une politique publique | quatre etudes experimentales, participants americains | sans objet | attitude declaree selon la position attribuee au parti, contenu de la politique tenu constant | **l'attitude depend « almost exclusively upon the stated position of one's political party »**, effet qui ecrase le contenu objectif de la politique et l'ideologie declaree du participant, y compris sous traitement attentif ; le mecanisme passe par un deplacement des qualites factuelles supposees et des connotations morales attribuees a la politique. Et : **les participants nient avoir ete influences par leur groupe**, tout en pensant que les autres, surtout leurs adversaires, le seraient | echantillons etudiants et experimentaux, annees 2000 | c'est la formulation la plus nette du pont. Un humain a qui l'on donne une etiquette de groupe repond **comme son groupe est cense repondre**, sans le savoir. Un agent conditionne par une etiquette fait la meme substitution, mesuree chez nous en a31, rapport 4,45 avec etiquette contre 0,44 sans | citation amont depuis l'expressive responding | [PROBABLE] |
| L04-16 | Barber, M. et Pope, J. C. (2019), « Does party trump ideology? Disentangling party and ideology in America », *APSR* 113(1), 38 a 54 | quand parti et ideologie divergent, laquelle commande la reponse | enquete americaine, enonces de politique reellement tenus par Trump, les uns liberaux les autres conservateurs | sans objet | acceptation du signal partisan selon le niveau de connaissance et l'auto description ideologique | les repondants a faible connaissance, les republicains forts, les approbateurs de Trump **et les personnes qui se declarent conservatrices** sont les plus enclins a suivre le signal, **dans la direction liberale comme dans la direction conservatrice**. Conclusion des auteurs : **« group loyalty is the stronger motivator of opinion than are any ideological principles »**, et « their claims to being a self-defined conservative are suspect » | un seul emetteur de signal, une periode particuliere | seconde jambe du pont, et elle porte sur `polviews`, qui est un de nos items. Une etiquette ideologique auto declaree ne predit pas une position, elle predit **une disposition a suivre le groupe**. C'est exactement ce que fait un agent a qui l'on donne `polviews` dans son persona | citation amont | [PROBABLE] |
| L04-17 | Kahan, D. M., Peters, E., Dawson, E. C. et Slovic, P. (2017), « Motivated numeracy and enlightened self-government », *Behavioural Public Policy* 1(1), 54 a 86 | la competence protege t elle du raisonnement identitaire | experience, meme jeu de donnees presente comme une etude de creme dermatologique ou comme une etude d'interdiction des armes | sans objet | exactitude de l'inference causale selon la numeratie et selon le cadrage politique | sous cadrage neutre, les plus numerates font nettement mieux ; sous cadrage politique, les reponses se polarisent et deviennent **moins** exactes, et **la polarisation ne s'attenue pas chez les plus numerates, elle augmente** | echantillon en ligne, une seule tache ; replications contestees | c'est le mecanisme de la cognition protectrice d'identite : la capacite est **mise au service** de la conformite au groupe. Transpose chez nous : plus un agent est capable, plus il peut produire la reponse typique de l'etiquette. Cela predit que le modele plus gros de l'option C d'`ARBITRAGE.md` **aggravera** la substitution personne vers groupe, et non l'inverse | citation amont | [PROBABLE] |
| L04-18 | Oceno, M. (2025), « How social desirability bias impacts the expression of emotions », *Political Science Research and Methods* 13(4), 966 a 980, DOI 10.1017/psrm.2025.10016 | l'expression des emotions politiques est elle biaisee par le mode, et de la meme facon a gauche et a droite | ANES 2012 (face a face n = 2 054, web n = 3 860) et ANES 2016 (face a face n = 1 180, web n = 3 090) ; colere, peur, espoir, fierte envers les candidats | MCO avec controles de genre, race, ethnicite, age, education, revenu, interet et connaissance politiques | difference de niveau declare entre modes, par parti | **emotions negatives, meme sens dans les deux camps** : sur le web, 2012, democrates plus 6 points de colere et plus 5 de peur, republicains plus 8 et plus 12 ; 2016, democrates plus 10 et plus 12, republicains plus 6 et plus 6, tous p < 0,01 au moins. **Emotions positives, sens oppose selon le camp et selon l'annee** : en 2012 les democrates declarent plus d'espoir (plus 6) et de fierte (plus 5) envers Obama **en face a face** ; en 2016 les republicains declarent plus d'espoir (plus 6) et de fierte (plus 8) envers Trump **sur le web**. Formulation des auteurs : **« Republicans' positive emotions in 2016 mirror, in reverse, those of Democrats in 2012 »** | composition des echantillons differente entre modes, selection et mesure non separees ; deux elections | **la reponse la plus nette a la question « la desirabilite est elle la meme a gauche et a droite ».** Non. Le pole desirable d'un item positif **change de camp selon l'objet et selon la date**. Consequence directe pour `a25` : un pole de desirabilite unique par item, valable pour toute la population, est mal specifie ; la table `DESIRABILITE` de `a25_commun.py` devrait etre indexee par item **et par camp** | citation aval de 04-11 | [CONFIRME] |
| L04-19 | Gibson, J. L. et Sutherland, J. L. (2023), « Keeping your mouth shut: spiraling self-censorship in the United States », *Political Science Quarterly* 138(3), 361 a 376 | qui se tait, et est ce le meme camp qu'avant | series americaines de 1954 a 2020 | sans objet | part declarant ne pas se sentir libre d'exprimer ses opinions | la part a **triple** depuis le maccarthysme ; **plus de quatre personnes sur dix** s'auto censurent en 2020. **« Conservatives report engaging in more self-censorship than liberals »**, mais le motif ne se retrouve pas en opposant republicains et democrates. Le moteur est le micro environnement, la crainte d'etre isole de ses proches, pas la repression percue de l'Etat, ni l'opposition aux libertes civiles, sans relation | texte integral non atteint, OUP en 403 le 8 septembre 2026 ; les series de 1954 a 2019 ne sont pas parfaitement comparables | asymetrie mesuree entre gauche et droite, sur l'auto censure declaree. C'est un candidat de moderateur pour la these : si le camp conservateur se tait plus, une enquete de reference sous estime plus la droite que la gauche, et une simulation entrainee dessus herite d'une droite deja rabotee. A rapprocher de a30, ou la gauche simulee devient unanime | citation aval | [PROBABLE] |
| L04-20 | Crandall, C. S., Eshleman, A. et O'Brien, L. (2002), « Social norms and the expression and suppression of prejudice: the struggle for internalization », *JPSP* 82(3), 359 a 378 | l'expression du prejuge suit elle la norme, cible par cible | sept etudes, **N = 1 504**, **105 groupes sociaux** cibles | theorie des normes de groupe de Sherif | correlation entre approbation sociale de l'expression du prejuge envers un groupe et prejuge exprime envers ce groupe | **« The public expression of prejudice toward 105 social groups was very highly correlated with social approval of that expression »** ; les repondants suivent la norme aussi bien pour exprimer un prejuge que pour evaluer des scenarios de discrimination et reagir a des blagues hostiles. Les echelles de « suppression » mesurent en fait le suivi des normes, pas un engagement personnel : les hauts suppresseurs sont des **suiveurs de normes** et sont plus sensibles aux deplacements de normes locales | echantillons etudiants, annees 1990 ; la valeur exacte du r n'a pas ete lue dans le texte, seul l'abstract a ete atteint | c'est le modele de ce que serait une **ampleur de desirabilite par item**, mesuree directement plutot que deduite : demander a des humains le degre d'acceptabilite de chaque reponse. Faisable chez nous sur nos 149 items, y compris en le demandant a des humains recrutes a cout zero, ou en le mesurant sur le modele lui meme | citation amont | [PROBABLE] |
| L04-21 | Engelhardt, A. M. (2021), « Observational equivalence in explaining attitude change: have white racial attitudes genuinely changed? », *AJPS* 65(4), 968 a 984 | le mouvement recent des attitudes raciales blanches est il reel ou declaratif | panels americains, echelle de ressentiment racial | analyse factorielle confirmatoire multigroupe, cadre d'invariance de mesure | test de quatre explications observationnellement equivalentes : changement reel, desirabilite, reponse expressive partisane, derive de l'instrument | **le changement est reel.** L'invariance de mesure tient, ce qui « indicates social desirability pressures have not changed how Whites answer at least one racial attitude measure » et « suggests partisan expressive responding may have limits » | un seul instrument, une seule population, methode indirecte | resultat negatif majeur sur le domaine racial, qui est le domaine de quatre de nos douze items sensibles (`spkrac/y`, `natrace/y`) et de `racdif1` a `racdif4`. **A citer chaque fois que nous attribuons un ecart racial a la desirabilite** | citation aval | [PROBABLE] |
| L04-22 | Magalhaes, P. C. et Aarslew, L. F. (2025), « Survey measures of democratic attitudes and social desirability bias », *Political Science Research and Methods* | le soutien declare a la democratie est il gonfle par la desirabilite | module Democratie de l'European Social Survey, jusqu'a **24 pays**, variation de mode auto administre contre face a face ; plus une double experience de liste | sans objet | ecart entre modes, et estimation par experience de liste d'une attitude anti democratique | **« we find no evidence that SDB inflates survey measures of democratic attitudes »**, sur trois etudes | pas de verite terrain individuelle ; les items democratiques ne sont peut etre pas percus comme sensibles | resultat negatif de grande envergure, sur des items d'attitude, avec les deux methodes que nous employons. **A ranger avec Coppock 04-30, Lax 04-22, AAPOR 04-31 et Engelhardt L04-21** : la liste des attitudes politiques ou l'on **ne trouve pas** de desirabilite s'allonge | citation aval de 04-11 | [PROBABLE] |
| L04-23 | Kaftan, L. (2024), « Lip service to liberal democracy in Western Europe? », *Political Behavior* | meme question, autre dispositif | **14 000 repondants** YouGov, Royaume Uni, France, Allemagne, Italie | experience de liste | ecart entre soutien declare et soutien estime indirectement | **les repondants ne se sentent pas contraints de sur declarer leur soutien a la democratie** ; en revanche ce qu'ils entendent par democratie ne recouvre que des conceptions minimales | un seul construit ; l'experience de liste a une puissance limitee | troisieme resultat negatif independant sur le meme objet. Le probleme n'est pas que les gens mentent, c'est qu'ils ne repondent pas a la question qu'on croit poser | citation aval | [PROBABLE] |
| L04-24 | Valentim, V. (2024), *The Normalization of the Radical Right: A Norms Theory of Political Supply and Demand*, Oxford University Press ; et Valentim, V. (2024), « Norms of democracy, staged democrats, and supply of exclusionary ideology », *Journal of Politics* | que se passe t il quand la norme qui faisait taire un camp cede | comportements electoraux compares aux attitudes en Europe de l'Ouest ; pour l'article, referendums suisses comme revelateurs de preferences sinceres, plus sondages et positions de partis | modele de normes appliquee a l'offre et a la demande politiques | evolution du vote radical par rapport a l'evolution des attitudes ; reaction des partis aux resultats de referendum | le comportement radical de droite augmente vite alors que les attitudes bougent lentement, parce que des individus qui tenaient deja ces vues n'agissaient pas, les croyant socialement inacceptables. Article : quand un referendum revele que les positions de l'extreme droite sont plus populaires qu'attendu, ces partis **deviennent plus exclusifs** ; les « staged democrats » ne sont pas un rempart, et **« attitudes only prevent illiberal policy if they are sincerely held »** | mesures aggregees, pas de verite terrain individuelle ; contexte europeen | c'est Kuran (04-23 de la table initiale) rendu mesurable, et c'est **asymetrique par camp** : l'objet cache est ici a droite. Pour nous, c'est l'argument de la consequence : ce que la simulation efface n'est pas du bruit, c'est ce qui bascule | citation aval de 04-11 | [PROBABLE] |
| L04-25 | Ye, C., Fulton, J. et Tourangeau, R. (2011), « More positive or more extreme? A meta-analysis of mode differences in response choice », *POQ* 75(2), 349 a 365, DOI 10.1093/poq/nfr009 | le telephone rend il les reponses plus extremes ou plus positives | **18 comparaisons experimentales** entre telephone et un autre mode | meta analyse | part de reponses extremes positives et extremes negatives | **les repondants au telephone donnent significativement plus de reponses extremement positives, mais pas plus de reponses extremement negatives** ; les auteurs relient cette asymetrie a la presence de l'enqueteur et a l'effet MUM, la reticence a annoncer une mauvaise nouvelle | 18 comparaisons seulement ; texte integral non lu, abstract seul | **la contre hypothese qu'il faut opposer a `a25` sur les items ordinaux.** Ce que le mode deplace, sur une echelle, ce n'est pas « vers le pole desirable », c'est « vers l'extremite positive ». Cela reinterprete les 18 et 14 points de satisfaction du panel Pew (04-15) et les poles retenus pour `happy`, `satfin`, `satjob`, `health` | citation amont depuis 04-03 | [PROBABLE] |
| L04-26 | Kibuchi, E., Sturgis, P. et al. (2024), « The efficacy of propensity score matching for separating selection and measurement effects across different survey modes », *Journal of the Royal Statistical Society Series A* | peut on separer selection et mesure entre modes par appariement | enquetes paralleles face a face et en ligne | appariement par score de propension sur les demographies standard | ecarts d'estimation apres appariement | **de gros ecarts subsistent apres appariement** ; et surtout, **des ecarts subsistent entre deux enquetes conduites dans le meme mode en ligne**, ou toute difference de mesure est exclue a priori. Conclusion : l'appariement a « substantial limitations » | deux enquetes, contexte britannique | avertissement methodologique lourd. Il vaut pour NORC 04-18 comme pour nous : un ecart entre deux populations sur les memes items **ne se ramene pas** a un effet de mesure par appariement demographique. C'est aussi une borne sur ce que a30 et a31 peuvent conclure de leur appariement demographique | citation aval de 04-11 | [PROBABLE] |
| L04-27 | Zierahn, K., Cachero, C., Korhonen, A. et al. (2026), « Personality without persons? A psychometric critique of Big Five testing in large language models », arXiv 2607.02325v2, 2 juillet 2026 | les inventaires de personnalite mesurent ils quelque chose chez un LLM | **N = 264 modeles**, **50 familles**, cinq inventaires Big Five candidats | 264 modeles, dont paires socle contre instruit | validite de contenu, variance inter modele, structure factorielle | les items adaptes aux LLM atteignent une validite de contenu acceptable, **les items humains d'origine non** ; la variance inter modele ne represente que **7 a 17 pour cent** de la variance totale ; la structure a cinq facteurs ne se reproduit pas, **quatre facettes sur cinq s'effondrent en une seule, r >= 0,90** ; et, point decisif, **« comparisons between base and instruction-tuned variants suggest that alignment training shifts Big Five scores toward socially desirable profiles »** | comparaison socle contre instruit sur un sous ensemble, pas une ablation controlee ; instrument reecrit | **la reponse publiee a la question ouverte n. 3 de `a25` et a la derniere ligne d'`ARBITRAGE.md`** : la desirabilite d'un LLM apparait a l'etape d'alignement, pas dans le socle. Cela ne dispense pas de notre propre test socle contre aligne, cela lui donne une prediction dirigee. Cela relativise aussi 04-32 et 04-46 : ce qui est mesure par le Big Five chez un LLM n'est pas de la personnalite | arXiv | [PROBABLE] |
| L04-28 | Anonyme et al. (2025), « Social simulations with large language model risk utopian illusion », arXiv 2510.21180v1, 24 octobre 2025 | les societes simulees par LLM ressemblent elles aux societes reelles | conversations multi agents de type salon de discussion | **huit modeles, trois familles** | cinq dimensions linguistiques, biais socio cognitifs emergents | **« LLMs do not faithfully reproduce genuine human behavior but instead reflect overly idealized versions of it, shaped by the social desirability bias »** ; biais de role social, effet de primaute, biais de positivite ; il en resulte des **« 'Utopian' societies that lack the complexity and variability of real human interactions »** | interaction libre entre agents, pas d'items d'enquete ; pas de population humaine appariee ; analyse linguistique et non distributionnelle | **c'est la formulation publiee de la these que `a25` a fait tomber sur nos donnees.** Quelqu'un affirme deja « la simulation rend une societe presentable ». Il l'affirme sur des conversations, pas sur des reponses a des items sensibles mesures independamment, et sans population humaine de comparaison. Notre resultat negatif devient une contribution : sur les items du GSS classes sensibles au mode, la direction n'est pas celle la | arXiv | [PROBABLE] |
| L04-29 | Kinzinger, L. et Hartmann, J. (2026), « Synthetic personalities: how well can LLMs mimic individual respondents using socio-economic microdata? », arXiv 2606.04592v1, 3 juin 2026 | des jumeaux individuels construits sur des microdonnees de panel existantes sont ils fideles | Socio-Economic Panel allemand, **500 participants**, **183 questions retenues hors apprentissage**, **plus de 2,1 millions de reponses de jumeaux** | trois LLM a poids ouverts, grille 3 x 5 x 2 x 2 : profondeur d'information par quartile d'entropie de Shannon normalisee, deux methodes d'ancrage, deux modes de raisonnement | exactitude hors echantillon, correlation de rang apres transformation de Fisher | **exactitude de la meilleure cellule 78,8 pour cent, r = 0,590** ; la qualite croit avec la profondeur d'information mais avec des rendements decroissants au dela du quartile 75 pour cent ; remplacer un resume narratif de persona par **l'historique brut des reponses passees** ameliore l'exactitude dans toutes les cellules a profondeur maximale ; le mode « raisonnement » ameliore la correlation de rang sans bouger l'exactitude | pas de comparaison a un plancher humain test retest ; SOEP allemand, pas le GSS ; pas d'items sensibles isoles | c'est la comparaison la plus proche de nos conditions C2 et C3, et elle tranche le meme point : **l'historique de reponses bat la persona narrative**, ce qui est exactement l'ordre C3 devant C2 que nous mesurons. Le 78,8 pour cent donne une borne externe a nos chiffres d'exactitude | citation aval de 04-32 | [PROBABLE] |
| L04-30 | Miklian, J., Hoelscher, K. et Katsos, J. E. (2026), « Stochastic parrots or singing in harmony? Testing five leading LLMs for their ability to replicate a human survey with synthetic data », arXiv 2603.00059v3, 10 fevrier 2026 | des repondants synthetiques retrouvent ils les resultats contre intuitifs d'une enquete humaine | enquete humaine sur **420 developpeurs de la Silicon Valley**, plus donnees synthetiques | cinq modeles de pointe, dont GPT-5, Claude Sonnet 4.5, Gemini 2.5 Pro, DeepSeek 3.2 | comparaison des reponses et des conclusions | les agents produisent des resultats plausibles, plus replicables qu'attendu, mais **aucun ne retrouve les resultats contre intuitifs qui faisaient la valeur de l'enquete humaine** ; et **« deviations grouped together for all models, leaving the real data as the outlier »** | une seule enquete, population professionnelle etroite ; comparaison qualitative autant que quantitative | c'est le meme motif que notre contraste de groupe de a28 section 1.6, observe ailleurs : **les modeles se ressemblent entre eux plus qu'ils ne ressemblent aux humains**, et l'humain est l'exception. C'est une replication independante de l'argument, et un argument pour publier le contraste de groupe | citation aval de 04-32 | [PROBABLE] |
| L04-31 | Choi, E., Young, L. E. et Ferrara, E. (2026), « Overstating attitudes, ignoring networks: LLM biases in simulating misinformation susceptibility », arXiv 2602.04674v2, ICWSM | des repondants simules reproduisent ils la structure des associations humaines | trois enquetes en ligne comme reference, profils comprenant reseau, demographie, attitudes et comportements | LLM avec profils de participants | correspondance des distributions et recuperation des associations trait vers resultat | les distributions larges sont capturees et la correlation avec les humains est modeste, mais les modeles **surestiment systematiquement l'association entre croyance et partage** ; les modeles lineaires ajustes sur les reponses simulees ont une **variance expliquee nettement plus elevee** et donnent un poids disproportionne aux traits attitudinaux et comportementaux, **en ignorant largement les caracteristiques de reseau** | trois enquetes en ligne, un domaine ; pas de comparaison individuelle appariee | recoupe le resultat n. 2 de `ARBITRAGE.md` : la simulation n'efface pas au hasard, elle **sur ajuste ce qui est dans l'etiquette et ignore ce qui n'y est pas**. Ici l'oublie est le reseau social ; chez nous c'est la personne derriere le segment | citation aval de 04-32 | [PROBABLE] |
| L04-32 | Kozlowski, A. C. et Evans, J. A. (2025), « Simulating subjects: the promise and peril of artificial intelligence stand-ins for social agents and interactions », *Sociological Methodology* | quelles sont les limites structurelles de la simulation de sujets humains | revue de l'IA et de la science sociale computationnelle | sans objet | sans objet | six caracteristiques qui empechent une simulation realiste : **biais, uniformite, atemporalite, desincarnation, cultures linguistiques, intelligence etrangere** ; les auteurs plaident pour un programme methodologique continu et rappellent que la validation contre des donnees humaines reste indispensable | revue, aucune mesure propre | fournit le vocabulaire de cadrage. « Uniformite » est notre ecrasement de variance, « atemporalite » est le theme 07, « intelligence etrangere » est la formulation de `corpus/04` sur le regime de reponse substitue | citation aval de 04-11 | [PROBABLE] |
| L04-33 | Kazinnik, S. et Enriquez, J. R. (2026), « Sex, drugs, and LLMs: social desirability bias in language models », SSRN 6752998 | sans objet, non lu | | | | non lu, SSRN en 403 le 8 septembre 2026 | | titre exactement sur le theme, a recuperer avant toute revendication de nouveaute | citation aval | [NON LU] |
| L04-34 | Treglown, L. et Furnham, A. (2025), « AI, social desirability, and personality assessments: impression management in large language models », *Personality and Individual Differences* 244, 113563 | sans objet, non lu | | | | non lu, ScienceDirect en 403 le 8 septembre 2026 | | replication probable de 04-32 et 04-46 dans une revue de psychometrie | citation aval | [NON LU] |
| L04-35 | Wang, L. (2026), « Generative-agent modeling of protest mobilization and preference falsification with large language models », SSRN 7338838 | sans objet, non lu | | | | non lu, SSRN inaccessible | | **le titre revendique exactement la transposition de Kuran aux agents generatifs.** A recuperer en priorite : c'est le voisin le plus dangereux pour la revendication de nouveaute du point 5 de « ce que personne n'a fait » | citation aval | [NON LU] |
| L04-36 | Lee, H., Cho, M. et Kang, M. (2026), « Assessing and adjusting social desirability bias in self-reported surveys using large language models », *AMCIS 2026 TREOs* | un LLM peut il estimer la susceptibilite d'une reponse humaine a la desirabilite et la corriger | recherche en systemes d'information, protocole compare aux techniques de covariance avec echelles IM et SDE | LLM non precise dans le resume | estimation de la susceptibilite puis production d'estimations corrigees | resume seul : la proposition est d'utiliser le LLM comme **estimateur du biais chez l'humain**, en remplacement des echelles de desirabilite qui allongent le questionnaire | resume etendu de conference, pas d'article complet ; aucun chiffre | inversion utile du probleme, dans la lignee de 04-47 : le modele comme instrument de mesure de la desirabilite humaine. C'est une facon de construire notre score par item sans recruter personne | citation aval | [PROBABLE] |

---

## Comment ca fonctionne

### Un phenomene, trois moteurs, et un seul d'entre eux peut exister chez un agent

L'apport conceptuel le plus utile de cette lecture tient en une distinction que l'atlas de Bursztyn,
Haaland, Rover et Roth (L04-09) pose des sa deuxieme section : la reponse socialement desirable a
trois sources separables, les **couts materiels** quand avouer expose a une sanction, les
**preoccupations d'image sociale** quand la reponse sera jugee par autrui, et les **preoccupations
d'image de soi** quand avouer contredit l'idee qu'on se fait de soi. Cette taxonomie, qui prolonge
la distinction auto duperie contre gestion de l'impression de Paulhus (04-02), tranche notre cas
d'un coup : un agent de langage n'a **aucun cout materiel** et **aucune image sociale**, puisqu'il
n'a rien a perdre et personne devant qui perdre la face. Si un ecart subsiste, il ne peut relever
que de la troisieme source, et cette troisieme source n'est pas psychologique chez lui, elle est
installee. Zierahn et ses coauteurs (L04-27) la localisent : en comparant des variantes socle et des
variantes instruites de 264 modeles, ils concluent que **l'entrainement d'alignement deplace les
scores vers des profils socialement desirables**. La chaine est donc : preference humaine agregee,
puis modele de recompense (04-45), puis profil desirable a la sortie. Ce n'est pas une imitation du
repondant humain, c'est la sedimentation de la moyenne de ce que des annotateurs humains ont
prefere lire.

Cela a une consequence immediate et rarement enoncee : les leviers qui reduisent la desirabilite
humaine et les leviers qui reduisent celle d'un modele ne sont **pas les memes**. L'anonymat, qui
agit sur les deux premieres sources, n'a aucune prise sur la troisieme. L'atlas le dit d'ailleurs
pour les humains eux memes : trop insister sur l'anonymat « might signal that a question is
particularly sensitive », et une garantie d'anonymat est au fond du « cheap talk ». Coffman, Coffman
et Ericson (04-21) l'avaient deja montre empiriquement, en obtenant un voile efficace **alors meme
que la condition de reference offrait deja anonymat complet**. Rendre un prompt « prive » ne
fabriquera donc pas un agent sincere ; cela peut au contraire lui signaler que la question est
sensible, ce qui est exactement le declencheur d'evaluation mesure par Salecha et al. (04-32). Cela
explique aussi, sans avoir besoin d'une hypothese sur Qwen3-4B, pourquoi les preambules de sincerite
de Chapala, Mironov et Deng (04-35) « n'apportent aucun benefice systematique » : ils s'adressent a
une source que le modele n'a pas.

### L'ampleur par item existe, mais elle vit dans les rapports methodologiques

`a25` conclut, dans son point 1 de « ce que je n'ai pas pu verifier », que « NORC ne publie pas
d'ampleur par item » et qu'en consequence la version continue de la prediction « n'est pas testable
en l'etat ». C'est exact pour la note de sensibilite au mode de 2022, qui ne donne que trois classes.
C'est faux pour NORC dans son ensemble. Le catalogue des rapports methodologiques du GSS contient
au moins quatre pieces qui donnent une ampleur continue, item par item, sur des items qui sont
dans nos 149.

MR099 (L04-01) est la plus directe. Smith et Dennis comparent le GSS 2002 en face a face au panel
web de Knowledge Networks sur les **17 items de depenses**, poses en premier des deux cotes pour
neutraliser le contexte. Ils obtiennent un ecart moyen de **3,9 points** avec seulement 6
comparaisons significatives sur 17, mais une queue lourde : les depenses pour les Noirs bougent de
**13,8 points**, le welfare de 9,7, l'aide etrangere de 8,5, la toxicomanie de 7,0, les grandes
villes de 6,3. Ce n'est pas anecdotique pour nous : `natrace/y` est l'un de nos douze items
sensibles, et c'est celui ou l'ampleur mesuree est la plus grande de sa famille.

MR141 (L04-03) donne la seconde ampleur, et elle est plus grande que la premiere. Sur le GSS 2021 et
2022, quand la modalite « volontaire » devient visible a l'ecran, la part qui la choisit va de
**0,8 pour cent a 62,8 pour cent selon l'item**. Sur `aged`, la modalite « ca depend » attire 63,9
pour cent des repondants et fait chuter « bonne idee » de 66,9 a 25,5 pour cent. Ce n'est pas de la
desirabilite, c'est de la conception d'item, mais l'effet depasse d'un ordre de grandeur tous les
effets de mode du theme. C'est le prolongement direct de Berinsky (04-19) : le « je ne sais pas »
n'est pas une absence de reponse, c'est une option, et sa disponibilite reorganise la distribution
entiere.

MR010 (L04-06) donne une troisieme ampleur, sur l'item precis qui porte le resultat de la section 4
de `a25`. Sur `polhitok` et `polabuse`, **86 pour cent** des repondants qui disent « non » a la
question absolue approuvent ensuite au moins une situation concrete, avec 1,52 situation approuvee
en moyenne, quand seuls **1,1 pour cent** des « oui » ne trouvent aucune situation acceptable.
Smith en tire une phrase qui vaut pour tout le theme : « In answering survey questions, people do
not always mean what they say ». Et il ajoute que cette erreur est **correlee** et non aleatoire, ce
qui « undermines the assumption that the measurement error attenuates relationships » et se
retrouve d'une vague a l'autre, donc echappe a une correction par test retest.

Enfin, le versant comportemental de l'ampleur est desormais rassemble par l'atlas (L04-09), avec un
critere d'inclusion severe : uniquement les etudes qui apparient declaration et registre **au niveau
de l'individu**. Le resultat est une asymetrie propre : sur les comportements indesirables, les faux
negatifs depassent les faux positifs de plusieurs ordres de grandeur ; sur les comportements
desirables, c'est l'inverse. La fraude fiscale des entreprises culmine a **85 pour cent de faux
negatifs**. Cette asymetrie est exactement celle que Kreuter, Presser et Tourangeau (04-11) avaient
trouvee entre modes sur les items indesirables et non sur les items flatteurs.

### La direction n'est pas une propriete de l'item, c'est une propriete du couple item et camp

C'est le point ou la lecture change quelque chose au protocole. `a25` fixe, item par item, un pole
socialement desirable unique, valable pour toute la population. Oceno (L04-18) montre sur l'ANES
2012 et 2016 que cette hypothese est fausse pour les items evaluatifs. Sur les emotions negatives,
les deux camps vont dans le meme sens : tout le monde declare plus de colere et plus de peur en
ligne, de 5 a 12 points selon le camp et l'annee. Mais sur les emotions positives, le sens
**s'inverse selon le camp et selon l'objet** : les democrates declarent plus d'espoir et de fierte
envers Obama **en face a face** en 2012, les republicains declarent plus d'espoir et de fierte
envers Trump **en ligne** en 2016. L'auteur le formule ainsi : « Republicans' positive emotions in
2016 mirror, in reverse, those of Democrats in 2012 ». Autrement dit, ce qui etait desirable a dire
a un enqueteur en 2012 etait devenu honteux en 2016, pour l'autre camp, sur le meme type d'item.

Crandall, Eshleman et O'Brien (L04-20) donnent la loi generale derriere ce fait : sur **105 groupes
sociaux**, l'expression publique du prejuge est « very highly correlated » avec l'approbation
sociale de cette expression. La desirabilite n'est pas un trait du repondant ni une propriete du
theme, c'est une **fonction de la cible**, et cette fonction est estimable. Et Gibson et Sutherland
(L04-19) ajoutent l'asymetrie de niveau : plus de quatre Americains sur dix s'auto censurent en
2020, contre un sur sept dans les annees 1950, et « conservatives report engaging in more
self-censorship than liberals », le motif disparaissant si l'on remplace l'ideologie par le parti.
Valentim (L04-24) montre enfin ce que produit la levee de la norme : le comportement radical de
droite explose sans que les attitudes bougent, parce que des gens qui pensaient deja ainsi cessent
de se taire.

Cela recompose l'analyse de a30 et a31. Si la droite se tait davantage dans les enquetes, alors la
population de reference du GSS contient deja une droite rabotee, et une simulation entrainee dessus
herite de ce rabotage avant d'y ajouter le sien. Et le fait mesure a30, « la gauche est le camp le
moins varie, et la simulation avec etiquette la rend unanime », se lit alors sur deux couches et non
une.

### Le pont avec notre these : jouer son groupe, et ne pas le savoir

La question posee dans la commande est la bonne : un humain qui « joue son groupe » ressemble t il a
un agent a etiquette ? La litterature repond oui, et elle chiffre.

Cohen (L04-15) etablit la forme forte : l'attitude declaree sur une politique publique depend
« almost exclusively upon the stated position of one's political party », en ecrasant a la fois le
contenu objectif de la politique et l'ideologie declaree du participant, y compris sous traitement
attentif. Le mecanisme n'est pas un simple mensonge : le participant **reconstruit les faits** qu'il
attribue a la politique et **ses connotations morales**. Et il **nie** avoir ete influence, tout en
pensant que ses adversaires le seraient. Barber et Pope (L04-16) etendent le resultat au cas ou
parti et ideologie divergent : ceux qui se declarent conservateurs suivent le signal du chef dans la
direction liberale comme dans la direction conservatrice, ce qui conduit les auteurs a ecrire que
« their claims to being a self-defined conservative are suspect ». Une etiquette ideologique
auto declaree ne code donc pas une position, elle code une **disposition a suivre**.

C'est precisement la structure de nos agents avec etiquette. Un agent a qui l'on donne `polviews`
produit la reponse typique du segment ; a31 mesure que ses fausses raretes sont les raretes typiques
du segment et non celles de la personne, rapport 4,45 avec etiquette contre 0,44 sans. La
correspondance est reelle et elle est le meilleur argument narratif du projet.

Elle a cependant une limite, et il faut la porter avec le reste. Bullock, Gerber, Hill et Huber
(L04-10) montrent que payer pour l'exactitude retire 55 a 60 pour cent de l'ecart partisan sur des
faits, et que payer aussi pour « je ne sais pas » en retire 20 de plus, laissant environ **20 pour
cent** de l'ecart initial ; ils en concluent que la moitie du residu vient de gens qui ignorent la
reponse et le savent. Prior, Sood et Khanna (L04-11) obtiennent un resultat de meme nature, et
formulent le point le plus important : « many partisans interpret factual questions about economic
conditions as opinion questions, unless motivated to see them otherwise ». Le repondant humain
**change de regime de reponse** selon la lecture qu'il fait de la demande, exactement comme GPT-4
bascule vers le pole desirable des qu'il infere qu'il passe un test (04-32).

Kahan et ses coauteurs (L04-17) ajoutent la torsion qui compte pour notre feuille de route : sous
cadrage politique, la polarisation **ne s'attenue pas** chez les plus competents, elle **augmente**.
La capacite est mise au service de la conformite. Transposee, cette regularite predit que le modele
plus gros de l'option C d'`ARBITRAGE.md` **aggravera** la substitution de la personne par le groupe
au lieu de la corriger. C'est une prediction dirigee, gratuite, et falsifiable des la nuit de calcul
prevue.

### Ce que les modeles font des biais de reponse humains, mis a jour

La table initiale etablissait deja que les modeles ne reproduisent pas les biais de conception
d'enquete (04-39, 04-40, 04-41, 04-42, 04-43). Cette lecture ajoute quatre elements.

D'abord, l'origine du profil desirable est localisee : l'alignement, pas le socle (L04-27). Ensuite,
la nature de l'instrument est disqualifiee : chez 264 modeles, quatre facettes du Big Five sur cinq
s'effondrent en une seule avec r >= 0,90, et la variance inter modele ne represente que 7 a 17 pour
cent du total. Ce qui est mesure par 04-32, 04-33 et 04-46 n'est donc pas de la personnalite au sens
humain, c'est un axe unique d'agrement. Troisiemement, la these « la simulation rend une societe
presentable » est deja publiee, sous le nom d'illusion utopique (L04-28), sur des conversations
multi agents : biais de positivite, biais de role social, effet de primaute, et des societes qui
« lack the complexity and variability of real human interactions ». Enfin, deux travaux mesurent
sur des enquetes reelles la forme du derapage, et elle est la meme dans les deux cas : les modeles
**sur ajustent ce qui est dans le profil** et **ignorent ce qui n'y est pas** (L04-31, ou le poids
va aux attitudes et le reseau social disparait), et ils **se ressemblent entre eux plus qu'ils ne
ressemblent aux humains**, l'humain devenant l'observation aberrante (L04-30). Ce dernier motif est
notre contraste de groupe de a28 section 1.6, retrouve independamment sur une autre enquete.

Un cinquieme element vient de NORC lui meme (L04-08) : dans le codage des reponses ouvertes du GSS
2024, ajouter les demographies du repondant au prompt gagne 33 points sur une categorie et en perd
11,8 sur une autre, tout en produisant plus d'erreurs de format. Le contexte demographique n'est pas
un enrichissement neutre, il est un pari dont le signe depend de la cible. C'est le meme signe que
notre a31.

---

## Ce qui se contredit

**1. La presence d'un tiers : facteur decisif ou effet nul.** Gnambs et Kaspar (04-14) trouvent que
le moderateur le plus puissant de la declaration de comportements honteux est la situation de
passation, Omega = 1,61 seul contre 1,18 accompagne, ce qui explique la moitie de la variance
residuelle. Smith (L04-02), sur le GSS, ne trouve **aucune** difference significative associee a la
presence du conjoint, 3 associations sur 13 pour la presence de quelqu'un, et une seule qui survit
aux controles. **La variable qui explique** : Gnambs mesure des comportements stigmatises declares
en auto administration, Smith mesure des attitudes dites a voix haute a un enqueteur. C'est la meme
frontiere que 04-14 contre 04-14b, faits contre traits, et elle se generalise : la desirabilite est
un phenomene de **comportement verifiable**, pas d'attitude.

**2. La desirabilite sur les attitudes politiques : partout ou nulle part.** D'un cote, un corpus
etabli sur la race (04-06, 04-19, 04-21) et sur l'immigration (04-27). De l'autre, une serie de
resultats negatifs desormais longue et bien dimensionnee : Coppock sur le vote Trump (04-30), Lax,
Phillips et Stollwerk sur le mariage entre personnes de meme sexe (04-22), les deux rapports AAPOR
(04-29, 04-31), Engelhardt sur le ressentiment racial avec invariance de mesure (L04-21),
Magalhaes et Aarslew sur 24 pays (L04-22), Kaftan sur 14 000 repondants (L04-23). **La variable qui
explique**, et c'est visible dans le critere d'inclusion de l'atlas (L04-09) : les etudes qui
trouvent de la desirabilite disposent d'une **verite terrain individuelle** et portent sur des
**comportements** ; celles qui n'en trouvent pas portent sur des **attitudes** sans verite terrain.
Il reste possible que les attitudes soient aussi falsifiees et que nous n'ayons simplement aucun
moyen de le savoir. Mais la charge de la preuve n'est pas de notre cote, et la section 4 de `a25`,
qui echoue a trouver une direction sur des items d'attitude du GSS, se range **avec** la majorite de
la litterature et non contre elle. C'est une reformulation qui vaut la peine d'etre ecrite ainsi.

**3. La reponse expressive : reelle ou surestimee.** Schaffner et Luks (L04-12) trouvent une preuve
« claire » sur les photographies d'investiture, Bullock et al. (L04-10) et Prior et al. (L04-11)
retirent 55 a 80 pour cent de l'ecart partisan avec des incitations. Graham (L04-13) trouve, sur les
fausses croyances electorales de 2020, que les traitements d'exactitude sont inefficaces et parfois
contre productifs. Malka et Adelman (L04-14) concluent que la preuve est « limited and ambiguous ».
**La variable qui explique**, telle qu'elle ressort de Malka et Adelman : l'incitation ne separe pas
« mentir » et « cesser de justifier une allegeance ». Quand elle marche, c'est peut etre parce que
la croyance etait un moyen interchangeable de justifier une loyaute stable, pas parce qu'elle etait
un mensonge. Ce qui, pour nous, est une bonne nouvelle et une mauvaise : le pont avec l'agent a
etiquette tient mecaniquement, mais il ne prouve pas l'insincerite.

**4. La sur declaration de vote : 15,8 points ou 1,4 point.** Ansolabehere et Hersh (04-20) trouvent
15,8 points d'ecart entre vote declare et vote valide sur le CCES 2008, et 52 pour cent des non
votants qui declarent avoir vote. Kleven, rapporte par l'atlas (L04-09), trouve sur cinq decennies
d'enquetes norvegiennes appariees aux registres **96 pour cent d'accord**, et une experience de mode
qui donne 4,2 pour cent de sur declaration au telephone contre 2,8 pour cent sur le web, soit
**1,4 point d'ecart de mode**. MR021 (L04-07) donne pour le GSS environ 10 points au dessus des
resultats. **La variable qui explique** : la qualite de l'appariement. Le registre norvegien est
exhaustif, l'appariement Catalist du CCES ne l'est pas et produit ses propres erreurs, ce que les
auteurs du CCES reconnaissent. S'y ajoute, sur la comparaison CPS contre GSS, un artefact que MR021
identifie : le CPS utilise des **informants** pour les autres membres du menage, ce qui « probably
reduces the percent voting by lessening the social desirability bias ». Conclusion pour `a25` : le
pole « voted » retenu pour `vote16` reste defendable, mais l'ampleur associee dans le score S2 de
a28, 15,8 points, est la borne haute d'une plage qui commence a 1,4.

**5. Le pole desirable des items de depenses : NORC contre `a25`.** `a25` applique aux 17 items
`nat*` une regle uniforme, « too little » egale pole desirable, marquee [HYPOTHESE], et cette regle
porte 3 des 12 items sensibles. MR099 (L04-01) mesure la direction reelle : le GSS en face a face
donne **moins** de « trop » sur les 17 items et **plus** de « pas assez » sur 12 sur 17, ce qui est
coherent avec la regle. Mais Smith et Dennis refusent explicitement de l'interpreter ainsi :
**« these items are not about behaviors and it is not clear that being pro-spending is necessarily
the socially desirable response »**, en relevant qu'il existe une large majorite hostile a l'aide
etrangere et que le soutien aux depenses contre la toxicomanie correle avec des reponses punitives
et non avec des reponses genereuses. La regle uniforme de `a25` est donc **empiriquement soutenue et
theoriquement recusee par la meme source**. Ce point doit figurer dans le papier.

**6. La chute de la religiosite sur le web : desirabilite ou carte de reponse manquante.** La note
de mode de 2022 (04-18) classe `attend`, `pray`, `reborn`, `savesoul` comme sensibles au mode et
donne la direction, ce qui fonde quatre poles [CONFIRME] de `a25`. MR145 (L04-05), publie par NORC
en mars 2026, attribue une part des memes ecarts a un **stimulus differentiel** : l'ecran web
affichait la liste des religions, aucune carte n'etait remise en face a face. Et le web se revele
**plus stable dans le temps** que le face a face, ce qu'un effet de selection pur n'expliquerait
pas. **La variable qui explique** n'est pas tranchee par la source elle meme, qui ecrit qu'il est
« difficult to fully control for the effect ». Consequence : les quatre poles religieux de `a25`
devraient descendre de [CONFIRME] a [PROBABLE].

**7. L'extremite positive contre le pole desirable.** Ye, Fulton et Tourangeau (L04-25) trouvent sur
18 comparaisons que le telephone produit plus de reponses **extremement positives** mais pas plus de
reponses extremement negatives. C'est une explication concurrente et plus economique des 18 et 14
points de satisfaction observes par Pew (04-15), et des poles retenus par `a25` pour `happy`,
`satfin`, `satjob`, `health` et `life`. Sur une echelle ordinale, l'enqueteur ne pousse pas vers le
« bien vu », il pousse vers le haut. **Test de departage** : sur les items ou le pole desirable est
au **bas** de l'echelle, les deux hypotheses divergent.

**8. Le contraste de mode est il un effet de mesure.** Kibuchi, Sturgis et al. (L04-26) montrent que
l'appariement par score de propension ne separe pas selection et mesure, et que des ecarts
subsistent **entre deux enquetes conduites dans le meme mode**. C'est la meme reserve que NORC
formule sur sa propre note. Cela ne detruit pas `a25`, dont le contraste est calcule entre methodes
sur les **memes personnes**, mais cela interdit de presenter la liste NORC comme une liste
d'« items ou l'humain se surveille » ; c'est une liste d'items ou la distribution bouge avec le
mode, toutes causes confondues.

---

## Ce que ca permet de tester chez nous tout de suite

Aucun de ces tests ne demande d'appel de modele. Les couts sont donnes en temps de travail plus
temps de calcul, et supposent que rien d'existant n'est modifie.

**T1. Remplacer le score S2 fabrique par des ampleurs mesurees.** Le tableau S2 de a28 section 1.5
attribue une valeur en points par domaine, dont cinq entrees [HYPOTHESE]. Trois sources permettent
de le refaire sur mesure : les 17 valeurs par item de MR099 pour la famille `nat*`, le rapport
declare sur reel par domaine de l'atlas (L04-09) pour les comportements, et les 1,4 point de mode de
Kleven pour le vote. **Cout** : environ deux heures, aucune ecriture dans `data/`, une nouvelle
colonne dans `a28-t1-scores-items.csv`, puis neuf secondes de `a28`. **Gain** : la couverture de S2
passe de 5 des 12 items sensibles a au moins 8, et les valeurs cessent d'etre des transpositions.

**T2. Retester le sens de l'ecart avec le pole `nat*` inverse.** `a25` reconnait que trois des douze
items sensibles reposent sur la regle uniforme « too little ». MR099 documente que NORC lui meme
refuse cette lecture. **Cout** : un drapeau dans `a25_commun.py`, un rejeu de `a25_contrastes.py`,
soit neuf secondes plus une demi heure d'ecriture. **Gain** : une analyse de sensibilite au choix
des poles, qui est le point 4 de « ce que je n'ai pas pu verifier » de `a25` et l'objection
principale a sa section 4.

**T3. Le confondant de la modalite volontaire.** MR141 donne, pour une vingtaine d'items du GSS 2021
et 2022, la part de repondants qui choisissent la modalite volontaire quand elle est affichee, de
0,8 a 62,8 pour cent. Plusieurs de ces items appartiennent a nos 65 temoins negatifs. Test :
correler, item par item, l'ecart de distribution agent contre humain de `a25-par-item-condition.csv`
avec cette part. **Cout** : saisie manuelle de vingt valeurs et une correlation de rang, environ une
heure. **Gain** : si la correlation est forte, une part de l'ecart que `a25` attribue au modele
vient de ce que l'humain disposait d'une echappatoire que l'agent n'a jamais. C'est un test qui peut
faire tomber une partie du resultat, et c'est pour cela qu'il faut le faire.

**T4. Rejuger `polabuse` contre la version situationnelle.** MR010 etablit que 86 pour cent des
« non » a la question absolue approuvent au moins une situation concrete. Test : verifier si
l'archive de Stanford contient, pour les memes personnes, les items situationnels de la famille
`polhitok`, `polescap`, `polmurdr`, `polattak`, et recalculer l'erreur de C2 et C3 contre le profil
situationnel plutot que contre l'item absolu. **Cout** : une lecture de l'archive et un script de
comptage, environ deux heures. **Gain** : `polabuse/y` est l'item qui produit le chiffre le plus
spectaculaire de `a25`, 71 et 50 agents sur 150 contre 9 humains. Si le profil situationnel humain
est proche de ce que produisent les agents, la phrase « une simulation qui produit une population
plus dure » devient fausse et doit etre retiree.

**T5. Indexer la desirabilite par camp.** Oceno montre que le pole desirable d'un item evaluatif
s'inverse selon le camp. Test : recalculer la mesure de sens de `a25` separement pour les personnes
de gauche, du centre et de droite, en reutilisant le decoupage de a30. **Cout** : une boucle
supplementaire dans `a25_contrastes.py`, moins d'une heure et neuf secondes de calcul. **Gain** :
c'est le seul chemin par lequel la section 4 de `a25` peut encore produire un resultat. Une direction
nulle en moyenne peut cacher deux directions opposees qui s'annulent, ce qui est exactement le motif
mesure sur l'ANES.

**T6. La prediction de Zierahn sur socle contre aligne.** L04-27 predit que le profil desirable
apparait a l'alignement. Notre comparaison socle contre aligne, deja prevue en option C
d'`ARBITRAGE.md`, devient un test dirige et non exploratoire : si la substitution de la personne par
le groupe est presente dans le socle, L04-27 est contredit et le resultat est publiable comme tel.
**Cout** : la nuit de calcul deja budgetee, plus le rejeu de `a25` et `a28` dessus.

**T7. La prediction de Kahan sur le modele plus gros.** L04-17 predit que la capacite renforce la
conformite au groupe. Applique a nous : sur un modele plus gros, l'appariement des raretes avec
etiquette doit **baisser** encore par rapport a sans etiquette. **Cout** : nul en plus de T6,
c'est une hypothese preenregistree a ecrire avant le calcul.

**T8. Construire notre propre ampleur par item, a la Crandall.** L04-20 mesure l'acceptabilite
sociale de l'expression pour 105 cibles et la correle a l'expression. Rien n'interdit de produire la
meme chose pour nos 149 items, en faisant noter par plusieurs juges independants, ou par le modele
lui meme dans une passe separee, le degre d'acceptabilite de chaque modalite. **Cout** : une heure
pour deux codeurs humains sur les seuls items sensibles, comme le suggere deja la question ouverte
n. 6 de `a25` ; une passe de modele pour la version complete. **Gain** : c'est la seule facon
d'obtenir un score continu couvrant les 149 items, et c'est la reponse a la question ouverte n. 2 de
`a25`, moins couteuse que le recalcul des microdonnees du GSS 2022.

---

## Ce que personne n'a fait

La verification de `corpus/04` reste valable, avec quatre corrections et une addition.

**Ce qu'il ne faut plus revendiquer, en plus de la liste de `corpus/04`.**

1. « La simulation rend une societe presentable » est **publie** depuis octobre 2025 sous le nom
   d'illusion utopique (L04-28), sur des conversations multi agents. Notre resultat n'est pas de
   confirmer cela, c'est de montrer que la formulation **ne survit pas** quand on la teste sur des
   items dont la sensibilite est mesuree independamment et contre une population humaine appariee.
2. « L'historique de reponses bat la persona demographique » est mesure par L04-29 sur le SOEP, avec
   une exactitude de 78,8 pour cent. Notre C3 devant C2 est une replication, pas une decouverte.
3. « Les modeles se ressemblent entre eux plus qu'ils ne ressemblent aux humains » est observe par
   L04-30 sur une enquete professionnelle. Notre contraste de groupe de a28 section 1.6 en est une
   version quantifiee sur des items sensibles, ce qui reste distinct, mais l'anteriorite existe.
4. « La desirabilite des LLM vient de l'alignement » est etabli par L04-27 sur 264 modeles.

**Ce qui reste ouvert au 8 septembre 2026.**

1. **Personne ne dispose simultanement d'une ampleur de mode par item, mesuree chez l'humain, et
   d'un ecart agent contre humain sur les memes items.** L'ampleur existe maintenant, morcelee entre
   MR099, MR141, l'atlas et Oceno ; l'ecart existe chez nous ; le croisement continu n'est pas fait.
   C'est le point 4 de `corpus/04`, et il est desormais **realisable**, ce que `a25` declarait
   impossible.
2. **Personne n'a indexe la desirabilite par item et par camp dans une evaluation de simulation.**
   Oceno le fait chez l'humain, aucune etude LLM ne le fait. C'est le creneau le plus net qui reste,
   et il branche directement sur a30.
3. **Personne n'a mesure ce que devient l'ecart agent contre humain quand on retire a l'humain sa
   modalite d'echappement.** Le GSS 2021 a supprime « je ne sais pas » sur toutes les attitudes
   (L04-04) et le GSS 2021 et 2022 ont randomise l'affichage des modalites volontaires (L04-03). Il
   existe donc, sur le meme jeu de donnees que le notre, une condition humaine en **choix force**,
   c'est a dire dans le regime exact de nos agents. Personne n'a compare un agent a un humain en
   choix force.
4. **Personne n'a repris un item dont on sait que la reponse absolue est contredite par la reponse
   situationnelle chez 86 pour cent des repondants, et demande a un agent les deux formes.** MR010
   fournit l'item et le chiffre ; c'est un protocole a un seul item, tres bon marche, et il touche
   exactement l'endroit ou nos agents divergent le plus.
5. **La transposition de l'experience de liste a un agent simulant une personne** reste, en
   apparence, non faite. Avertissement : L04-35, « Generative-agent modeling of protest mobilization
   and preference falsification with large language models », n'a pas pu etre lu. Son titre
   revendique la transposition de Kuran aux agents generatifs. **Cette revendication de nouveaute ne
   doit pas etre ecrite avant d'avoir lu ce texte.**

---

## Ce que je n'ai pas pu verifier

1. **Le budget de recherche web etait epuise des le debut de la session** (200 appels sur 200). Toute
   la lecture repose sur OpenAlex, Semantic Scholar, l'API arXiv et l'exploration directe des
   depots. La recherche par moteur generaliste n'a pas ete faite, ce qui laisse un angle mort sur la
   litterature grise, les theses et les rapports d'instituts.
2. **Trois references directement sur le theme n'ont pas pu etre lues du tout** : Kazinnik et
   Enriquez, « Sex, drugs, and LLMs » (L04-33, SSRN en 403) ; Treglown et Furnham (L04-34,
   ScienceDirect en 403) ; Wang, « Generative-agent modeling of protest mobilization and preference
   falsification » (L04-35, SSRN inaccessible). La troisieme est la plus genante, voir le point 5 de
   la section precedente.
3. **Malka et Adelman (L04-14)** : Cambridge a renvoye une erreur 500 puis un 403. Seul le resume a
   ete lu. C'est la revue qui arbitre toute la litterature de la reponse expressive ; ne rien lui
   attribuer au dela de ses deux conclusions citees.
4. **Prior, Sood et Khanna (L04-11)** : nowpublishers en 403. L'ampleur exacte de la reduction de
   l'ecart partisan n'a pas ete lue, seul le resume l'a ete. Ne pas reprendre de pourcentage.
5. **Schaffner et Luks (L04-12)** : non OA. Les pourcentages celebres de cette etude circulent en
   source secondaire ; aucun n'est repris ici.
6. **Gibson et Sutherland (L04-19)** : OUP en 403 sur le PDF. Les series annuelles de 1954 a 2020 et
   les effectifs n'ont pas ete lus. Seules les phrases du resume sont citees.
7. **Crandall, Eshleman et O'Brien (L04-20)** : la valeur exacte du coefficient de correlation entre
   approbation sociale et expression du prejuge n'a pas ete lue dans le texte. Le resume dit « very
   highly correlated ». **Ne pas citer de valeur numerique pour ce coefficient.**
8. **Le rapport Pew de janvier 2021 sur la mesure de la religion (04-16 de la table initiale) reste
   non lu** : pewresearch.org renvoie un 403 sur la page et un 404 sur les deux URL de PDF essayees.
   L'ecart de mode sur la religion dans le panel Pew reste non chiffre chez nous, alors qu'il l'est
   maintenant pour le GSS par L04-05.
9. **MR021 (L04-07) n'a ete lu que par extraits**, la numerisation etant de mauvaise qualite. Les
   tables completes n'ont pas ete depouillees ; les chiffres repris sont ceux du corps du texte.
10. **L'atlas (L04-09) a ete lu dans son corps, pas dans ses annexes.** La table A3, qui porte les
    taux de faux positifs et de faux negatifs etude par etude, n'a pas ete depouillee. C'est
    pourtant elle qui contient l'ampleur par item la plus fine du document, et c'est la prochaine
    chose a lire si T1 est retenu.
11. **L04-28 est cite sans ses auteurs**, l'entree arXiv n'ayant pas ete depouillee au dela du
    resume. A completer avant toute citation dans un papier.
12. **Aucune verification n'a ete faite du recouvrement exact** entre les vingt items de MR141 et nos
    149. Le T3 en depend entierement ; s'il y a moins de dix items communs, le test n'a pas de
    puissance.
13. **Les 119 temoins negatifs de la note de mode 2022 n'ont pas ete recroises avec MR141.** Si un
    item classe « peu susceptible d'etre sensible au mode » se revele porter 40 pour cent de
    modalite volontaire, la notion meme de temoin negatif est a redefinir.
