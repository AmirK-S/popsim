# 04. Protocole de reproduction

Agent 4. Redige le 2 septembre 2026. Revision 2, integrant les elements verifies transmis par la
coordination (archive OSF de Stanford, jeu Twin-2K-500, resultats de juillet 2026, mesures
materielles de l'agent infrastructure).

Contraintes appliquees : budget zero, aucun humain recrute, phase exploratoire, documents et non
implementations.

Etat de coordination : `exploration/05-datasets-publics.md` et
`exploration/06-infrastructure-zero-cout.md` n'etaient pas encore ecrits sur disque au moment de
la redaction, mais leurs conclusions m'ont ete transmises et sont integrees ici. Les elements que
je reprends sans les avoir verifies moi meme sont etiquetes `[VERIFIE PAR COORDINATION]`.

---

## Resume executif, a lire en premier

1. **Dimension recommandee : les opinions politiques et sociales.** Recommandation renforcee par un
   resultat qui disqualifie serieusement l'alternative : chez Stanford, sur les jeux economiques
   incites, **aucune condition d'agent ne se distingue des autres** (F = 1,63, p = 0,16), y compris
   la condition demographique. Or les jeux economiques sont le proxy le plus proche du comportement
   d'achat dans la batterie. Commencer par le comportement d'achat, c'est commencer par le seul
   domaine ou la litterature a deja constate l'absence de signal.

2. **Jeu de donnees recommande pour la voie A, en deux temps.**
   - **Substrat de reanalyse immediate : l'archive OSF du papier de Stanford,
     `https://osf.io/t6g7k/`.** Elle contient les reponses individuelles reelles des 1 052
     participants (vague 1 **et** vague 2) **et les reponses produites par les cinq conditions
     d'agents**. Consequence : **on peut calculer nos metriques de variance sur les sorties de
     Stanford sans passer un seul appel de modele.** C'est l'etape 1 du protocole et elle coute
     zero euro et zero minute de calcul.
   - **Substrat de replication de bout en bout : Twin-2K-500**, 2 058 personnes, plus de 500
     questions, quatre vagues, entierement public sur Hugging Face avec son code
     (`https://huggingface.co/datasets/LLM-Digital-Twin/Twin-2K-500`, papier arXiv:2505.17479).
   - Le panel roulant du GSS passe en troisieme position, comme test de generalisation.

3. **Metrique de variance retenue : l'Indice de Diversite Preservee (IDP)**, moyenne geometrique de
   **six** sous scores dans [0,1]. Deux d'entre eux sont nouveaux par rapport a la version 1 de ce
   document et repondent directement aux resultats de juillet 2026 : la dispersion inter individus
   est **corrigee du bruit intra personne** grace a la vague de retest, et un sixieme sous score
   penalise la **sur determination demographique**, c'est a dire le fait documente que les modeles
   gonflent les ecarts entre segments.

4. **Changement de methode d'evaluation : on lit les probabilites de tokens, on ne genere pas de
   texte.** Sur des questions fermees, lire la distribution de probabilite du modele sur les
   modalites de reponse est environ mille fois moins cher, supprime le bruit d'echantillonnage, et
   **donne directement la decomposition de la variance totale en variance intra individu plus
   variance inter individus**. C'est exactement la quantite que le projet veut mesurer. C'est le
   mode par defaut du protocole. Justification complete en A.8.

5. **Le facteur limitant du projet n'est pas le calcul, c'est la matiere humaine. Le budget zero
   n'est pas une contrainte serieuse pour la phase 1.** Mon calcul de puissance independant
   converge avec celui de l'agent infrastructure : **70 a 100 personas sur 30 a 50 questions**
   suffisent pour la phase 1, soit de l'ordre de 15 a 60 minutes de calcul sur le Mac d'Amir.
   Capacite locale mesuree : environ 400 000 appels par semaine, contre environ 12 000 par semaine
   pour toutes les offres gratuites d'API cumulees `[VERIFIE PAR COORDINATION]`. C'est le message a
   faire passer a Simon : ce qui bloque, ce n'est pas l'argent.

6. **Deux avertissements de la litterature de juillet 2026 sont integres comme contraintes de
   protocole, pas comme remarques.** Sur la prediction individuelle, des baselines statistiques
   simples battent les LLM ; et les modeles sur determinent les demographies. Cela impose des
   baselines non LLM **obligatoires** (section A.4) et une metrique de sur determination
   (section A.8.2).

---

## 0. Base factuelle recalibree sur le papier de reference

### 0.1 La reference

**La reference `https://arxiv.org/html/2603.28066v1` donnee dans `CONTEXTE.md` ne correspond pas au
papier attendu.** [CONFIRME] Le papier est `arXiv:2411.10109`, initialement *Generative Agent
Simulations of 1,000 People*, retitre en **version 3 du 28 juin 2026** en *LLM Agents Grounded in
Self-Reports Enable General-Purpose Simulation of Individuals* (Park, Zou, Kamphorst, Egan, Shaw,
Hill, Cai, Morris, Liang, Willer, Bernstein). J'ai telecharge et lu integralement ce PDF (86 pages)
depuis `https://arxiv.org/pdf/2411.10109`. Tous les chiffres ci dessous en proviennent.

### 0.2 Les chiffres a utiliser

**Le chiffre de 85 pour cent cite dans `CONTEXTE.md` est perime.** La version courante donne :

| Condition | Fidelite normalisee GSS |
|---|---|
| Entretien seul | **0,83** |
| **Sondage seul** | **0,82** |
| Sondage + entretien | **0,86** |
| Demographique seul | **0,74** |
| Persona (paragraphe autodescriptif) | **0,71** `[VERIFIE PAR COORDINATION]` |

Denominateur et numerateur explicites : **precision brute 65,67 pour cent**, **consistance test
retest humaine 79,53 pour cent** `[VERIFIE PAR COORDINATION]`, ce qui donne bien 0,826.
(La version PDF que j'ai lue rapporte, pour une variante voisine, 0,83 avec ecart type 0,11 a
partir d'une precision brute de 65,67 (ecart type 6,51) et d'une auto consistance de 79,53
(ecart type 8,65). Les deux sources concordent.)

### 0.3 Le reste du protocole de Stanford

| Element | Valeur | Source |
|---|---|---|
| Echantillon | 1 052 adultes americains stratifies | [CONFIRME] PDF |
| Entretien | ~2 h, voix a voix, **agent IA** (TTS OpenAI Audio, Whisper, GPT-4o pour la relance), script American Voices Project abrege | [CONFIRME] |
| Transcripts | 6 491 mots en moyenne (ecart type 2 541) ; 99 questions scriptees, 81,7 relances en moyenne | [CONFIRME] |
| Batteries | GSS core (177 items categoriels + 6 numeriques), BFI-44, 5 jeux economiques, 5 replications d'experiences | [CONFIRME] |
| Test retest | toute la cohorte, meme batterie **deux semaines** plus tard, hors entretien | [CONFIRME] |
| Items d'evaluation GSS | 150 apres retrait de 27 items redondants avec l'entretien ; 3,31 modalites en moyenne ; hasard = 0,30 | [CONFIRME] |
| Modele | GPT-4o pour tous les agents | [CONFIRME] |
| Architecture | memoire = self-report + « expert reflections » par 4 personas d'expert, selection de l'expert au moment de la prediction, puis chaine de pensee | [CONFIRME] |
| **Jeux economiques** | **aucune difference significative entre conditions, F = 1,63, p = 0,16** ; les auteurs les traitent comme « cas limite » | `[VERIFIE PAR COORDINATION]`, coherent avec le texte du PDF que j'ai lu |
| Fine tuning | GPT-4o fine tune sur 500 agents, evalue sur 552 : **0,79**, contre **0,84** avec le meme prompt sans fine tuning | [CONFIRME] |
| Ablation resume a puces | 0,81 | [CONFIRME] |
| **Mecanisme d'extraction** | une part de la performance des agents entretien vient de la **recuperation directe** de reponses deja donnees pendant l'entretien, confirmee par les auteurs via une analyse de retrait progressif | [CONFIRME] PDF, section mecanismes |
| Comparaison de modeles (50 agents, precision brute) | GPT-5 0,67, GPT-4.1 0,67, o1 0,67, o3 0,67, GPT-4o 0,66, o1-mini 0,62, GPT-4o-mini 0,60 | [CONFIRME] |
| DPD, ideologie politique, GSS | 13,75 % demographique, 8,60 % entretien, 6,22 % sondage, 7,09 % sondage+entretien | [CONFIRME] |
| Remuneration | 60 USD phase 1 + 30 USD phase 2 + bonus 0 a 10 USD | [CONFIRME] |
| Archive | `https://osf.io/t6g7k/` | [CONFIRME] cite dans le PDF |

### 0.4 L'archive OSF, et pourquoi elle change le protocole

`[VERIFIE PAR COORDINATION]`, verification faite sur place par un autre agent qui a telecharge les
fichiers : l'archive `https://osf.io/t6g7k/` contient **8 fichiers CSV, 1 052 lignes, 178 colonnes
par domaine**, avec les reponses individuelles reelles au GSS, au BFI et aux jeux economiques,
**pour la vague 1 et la vague 2**, plus **les reponses produites par les cinq conditions d'agents**,
plus le code d'analyse.

**Note d'honnetete** : le texte du PDF que j'ai lu ecrit, dans sa section sur le partage de
donnees, « we provide open access to **aggregated** responses to the fixed survey instruments ».
La description transmise par la coordination (1 052 lignes par fichier) decrit au contraire des
donnees ligne a ligne. Je n'ai pas pu ouvrir l'archive moi meme (la page OSF est rendue par
JavaScript et n'est pas lisible par simple recuperation HTTP). **La premiere action du protocole
est de lever cette ambiguite** : etape A1.

Quatre consequences, si la description de la coordination est exacte.

- **Le denominateur du score normalise est disponible directement.** La vague 2 sur les memes
  individus donne la fiabilite test retest humaine a deux semaines, individu par individu, sans
  aucune re interrogation a organiser. **Tout l'echafaudage de la version 1 de ce document
  (estimateur de Heise sur trois vagues d'un panel) devient un plan de repli, pas le plan
  principal.** C'est une simplification massive.
- **On peut mesurer notre contribution sans generer un seul token.** Les sorties des cinq
  conditions d'agents sont dans l'archive. L'IDP se calcule dessus. On produit donc un resultat
  quantitatif original sur les donnees du papier de reference, en quelques heures de calcul de
  tableur, a cout strictement nul. **C'est le meilleur rapport valeur sur cout de tout le projet.**
- **On dispose gratuitement des cinq conditions de controle de Stanford**, deja calculees. Nos
  propres conditions de controle deviennent des complements, pas des prerequis.
- **En revanche l'archive ne permet probablement pas une replication de bout en bout** : les
  transcripts d'entretien ne sont pas publics (les auteurs insistent sur leur difficulte a
  anonymiser). D'ou le second jeu de donnees.

### 0.5 Twin-2K-500

[CONFIRME] `https://huggingface.co/datasets/LLM-Digital-Twin/Twin-2K-500`, papier
`arXiv:2505.17479`, *Twin-2K-500: A dataset for building digital twins of over 2,000 people based
on their answers to over 500 questions*.

- N = 2 058, echantillon representatif americain, en moyenne 2,42 h de passation par personne.
- **Quatre vagues.** Les trois premieres, lancees a une semaine d'intervalle, melangent
  demographie, echelles psychologiques, performance cognitive, preferences economiques et
  experiences de behavioral economics. **La vague 4, lancee deux semaines apres la vague 3, repete
  les experiences de biais et heuristiques et fournit ainsi une mesure de fiabilite test retest.**
- Public, avec son code.

**Nuance importante a ne pas perdre** : la vague 4 ne repete que les experiences de biais et
heuristiques, pas les 500 questions. La fiabilite test retest directe n'est donc disponible que
sur ce sous ensemble. Pour le reste des items, il faut soit l'estimateur de Heise sur les vagues 1
a 3 (qui sont espacees d'une semaine seulement, donc peu de changement reel : condition favorable),
soit la fiabilite d'item publiee. C'est un point a verifier des l'etape A2.

---

## 1. Choix de la premiere dimension

### 1.1 Les trois candidats

- **D1, opinions politiques et sociales.** Positionnement partisan, ideologie, confiance
  institutionnelle, positions sur avortement, armes, immigration, depenses publiques, tolerance.
- **D2, comportement d'achat.** Choix de marque, panier, sensibilite au prix, fidelite, reponse
  aux promotions.
- **D3, comportements et attitudes de sante.** Tabac, alcool, activite physique, observance,
  recours aux soins, attitude vaccinale.

### 1.2 Notation critere par critere

Echelle 1 (tres defavorable) a 5 (tres favorable).

| Critere | D1 politique | D2 achat | D3 sante |
|---|---|---|---|
| Disponibilite de donnees individuelles publiques | **5** | 2 | 4 |
| Facilite d'evaluation objective | **5** | 4 | 4 |
| Fidelite documentee des LLM sur ce domaine | **5** | **1** | 2 |
| Monetisabilite | 3 | **5** | 4 |
| Sensibilite des donnees | 3 | **4** | 1 |
| Risque de contamination du corpus d'entrainement | 2 | **4** | 3 |
| Risque reputationnel | 2 | **4** | 2 |
| **Total brut** | **25** | 24 | 20 |

**Le changement par rapport a la version 1 de ce document porte sur une seule case, et il est
decisif.** J'avais note D2 a 2 sur « fidelite documentee ». Je la descends a **1** : ce n'est plus
« pas de resultat connu », c'est **« le resultat connu est negatif »**. Sur les jeux economiques
incites de Stanford, qui sont le proxy le plus proche du choix de consommation dans la batterie,
l'ANOVA entre conditions d'agents donne **F = 1,63, p = 0,16**. Aucune condition, y compris le
persona complet construit sur deux heures d'entretien, ne bat la condition demographique. Les
auteurs eux memes ecrivent qu'ils traitent les jeux comme « un cas limite plutot qu'un domaine ou
les self-reports aident clairement ».

**Justifications des autres cases**, inchangees pour l'essentiel.

**Disponibilite.** D1 = 5 : GSS gratuit `https://gss.norc.org` [CONFIRME], ANES avec fichiers
panel fusionnes en acces libre [CONFIRME], LISS gratuit apres engagement d'usage non commercial
[CONFIRME], Pew ATP apres compte gratuit [CONFIRME], et maintenant l'archive OSF de Stanford et
Twin-2K-500. D2 = 2 : les donnees d'achat vraiment ouvertes sont des transactions **sans personne
derriere**, c'est a dire sans profil sociodemographique riche. dunnhumby *The Complete Journey*
(2 500 menages, deux ans, demographie **partielle**) reste le meilleur candidat public [CONFIRME
qu'il existe ; licence et couverture demographique **non verifiees**]. D3 = 4.

**Evaluation objective.** D1 = 5 : modalite dans une liste finie, accuracy sans ambiguite, hasard
calculable. **Et surtout, avec la lecture de logprobs (section A.8), une distribution complete par
persona.** D2 = 4 : support enorme et non ordonne, il faut passer au ranking, plus comparable a
Stanford. D3 = 4.

**Monetisabilite.** D2 = 5, D3 = 4, D1 = 3.

**Sensibilite.** D3 = 1 (donnees de sante, categorie particuliere RGPD). D1 = 3 (l'opinion
politique est aussi une categorie particuliere au sens de l'article 9 du RGPD [PROBABLE, non
verifie dans le texte], mais les archives publiques sont deja diffusees comme anonymisees). D2 = 4.

**Contamination.** D1 = 2 (le GSS est massivement decrit et tabule depuis cinquante ans), D2 = 4,
D3 = 3. Traite en A.3.

**Reputation.** D1 = 2 (« des IA qui simulent des electeurs » est le pire titre de presse
possible), D2 = 4, D3 = 2.

### 1.3 Recommandation, tranchee

**On commence par D1, les opinions politiques et sociales. Le comportement d'achat devient
l'extension numero 1, pas l'ouverture. Cette recommandation est renforcee, pas affaiblie, par les
elements nouveaux.**

Trois arguments, dans l'ordre de force.

1. **Le seul resultat connu sur le domaine le plus proche du comportement d'achat est un resultat
   nul.** F = 1,63, p = 0,16. Ouvrir sur D2 revient a parier que Stanford s'est trompe sur le seul
   point ou ils rapportent un echec. Ce n'est pas un pari raisonnable a ce stade, et il n'y a
   aucune urgence : l'etape A12 rejoue le protocole complet sur un jeu d'achat une fois la methode
   validee, ce qui produit la preuve de transferabilite dont le commercial a besoin.

2. **A budget zero et sans humains, ce qui domine est la disponibilite de donnees individuelles
   publiques appariees a un profil riche et a une vague de retest.** D1 offre desormais trois
   sources qui remplissent les trois conditions (archive Stanford, Twin-2K-500, panels GSS/ANES).
   D2 n'en offre aucune.

3. **Sans point de comparaison, le premier resultat ne vaut rien.** Sur D1 on a 0,83 / 0,82 / 0,86
   / 0,74 / 0,71 comme reperes, produits par l'equipe avec laquelle on veut publier, et desormais
   les fichiers bruts qui les ont produits. Sur D2 on n'aurait rien.

**Ce que cela coute et comment on le compense.** On repousse la monetisabilite. C'est coherent avec
la position officielle du projet. La compensation est explicite dans le plan (etape A12).

**Une remarque de cadrage sur le risque reputationnel de D1.** On ne simule pas des electeurs pour
prevoir une election. On mesure la capacite d'un modele a **preserver la diversite d'opinion** d'une
population, et on documente les cas ou il echoue. C'est litteralement le contraire du titre
hostile, et c'est la contribution scientifique visee.

---

# VOIE A, PRIORITAIRE : REPRODUCTION SANS HUMAINS ET SANS ARGENT

## A.0. Principe

On ne collecte pas, on mesure. La « personne » est un repondant reel d'une enquete publique dont
on connait la totalite des reponses individuelles et le profil. On coupe ses donnees en deux : une
partie construit le persona, l'autre est tenue secrete et sert de verite terrain.

Notations utilisees dans tout le document :
- `X_i` : bloc d'entree donne au modele.
- `Y_i` : bloc d'evaluation, tenu secret.
- `q_{i,j}` : **distribution de probabilite** produite par le persona `i` sur les modalites de
  l'item `j`, lue dans les logprobs (section A.8).
- `rho_i` : fiabilite test retest de l'individu `i`, desormais **mesuree** et non estimee.

**Trois etages de travail, du moins cher au plus cher, et il faut les faire dans cet ordre.**

| Etage | Ce qu'on fait | Cout en calcul | Ce que ca produit |
|---|---|---|---|
| **E1, reanalyse** | on recalcule nos metriques sur les sorties d'agents deja publiees par Stanford | **nul** | notre contribution sur la variance, sur les donnees du papier de reference |
| **E2, replication** | on reconstruit des personas et on les evalue nous memes sur Twin-2K-500 | ~1 h de calcul local | la preuve qu'on sait faire, et le controle des methodes d'injection |
| **E3, generalisation** | on rejoue sur GSS/ANES/LISS, puis sur un jeu d'achat | quelques heures | la transferabilite |

## A.1. Jeux de donnees

### A.1.1 Substrat de reanalyse : l'archive OSF de Stanford

**`https://osf.io/t6g7k/`**. Role : etage E1. C'est le seul endroit ou l'on dispose simultanement
des reponses humaines des deux vagues **et** des sorties de cinq conditions d'agents deja
calculees. C'est donc le seul endroit ou l'on peut mesurer la preservation de la variance **sur
les agents exacts du papier de reference**, ce qui rend la comparaison incontestable.

*Verification prealable obligatoire (etape A1)* : confirmer que les fichiers sont bien au niveau
individuel et non agreges, et que les reponses d'agents sont appariables aux individus. Le texte du
papier dit « aggregated », la verification de terrain dit 1 052 lignes. **Tant que ce point n'est
pas tranche, l'etage E1 est suspendu.**

### A.1.2 Substrat de replication : Twin-2K-500

**`https://huggingface.co/datasets/LLM-Digital-Twin/Twin-2K-500`**, papier `arXiv:2505.17479`.
Role : etage E2, replication de bout en bout.

Pourquoi lui plutot que le GSS pour l'etage E2 :
- **500 questions par personne**, ce qui autorise un decoupage entree/evaluation genereux des deux
  cotes (par exemple 350 en entree, 150 en evaluation) sans jamais manquer d'items.
- **2 058 personnes**, soit vingt fois ce dont on a besoin pour la phase 1.
- **Une vague 4 de retest a deux semaines**, donc un denominateur mesure sur au moins un sous
  ensemble d'items.
- **Public, immediat, avec code.** Aucune inscription, aucun delai.
- **Faible contamination probable** : jeu recent, diffuse sous forme de fichiers de donnees.

Limites a documenter : la vague 4 ne repete que les experiences de biais et heuristiques ; le
contenu est plus psychologique et economique que politique, ce qui est un ecart avec le GSS.

### A.1.3 Substrats de generalisation

| Jeu | Vagues appariees | Acces | Role | Confiance |
|---|---|---|---|---|
| GSS, panels roulants 2006-2008-2010, 2008-2010-2012, 2010-2012-2014 | 3 vagues, ~1 300 individus complets par panel | libre | generalisation politique, et **seul cas ou l'estimateur de Heise est necessaire** | [CONFIRME] design et effectifs, codebook panel NORC et Morgan & Lee 2024 |
| ANES, panel fusionne 2016-2020-2024 | 3 points | libre | generalisation politique specialisee | [CONFIRME] |
| Pew ATP + OpinionQA | panel ; OpinionQA en coupe | compte gratuit ; `tatsu-lab/opinions_qa` | 500 questions clivantes, 9 traits demographiques par repondant | [CONFIRME] structure |
| LISS | panel annuel depuis 2007 | gratuit apres engagement non commercial | generalisation culturelle, faible contamination | [CONFIRME] |
| ESS, WVS | coupes repetees, **pas d'individus apparies** | gratuit | **uniquement** distributions de reference. Ne permet pas de fidelite individuelle | [PROBABLE] |
| Understanding Society, UAS, SHARE | panels | inscription academique | reserve, delais d'acces | [PROBABLE], non verifie |
| dunnhumby *The Complete Journey* | 2 500 menages, 2 ans | Kaggle / Mendeley | etape A12, extension achat | [CONFIRME] existence ; licence **non verifiee** |

**Regle d'exclusion** : un jeu en coupes repetees ne permet pas de mesurer la fidelite
individuelle. Il ne sert qu'aux distributions de reference.

## A.2. Decoupage entree / evaluation et prevention des fuites

### A.2.1 Le decoupage

Trois niveaux de severite, a executer dans cet ordre.

- **L0, item retire.** Entree = tout sauf l'item cible. Le plus permissif. Stanford obtient 0,82 a
  0,85 dans cette configuration.
- **L1, module retire.** Entree = tout sauf le module thematique de l'item cible. Stanford mesure
  une chute a **0,77**. C'est le reglage honnete.
- **L2, blocs disjoints.** Partition thematique `A` / `B` figee a l'avance. Entree = tout `A`,
  evaluation = tout `B`. **Reglage principal recommande.**

Partition proposee, a figer avant tout run (formulee pour le GSS ; a transposer pour Twin-2K-500) :

- **A (entree)** : demographie, famille et menage, education, emploi et profession, revenu,
  religion et pratique, mobilite, sante subjective, satisfaction de vie et de travail, sociabilite
  et confiance interpersonnelle, usage des medias.
- **B (evaluation)** : positions politiques et partisanes, confiance institutionnelle, avortement,
  armes, peine de mort, immigration, roles de genre, race et discrimination, depenses publiques,
  tolerance, morale sexuelle.

`A` est ce qu'une entreprise a dans son CRM. `B` est ce qu'elle veut savoir. **Ce decoupage n'est
pas seulement methodologique, c'est le produit.**

### A.2.2 Les six mecanismes de fuite et leur parade

1. **Fuite triviale.** L'item cible est dans l'entree. Parade : retrait automatique + assertion
   dans le code (l'identifiant de l'item cible n'apparait dans aucune chaine du prompt).
2. **Fuite par item synonyme.** Parade : detection automatique des paires quasi synonymes par
   modele juge, puis revue manuelle exhaustive des paires signalees. Stanford a applique cette
   procedure (classifieur GPT-4.1 puis revue humaine, 27 items GSS retires pour redondance avec
   l'entretien) et **n'a trouve aucun couple synonyme a l'interieur du GSS lui meme** [CONFIRME].
3. **Fuite par inference forte.** Un item de `A` rend un item de `B` quasi deductible. **Ce n'est
   pas une fuite a supprimer, c'est le signal qu'on veut mesurer**, mais il faut le quantifier.
   Parade : reproduire l'analyse de mecanisme de Stanford (classification de chaque paire en
   « recuperable », « inferable », « ni l'un ni l'autre », puis recalcul de la fidelite en retirant
   progressivement les items les plus inferables). Critere de succes : **l'ecart avec les
   conditions de controle doit survivre au retrait**. Chez Stanford, apres retrait de 80 questions,
   les agents entretien tiennent a 0,79 contre 0,71 pour les agents demographiques [CONFIRME].
4. **Fuite par la structure de reponse.** Un style de reponse (acquiescement, preference pour
   l'extreme) peut fuiter par l'ordre des modalites. Parade : randomiser l'ordre des modalites,
   avec la graine enregistree dans les metadonnees. **En mode logprobs, cette parade est
   particulierement importante**, parce que la position d'un token dans la liste influence sa
   probabilite ; il faut donc mesurer et corriger le biais de position (section A.8.5).
5. **Fuite par la vague.** Parade : **toujours evaluer sur une vague posterieure a celle de
   l'entree.**
6. **Fuite par extraction plutot que simulation.** **Nouveau, et impose par la coordination.**
   Les auteurs confirment qu'une part de la performance de la condition entretien vient de la
   recuperation d'une reponse deja donnee pendant l'entretien, pas d'une simulation. En voie A,
   le probleme se transpose et s'aggrave : les items d'entree sont des items de sondage, donc
   formates exactement comme les items d'evaluation. **Sans controle dedie, on mesurerait de la
   memoire de contexte, pas de la prediction.** Parade : la condition **C7** de la section A.4.

### A.2.3 Critere de succes de l'etape

- Zero item cible present dans un prompt d'entree, sur 100 pour cent des prompts (test automatique).
- Paires signalees revues a 100 pour cent, decisions tracees et committees.
- Courbe de fidelite en fonction du nombre d'items inferables retires, produite pour chaque
  condition.
- Biais de position mesure et inferieur a un seuil fixe a l'avance (A.8.5).

## A.3. Contamination du corpus d'entrainement

Trois niveaux, aux consequences differentes.

- **Niveau 1, l'instrument.** Le modele connait les questions. **Certain et sans importance.**
- **Niveau 2, les marginales.** Le modele connait les distributions agregees. **Tres probable.**
  Consequence : cela **gonfle les conditions de controle** (mode de la population, tirage dans la
  marginale, persona demographique), donc cela rend notre test **plus severe**. Argument a
  retourner explicitement dans le papier.
- **Niveau 3, les lignes individuelles.** Le modele a memorise la ligne du repondant `#4471`.
  **Seul niveau qui invaliderait le resultat.** [HYPOTHESE] peu probable pour des microdonnees
  distribuees en fichiers tabulaires compresses, sans texte narratif associant un identifiant a
  des reponses. Mais peu probable n'est pas verifie.

**Note specifique a l'archive OSF** : les sorties d'agents de Stanford sont publiques depuis 2024.
Elles peuvent donc etre dans les corpus d'entrainement des modeles recents. Cela n'affecte pas
l'etage E1 (on ne demande rien a un modele, on recalcule des metriques sur des fichiers), mais cela
affecte toute tentative de refaire tourner un modele sur ces memes individus. **A l'etage E2, on
travaille sur Twin-2K-500, plus recent, ce qui limite le risque.**

### A.3.1 Protocole de test, executable

- **T1, restitution directe.** Demander au modele, sans contexte, les reponses de l'individu
  `id = 4471`. **Critere : precision au niveau du hasard.** Sinon, memorisation de niveau 3, jeu
  disqualifie.
- **T2, identifiant faux.** Meme chose avec un identifiant inexistant. Controle de confabulation.
- **T3, profil sans reponses.** C'est la condition C2. Si C2 est deja tres proche de la condition
  complete, soit le domaine est trivialement predictible, soit il y a contamination.
- **T4, decalage temporel.** Rejouer sur une vague posterieure a la date de coupure du modele.
  **Critere : la fidelite normalisee ne chute pas de plus de 0,03.** Methode standard quand on n'a
  pas acces au corpus d'entrainement (*Data Contamination Through the Lens of Time*,
  `https://arxiv.org/pdf/2310.10628`) [CONFIRME].
- **Parade structurelle.** Replication sur LISS (hors Etats Unis, faible contamination). Si le
  resultat tient sur les deux, la contamination cesse d'etre une explication plausible.

### A.3.2 Critere de succes

- T1 non significativement superieur au hasard (test binomial, alpha 0,05).
- T4 : ecart inferieur a 0,03.
- Resultats consignes, y compris mauvais.

## A.4. Conditions de controle

**Un chiffre de fidelite sans condition de controle ne veut strictement rien dire.** C'est le point
sur lequel ce document insiste le plus, et deux resultats de juillet 2026 le confirment
brutalement.

### A.4.1 Ce que la litterature recente impose

- **Chen, Zhu, Zheng, *When Synthetic Users Fail: A Cross-Domain Benchmark of LLM-Simulated Human
  Survey Responses*, arXiv:2607.26348, depose le 28 juillet 2026.** [CONFIRME par recuperation de
  la notice] Quatre modeles testes sur deux domaines de donnees humaines reelles (General Social
  Survey et World Values Survey) contre des baselines statistiques. Deux echecs constants :
  **au niveau individuel, aucun LLM ne bat meme la meilleure baseline** ; et les modeles
  **sur determinent systematiquement les demographies**, traitant l'identite comme bien plus
  predictive des attitudes qu'elle ne l'est chez les vraies personnes. Les echecs persistent quelle
  que soit la taille du modele.
- **Lukauskas, Sarkauskaite, *Plausible but Not Valid: A Psychometric Audit of LLMs as Synthetic
  Survey Respondents*, arXiv:2608.14606, depose le 6 juillet 2026.** [CONFIRME par recuperation de
  la notice] 37 modeles, jeu lituanien de psychologie organisationnelle, 68 items, 12 sous echelles.
  Les substitutions contrefactuelles revelent des effets pilotes par l'education (|d| moyen = 0,56)
  qui ecrasent le genre (0,12) et le role (0,18), soit des rapports d'environ 4,7 et 3,1.
  **Note d'honnetete** : la coordination m'a transmis ce papier comme montrant un gonflement des
  ecarts inter segments d'un facteur 2 a 4. Ce que j'ai pu verifier moi meme est le rapport entre
  effets demographiques a l'interieur du modele, pas le rapport modele sur humain. Le message
  operationnel (les modeles ne traitent pas les segments demographiques comme les humains) est
  robuste ; le facteur exact ne l'est pas dans ma verification.

**Consequence de protocole, non negociable : les baselines non LLM deviennent obligatoires.**
Publier une fidelite de LLM sans montrer qu'elle bat une regression logistique, apres juillet 2026,
serait immediatement rejete.

### A.4.2 Les huit conditions, sur exactement les memes individus et items

| Code | Condition | Contenu | Ce qu'elle teste | Cout LLM |
|---|---|---|---|---|
| **C0** | Hasard uniforme | tirage uniforme sur les modalites | plancher absolu, analytique | nul |
| **C1** | Mode de la population | pour chaque item, la modalite la plus frequente, identique pour tous | plancher « tout sur la population, rien sur la personne ». Par construction **IDP = 0** | nul |
| **C1b** | **Tirage dans la marginale observee** | pour chaque item, tirage dans la distribution empirique observee, independamment par individu | **impose par la coordination.** Baseline a **variance parfaite et fidelite individuelle nulle**. C'est l'antipode exact de C1 sur le plan (fidelite, IDP), et le repere qui rend ce plan lisible | nul |
| **C2** | Persona demographique | age, genre, race, region, education, ideologie declaree | la baseline dominante de la litterature (0,74 chez Stanford) | oui |
| **C3** | **Persona aleatoire (placebo)** | on donne le bloc `A` d'un **autre** individu tire au hasard, on evalue sur le `B` de l'individu cible | **le controle le plus important et le plus souvent oublie.** Si C3 est proche de CT, le modele ne personnalise pas, il produit un citoyen generique | oui |
| **C4** | Regression logistique sur demographies | multinomiale ou ordinale, item par item, predicteurs = variables demographiques du bloc `A` | « votre LLM bat il une regression logistique de 1970 ? » | nul |
| **C5** | Regression logistique enrichie | idem + reponses du bloc `A` reduites par ACP ou selection L1 | **la baseline serieuse.** Un LLM qui ne bat pas C5 n'a qu'un interet de generalite, pas de prediction | nul |
| **C7** | **Controle d'extraction** | on retire du bloc `A` tous les items classes « recuperables » ou « inferables » vis a vis de l'item cible, et on remesure | **impose par la coordination.** Isole la simulation de la memoire de contexte | oui |
| **CT** | Traitement | persona complet, bloc `A` + reflections d'expert | ce qu'on evalue | oui |

Note : C4, C5, C1b sont des baselines **entrainees ou calibrees sur des individus disjoints** de
ceux evalues (validation croisee **par individu**, jamais par ligne).

### A.4.3 Ce que les controles permettent d'annoncer

Quatre quantites, toutes indispensables, aucune suffisante seule :

- `CT - C2` : le gain sur le controle demographique. C'est le chiffre de Stanford (0,83 - 0,74).
- `CT - C3` : le gain sur le placebo. C'est le chiffre qui **prouve la personnalisation**.
- `CT - C5` : le gain sur la statistique. C'est le chiffre qui **prouve l'utilite**, et celui que
  la litterature de juillet 2026 dit negatif. **S'il est negatif chez nous aussi, c'est un
  resultat, pas un echec** : il faut alors reformuler la contribution autour de la generalite
  (un persona repond a n'importe quelle question, une regression logistique doit etre reentrainee
  par question) et autour de la variance.
- `CT - C7` : la part de la performance qui n'est **pas** de l'extraction.

Sur l'axe variance : `IDP(CT)` compare a `IDP = 1` pour la population observee, `IDP(C1) = 0`, et
`IDP(C1b)` proche de 1 avec une fidelite nulle.

### A.4.4 Critere de succes

- Les huit conditions tournent sur exactement les memes couples `(individu, item)`.
- **`CT > C3` avec p < 0,05.** Si ce test echoue, le projet s'arrete et on reflechit : cela
  signifie que le modele ne personnalise pas du tout.
- `CT > C2` avec p < 0,05.
- `CT` compare a `C5` : quel que soit le signe, connu **avant** d'ecrire quoi que ce soit.
- `CT - C7` estime et publie.

## A.5. Feature engineering

### A.5.1 Ce que la litterature etablit

- **L'identification partisane est le predicteur dominant du vote et d'une large part des positions
  politiques.** [CONFIRME] Bartels, *Partisanship and Voting Behavior, 1952-1996*, American Journal
  of Political Science 44(1), 2000, pp. 35-50,
  `https://www.acsu.buffalo.edu/~jcampbel/documents/BartelsAJPS2000.pdf`. Filiation theorique :
  Campbell et al., *The American Voter*, 1960.
- **Le comportement passe est le meilleur predicteur du comportement futur.** [CONFIRME]
  Ouellette & Wood, *Habit and Intention in Everyday Life*, Psychological Bulletin 124(1), 1998,
  pp. 54-74,
  `https://dornsife.usc.edu/wendy-wood/wp-content/uploads/sites/183/2023/10/Ouellette.Wood_.1998_Habit_and_intention_in_everyday_life.pdf`.
  Traduction : **les reponses passees de la personne sur des items voisins battent n'importe quel
  attribut de profil.** C'est exactement ce que montre le 0,82 des agents sondage contre 0,74 des
  agents demographiques.
- **La demographie seule fonctionne mal comme ancrage attitudinal.** [CONFIRME] Boelaert, Coavoux,
  Ollion, Petev, Prag, *Machine Bias. How Do Generative Language Models Answer Opinion Polls?*,
  Sociological Methods & Research, 2025,
  `https://journals.sagepub.com/doi/10.1177/00491241251330582`. Biais fort et variance faible sur
  chaque sujet, biais variant aleatoirement d'un sujet a l'autre ; conditionner sur cinq variables
  sociodemographiques ne differencie pas les sous groupes ; les caracteristiques demographiques
  fonctionnent comme des **etiquettes d'identite** et non comme des **ancrages attitudinaux**.
- **Et pourtant les modeles sur ponderent ces memes demographies.** Chen et al. 2026, cite en A.4.1.
  Les deux resultats ne se contredisent pas : le modele donne trop de poids a la demographie **et**
  s'en sert mal.

### A.5.2 Hierarchie predictif / decoratif, pour D1

**Niveau 1, predictif fort. A inclure toujours.**

| Feature | Justification |
|---|---|
| Reponses passees de l'individu sur des items du meme domaine | Ouellette & Wood ; effet mesure par Stanford (0,82 contre 0,74) |
| Identification partisane et auto placement ideologique | Bartels |
| Pratique religieuse (frequence, pas seulement affiliation) | [PROBABLE] la frequence structure les positions morales plus que l'affiliation ; pas de source primaire chiffree verifiee |
| Niveau d'education atteint | [PROBABLE] predicteur robuste de la tolerance et du liberalisme culturel. **Attention** : c'est aussi la variable que Lukauskas et al. identifient comme la plus amplifiee par les modeles |
| Confiance interpersonnelle et institutionnelle | items fortement correles entre eux |

**Niveau 2, predictif modere. A inclure.** Profession, secteur, statut d'emploi, syndicalisation ;
revenu du menage et **perception subjective** du revenu (souvent plus predictive que le montant
[HYPOTHESE]) ; race et origine (fortement associe au vote aux Etats Unis, mais aussi source de
biais : le DPD par race est mesure chez Stanford) ; region et urbanicite ; composition du menage ;
sources d'information. Tous [PROBABLE].

**Niveau 3, decoratif. A exclure du persona, sauf comme variable de controle.**

| Feature | Pourquoi |
|---|---|
| Age exact plutot que cohorte | l'annee precise n'apporte rien au dela de la generation |
| Prenom, ville precise, details biographiques uniques | aucun pouvoir predictif ; augmentent le risque de reidentification et de stereotypage |
| Traits Big Five | Stanford les **predit** mais ne montre pas qu'ils ameliorent la prediction politique. [HYPOTHESE] a tester comme feature additive |
| Style d'ecriture | Stanford : resume a puces 0,81 contre transcript brut 0,83. Le style vaut deux points, et il est sans objet en voie A |
| **Reponses aux jeux economiques** | **aucun type d'agent ne bat la baseline demographique (F = 1,63, p = 0,16).** Ne pas en faire une feature |

### A.5.3 Les reflections d'expert

Stanford genere, une fois par individu, quatre jeux de reflections par personas d'expert
(psychologue, economiste comportemental, politiste, demographe), puis selectionne le jeu pertinent
au moment de la prediction [CONFIRME]. En voie A, reproductible a l'identique et a cout marginal
quasi nul (une generation par individu, reutilisee sur toutes les questions). **A inclure comme
condition experimentale separee** (`CT` avec reflections contre sans), parce que c'est une des
rares parties de l'architecture ablatables proprement et que Stanford ne l'a pas ablatee isolement.

### A.5.4 Critere de succes

- Liste figee des features de niveau 1 et 2, mappee item par item.
- Ablation du niveau 2 entier : perte attendue inferieure a 0,03. **Si la perte est nulle, le
  niveau 2 est decoratif** et le persona peut etre drastiquement compresse.

## A.6. Schema de donnees

Format : **YAML** pour l'individu, **JSONL** pour les runs.

```yaml
# popsim / schema personne v0.2
# Un fichier par individu. Nom du fichier : {pseudo_id}.yaml

pseudo_id: PS-TWIN2K-001842
source:
  dataset: Twin-2K-500
  url: "https://huggingface.co/datasets/LLM-Digital-Twin/Twin-2K-500"
  original_id_hash: "sha256:9f2c...a1"      # hash sale, non reversible
  waves_available: [1, 2, 3, 4]
  input_wave: 1
  eval_wave: 3
  retest_pair: [3, 4]                        # la paire qui donne la fiabilite mesuree
  license: "public, Hugging Face"
  retrieved_at: "2026-09-10"

# --- attributs : le bloc A ---
attributes:
  demographics:
    birth_cohort: "1971-1975"                # cohorte, pas age exact (cf. A.5.2)
    gender: female
    race: white
    census_region: "east_north_central"
    urbanicity: suburb
    education_degree: bachelor
  household:
    marital_status: married
    children: 2
    household_income_bracket: "50000-59999"
    income_subjective: average
  work:
    employment_status: employed_full_time
    occupation_major: "technicians and associate professionals"
    industry: healthcare
    union_member: false
  religion:
    affiliation: catholic
    attendance: "several times a year"
  political_anchor:
    party_id_7pt: 3                          # 0 = strong dem ... 6 = strong rep
    ideology_7pt: 4
  media:
    news_frequency: "once a week"

# --- reponses sources : le bloc A en items bruts ---
source_responses:
  wave: 1
  block: A
  items:
    - item_id: HAPPY
      text: "Taken all together, how would you say things are these days?"
      options: ["very happy", "pretty happy", "not too happy"]
      answer_index: 1
    - item_id: TRUST
      text: "Generally speaking, would you say that most people can be trusted?"
      options: ["can trust", "cannot trust", "depends"]
      answer_index: 1
    # ... ~350 items du bloc A

# --- memoire structuree : derivee, jamais saisie a la main ---
memory:
  generated_by: "qwen3-30b-a3b-instruct-q4"
  generated_at: "2026-09-12T10:04:00Z"
  prompt_version: "reflect-v0.3"
  expert_reflections:
    demographer:
      - "Menage de quatre personnes, deux revenus probables, classe moyenne du Midwest."
    psychologist:
      - "Faible confiance interpersonnelle malgre un environnement stable."
    political_scientist:
      - "Positionnement partisan et ideologique exactement median : faible ancrage."
    behavioral_economist:
      - "Revenu percu comme moyen malgre une tranche superieure a la mediane nationale."
  condensed_profile: >
    Femme, cohorte du debut des annees 1970, mariee, deux enfants, banlieue du Midwest,
    diplomee du superieur, technicienne dans la sante, catholique pratiquante occasionnelle,
    revenu du menage moyen percu comme moyen, positionnement partisan et ideologique median,
    faible confiance interpersonnelle.
  condensed_profile_tokens: 71

# --- questions d'evaluation : tenues secretes ---
evaluation:
  wave: 3
  block: B
  leakage_check:
    method: "llm-judge + revue manuelle"
    judge_model: "qwen3-30b-a3b-instruct-q4"
    flagged_pairs: 3
    removed_items: ["ABANY"]
    reviewed_by: amir
  extraction_control:                        # cf. condition C7
    retrievable_from_A: ["POLVIEWS"]
    inferable_from_A: ["PARTYID", "CONFED"]
  items:
    - item_id: POLVIEWS
      text: "Where would you place yourself on this liberal-conservative scale?"
      options: ["extremely liberal", "liberal", "slightly liberal", "moderate",
                "slightly conservative", "conservative", "extremely conservative"]
      option_scores: [1, 2, 3, 4, 5, 6, 7]   # score numerique pour les items ordinaux
      permutation_seed: 1842                  # ordre randomise, cf. biais de position
      reference_answer_index: 3               # verite terrain, vague 3
      retest_answer_index: 4                  # vague 4, sert au calcul de fiabilite
    # ... ~150 items du bloc B

# --- reponses produites : une entree par condition et par run ---
predictions:
  - run_id: "run-2026-09-20-a"
    condition: CT                             # C0 C1 C1b C2 C3 C4 C5 C7 CT
    injection: rag_k10                        # cf. A.7
    mode: logprobs                            # logprobs | generation
    model: "qwen3-30b-a3b-instruct-q4"
    answers:
      POLVIEWS:
        # la distribution complete, dans l'ordre canonique des modalites
        probs: [0.02, 0.06, 0.14, 0.41, 0.26, 0.09, 0.02]
        argmax_index: 3
        p_reference: 0.41                     # probabilite attribuee a la bonne reponse
        expected_score: 4.19                  # sum_k p_k * score_k
        within_variance: 1.31                 # sum_k p_k (score_k - expected)^2
        correct_argmax: true
      CONFED:
        probs: [0.11, 0.68, 0.21]
        argmax_index: 1
        p_reference: 0.68
        expected_score: 2.10
        within_variance: 0.33
        correct_argmax: true
    summary:
      n_items: 50
      accuracy_argmax: 0.640
      accuracy_expected: 0.612                # mean_j p_reference,j ; metrique principale
      reliability_measured: 0.795             # test retest mesure, vagues 3 et 4
      normalized_accuracy: 0.770

# --- metadonnees de run ---
run_metadata:
  - run_id: "run-2026-09-20-a"
    started_at: "2026-09-20T09:12:00Z"
    duration_seconds: 412
    model_id: "qwen3-30b-a3b-instruct-q4"
    backend: "llama.cpp, Apple M5, 32 GiB"
    prefix_cache_reused: true
    batch_size: 32
    temperature_for_logprobs: 1.0             # distribution native, cf. A.8.3
    prompt_version: "predict-v0.5"
    context_tokens_prefix: 1180
    context_tokens_incremental_mean: 58
    total_forward_passes: 5000
    position_bias_measured: 0.011             # cf. A.8.5
    leakage_assertions_passed: true
    contamination_tests: ["T1:pass", "T2:pass", "T4:not_run"]
    git_commit: "a2f5376"
```

### A.6.1 Quatre regles non negociables

1. **`reference_answer_index` et `retest_answer_index` ne transitent jamais par un prompt.** Deux
   fonctions de chargement distinctes, `load_persona()` et `load_ground_truth()`, et une assertion
   qui echoue si la seconde est appelee depuis le module de generation.
2. **Aucun identifiant source en clair.** `pseudo_id` stable, `original_id_hash` sale. Cela permet
   de publier les fichiers persona sans republier les microdonnees.
3. **Tout champ derive porte le modele, la version de prompt et l'horodatage.** Sans cela, aucun
   run n'est reproductible.
4. **On stocke la distribution complete `probs`, pas seulement l'argmax.** C'est la matiere
   premiere de toute la section A.8. Un run qui n'a garde que l'argmax est a refaire.

### A.6.2 Critere de succes

- 100 fichiers individus valides contre un schema Pydantic ou JSON Schema.
- Test automatique : aucune valeur de reference presente dans aucun prompt genere.
- Un fichier exemple complet, avec un individu **fictif**, versionne dans le depot.

## A.7. Methode d'injection

Le critere donne par Simon structure l'ordre : **on ne passe au fine tuning que si le retrieval ne
donne pas la fidelite voulue.** Stanford donne une raison empirique de plus d'y aller en dernier.

### A.7.1 Les quatre options

| # | Methode | Contexte / requete | Mise en place | Cout marginal | Faisabilite budget zero | Limite |
|---|---|---|---|---|---|---|
| **M1** | Prompt systeme, profil condense | 300 a 900 tokens | nulle | tres bas | **excellente** | perte d'information : on jette les items, on garde un resume |
| **M2** | Contexte long, bloc `A` integral | 5 000 a 20 000 tokens selon le jeu | nulle | eleve, mais **fortement amorti par le cache de prefixe** | **bonne en local**, mediocre sur API gratuite | fenetre de contexte ; degradation de l'attention sur contexte long |
| **M3** | RAG sur les donnees de la personne | 800 a 1 500 tokens (k items les plus proches) | index vectoriel local, embeddings gratuits (`bge-small`, `e5-small`) | bas | **excellente** | risque de rater un item pertinent mais lexicalement eloigne ; hyperparametre `k` |
| **M4** | LoRA sur modele ouvert | 300 tokens | GPU. Sur M5 32 Gio, entrainement possible mais lent | tres bas | **mediocre** | un adaptateur par individu est absurde ; un adaptateur global apprend la population, pas la personne. **Stanford mesure 0,79 contre 0,84 sans fine tuning** |

**Remarque importante sur M2 en regime logprobs.** Le cache de prefixe change l'economie. Le bloc
`A` est identique pour les 50 questions d'un meme persona : il est encode **une fois**, puis chaque
question ne coute que ses ~58 tokens incrementaux et un passage avant. C'est une part du facteur
75 mesure par l'agent infrastructure. **M2 redevient donc competitif en local, alors qu'il etait
disqualifie dans la version 1 de ce document.**

### A.7.2 Ordre d'experimentation, avec criteres chiffres de passage

**Palier 0. Etalonner le plafond.** M2 sur un pilote reduit (N = 30, M = 30, conditions CT et C2),
sur le meilleur modele accessible. Cela donne `F_max`.
*Sortie* : `F_max` mesure et `F_max > F(C2)` avec p < 0,05. Sinon, arret et diagnostic.

**Palier 1. M1, profil condense.**
- **Si `F(M1) >= F_max - 0,02`** : on s'arrete. Le profil condense suffit. Plausible : Stanford
  montre que le resume a puces ne coute que deux points (0,81 contre 0,83).
- Sinon, palier 2.

**Palier 2. M3, RAG.** Pour `k` dans {5, 10, 20}.
- **Si `F(M3) >= F_max - 0,02`** : on s'arrete. Regime nominal attendu.
- Sinon, palier 3.

**Palier 3. M2, contexte integral.**
- **Si `F(M2) - F(M3) < 0,02`** : le contexte integral n'apporte rien, M3 devient la reference et
  on le dit.
- Sinon, M2 devient la reference.

**Palier 4. M4, LoRA. Declenche seulement si les trois conditions sont reunies :**
1. `F(M3) < F_max - 0,05`, le retrieval echoue nettement, **et**
2. `F(M2) < F(C5) + 0,02`, meme le contexte integral ne bat pas la regression enrichie, **et**
3. un GPU exploitable est disponible sur plusieurs heures.

Si ces trois conditions ne sont pas reunies, **on ne fait pas de fine tuning**, et on cite Stanford
(0,79 contre 0,84). Cette regle est a graver.

**Une exception a signaler.** Il existe une variante de M4 que Stanford n'a pas testee et qui
merite d'etre posee a Simon : un adaptateur entraine non pas a maximiser la precision, mais a
**preserver la variance** (fonction de perte penalisant l'ecart entre distribution simulee et
distribution observee, par exemple une divergence sur les marginales). C'est aligne avec la
contribution visee et cela ne tombe pas sous le verdict de Stanford, qui portait sur un fine tuning
oriente precision. Voir question ouverte 9.

### A.7.3 Critere de succes

- `F(M1)`, `F(M3)`, `F(M2)` et le cout en passages avant de chacune, tabules.
- Une decision tracee, avec le palier atteint et la raison de l'arret.
- Le rapport `F / cout` par methode, qui est le livrable operationnel pour le passage a l'echelle.

## A.8. Protocole d'evaluation

C'est la section la plus importante du document.

### A.8.0 Le mode d'evaluation par defaut : lire les probabilites, pas generer du texte

**Sur des questions fermees, on n'evalue jamais du texte genere. On lit la distribution de
probabilite du modele sur les modalites de reponse.** `[VERIFIE PAR COORDINATION]` pour le gain de
cout et la faisabilite ; le raisonnement statistique ci dessous est le mien.

Concretement : on presente la question et ses `K` modalites etiquetees, on force le format de
reponse a une seule etiquette, et on lit les logprobs du modele sur les `K` tokens d'etiquette au
premier pas de generation. Apres renormalisation sur les `K` modalites, on obtient une distribution
`q_{i,j} = (q_{i,j,1}, ..., q_{i,j,K})`.

**Quatre raisons, dont une est decisive.**

1. **Cout.** Zero token genere. Un seul passage avant par question, et avec le cache de prefixe le
   contexte du persona n'est encode qu'une fois par persona. C'est une part du facteur 75 mesure.
2. **Pas de bruit d'echantillonnage.** En generation, la reponse d'un persona a temperature > 0 est
   un tirage ; il faudrait des dizaines de repetitions pour estimer sa distribution. Ici on l'a
   exactement, en un passage.
3. **Pas de perte par parsing.** Aucun risque de reponse hors format, de bavardage, de refus.
4. **Decisive : cela donne directement la decomposition de la variance.** C'est developpe en
   A.8.2.

**Les trois limites a assumer et a documenter.**

- **Cela nous lie a des modeles a poids ouverts, executes localement.** La plupart des API
  frontieres n'exposent pas des logprobs exploitables sur des modalites arbitraires ; Groq a
  d'ailleurs ete ecarte precisement parce que ses logprobs renvoient une erreur
  `[VERIFIE PAR COORDINATION]`. On echange donc de la **qualite de modele** contre de la
  **precision de mesure et de la gratuite**. C'est un arbitrage explicite, pas un impense.
- **Il faut un run de controle en generation**, sur un sous echantillon, avec chaine de pensee,
  pour verifier que le passage aux logprobs ne deplace pas la fidelite. **Critere : ecart de
  fidelite inferieur a 0,03 entre mode logprobs et mode generation sur le meme sous echantillon.**
  Si l'ecart est superieur, la chaine de pensee apporte quelque chose que le premier token ne
  capte pas, et il faut le dire.
- **La probabilite du premier token n'est pas exactement la croyance du modele.** Elle est sensible
  a l'etiquetage des modalites et a leur ordre. D'ou A.8.5.

**Metrique principale en mode logprobs.** Plutot que l'accuracy binaire, on utilise l'**accuracy
esperee** :

```
                1
A_i^exp(c)  =  ---  sum_{j in J}  q_{i,j}( y_{i,j} )
                M
```

c'est a dire la probabilite moyenne attribuee a la bonne reponse. C'est une regle de score propre,
elle est directement comparable a l'accuracy argmax (qu'on rapporte aussi pour la comparabilite
avec Stanford), et **sa variance d'echantillonnage sur `M` items est nettement plus faible que
celle d'une accuracy binaire**, ce qui reduit le nombre de questions necessaires (section A.8.4).

### A.8.1 Famille 1 : fidelite individuelle

**Precision brute (argmax), pour comparabilite avec Stanford :**

```
              1
A_i(c)  =  ---  sum_{j in J}  1[ argmax_k q_{i,j,k} == y_{i,j} ]
              M
```

**Correlation sur items d'echelle**, avec `mu_{i,j} = sum_k q_{i,j,k} s(k)` l'esperance du score :

```
r_i(c) = Pearson( { mu_{i,j} }_{j in J} , { s(y_{i,j}) }_{j in J} )
```

Agregation : moyenne simple pour `A`, **moyenne apres transformation z de Fisher puis
transformation inverse** pour `r`. C'est la procedure de Stanford [CONFIRME].

**Precision normalisee :**

```
                 A_i(c)
NA_i(c)  =  --------------
                 rho_i
```

`NA = 1` signifie « l'agent predit l'individu aussi bien que l'individu se reproduit lui meme ».

**Erreur absolue moyenne** pour les items numeriques, apres normalisation min-max sur l'etendue
historique. **La normalisation n'est pas calculable sur la MAE** (la consistance interne peut valoir
0 au denominateur) ; Stanford le signale et ne normalise que l'accuracy et la correlation
[CONFIRME]. A reproduire tel quel.

### A.8.1.b Le denominateur `rho_i` : desormais mesure, plus estime

**C'etait le point dur de la version 1 de ce document. Il ne l'est plus.**

**Cas nominal, recommande : `rho_i` est mesure directement.**
- Sur l'archive OSF de Stanford : vague 2 a deux semaines, sur toute la cohorte. Denominateur
  agrege connu : **79,53 pour cent**.
- Sur Twin-2K-500 : vague 4 a deux semaines de la vague 3, sur le sous ensemble d'items repete.

```
             1
rho_i  =   ---  sum_{j in J}  1[ y_{i,j}^{(t)} == y_{i,j}^{(t+2sem)} ]
             M
```

C'est exactement la definition de Stanford. Aucune hypothese de modele, aucune estimation.

**Cas de repli, pour les jeux sans vague de retest (GSS, ANES) : l'estimateur de Heise a trois
vagues.**
Heise, D. R. (1969), *Separating Reliability and Stability in Test-Retest Correlation*, American
Sociological Review 34(1), pp. 93-101, DOI 10.2307/2092790. [CONFIRME que le papier et la methode
existent, et qu'ils sont implementes dans le paquet R `panelr`, fonction `heise`,
`https://panelr.jacob-long.com/reference/heise`. **Je n'ai pas lu le texte original ni verifie la
forme algebrique exacte.**]

Le probleme : une correlation entre deux vagues espacees de deux ans melange l'infidelite de mesure
et le changement reel d'attitude, donc **sous estime** la fiabilite, donc **surestime** `NA`.
Avec **trois** vagues, on dispose de `r12`, `r23`, `r13`, ce qui suffit a resoudre pour la
fiabilite et la stabilite separement, sous un modele simplexe d'ordre 1 (vrai score markovien,
erreurs non correlees, fiabilite constante) :

```
              r12 * r23
rho_hat_j  =  -----------
                 r13
```

Deux consequences :
- **C'est le critere qui impose de choisir des panels a trois vagues** (les panels roulants du GSS)
  et non a deux, pour l'etage E3.
- L'estimateur est **par item**, pas par individu. La normalisation devient
  `NA_i = A_i / rho_bar_i` avec `rho_bar_i = (1/M) sum_j rho_hat_j`. **C'est une difference reelle
  avec Stanford**, a documenter honnetement.

**Analyse de sensibilite obligatoire.** Quand les deux voies sont disponibles (c'est le cas sur
Twin-2K-500 pour les items repetes), rapporter `NA` sous **les deux** denominateurs et comparer.
**C'est un resultat methodologique publiable en soi** : cela dit si l'astuce de Heise est un
substitut valable au retest, ce qui interesse tous ceux qui travaillent sur des panels sans retest.
Critere : ecart entre les deux normalisations inferieur a 0,05.

### A.8.2 Famille 2 : preservation de la variance inter individus

**C'est la contribution scientifique visee.** Le papier de Stanford ne la mesure pas : il mesure
la reduction de disparite d'exactitude entre sous groupes (DPD), ce qui est autre chose [CONFIRME
par lecture]. Le creneau est libre.

