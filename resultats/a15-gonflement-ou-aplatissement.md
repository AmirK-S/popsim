# a15. Gonflement ou aplatissement des ecarts inter groupes : reconciliation

Date : 7 septembre 2026. Auteur : agent de recherche a15. Aucun code execute, aucune
microdonnee manipulee, aucun fichier existant modifie. Trois travaux lus en entier dans leur
texte source, plus deux relus sur les points litigieux.

---

## Reponse en une ligne

**Il n'y a pas de contradiction empirique, il y a une collision de vocabulaire sur deux
quantites differentes, et la variable qui separe reellement les deux camps n'est aucune des
cinq proposees : c'est l'axe de segmentation.** Les travaux qui segmentent sur un axe politique
mesurent un gonflement ; les travaux qui segmentent sur des axes demographiques non politiques
mesurent un ecart proche de 1 ou legerement inferieur, et quand ils annoncent un
"aplatissement" ils le lisent sur une metrique globale de dispersion qui ne separe pas l'inter
de l'intra. Le papier PSII, qui est cite comme le contradicteur principal, **ne mesure jamais
d'ecart inter groupes sur ses sorties**, et son introduction ecrit noir sur blanc que
l'injection de demographies par l'invite "exaggerates between-group differences".

---

## Table des matieres

1. Ce qui a ete lu, et ce qui ne l'a pas ete
2. Le fait central : PSII ne mesure pas ce que son resume annonce
3. Fiche par travail : modele, temperature, decodage, invite, donnees, segmentation, metrique, sens
4. Le tableau de reconciliation
5. Les cinq hypotheses, verdict par hypothese
6. La variable qui separe reellement, et deux variables non listees
7. Ce que popsim peut ecrire de la contradiction
8. Ce qu'il faut mesurer chez nous, et le contraste exact a regarder au matin
9. Ce que je n'ai pas pu verifier
10. Questions ouvertes pour Simon

---

# 1. Ce qui a ete lu, et ce qui ne l'a pas ete

| source | acces | etendue de lecture |
|---|---|---|
| arXiv 2603.16142 v2, PSII | HTML arXiv complet recupere et converti en texte, 98 469 caracteres | **entier**, corps et annexes A a E |
| arXiv 2305.09620 v4, Kim et Lee | HTML arXiv complet recupere et converti en texte, 250 004 caracteres | **entier**, corps et annexes A a F |
| Bisbee, Clinton, Dorff, Kenkel, Larson 2024, Political Analysis 32(4) 401 a 416 | **PDF complet et gratuit** sur Cambridge Core, 16 pages, extrait en texte | **entier**, corps de l'article. Le Supporting Information n'est pas dans ce PDF |
| arXiv 2607.26348 v1, Chen, Zhu, Zheng | HTML arXiv complet | relu sur les points de methode que a10 n'avait pas couverts : temperature, style d'invite, indice eta carre |
| arXiv 2608.19621, LifeMem | page de resume arXiv | resume seul, le reste vient de la lecture faite en a13 |
| arXiv 2605.16303, Garzon et al. | rien de neuf | valeurs reprises de a13, qui l'a lu en entier |

**Bisbee et al. 2024 n'est pas derriere un paywall.** Le PDF de l'article publie est
telechargeable librement depuis Cambridge Core.
[CONFIRME avec URL]
https://www.cambridge.org/core/services/aop-cambridge-core/content/view/B92267DC26195C7F36E63EA04A47D2FE/S1047198724000056a.pdf/synthetic-replacements-for-human-survey-data-the-perils-of-large-language-models.pdf
En tete de page : "Political Analysis (2024), 32, 401 to 416, doi:10.1017/pan.2024.5",
"(Received 2 May 2023; revised 18 January 2024; accepted 20 January 2024; published online 17
May 2024)". Affiliation unique : "Political Science Department, Vanderbilt University,
Nashville, TN, USA". Le materiel supplementaire, cite dans l'article sous le nom "SI Section
1" a "SI Section 13", n'est pas inclus dans ce PDF et n'a pas ete recupere. Les donnees de
replication sont annoncees a https://doi.org/10.7910/DVN/VPN481, non ouvertes ici.

---

# 2. Le fait central : PSII ne mesure pas ce que son resume annonce

C'est le resultat le plus important du rapport et il desamorce la contradiction avant tout le
reste.

## 2.1 Ce que le resume affirme

Citation exacte, resume, phrase 2 :
"Despite their scalability, current LLM-based simulation methods fail to capture social
diversity, producing flattened inter-group differences and overly homogeneous responses across
demographic groups."
[CONFIRME avec URL et section] https://arxiv.org/html/2603.16142v2, resume.

## 2.2 Ce que le papier mesure reellement sur les sorties

**Deux metriques, et une seule unite d'agregation.** Citation exacte, section 4.1, Dataset and
Evaluation Metrics :
"Model performance is evaluated at the group level by comparing the distribution of
model-generated responses with the human ground-truth distribution. We report KL divergence to
measure distributional accuracy, where lower values indicate better alignment with human
responses."
Puis :
"To assess diversity, we compute Entropy Deviation (ED), defined as the absolute difference
between the normalized entropy of model-generated responses and that of human responses, where
a lower ED indicates closer diversity matching to the human distribution."
[CONFIRME avec URL et section] https://arxiv.org/html/2603.16142v2, section 4.1.

Ces deux quantites sont calculees **sur la distribution de reponses de la population entiere**,
100 agents echantillonnes parmi 97 220 repondants du WVS, question par question, puis moyennees
par categorie thematique. Aucune des deux ne separe la composante inter groupes de la
composante intra groupes. Le mot "group level" dans la phrase citee designe le niveau agrege
par opposition au niveau individuel, pas une segmentation demographique : le tableau 1 ne
comporte aucune colonne de segment, ses colonnes sont les quatre categories de questions et le
total.

**Il n'existe dans tout le papier aucune valeur d'ecart entre groupes calculee sur les reponses
et comparee a la valeur humaine.** Recherche exhaustive faite sur le texte integral converti :
les chaines "inter-group", "intergroup", "between-group" et "flatten" apparaissent en tout six
fois, dont une dans le resume, trois dans l'introduction, une dans la conclusion et une dans la
declaration d'impact ethique. Aucune dans les sections 4, 5 ou dans les annexes de resultats.
[CONFIRME, recherche sur le texte integral]

## 2.3 Sur quoi repose alors l'affirmation d'aplatissement

Sur deux choses, aucune des deux n'etant une mesure d'ecart inter groupes sur les reponses.

**(a) La dispersion des etats caches.** Citation, legende de la figure 1 :
"In the top panels, red points denote baseline methods and gray points denote PSII-generated
agents; the reported scores measure the average spatial dispersion of representations in each
layer."
Et l'annexe E.4 precise la metrique :
"We further quantify representation-level heterogeneity using a k-nearest-neighbor (kNN) radius
metric, defined as the average distance from each hidden-state vector to its k-th nearest
neighbor, scaled by a factor of 100 for readability, where larger values indicate more
dispersed and diverse representations."
[CONFIRME avec URL et section] https://arxiv.org/html/2603.16142v2, figure 1 et annexe E.4.

**Le rayon kNN moyen sur 500 agents est une dispersion totale : il melange l'inter et l'intra
exactement comme la colonne "ce que voit une mesure globale" de a1 section 3.** Une chute de ce
rayon est parfaitement compatible avec un ecrasement intra accompagne d'un gonflement inter,
c'est a dire avec la double distorsion. Le papier appelle cette chute "Diversity Collapse" et
n'en tire aucune decomposition.

