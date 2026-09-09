# a16. Ce que le depot public de code de Stanford dit reellement

## Errata du 8 septembre 2026

Corrections apportees a la suite de la relecture adverse `a17-relecture-adverse.md`. Le corps
du rapport n'est pas reecrit, il reste lisible tel qu'il a ete rendu le 7 septembre. Chaque
point cite la phrase d'origine, donne la correction et la preuve. Recalcul :
`analyses/a19_denominateurs.py`, tableau `resultats/a19-recopie-items-ecartes.csv`. Aucun appel
de modele.

**Aucune lecture du depot n'est remise en cause.** Les trois artefacts de code identifies dans
la section 3.3 existent, leurs champs sont bien ceux qui sont cites, et la verification par
script des 3 505 `scratch.json` est valable. Ce qui est corrige est l'**inference** tiree de ces
artefacts sur un fichier de sortie precis du paquet OSF.

### E1. Section 3.3 et "Ce que cette lecture change au dossier" : la correction apportee a `a2-baselines.md` est retiree. Objection a17 8.1 et 2.3, contradiction C1. Gravite : bloquante.

**Phrase d'origine, section 3.3.** "**La deduction de a2 section 2.1, l'agent demographique n'a
probablement pas recu l'orientation politique, est desormais contredite par trois artefacts de
code independants** : la classe `Scratch` de Stanford, la banque publique de 3 505 agents, et le
fichier demographique du paquet de replication, en plus de l'exemple litteral du materiel
supplementaire deja releve par a14 section 3.1."

**Phrase d'origine, "Ce que cette lecture change au dossier", a2 section 2.1.** "Le paragraphe
L'agent demographique n'a probablement pas recu l'orientation politique doit etre reecrit. Il
etait donne comme une deduction explicite, et **la deduction est fausse**. [...] L'honnetete du
dossier exige de dire que cette deduction, faite de bonne foi sur un fait mesure, a ete
infirmee par le code."

**Phrase d'origine, suite.** "La phrase suivante doit etre corrigee dans la foulee. Consequence,
la comparaison B1 contre agent demographique n'est pas un duel a armes egales : c'est l'inverse.
La comparaison a armes egales est **B1 complet a 0,6209 contre 0,5818**."

**Ces trois passages sont annules.** La deduction de a2 n'est pas fausse : elle est confirmee
par la mesure, pour le fichier que a2 evalue.

**Ce que les trois artefacts etablissent, et ce qu'ils n'etablissent pas.** Ils etablissent que
la representation demographique de Stanford **peut** porter l'ideologie et le parti : c'est
vrai de la classe `Scratch`, vrai des 3 505 `scratch.json` de la banque publique, vrai des
colonnes de `demographic_summary.csv`. Ils n'etablissent pas que le fichier
`gss_v6_summary.csv`, celui que la figure 2 du papier emploie comme condition demographique et
celui que a2 evalue, les portait. **Un fichier de sortie ne se deduit pas d'une structure de
donnees : il se mesure.**

**Preuve, taux d'accord avec la vague 1 sur les 1 052 memes participants.** [MESURE,
`resultats/a19-recopie-items-ecartes.csv`]

| item | modalite majoritaire | `gss_v6`, evalue par a2 | `gss_v8` |
|---|---|---|---|
| `polviews` | 0,288 | **0,200** | **0,961** |
| `partyid` | 0,220 | **0,165** | **0,994** |
| `marital` | 0,420 | **0,999** | 0,461 |
| `relig*` | 0,405 | **0,994** | 0,430 |
| `degree*` | 0,389 | **0,998** | 0,267 |
| `income` | 0,516 | **0,994** | 0,454 |
| `zodiac` | 0,092 | **0,999** | 0,062 |
| `hispanic` | 0,865 | **0,999** | 0,863 |
| `sex*` | 0,564 | **0,999** | **0,998** |
| `race*` | 0,759 | **0,998** | **0,999** |

`gss_v6` est **sous la modalite majoritaire** sur `polviews` et sur `partyid`, et il recopie a
plus de 99 pour cent l'etat civil, la religion, le diplome, le revenu, la date de naissance par
le zodiaque et l'origine hispanique. `gss_v8` recopie l'ideologie, le parti, la race et le
genre, et rien d'autre. Ce sont deux invites differentes, et c'est `gss_v8` qui correspond a la
representation decrite par le depot et par le papier.

**Ligne de remplacement pour "Ce que cette lecture change au dossier", a2 section 2.1.**
"Le paragraphe de a2 doit etre reecrit, mais dans l'autre sens : la deduction est **confirmee**
et devient un fait mesure. Le depot de code etablit que la representation demographique de
Stanford peut contenir l'ideologie et le parti ; la mesure item par item etablit que la
generation `gss_v6`, celle que a2 evalue, ne les contenait pas, et que la generation `gss_v8`
les contenait. Les deux constats sont compatibles : ils portent sur deux generations
differentes. La comparaison a armes egales face a `v6` reste B1 sans les attributs politiques,
0,5998 contre 0,5818."

**Le point favorable du rapport reste entier.** La section 3.3 avait raison de chercher la
reponse dans le code plutot que dans le papier, et le second paragraphe de sa conclusion sur
a2, "le fait mesure, lui, ne bouge pas et reste precieux. L'agent demographique obtient 0,1996
sur `polviews`, sous la modalite majoritaire a 0,2880. Ce fait demande une explication, et il en
reste deux : la regle de retrait, ou un traitement particulier de cet item", est la bonne
posture. La mesure tranche aujourd'hui entre les deux : **ni l'une ni l'autre**, c'est une
generation differente.

### E2. Section 2.3 : la question du sigle `LA` est close, et la question qu'elle portait est resolue. Complement.

**Phrase d'origine.** "Le sigle LA reste inexplique, et la recherche est maintenant complete."

**Complement.** Le sigle reste inexplique et la recherche reste close, trois sources epuisees.
Mais la question de fond, ce qui differencie `v6` de `v8`, ne depend plus de lui : elle est
tranchee par le tableau ci dessus. `v8` est l'ablation demographique du papier, `v6` est une
ablation a profil d'etat civil sans politique. Ce constat rend inutile toute recherche
ulterieure sur `LA` pour l'usage que le dossier en faisait.

### E3. "Ce que cette lecture change au dossier", a1 section 7.4 : le "non etabli" tombe.

**Phrase d'origine.** "La phrase Le seul element est la mention `ablation (demog) -- LA` pour
`v8`, dont la signification de `LA` n'est explicitee nulle part dans le paquet doit devenir :
dont la signification n'est explicitee **ni dans le paquet, ni dans le papier, ni dans le depot
de code de Stanford ni dans ses deux depots freres**."

**Complement.** Cette reecriture reste juste et doit etre faite. Il faut y ajouter le fait
nouveau : ce que la mention `LA` cachait est desormais mesure, item par item, et a1 section 7.4
porte cet errata depuis le 8 septembre. Voir l'errata E4 de `a1-double-distorsion.md`.

### E4. Section 5 : le test propose est deja tranche.

**Phrase d'origine, "Ce que cette lecture change au dossier", a1 section 7.5.** "S'y ajoute
maintenant un second test, moins cher, decrit en section 5 ci dessus : mesurer si le deficit de
l'agent demographique est concentre sur `polviews` ou diffus sur les items politiques, ce qui
tranche l'hypothese de la regle de retrait."