Etat de l'art verifie :
- Boelaert et al. 2025 : biais fort et **variance faible** sur chaque sujet ; conditionner sur cinq
  variables sociodemographiques ne differencie pas les sous groupes. [CONFIRME]
- Bisbee et al., *Synthetic Replacements for Human Survey Data? The Perils of Large Language
  Models*, Political Analysis : **variance anormalement basse** et coefficients de regression
  desalignes. [CONFIRME que le papier porte ce resultat]
- Chen et al. 2026, arXiv:2607.26348 : **sur determination des demographies**, aucun LLM ne bat la
  meilleure baseline au niveau individuel. [CONFIRME]

#### A.8.2.a La decomposition de variance, rendue possible par les logprobs

C'est le coeur technique de la contribution.

Pour l'item `j`, sur la population simulee, la **loi de la variance totale** donne exactement :

```
Var_sim(j)  =  E_i[ v_{i,j} ]   +   Var_i[ mu_{i,j} ]
               \___________/       \______________/
                intra individu       inter individus
```

avec `mu_{i,j} = sum_k q_{i,j,k} s(k)` et `v_{i,j} = sum_k q_{i,j,k} (s(k) - mu_{i,j})^2`.
**Les deux termes sont calculables exactement, sans aucun echantillonnage, parce qu'on a la
distribution complete.** C'est impossible en mode generation sans repetitions massives.