**(b) Les distributions de reponses concentrees.** Citation, section 5 :
"As shown in Figure 3, baseline methods tend to concentrate responses on a small number of
options, exhibiting limited diversity."
[CONFIRME] C'est une affirmation sur la diversite totale, sur quatre questions choisies au
hasard, sans segmentation.

## 2.4 Et l'introduction du meme papier dit l'inverse du resume

C'est le point qui tranche. L'introduction distingue explicitement deux regimes et leur donne
deux sens opposes.

Citation exacte, introduction, "Their limitations in diversity manifest at two distinct levels" :

> "First, the inter-group diversity. Standard training objectives for LLMs, such as maximum
> likelihood estimation with cross-entropy loss, inherently favor the most probable
> continuations. As a result, minority or low-frequency viewpoints tend to be underrepresented,
> leading to flattened response distributions in which distinct subpopulations become difficult
> to distinguish.
> Second, intra-group diversity. When demographic attributes are injected via prompts,
> identities are treated as fixed explanatory variables that dominate response generation. This
> method ignores the heterogeneity within groups, **exaggerates between-group differences**, and
> reinforces group stereotypes as a consequence."

[CONFIRME avec URL et section] https://arxiv.org/html/2603.16142v2, section 1, Introduction.
La mise en gras est de ce rapport, la phrase est litterale.

**Lecture.** Le papier attribue l'aplatissement au regime **sans persona**, celui du
questionnement direct sans conditionnement, ou le mecanisme invoque est l'objectif
d'entrainement lui meme. Il attribue le **gonflement** au regime **avec persona demographique
dans l'invite**, qui est exactement le regime de Chen et al., de Bisbee et al., des agents
demographiques de Stanford et de nos conditions a5. Les deux camps sont donc d'accord, y
compris a l'interieur de PSII, et le resume du papier compresse les deux regimes en une seule
phrase qui n'est vraie que du premier.

Une confirmation par la structure des baselines. Le baseline "Direct" est defini ainsi :
"The Direct baseline performs LLM-based simulation without any explicit mechanisms for
diversity control or identity conditioning. For each survey question, the model is prompted to
generate a response directly, serving as a minimal and commonly used reference setting in prior
social simulation work."
[CONFIRME avec URL et section] https://arxiv.org/html/2603.16142v2, annexe B.
**Dans ce regime, les 100 agents recoivent une invite identique. L'ecart entre groupes
demographiques y est nul par construction, puisque le groupe n'entre nulle part dans le calcul
de la reponse.** "Flattened inter-group differences" est, pour ce baseline, une verite
tautologique et non un resultat de mesure.

---

# 3. Fiche par travail

## 3.1 popsim, a1, sur le paquet de replication de Stanford

| | |
|---|---|
| Modele | non applicable, reanalyse de sorties produites par l'equipe de Stanford, modele non redocumente dans a1 |
| Temperature et decodage | inconnu de nous, texte genere puis apparie a la nomenclature ; 0,04 a 0,33 pour cent de sorties non codables chez les agents contre 0,00 chez les humains |
| Contenu de l'invite | six conditions distinctes : entretien `gss_v3`, persona `gss_v7`, questionnaire `survey_agents`, questionnaire plus entretien `composite_agents`, et deux variantes etiquetees demographiques `gss_v6` et `gss_v8` |
| Jeu de donnees | GSS, 1 052 participants apparies, 169 items retenus sur 177 |
| Segmentation | 6 axes : genre, race, ideologie politique, age, education, profil croise genre x race x ideologie a 18 segments |
| Metrique | ratio a l'humain de vague 1 de la composante inter et de la composante intra d'une decomposition additive `D = D_intra + D_inter`, trois mesures de dispersion, bootstrap 1 000 tirages |
| Sens trouve | **les deux**, selon la condition |

Ratios inter : composite 1,753 ; entretien 2,156 ; enquete 1,824 ; **persona `gss_v7` 0,437** ;
**demographique `gss_v6` 0,855** ; demographique `gss_v8` 5,907. Ratios intra : 0,637 a 0,885,
donc ecrasement dans les six conditions.
[source interne] `resultats/a1-double-distorsion.md` section 3.

**Le detail par axe, et il est decisif pour la suite.** Ratio inter, mesure entropie :

| condition | genre | race | ideologie | age | education | profil croise |
|---|---|---|---|---|---|---|
| composite | 1,26 | 1,48 | **2,09** | 1,17 | 1,35 | 1,89 |
| entretien | 1,36 | 1,61 | **2,72** | 1,19 | 1,27 | 2,44 |
| enquete | 0,80 | 1,22 | **2,49** | 0,78 | 1,06 | 2,06 |
| persona v7 | 0,99 | 0,73 | 0,27 | 0,72 | 0,35 | 0,38 |
| demographique v6 | 1,57 | 2,44 | 0,34 | 0,70 | 2,69 | 0,71 |
| demographique v8 | 1,09 | 4,01 | **8,51** | 3,50 | 0,37 | 6,64 |

[source interne] `resultats/a1-ratios-par-axe.csv`, recopie dans a1 section 4.

**A retenir pour la reconciliation : sur les axes non politiques, les conditions ancrees sont a
1 ou en dessous.** Genre 0,80 et age 0,78 pour la condition enquete, age 0,72 pour la condition
persona, education 0,35. Autrement dit, **si on ne segmente pas sur la politique, a1 mesure lui
aussi un aplatissement leger.**

## 3.2 Chen, Zhu, Zheng, arXiv 2607.26348 v1

| | |
|---|---|
| Modeles | Claude Haiku 4.5, Claude Sonnet 4.6, Llama-3.1-8B-Instruct, Llama-3.3-70B-Instruct |
| Temperature | **1,0**. Citation : "Decoding uses temperature 1.0 (the model's default sampling; where a model rejects an explicit temperature field it is omitted and the provider default applies) and a token cap of 100." [CONFIRME avec URL et section] https://arxiv.org/html/2607.26348v1, annexe A, "Model call settings" |
| Decodage | **les deux modes, et c'est un fait neuf par rapport a a10.** "Style A, the single-answer prompt. The model is shown the demographic profile and question and must return one answer (an option letter for short-labelled questions, or the scale number for numeric scales)." et "Style C, the distribution prompt. The model must return a probability for each answer option, expressed as JSON." [CONFIRME avec URL et section] section 3.2. Dans les deux cas c'est du texte genere, jamais des logits lus |
| Invite | demographies seules, **ideologie politique et identification partisane incluses sur le GSS** : age, sexe, race, diplome, region, opinions politiques, identification partisane. Aucune reponse anterieure de la personne |
| Jeux de donnees | GSS 2016 a 2024, 14 704 repondants, 10 questions ; WVS vague 7, 63 pays, 91 774 repondants, 16 questions |
| Segmentation | paire (question, axe demographique) ; **axe principal GSS "political views", axe principal WVS "country"** |
| Metrique 1 | facteur de gonflement d'ecart, `gap_model / gap_human` avec `gap = max_g p_g - min_g p_g` ou `p_g` est "the fraction of segment g on the high end of the answer scale" |
| Metrique 2, non relevee en a10 | **indice de stereotypage `Delta eta^2 = eta^2_model - eta^2_human`**. Citation : "The natural measure is the share of the total variation in answers that is explained by which group a person belongs to. Statisticians call this eta^2, the ratio of the variation between groups to the total variation (between plus within groups)." [CONFIRME avec URL et section] section 3.3 |
| Sens trouve | **gonflement, dans les 16 cellules** |

Le fait a retenir : `eta^2` est **la meme quantite que le ratio inter de a1**, a la
normalisation pres, puisque c'est la part de variance imputable au groupe. Chen la publie pour
les humains et pour le modele, et sa difference est positive partout.