**Le test est fait, et il tranche contre la regle de retrait.** Le deficit de `gss_v6` n'est pas
concentre sur `polviews` : il porte aussi sur `partyid`, 0,165 contre 0,220 de modalite
majoritaire, alors que la regle de retrait ne retire jamais `partyid` quand on predit
`polviews`. Et, symetriquement, `gss_v8` obtient 0,961 sur `polviews`, ce qu'aucune regle de
retrait n'autorise si elle s'appliquait au descripteur. Le test est clos. [MESURE]

### E5. Ce que ces errata ne changent pas

L'identite du depot, la licence, les dates, le second depot non cite, l'absence du code de
generation, le contenu des invites, la phrase supprimee du papier, la temperature a 0,7,
l'expression reguliere d'extraction, le champ `private_self_description` et les deux
contradictions entre le papier et ses artefacts ne sont pas touches. Ce sont les lectures les
plus utiles du rapport et elles restent valables telles quelles.

---

Rapport du 7 septembre 2026. Repond au point 5 de la section "Ce que je n'ai pas pu verifier"
de a14 et a la question 4 de ses "Questions ouvertes pour Simon" : le depot GitHub cite par le
papier arXiv 2411.10109 v3 n'avait jamais ete consulte.

Methode : clone en lecture seule dans un dossier temporaire hors du projet, lecture integrale
des 28 fichiers hors banque d'agents, inventaire de la banque d'agents par script, lecture des
16 fils d'issues et de pull requests via l'API GitHub, et comparaison mot a mot avec le PDF du
papier retelecharge pour l'occasion. Aucun fichier du projet n'a ete modifie. Aucun appel de
modele n'a ete fait.

---

## Reponse en une ligne

Le depot existe, il est vivant et exploitable, mais **il ne contient ni le code de generation
des agents du papier, ni l'enqueteur, ni les etiquettes v3 v6 v7 v8, ni la moindre trace du
sigle LA** ; en revanche il livre trois choses que le papier ne donne pas, la temperature
reelle (0,7), l'extraction de la modalite (une expression reguliere, sans aucun appariement a
la nomenclature) et **une banque de 3 505 agents demographiques telechargeable sous licence
MIT**, et il met en evidence **deux affirmations du papier que ses propres artefacts
contredisent**.

---

## 1. Identite du depot, licence, dates

Le papier ecrit, page PDF 12 :

> "The code for generating all the different agents is available in an open-source repository
> here: https://osf.io/t6g7k/files/osfstorage The code to create the interview agents, including
> the AI interviewer, can be found here: https://github.com/joonspk-research/generative_agent .
> Researchers interested in constructing agents from their own data can use these resources."

[CONFIRME, arXiv 2411.10109v3, PDF p. 12, extraction pypdf de `paper.pdf`]

L'URL `https://github.com/joonspk-research/generative_agent` **repond HTTP 301** et redirige
vers **`https://github.com/StanfordHCI/genagents`**. C'est le meme objet : GitHub conserve les
redirections apres transfert d'un depot d'un compte a une organisation.
[CONFIRME `curl -s -o /dev/null -w "%{http_code}" https://api.github.com/repos/joonspk-research/generative_agent` renvoie 301, puis `curl -sL` renvoie `"full_name": "StanfordHCI/genagents"`]

| element | valeur | source |
|---|---|---|
| depot canonique | `StanfordHCI/genagents` | API GitHub, champ `full_name` |
| licence | **MIT**, "Copyright (c) 2024 Joon Sung Park" | `LICENSE`, API champ `license.spdx_id` = `MIT` |
| creation | 2024-11-15T10:16:20Z | API, `created_at` |
| **dernier commit** | **2024-11-18T14:36:12Z** | API, `pushed_at`, et `git log` |
| branches | `main` seule | API `/branches` |
| etiquettes, releases | **aucune** | API `/tags` et `/releases` renvoient `[]` |
| taille | 6 129 Kio annonces, 59 Mio de banque d'agents sur disque | API `size`, `du -sh agent_bank` |
| etoiles | 604 | API `stargazers_count` |
| fichiers hors banque d'agents | **28**, dont 1 867 lignes de Python | `find` et `wc -l` |

**Le depot est gele depuis le 18 novembre 2024**, soit trois jours apres sa creation et un an
et demi avant la version 3 du papier. Le champ `updated_at` du 7 septembre 2026 ne reflete que
des evenements de metadonnees, etoiles et forks, pas une modification de contenu.
[CONFIRME, `git log --format="%H %ad"` : le commit le plus recent est
`96854071ef4c2d79c93144c973c7820722d52bab`, 2024-11-18]

**Aucun mainteneur n'a jamais repondu a une issue.** Seize fils au total, huit issues ouvertes,
aucune reponse de `joonspk` ni de `akaashkolluri`. Les trois derniers fils, PR 14, 15 et 16
d'octobre 2025, viennent de tiers et ont ete fermes sans fusion.
[CONFIRME, API `/issues?state=all&per_page=100` et `/pulls/{14,15,16}`, champ `merged` a `false`]

### 1.1 Un second depot, non cite par le papier, et plus interessant