Cote humain, on n'observe qu'une reponse par personne et par vague. Mais la **vague de retest**
donne un estimateur sans biais de la variance intra personne :

```
                        1
E_i[ v^hum_{i,j} ]  =  ---  sum_i  ( s(y_{i,j}^{(t)}) - s(y_{i,j}^{(t+2sem)}) )^2  /  2
                        N
```

d'ou la variance **inter individus reelle**, corrigee du bruit de mesure humain :

```
Var_inter_obs(j)  =  Var_obs(j)  -  E_i[ v^hum_{i,j} ]
```

**C'est la quantite que le projet veut reproduire.** Toute la litterature qui parle de « variance
ecrasee » compare en fait `Var_sim` brute a `Var_obs` brute, sans corriger le bruit humain, ce qui
melange deux choses. **Nous pouvons faire mieux, et c'est un argument de papier.**

#### A.8.2.b Les six sous scores de l'IDP

Tous dans [0,1], tous valant 1 sur la population observee par construction.

**S1, dispersion inter individus corrigee.** Le sous score principal.

```
                   sqrt( Var_i[ mu_{i,j} ] )
lambda_j   =    ---------------------------------
                   sqrt( Var_inter_obs(j) )

S1  =  (1/|J|) sum_j  min( lambda_j , 1/lambda_j )
```