| jeu | modele | style | `Delta eta^2` median | cellules significatives |
|---|---|---|---|---|
| GSS | Haiku 4.5 | A texte | +0,048 | 5 sur 8 |
| GSS | Haiku 4.5 | C probabilites | +0,059 | 9 sur 12 |
| GSS | Sonnet 4.6 | A texte | +0,081 | 10 sur 12 |
| GSS | Sonnet 4.6 | C probabilites | **+0,104** | 9 sur 12 |
| GSS | Llama 8B | A texte | +0,026 | 7 sur 12 |
| GSS | Llama 8B | C probabilites | +0,026 | 3 sur 7 |
| GSS | Llama 70B | A texte | +0,051 | 6 sur 8 |
| GSS | Llama 70B | C probabilites | +0,031 | 5 sur 8 |
| WVS | Haiku 4.5 | A / C | +0,087 / +0,056 | 30 sur 32 / 21 sur 24 |
| WVS | Sonnet 4.6 | A / C | +0,107 / +0,103 | 31 sur 32 / 26 sur 28 |
| WVS | Llama 8B | A / C | +0,030 / +0,376 | 22 sur 32 / 1 sur 1 |
| WVS | Llama 70B | A / C | +0,136 / +0,054 | 31 sur 32 / 27 sur 30 |

[CONFIRME avec URL et section] https://arxiv.org/html/2607.26348v1, tableau de la section 4,
colonne `Delta eta^2 (sig)`. La cellule Llama-8B Style C sur WVS porte une reserve des auteurs :
"Llama-8B Style-C on WVS is effectively unusable (85% invalid, n = 440)".

**Seize cellules sur seize sont positives. Aucune inversion de signe entre le mode texte et le
mode probabilites.** Pour Sonnet sur le GSS, le mode probabilites gonfle **davantage** que le
mode texte, +0,104 contre +0,081.

## 3.3 Bisbee, Clinton, Dorff, Kenkel et Larson 2024, Political Analysis

| | |
|---|---|
| Modele | **ChatGPT 3.5 Turbo**, version anterieure au 25 juin 2023, plus un controle sur Falcon-40B-Instruct. Citation : "our original analyses were conducted on the pre-June 25 version of ChatGPT 3.5 Turbo, but that version was only accessible until September 2023" |
| Temperature | **1**. Citation, note 19 : "We use a temperature parameter of 1 in our main analysis and demonstrate the strong positive association between this hyperparameter and the empirical variance of the synthetic data in SI Section 2." [CONFIRME avec URL et section] PDF Cambridge, page 407, note de bas de page 19 |
| Decodage | texte genere, format tsv impose, avec justification et confiance auto declaree. 30 repondants synthetiques par humain, 7 530 humains, **3 614 400 reponses** |
| Invite | **persona a la deuxieme personne contenant l'ideologie et le parti.** Citation exacte : "It is [YEAR]. You are a [AGE] year-old, [MARST], [RACETH] [GENDER] with [EDUCATION] making [INCOME] per year, living in the United States. You are [IDEO], [REGIS] [PID] who [INTEREST] pays attention to what's going on in government and politics." [IDEO] prend sept valeurs de "an extremely liberal" a "an extremely conservative", [PID] trois valeurs |
| Jeu de donnees | ANES vagues 2016 et 2020, 7 530 repondants, thermometres de sentiment sur 11 groupes sociopolitiques mesures dans l'ANES sur 16 demandes |
| Segmentation | **race croisee avec identification partisane** pour la figure 2 |
| Metrique | moyennes et ecarts types par groupe, comparaison directe aux valeurs ANES ; plus des coefficients de regression ; plus un calcul de puissance |
| Sens trouve | **les deux termes, dans les deux sens opposes, dans la meme figure** |

Citations exactes du terme inter, section 2.1 :
"Even though the synthetic data broadly perform well in terms of summarizing overall human
opinion, issues emerge when we look at subgroups. To demonstrate, we examine affective
polarization and partisan sectarianism, calculating how average opinions toward liberals,
conservatives, and the major parties vary across groups of respondents defined by race and
partisanship. Figure 2 presents the results, highlighting the relative extremity of ChatGPT
responses, especially among Democrats, that is masked when averaging over partisanship in
Figure 1. These differences are substantively meaningful, amounting to 0.5 to 1 standard
deviations of the ANES distribution of attitudes, and 10 to 20 points on the 100-point
thermometer scale. In particular, these results suggest that Democrats like liberals more, and
conservatives less, than their human counterparts, exaggerating the out-group antipathy along
ideological lines."
[CONFIRME avec URL et section] PDF Cambridge, page 406, section 2.1.

Citation exacte du terme intra, phrase suivante :
"Figure 2 also reveals far smaller standard deviations in the synthetic estimates than found in
the ANES."
Et la garantie que ce n'est pas un artefact de moyennage, note 20 :
"These tighter standard deviations are not the product of calculating the average of 30
synthetic responses, as we calculate these based on a single synthetic measure per human
respondent."
[CONFIRME avec URL et section] PDF Cambridge, page 406 et note 20.

**Le seul couple chiffre publie des deux termes, tableau 1 page 407.** Legende exacte :
"The second column records the calculation if we assume an effect size and variance equal to
the 2016 to 2020 pooled ANES values (size 7.8, sd 31.4); the third column is the same
calculation with our ChatGPT estimates (size 12.5, sd 16.1)."
[CONFIRME avec URL et section] PDF Cambridge, tableau 1, page 407.

| quantite | ANES | ChatGPT | ratio |
|---|---|---|---|
| ampleur, ecart a la polarisation affective de 2012 | 7,8 | 12,5 | **1,60** |
| ecart type de la polarisation affective entre repondants | 31,4 | 16,1 | **0,513** |

**Reserve importante sur la premiere ligne.** "Size" n'est pas l'ecart entre groupes lui meme,
c'est l'ecart entre le niveau 2016 a 2020 et le niveau 2012, dont l'article rappelle qu'il
valait 47,4 : "when the average gap between in-party and out-party assessments among partisans
in the ANES was 47.4". Le facteur 1,60 est donc un gonflement d'une **variation** de l'ecart
inter partisan, pas du niveau de l'ecart, qui passe de 55,2 a 59,9, soit un facteur 1,08. **Ne
pas citer 1,60 comme un ratio inter groupes.** La deuxieme ligne, en revanche, 0,513, est un
ratio d'ecarts types entre repondants sur une quantite construite, et c'est vraisemblablement
[PROBABLE] la source de la fourchette "0,40 a 0,56" que PASSATION.md section 5 attribue au ratio
d'ecarts types.

**Le test d'invite, et c'est le seul du corpus qui manipule explicitement la politique.**
Citation exacte, section 3.1 :
"The first prompt only describes the nonpolitical profile of the synthetic respondent,
including their age, gender, race, marital status, education, and income. The second prompt
only includes a description of the synthetic respondent's political characteristics, including
their ideology, partisanship, registration status, and interest in news and politics."
Resultat :
"As illustrated in Figure 4, the mean absolute error is basically identical between the full
prompt and politics-only prompt. However, failing to include information on the respondent's
politics dramatically inflates the error for certain groups, notably those groups which are
more politically salient (the parties, ideological groups, gays and lesbians, and Muslims)."
Et en note 13 :
"In Section 3.1, we demonstrate that the synthetic data are sensitive to which attributes are
included in the prompt, finding that the majority of the performance hinges on the political
covariates."
[CONFIRME avec URL et section] PDF Cambridge, pages 404 et 410 a 411.

**Limite decisive de ce test pour nous : la metrique rapportee est l'erreur absolue moyenne,
pas une decomposition de variance.** Il etablit que les covariables politiques portent
l'essentiel de la performance, il n'etablit pas que leur retrait inverse le signe du terme
inter. Il ne peut donc pas trancher l'hypothese 2 a lui seul.