`https://github.com/joonspk-research/gabm-stanford-main`, cree le 4 novembre 2024, **onze jours
avant genagents**, commit unique "Initial commit", **sans licence**, 35 fichiers. C'est une
version anterieure de la meme base de code, et elle contient un module que `genagents` a perdu :
`generative_agent/modules/scratch.py`.
[CONFIRME https://api.github.com/repos/joonspk-research/gabm-stanford-main et
https://api.github.com/repos/joonspk-research/gabm-stanford-main/commits]

Un troisieme depot, `joonspk-research/gabm-stanford-cs222`, est la version pedagogique du meme
code, avec des trous a remplir par les etudiants ("Hint: Use agent.scratch.self_description",
`generative_agent/modules/interaction.py` ligne 35). Sans interet direct, sauf comme confirmation
que la classe `Scratch` est bien la representation officielle d'un agent chez Stanford.
[CONFIRME https://raw.githubusercontent.com/joonspk-research/gabm-stanford-cs222/main/generative_agent/modules/interaction.py]

Le quatrieme depot du compte, `joonspk-research/generative_agents`, 22 069 etoiles, est le code
de *Generative Agents: Interactive Simulacra of Human Behavior*, arXiv 2304.03442, la simulation
de Smallville. **Ce n'est pas le meme papier et il ne doit pas etre confondu avec le notre.**
[CONFIRME API, `description` = "Generative Agents: Interactive Simulacra of Human Behavior"]

Aucun depot nomme `agentbank` ou `generative_agents_bank` n'existe sous ce compte, les deux
renvoient HTTP 404.

---

## 2. Question 1 : le depot contient il le code de generation ? Que signifie LA ?

### 2.1 Le code de generation des agents du papier n'y est pas

Le depot livre une bibliotheque generique de 1 867 lignes : charger un agent depuis un dossier,
lui poser des questions categorielles ou numeriques, le faire parler, ajouter des souvenirs,
reflechir. Il ne contient **aucun script d'experience**, aucun jeu de questions du GSS, aucune
boucle sur 1 052 participants, aucun code de construction d'une condition experimentale.
Inventaire complet hors banque d'agents et hors images : `main.py`, `genagents/genagents.py`,
`genagents/modules/{interaction,memory_stream}.py`,
`simulation_engine/{gpt_structure,llm_json_parser,global_methods,example-settings}.py`,
`environment/{environment,interview/interview,survey/survey}.py`, neuf gabarits d'invite,
`README.md`, `LICENSE`, `requirements.txt`, `.gitignore`.
[CONFIRME, `find . -type f -not -path "./.git/*" -not -path "./agent_bank/*"` renvoie 28 entrees]

### 2.2 Aucune etiquette de generation n'y figure

Recherche exhaustive, mot entier, insensible a la casse, sur tout le depot hors `.git` et hors
banque d'agents, pour : `ablation`, `LA`, `persona`, `composite`, `demog`, `survey_agent`, `v3`,
`v6`, `v7`, `v8`, `lesion`, `summary`, `maximal`, `logprob`, `seed`, `exclude`, `remove`, `drop`.

**Resultat : zero occurrence pour toutes**, sauf `persona` qui n'apparait que dans trois
docstrings heritees du papier de 2023 ("Gets the current Persona object", `memory_stream.py`
lignes 211, 235, 254), et `temperature` traite en section 4.
[CONFIRME, `grep -rn -i --exclude-dir=.git --exclude-dir=agent_bank -w "<mot>" .`]

**Consequence directe.** La question posee par a1 section 7.4 et reprise par a14 section 3.3,
"que differencie concretement `gss_v6` de `gss_v8`", **ne trouve pas plus de reponse dans le
depot que dans le papier**. La piste que a14 qualifiait de "la plus rentable ouverte par cette
lecture" est fermee. Elle n'etait pas absurde, elle est simplement vide.

### 2.3 Le sigle LA reste inexplique, et la recherche est maintenant complete

Le sigle n'apparait que **deux fois dans tout le materiel disponible**, aux deux memes lignes du
paquet OSF deja citees par a1 :

> "- **Demog agents**: demographic-ablation \"LA\" variant (gen label: `v8`)"
> "> Note: `v8` is **not** interview-transcript-only; it is `ablation (demog) -- LA` in the
> generation code."

[CONFIRME `data/osf-t6g7k-stanford/camerer_five_studies_results.md`, lignes 21 et 24, verifie a
nouveau par `grep -rIn -w "LA"` sur l'ensemble du paquet OSF : deux occurrences, aucune ailleurs]

Le mot "ablation" lui meme n'apparait dans le paquet OSF qu'a cinq endroits, tous des
commentaires : les trois lignes ci dessus et les commentaires de `plot_figure_2.py` lignes 102 a
104 et 111 a 113, qui distinguent "ablation demog" de "ablation self-desc".
[CONFIRME `grep -rIn -i "ablation"` sur le paquet OSF]

Trois sources ont donc ete epuisees : le papier et ses 86 pages, le paquet OSF, le depot GitHub
et ses deux depots freres. **Aucune ne definit LA.** La phrase du paquet dit explicitement que
le sigle vient du "generation code", et le generation code n'est publie nulle part.

**Ce qu'il faut ecrire desormais dans le dossier** : "LA est une etiquette interne de la chaine
de generation de Stanford, absente du papier, du paquet de replication et du depot de code ; sa
signification est inconnue et ne peut etre obtenue qu'en ecrivant aux auteurs." Toute
interpretation du sigle serait une invention. [CONFIRME par exhaustion des trois sources]

---

## 3. Question 2 : le contenu exact des invites

### 3.1 L'invite de prediction, et une phrase que le papier a supprimee

Le depot publie l'invite complete. Version pour plusieurs questions, fichier
`simulation_engine/prompt_template/generative_agent/interaction/categorical_resp/batch_v1.txt`.
En tete du fichier, une note des auteurs :

> "Variables:
>
> Note: basically main version (ver 3) but with \"reasoning\" step"

[CONFIRME, memes lignes dans `categorical_resp/singular_v1.txt`, `numerical_resp/batch_v1.txt`
et `numerical_resp/singular_v1.txt`]

Le corps de l'invite :

> "Task: What you see above is an interview transcript. Based on the interview transcript, I
> want you to predict the participant's survey responses. All questions are multiple choice
> where you must guess from one of the options presented.
>
> As you answer, I want you to take the following steps:
> Step 1) Describe in a few sentences the kind of person that would choose each of the response
> options. (\"Option Interpretation\")
> Step 2) For each response options, reason about why the Participant might answer with the
> particular option. (\"Option Choice\")
> Step 3) Write a few sentences reasoning on which of the option best predicts the participant's
> response (\"Reasoning\")
> Step 4) Predict how the participant will actually respond in the survey. Predict based on the
> interview and your thoughts, but ultimately, DON'T over think it. Use your system 1 (fast,
> intuitive) thinking. (\"Response\")"

[CONFIRME `categorical_resp/batch_v1.txt`, ligne 16 pour l'etape 4]

Le papier, page PDF 31, publie la meme invite **sans la fin de l'etape 4** :

> "Step 4) Predict how the participant will actually respond in the survey. Predict based on the
> interview and your thoughts. (\"Response\")"

[CONFIRME, PDF p. 31, extraction pypdf ; la chaine "system 1" est **absente des 86 pages**,
recherche plein texte]

**C'est un ecart de fond, pas de forme.** La phrase supprimee, "DON'T over think it. Use your
system 1 (fast, intuitive) thinking", est une instruction de reduction de la deliberation.
Elle figure aussi dans l'invite numerique, `numerical_resp/batch_v1.txt` ligne 15. Un lecteur
du papier qui reproduit l'invite telle qu'elle est publiee **n'execute pas l'invite du depot**.
Quel effet cela a sur la dispersion des reponses est une question empirique ouverte, et c'est
precisement le genre d'instruction dont on attend qu'elle deplace la variance.

Note de prudence : rien ne prouve que l'invite du depot est celle qui a produit les chiffres du
papier. Le depot est une bibliotheque publique degagee du code d'experience. La note "basically
main version (ver 3)" suggere au contraire une **variante** de l'invite principale. Le point
etabli est plus etroit et suffit : **les deux artefacts publies par la meme equipe pour la meme
tache ne portent pas le meme texte.** [CONFIRME par comparaison mot a mot]

### 3.2 Le contexte assemble avant l'invite

Fonction `_main_agent_desc`, `genagents/modules/interaction.py` lignes 17 a 28 :

> ```
>   agent_desc += f"Self description: {agent.get_self_description()}\n==\n"
>   agent_desc += f"Other observations about the subject:\n\n"
>
>   retrieved = agent.memory_stream.retrieve([anchor], 0, n_count=120)
> ```

[CONFIRME `genagents/modules/interaction.py`, lignes 19, 20 et 22]

Deux choses en decoulent.

**Le "self description" du depot public est le dictionnaire Python brut.**
`genagents/genagents.py` ligne 97 : `return str(self.scratch)`. L'invite recoit donc
litteralement `{'first_name': 'Richard', 'last_name': 'Nez', 'age': 65, ...}`, pas une phrase.
[CONFIRME `genagents/genagents.py` lignes 96 et 97]

**Le nombre de souvenirs injectes est 120**, choisis par le score de recuperation, et l'ancre
est la concatenation des questions posees : `anchor = " ".join(list(questions.keys()))`,
`interaction.py` ligne 85. Le score de recuperation pondere recence 0, pertinence 1, importance
0,5 : `retrieve(self, focal_points, time_step, n_count=120, curr_filter="all", hp=[0, 1, 0.5], stateless=True, ...)`,
`genagents/modules/memory_stream.py` lignes 346 et 347. Le poids de recence a zero signifie que
l'ordre des souvenirs n'entre pas dans la selection ; seules la pertinence a la question et
l'importance jouent. [CONFIRME]

**Ecart avec le depot anterieur.** Dans `gabm-stanford-main`, la meme fonction assemble trois
champs et **8 souvenirs seulement** :

> ```
>   agent_desc += f"Self description: {agent.scratch.self_description}\n==\n"
>   agent_desc += f"Private information: {agent.scratch.private_self_description}\n==\n"
>   agent_desc += f"Other observations about the subject:\n\n"
>
>   retrieved = agent.memory_stream.retrieve([anchor], 0, n_count=8)
> ```

[CONFIRME https://raw.githubusercontent.com/joonspk-research/gabm-stanford-main/main/generative_agent/modules/interaction.py]

Huit contre cent vingt. Ce n'est pas un detail de reglage : c'est la difference entre injecter
un extrait et injecter tout un entretien. Le papier ne donne aucun des deux chiffres. Lequel a
produit les resultats publies est indeterminable.

### 3.3 La condition demographique : ce que le code montre

Le depot public ne contient pas la condition demographique du papier, mais il contient **la
representation Stanford d'un agent demographique**, a deux endroits independants.

**Premier endroit, la banque publique.** Chacun des 3 505 agents de `agent_bank/populations/gss_agents/`
porte un `scratch.json` de **30 champs strictement identiques d'un agent a l'autre**. Exemple
integral, agent `67d6f6df-32ac-430e-a78a-dba78881beb7` :

> ```
> {"first_name": "Richard", "last_name": "Nez", "age": 65, "sex": "Male",
>  "ethnicity": "American Indian", "race": "Other",
>  "detailed_race": "Native American or Alaska Native", "hispanic_origin": "Not Hispanic",
>  "street_address": "1234 Cedar Circle", "city": "Overland Park", "state": "KS",
>  "political_views": "Liberal", "party_identification": "Not very strong democrat",
>  "residence_at_16": "West North Central", "same_residence_since_16": "Same state, different city",
>  "family_structure_at_16": "Lived with parents", "family_income_at_16": "Average",
>  "fathers_highest_degree": "High school", "mothers_highest_degree": "High school",
>  "mothers_work_history": "Yes", "marital_status": "Married",
>  "work_status": "Working part time", "military_service_duration": "No active duty",
>  "religion": "Protestant", "religion_at_16": "Protestant", "born_in_us": "Yes",
>  "us_citizenship_status": "A U.S. citizen", "highest_degree_received": "Graduate",
>  "speak_other_language": "No", "total_wealth": "$1 million to $2 million"}
> ```

[CONFIRME `agent_bank/populations/gss_agents/67d6f6df-32ac-430e-a78a-dba78881beb7/scratch.json`,
et verification par script que les 3 505 agents partagent le meme jeu de 30 cles]

**`political_views` et `party_identification` sont deux des trente champs.** L'ideologie
politique et le parti figurent dans la representation demographique de Stanford.

**Second endroit, la classe `Scratch` du depot anterieur**, qui n'existe plus dans genagents :

> ```
>     self.census_division = ""
>     self.political_ideology = ""
>     self.political_party = ""
>     self.education = ""
>     self.race = ""
>     self.ethnicity = ""
>     self.annual_income = 0.0
>     ...
>     self.fact_sheet = ""
>     self.speech_pattern = ""
>     self.self_description = ""
>     self.private_self_description = ""
> ```

[CONFIRME https://raw.githubusercontent.com/joonspk-research/gabm-stanford-main/main/generative_agent/modules/scratch.py]

Sept de ces noms de champs sont **identiques caractere pour caractere** aux colonnes du fichier
demographique du paquet OSF : `age`, `census_division`, `political_ideology`, `political_party`,
`education`, `race`, `ethnicity`.
[CONFIRME, en tete de `data/osf-t6g7k-stanford/figure3/data/demographic_summary.csv` :
`email,age,census_division,political_ideology,political_party,education,race,ethnicity,gender,income,neighborhood,sexual_orientation`]

C'est la meme structure de donnees des deux cotes. **La deduction de a2 section 2.1, "l'agent
demographique n'a probablement pas recu l'orientation politique", est desormais contredite par
trois artefacts de code independants** : la classe `Scratch` de Stanford, la banque publique de
3 505 agents, et le fichier demographique du paquet de replication, en plus de l'exemple
litteral du materiel supplementaire deja releve par a14 section 3.1.

### 3.4 La condition persona : confirmee comme texte humain

Le paquet OSF nomme la condition "Persona/self-desc agents: self-description ablation (gen label:
`v4`)" [CONFIRME `camerer_five_studies_results.md` ligne 22], le depot anterieur porte un champ
`self_description`, et le papier dit que le paragraphe est ecrit par le participant. Les trois
concordent. **Le persona du papier n'est pas un texte genere par un modele.** La reponse a la
question posee est donc : texte narratif, mais ecrit a la main par la personne, a la fin de sa
phase 1, sur consigne de se decrire a un inconnu.
[CONFIRME PDF p. 40 pour la consigne, deja cite par a14 section 3.2]

Le depot ajoute un element que le papier ne mentionne pas : un champ **`private_self_description`**
distinct de `self_description`, injecte dans l'invite sous l'etiquette "Private information:".
Le papier ne decrit nulle part ce second champ. Ce qu'il contenait est inconnu. [CONFIRME pour
l'existence du champ, inconnu pour son contenu]

### 3.5 Les conditions enquete et composite

**Absentes du depot.** Aucun code ne construit une entree a partir de reponses d'enquete, ni ne
combine entretien et enquete. Ces deux conditions n'existent que dans le papier et dans les
sorties du paquet OSF. [CONFIRME par la recherche de la section 2.2]

### 3.6 La reflexion d'expert : le module du papier n'est pas celui du depot

Le papier decrit, page PDF 5 :

> "Each agent also stores a set of expert reflections: short, model-generated notes written from
> the perspective of four social-science experts (a psychologist, behavioral economist, political
> scientist, and demographer)"

[CONFIRME PDF p. 5, et developpement p. 29]

L'invite de reflexion du depot ne contient **aucune persona d'expert** :

> "Task: Above are observations about a fictional human subject. Write a list of !<INPUT 1>!
> reflections (in first person voice, from the perspective of the subject) that you can infer
> from the observations above about the subject on the following anchoring topic/phrase:
> \"!<INPUT 2>!\"."

[CONFIRME `simulation_engine/prompt_template/generative_agent/memory_stream/reflection/batch_v1.txt`,
ligne 8]

C'est l'inverse exact : le papier fait ecrire quatre experts a la troisieme personne, le depot
fait ecrire le sujet a la premiere personne. Une issue le demande depuis le 23 decembre 2024,
"Request for Expert Reflection Prompt Templates", **sans reponse a ce jour**.
[CONFIRME https://github.com/StanfordHCI/genagents/issues/11, champ `comments` a 0]

Or l'invite de prediction du papier prend en entree "Participant's interview transcript **and
relevant expert reflections**" [CONFIRME PDF p. 31]. **La moitie de l'entree du papier n'est
donc pas reproductible depuis le depot.**

---

## 4. Question 3 : le decodage

C'est l'apport le plus net de cette lecture. a14 section 6.3 concluait "Le papier n'est pas
reproductible sur le plan du decodage". Le depot comble trois des quatre trous.

| element | valeur | source |
|---|---|---|
| **temperature** | **0.7**, en dur, non parametrable | `simulation_engine/gpt_structure.py` ligne 74 |
| modele par defaut de la fonction | `"gpt-4o"` | `gpt_structure.py` ligne 54 |
| modele par defaut des reglages livres | **`"gpt-4o-mini"`** | `simulation_engine/example-settings.py` ligne 11 |
| plafond de jetons | `max_tokens: int = 1500` | `gpt_structure.py` ligne 55 |
| **nombre d'echantillons** | **un seul appel**, `repeat=1` partout | `gpt_structure.py` ligne 99, et `interaction.py` lignes 78, 129, 171 |
| graine | **aucune** | recherche `seed` : zero occurrence |
| log probabilites | **aucune** | recherche `logprob` : zero occurrence |
| embeddings | `text-embedding-3-small` | `gpt_structure.py` ligne 156 |

Le corps de l'appel, `gpt_structure.py` lignes 68 a 78 :

> ```
>     response = client.chat.completions.create(
>       model=model,
>       messages=[{"role": "user", "content": prompt}],
>       max_tokens=max_tokens,
>       temperature=0.7
>     )
> ```

[CONFIRME, memes lignes et meme valeur dans le depot anterieur
https://raw.githubusercontent.com/joonspk-research/gabm-stanford-main/main/simulation_engine/gpt_structure.py]

Le parametre `repeat` existe mais ne sert **qu'a reessayer apres une erreur**, jamais a voter :

> ```
>     for i in range(repeat):
>       response = gpt_request(prompt, model=gpt_version)
>       if response != "GENERATION ERROR":
>         break
>       time.sleep(2**i)
> ```

[CONFIRME `gpt_structure.py` lignes 134 a 138. Bogue au passage : le test compare a la chaine
exacte `"GENERATION ERROR"` alors que la fonction renvoie `f"GENERATION ERROR: {str(e)}"`, donc
la condition est toujours vraie et **aucune reessai n'a jamais lieu**, `gpt_structure.py`
lignes 66 et 78]

### 4.1 L'extraction de la modalite : il n'y en a pas

C'est le point le plus important de la section 4. Fichier
`simulation_engine/llm_json_parser.py`, lignes 40 a 47, dans son integralite :

> ```
> def extract_first_json_dict_categorical(input_str):
>   reasoning_pattern = r'"Reasoning":\s*"([^"]+)"'
>   response_pattern = r'"Response":\s*"([^"]+)"'
>
>   reasonings = re.findall(reasoning_pattern, input_str)
>   responses = re.findall(response_pattern, input_str)
>
>   return responses, reasonings
> ```

[CONFIRME `simulation_engine/llm_json_parser.py` lignes 40 a 47]

**Il n'y a aucun appariement a la nomenclature.** La reponse retenue est la chaine brute que le
modele a ecrite apres `"Response":`, quelle qu'elle soit. Aucune verification qu'elle appartient
a la liste d'options passee dans l'invite, aucune normalisation de casse ou de ponctuation,
aucun repli, aucun rejet, aucun comptage des reponses hors nomenclature.

Quatre consequences, toutes verifiables sur le code.

1. **Une reponse hors nomenclature est enregistree telle quelle.** C'est exactement le phenomene
   que a1 section 7.4 a du traiter a la main sur les fichiers OSF, phrases de justification et
   variantes de ponctuation comptees comme des modalites nouvelles. Le mecanisme est maintenant
   identifie dans le code, ce n'etait plus une conjecture.
2. **La reponse est cherchee dans tout le texte, y compris dans les etapes de raisonnement.**
   `re.findall` ne s'arrete pas au JSON : la fonction s'appelle `extract_first_json_dict_categorical`
   mais ne parse aucun JSON.
3. **L'appariement question / reponse est purement positionnel.**
   `environment/survey/survey.py` lignes 76 et 77 : `{question: output["responses"][i] for i, question in enumerate(questions.keys())}`.
   Si le modele omet une question ou en ajoute une, tout le bloc glisse d'un cran, sans erreur.
4. **Une reponse contenant un guillemet double casse la capture**, parce que la classe `[^"]+`
   s'arrete au premier guillemet.

Le pendant numerique, lignes 50 a 56, capture `r'"Response":\s*(\d+\.?\d*)'`, ce qui **rejette
silencieusement toute valeur negative** puisque le signe moins n'est pas dans le motif.
[CONFIRME `llm_json_parser.py` ligne 52]

Enfin, le decoupage en lots est reel : une invite est envoyee par lot de questions, `batch_v1.txt`
au dela d'une question, `singular_v1.txt` pour une seule [CONFIRME `interaction.py` lignes 69 a
72]. La taille du lot est censee etre pilotee par `MAX_CHUNK_SIZE = 4` des reglages, mais **cette
constante n'est utilisee nulle part dans le code**, recherche exhaustive : trois occurrences, le
README, le fichier de reglages d'exemple, et rien d'autre. [CONFIRME `grep -rn "MAX_CHUNK_SIZE"`]

---

## 5. Question 4 : la regle de retrait de la question predite

**Elle n'est pas dans le depot.** Aucune fonction ne filtre le contexte en fonction de la
question posee. Les recherches sur `exclude`, `remove`, `drop` ne renvoient rien, et la lecture
integrale de `interaction.py` et `memory_stream.py` confirme que le contexte est assemble sans
connaissance de la cible : `_main_agent_desc` recoit l'ancre, s'en sert pour classer les
souvenirs par pertinence, et n'en retire aucun.
[CONFIRME, `genagents/modules/interaction.py` lignes 17 a 28]

La regle n'existe donc que dans le texte du papier, et il en existe **deux formulations**, que
a14 ne rapproche pas :

> "When we use as input any GSS questions from the first survey wave while predicting on the GSS
> in the second wave, we ensure that the question we are predicting on is not in the input for
> the agents." [CONFIRME PDF p. 38]

> "As discussed in the manuscript, when we evaluate on constructs that are used in the input for
> the agents, we ensure to remove the question we predict on from the input (for the GSS), and
> all questions in the same question block (for the Big5)." [CONFIRME PDF p. 32]

Les deux conditionnent le retrait au fait que **les questions du GSS soient l'entree de l'agent**.
Or l'entree de l'agent demographique n'est pas un jeu de questions du GSS, c'est un descripteur
reconstruit a partir de ces reponses. Le papier ecrit d'ailleurs : "We reconstruct these
descriptors for our participants using their responses to the GSS. Then, to prompt the language
model with this data, we replace any other self-report data with the demographic descriptors."
[CONFIRME PDF p. 40]

**L'hypothese de reconciliation de a14 section 3.1 n'est donc ni confirmee ni infirmee par le
depot, et elle est un peu moins confortable qu'elle ne le paraissait.** Les deux enonces de la
regle visent des items du GSS presents dans l'entree, pas un attribut derive. Le seul moyen de
trancher est d'ecrire aux auteurs, ou de mesurer : si l'ideologie avait ete retiree seulement sur
`polviews`, l'exactitude de l'agent demographique sur cet item precis serait basse et normale
partout ailleurs, ce que a2 a deja observe. Si elle avait ete absente partout, on attendrait un
deficit diffus sur tous les items politiquement charges. **Ce test est faisable sur les fichiers
deja en place, sans appel de modele, et il tranche l'alternative.** C'est le test le moins cher
identifie par ce rapport. [HYPOTHESE pour le mecanisme, PROBABLE pour la faisabilite du test]

---

## 6. Question 5 : traces, sorties, banques d'agents, licence

**Aucune trace d'execution, aucune sortie de generation, aucun fichier de reponses.** Le depot ne
contient pas une seule reponse produite par un agent du papier.

**Deux banques d'agents, en revanche, et elles sont telechargeables.**

| banque | contenu | souvenirs | licence |
|---|---|---|---|
| `agent_bank/populations/gss_agents/` | **3 505 agents**, 30 attributs demographiques chacun | **0**, `nodes.json` et `embeddings.json` vides pour les 3 505 | MIT |
| `agent_bank/populations/single_agent/` | **1 agent**, Joon Sung Park lui meme | **116 observations**, transcription d'entretien decoupee par paire question reponse | MIT |

[CONFIRME par script sur le clone : `nodes count distribution Counter({0: 3505})`, un seul jeu de
30 cles pour les 3 505, et 116 noeuds de type `observation` pour l'agent unique]

Les 3 505 agents demographiques sont conformes au codage du GSS : `political_views` a sept
modalites, de "Extremely liberal" a "Extremely conservative", `party_identification` a huit
modalites. Distribution mesuree : "Moderate, middle of the road" 1 370, "Liberal" 485,
"Conservative" 483, "Slightly conservative" 419, "Slightly liberal" 395, "Extremely liberal" 200,
"Extremely conservative" 153 ; 1 882 femmes et 1 623 hommes.
[CONFIRME par comptage sur les 3 505 `scratch.json`]

Le README precise leur statut :

> "**Demographic Agent Banks**: A bank of over 3,000 agents created using demographic information
> from the General Social Survey (GSS) as a starting point to explore the codebase. *Note: The
> names and addresses are fictional.*"

[CONFIRME `README.md`]

**Ces agents ne sont pas les 1 052 participants du papier.** Ce sont des personas demographiques
synthetiques. Le README est explicite sur la banque du papier :

> "Due to participant privacy concerns, the full agent bank containing over 1,000 generative
> agents based on real interviews is not publicly available at the moment. However, we plan to
> make aggregated responses on fixed tasks accessible for general research use in the coming
> months."

[CONFIRME `README.md`]

Cette promesse date de novembre 2024. **Vingt et un mois plus tard, le depot n'a pas bouge, aucune
issue n'a recu de reponse, et aucune API n'est annoncee.** Le depot Stanford Digital Repository
`purl.stanford.edu/jm164ch6237` ne contient que la these de doctorat de Park, sous CC BY-NC, sans
code ni donnees. [CONFIRME https://purl.stanford.edu/jm164ch6237 ; PROBABLE pour l'absence d'API,
fonde sur l'absence de toute trace publique et sur le gel du depot]

**Le point pratique pour popsim.** La licence MIT couvre tout le depot, code et banque. Les
3 505 personas demographiques sont donc utilisables, redistribuables et modifiables sans
autorisation, sans cout et sans humain, sous reserve de conserver l'avis de copyright. Ils sont
des personas synthetiques, pas des microdonnees : **les contraintes 2 et 5 de la passation ne
s'y appliquent pas.**

---

## 7. Question 6 : ce qui, dans le depot, differe de ce que le papier decrit

Sept ecarts, ranges du plus grave au plus anodin. Les deux premiers sont des affirmations du
papier que ses propres artefacts contredisent.

**1. Le papier annonce que le code de generation est sur OSF. Il n'y est pas.**
Le papier ecrit "The code for generating all the different agents is available in an open-source
repository here: https://osf.io/t6g7k/files/osfstorage" [CONFIRME PDF p. 12]. Le paquet OSF
contient **15 fichiers Python**, tous d'analyse et de trace : trois `run_pipeline.py`, quatre
scripts d'analyse, deux de trace, des utilitaires. **Aucun n'importe `openai`, n'appelle
`chat.completions` ni ne lit un gabarit d'invite.**
[CONFIRME `find . -name "*.py" | wc -l` renvoie 15 sur `data/osf-t6g7k-stanford`, et
`grep -rIl -i "openai\|chat.completions\|gpt-4\|prompt_template" --include="*.py" .` ne renvoie
aucun fichier]

**2. Le papier annonce que l'enqueteur IA est sur GitHub. Il n'y est pas.**
Le papier ecrit "The code to create the interview agents, including the AI interviewer, can be
found here" [CONFIRME PDF p. 12]. Le depot ne contient aucun enqueteur. La classe
`environment/interview/interview.py` fait interviewer un agent par un script fige de questions,
ce qui est l'inverse. Une issue le signale depuis le 8 decembre 2024, "Is there a plan to open
source the interviewer agent?", trois commentaires de tiers, **aucune reponse des auteurs**. Un
utilisateur y ecrit :

> "it appears that the interviewer agent is not implemented in the codebase at this time. The
> `_interview_agent` method in `environment/interview/interview.py` is used for interviewing
> other generative agents using the questions listed in the interview script, rather than
> implementing the interviewer agent itself."

[CONFIRME https://github.com/StanfordHCI/genagents/issues/6, commentaire de `kirisame-wang`,
2025-02-20]

**Ces deux points signifient que ni la generation des agents ni la conduite des entretiens ne
sont reproductibles, alors que le papier declare les deux disponibles.** C'est un constat plus
grave que la double generation demographique de a14 section 3.3, parce qu'il ne demande aucune
arithmetique : il suffit de suivre les deux liens du papier.

**3. L'invite publiee dans le papier n'est pas celle du depot.** Section 3.1 ci dessus. La phrase
"DON'T over think it. Use your system 1 (fast, intuitive) thinking" existe dans le depot et est
absente des 86 pages.

**4. Le module de reflexion d'expert du papier n'existe pas dans le depot.** Section 3.6. Le
papier decrit quatre personas d'expert a la troisieme personne, le depot fait reflechir le sujet
a la premiere personne, et l'invite de prediction du papier prend les reflexions d'expert en
entree.

**5. Le modele par defaut des reglages livres est `gpt-4o-mini`, pas `gpt-4o`.** Le papier ecrit
"We use GPT-4o for all agent types" [CONFIRME PDF p. 5]. Le fichier de reglages et le README du
depot indiquent `LLM_VERS = "gpt-4o-mini"` [CONFIRME `example-settings.py` ligne 11 et
`README.md`]. Un utilisateur qui suit le README a la lettre execute le modele que le papier
classe **dernier** de son etude de robustesse, a 0,60 contre 0,66.

**6. Le nombre de souvenirs injectes differe entre les deux depots Stanford**, 120 contre 8.
Section 3.2. Le papier ne donne ni l'un ni l'autre.

**7. Le sous dossier `environment/` du depot public est du code mort.**
`environment/interview/interview.py` ligne 40 et `environment/survey/survey.py` ligne 44 appellent
`GenerativeAgent(population, agent_id)` avec deux arguments, alors que le constructeur publie en
prend un seul, `def __init__(self, agent_folder=None)` [CONFIRME `genagents/genagents.py` ligne
12]. `interview.py` ligne 45 appelle `curr_agent.scratch.get_fullname()`, or `scratch` est un
dictionnaire dans cette version. `interaction.py` ligne 220 pointe vers
`prompt_template/generative_agent/interaction/ask/batch_v1.txt`, **fichier qui n'existe pas**
dans le depot [CONFIRME `ls simulation_engine/prompt_template/generative_agent/interaction/`
renvoie trois entrees, `categorical_resp`, `numerical_resp`, `utternace`]. Ces fragments viennent
du depot anterieur et n'ont pas ete adaptes. Le depot public **n'a jamais ete execute en entier**.

---

## Ce que cette lecture change au dossier

### a1-double-distorsion.md, section 7

**Section 7.2, dernier paragraphe.** La phrase "le paquet ne contient ni le code de generation ni
les invites, seulement le code d'analyse et de trace, ce qui a ete verifie par recherche
exhaustive sur les fichiers du paquet" est **exacte et doit etre renforcee**, pas corrigee : la
recherche a ete refaite independamment ici, 15 fichiers Python, aucun appel de modele. Ajouter
une phrase : "Le depot GitHub cite par le papier ne les contient pas davantage, verification du
7 septembre 2026."

**Section 7.4, deuxieme paragraphe "Non etabli non plus".** La phrase "Le seul element est la
mention `ablation (demog) -- LA` pour `v8`, dont la signification de `LA` n'est explicitee nulle
part dans le paquet" doit devenir : "dont la signification n'est explicitee **ni dans le paquet,
ni dans le papier, ni dans le depot de code de Stanford ni dans ses deux depots freres**". La
recherche est close, trois sources epuisees. Cela transforme une lacune apparente du dossier en
un constat sur le materiel publie.

**Section 7.4, avertissement de methode final.** L'avertissement sur les reponses mal formees
gagne **une explication mecanique** : l'extraction de Stanford est l'expression reguliere
`r'"Response":\s*"([^"]+)"'`, sans aucun appariement a la nomenclature, `llm_json_parser.py`
lignes 40 a 47. Ce n'etait pas une negligence de mesure de notre cote, c'est une propriete de
leur chaine. Ajouter la citation exacte du code : elle rend l'avertissement opposable.

**Section 8, limites.** a14 section 6.3 demandait d'ajouter aux limites de a1 que "toute mesure
de diversite de reponse que nous produisons sur leurs fichiers de sortie est necessairement
confondue avec un reglage de temperature inconnu". **La temperature n'est plus inconnue : 0,7,
en dur, dans les deux depots Stanford.** La limite doit etre reformulee, pas supprimee, parce que
rien ne prouve que le code d'experience employait la meme valeur que la bibliotheque publique.
Formulation proposee : "Le seul chiffre de temperature publie par l'equipe est 0,7, en dur dans
`simulation_engine/gpt_structure.py` ligne 74 de son depot public ; le papier n'en donne aucun,
et rien n'etablit que le code d'experience employait cette valeur."

**Section 7.5, test suivant.** Le test propose sur `econ_games` et `bigfive` reste le bon.
S'y ajoute maintenant un second test, moins cher, decrit en section 5 ci dessus : mesurer si le
deficit de l'agent demographique est concentre sur `polviews` ou diffus sur les items politiques,
ce qui tranche l'hypothese de la regle de retrait.

### a2-baselines.md, section 2.1

**Le paragraphe "L'agent demographique n'a probablement pas recu l'orientation politique" doit
etre reecrit.** Il etait donne comme une deduction explicite, et la deduction est fausse. Trois
artefacts de code de Stanford portent l'ideologie politique et le parti dans la representation
d'un agent demographique : la classe `Scratch` du depot `gabm-stanford-main`, champs
`political_ideology` et `political_party` ; les 3 505 `scratch.json` de la banque publique,
champs `political_views` et `party_identification` ; et les colonnes du fichier
`figure3/data/demographic_summary.csv` du paquet OSF. S'y ajoute l'exemple litteral du materiel
supplementaire releve par a14. **L'honnetete du dossier exige de dire que cette deduction, faite
de bonne foi sur un fait mesure, a ete infirmee par le code.**

**La phrase suivante doit etre corrigee dans la foulee.** "Consequence, la comparaison B1 contre
agent demographique n'est pas un duel a armes egales" : c'est l'inverse. La comparaison a armes
egales est **B1 complet a 0,6209 contre 0,5818**, comme a14 section 3.1 l'a deja ecrit. La
variante privee de l'ideologie et du parti, 0,5998, n'est pas la comparaison de reference ; elle
reste utile comme borne, mais elle doit etre presentee comme telle et non comme le duel loyal.

**Le fait mesure, lui, ne bouge pas et reste precieux.** L'agent demographique obtient 0,1996 sur
`polviews`, sous la modalite majoritaire a 0,2880. Ce fait demande une explication, et il en
reste deux : la regle de retrait, ou un traitement particulier de cet item. Le dossier doit
porter le fait et les deux explications, sans en choisir une.

**Le retrait de `polviews` de la cible, lui, reste entierement justifie** et n'est pas affecte :
l'identite caractere pour caractere entre l'item et l'attribut demographique est un fait mesure
sur les 1 052 participants.

### a14-lecture-2411-10109-v3.md

**"Ce que je n'ai pas pu verifier", point 5.** A remplacer : le depot a ete consulte le
7 septembre 2026. Il ne contient pas le code de generation, il ne repond ni a la question des
deux generations demographiques ni a celle de `LA`. La piste est fermee, la demonstration
arithmetique de la section 3.3 reste le meilleur element du dossier sur ce point.

**Questions ouvertes pour Simon, question 4.** "Le depot GitHub doit il etre ouvert maintenant ?
Une demi journee." A remplacer par le resultat : c'est fait, cela a pris deux heures, et le
rendement est different de celui espere. Le depot ne tranche pas la question des deux
generations, mais il livre le decodage et deux contradictions entre le papier et ses artefacts.

**Section 6.3.** Les quatre manques declares deviennent : temperature **connue** a 0,7 dans le
depot public, nombre d'echantillons **connu** a un seul appel, graine **toujours absente**,
analyse syntaxique de la reponse **connue** et reduite a une expression reguliere sans
appariement a la nomenclature. La conclusion "Le papier n'est pas reproductible sur le plan du
decodage" tient toujours, parce que rien n'etablit que le code d'experience partageait ces
reglages, mais elle doit citer les valeurs plutot que constater leur absence.

**Section 3.2, invite persona.** Ajouter le champ `private_self_description`, qui existe dans le
code de Stanford, qui est injecte dans l'invite sous l'etiquette "Private information:", et dont
le papier ne parle jamais.

**Section 6.2.** L'invite reproduite depuis le papier doit etre accompagnee de la version du
depot et de leur difference, la phrase sur le "system 1". C'est un ecart entre deux artefacts de
la meme equipe, il se cite en deux lignes.

**Nouvelle section a ouvrir, et c'est la plus rentable.** Les deux liens de reproductibilite du
papier, page 12, pointent l'un et l'autre vers des artefacts qui ne contiennent pas ce qu'il
annonce. Cela se verifie en cliquant. C'est du meme ordre que la reconstruction arithmetique de
la section 3.3, et cela porte sur la meme phrase du papier : ce qui est declare disponible ne
l'est pas.

### PASSATION.md, section 6

Ajouter une ligne a "L'etat des lieux materiel" : une banque de 3 505 personas demographiques
sous licence MIT est telechargeable, `github.com/StanfordHCI/genagents`, dossier
`agent_bank/populations/gss_agents/`, 59 Mio, 30 attributs par agent dont l'ideologie et le parti,
zero souvenir. Rappel de la contrainte du Bureau synchronise iCloud : la stocker hors du Bureau.

---

## Ce que je n'ai pas pu verifier

1. **Que l'invite du depot soit celle qui a produit les chiffres du papier.** La note interne
   "basically main version (ver 3) but with \"reasoning\" step" suggere le contraire. Ce qui est
   etabli est l'ecart entre deux textes publies, pas lequel a servi.
2. **Que la temperature 0,7 soit celle du code d'experience.** Elle est en dur dans les deux
   depots publics de l'equipe, ce qui est un indice fort, pas une preuve.
3. **Le contenu de `private_self_description`.** Le champ existe, il est injecte dans l'invite,
   son contenu n'est documente nulle part.
4. **Les 116 observations de l'agent unique** n'ont ete lues qu'en tete et en queue, trois noeuds
   de chaque cote. Leur decoupage, une paire question reponse par noeud, a ete verifie par
   echantillonnage, pas exhaustivement.
5. **Les forks du depot.** Certains, comme la branche `add_new_model_options` de `AdonaiVera`
   citee dans l'issue 2, ajoutent Anthropic et GPT4All. Aucun n'a ete examine. Un fork pourrait
   contenir du code de generation reconstitue, ce serait un travail tiers et non une source
   Stanford.
6. **L'existence eventuelle d'une API de la banque d'agents.** Recherche web negative, depot gele,
   aucune annonce trouvee. Je ne peux pas prouver une absence.
7. **Les pull requests 14, 15 et 16**, fermees sans fusion, n'ont ete lues qu'en titre et en
   metadonnees. La PR 14 touche 16 209 fichiers, ce qui est presque certainement un re-import de
   la banque d'agents et non un apport de code.
8. **Le materiel supplementaire du papier au dela des pages citees par a14.** Je n'ai extrait que
   les pages 5, 12, 29, 31, 32, 40 et 54 pour les comparaisons de ce rapport.

---

## Questions ouvertes pour Simon

1. **Les deux liens morts du papier se publient ils, et sous quelle forme ?** Le papier declare
   page 12 que le code de generation est sur OSF et que l'enqueteur est sur GitHub. Ni l'un ni
   l'autre n'y est. Cela se verifie en deux clics, sans arithmetique, et cela concerne la
   reproductibilite declaree d'un papier publie. Est ce une ligne de la section methode de notre
   papier sur la mesure, une note aux auteurs, ou un simple element de dossier a garder ?
   La question est la meme que la question 1 de a14, posee sur un constat different.

2. **Faut il utiliser les 3 505 agents MIT, et pour quoi ?** Ils sont gratuits, sans humain, sans
   licence restrictive, avec ideologie et parti. Ils ne sont pas les participants du papier et ne
   permettent aucune comparaison de fidelite. Mais ils constituent une population de personas
   demographiques prete a l'emploi pour le chantier 3, le retrecissement calibre des ecarts inter
   groupes, ou pour la courbe de croisement de a2 sur un troisieme jeu. **Est ce une distraction
   ou une economie de deux jours ?**

3. **Le test de la regle de retrait vaut il la demi journee ?** Mesurer si le deficit de l'agent
   demographique est concentre sur `polviews` ou diffus sur les items politiques trancherait entre
   les deux explications restantes, sur des fichiers deja en place et sans appel de modele. Cela
   solderait une contradiction ouverte entre a2 et a14. Le risque est que le resultat soit
   ambigu et n'ajoute rien.

4. **L'ecart d'invite se mesure il ?** La phrase "DON'T over think it. Use your system 1" est une
   instruction de reduction de la deliberation, et notre these porte sur la variance. Comparer
   les deux invites sur nos modeles locaux, avec et sans cette phrase, est un protocole propre,
   peu couteux, et il teste directement si une instruction de decodage deplace la variance intra
   et inter. **Est ce le premier resultat original du projet sur des agents que nous generons
   nous memes, ou un detour ?**

5. **Faut il ecrire aux auteurs maintenant, et cette lecture change t elle la reponse ?** a14
   posait la question sur la double generation demographique. Il y a desormais trois sujets a
   leur soumettre : les deux generations, les deux liens morts, et le sens de `LA`. Le troisieme
   est une simple demande de clarification qui n'a rien d'accusatoire et qui ouvrirait le
   dialogue sur les deux autres. **Est ce un angle d'approche acceptable, sachant que Park,
   Bernstein et Liang dirigent Simile ?**

---

## Reproduction

```
cd "$SCRATCH"
git clone https://github.com/StanfordHCI/genagents.git
curl -sL "https://api.github.com/repos/joonspk-research/generative_agent"   # -> StanfordHCI/genagents
curl -s "https://api.github.com/repos/StanfordHCI/genagents/issues?state=all&per_page=100"
curl -sL -A "Mozilla/5.0" -o paper.pdf https://arxiv.org/pdf/2411.10109v3
```

Verification de l'absence des etiquettes de generation :

```
cd genagents
grep -rn -i --exclude-dir=.git --exclude-dir=agent_bank -w "ablation\|LA\|v8\|logprob\|seed" .
# -> aucune sortie
```

Inventaire de la banque d'agents :

```
python3 - <<'PY'
import json, os, collections
base = "agent_bank/populations/gss_agents"
ds = sorted(os.listdir(base))
nodes = collections.Counter()
keys = collections.Counter()
for d in ds:
    nodes[len(json.load(open(f"{base}/{d}/memory_stream/nodes.json")))] += 1
    keys[tuple(sorted(json.load(open(f"{base}/{d}/scratch.json"))))] += 1
print(len(ds), nodes, len(keys))
# -> 3505 Counter({0: 3505}) 1
PY
```

Verification que le paquet OSF ne contient pas de code de generation :

```
cd data/osf-t6g7k-stanford
find . -name "*.py" | wc -l                                                       # 15
grep -rIl -i "openai\|chat.completions\|gpt-4\|prompt_template" --include="*.py" . # rien
```