Le `min(x, 1/x)` penalise symetriquement la sous dispersion et la sur dispersion. **Le chiffre a
annoncer dans le papier reste le `lambda_j` median brut**, parce qu'il est interpretable
directement : « les personas simules ont 61 pour cent de l'ecart type inter individus observe ».

**S2, distance de Wasserstein normalisee.** Sur une echelle ordinale a `K_j` rangs, soit `p_j` la
distribution marginale observee et `Q_j = (1/N) sum_i q_{i,j}` la marginale simulee :

```
W1(p_j, Q_j)  =  sum_{k=1}^{K_j - 1}  | F_p(k) - F_Q(k) |

S2  =  1  -  (1/|J|) sum_j  W1(p_j, Q_j) / (K_j - 1)
```

Le maximum atteignable est `K_j - 1` (deux masses de Dirac aux extremes), d'ou la normalisation.

**S3, ratio d'entropie.** `H(p) = - sum_k p_k log p_k` en nats.

```
S3  =  (1/|J|) sum_j  min( H(Q_j)/H(p_j) , H(p_j)/H(Q_j) )
```

Items avec `H(p_j) = 0` exclus de la moyenne.

**S4, structure inter items.** Soit `C_obs` et `C_sim` les matrices de correlation entre items
(Spearman, ou polychorique si le budget de calcul le permet) sur les `N` individus, `C_sim` etant
calculee sur les esperances `mu_{i,j}`. Soit `v_obs` et `v_sim` les vecteurs des elements hors
diagonale du triangle superieur.