**Un fait non liste dans les cinq hypotheses et qui merite d'y entrer.** Note 23 :
"The synthetic data used in our main analyses rely on a second-person prompt ("You are a ...").
Levendusky and Malhotra (2016) demonstrate that asking humans estimate others' attitudes
produces exaggerated estimates of polarization. In SI Section 3, we regather synthetic data
using a first-person prompt ("I am a ..."), finding less evidence of exaggerated polarization,
although worse overall performance in terms of mean absolute error."
[CONFIRME avec URL et section] PDF Cambridge, page 410, note 23.

## 3.4 Kim et Lee, arXiv 2305.09620 v4

| | |
|---|---|
| Modele | **Alpaca-7B gele**, plus GPT-J-6B et RoBERTa-large en variantes. Ce n'est pas une simulation par invite : le modele n'encode que le texte de la question, et deux plongements appris, un par repondant et un par periode, sont concatenes puis passes dans un Deep Cross Network a sortie sigmoide |
| Temperature et decodage | **sans objet.** La sortie est une probabilite `P(Agree)` dans [0,1] produite par une tete de classification. Pas d'echantillonnage, pas de generation. Gemini-2.5-Pro a temperature 0,2 n'intervient que pour annoter et binariser les items en amont |
| Contenu de l'invite | **aucune demographie n'entre dans le modele.** L'entree est le texte de la question, l'identifiant du repondant et l'annee. Les demographies ne servent qu'a segmenter a l'evaluation et comme controles de regression |
| Jeu de donnees | GSS 1972 a 2021, 68 846 individus, 3 699 questions binarisees, 33 vagues |
| Segmentation | genre, race, age, education, orientation politique, plus un panneau "All" |
| Metrique inter | "To assess between-group variance, we estimate the standard deviation of predicted and observed group means across key demographic categories" ; comparaison predit contre observe par nuage de points, correlation de Spearman et erreur absolue moyenne, un point par variable du GSS |
| Metrique intra | ecart type des reponses individuelles dans chaque sous groupe, **sur des predictions binarisees au seuil 0,5** |
| Sens trouve | **inter : bien reproduit, sans signe publie. intra : sous estime.** |

Citation exacte du resultat :
"The model captures between-group variance well, particularly for political stance and
education (fig. A13). For within-group variance, predicted and observed subgroup standard
deviations are strongly correlated across categories; nevertheless, the model underestimates
the absolute level of within-group variance across most demographic categories (fig. A14)."
[CONFIRME avec URL et section] https://arxiv.org/html/2305.09620v4, section "Evaluation of
Predicting Between-and Within-Group Variances".

Et l'origine methodologique :
"Following Bisbee et al. (2024), we evaluate whether the model captures between-group and
within-group response variance across gender, race, age, education, and political-stance
subgroups."
[CONFIRME]

**Trois points qui interdisent de compter ce travail dans l'un ou l'autre camp.**

1. **Le modele est entraine sur le GSS lui meme.** Un modele supervise sur les sorties n'a
   aucune raison structurelle de gonfler l'inter, et de fait il le reproduit. C'est un regime
   different de la simulation par invite.
2. **Aucun signe n'est publie pour l'inter.** Une correlation de Spearman et une erreur absolue
   moyenne entre ecarts types predits et observes ne disent pas si le predit est au dessus ou
   au dessous. Le mot "well" n'est pas un signe.
3. **Le terme intra est calcule sur des predictions binarisees au seuil 0,5.** Citation :
   "The within-group comparison uses binarized predictions (threshold 0.5) to match the scale
   of the observed binary responses." [CONFIRME, annexe F] C'est un durcissement de type argmax
   qui detruit une partie de la dispersion probabiliste avant de la mesurer, exactement le
   probleme signale par a5 section 3 sur l'ecart entre lecture argmax et lecture
   distributionnelle.

**Ce que Kim et Lee apportent pour notre question, et que a13 n'avait pas releve.** Leur v4
contient un banc de modeles d'etagere invites en persona, sur le GSS 2018, avec trois niveaux
de richesse d'invite. Citation exacte :
"We benchmark our model against GPT-4o and Gemini-2.5-flash on the 2018 GSS data under three
prompting strategies, following (Argyle et al., 2023): (i) a demographics-only prompt that
includes 15 respondent characteristics (year, ideology, party affiliation, race, sex, family
income, age, birth year, education, region, urbanicity, ethnic background, work status, marital
status, religion); (ii) a random-k=10 context prompt that adds the respondent's binarized
responses to 10 randomly selected GSS items on top of (i); and (iii) a correlation-top-k=10
context prompt that instead adds the 10 items whose responses correlate most strongly with the
target variable in the training data."
[CONFIRME avec URL et section] https://arxiv.org/html/2305.09620v4, annexe E, "Prompted
out-of-shelf LLMs".

**C'est le plan experimental exact de l'hypothese 1, avec l'ideologie presente dans les trois
conditions. Mais ils ne publient pour ces trois conditions que l'exactitude et le F1**, dans le
tableau A15, jamais la decomposition inter et intra. L'occasion est manquee d'un cheveu.

## 3.5 PSII, arXiv 2603.16142 v2

| | |
|---|---|
| Modeles | Qwen2.5-7B-Instruct, Qwen2.5-14B-Instruct, Llama-3.1-8B-Instruct, Mistral-24B-Instruct |
| Temperature | **0,7 par defaut**, top_k 20. Citation : "Unless otherwise specified, generation uses default decoding parameters with temperature = 0.7 and top_k = 20." Un baseline dedie "High-Temp" a temperature 2 |
| Decodage | texte genere, une reponse par question, dans l'ordre original du WVS |
| Invite du baseline persona "PE" | **demographies seules, sans aucune variable politique ni ideologique.** Texte litteral : "You are a {sex}. You are aged {age}. You live in {country}. You are {citizenship}. ... You are {marital_status}, have {num_children} children. Your education level is {education_self}. ... You belong to the {social_class}. Your income is in income group {income_decile} (1 = lowest, 10 = highest). {religion_status}. Your ethnic group is {ethnic_group}." |
| Baseline "Direct" | **aucune persona du tout**, les 100 agents recoivent la meme invite |
| Jeu de donnees | WVS vague 7, questions Q1 a Q259 en cible, Q260 a Q290 en demographies, **100 repondants tires au hasard parmi 97 220** |
| Segmentation declaree | tableau 4 : sexe, statut d'immigration, cohabitation parentale, statut marital, education, emploi, profession, type d'employeur, role de salarie, finances familiales, classe sociale, decile de revenu, religion. **Aucun axe politique** |
| Metriques sur sorties | divergence KL et Entropy Deviation, **toutes deux sur la population entiere** |
| Sens trouve sur les sorties | **aucun, faute de mesure inter groupes** |
| Sens affirme dans le resume | aplatissement |

**L'effet de la persona sur la diversite totale, chez eux, va dans le sens du gonflement de
diversite.** Tableau 1, Qwen2.5-7B, colonne Overall : Direct KL 1,3915 et ED 0,7340 ; PE
KL 1,2209 et ED 0,5443. Comme l'ED est la valeur absolue de la difference d'entropie normalisee
et que les modeles sont moins diversifies que les humains, une baisse d'ED signifie que la
persona **rapproche** l'entropie de la valeur humaine. Le passage en High-Temp fait de meme,
ED 0,5778. [CONFIRME avec URL et section] tableau 1.

## 3.6 LifeMem, arXiv 2608.19621, et Garzon et al., arXiv 2605.16303

Repris de a13, avec un seul element neuf.

