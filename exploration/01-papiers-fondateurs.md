# 01. Papiers fondateurs, fiches de lecture

Agent 1 de l'exploration popsim. Rediges le 2 septembre 2026.
Regles de redaction : voir CONTEXTE.md. Chaque affirmation non triviale porte
[CONFIRME] avec URL, [PROBABLE] avec raisonnement, ou [HYPOTHESE] non verifiee.
Un quatrieme tag est utilise ici : [CALCUL PROPRE] pour les chiffres que j'ai
calcules moi meme a partir de donnees publiques, avec la methode indiquee pour
que le calcul soit refait.

---

## Resume en tete

1. Le papier de reference existe, mais il a change de titre et de contenu.
   Il ne s'appelle plus "Generative Agent Simulations of 1,000 People".
2. Le chiffre de 85 pour cent n'est plus le chiffre du papier. La version
   courante donne 83 pour cent pour les agents batis sur entretien, 82 pour cent
   pour les agents batis sur questionnaire seul, 86 pour cent pour la
   combinaison des deux, contre 74 pour cent pour la ligne de base demographique.
3. L'URL fournie par le porteur du projet existe bel et bien, mais elle pointe
   vers un poster CHI de 6 pages avec N=30 personas synthetiques, pas vers le
   papier phare. Ses auteurs sont bien a Stanford, mais ce ne sont pas ceux du
   papier phare, et leur r de 0,59 n'est pas une exactitude : il n'est pas
   comparable au 86 pour cent, il ne mesure meme pas la meme chose. Voir b.5.
4. Il existe une archive publique, gratuite et deja telechargee qui contient les
   reponses individuelles reelles des 1 052 participants (vague 1 et vague 2)
   plus les reponses des cinq conditions d'agents. C'est la trouvaille la plus
   importante de cette fiche pour une contrainte de budget zero.
5. Sur ces donnees, j'ai mesure l'ecrasement de variance que le projet vise a
   attaquer. Il est massif et chiffrable des maintenant.
6. Le papier Nature en psychiatrie n'existe probablement pas sous cette forme.
   Le candidat le plus vraisemblable est un papier Nature d'aout 2026 en sciences
   sociales, coauteur Robb Willer, avec un r de 0,85. Voir le tableau des trois
   "85" en c.3, c'est un piege de communication a desamorcer tot.

---

# (a) FICHE 1. Le papier Stanford de reference

## a.1 Identite exacte, et le piege du titre

[CONFIRME] L'identifiant arXiv 2411.10109 est le bon, mais l'objet a change trois
fois. Page de reference : https://arxiv.org/abs/2411.10109

| Version | Date | Titre |
|---|---|---|
| v1 | 15 novembre 2024 | Generative Agent Simulations of 1,000 People |
| v2 | 22 avril 2026 | LLM Agents Grounded in Self-Reports Enable General-Purpose Simulation of Individuals |
| v3 | 28 juin 2026 (courante) | LLM Agents Grounded in Self-Reports Enable General-Purpose Simulation of Individuals |