```
S4  =  max( 0 , Pearson( v_obs , v_sim ) )
```

S4 capte ce que les autres ne voient pas : **un modele peut reproduire parfaitement chaque
marginale et detruire toute la structure de correlation, c'est a dire produire des individus
incoherents.** Test de Mantel avec permutations pour la p-valeur.

**S5, taux de clonage.** Le plus parlant pour un lecteur non technique. Calcule sur les reponses
argmax, pour etre directement comparable aux reponses ponctuelles humaines :

```
tau_sim  =  P( argmax q_{i,j} == argmax q_{i',j} )   sur des paires (i, i') distinctes
tau_obs  =  P( y_{i,j} == y_{i',j} )                 idem sur les donnees observees

S5  =  1  -  max( 0 , (tau_sim - tau_obs) / (1 - tau_obs) )
```

`S5 = 1` si les personas se ressemblent exactement autant que les vraies personnes, `S5 = 0` si
tous repondent identiquement. Version continue supplementaire, a rapporter en annexe :
`delta_sim = E_{i != i'}[ TVD(q_i, q_{i'}) ]`, la distance en variation totale moyenne entre deux
personas.

**S6, fidelite de la structure inter groupes. Nouveau, impose par les resultats de juillet 2026.**
Pour chaque item `j` et chaque partition demographique `g` (genre, education, race, region,
cohorte), on calcule la part de variance expliquee par l'appartenance au groupe (eta carre d'une
ANOVA a un facteur), du cote observe et du cote simule :

```
                 eta^2_sim(j, g)
FAD(j, g)  =  ---------------------          (facteur d'amplification demographique)
                 eta^2_obs(j, g)

S6  =  moyenne sur (j, g) de   min( FAD(j,g) , 1/FAD(j,g) )
```

`FAD > 1` signifie que le modele **gonfle** l'ecart entre segments demographiques par rapport aux
humains. C'est exactement le defaut documente par Chen et al. 2026. **Le FAD median brut est un
chiffre a annoncer separement**, parce qu'il est directement comparable a la litterature.

**S6 est ce qui separe la variance intra groupe de l'ecart inter groupes.** Un modele peut avoir
un S1 correct globalement tout en produisant deux blocs homogenes tres separes (chaque democrate
identique aux autres democrates, chaque republicain identique aux autres republicains) : S1 ne le
verra pas, S6 si.

#### A.8.2.c L'indicateur synthetique

```
IDP  =  ( S1 * S2 * S3 * S4 * S5 * S6 )^(1/6)
```

Trois proprietes qui le rendent defendable en revue :

1. **Moyenne geometrique, pas arithmetique.** Un effondrement sur un seul axe (par exemple S5 = 0,
   tous les personas identiques) fait tomber l'IDP a 0 meme si les cinq autres sont excellents.
   **La diversite n'est pas une moyenne de proprietes, c'est une conjonction.**
2. **Ancrages naturels.** `IDP = 1` pour la population observee. `IDP = 0` pour C1 (mode de la
   population, variance nulle). `IDP` proche de 1 pour C1b (tirage dans la marginale observee),
   avec une fidelite individuelle nulle. Toute methode se situe sur un plan borne et lisible.
3. **Decomposable.** On publie toujours l'IDP **et** ses six composantes. Un IDP de 0,55 ne dit pas
   ou est le probleme ; `S1 = 0,61 ; S5 = 0,42 ; S6 = 0,38` le dit.

**Le livrable scientifique est le plan (fidelite, IDP).** Une methode qui monte la fidelite en
faisant chuter l'IDP echange de la diversite contre de l'ajustement a la moyenne. C'est le defaut
de toute la litterature, et l'affichage sur deux axes le rend visible d'un coup d'oeil, avec C1 et
C1b comme bornes. **C'est la figure 1 du papier vise.**

### A.8.3 Regime d'echantillonnage et temperature