**LifeMem affirme le gonflement dans son resume, ce que a13 n'avait pas mis en avant.** Citation
exacte : "Our analysis shows that static-profile agents exhibit stronger demographic separation
and within-group compression than humans, a pattern consistent with identity essentialism:
demographic labels can encourage models to treat group-average tendencies as individual traits,
homogenizing responses within groups."
[CONFIRME avec URL et section] https://arxiv.org/abs/2608.19621, resume.

C'est **la double distorsion enoncee en une phrase, avec referent humain**. Mais a13 a etabli
que les quatre metriques publiees ne comprennent aucun terme inter, et que le seul chiffre de
separation, le silhouette 0,19 contre -0,02 chez les humains, est en annexe B, sur le WVS vague
7, avec **des tertiles de statut socio economique** pour segmentation, un axe non politique.

**Garzon et al.** : ICC de 0,17 pour les agents demographiques contre 0,06 pour les agents
ancres sur l'echelle RS, segmentation age croise genre uniquement, **aucun referent humain**.
Le sens n'est donc pas determinable et ce travail ne compte dans aucun camp.

---

# 4. Le tableau de reconciliation

| travail | modele | temperature | lecture | ideologie dans l'invite | axe de segmentation | metrique du terme inter | referent humain | sens du terme inter |
|---|---|---|---|---|---|---|---|---|
| **a1**, conditions ancrees | Stanford, inconnu | inconnue | texte | oui pour v6 et v8 selon a1, **conteste par a2** | 6 axes dont ideologie | ratio de composante de variance | oui, vague 1 et vague 2 | **gonflement 1,75 a 2,16**, mais **0,78 a 1,36 sur genre et age** |
| **a1**, persona v7 et demo v6 | idem | idem | texte | idem | idem | idem | oui | **aplatissement 0,44 et 0,86** |
| **a1**, demo v8 | idem | idem | texte | idem | idem | idem | oui | **gonflement 5,91**, dont 8,51 sur l'ideologie |
| **Chen et al.** | Haiku 4.5, Sonnet 4.6, Llama 8B et 70B | **1,0** | texte, styles A et C | **oui**, "political views" et "party identification" | **"political views" sur GSS**, "country" sur WVS | `gap_model/gap_human` et `Delta eta^2` | oui | **gonflement, 16 cellules sur 16** |
| **Bisbee et al.** | ChatGPT 3.5 Turbo, avant 25 juin 2023 | **1** | texte | **oui**, sept modalites d'ideologie et trois de parti | **race x partisanship** | moyennes de groupe comparees a l'ANES | oui | **gonflement**, "exaggerating the out-group antipathy along ideological lines" |
| **LifeMem** | Llama-3.1-8B, Ministral-3-8B, Qwen3.5-9B | decodage deterministe | texte | non | sexe, naissance, marital, emploi, religion, diplome ; SES en tertiles pour le silhouette | aucune metrique inter publiee, un silhouette en annexe | oui pour le silhouette | **gonflement affirme**, mesure seulement par silhouette sur un axe SES |
| **Garzon et al.** | non redocumente ici | idem | texte | non | **age x genre seulement** | ICC(1), donc un rapport | **non** | **indeterminable** |
| **Kim et Lee** | Alpaca-7B gele plus tete supervisee | sans objet | probabilite de classification | **non, aucune entree demographique** | genre, race, age, education, orientation politique | ecart type des moyennes de groupe, Spearman et MAE | oui | **aucun signe publie**, "captures between-group variance well" |
| **PSII** | Qwen2.5-7B et 14B, Llama-3.1-8B, Mistral-24B | **0,7**, et 2 pour un baseline | texte | **non** | tableau 4, **aucun axe politique** | **aucune** | non applicable | **aplatissement affirme, jamais mesure sur les sorties** |

---

# 5. Les cinq hypotheses, verdict par hypothese

## H1. La richesse de l'invite : demographies seules aplatissent, reponses reelles gonflent

**CONTREDITE, dans le sens ou elle est formulee.**

Trois faits la contredisent frontalement.

1. **a1.** La condition qui gonfle le plus n'est pas la plus riche, c'est la variante
   demographique `gss_v8` a 5,907. Les conditions les plus riches en information sur la
   personne, composite et entretien, sont a 1,753 et 2,156, soit trois fois moins.
2. **Garzon et al.** vont dans le meme sens. "Demographics7 agents show consistently higher ICC
   than survey-anchored agents across all scales (RS: 0.17 vs. 0.06; KFP: 0.08 vs. 0.02; FTP:
   0.07 vs. 0.04; FRT: 0.10 vs. 0.02), indicating greater demographic determinism". [CONFIRME,
   repris de a13, section 4.3.2 du papier] L'agent demographique concentre **plus** de variance
   entre strates que l'agent ancre, pas moins.
3. **Chen et al.** n'evaluent que des agents demographiques purs et mesurent un gonflement dans
   les seize cellules. Si l'hypothese etait juste, ce regime devrait aplatir.

Un fait la contredit dans l'autre sens et interdit de la retourner : **la condition persona
`gss_v7` et la variante `gss_v6`, toutes deux pauvres en information, aplatissent** a 0,437 et
0,855. La richesse de l'invite n'ordonne donc le signe dans aucun sens : elle ordonne peut etre
l'amplitude parmi les conditions qui gonflent [HYPOTHESE], elle ne predit pas le signe.

**Occasion manquee.** Kim et Lee v4 fait tourner exactement le plan factoriel de H1, GPT-4o et
Gemini-2.5-flash sur le GSS 2018 en demographies seules, puis plus 10 items aleatoires, puis
plus 10 items correles, et ne publie que l'exactitude et le F1. Personne n'a publie la
decomposition inter et intra sur ce plan. **Nous pouvons le faire, voir la section 8.**

## H2. La presence de l'ideologie politique dans l'invite

**NE PERMET PAS DE TRANCHER, et un fait interne l'affaiblit serieusement.**

Ce qui la soutient :

- Bisbee, ideologie et parti dans l'invite, gonflement mesure sur l'axe partisan, et note 13
  qui dit que "the majority of the performance hinges on the political covariates".
- Chen, opinions politiques et identification partisane dans l'invite sur le GSS, gonflement
  median 2,3 sur l'axe "political views".
- PSII, **aucune variable politique dans l'invite PE** ni dans sa liste de segmentation, et
  aucun gonflement rapporte.
- a1, `gss_v6` et `gss_v8` portent la meme etiquette demographique et se separent d'un facteur
  25 sur le seul axe ideologique, 0,34 contre 8,51, ce qui est compatible avec une difference
  de contenu d'invite sur cette variable [HYPOTHESE, le contenu des deux invites n'est pas
  connu].

**Ce qui l'affaiblit, et c'est un fait interne a a1.** La condition `survey_agents`, construite
sur le seul questionnaire, ne contient **aucune etiquette demographique** et **aucune
ideologie**, et elle gonfle l'axe ideologique de 2,49, davantage que la condition composite qui
en contient. Si H2 etait juste au sens litteral, cette cellule devrait etre proche de 1. Elle ne
l'est pas.

**Une incoherence interne du dossier a signaler.** a1 section 1 ecrit "Un agent demographique a
recu ces valeurs dans son invite" en incluant `polviews` et `partyid` parmi les huit items
retires. a2 section 2.1 ecrit l'inverse : "L'agent demographique n'a probablement pas recu
l'orientation politique", sur la base d'une mesure, 0,1996 d'exactitude sur `polviews`, soit
moins que la modalite majoritaire a 0,2880. **Les deux rapports du projet se contredisent sur
un point qui commande l'hypothese 2.** A trancher avant toute redaction, et le meilleur moyen
est de retrouver le fichier d'invite dans le paquet OSF plutot que de deduire.

## H3. La temperature ou le mode de lecture