[CONFIRME] Auteurs v1 (https://arxiv.org/abs/2411.10109v1) : Joon Sung Park,
Carolyn Q. Zou, Aaron Shaw, Benjamin Mako Hill, Carrie Cai, Meredith Ringel
Morris, Robb Willer, Percy Liang, Michael S. Bernstein. Neuf auteurs.

[CONFIRME] Auteurs v3 (PDF telecharge depuis https://arxiv.org/pdf/2411.10109) :
Joon Sung Park (Stanford, CS), Carolyn Q. Zou (Stanford CS et Northwestern),
Jonne Kamphorst (CDSP et CEE, Sciences Po, Paris), Niles Egan (Stanford CS),
Aaron Shaw (Northwestern), Benjamin Mako Hill (University of Washington),
Carrie Cai (Google DeepMind), Meredith Ringel Morris (Google DeepMind),
Percy Liang (Stanford), Robb Willer (Stanford, Sociologie), Michael S. Bernstein
(Stanford). Onze auteurs. Deux nouveaux entrants : Kamphorst et Egan.
Auteurs correspondants : Park et Kamphorst.

Consequence operationnelle. Citer "Generative Agent Simulations of 1,000 People,
2024" devant un jury MIT en septembre 2026 signalerait qu'on a lu la version
perimee. La bonne citation est la v3 de juin 2026. Le changement de titre n'est
pas cosmetique : le papier a bascule d'une revendication sur la simulation de
personnes vers une revendication sur la valeur des donnees d'auto-declaration.

## a.2 Lisa Argyle, la confusion a eviter

[CONFIRME] Lisa P. Argyle n'est pas autrice du papier Stanford. Elle est premiere
autrice de : Argyle, Busby, Fulda, Gubler, Rytting, Wingate, "Out of One, Many:
Using Language Models to Simulate Human Samples", Political Analysis 31(3),
337 a 351, 2023. Preprint : https://arxiv.org/abs/2209.06899
Version editeur : https://www.cambridge.org/core/journals/political-analysis/article/abs/out-of-one-many-using-language-models-to-simulate-human-samples/035D7C8A55B237942FB6DBAD7CAA4E49

Distinction de fond, et elle compte pour popsim :

| | Argyle et al. 2023 | Park et al. 2024 a 2026 |
|---|---|---|
| Unite simulee | un sous groupe demographique | un individu nomme |
| Conditionnement | "backstories" socio demographiques | transcript d'entretien de 2 h et/ou questionnaires |
| Metrique | fidelite de la DISTRIBUTION agregee ("algorithmic fidelity") | exactitude sur les reponses INDIVIDUELLES tenues cachees |
| Modele | GPT-3 | GPT-4o |

[CONFIRME] Argyle et al. est cite en reference 2 du papier Stanford, et sert
explicitement de source pour la construction de la ligne de base "demographic
based agents". Autrement dit, dans Park et al., Argyle est le baseline a battre,
pas la methode retenue. C'est ce baseline qui plafonne a 74 pour cent.

Si le porteur du projet melange les deux, le risque est concret : il croirait
que le 85 pour cent est atteint par du prompt demographique, alors que c'est
precisement la condition qui echoue et qui produit l'ecrasement de variance que
popsim veut attaquer.

## a.3 Le protocole d'entretien

Toutes les valeurs de cette section sont [CONFIRME], extraites du PDF v3
(https://arxiv.org/pdf/2411.10109), sections "Materials and Methods Summary" et
"Supplementary Materials 1 et 2".

| Element | Valeur |
|---|---|
| Echantillon final | N = 1 052 adultes americains |
| Recrutes en phase 1 | 1 300 (attrition anticipee de 20 pour cent, moins d'abandons que prevu, redescendus a 1 052 pour preserver la representativite) |
| Recruteur | societe d'etudes Bovitz |
| Stratification | age, race, genre, region de residence, niveau d'education, identification partisane. Quotas census nationaux |
| Criteres d'inclusion | 18 ans ou plus, resident aux Etats Unis. Rien d'autre |
| Duree d'entretien | environ 2 heures, voix a voix, en anglais |
| Qui menait l'entretien | un agent IA autonome, PAS un humain |
| Script | protocole de l'American Voices Project, adopte tel quel |
| Longueur de transcript | 6 491 mots en moyenne, ecart type 2 541 |
| Remuneration | 60 dollars phase 1, 30 dollars phase 2, plus bonus de 0 a 10 dollars selon les jeux economiques |
| Vague 2 | memes questionnaires et experiences, deux semaines plus tard, sans entretien |
| Age moyen | 47,55 ans, ecart type 15,93, min 18, max 84 |
| Genre | 593 femmes, 459 hommes |
| Ethnicite | 833 blancs, 154 noirs, 53 asiatiques, 95 autres (choix multiples possibles) |
| Ethique | plus de six mois de travail avec l'IRB sur la procedure de consentement. Droit de retrait honore pendant 25 ans |

Le point le plus sous estime : **l'entretieneur est une IA**. [CONFIRME] Le
papier decrit un agent interviewer construit sur une variante de l'architecture
des generative agents, alimente par Whisper pour la reconnaissance vocale, GPT-4o
pour le moteur de decision et une synthese vocale pour la restitution. Il suit
un script fixe mais genere des relances adaptatives en temps reel, avec un budget
de mots par module et une limite de temps par question pour tenir dans les deux
heures sans couper la parole au participant. Un module de reflexion resume
l'entretien en cours pour mieux formuler les relances.

Consequence pour popsim : la couche "recruter et faire parler des humains" est
la seule qui coute vraiment cher, mais la couche "mener un entretien de qualite"
est deja automatisee et le code est publie (voir a.7). Le gout de la contrainte
"aucun humain recrute" est donc moins amer qu'il n'y parait : ce n'est pas la
competence d'entretien qui manque, c'est l'acces aux sujets.

[CONFIRME] Le script AVP est documente publiquement par Stanford :
https://inequality.stanford.edu/avp/methodology
[CONFIRME] Les donnees AVP elles memes sont sous acces controle, pas en
telechargement libre : https://inequality.stanford.edu/data/american-voices-project-data

## a.4 La methode d'injection exacte

Reponse courte : ce n'est ni du RAG, ni du fine tuning, ni une memoire vectorielle.
C'est **le transcript integral dans le prompt, plus une couche de reflexions
pre calculees, plus une chaine de pensee en quatre etapes**. [CONFIRME], PDF v3,
SM section 3 "Generative Agent Architecture".

Mecanisme precis, dans l'ordre :

1. **Memoire = donnee brute**. Le transcript d'entretien complet et/ou les
   reponses aux questionnaires sont places tels quels dans la memoire de l'agent.
   Aucun decoupage en chunks, aucune recherche par similarite sur le transcript.

2. **Expert reflection, hors ligne, une seule fois par participant**. On prompte
   GPT-4o avec les donnees du participant en lui demandant d'endosser quatre
   personas d'expert : psychologue, economiste comportemental, politiste,
   demographe. Chaque expert produit entre 5 et 20 observations. Prompt cite
   verbatim dans le papier, exemple pour le demographe : "Imagine you are an
   expert demographer (with a PhD) taking notes while observing this interview.
   Write observations/reflections about the interviewee's demographic traits and
   social status." Les quatre jeux de reflexions sont stockes.

3. **Routage au moment de la question**. On demande au modele de classifier quel
   expert est le mieux place pour repondre a la question posee, puis on recupere
   **toutes** les reflexions de cet expert. C'est la seule etape qui ressemble a
   de la recuperation, et elle porte sur les reflexions, pas sur le transcript.

4. **Prompt final et chaine de pensee en 4 etapes** : Option Interpretation,
   Option Choice, Reasoning, Response. Pour les reponses numeriques, une variante
   en 3 etapes.

Taille de contexte impliquee. [CALCUL PROPRE] 6 491 mots de transcript en moyenne,
soit de l'ordre de 8 500 a 9 500 tokens, plus les reflexions d'un expert (jusqu'a
20 observations), plus le prompt de tache. On est donc typiquement entre 10 000 et
15 000 tokens en entree par question posee. C'est parfaitement dans la fenetre de
n'importe quel modele ouvert moderne. Aucune contrainte de contexte long
n'interdit la reproduction en local.

[CONFIRME] Le fine tuning a ete teste et il DEGRADE le resultat. GPT-4o fine tune
sur 500 agents et evalue sur les 552 restants : exactitude normalisee 0,79.
Le meme modele non fine tune avec le prompt du papier complet : 0,84. Point
important pour popsim, qui pourrait etre tente d'aller vers l'entrainement.

[CONFIRME] Ablations qui changent l'arbitrage cout / performance :
- Retirer 80 pour cent du transcript au hasard, soit 96 minutes sur 120 :
  exactitude normalisee GSS de 0,83 a 0,79, correlation Big Five de 0,80 a 0,73.
- Remplacer le transcript par un resume en puces genere par LLM, ce qui detruit
  les indices linguistiques et ne garde que le contenu factuel : 0,81 sur le GSS,
  0,70 sur le Big Five.

Lecture : **quatre cinquiemes du transcript ne servent presque a rien**. Un
entretien de 24 minutes vaut 0,79 la ou 120 minutes valent 0,83. C'est un levier
direct sur le cout d'une collecte future.

## a.5 Les conditions comparees et les ecarts

[CONFIRME] Cinq conditions d'agents, plus deux reperes (aleatoire, et les humains
face a eux memes). Evaluation principale sur 150 questions du core GSS
(177 categorielles retenues au depart, dont 27 retirees pour cause de synonymie
avec des questions d'entretien). Moyenne de 3,31 options par question, ecart type
1,58, donc une exactitude au hasard de 0,30.

### GSS, exactitude normalisee

| Condition | Exactitude normalisee | Ecart type |
|---|---|---|
| Survey + Interview (composite) | **0,86** | 0,09 |
| Interview seul | 0,83 | 0,11 |
| Survey seul | 0,82 | 0,11 |
| Demographique | 0,74 | 0,12 |
| Persona (paragraphe redige par le participant) | 0,71 | 0,12 |
| Aleatoire | environ 0,30 en brut | |

Detail du calcul de la ligne "Interview" : exactitude brute 65,67 pour cent
(ecart type 6,51) divisee par la coherence interne des participants de
**79,53 pour cent** (ecart type 8,65), ce qui donne 0,83.

[CONFIRME] ANOVA a un facteur sur les cinq conditions : F(4, 5255) = 577,83,
p < 0,001. Tukey post hoc : interview, survey et composite battent chacun
demographique et persona (tous p < 0,001) ; interview et survey ne se
distinguent pas entre eux (p = 0,16) ; composite bat les deux (p < 0,001).

Ecart cle a retenir : **12 points normalises entre le meilleur agent (0,86) et
le baseline demographique (0,74)**, et 15 points face au baseline persona (0,71).
C'est l'espace ou popsim doit se positionner.

### Big Five BFI-44, correlation normalisee

| Condition | Correlation normalisee |
|---|---|
| Interview seul | 0,80 |
| Survey + Interview | 0,77 |
| Persona | 0,75 |
| Survey seul | 0,65 |
| Demographique | 0,61 |

Detail : correlation brute r = 0,78 divisee par la correlation de replication des
participants entre vague 1 et vague 2, r = 0,95.
[CONFIRME] ANOVA F(4, 5255) = 26,66, p < 0,001. Le survey seul ne se distingue
significativement d'aucun des deux baselines. Combiner n'apporte rien face a
l'entretien seul (p = 0,99).

### Jeux economiques, correlation normalisee

| Condition | Correlation normalisee |
|---|---|
| Interview | 0,66 |
| Persona | 0,57 |
| Composite | 0,49 |
| Demographique | 0,48 |
| Survey | 0,38 |

[CONFIRME] ANOVA F(4, 5255) = 1,63, p = 0,16. **Aucune difference significative,
aucun contraste par paires significatif.** Les ecarts types sont enormes (2,79 a
3,01). C'est le trou dans la raquette du papier, et il est explicitement assume.

Consequence pour popsim, cote commercial : le pitch "on remplace votre etude de
marche" repose sur du comportement de choix avec enjeu, pas sur des opinions
declarees. Or c'est exactement la que la litterature fondatrice n'a rien
demontre. A ne pas survendre a Simon ni au MIT.

## a.6 Le protocole d'evaluation et le calcul du 85 pour cent

### La batterie

[CONFIRME] Ordre d'administration en vague 1 : GSS, puis BFI-44, puis cinq jeux
economiques, puis cinq experiences de replication. Ordre des sous composants
randomise pour contrebalancement, sauf le GSS qui suit la sequence recommandee.
Administration en ligne via Qualtrics depuis une plateforme maison.

**GSS.** Core module. Exclusions : questions conditionnelles, questions a plus de
25 options, questions en texte libre. Reste 177 categorielles ou ordinales plus
6 numeriques. Sur ces 177, 27 ont ete retirees a l'evaluation apres un criblage
des 54 694 paires possibles entre items GSS et questions d'entretien, par un
classifieur GPT-4.1 puis revue humaine. Il reste les 150 questions du resultat
principal.

**BFI-44.** John et Srivastava 1998, 44 items, 5 dimensions, echelles de Likert.
Les agents predisent item par item, les scores de dimension sont recalcules
ensuite selon la methode d'agregation d'origine.

**Cinq jeux economiques, avec argent reel :**
1. Dictator Game, dotation de 5 dollars.
2. Trust Game premier joueur, dotation de 3 dollars, montant envoye triple.
3. Trust Game second joueur, restitution.
4. Public Goods Game, 4 joueurs, 4 dollars chacun, pot commun double.
5. Prisoner's Dilemma, matrice 6 / 8 / 2 / 4 dollars.
Un seul jeu, tire au sort a l'avance (le Dictator Game), a servi au calcul du bonus.

**Cinq experiences repliquees**, toutes tirees de l'effort de replication de
Camerer et al. sur 41 etudes PNAS, avec deux criteres de selection annonces
d'avance pour eviter le choix opportuniste (descriptible en langage naturel,
et detectable avec 1 000 participants ou moins) :
1. Ames et Fiske, 2015. Intention percue et attribution du blame.
2. Cooney et al., 2016. Equite percue et reaction emotionnelle.
3. Halevy et Halali, 2015. Benefices percus de l'intervention dans un conflit.
4. Rai et al., 2017. Deshumanisation et disposition a nuire contre remuneration.
5. Schilke et al., 2015. Pouvoir et confiance dans les echanges sociaux.

[CONFIRME] Correlations des tailles d'effet entre agents et humains rapportees
entre r = 0,91 et r = 0,99, avec la reserve explicite des auteurs : un design a
cinq etudes est sous dimensionne pour comparer des tailles d'effet.

### Le calcul du score normalise, en clair

[CONFIRME] Formule exacte, citee du papier :

```
exactitude normalisee = exactitude de prediction de l'agent / coherence interne du participant
```

Le denominateur n'est PAS 100 pour cent. C'est **le taux auquel le participant
redonne la meme reponse a la meme question deux semaines plus tard**, mesure sur
la meme batterie, sur les memes 1 052 personnes.

Numeriquement, pour le GSS :
- Numerateur, agents interview : 65,67 pour cent de reponses exactes.
- Denominateur, humains contre eux memes a deux semaines : **79,53 pour cent**.
- 65,67 / 79,53 = 0,826, arrondi a 0,83.

Ce qu'il faut dire et ne pas dire.
- A dire : "les agents retrouvent 83 pour cent de ce que la personne elle meme
  reproduit de ses propres reponses a quinze jours".
- A ne pas dire : "les agents reproduisent 83 pour cent du comportement". En
  valeur absolue, un agent se trompe sur une question GSS sur trois.
- Le plafond n'est pas 1,0 par magie. Une exactitude normalisee de 1,0
  signifierait que l'agent predit aussi bien que la personne se predit elle meme.
  Rien n'interdit mathematiquement de depasser 1,0 : dans les donnees de
  replication, certaines lignes individuelles depassent 1,0 (j'en ai vu, par
  exemple 1,145 et 1,163 sur des participants isoles).
- Le denominateur bouge selon la construction. Pour le Big Five, le denominateur
  n'est pas une exactitude mais une correlation test retest de r = 0,95.

Trois precautions methodologiques que popsim devra reproduire pour etre credible :
1. Le denominateur est calcule **par individu** puis moyenne, pas globalement.
   Analyse dite "individual level". L'analyse "construct level" existe aussi dans
   le papier mais n'est pas celle du resultat principal.
2. Les correlations sont moyennees apres transformation z de Fisher, pas
   directement.
3. L'exactitude normalisee n'est pas calculable pour les MAE, parce que certains
   participants ont une coherence interne de 0, ce qui annule le denominateur.

### Pourquoi ca marche, la reponse gênante

[CONFIRME] Section "Why do interview-based generative agents work?" du SM.
Mecanisme 1 teste et **confirme** : la recuperation directe de reponses. Pour
59 agents, environ 21 713 paires question GSS / reponse d'entretien ont ete
classifiees par GPT-4o-mini pour savoir si la reponse d'entretien contient deja
l'information. Puis on retire progressivement les questions les plus
"directement repondables". L'exactitude normalisee des agents interview chute,
celle des agents demographiques et persona ne bouge pas.

Traduction brutale : une partie de la performance de l'entretien vient du fait
que la personne a deja donne la reponse, autrement formulee, quelque part dans
ses deux heures de parole. Ce n'est pas de la simulation, c'est de l'extraction.
C'est une faille que popsim peut soit denoncer, soit exploiter, mais pas ignorer.

## a.7 Reduction de biais, Demographic Parity Difference

[CONFIRME] DPD = ecart de performance entre le sous groupe le mieux predit et le
sous groupe le moins bien predit. En points de pourcentage pour le GSS, en
coefficients de correlation pour Big Five et jeux economiques.

### GSS, ideologie politique (le cas le plus spectaculaire)

| Condition | DPD | Groupe le moins bien predit | Groupe le mieux predit |
|---|---|---|---|
| Demographique | 13,75 | conservateur, 49,19 pour cent | extremement liberal, 62,94 pour cent |
| Persona | 13,00 | extremement conservateur, 49,17 | extremement liberal, 62,17 |
| Interview | 8,60 | conservateur, 62,69 | extremement liberal, 71,29 |
| Survey + Interview | 7,09 | extremement conservateur, 66,09 | extremement liberal, 73,18 |
| Survey | 6,22 | extremement conservateur, 62,68 | extremement liberal, 68,90 |

### GSS, parti politique

Demographique 11,26, persona 10,27, interview 6,98, survey + interview 5,38,
survey 5,16. Le groupe systematiquement le plus mal predit : "strong republican".

### GSS, race

3,39 (demographique), 2,22 (interview), 1,95 (survey), 2,49 (composite).

### Big Five, ideologie politique

0,166 (demographique), 0,063 (interview), 0,176 (survey), 0,048 (composite).
A noter : le survey seul est PIRE que le demographique ici.

### Jeux economiques, ideologie politique

0,498 (demographique), 0,194 (interview), 0,216 (survey), 0,214 (composite).
Le detail est eloquent : en condition demographique, le groupe "extremement
conservateur" obtient une correlation de **moins 0,03**. Le modele ne predit pas
seulement mal ce groupe, il le predit a l'envers.

### Genre

Uniformement sous 1 pour cent dans toutes les conditions et toutes les taches.
Rien a exploiter la.

Lecture pour popsim. Le biais politique n'est pas un detail equitable, c'est un
defaut de validite. Un sondage simule par prompt demographique surestime
mecaniquement les liberaux et manque les conservateurs. Pour un client d'etudes
politiques, c'est disqualifiant. C'est un argument de vente aussi bien qu'un
argument scientifique, et il est deja publie, donc gratuit a reutiliser.

## a.8 L'agent bank, le code, les licences, et ce qui est reellement accessible

C'est le point critique compte tenu de la contrainte de budget zero.

### Ce qui n'est PAS accessible

[CONFIRME] https://github.com/StanfordHCI/genagents, README :
"the full agent bank containing over 1,000 generative agents based on real
interviews is not publicly available at the moment". Les transcripts d'entretien
ne sont pas publies et ne le seront probablement jamais en clair.

[CONFIRME] Procedure d'acces : il n'y a **pas** de formulaire, pas de portail,
pas d'URL de demande. Le README dit seulement que les chercheurs interesses par
les reponses individuelles sur taches ouvertes peuvent demander un acces
restreint en contactant les auteurs. Le seul contact publie est
**joonspk@stanford.edu** (Joon Sung Park).

[PROBABLE] Il n'existe donc aucun delai annonce, aucun SLA, aucune condition
publiee. Le canal MIT de Simon est, en l'etat, le seul levier realiste pour
obtenir mieux qu'un mail froid. Je n'ai trouve aucune trace publique d'un
chercheur tiers ayant obtenu cet acces.

### Ce qui EST accessible, gratuitement, tout de suite

**1. Le code des agents.** [CONFIRME] https://github.com/StanfordHCI/genagents
Licence MIT. Contient le module de creation d'agents, le moteur de simulation,
les prompts. Necessite une cle OpenAI, `gpt-4o-mini` par defaut dans la config.
Contient aussi une banque de plus de 3 000 agents demographiques construits sur
des donnees GSS avec noms et adresses fictifs, plus un agent exemple construit
sur l'entretien d'un des auteurs (`agent_bank/populations/single_agent/`).

**2. Le code de l'entretieneur IA.** [CONFIRME]
https://github.com/joonspk-research/generative_agent
C'est le depot cite par le papier v3 pour la creation des agents d'entretien,
entretieneur IA inclus. Je n'ai pas verifie son contenu ligne a ligne.

**3. L'archive de replication OSF. C'est la trouvaille.**
[CONFIRME] https://osf.io/t6g7k/files/osfstorage
Projet OSF public (verifie via https://api.osf.io/v2/nodes/t6g7k/, champ
`"public": true`), cree et modifie le 21 avril 2026, intitule "LLM Agents
Grounded in Self-Reports Enable General-Purpose Simulation of Individuals".

L'archive ne contient qu'un seul fichier, `replication_instructions.rar`,
3,4 Mo, telechargeable sans compte a l'adresse
https://osf.io/download/69e74db2344ec3e0a3fd877d/
Je l'ai telecharge et decompresse. Contenu verifie, 203 entrees :

| Contenu | Detail |
|---|---|
| `figure2/data/.../gss_filtered/preparation/` | 8 fichiers CSV, **1 052 lignes, 178 colonnes chacun** |
| dont `p_wave1_summary.csv` | les reponses GSS reelles des 1 052 participants, vague 1 |
| dont `p_wave2_summary.csv` | les memes, vague 2, deux semaines plus tard |
| dont `gss_v3_summary.csv` | reponses des agents interview |
| dont `gss_v6_summary.csv` | reponses des agents demographiques |
| dont `gss_v7_summary.csv` | reponses des agents persona |
| dont `survey_agents_summary.csv`, `composite_agents_summary.csv`, `gss_v8_summary.csv` | les autres conditions |
| idem pour Big Five et jeux economiques | 8 CSV x 1 052 lignes chacun |
| `question_master/gss/main.csv` | libelles et options des 177 questions GSS |
| `question_master/big_five/main.csv`, `econ_games/main.csv` | idem |
| `figure2/run_pipeline.py`, `figure2/R/figure2_reproduce.R` | pipeline complet de la figure 2 |
| `figure3/code/dpd/` | pipeline complet du DPD |
| `camerer_five_studies/` | rapports GPT-4o et tailles d'effet standardisees des 5 replications |

Anonymisation : les emails sont remplaces par `participant_0001` a
`participant_1052`. Les transcripts d'entretien ne sont PAS dans l'archive.

Ce que cela autorise, sans un euro et sans un seul humain recrute :
- Recalculer soi meme le 0,83 et le 0,86, et verifier la formule.
- Recalculer la coherence test retest des humains a partir des donnees brutes.
- Recalculer tous les DPD.
- **Evaluer une architecture nouvelle contre exactement les memes 1 052 personnes
  et les memes items, dans les memes conditions**, du moment que l'architecture
  se contente des reponses de questionnaire en entree (l'entretien reste
  indisponible).
- Mesurer la variance et sa perte, condition par condition. Voir la section
  suivante.

Reserve honnete : je n'ai pas trouve, ni dans l'archive OSF ni ailleurs, les
"reponses agregees en acces ouvert" que le papier promet en section
"Data and materials availability". L'archive contient des reponses
**individuelles** de niveau item, pseudonymisees, ce qui est plus riche que ce
qui etait annonce. [HYPOTHESE] Il est possible que cette publication soit plus
large que ce que les auteurs avaient prevu de rendre public. Cela ne change rien
a sa licite d'usage, le projet OSF etant declare public, mais cela justifie de
citer la source proprement et de ne pas rediffuser les fichiers tels quels.

**4. Le pre enregistrement.** [CONFIRME]
https://osf.io/mexkf/?view_only=375fe67b9a3e48afa7c3684c9d344da4
Utile pour voir les deviations declarees au plan d'analyse.

### Effet du modele, information de cout directe

[CONFIRME] Sur un sous echantillon de 50 agents, exactitude brute GSS, tous les
prompts et temperatures identiques, seul le modele change :

| Modele | Exactitude brute |
|---|---|
| GPT-5 | 0,67 |
| GPT-4.1 | 0,67 |
| o1 | 0,67 |
| o3 | 0,67 |
| GPT-4o (2024, reference du papier) | 0,66 |
| o3-mini | 0,64 |
| o4-mini | 0,64 |
| GPT-4o (instance 2025) | 0,64 |
| o1-mini | 0,62 |
| GPT-4o-mini | 0,60 |

Conclusion des auteurs, citee : l'avantage des modeles avances est faible et
statistiquement indistinguable sur 50 agents. La derive de modele est minime.

[PROBABLE] Pour popsim, cela signifie qu'un bon modele ouvert execute en local
(classe 70B a 120B) devrait se situer dans la fourchette 0,60 a 0,66 en brut,
donc 0,75 a 0,83 en normalise. Le raisonnement : l'ecart entre le meilleur modele
proprietaire de 2026 et GPT-4o de 2024 est de 1 point, et l'ecart entre GPT-4o et
sa version mini est de 6 points. La qualite de la donnee source domine largement
la qualite du modele. C'est ecrit noir sur blanc dans la discussion du papier :
"the quality of individual simulation depends far less on model scale or
synthetic persona engineering than on the depth and reliability of the data an
agent is built from". C'est la meilleure nouvelle possible pour une contrainte de
budget zero. A verifier empiriquement, ce n'est pas mesure par les auteurs.

## a.9 Bonus, la variance ecrasee, mesuree

C'est la contribution scientifique que popsim vise. Elle est mesurable des
maintenant sur les donnees ci dessus. Je l'ai fait.

[CALCUL PROPRE] Methode : pour chacun des 177 items GSS, calcul de l'entropie de
Shannon de la distribution des reponses sur les 1 052 individus, puis moyenne sur
les items. Une entropie plus basse signifie une population plus homogene.
Fichiers utilises : les 8 CSV de
`replication_instructions/figure2/data/new_analysis_summaries/gss_filtered/preparation/`.
Script de 20 lignes en python standard, sans dependance.

| Population | Entropie moyenne par item | Ratio par rapport aux humains |
|---|---|---|
| Humains, vague 1 | 0,8923 | 1,000 |
| Humains, vague 2 | 0,8955 | 1,004 |
| Agents composite (survey + interview) | 0,8129 | **0,911** |
| Agents interview | 0,8029 | **0,900** |
| Agents survey | 0,7681 | 0,861 |
| Agents persona | 0,6047 | **0,678** |
| Agents demographiques | 0,6034 | **0,676** |

Lecture. Les humains sont parfaitement stables entre les deux vagues, ratio 1,004,
ce qui valide la mesure. Les agents demographiques et persona, ceux de la
tradition Argyle, ne conservent que **68 pour cent** de la diversite de reponse
humaine. C'est l'ecrasement de variance decrit dans la litterature, ici chiffre.
Les agents nourris a l'entretien remontent a 90 pour cent, sans jamais atteindre
100.

Trois consequences directes pour le projet :
1. La these de popsim est **empiriquement fondee et deja quantifiee**, sur les
   donnees memes de Stanford, sans depenser un centime. Un residu de 10 points
   d'entropie manquante subsiste meme dans la meilleure condition. C'est
   l'espace de contribution.
2. Une metrique de variance est disponible immediatement, et elle est
   orthogonale a l'exactitude. Aucun des chiffres du papier Stanford ne la
   mesure. C'est exactement le type d'angle mort qui fait un papier.
3. Attention au piege : maximiser l'exactitude individuelle et maximiser la
   variance de population sont deux objectifs partiellement antagonistes. Un
   agent qui repond toujours la modalite majoritaire maximise l'exactitude
   moyenne et annule la variance. Le vrai livrable scientifique est une metrique
   conjointe, pas la variance seule.

[HYPOTHESE, non verifiee] Ce calcul est une premiere passe. Il faudrait le
refaire en ponderant par le nombre d'options par item, en separant ordinal et
nominal, et en le doublant d'une distance de distribution (Earth Mover's Distance
pour l'ordinal, Total Variation Distance pour le nominal) plutot que d'une simple
entropie. C'est precisement ce que fait le papier Synonymix, voir fiche 2.

---

# (b) FICHE 2. Le papier de 2026, "unified group personas"

## b.1 L'URL du porteur du projet est valide

[CONFIRME] https://arxiv.org/html/2603.28066v1 existe et repond.
Reference exacte : Huanxing Chen, Aditesh Kumar, "Synonymix: Unified Group
Personas for Generative Simulations", arXiv:2603.28066, depose le 30 mars 2026.
Categories cs.HC et cs.AI.
Page abstract : https://arxiv.org/abs/2603.28066

[CONFIRME] Champ commentaires de l'arXiv : "CHI'26 Extended Abstract (Poster),
6 pages excluding appendix, 3 figures". Extended Abstracts of the 2026 CHI
Conference, 13 au 17 avril 2026, Barcelone.
DOI : 10.1145/3772363.3799082. ISBN : 979-8-4007-2281-3/2026/04.
Licence : **CC BY 4.0**, donc reutilisable librement avec attribution.

Verdict de correspondance avec la description donnee de memoire : **exacte**.
Recits de vie decomposes en graphe de connaissances a trois types de noeuds,
grammaire d'aretes restreinte a quatre types, fusion avec provenance,
generalisation des etiquettes. Tout y est.

## b.1 bis. Correction a porter au porteur du projet et a Simon

Il faut dire les choses sans detour, mais il faut les dire **justes**. Le message
de l'orchestrateur affirmait que ce n'est pas un papier de Stanford. Verification
faite a la source, c'est inexact sur ce point precis, et propager cette erreur
serait aussi dommageable que l'erreur inverse.

[CONFIRME] Extraction directe du HTML de l'arXiv, bloc `ltx_creator` de
https://arxiv.org/html/2603.28066v1 :

- Huanxing Chen, **huanxing@stanford.edu**, Affiliation : Stanford University,
  Stanford, CA, USA.
- Aditesh Kumar, **aditesh@stanford.edu**, Affiliation : Stanford University,
  Stanford, CA, USA.
- Note imprimee sur le papier : "Both authors contributed equally to this
  research."

Donc, formulation exacte de la correction a transmettre :

> Ce papier **est** signe par deux chercheurs de Stanford, mais ce n'est **pas**
> le papier phare, ce n'est **pas** l'equipe de Joon Sung Park et Michael
> Bernstein, et ce n'est **pas** un article de recherche complet. C'est un
> poster de 6 pages a la session Extended Abstracts de CHI 2026, a deux auteurs
> contributeurs a parts egales, avec N = 30 personas **synthetiques**, aucune
> donnee humaine reelle, et aucun code publie.

La nuance n'est pas de la coquetterie. Dire "ce n'est pas Stanford" a quelqu'un
qui a le papier sous les yeux avec deux adresses @stanford.edu detruit la
credibilite de tout le reste de la note. Dire "c'est Stanford mais c'est un
poster de 6 pages a N = 30 sur des donnees synthetiques" est a la fois vrai et
suffisant pour corriger l'erreur de calibrage.

[PROBABLE] Filiation avec l'equipe Park et al. : Huanxing Chen est nommement
remercie dans les remerciements du papier arXiv 2411.10109 v3, "We thank
Huanxing Chen, Garbo Chung, David Grusky, Luke Hewitt, and Chrystal Redekopp for
their contributions to the project". Chen a donc travaille sur le projet phare
sans en etre coauteur. Synonymix est un travail satellite du meme laboratoire,
pas une suite officielle. Aditesh Kumar n'apparait nulle part dans le papier
phare.

Echelle de comparaison, pour fixer les idees :

| | Park et al. v3 | Synonymix |
|---|---|---|
| Format | article complet, 18 pages plus 50 pages de materiel supplementaire | poster, 6 pages hors annexe |
| Auteurs | 11, dont Percy Liang, Michael Bernstein, Robb Willer, Google DeepMind | 2, contributions egales |
| Sujets | 1 052 humains reels | 30 personas generes par LLM |
| Verite terrain | oui, reponses reelles en 2 vagues | **aucune** |
| Code et donnees | code MIT plus archive de replication OSF | rien |
| Revision par les pairs | soumis, 3 versions | accepte comme poster CHI EA |

## b.2 Le pipeline, en detail

[CONFIRME] Toutes les citations qui suivent viennent de
https://arxiv.org/html/2603.28066v1

**Trois types de noeuds.**
- Sujets (S) : "recurring proper nouns (people, places, institutions)".
- Faits (F) : "concrete events, actions, or milestones".
- Interpretations (I) : "values, motivations, or reflective self-narratives
  derived from factual experiences". Genereees par annotation LLM simulant les
  points de vue d'experts psychologues, sociologues et anthropologues. On
  reconnait la l'expert reflection de Park et al., transposee dans un graphe.

**Quatre types d'aretes autorises, et trois interdits.**

| Arete | Semantique | Etiquettes |
|---|---|---|
| F vers S | spatial, temporel, relationnel | inventaire adapte de PropBank et FrameNet |
| F vers F | relations entre evenements | precedes, enables, causes |
| F vers I | derivation du sens | yields, evokes, supports |
| I vers F | influence | guides, constrains |

Interdits deliberement : S vers F, I vers S, I vers I, pour "maintain balance
between expressive power and structural tractability".

**Deux operations d'agregation.**
1. Genericisation des etiquettes : "Factual nodes are converted to their generic
   variant with non-generic entities extracted and connected via an F->S edge".
   C'est la generalisation des etiquettes decrite par le porteur du projet.
2. Fusion de noeuds : les noeuds a etiquettes identiques ou semantiquement
   equivalentes sont fusionnes entre personas, avec des balises de provenance qui
   tracent la contribution de chaque source.

**Echantillonnage.** "Thematic Random Walk", marche aleatoire qui maintient une
ancre thematique representee par le vecteur d'un noeud I choisi, pour eviter de
generer des personas incoherents.

## b.3 L'evaluation et ses limites

[CONFIRME] Trois banques d'agents, N = 30 chacune.
- D, demographique : concatenation de graines demographiques GSS.
- L, life story : recits narratifs generes selon le cadre d'entretien de vie de
  McAdams.
- F, "Frankenstein" : personas synthetiques issus du pipeline Synonymix.

Evaluation sur 108 items GSS non demographiques. Ordinaux (n = 69) mesures par
Earth Mover's Distance, nominaux (n = 39) par Total Variation Distance.

Deux distances comparees :
- Distance d'enrichissement dist(D, L), le signal comportemental ajoute par
  l'expansion narrative.
- Distance de transformation dist(L, F), le signal comportemental perdu par le
  pipeline Synonymix.
Hypothese : la seconde doit etre inferieure a la premiere.

[CONFIRME] Test statistique employe, cite verbatim : "We test this hypothesis
using a one-sided Wilcoxon signed-rank test, a non-parametric paired test
appropriate for comparing distances within items without distributional
assumptions. We report **rank-biserial correlation (r) as effect size** and
interpret r > 0.5 as large and r > 0.3 as medium."

[CONFIRME] Resultats. Sur les questions ordinales, dist(L,F) = 0,061 contre
dist(D,L) = 0,094, Wilcoxon p < 0,001, r = 0,585, effet dit large. 65 pour cent
des items ordinaux verifient l'inegalite.
Metrique de confidentialite, Maximum Source Contribution : moyenne 0,129,
ecart type 0,031, plage 0,091 a 0,195, 100 pour cent des personas sous 0,50.
Chaque persona synthetique puise en moyenne dans 29,4 des 30 individus sources.

**Anomalie relevee sur les items nominaux.** [CONFIRME, citation exacte] Le
papier ecrit : "For nominal questions, the pattern held directionally
(dist(D,L)=0.074 < dist(L,F)=0.111) with medium effect size (r=0.462), but did
not reach statistical significance (p=0.103)". Or l'inegalite imprimee dit que la
distance de transformation (0,111) est **superieure** a la distance
d'enrichissement (0,074), ce qui **contredit** l'hypothese au lieu de la
soutenir. Et le papier ajoute que seulement 49 pour cent des items nominaux
passent le test, soit moins qu'un tirage a pile ou face.
[PROBABLE] Il s'agit soit d'une inversion typographique dans le papier, soit
d'une formulation qui presente un resultat defavorable comme "directionnellement"
favorable. Dans les deux cas, sur les 39 items nominaux, **le pipeline perd plus
de signal qu'il n'en apporte**. La revendication du papier ne tient que sur les
69 items ordinaux. A ne surtout pas citer sans cette reserve.

**Limites, citees par les auteurs eux memes.**
[CONFIRME] Les 30 personas ne sont PAS des humains reels. Ce sont des recits
generes par LLM a partir de graines demographiques GSS : "Due to ethics-related
concerns about using high-fidelity human data in an unvalidated pipeline, we
experiment only with synthetic agent banks". Et : "Probabilistically-sampled
narratives do not capture the nuances of real human personas, raising concerns
about consistency, granularity, and representation of intersectional identities".
La confidentialite differentielle n'est pas evaluee, reportee a plus tard a cause
de la rarete des noeuds a N = 30.
[CONFIRME] Modele utilise : gpt-oss-120b heberge sur Lightning.AI, "due to
compute constraints". Detail interessant pour popsim : une equipe Stanford a
tourne cette experience sur un modele **ouvert**, faute de budget.
[CONFIRME] Aucun depot de code, aucune donnee publiee.

## b.4 Comparaison des deux pipelines, et la question de la variance

| | Park et al. (2024 a 2026) | Synonymix (2026) |
|---|---|---|
| Objet simule | un individu reel identifie | un groupe, "meso level" |
| Source | 2 h d'entretien reel, transcript integral | recits generes par LLM depuis des graines GSS |
| Representation | texte brut en contexte, plus reflexions expertes en texte | graphe de connaissances typé, S / F / I |
| Fusion entre personnes | aucune, chaque agent est cloisonne | explicite, c'est le coeur de la methode |
| Ce qui est optimise | exactitude individuelle | preservation du signal comportemental sous contrainte de confidentialite |
| N | 1 052 humains reels | 30 personas synthetiques |
| Statut | article de recherche complet, 3 versions | poster de 6 pages |
| Code | oui, MIT, plus donnees OSF | non |

Ce qui change dans la representation de la personne : on passe d'un **texte non
structure** a un **graphe type et contraint**. Le gain theorique n'est pas la
fidelite, c'est la **composabilite**. Un texte ne se fusionne pas, ne
s'anonymise pas proprement, ne se requete pas. Un graphe fait les trois.

Pourquoi cela pourrait mieux preserver la variance inter individuelle, en toute
honnetete :

[HYPOTHESE, non demontree par le papier] L'argument plausible est que la
generalisation des etiquettes est **selective**. Elle detruit l'identifiant
(le nom de l'employeur, la ville) mais preserve la structure relationnelle (le
fait que cette personne relie tel type d'evenement a telle interpretation). Un
prompt demographique, lui, detruit les deux et ne laisse que la moyenne du
groupe, d'ou les 0,676 d'entropie residuelle mesures en a.9. Un graphe permet en
principe d'echantillonner des combinaisons rares, la ou un prompt de persona
converge vers le mode.

[CONFIRME, contre argument] Mais le papier lui meme ne mesure PAS la variance
inter individuelle. Il mesure une distance de distribution agregee entre banques
d'agents. Et son operation centrale, la fusion de noeuds entre personas, est par
construction **destructrice** d'individualite : chaque persona synthetique puise
dans 29,4 des 30 sources. On fabrique des chimeres representatives, pas des
individus distincts. Rien dans ce papier ne demontre une meilleure preservation
de la variance inter individuelle. Affirmer le contraire devant le MIT serait
une surinterpretation.

Position defendable pour popsim : Synonymix est une bonne **brique de
representation** a emprunter (le typage S / F / I, la grammaire d'aretes
restreinte), pas un resultat a revendiquer. La contribution originale resterait
entiere : personne n'a encore mesure ni optimise la variance inter individuelle.

## b.5 Pourquoi le r de 0,59 et le 86 pour cent ne sont pas comparables

C'est le piege de lecture le plus dangereux des deux fiches, parce que les deux
nombres sont des decimales entre 0 et 1 posees a cote du mot GSS. Ils ne mesurent
pas la meme chose, pas sur le meme echantillon, pas contre la meme reference, et
ils n'ont meme pas la meme nature mathematique.

### Ce que mesure reellement le r = 0,585

[CONFIRME] Ce **n'est pas une correlation entre des reponses et une verite
terrain**. C'est une **correlation rang-bisériale**, c'est a dire la taille
d'effet d'un test de Wilcoxon apparie unilateral. Elle repond a une question de
la forme "quand je compare deux series de distances appariees item par item,
quelle proportion des paires va dans le sens attendu, corrigee des rangs".

Decomposition complete :

| Question | Reponse |
|---|---|
| Unite d'observation | **un item du GSS**, pas une personne |
| Effectif du test | n = 69 items ordinaux (et n = 39 nominaux, non significatifs) |
| Ce qui est compare | deux distances entre distributions agregees, dist(L,F) contre dist(D,L) |
| Nature des grandeurs | Earth Mover's Distance et Total Variation Distance entre banques d'agents |
| Verite terrain humaine | **aucune** |
| Ce que r = 0,585 signifie | l'ecart entre les deux distances est systematique en rang, effet dit large selon leur propre seuil |
| Ce que r = 0,585 ne signifie pas | ni une exactitude, ni une fidelite a des humains, ni un pourcentage de comportement reproduit |

Le point decisif est ecrit noir sur blanc par les auteurs eux memes :
[CONFIRME] "We're interested in using population-level distributional distance as
a proxy for a simulation's fidelity **as Synonymix's F agent bank lacks a ground
truth for individual-level metric evaluation**."

Autrement dit : ils n'ont aucun humain a qui se comparer, donc ils comparent des
agents a d'autres agents. Les trois banques D, L et F sont **toutes les trois
synthetiques**. Le papier ne mesure a aucun moment un ecart a un comportement
humain reel.

### La baseline invoquee n'est pas non plus la meme

Le resume dit "preservation du signal comportemental au dela des baselines
demographiques". C'est une formulation qui prete a confusion. La banque D n'est
pas un comparateur de performance qu'on bat, comme le sont les agents
demographiques a 0,74 chez Park et al. Ici, D sert a fabriquer une **unite de
mesure** : on mesure de combien la narration eloigne les reponses du prompt
demographique (distance d'enrichissement), et on verifie que la fusion en graphe
deplace les reponses de **moins** que cela (distance de transformation). C'est un
argument de conservation, pas un argument de superiorite.

Traduction en une phrase : *le pipeline abime moins le signal que la narration
n'en a ajoute*. Ce n'est pas *le pipeline predit mieux les gens*.

### Tableau de non comparabilite

| | Park et al., 0,86 | Synonymix, r = 0,585 |
|---|---|---|
| Nature du nombre | ratio de deux exactitudes | taille d'effet d'un test non parametrique |
| Unite d'observation | un individu (1 052) puis moyenne | un item du GSS (69) |
| Verite terrain | reponses reelles de personnes reelles | aucune |
| Reference au denominateur | la coherence test retest des memes humains a 2 semaines | aucun denominateur, c'est une statistique de rang |
| Ce qu'on peut affirmer | "l'agent retrouve 86 pour cent de ce que la personne reproduit d'elle meme" | "sur 69 items, la fusion deplace les distributions moins que la narration ne les avait deplacees" |
| Direction de la preuve | validite predictive individuelle | conservation de signal agrege sous contrainte de confidentialite |
| Peut on en deduire une fidelite a des humains | oui, c'est la mesure meme | **non, a aucun degre** |

### La regle a retenir pour popsim

Un chiffre de fidelite n'a de sens que si l'on peut nommer les trois elements
suivants : **qui** est predit, **par rapport a quoi** on normalise, et **quelle
erreur humaine** sert de plancher. Park et al. peuvent repondre aux trois.
Synonymix ne peut repondre a aucun des trois, et le dit.

Consequence de methode, et elle vaut pour tout le projet : dans le depot popsim,
aucun score ne devra etre publie sans ces trois elements attaches. C'est
exactement la confusion que le porteur du projet a failli propager en donnant
l'URL de Synonymix comme source du 85 pour cent. La meme rigueur nous protegera
face au MIT.

---

# (c) FICHE 3. Le travail equivalent en psychiatrie dans Nature

## c.1 Verdict

Je n'ai pas trouve de papier publie dans Nature ou dans une revue du groupe
Nature qui soit l'equivalent psychiatrique du papier Stanford, c'est a dire :
des agents generatifs construits a partir d'entretiens individuels avec de vrais
patients, evalues sur leur capacite a predire les reponses individuelles tenues
cachees de ces memes patients, avec un denominateur test retest.

Je l'ecris noir sur blanc plutot que de combler. Cinq requetes distinctes sur
Nature, Nature Medicine, Nature Human Behaviour, npj Digital Medicine, Nature
Mental Health et npj Mental Health Research n'ont pas ramene ce papier.

En revanche, j'ai trouve un papier **dans Nature**, publie en aout 2026, coecrit
par un coauteur du papier Stanford, qui porte un chiffre de 0,85. Ce n'est pas de
la psychiatrie, mais c'est probablement la source du souvenir. Voir candidat 0.

[HYPOTHESE] Trois explications possibles, non departagees, la premiere etant
desormais la plus probable :
1. Simon pense au candidat 0 (Nature, aout 2026, Willer coauteur, r = 0,85) et
   le mot "psychiatrie" est un glissement de memoire.
2. Il parle d'un travail en cours, non publie, connu par son reseau MIT.
3. Le papier existe et ma recherche l'a manque, notamment s'il est recent ou
   indexe sous un vocabulaire inattendu.

## c.2 Les candidats, classes par proximite

### Candidat 0, le plus probable, trouve en dernier

**Ashokkumar, Hewitt, Ghezae, Willer, "Large language models can predict the
results of social science experiments", Nature 656, 115 a 122, aout 2026.**
https://www.nature.com/articles/s41586-026-10742-x
DOI : 10.1038/s41586-026-10742-x. PubMed : https://pubmed.ncbi.nlm.nih.gov/42420458/
Page projet Stanford : https://ai4pb.stanford.edu/projects/predicting-results-of-social-science-experiments-using-large-language-models

[CONFIRME] C'est un article dans **Nature**, la revue mere, pas dans une revue
satellite. Archive de 70 experiences d'enquete pre enregistrees et
representatives au niveau national aux Etats Unis, 469 effets de traitement,
119 330 participants. GPT-4 simule les reponses de echantillons representatifs,
les effets de traitement sont deduits par comparaison entre conditions.

Pourquoi c'est le candidat numero un malgre l'absence de psychiatrie :
- [CONFIRME] **Robb Willer en est coauteur, et il est aussi coauteur du papier
  Stanford.** C'est la meme ecurie, le meme laboratoire, le meme sujet.
- [CONFIRME] C'est la **reference numero 1** de la bibliographie du papier
  Stanford v3.
- [CONFIRME] La correlation annoncee sur la page du projet est **r = 0,85**, et
  r = 0,90 sur les etudes non publiees.

**C'est tres probablement la source de la confusion.** Quelqu'un qui a entendu
parler d'un "papier Nature" adjacent aux travaux de Stanford, avec un chiffre de
0,85, pense a celui la. Il n'y a pas de psychiatrie dedans, mais il y a Nature,
il y a 0,85 et il y a Willer.
**Niveau de confiance que ce soit ce que Simon avait en tete : moyen a eleve**,
sous reserve que le mot "psychiatrie" soit une deformation de memoire.

Reserve importante : [CONFIRME] le papier lui meme est derriere une
authentification, je n'ai pas pu lire la declaration de disponibilite des
donnees. Je ne sais donc pas si l'archive des 70 experiences est telechargeable.
La page projet mentionne des documents supplementaires via DocSend et une demo a
treatmenteffect.app, sans depot public identifie. A verifier, l'enjeu est reel :
70 experiences pre enregistrees avec leurs effets mesures constitueraient un banc
d'essai gratuit de premier ordre.

Note de vocabulaire, qui compte : ce papier predit des **effets de traitement
agreges**, pas des individus. C'est la tradition Argyle poussee a son maximum,
pas la tradition Park. Il ne repond donc pas a la question de la variance inter
individuelle, il l'evite par construction.

### Candidat 1, le plus proche sur la forme et le prestige

**Binz et al., "A foundation model to predict and capture human cognition",
Nature, volume 644, numero 8078, pages 1002 a 1009, 28 aout 2025.**
https://www.nature.com/articles/s41586-025-09215-4
Preprint : https://arxiv.org/abs/2410.20268
Modele et code : https://github.com/marcelbinz/Llama-3.1-Centaur-70B

Correspondance : forte sur le fond scientifique, faible sur la psychiatrie.
Modele Centaur, obtenu par fine tuning d'un Llama 3.1 70B sur le jeu de donnees
Psych-101 : plus de 60 000 participants, plus de 10 millions de choix, 160
experiences. Il predit le comportement de participants tenus hors echantillon
mieux que les modeles cognitifs existants, et generalise a des taches nouvelles.
[CONFIRME] pour l'existence, le volume et la revue.
C'est bien "le papier Nature qui predit le comportement individuel". Mais c'est
de la cognition experimentale, pas de la psychiatrie clinique, et la methode est
du fine tuning sur des donnees de tache, pas du conditionnement sur des recits de
vie. **Niveau de confiance que ce soit ce que Simon avait en tete : moyen.**

Note importante : c'est le seul candidat qui publie un modele ouvert, entrainable
et reutilisable gratuitement. Independamment de la question de Simon, il merite
une fiche a lui seul dans une prochaine exploration.

### Candidat 2, le plus proche sur "vies individuelles"

**Savcisens et al., "Using sequences of life-events to predict human lives",
Nature Computational Science 4, 43 a 56, janvier 2024.**
https://www.nature.com/articles/s43588-023-00573-5
Site du projet : https://life2vec.dk/

Correspondance : forte sur l'idee de jumeau numerique longitudinal, nulle sur les
LLM conversationnels. Modele life2vec, transformer entraine sur le registre
national danois, 6 millions de personnes, evenements de sante, education, emploi,
revenu, adresse, au jour le jour. Predit la mortalite precoce et des traits de
personnalite, dont l'extraversion.
[CONFIRME] La revue est bien du groupe Nature. [CONFIRME] Le modele **n'est pas
public** et les donnees de registre danois sont inaccessibles hors procedure
nationale. Inutilisable a budget zero.
**Niveau de confiance : faible a moyen.** La sante mentale n'est qu'une
dimension parmi d'autres.

### Candidat 3, le plus proche sur le mot "psychiatrie"

**WiseMind, "a knowledge-guided multi-agent framework for accurate and empathetic
psychiatric diagnosis", npj Digital Medicine, mars 2026.**
https://www.nature.com/articles/s41746-026-02559-9
[CONFIRME] Existence et revue. 1 206 conversations simulees, 180 sessions
utilisateurs reelles, 85,6 pour cent d'exactitude diagnostique top 1.
Attention au faux ami : le 85,6 pour cent est une exactitude **diagnostique**,
pas un score normalise par une coherence test retest. Le rapprochement avec le
85 pour cent de Stanford serait une coincidence numerique, pas une equivalence.
Et l'objet simule est le clinicien, pas le patient.
**Niveau de confiance : faible.**

### Candidat 4, les jumeaux numeriques cliniques

**"Large language models forecast patient health trajectories enabling digital
twins", npj Digital Medicine, 2025.**
https://www.nature.com/articles/s41746-025-02004-3
Modele DT-GPT, prevision de trajectoires cliniques depuis les dossiers
electroniques. Cancer du poumon non a petites cellules, soins intensifs, maladie
d'Alzheimer. [CONFIRME] Existence et revue. Ni psychiatrie, ni entretien, ni LLM
conditionne sur du recit.
**Niveau de confiance : tres faible.**

### Candidat 5, le plus proche par la methode, mais hors Nature

**Toubia, Gui, Peng, Merlau, Li, Chen, "Twin-2K-500: A Data Set for Building
Digital Twins of over 2,000 People Based on Their Answers to over 500 Questions",
Marketing Science 44, 1446 a 1455, 2025.**
https://arxiv.org/html/2505.17479
https://pubsonline.informs.org/doi/10.1287/mksc.2025.0262
Ce n'est pas Nature, mais c'est methodologiquement le jumeau le plus exact du
papier Stanford, et surtout il est **entierement public**. Voir la fiche 4, c'est
un actif majeur pour popsim.

### Piege a signaler, un candidat a NE PAS citer

**"Plausible Patients, Impossible Populations: Auditing Epidemiological Fidelity
in Large Language Model Mental Health Simulations"** (anciennement PsychBench),
Patrick Keough, arXiv:2604.17359, v1 du 19 avril 2026, v2 du 5 aout 2026.
https://arxiv.org/abs/2604.17359

Ce papier ressemble beaucoup a ce que popsim cherche : audit de la simulation de
patients psychiatriques par LLM, 28 800 profils, quatre modeles, 120 cohortes,
compare a des ancres PHQ-8 ponderees derivees des microdonnees NHANES.
Il circule avec un chiffre tres attractif pour nous : une compression de variance
de 14 a 62 pour cent selon le modele.

**Ne pas utiliser ce chiffre.** [CONFIRME] Le champ commentaires de la v2 dit
exactement : "v2: substantially revised and retitled; **withdraws the
variance-compression and transgender-suppression results** and adds a
pre-registered decoding control."

L'auteur a retire lui meme le resultat de compression de variance. C'est
precisement le chiffre qui aurait servi notre these, et il est retracte. Un
auteur unique, pas de revue par les pairs, un resultat central retire en quatre
mois. Le citer serait une faute grave devant le MIT.

[CONFIRME] Ce qui subsiste en v2, et qui reste interessant a titre qualitatif :
la dissociation coherence contre fidelite. 97,3 pour cent des cas simules
remplissent les criteres DSM-5 et paraissent cliniquement plausibles un par un,
mais les populations agregees divergent des donnees epidemiologiques reelles.
Scores PHQ-8 gonfles de 2,8 a 5,5 points, disparites raciales erodees,
covariance des symptomes instable, et un tiers des patients changent de
categorie de severite entre deux generations avec un prompt identique.

Lecon de methode a retenir : la plausibilite individuelle et la fidelite
populationnelle sont deux choses distinctes, et un modele peut exceller a la
premiere en echouant a la seconde. C'est la formulation la plus claire que j'aie
trouvee du probleme que popsim veut attaquer, meme si sa quantification a ete
retiree.

## c.3 Le piege des trois "85"

Il y a au moins **trois chiffres distincts autour de 85** dans ce paysage, tous
associes a Stanford ou a Nature, tous portant sur des LLM qui simulent des
humains. Les confondre est facile et couteux.

| Chiffre | Source | Ce que c'est vraiment |
|---|---|---|
| 85 pour cent | Park et al., arXiv 2411.10109 **v1 de 2024** | exactitude normalisee individuelle sur le GSS. **Perime**, la v3 dit 83, 82 et 86 selon la condition |
| r = 0,85 | Ashokkumar et al., **Nature** 656, 2026 | correlation entre effets de traitement **agreges** predits et mesures, sur 70 experiences. Aucun individu |
| 85,6 pour cent | WiseMind, npj Digital Medicine, 2026 | exactitude **diagnostique** top 1 d'un systeme multi agents. Simule le clinicien, pas le patient |

Ajoutons le quatrieme, qui n'est pas un 85 mais qui sera cite dans les memes
conversations : 88 pour cent pour Twin-2K-500, exactitude moyenne relative a un
banc test retest, sur donnees publiques.

Pour popsim, ce tableau vaut mieux qu'un long discours : il montre au MIT qu'on
sait de quoi on parle, et il protege le projet contre sa propre communication.

## c.4 Recommandation

Demander la reference a Simon plutot que de deviner, en lui soumettant
directement le candidat 0. Une question precise vaut mieux qu'une bibliographie
approximative. Formulation suggeree en fin de document.

---

# (d) DELTA OPERATIONNEL

Contraintes rappelees : budget zero, aucun humain recrute, phase exploratoire,
objectif un depot serieux et quantitatif presentable au MIT.

## d.1 Papier Stanford, ligne par ligne

| Ce qu'ils ont fait | Reproductible a budget zero et sans humains | Necessite des humains | Necessite du budget |
|---|---|---|---|
| Recruter 1 052 Americains stratifies via Bovitz | Non. Rien a faire. | Oui, entierement | Oui. 60 + 30 dollars par personne plus bonus, soit environ 95 000 a 100 000 dollars de remuneration seule pour 1 052 personnes |
| Mener 2 104 heures d'entretien par IA | Le code est public (MIT). Utilisable sur soi meme, sur des donnees deja collectees, sur des transcripts publics. | Oui pour de nouveaux sujets | Cout API. Environ 6 500 mots produits par entretien, plus les relances. Nul si modele local |
| Transcrire et pseudonymiser | Oui. Whisper tourne en local, gratuit | Non | Non |
| Construire les agents (expert reflection plus chaine de pensee) | **Oui, integralement.** Prompts cites verbatim dans le papier, code MIT disponible | Non | Nul si modele ouvert local. Sinon quelques centimes par agent |
| Administrer GSS, BFI-44, jeux et experiences a des humains | Non | Oui | Oui, plateforme Qualtrics et incitations monetaires reelles |
| **Disposer des reponses humaines vague 1 et vague 2 des 1 052 participants** | **Oui. Deja telecharge. Gratuit.** OSF t6g7k | Non | Non |
| Calculer la coherence test retest a deux semaines | **Oui, sur les donnees OSF** | Non | Non |
| Calculer les exactitudes normalisees des 5 conditions | **Oui, code python et R fournis dans l'archive** | Non | Non |
| Calculer les DPD | **Oui, `figure3/code/dpd/` fourni** | Non | Non |
| Repliquer les 5 experiences de Camerer sur des agents | **Oui, protocoles publies, sorties GPT-4o fournies dans l'archive** | Non pour la partie agent | API seulement |
| Comparer les modeles (GPT-5, o3, mini, etc.) | Partiellement. Modeles ouverts oui, modeles proprietaires non | Non | Oui pour les modeles proprietaires |
| Acceder aux 1 052 transcripts d'entretien | **Non. Bloque.** Pas de procedure publiee | Non | Le budget n'y change rien. Seul un accord avec Joon Sung Park le debloque |
| Interroger la banque des 1 000 agents sur de nouvelles taches | Non | Non | Le budget n'y change rien. Meme blocage |

### La reponse a la question posee dans la mission

*Peut on reproduire leur evaluation en utilisant leur agent bank ou des jeux de
donnees publics au lieu de mener nos propres entretiens ?*

**Oui, a 80 pour cent, et pas via l'agent bank.** L'agent bank reste ferme.
Mais l'archive OSF donne quelque chose de plus utile pour une evaluation : les
reponses de verite terrain individuelles, les reponses de toutes les conditions
d'agents, les items, et le code d'analyse. On peut donc :

- refaire toute la partie analytique du papier, a l'identique, ce soir ;
- mesurer une nouvelle metrique (la variance, deja fait en a.9) que les auteurs
  n'ont pas mesuree ;
- **evaluer une architecture popsim contre le meme banc d'essai**, a condition de
  se limiter aux conditions "survey" et "demographique" en entree, puisque les
  transcripts manquent.

Les 20 pour cent inaccessibles : toute revendication de la forme "notre
architecture fait mieux que leurs agents interview" est hors de portee sans les
transcripts. C'est la limite dure, et il faut la nommer avant que quelqu'un
d'autre ne la nomme.

## d.2 Papier Synonymix

| Ce qu'ils ont fait | Reproductible a budget zero et sans humains | Necessite des humains | Necessite du budget |
|---|---|---|---|
| Generer 30 recits de vie par LLM depuis des graines GSS | **Oui, entierement.** C'est deja synthetique par construction | Non | Nul en local |
| Extraire le graphe S / F / I | Oui, mais le code n'est pas publie, donc a reimplementer. L'ontologie et la grammaire d'aretes sont decrites de facon suffisamment precise dans le papier | Non | Nul en local |
| Genericisation, fusion, provenance | Oui, a reimplementer | Non | Nul |
| Thematic Random Walk | Oui, a reimplementer. Necessite des embeddings, disponibles gratuitement en local | Non | Nul |
| Evaluation EMD / TVD sur 108 items GSS | **Oui**, et on peut faire mieux qu'eux : ils avaient 30 personas synthetiques, l'archive OSF en offre 1 052 reels | Non | Nul |
| Inference sur gpt-oss-120b | Oui si machine suffisante, ou offres gratuites d'inference. Sinon substituer un modele plus petit | Non | Zero a modere selon la machine |
| Evaluation de la confidentialite differentielle | Non fait par eux non plus. Terrain vierge | Non | Nul |

Verdict : **ce papier est integralement reproductible et depassable a budget
zero.** N = 30 et des personas synthetiques, c'est un plancher tres bas. Refaire
leur experience sur les 1 052 individus reels de l'archive OSF constituerait deja
un resultat publiable, et repondrait a leur propre limite declaree.

## d.3 Les autres actifs gratuits identifies en chemin

| Actif | URL | Ce que ca donne | Cout |
|---|---|---|---|
| **Twin-2K-500** | https://huggingface.co/datasets/LLM-Digital-Twin/Twin-2K-500 | 2 058 Americains, plus de 500 questions, 4 vagues, 2,42 h par personne en moyenne, mesures demographiques, psychologiques, economiques, de personnalite et cognitives, replications d'economie comportementale. **Public sur Hugging Face** | Zero |
| Code de simulation Twin-2K-500 | https://github.com/tianyipeng-lab/Digital-Twin-Simulation | Le pipeline de simulation associe | Zero |
| Jeu de donnees Mega-Study | https://huggingface.co/datasets/LLM-Digital-Twin/Twin-2K-500-Mega-Study | Extension | Zero |
| genagents | https://github.com/StanfordHCI/genagents | Code MIT plus 3 000 agents demographiques GSS | Zero, hors API |
| Entretieneur IA | https://github.com/joonspk-research/generative_agent | Code de l'entretieneur autonome | Zero, hors API |
| Archive de replication Stanford | https://osf.io/t6g7k/files/osfstorage | Reponses individuelles des 1 052, toutes conditions, plus code d'analyse | Zero |
| Centaur 70B | https://github.com/marcelbinz/Llama-3.1-Centaur-70B | Modele ouvert de cognition humaine | Zero, hors calcul |
| GSS complet | https://gss.norc.org | Donnees de reference et codebook | Zero |
| Synonymix, texte integral | https://arxiv.org/html/2603.28066v1 | Licence **CC BY 4.0**, ontologie et grammaire d'aretes reutilisables avec attribution | Zero |
| Archive des 70 experiences (Nature 2026) | https://www.nature.com/articles/s41586-026-10742-x | 469 effets de traitement, 119 330 participants. **Disponibilite non verifiee**, article sous authentification | Inconnu |

[CONFIRME] Twin-2K-500 annonce 88 pour cent d'exactitude moyenne relative a un
banc de reference test retest sur des taches tenues cachees. C'est le meme type
de metrique normalisee que Stanford, sur un jeu de donnees **entierement public**.

Ce point merite d'etre souligne au porteur du projet : **Twin-2K-500 permet de
reproduire l'esprit du resultat Stanford de bout en bout, entrees comprises,
sans transcript manquant, sans acces restreint et sans budget.** Ce que
l'archive OSF ne permet pas (evaluer une architecture qui consomme des donnees
riches en entree), Twin-2K-500 le permet. Les deux sont complementaires.

## d.4 Chemin critique recommande, sans budget et sans humains

Ordre propose, du plus rentable au moins rentable :

1. **Recalculer la figure 2 et la figure 3 de Stanford** sur l'archive OSF.
   Cout zero, delai un a deux jours. Produit : la preuve qu'on maitrise leur
   metrique. Presentable tel quel.
2. **Consolider la mesure de variance** de la section a.9 avec EMD et TVD,
   separement pour ordinal et nominal, ponderee par le nombre d'options.
   Cout zero. Produit : le premier resultat original du projet.
3. **Basculer sur Twin-2K-500** pour construire des agents de bout en bout avec
   un modele ouvert local, et mesurer exactitude ET variance conjointement.
   Cout zero hors electricite. Produit : une replication complete et une metrique
   nouvelle.
4. **Reimplementer Synonymix** sur les vraies personnes plutot que sur
   30 personas synthetiques. Cout zero. Produit : un depassement direct d'un
   papier CHI 2026.
5. **Ecrire a Joon Sung Park** (joonspk@stanford.edu) pour l'acces restreint, en
   joignant les points 1 et 2 comme preuve de serieux. C'est la seule voie vers
   les transcripts, et elle est infiniment plus credible avec des resultats
   deja produits qu'avec une intention.

Cet ordre a une propriete utile : chaque etape produit un livrable autonome, et
aucune ne depend de l'acces restreint.

---

## Ce que je n'ai pas pu verifier

1. **La procedure exacte d'acces a l'agent bank.** Il n'en existe aucune de
   publiee. Ni URL, ni formulaire, ni delai, ni criteres. Le README de genagents
   dit seulement de contacter les auteurs. Je n'ai trouve aucun temoignage
   public d'un chercheur tiers ayant obtenu cet acces, ni dans un sens ni dans
   l'autre. Toute estimation de delai serait inventee.
2. **Les "reponses agregees en acces ouvert"** promises dans la section
   disponibilite du papier. Je ne les ai pas trouvees. L'archive OSF contient
   des reponses individuelles pseudonymisees, ce qui est different et plus riche.
   Je ne sais pas si c'est une publication deliberee ou un depassement de ce qui
   etait prevu.
3. **Le contenu du depot github.com/joonspk-research/generative_agent.** Je l'ai
   cite parce que le papier le cite, mais je n'ai pas inspecte son arborescence
   ni verifie sa licence.
4. ~~Les affiliations du papier Synonymix.~~ **Point resolu.** Verifie a la
   source dans le HTML arXiv : Huanxing Chen (huanxing@stanford.edu) et Aditesh
   Kumar (aditesh@stanford.edu), tous deux Stanford University, contributions
   egales. Voir b.1 bis. En revanche je n'ai pas pu etablir le statut de chacun
   (doctorant, master, chercheur), ni si le travail a ete supervise par le
   laboratoire de Bernstein.
5. **La figure 2 du papier Stanford telle qu'imprimee.** J'ai travaille sur le
   texte extrait du PDF. Les valeurs numeriques citees viennent du corps du texte,
   pas de la lecture des points de la figure. Les valeurs des tableaux de
   robustesse en annexe ont ete extraites d'un PDF a mise en page complexe, elles
   sont a re verifier avant toute citation dans un livrable externe.
6. **Le papier de psychiatrie mentionne par Simon.** Non identifie. Voir fiche 3.
7. **La performance reelle d'un modele ouvert local** sur cette tache. Ma
   fourchette de 0,75 a 0,83 en normalise est un raisonnement par extrapolation,
   pas une mesure. Aucun des papiers lus ne teste un modele ouvert sur le banc
   d'essai de Stanford, a l'exception de Synonymix qui utilise gpt-oss-120b mais
   sur son propre protocole.
8. **Les conditions juridiques d'usage de l'archive OSF.** Le projet est declare
   public, mais je n'ai pas trouve de licence explicite attachee aux fichiers de
   donnees. A verifier avant toute rediffusion ou publication derivee.

---

## Questions ouvertes pour Simon

1. **La reference du papier de psychiatrie.** Aucun candidat ne correspond
   exactement, mais un se detache : Ashokkumar, Hewitt, Ghezae et **Willer**,
   "Large language models can predict the results of social science experiments",
   **Nature** 656, 115 a 122, aout 2026. Willer est coauteur des deux papiers, la
   correlation annoncee est r = 0,85, et c'est la reference numero 1 de la
   bibliographie de Park et al. Question a poser telle quelle : *est ce ce
   papier la, avec "psychiatrie" en glissement de memoire, ou bien un travail
   distinct non publie connu par le reseau MIT ?* Les autres pistes sont Centaur
   (Nature, aout 2025) et life2vec (Nature Computational Science, 2024). Une
   ligne de reponse fait gagner une journee.

2. **Le contact MIT peut il ouvrir la porte de l'agent bank ?** Il n'existe
   aucune procedure publique. Le seul canal est un mail a joonspk@stanford.edu.
   La question n'est pas "peut on demander", c'est "qui, dans le reseau, peut
   faire une introduction". Sans transcript, une revendication du type "on fait
   mieux que leurs agents interview" est structurellement hors de portee.

3. **Que vise t on exactement en priorite : l'exactitude ou la variance ?** Les
   deux objectifs sont partiellement antagonistes. Un agent qui repond toujours
   la modalite majoritaire maximise l'exactitude individuelle moyenne et annule
   la variance de population. Si la contribution scientifique est bien la
   variance, il faut arbitrer la metrique conjointe maintenant, pas apres avoir
   ecrit du code.

4. **Le porteur du projet a t il confondu Synonymix avec le papier phare ?**
   L'URL qu'il a donnee pointe vers un poster CHI de 6 pages, deux auteurs de
   Stanford, N = 30 personas synthetiques, aucune verite terrain humaine, aucun
   code. Ce n'est pas un mauvais papier, mais ce n'est pas la reference, et son
   r de 0,59 n'est pas une exactitude comparable au 86 pour cent : c'est la
   taille d'effet d'un test de Wilcoxon sur 69 items, sans aucun humain dans la
   boucle (voir b.5). Il vaut mieux clarifier tot, et clarifier avec la bonne
   formulation : c'est bien Stanford, ce n'est pas la bonne equipe ni le bon
   format.

5. **Les jeux economiques sont le point faible publie de la litterature**
   (aucune difference significative entre toutes les conditions, p = 0,16). Or
   c'est exactement le registre du comportement d'achat, qui figure dans les cas
   d'usage monetisables du projet. Est ce un angle mort a exploiter comme
   contribution, ou une zone a eviter dans le pitch ?

6. **Twin-2K-500 change t il l'ordre de marche ?** 2 058 personnes, 500 questions,
   4 vagues, entierement public sur Hugging Face, avec code de simulation. C'est
   le seul chemin qui permet de construire des agents de bout en bout et de
   mesurer exactitude et variance sur les memes personnes, a budget zero. Faut il
   en faire le socle du premier resultat plutot que l'archive Stanford ?

7. **Statut de la mesure de variance produite en a.9.** Les agents demographiques
   ne conservent que 67,6 pour cent de l'entropie de reponse humaine, contre
   91,1 pour cent pour les meilleurs agents. Ce chiffre est calcule sur les
   donnees publiques de Stanford, il ne coute rien, et il n'apparait dans aucun
   des papiers lus. Est ce deja assez pour amorcer la conversation avec le MIT,
   ou faut il attendre une metrique consolidee ?