En mode logprobs, on lit la distribution **native** du modele au premier pas, sans reechantillonner.
La temperature de generation ne s'applique pas. En revanche, la temperature de softmax utilisee
pour renormaliser sur les `K` modalites est un choix : **on prend 1,0**, c'est a dire la
distribution telle que le modele la produit.

Cela a une consequence importante : **si le modele est mal calibre (trop confiant), l'IDP sera
penalise a travers S3 et S1, et ce sera un vrai resultat, pas un artefact.** Une eventuelle
recalibration par temperature (chercher le `T` qui minimise l'ecart de calibration sur un jeu de
developpement disjoint) doit etre traitee comme une **condition experimentale supplementaire**,
publiee separement, jamais comme un reglage silencieux. C'est un point d'integrite : recalibrer
jusqu'a obtenir un bel IDP serait de la fabrication.

En mode generation (run de controle uniquement) : temperature 0 pour la mesure principale, et un
run de sensibilite a 0,7 rapporte separement. Ne jamais melanger les deux dans une meme figure.

### A.8.4 Puissance statistique : confrontation avec l'agent infrastructure

**Modele.** Unite d'analyse = l'individu. Comparaison **appariee** entre deux conditions sur les
memes individus et les memes items. Test : t apparie, ou Wilcoxon signe si non normalite.
Soit `d_i = NA_i(c1) - NA_i(c2)`.

```
Var(d)  =  2 * sigma_b^2 * (1 - rho_cond)  +  2 * sigma_e^2
```

- `sigma_b` : ecart type **entre individus** du vrai score de fidelite.
- `rho_cond` : correlation entre conditions des vrais scores individuels.
- `sigma_e` : bruit d'estimation du score d'un individu, du au nombre fini d'items.

**Calibration a partir des chiffres reels de Stanford** : `p = 0,6567`, `rho = 0,7953`, ecart type
de la fidelite normalisee entre individus = 0,11.

*En mode generation (accuracy binaire)*, avec `M` items :
`sigma_e = sqrt(p(1-p)/M) / rho`. Pour `M = 50` : `sigma_e = 0,0672 / 0,7953 = 0,0845`.

*En mode logprobs (accuracy esperee)*, le score par item n'est plus un tirage de Bernoulli mais une
probabilite. [HYPOTHESE, a mesurer sur le pilote] la variance par item est reduite d'un facteur de
l'ordre de 2 a 3 ; je retiens 2,5. Alors `sigma_e ~= 0,0845 / sqrt(2,5) = 0,053`.

Ecart type total observe 0,11, donc `sigma_b^2 = 0,11^2 - 0,053^2 = 0,0093`.
En posant `rho_cond = 0,6` (hypothese moderee) :

```
Var(d)  =  2 * 0,0093 * 0,4  +  2 * 0,053^2  =  0,00744 + 0,00562  =  0,0131
sd(d)   =  0,114
```

**Taille d'echantillon** (bilateral, alpha = 0,05, puissance 0,80) :

```
N  =  (1,96 + 0,8416)^2 * sd(d)^2 / delta^2  =  7,849 * 0,0131 / delta^2  =  0,1028 / delta^2
```

| Ecart a detecter | Exemple concret | N requis, **M = 50, mode logprobs** |
|---|---|---|
| 0,12 | persona complet contre persona (0,83 contre 0,71) | **8** |
| 0,09 | persona complet contre demographique (0,83 contre 0,74) | **13** |
| 0,05 | persona complet contre placebo, si effet net | **42** |
| 0,03 | RAG contre contexte integral | **115** |
| 0,02 | avec reflections contre sans | **257** |

**En mode generation, meme `M = 50`** : `Var(d) = 0,00744 + 2*0,0845^2 = 0,0217`, `sd(d) = 0,147`,
`N = 0,170 / delta^2`. Pour `delta = 0,03`, il faut alors **189** individus au lieu de 115.

**Deux conclusions operationnelles.**

1. **Le mode logprobs divise par 1,65 le nombre d'individus necessaires, a nombre de questions
   constant.** Ce n'est pas seulement une economie de calcul, c'est un gain de puissance.
2. **Augmenter `M` coute beaucoup moins cher qu'augmenter `N`**, parce que le contexte du persona
   est encode une seule fois et amorti sur toutes ses questions (cache de prefixe). **Le bon
   reglage est donc peu d'individus et beaucoup de questions.** C'est contre intuitif et c'est le
   resultat le plus utile de ce calcul.

**Confrontation avec l'agent infrastructure. Je confirme son chiffre.**
Sa conclusion : la phase 1 demande **70 a 100 personas sur 30 a 50 questions**. Mon calcul
independant, en mode logprobs avec `M = 50`, donne `N = 42` pour detecter 0,05 et `N = 13` pour
detecter 0,09. **Donc 70 a 100 personas sont non seulement suffisants, ils sont confortables** :
ils detectent des ecarts de 0,032 a 0,038, ce qui couvre largement les trois contrastes de la
phase 1 (`CT - C2` attendu a 0,09, `CT - C3` attendu du meme ordre, `CT - C7` inconnu).

Avec `M = 30` au lieu de 50, `sigma_e` monte a 0,068, `Var(d) = 0,00744 + 0,0092 = 0,0166`,
`sd(d) = 0,129`, `N = 0,130/delta^2` : pour `N = 100`, on detecte 0,036. **Toujours suffisant.**

**Le message a faire passer, en une phrase.** Le facteur limitant du projet n'est pas le calcul :
100 personas sur 50 questions et 5 conditions LLM font 25 000 passages avant, soit de l'ordre d'une
heure sur le Mac d'Amir. **Le facteur limitant est la matiere humaine, et le budget zero n'est pas
une contrainte serieuse pour la phase 1.**

**Ou le budget redevient une contrainte** : quand on veut detecter des ecarts de 0,02 entre
methodes d'injection (N = 257, M = 150, 4 methodes = 154 000 passages avant), et surtout quand on
veut la **qualite de modele** d'un GPT-4o plutot que celle d'un Qwen3 30B. Voir A.9.4.

**Correction de multiplicite.** Huit conditions font 28 comparaisons deux a deux. **Pre enregistrer
quatre contrastes seulement** (`CT - C2`, `CT - C3`, `CT - C5`, `CT - C7`) et ne pas corriger, ou
corriger par Holm si on en ajoute. La premiere option est preferable, et c'est a cela que sert le
pre enregistrement.

**Puissance sur les metriques de variance.** Le ratio `lambda_j` est estime par item sur `N`
individus ; l'erreur type relative d'un ecart type estime vaut environ `1/sqrt(2(N-1))`, soit 0,071
pour `N = 100`. Un `lambda` observe de 0,60 est distinguable de 1,0 sans difficulte. Pour S6, la
contrainte est plus dure : un eta carre par groupe demande des effectifs par cellule, donc **au
moins 25 individus par groupe demographique**. Avec `N = 100` et une partition binaire, c'est
tenu ; avec une partition en cinq groupes, il faut `N = 150`. **C'est S6 qui fixe la taille
d'echantillon de la phase 1, pas la fidelite.** Recommandation finale : `N = 150`, `M = 50`.

### A.8.5 Trois precautions de mesure specifiques au mode logprobs

1. **Biais de position.** La probabilite d'une etiquette depend de sa position dans la liste.
   Parade : chaque question est posee sous `P` permutations aleatoires des modalites (`P = 4`
   suffit), et `q_{i,j}` est la moyenne des distributions renormalisees sur les permutations.
   **Mesure a rapporter** : ecart type entre permutations de la probabilite attribuee a une
   modalite donnee. **Critere : inferieur a 0,05.** Au dela, augmenter `P`.
2. **Choix des etiquettes.** Utiliser des etiquettes neutres et equilibrees en frequence
   (`A`, `B`, `C`... plutot que `1`, `2`, `3` qui portent un ordre implicite fort). Verifier que le
   modele sans contexte ne prefere pas systematiquement une etiquette (test a vide sur 200
   questions).
3. **Renormalisation.** La masse de probabilite hors des `K` etiquettes doit etre mesuree et
   rapportee. Si elle depasse 20 pour cent, le prompt de format est mauvais et il faut le corriger
   avant tout run.

### A.8.6 Critere de succes de l'etape

- Les quatre contrastes pre enregistres estimes avec intervalle de confiance.
- L'IDP et ses six composantes pour chaque condition, plus `lambda` median et FAD median en brut.
- Le plan (fidelite, IDP) trace, avec les huit conditions positionnees.
- La comparaison logprobs contre generation sur un sous echantillon, ecart inferieur a 0,03.
- Le biais de position mesure, inferieur a 0,05.
- Quand les deux denominateurs sont disponibles, la comparaison retest mesure contre Heise estime.

## A.9. Couts, materiel et modeles candidats

`[VERIFIE PAR COORDINATION]` pour toutes les mesures materielles de cette section.

### A.9.1 Le materiel reel

**Apple M5 de base : 10 coeurs CPU, GPU 10 coeurs, 32 Gio de memoire unifiee, 593 Gio libres.**
Ni Pro ni Max. Toutes les estimations ci dessous sont des **mesures**, pas des extrapolations.

### A.9.2 Capacite et facteur d'optimisation

| Mesure | Valeur |
|---|---|
| Volume realisable gratuitement en **local** | **~400 000 appels de modele par semaine** |
| Volume realisable sur **toutes les offres gratuites d'API cumulees** | **~12 000 appels par semaine** |
| Rapport | **facteur 33 en faveur du local** |
| 10 000 appels, implementation naive | **31 heures** |
| 10 000 appels, avec cache de prefixe + batch + lecture des logprobs | **25 minutes** |
| Facteur d'optimisation | **75** |

**Ces deux lignes suffisent a trancher tout le debat infrastructure.** Le local n'est pas un repli
degrade, il est trente fois plus capable que l'ensemble des offres gratuites, et l'optimisation
(cache de prefixe, batch, logprobs) vaut soixante quinze fois plus que le choix du fournisseur.

### A.9.3 Modeles retenus

| Modele | Role |
|---|---|
| **Qwen3 4B Q4** | degrossir : mise au point des prompts, tests de fuite, iterations rapides |
| **Qwen3 30B-A3B Q4** | qualite : le modele de reference pour les resultats publies |
| **Llama 3.1 8B Q4** | troisieme famille, condition de controle sur la dependance au modele |

**Ecartes, et pourquoi** :
- **Groq** : ses logprobs renvoient une erreur. Incompatible avec le mode d'evaluation par defaut.
- **Modeles gratuits d'OpenRouter** : exigent d'accepter la publication des prompts. Incompatible
  avec un projet qui manipule des donnees d'enquete, meme publiques, et avec une visee de
  publication.

**Le controle a trois familles de modeles est important pour le papier.** Chen et al. 2026 montrent
que les echecs persistent quelle que soit la taille du modele. Si nos resultats sont stables sur
Qwen3 4B, Qwen3 30B-A3B et Llama 3.1 8B, l'objection « c'est un artefact de votre modele » tombe.

**Limite a assumer.** Stanford mesure 0,66 de precision brute avec GPT-4o et 0,60 avec GPT-4o-mini.
[HYPOTHESE] Un Qwen3 30B-A3B quantifie se situe probablement dans cette fourchette, plutot vers le
bas. **On perd donc quelques points de precision brute par rapport a Stanford.** Ce n'est pas
grave, pour deux raisons : nos conclusions portent sur des **ecarts entre conditions** mesures avec
le meme modele, pas sur un niveau absolu ; et le score normalise absorbe une partie de l'ecart.
Mais il faut le dire, et il faut ajouter un run de plafond sur un modele plus fort si l'occasion se
presente.

### A.9.4 Volumes de l'experience, et ou est le mur

Design de la phase 1 : `N = 150`, `M = 50`, conditions LLM = CT, C2, C3, C7 (les autres ne
consomment aucun appel), `P = 4` permutations.

Passages avant = 150 x 50 x 4 x 4 = **120 000**.

| Palier | Design | Passages avant | Temps local estime | Faisable a zero euro ? |
|---|---|---|---|---|
| Etage E1, reanalyse OSF | aucun appel de modele | **0** | quelques heures de calcul tabulaire | **Oui, trivialement** |
| Pilote | N=30, M=30, 2 conditions, P=2 | 3 600 | **~10 min** | **Oui** |
| **Phase 1** | N=150, M=50, 4 conditions, P=4 | 120 000 | **~5 h** | **Oui** |
| Comparaison fine des injections | N=250, M=150, 4 methodes, P=4 | 600 000 | ~25 h, soit une semaine et demie de capacite | **Oui, mais ca commence a mordre** |
| Trois familles de modeles | x3 sur la phase 1 | 360 000 | ~15 h | **Oui** |
| Echelle 10 000 agents | N=10 000, M=150, 1 condition, P=4 | 6 000 000 | ~250 h, soit ~2,5 semaines de capacite continue | **Oui en local**, si on accepte le delai |

**Le mur ne se situe plus dans le volume.** Avec 400 000 appels par semaine en local, meme le
passage a 10 000 agents tient, en deux a trois semaines de calcul continu. **Le mur est ailleurs,
et il est double :**