**CONTREDITE pour le signe du terme inter. SOUTENUE pour le niveau du terme intra.**

Sur le signe :

- Chen mesure `Delta eta^2` en mode texte et en mode probabilites, seize cellules, **toutes
  positives**. Pour Sonnet sur le GSS, le mode probabilites gonfle davantage, +0,104 contre
  +0,081. Le mode de lecture ne renverse rien.
- Bisbee a temperature 1 et PSII a temperature 0,7 sont dans deux camps opposes, ce qui exclut
  une lecture par la temperature seule, d'autant que la difference est faible.
- a1 mesure les deux signes sur des conditions produites par le meme pipeline, donc a
  temperature constante.

Sur le niveau du terme intra, en revanche, les deux camps sont d'accord et le disent :

- Bisbee, note 19 : "the strong positive association between this hyperparameter and the
  empirical variance of the synthetic data".
- PSII, baseline High-Temp a temperature 2 : ED de Qwen2.5-7B passe de 0,7340 a 0,5778, soit un
  rapprochement de l'entropie humaine. Mais les auteurs refusent d'en faire une solution :
  "High-temperature decoding performs relatively well on Mistral-24B, but degrades substantially
  on other models, indicating that uncontrolled randomness alone does not provide a robust or
  general solution for realistic opinion simulation." [CONFIRME, section 5]

**C'est exactement le corollaire de PASSATION.md section 5, et il est maintenant appuye par deux
sources externes : la temperature est un dilatateur de variance, pas un transporteur de
variance.** Elle remonte la dispersion totale sans deplacer quoi que ce soit de l'inter vers
l'intra. Ce point est desormais citable.

## H4. La generation du modele, 2023 contre 2025

**CONTREDITE.**

Le camp du gonflement couvre GPT-3.5 Turbo en 2023 chez Bisbee, Claude Sonnet 4.6 et Haiku 4.5
en 2026 chez Chen, et Llama-3.1-8B chez Chen et chez LifeMem. Le camp de l'aplatissement, PSII,
emploie Qwen2.5-7B et 14B, Mistral-24B et **Llama-3.1-8B-Instruct**, c'est a dire **le meme
modele exact** que Chen et LifeMem. Un modele identique se retrouve des deux cotes. La
generation ne separe pas.

## H5. La metrique : ecart de moyennes contre information mutuelle contre ICC

**SOUTENUE, et c'est la seule hypothese de la liste que les faits confirment.**

Le classement des travaux par metrique reproduit exactement le classement par camp.

| famille de metrique | separe inter et intra ? | travaux | sens rapporte |
|---|---|---|---|
| composante de variance rapportee a l'humain | oui | a1, Chen `Delta eta^2` | gonflement |
| ecart de moyennes de groupe rapporte a l'humain | oui | Bisbee, Chen `gap` | gonflement |
| ecart type de moyennes de groupe, sans signe | oui mais non signe | Kim et Lee | indetermine |
| ICC, rapport inter sur total | non, c'est un rapport | Garzon | indeterminable, pas de referent humain |
| divergence KL de population, ecart d'entropie de population | **non** | PSII | aplatissement |
| dispersion totale des etats caches, rayon kNN | **non** | PSII figure 1 | aplatissement |
| distance appariee intra groupe | mesure l'intra seulement | LifeMem | ecrasement intra |
| silhouette | mesure une separation, mais globale sur tous les items | LifeMem, a1 | 0,19 chez LifeMem, non retrouve par a1, max 0,079 |

**Toute metrique globale de dispersion enregistre un aplatissement, y compris sur nos propres
donnees.** a1 section 3, colonne "ce que voit une mesure globale" : 0,90 pour les agents
composite, 0,84 pour les agents enquete, 0,80 pour la variante `v8` qui gonfle pourtant l'inter
d'un facteur 5,9. **Un lecteur qui n'aurait de nos donnees que cette colonne ecrirait exactement
la phrase du resume de PSII.**

---

# 6. La variable qui separe reellement, et deux variables non listees

## 6.1 L'axe de segmentation

Les cinq hypotheses proposees ne rendent pas compte des faits. Une sixieme le fait, et elle
n'etait pas dans la liste.

| travail | axe de segmentation employe | sens |
|---|---|---|
| Chen, GSS | **political views** | gonflement 2,3 |
| Bisbee | **race x partisanship** | gonflement |
| a1, tous | **ideologie**, colonne dediee | 2,09 a 8,51 chez les conditions qui gonflent |
| a1, tous | genre, age | **0,72 a 1,36**, donc au voisinage de 1 ou en dessous |
| PSII | sexe, immigration, marital, education, emploi, profession, revenu, religion. **aucun axe politique** | aplatissement affirme |
| LifeMem | sexe, naissance, marital, emploi, religion, diplome. **aucun axe politique** | aucun inter publie |
| Garzon | **age x genre seulement** | indeterminable |

**Le partage est net.** Les travaux qui segmentent sur un axe politique mesurent un gonflement.
Ceux qui segmentent sur des axes demographiques non politiques ne publient pas de terme inter,
ou concluent a l'aplatissement depuis une mesure globale. Et **nos propres donnees reproduisent
le partage a l'interieur d'une seule condition** : la condition enquete gonfle l'ideologie de
2,49 et aplatit le genre a 0,80 et l'age a 0,78.

C'est ce que a1 section 4 avait deja ecrit sous une autre forme : "Le gonflement n'est pas
demographique en general, il est politique." Ce rapport ajoute que **cette phrase explique aussi
la litterature, et pas seulement nos chiffres**.

Le seul contre exemple est le silhouette de 0,19 de LifeMem, sur des tertiles de statut socio
economique dans le WVS, axe non politique. a10 section 1.b a montre que sur le WVS cet axe
proxie le pays, et que la separation mesuree capte une part de la separation nationale. Le
contre exemple porte donc peut etre sur un axe politique deguise [HYPOTHESE, l'analyse est de
a10 et n'a pas ete refaite ici].

## 6.2 Deux variables qui n'etaient dans aucune liste

**La personne grammaticale de l'invite.** Bisbee, note 23, compare "You are a ..." et "I am a
...", et trouve "less evidence of exaggerated polarization" a la premiere personne, au prix
d'une exactitude degradee. Ils rattachent l'effet a un resultat de psychologie sociale de 2016 :
demander a un humain d'estimer les attitudes d'autrui produit une estimation exageree de la
polarisation. **Aucun autre travail du corpus ne controle cette variable, et notre a5 est a la
troisieme personne** : "You are simulating one specific person answering a survey. Answer
exactly as this person would answer, not as you would." [source interne,
`analyses/a5_agents_locaux_gss.py`, constante `PREAMBULE`]

**L'existence meme d'une persona.** Le baseline "Direct" de PSII n'a pas de persona du tout, les
100 agents recoivent une invite identique. L'ecart entre groupes y est nul par construction.
C'est le seul regime ou "flattened inter-group differences" est indiscutable, et il ne
correspond a aucun protocole que le champ utilise serieusement pour simuler des individus.

---

# 7. Ce que popsim peut ecrire de la contradiction

## 7.1 La phrase de synthese, en francais

> Le sens de la distorsion inter groupes n'est pas une propriete des modeles de langage mais du
> dispositif de mesure : sans persona, la population simulee n'a aucun ecart entre groupes a
> montrer et toute metrique globale de dispersion enregistre un aplatissement ; des qu'une
> identite de groupe conditionne la reponse, l'ecart entre groupes est gonfle sur les axes
> politiquement charges pendant qu'il reste au voisinage de la fidelite sur le genre et l'age,
> et la dispersion interne reste ecrasee dans les deux cas, si bien qu'une metrique globale
> continue d'enregistrer un aplatissement.

Elle tient devant les deux camps parce qu'elle ne conteste aucune de leurs mesures : elle
explique pourquoi ils mesurent des choses differentes.

## 7.2 La meme chose en anglais, pour le related work

> Reports of "flattened" and "exaggerated" inter-group differences are not in conflict: they are
> measured on different quantities and on different axes. Population-level divergence and
> entropy metrics, and hidden-state dispersion, pool the between-group and the within-group
> terms and therefore register the within-group collapse as an overall flattening. When the
> between-group term is isolated and referenced to human data, it is inflated on politically
> charged partitions and close to fidelity on gender and age. We report both terms separately,
> per axis, against a measured human test-retest floor.

## 7.3 Trois phrases interdites, desormais

1. Ne pas ecrire que PSII contredit la these du projet. Son introduction affirme, sur le regime
   de la persona par invite, que la methode "exaggerates between-group differences". Ce qu'il
   contredit, c'est une formulation qui ne distinguerait pas les regimes.
2. Ne pas ecrire que "la richesse de l'invite explique le sens". Les faits la contredisent dans
   les deux directions.
3. Ne pas citer le facteur 1,60 de Bisbee comme un ratio inter groupes. C'est le ratio d'une
   variation temporelle d'ecart, pas d'un ecart.

## 7.4 Deux gains nets pour le dossier

**Bisbee et al. 2024 devient la premiere source du corpus qui publie les deux termes avec
referent humain.** Elle est anterieure de deux ans a LifeMem, gratuite, dans une revue de
methodologie, et son ratio d'ecarts types 16,1 sur 31,4 egale 0,513, dans la fourchette "0,40 a
0,56" de PASSATION.md. La revendication de a13, "la premiere mesure conjointe des deux termes
rapportee a un plafond humain mesure", doit donc etre **restreinte encore une fois** : ce qui
reste vrai est que Bisbee ne pose aucune identite additive, ne place pas les humains en (1,1),
ne mesure sur qu'une seule quantite construite, la polarisation affective, et **n'a pas de
plafond humain test retest**. C'est ce dernier point qui reste entierement a nous.

**L'indice de stereotypage de Chen, `Delta eta^2`, est notre ratio inter sous une autre forme.**
La difference `eta^2_model - eta^2_human` et notre `inter_model / inter_human` sont deux
fonctions du meme couple de quantites. Publier les deux formes dans le meme tableau rend nos
chiffres directement comparables aux seize cellules de Chen, ce qui est le geste de
positionnement le moins cher restant.

---

# 8. Ce qu'il faut mesurer chez nous, et le contraste exact a regarder au matin

Le run a5 tourne depuis le 7 septembre 22 h 45 et s'arrete de lui meme le 8 septembre a 07 h 30.
Configuration : Qwen3-4B-Instruct-2507 Q4_K_M, **temperature 0**, `n_probs` 40, `n_predict` 1,
distribution complete lue sur les K lettres d'options, 150 personnes, 149 items, C2 puis C3
passe 1. [source interne] `resultats/a5-agents-locaux-gss.md` sections 1 et 2.

**Ce que les deux conditions valent comme test des hypotheses.**

- **C2** contient les onze attributs de `demographic_summary.csv`, dont `political_ideology` et
  `political_party`, ecrits en clair. [CONFIRME, `analyses/a5_agents_locaux_gss.py`, constante
  `ETIQUETTES_DEMOGRAPHIQUES`] C'est donc une persona demographique **avec** ideologie, du meme
  type que celle de Chen et celle de Bisbee.
- **C3** contient les ~119 reponses d'enquete de la personne et **aucune demographie**. C'est
  l'equivalent de la condition `survey_agents` de Stanford, celle qui gonfle l'axe ideologique
  de 2,49 sans jamais recevoir d'etiquette.

Le couple C2 contre C3 est donc **le plan qui manque a la litterature entiere** : deux invites
sur les memes 150 personnes, les memes 149 items, le meme modele, la meme temperature, la meme
lecture, differant sur la presence des etiquettes de groupe.

## Les cinq contrastes a regarder, dans l'ordre

**Contraste 1, le plus important : le ratio inter par axe, C2 contre C3, colonne ideologie
contre colonnes genre et age.**
Passer les traces `data/traces/a5-C2-p1.jsonl` et `a5-C3-p1.jsonl` dans la meme decomposition
que a1, avec les humains de la vague 1 restreints aux memes 150 personnes comme referent.
Trois issues, trois conclusions distinctes.

- Si **C2 gonfle sur l'ideologie et reste au voisinage de 1 sur genre et age**, et si C3 fait de
  meme mais moins, alors la variable qui separe est bien **l'axe de segmentation** et non le
  contenu de l'invite. C'est le resultat attendu par ce rapport et il valide la phrase de
  synthese de 7.1.
- Si **C2 gonfle uniformement sur tous les axes et C3 sur aucun**, alors c'est **l'etiquette de
  groupe dans l'invite** qui commande, H2 elargie est soutenue, et la phrase de synthese doit
  etre reecrite autour de l'etiquette et non de l'axe.
- Si **C2 et C3 gonflent tous deux l'ideologie a un niveau comparable**, alors ni l'etiquette ni
  la richesse ne commandent : le modele reconstruit l'ideologie a partir des reponses et
  essentialise ensuite. C'est le resultat le plus interessant scientifiquement et le plus
  difficile a defendre, parce qu'il demande de montrer que C3 a bien reconstruit l'ideologie.

**Le controle qui va avec, gratuit.** Pour C3, verifier l'exactitude du modele sur les items
retires de la cible mais presents en contexte, ou mieux, mesurer la correlation entre
l'ideologie predite implicitement par C3 et l'ideologie declaree. Si C3 gonfle l'axe ideologique
sans jamais avoir vu l'etiquette, cette correlation est le mecanisme, et elle se calcule sans un
appel de modele supplementaire.

**Attention a une asymetrie qu'il faut ecrire et non cacher.** Pour C2, l'axe de segmentation
`political_ideology` est **dans l'invite**. Mesurer un gonflement sur un axe fourni au modele
n'est pas la meme chose que le mesurer sur un axe qu'il doit inferer. C'est le meme dispositif
que Chen et que Bisbee, donc comparable a eux, mais la reserve doit figurer dans le rapport. Pour
C3, l'axe n'est pas dans l'invite, et c'est ce qui fait sa valeur.

**Contraste 2, le plus rentable au regard du cout : argmax contre distribution, sur les memes
traces.**
a5 conserve la distribution complete sur les K lettres a chaque appel. La decomposition inter et
intra peut donc etre calculee **deux fois sans un seul appel supplementaire** : une fois sur la
reponse durcie par argmax, comparable au style A de Chen et aux reponses humaines, une fois sur
la distribution, comparable au style C. Chen predit que le signe ne change pas et que le mode
distributionnel gonfle au moins autant, +0,104 contre +0,081 pour Sonnet. **Si nous retrouvons
ce fait sur un modele de 4 milliards de parametres en local, l'hypothese 3 est close et nous
sommes le seul travail a l'avoir teste a modele, temperature et donnees constants.** C'est la
mesure la moins chere de tout le dossier.

Le rapport a5 signale deja l'ecart, section 3, sur le smoke test : la condition C2 conserve 81,7
pour cent de sa masse de probabilite sur l'argmax et se prononce a plus de 0,99 sur 82,2 pour
cent des appels. **A temperature 0 et avec cette calibration, la mesure distributionnelle sera
proche de la mesure argmax.** C'est une limite a annoncer d'avance, pas une raison de ne pas
faire la mesure.