1. **Le mur de qualite de modele.** Si les resultats ne tiennent qu'avec un modele frontiere, il
   faut payer. Chiffrage minimal, avec Claude Haiku 4.5 a 1,00 USD le million de tokens d'entree et
   5,00 USD le million de sortie, et l'API Batch a 50 pour cent [CONFIRME via la table tarifaire de
   reference chargee pour ce document] : la phase 1 en mode generation, avec un contexte RAG de
   1 300 tokens et 200 tokens de sortie, sur 30 000 appels (sans permutations, la generation les
   rendant trop chere), donne 39 M tokens d'entree et 6 M de sortie, soit **69 USD**, ou **~35 USD**
   en Batch. **La phase 1 sur modele frontiere coute donc de l'ordre de 35 a 70 dollars.** C'est le
   seul chiffre de depense reellement pertinent du projet.
2. **Le mur de la matiere humaine.** C'est le vrai. Voir voie B.

**Formulation a retenir pour Simon.** « L'experience de reproduction complete, avec ses huit
conditions de controle et son analyse de variance, tient a zero euro sur le Mac, en cinq heures de
calcul. La seule depense qui aurait un sens serait 35 a 70 dollars pour verifier que le resultat
tient aussi sur un modele frontiere. Ce qui nous limite n'est ni le calcul ni l'argent. »

### A.9.5 Credits academiques

[HYPOTHESE, non verifie] Des programmes de credits pour la recherche academique existent chez les
grands fournisseurs, ainsi que des allocations de calcul nationales. Le contact MIT de Simon est le
levier direct. **A verifier avant de budgeter quoi que ce soit**, mais compte tenu de A.9.4, ce
n'est plus une question urgente : c'est une commodite, pas un deblocage.

## A.10. Deroule executable de la voie A

Chaque etape porte un critere de succes verifiable. Ne pas passer a la suivante sans lui.

**A1. Lever l'ambiguite sur l'archive OSF.** Telecharger `https://osf.io/t6g7k/`, ouvrir les huit
CSV, verifier si les lignes sont individuelles ou agregees, si les reponses d'agents sont
appariables aux individus, et si les cinq conditions sont toutes presentes.
*Succes* : un compte rendu ecrit tranchant la question, avec la liste des colonnes.
**Si les donnees sont agregees, l'etape A2 est annulee et on passe directement a A4 sur
Twin-2K-500.** Duree : une demi journee.

**A2. Etage E1, reanalyse a cout nul.** Calculer, sur les sorties d'agents deja publiees par
Stanford, l'IDP et ses six composantes pour les cinq conditions, plus `lambda` median et FAD
median. Aucun appel de modele.
*Succes* : un tableau IDP x condition, et le plan (fidelite, IDP) trace avec les cinq conditions de
Stanford dessus. **C'est deja un resultat original publiable, obtenu sans budget et sans calcul.**
Duree : deux a trois jours.

**A3. Benchmark materiel.** Mesurer sur le M5 le debit reel en passages avant par seconde pour les
trois modeles retenus, avec et sans cache de prefixe, en mode logprobs, sur un contexte de 1 300 et
de 6 000 tokens.
*Succes* : un tableau de debits mesures, confrontant le facteur 75 annonce. Duree : une demi
journee.

**A4. Acquisition de Twin-2K-500.** Telecharger, verifier les quatre vagues, identifier precisement
quels items sont repetes en vague 4 (donc quels items disposent d'une fiabilite mesuree).
*Succes* : au moins 1 500 individus avec quatre vagues exploitables, et au moins 30 items avec
retest.

**A5. Dictionnaire d'items et partition `A` / `B`.** Table longue `(individu, item, vague, reponse,
modalites, scores, type)`. Figer la partition **avant** tout run et la committer.
*Succes* : partition figee et signee dans un commit date. Au moins 300 items en `A`, 100 en `B`,
dont 30 avec retest.

**A6. Denominateur.** Calculer `rho_i` par retest direct sur les items repetes. Sur les autres,
appliquer Heise aux vagues 1 a 3 et **comparer les deux estimateurs sur les items ou les deux sont
disponibles**.
*Succes* : `rho_i` disponible pour 100 pour cent des individus ; ecart entre les deux estimateurs
inferieur a 0,05 sur les items communs, ou ecart documente s'il est superieur.

**A7. Anti fuite.** Detection automatique des paires quasi synonymes `A` / `B`, revue manuelle
exhaustive des paires signalees, retrait. Classification de chaque paire en « recuperable »,
« inferable », « ni l'un ni l'autre » pour alimenter la condition C7.
*Succes* : 100 pour cent des paires signalees revues et tracees ; tables de recuperabilite et
d'inferabilite produites.

**A8. Audit de contamination.** T1, T2, T3, et T4 si une vague post coupure est disponible.
*Succes* : T1 non superieur au hasard. Resultats consignes quels qu'ils soient.

**A9. Baselines non LLM.** Entrainer C4 et C5 en validation croisee **par individu**. Calculer C0,
C1, C1b analytiquement.
*Succes* : precision de C0, C1, C1b, C4, C5 disponibles **avant tout run LLM**. C'est important de
les avoir avant, pour ne pas se raconter d'histoires apres.

**A10. Construction des personas.** Generer les fichiers YAML pour `N = 150`, avec reflections
d'expert et profil condense.
*Succes* : validation de schema a 100 pour cent, test automatique d'absence de fuite passe.

**A11. Calibration du mode logprobs.** Mesurer le biais de position, la masse hors etiquettes, et
comparer logprobs contre generation sur un sous echantillon de 30 individus.
*Succes* : biais de position inferieur a 0,05 ; masse hors etiquettes inferieure a 20 pour cent ;
ecart logprobs / generation inferieur a 0,03. **Si ce dernier critere echoue, le mode logprobs est
abandonne comme mode principal et tout le budget de la section A.9 est a refaire.**

**A12. Pilote.** N=30, M=30, conditions CT (en M2) et C2. Temperature native.
*Succes* : `F_max` mesure et `F_max > F(C2)` avec p < 0,05.

**A13. Echelle des methodes d'injection.** Paliers 0 a 4 de la section A.7.2, avec leurs criteres
chiffres de passage.
*Succes* : une methode retenue, son rapport fidelite/cout, une decision tracee.

**A14. Phase 1.** N=150, M=50, huit conditions, methode d'injection retenue, P=4 permutations,
sur Qwen3 30B-A3B.
*Succes* : les quatre contrastes pre enregistres avec intervalle de confiance ; l'IDP et ses six
composantes pour chaque condition ; le plan (fidelite, IDP) trace. **`CT > C3` avec p < 0,05 est le
critere bloquant.**

**A15. Controle de dependance au modele.** Rejouer A14 sur Qwen3 4B et Llama 3.1 8B.
*Succes* : le sens et l'ordre des quatre contrastes sont conserves sur les trois familles.

**A16. Generalisation.** Rejouer A5 a A14 sans modification du protocole sur un deuxieme jeu :
GSS panel (generalisation politique, et seul cas ou Heise est necessaire) ou LISS (generalisation
culturelle, faible contamination).
*Succes* : le sens des quatre contrastes est conserve.

**A17. Extension comportement d'achat.** Rejouer le protocole sur dunnhumby *The Complete Journey*,
en assumant l'adaptation des metriques au support non ordonne (recall@k au lieu d'accuracy).
*Succes* : un resultat, quel qu'il soit. **C'est ce qui donne au commercial sa preuve de
transferabilite, apres que la methode a ete validee et pas avant.**

**A18. Rapport.** Document quantitatif, avec le pre enregistrement, les criteres qui ont echoue,
et une section « ce qui n'a pas marche ».
*Succes* : presentable au MIT sans avoir a repondre a une question qu'on n'a pas anticipee.

---

# VOIE B, DIFFEREE : LE PROTOCOLE A 10 PERSONNES

**Statut : phase ulterieure. Ne se declenche que si de la matiere humaine devient disponible.**
Rien ici n'est a executer maintenant. Cette section existe pour etre prete le jour ou la contrainte
tombe, et pour chiffrer honnetement ce que la contrainte nous coute.

## B.0. Condition de declenchement, et une mise en garde

La voie B se declenche si et seulement si **au moins une** des trois conditions est remplie :
1. Un budget de participants est debloque (voir B.5).
2. Un partenaire academique ouvre l'acces a une cohorte consentante, aux transcripts de l'American
   Voices Project, ou aux transcripts non publies de Stanford.
3. Un vivier non remunere credible se constitue, en assumant explicitement le biais
   d'echantillonnage.

**Mise en garde, et elle est forte.** La voie B a une **valeur marginale faible** au vu des chiffres
actuels :
- L'entretien de deux heures rapporte **un point** de plus que les reponses de sondage (0,83 contre
  0,82).
- Une part de ce point vient d'un mecanisme d'**extraction** de reponses deja donnees pendant
  l'entretien, confirme par les auteurs, et non d'une simulation.
- Le facteur limitant du projet est desormais la matiere humaine, mais la voie A ne manque pas de
  matiere humaine : elle en a 1 052 chez Stanford et 2 058 chez Twin-2K-500, deja collectee.

**La seule raison serieuse de faire la voie B est l'etape B8**, qui valide ou invalide nos choix
methodologiques contre une mesure directe. Tout le reste est deja disponible gratuitement.

## B.1. Le script d'entretien de deux heures

Adapte de celui de Stanford, lui meme une version abregee du script de l'American Voices Project
(`https://inequality.stanford.edu/avp/methodology`). Le script complet figure en table 7 du PDF de
`arXiv:2411.10109` et **peut donc etre repris**. [CONFIRME]

Structure relevee dans le PDF, avec les durees telles que programmees par Stanford. Les blocs
regroupent les 99 questions scriptees.

| # | Bloc | Contenu | Duree cible |
|---|---|---|---|
| 0 | Cadrage et consentement | presentation, controles, consentement oral | 3 min |
| 1 | Recit de vie | « racontez moi l'histoire de votre vie » (625 s allouees a cette seule question), puis le moment de bifurcation, choix ou hasard | 20 min |
| 2 | Famille et entourage | partenaire, enfants, famille elargie, amis, relations hors famille | 8 min |
| 3 | Quartier et logement | description, sentiment de securite, vecu, roster du menage | 8 min |
| 4 | Routine et travail | semaine type, emploi, horaires, responsabilites, changements recents | 8 min |
| 5 | Police et justice | experiences avec les forces de l'ordre, arrestations dans l'entourage | 4 min |
| 6 | Politique | vote et abstention, description de ses opinions (310 s), evolutions recentes | 8 min |
| 7 | Race | Black Lives Matter, question raciale, reactions personnelles et de l'entourage | 8 min |
| 8 | Sante | sante generale, facilitateurs et obstacles, evenements recents, sante d'un proche, acces aux soins, renoncement, medecines alternatives | 12 min |
| 9 | Substances et vaccination | tabac, alcool, medicaments, cannabis ; attitude vaccinale et sources de confiance | 8 min |
| 10 | Etat emotionnel | ressenti de l'annee, episode difficile, depression et anxiete, famille | 8 min |
| 11 | Religion et spiritualite | importance dans la vie | 3 min |
| 12 | Reseaux sociaux | usage, recherche de soutien en ligne, evolution du stress | 4 min |
| 13 | Verification du menage | re verification du roster, partage des charges | 2 min |
| 14 | Budget | plus grosses depenses, total mensuel, proprietaire ou locataire, fluctuations | 8 min |
| 15 | Revenus et aides | sources de revenu, aides, difficultes | 8 min |
| 16 | Origine sociale | education et emploi des parents | 5 min |
| 17 | Projection et valeurs | « imaginez vous dans quelques annees » (155 s), « qu'est ce que vous valorisez le plus ? » (80 s) | 5 min |
| 18 | Cloture | remerciements, suite de l'etude | 2 min |

**Total scripte : environ 2 h**, relances comprises. Chez Stanford, l'intervieweur pose 81,7
relances en moyenne, produit 5 372 mots et obtient 6 491 mots du participant. [CONFIRME]

**Adaptation pour un contexte francais**, si on interroge des francais :
- Le bloc 7 n'a pas d'equivalent direct. Le remplacer par un bloc sur les discriminations et les
  origines, formule sans presupposer de categorie ethnique, la collecte de donnees ethno raciales
  etant encadree en France. [PROBABLE, a faire valider]
- Le bloc 5 est a conserver mais reformule ; le bloc 15 a remapper sur les dispositifs francais.
- **Attention** : plus on adapte, moins on est comparable a Stanford. Si l'objectif est la
  reproduction, interroger des americains anglophones est methodologiquement superieur.

**Modification imposee par le mecanisme d'extraction.** Puisque une part de la performance des
agents entretien vient de la recuperation de reponses deja donnees, il faut, **avant** de refaire
des entretiens, decider si on veut ce mecanisme ou non. Deux options a trancher avec Simon :
soit on garde le script tel quel et on **mesure** la part d'extraction (condition C7), soit on
**epure** le script de toute question dont la reponse chevauche la batterie d'evaluation, ce qui
donne une mesure plus pure de la simulation mais s'ecarte du protocole de reference.

## B.2. Intervieweur humain ou agent IA

Stanford a construit un intervieweur IA voix a voix et le presente comme une contribution
methodologique. Architecture : TTS pour poser les questions, Whisper pour transcrire, GPT-4o pour
decider de relancer, et un module de reflexion qui synthetise la conversation en notes courtes ;
le prompt fournit a chaque tour les notes accumulees plus les 5 000 derniers caracteres du
transcript. [CONFIRME]