**Contraste 3 : la mesure "a la Chen", sur C2 et C3.**
Pour chaque item et chaque axe, la difference `max_g p_g - min_g p_g` de la proportion de
repondants dans le haut de l'echelle, chez les humains et chez nos agents, puis la mediane du
rapport. C'est le seul chiffre directement comparable a 2,3. a10 section 1.c le recommande deja
pour a1 ; le faire simultanement sur C2, C3 et les six conditions de Stanford donne huit points
sur la meme regle graduee que Chen. Ajouter `Delta eta^2` au passage, qui est la meme famille et
ne coute rien de plus.

**Contraste 4 : le terme intra a temperature 0 contre le terme intra de Stanford.**
Nos agents tournent a temperature 0, le minimum de dispersion. Les conditions de Stanford sont a
0,637 a 0,885. Si C2 ressort nettement en dessous de cette bande sur l'intra tout en restant
dans la bande sur l'inter, cela isole la temperature comme un levier purement intra, ce qui est
la moitie soutenue de l'hypothese 3 et le corollaire du "transport a somme constante". **C'est
un resultat publiable a lui seul et il tombe gratuitement du run en cours.**

**Contraste 5, a ne pas oublier : C2 n'est pas une replication de l'agent demographique de
Stanford.**
C2 contient l'ideologie et le parti ; a2 a mesure que l'agent demographique de Stanford ne les
avait probablement pas. Presenter C2 comme une replication serait faux. C2 est **la variante
augmentee de l'ideologie**, et c'est justement ce qui en fait un test.

## Ce qu'il faut lancer ensuite, et rien d'autre

La passe 2 de C3 corrige un biais de position et double le cout de C3. Elle ne sert pas cette
question. **La priorite du 8 septembre au matin est un script d'analyse jetable sur les traces
existantes, pas un run de plus.** Les cinq contrastes ci dessus ne demandent aucun appel de
modele supplementaire.

---

# 9. Ce que je n'ai pas pu verifier

1. **Le materiel supplementaire de Bisbee et al.** Le PDF de l'article, gratuit, ne le contient
   pas. Les sections "SI Section 2" sur la temperature, "SI Section 3" sur la premiere personne
   et "SI Section 9.3" sur la variation posterieure sont donc citees d'apres le corps de
   l'article et non lues. **Le lien de replication Dataverse https://doi.org/10.7910/DVN/VPN481
   n'a pas ete ouvert.** Tant que "SI Section 2" n'est pas lu, l'association temperature vers
   variance est un fait rapporte par les auteurs, pas un fait verifie.
2. **Les figures A13 et A14 de Kim et Lee.** Elles portent les valeurs de Spearman et d'erreur
   absolue moyenne qui chiffreraient leur resultat inter et intra. Le HTML arXiv en donne les
   legendes mais pas les valeurs numeriques, qui sont dans l'image. **Aucun signe n'est donc
   disponible pour leur terme inter, et le mot "well" ne peut pas etre converti en chiffre.**
3. **Le tableau A15 de Kim et Lee**, qui contient les trois conditions d'invite pour GPT-4o et
   Gemini-2.5-flash. Seules les valeurs citees dans le corps ont ete relevees, et elles ne
   portent que sur l'exactitude et le F1.
4. **Le contenu exact des invites de `gss_v6` et `gss_v8`** dans le paquet OSF. C'est le point
   qui bloque l'hypothese 2 et il est verifiable localement, sur des fichiers deja telecharges.
   **a1 et a2 se contredisent dessus et je n'ai pas ouvert le paquet.**
5. **La figure 2 de Bisbee et al.** Les valeurs numeriques des moyennes par groupe race x
   partisanship sont dans l'image du PDF, pas dans le texte extrait. Les affirmations "0.5 to 1
   standard deviations" et "10 to 20 points" sont donc reprises telles quelles du corps du
   texte, sans lecture des points.
6. **La metrique de dispersion spatiale de la figure 1 de PSII.** Le rayon kNN est defini dans
   l'annexe E.4, mais la valeur de `k` n'est donnee nulle part dans le texte extrait.
7. **LifeMem** n'a pas ete relu pour ce rapport au dela de son resume. La lecture de a13 fait
   foi.
8. **Le sens du terme inter chez Garzon et al.** reste indeterminable, faute de referent humain
   dans leur papier. Ce n'est pas une limite de ma lecture, c'est une limite de leur protocole,
   qu'ils reconnaissent.

---

# 10. Questions ouvertes pour Simon

1. **La contradiction est desamorcee, mais faut il l'exposer ?** Ecrire dans le papier que le
   resume de PSII n'est pas soutenu par ses propres mesures est un geste couteux envers une
   equipe de Tsinghua active dans le champ. La formulation neutre existe : dire que les deux
   camps mesurent des quantites differentes, sans dire que l'un se trompe. Laquelle des deux ?
2. **L'axe de segmentation devient la variable centrale du papier. Est ce defendable ?**
   L'ideologie politique n'est pas une variable demographique, c'est une attitude auto declaree,
   reserve que a1 section 4 pose deja. Si l'effet principal du papier repose sur un axe
   attitudinal, un relecteur de sciences sociales objectera que nous predisons des attitudes a
   partir d'une attitude. Faut il un second axe non attitudinal qui gonfle, comme la religion ou
   le milieu de residence, pour tenir ?
3. **Bisbee 2024 retire une revendication de plus. Que reste il exactement ?** Apres LifeMem,
   Garzon, Kim et Lee et maintenant Bisbee, la contribution s'est reduite trois fois. Ce qui
   reste tient en deux points : le plafond humain test retest a deux semaines, et la dissociation
   entre exactitude et structure a un facteur 13,5. Est ce assez pour un papier, ou faut il
   basculer vers le chantier 3, le retrecissement calibre, qui reste sans precedent ?
4. **La contradiction interne entre a1 et a2 sur le contenu de l'invite demographique de
   Stanford.** Elle se tranche en ouvrant un fichier. Qui le fait, et faut il refaire les
   chiffres de a1 si a2 a raison ?
5. **Le contraste C2 contre C3 est le plan que la litterature n'a pas fait. Faut il le
   sanctuariser comme resultat principal ?** Il est bon marche, il tourne deja, et il repond a la
   question que ce rapport laisse ouverte. Mais il porte sur un modele de 4 milliards de
   parametres en Q4, ce qu'un relecteur qualifiera de jouet. Faut il prevoir d'emblee une
   replication sur un modele de 8 a 14 milliards avant de l'annoncer, ou publier le petit et
   annoncer la replication ?

---

## Fichiers et sources

| source | URL |
|---|---|
| PSII, arXiv 2603.16142 v2 | https://arxiv.org/html/2603.16142v2 |
| Kim et Lee, arXiv 2305.09620 v4 | https://arxiv.org/html/2305.09620v4 |
| Bisbee et al. 2024, PDF gratuit | https://www.cambridge.org/core/services/aop-cambridge-core/content/view/B92267DC26195C7F36E63EA04A47D2FE/S1047198724000056a.pdf/synthetic-replacements-for-human-survey-data-the-perils-of-large-language-models.pdf |
| Bisbee et al. 2024, page de revue | https://www.cambridge.org/core/journals/political-analysis/article/synthetic-replacements-for-human-survey-data-the-perils-of-large-language-models/B92267DC26195C7F36E63EA04A47D2FE |
| Bisbee et al., donnees de replication, non ouvertes ici | https://doi.org/10.7910/DVN/VPN481 |
| Chen, Zhu, Zheng, arXiv 2607.26348 v1 | https://arxiv.org/html/2607.26348v1 |
| LifeMem, arXiv 2608.19621 | https://arxiv.org/abs/2608.19621 |
| Garzon et al., arXiv 2605.16303 | https://arxiv.org/html/2605.16303 |

Aucun fichier existant du depot n'a ete modifie. Aucun fichier de donnees n'a ete cree.