| Critere | Intervieweur humain | Agent IA |
|---|---|---|
| Cout par entretien | 2 h de temps qualifie, poste dominant | quelques dollars d'API, ou zero en local |
| Passage a l'echelle | lineaire et bloquant | parallelisable |
| Qualite des relances | superieure | jugee suffisante par Stanford apres 3 vagues de 3 pilotes |
| Standardisation | variable | parfaite |
| Divulgation intime | [HYPOTHESE] potentiellement superieure avec un agent sur les sujets sensibles ; non verifie |
| Charge de developpement | nulle | reelle : chaine voix, coupures, reprises sur checkpoint |
| Acceptabilite ethique | etablie | a expliciter dans le consentement |

**Recommandation : agent IA.** C'est la configuration exacte de Stanford, donc comparable ; c'est
la seule qui passe a l'echelle ; et on ne construit pas un protocole pour 10 personnes, on
construit un protocole pour 1 000 qu'on teste sur 10.

**Version degradee a budget zero**, si la voie B se declenche sans argent : entretien semi
structure en visio, mene par Amir, enregistre, transcrit par Whisper en local (gratuit), sans
chaine voix a voix temps reel. On perd la standardisation et le passage a l'echelle, on garde la
matiere. **C'est la bonne facon de faire les 10 premiers.**

## B.3. Materiel necessaire

**Version agent IA** : plateforme web (inscription, consentement, modules sequences, checkpoints de
reprise) ; chaine voix (TTS, Whisper en local et gratuit, modele de decision de relance) ; stockage
chiffre des transcripts (Stanford insiste sur leur difficulte a anonymiser [CONFIRME]) ; batterie
d'evaluation en ligne ; protocole de consentement valide.

**Version degradee** : visio avec enregistrement, Whisper local, formulaire en ligne gratuit,
stockage chiffre. Cout : zero.

**Dans les deux cas** : un pre enregistrement depose avant collecte (OSF, gratuit), et un avis
ethique. **Point bloquant potentiel** : sans affiliation institutionnelle, obtenir un avis de
comite d'ethique est difficile. C'est un argument de plus pour que le partenariat MIT precede la
voie B, pas l'inverse.

## B.4. Deroule du protocole a 10 personnes

**B1.** Pre enregistrement du protocole et des hypotheses, avant tout contact.
*Succes* : depot horodate.

**B2.** Recrutement de 10 personnes, profils volontairement contrastes sur age, genre, education,
orientation politique. A 10 personnes, la representativite est hors d'atteinte : **l'objectif est la
variance, pas la representativite.**
*Succes* : 10 consentements signes, aucune cellule demographique a plus de 3 personnes.

**B3.** Entretien de 2 h par personne, selon le script B.1.
*Succes* : 10 transcripts, longueur mediane superieure a 4 000 mots. En dessous, l'entretien a
echoue.

**B4.** Passation vague 1 : GSS core et BFI-44. Duree mediane observee chez Stanford : 55 minutes
[CONFIRME].
*Succes* : 10 passations completes.

**B5.** Passation vague 2, **exactement deux semaines plus tard**, meme batterie sans entretien.
*Succes* : 10 re passations. **Aucune attrition toleree a N = 10.** Prevoir des rappels et une
compensation conditionnee a la vague 2.

**B6.** Construction de trois agents par personne : entretien seul, sondage seul, les deux.
*Succes* : 30 personas valides au schema A.6.

**B7.** Evaluation sur la vague 2, avec les huit conditions de controle de la voie A, en mode
logprobs, et `rho_i` **mesure directement**.
*Succes* : les quatre contrastes estimes. **Avec N = 10, seuls des ecarts d'environ 0,10 ou plus
sont detectables** (mon calcul A.8.4 donne N = 8 pour delta = 0,12 et N = 13 pour delta = 0,09).
Cela suffit pour reproduire l'ecart persona complet contre persona (0,83 contre 0,71) et,
tout juste, l'ecart contre le demographique. **Pour rien d'autre. Le dire d'emblee.**

**B8. La seule etape qui justifie vraiment la voie B.** Triple validation croisee des choix
methodologiques de la voie A contre des mesures directes, sur les memes 10 personnes :
- l'estimateur de Heise reproduit il le retest a deux semaines ? Critere : ecart inferieur a 0,05.
- le mode logprobs reproduit il le mode generation avec chaine de pensee ? Critere : ecart
  inferieur a 0,03.
- la correction du bruit intra personne dans S1 (section A.8.2.a) est elle stable ?
*Succes* : les trois criteres tenus, ou les ecarts documentes. **C'est ce resultat qu'il faut mettre
en avant pour justifier la depense, pas la fidelite elle meme.**

## B.5. Cout reel si un jour on paie des participants

Reference Stanford [CONFIRME] : 60 USD phase 1, 30 USD phase 2, bonus 0 a 10 USD. Soit **90 a 100
USD par participant**, hors frais de la societe de recrutement (Bovitz), non chiffres dans le
papier.

| Poste | 10 personnes | 100 personnes | 1 000 personnes |
|---|---|---|---|
| Tarif Stanford (95 USD) | 950 USD | 9 500 USD | 95 000 USD |
| Tarif plancher plausible (35 USD pour 3 h) [HYPOTHESE] | 350 USD | 3 500 USD | 35 000 USD |
| Frais de plateforme (Prolific, ~30 a 40 %) [HYPOTHESE, non verifie] | +30 % | +30 % | +30 % |
| API voix pour l'intervieweur IA (2 h par personne) | **non chiffre, tarifs voix non verifies** | | |
| Developpement de la plateforme | plusieurs semaines de temps Amir | idem | idem |

**L'arbitrage a poser a Simon, en une phrase.** 10 personnes coutent 350 a 1 250 USD. La phase 1 de
la voie A coute **zero**, et sa version sur modele frontiere coute **35 a 70 USD**. **Le premier
millier de dollars ne doit pas aller a la voie B**, il doit aller a un modele frontiere, a des
credits de calcul, ou nulle part.

---

## Ce que je n'ai pas pu verifier

- **Le contenu reel de l'archive OSF `https://osf.io/t6g7k/`.** La page est rendue par JavaScript
  et n'est pas lisible par simple recuperation HTTP. Je m'appuie sur la verification d'un autre
  agent (8 CSV, 1 052 lignes, 178 colonnes, vagues 1 et 2, sorties des cinq conditions).
  **Cette description contredit une phrase du papier lui meme**, qui annonce un acces ouvert aux
  reponses « agregees » aux instruments de sondage. **C'est l'etape A1 du protocole, et tout
  l'etage E1 en depend.**
- **La formule exacte de Heise** `rho = r12 * r23 / r13`. J'ai confirme l'existence du papier
  (Heise 1969, ASR 34(1), pp. 93-101, DOI 10.2307/2092790), le principe et l'existence d'une
  implementation dans le paquet R `panelr`. Je n'ai **pas** lu le texte original ni verifie la
  forme algebrique exacte ni la liste complete des hypotheses. Point critique uniquement pour
  l'etage E3 (jeux sans vague de retest), plus pour le chemin principal.
- **Le facteur de reduction de variance du mode logprobs** par rapport a l'accuracy binaire.
  J'ai pose 2,5 par [HYPOTHESE]. C'est mesurable directement sur le pilote et cela doit l'etre :
  tout le calcul de puissance en depend.
- **Le facteur 2 a 4 de gonflement des ecarts inter segments** attribue a arXiv:2608.14606. Ce que
  j'ai verifie dans la notice est un rapport entre effets demographiques **a l'interieur du
  modele** (education 0,56 contre genre 0,12 et role 0,18), pas un rapport modele sur humain.
  Le message operationnel tient, le facteur exact n'est pas verifie par moi.
- **Le nombre de 71 pour cent pour la condition persona.** Transmis par la coordination, coherent
  avec ce que le PDF dit qualitativement, mais je ne l'ai pas trouve chiffre dans le texte que j'ai
  extrait.
- **Les tarifs de synthese vocale et de transcription temps reel** pour un intervieweur IA. Poste
  non chiffre de la voie B.
- **La licence exacte et la richesse demographique de dunnhumby *The Complete Journey*.**
  Existence, taille et diffusion confirmees ; utilisabilite pour un travail a visee commerciale et
  taux de couverture demographique **non verifies**.
- **Les conditions d'acces reelles** de Understanding Society, Understanding America Study et
  SHARE.
- **Le statut de l'opinion politique comme donnee sensible au sens de l'article 9 du RGPD.**
- **Le multiplicateur de prix de la lecture en cache** chez les fournisseurs payants.
- **La position d'un Qwen3 30B-A3B quantifie par rapport a GPT-4o** sur cette tache. [HYPOTHESE]
  Mesurable des l'etape A12.
- **Le precedent en psychiatrie publie dans Nature** cite par Simon dans `CONTEXTE.md`. Hors de mon
  perimetre ; il porte peut etre une metrique de variance reutilisable et merite d'etre identifie.
- **Si le mecanisme d'extraction se comporte pareil en voie A qu'en voie B.** Stanford le mesure sur
  des transcripts. En voie A, l'entree est faite d'items de sondage, formates comme les items
  d'evaluation, donc la structure d'inference est differente et probablement plus forte. C'est une
  inconnue reelle : c'est ce que la condition C7 et le decoupage L2 cherchent a neutraliser.

## Questions ouvertes pour Simon

1. **Le contact MIT peut il ouvrir l'acces aux transcripts non publies de Stanford, ou a ceux de
   l'American Voices Project ?** Avec l'archive OSF et Twin-2K-500, nous avons deja les reponses de
   sondage de plus de 3 000 personnes. Ce qui nous manque, et seulement cela, c'est de la matiere
   d'entretien. Si ce verrou saute, la voie B devient realisable a budget zero et le projet est
   complet. **C'est de loin la question la plus rentable du document.**

2. **Faut il investir 35 a 70 dollars pour verifier la phase 1 sur un modele frontiere ?**
   Le protocole tient a zero euro en local sur Qwen3 30B-A3B. Le seul risque est que le resultat
   soit un artefact d'un modele plus faible que GPT-4o. Ce chiffre est le seul poste de depense qui
   me parait justifie dans tout le projet.

3. **Si `CT - C5` est negatif, quelle est la contribution ?** Chen et al. 2026 montrent qu'aucun LLM
   ne bat la meilleure baseline statistique sur la prediction individuelle. Il est probable que nous
   le retrouvions. Dans ce cas la contribution se deplace vers deux axes : la **generalite** (un
   persona repond a n'importe quelle question, une regression doit etre reentrainee par question)
   et la **variance**. Est ce que cela tient comme angle de publication, ou faut il reformuler
   l'ambition ?

4. **L'Indice de Diversite Preservee est il defendable en revue ?** Moyenne geometrique de six sous
   scores, avec la propriete voulue qu'un effondrement sur un axe fasse chuter l'indice. La critique
   previsible porte sur l'arbitraire du choix des six composantes et de leur egalite de poids.
   Faut il justifier les poids, en enlever, ou publier les six separement sans indice synthetique ?
   Simon a la double casquette psychologie et IA : c'est exactement son terrain.

5. **La correction du bruit intra personne dans la mesure de variance est elle un vrai apport ?**
   Ma proposition (section A.8.2.a) est de corriger `Var_obs` du bruit intra personne humain estime
   par la vague de retest, avant de la comparer a la variance inter personas simulee. Toute la
   litterature compare des variances brutes. Si c'est correct, c'est un point methodologique
   publiable en soi. Si j'ai rate une raison de ne pas le faire, il faut le savoir tout de suite.

6. **Le mode logprobs est il acceptable comme mode d'evaluation principal ?** Il nous lie a des
   modeles ouverts locaux et s'ecarte du protocole de Stanford, qui evalue du texte genere avec
   chaine de pensee. En echange il supprime le bruit d'echantillonnage, divise le cout par mille et
   donne la decomposition de variance. L'etape A11 le valide empiriquement (ecart inferieur a 0,03),
   mais c'est un choix de fond, pas un detail d'implementation.

7. **Le plan (fidelite, IDP) est il la bonne figure 1 ?** Ma conviction est que la contribution du
   projet n'est pas un chiffre de fidelite plus eleve que Stanford, mais la demonstration qu'il
   existe un compromis entre fidelite et diversite, et qu'on peut se deplacer dessus, avec C1 (mode
   de la population) et C1b (tirage dans la marginale) comme bornes.

8. **Faut il pre enregistrer maintenant ?** Le pre enregistrement du protocole voie A avant le
   premier run coute une journee et vaut beaucoup en credibilite pour une equipe sans antecedent.
   Stanford a pre enregistre ses metriques et ses analyses principales. Y a t il une raison de ne
   pas le faire ?

9. **Existe t il une variante de fine tuning qui echappe au verdict de Stanford ?** Ils ont mesure
   0,79 contre 0,84, avec un fine tuning oriente **precision**. Un adaptateur entraine a
   **preserver la variance** (perte penalisant l'ecart entre distribution simulee et distribution
   observee) ne tombe pas sous ce verdict et serait aligne avec la contribution visee. Est ce une
   piste, ou une complication inutile ?

10. **Confirmation de la reference.** `CONTEXTE.md` pointe vers `arxiv.org/html/2603.28066v1`, qui
    ne correspond pas. Le papier est `arXiv:2411.10109`, version 3 du 28 juin 2026, retitre en
    *LLM Agents Grounded in Self-Reports Enable General-Purpose Simulation of Individuals*, et le
    chiffre de 85 pour cent cite dans `CONTEXTE.md` est perime (c'est 83 / 82 / 86 contre 74 et 71).
    Est ce bien ce papier que Simon visait ?
