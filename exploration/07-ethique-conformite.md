# 07. Ethique et conformite, version proportionnee

Agent 7. Date : 2 septembre 2026.

Consigne appliquee : ne pas produire un traite de conformite. A ce stade, aucun humain n'est
recrute et le travail porte sur des donnees publiques. Le RGPD n'est donc pas le sujet. Le sujet,
c'est la licence des jeux de donnees et le trajet des donnees vers les API de modeles.

Trois horizons, trois checklists. Une action par ligne, un declencheur temporel par ligne.
Le formulaire de consentement est en annexe, pret a l'emploi.

---

## Le calibrage en une page

**Ce qui NE s'applique PAS a l'horizon 1**

- Le RGPD, pour les fichiers d'enquete publics diffuses anonymises. Le considerant 26 du RGPD
  ecrit que les principes de protection des donnees ne s'appliquent pas aux informations anonymes.
  [CONFIRME] https://www.privacy-regulation.eu/fr/r26.htm
  Consequence : pas de registre de traitement, pas d'analyse d'impact, pas de base legale a
  documenter, pas de DPO, tant qu'aucune personne n'est interrogee.
- Le comite d'ethique. Une approbation IRB ou CER porte sur une recherche impliquant des
  personnes. L'analyse secondaire de fichiers publics deja anonymises n'en releve pas en pratique.
  [PROBABLE] raisonnement : le declencheur reglementaire est l'interaction avec un sujet ou l'acces
  a des informations privees identifiables, ce qui n'est pas le cas ici. Voir la definition de
  l'engagement dans la recherche du MIT en horizon 3.
- La loi Jarde et le circuit CPP. Elle encadre les recherches impliquant la personne humaine et
  ne couvre pas les sciences humaines et sociales, raison pour laquelle les etablissements ont cree
  des comites d'ethique de la recherche ad hoc. [CONFIRME]
  https://www.univ-lorraine.fr/luniversite-de-lorraine/ethique-deontologie-integrite-scientifique/ethique/la-loi-jarde-et-son-application/

**Ce qui s'applique vraiment a l'horizon 1**

1. Le contrat de licence de chaque jeu de donnees. C'est un contrat, pas une reglementation :
   il n'y a pas de dispense pour la recherche, il n'y a que ce qui est signe au telechargement.
2. Le trajet des donnees vers une API de modele. C'est le risque numero un, developpe plus bas.
3. L'interdiction de reidentifier, presente dans la quasi totalite de ces licences.

---

## HORIZON 1, maintenant : donnees publiques, aucun humain recrute

### Checklist

| # | Action | Declencheur |
|---|--------|-------------|
| 1.1 | Archiver le texte exact de la licence acceptee, avec la date, dans `donnees/licences/<jeu>.md` | Au moment de chaque telechargement, jamais apres |
| 1.2 | Verifier avant tout usage commercial demontre si la licence est non lucrative (ESS, WVS) | Avant la premiere demo commerciale, pas avant |
| 1.3 | Ne jamais committer un fichier de microdonnees dans le depot git, meme public. Le depot est une redistribution | Des le premier `git add` de donnees, donc maintenant |
| 1.4 | Trancher local contre API pour tout traitement qui voit des lignes de microdonnees | Avant la premiere ligne de code de pipeline |
| 1.5 | Si une API est utilisee malgre tout, verifier la clause d'entrainement du palier exact utilise, pas du produit en general | Avant la premiere cle d'API creee |
| 1.6 | Interdire l'usage de claude.ai, ChatGPT grand public ou Le Chat pour manipuler des microdonnees | Immediatement, c'est une regle d'hygiene, pas un chantier |
| 1.7 | Ecrire noir sur blanc dans le README que le projet ne cherche pas a reidentifier de repondants | Avant le premier partage du depot avec Simon ou le MIT |
| 1.8 | Ne pas publier de persona qui reproduit une ligne de microdonnees complete | Au moment de la premiere sortie de personas, pas au moment de la publication |

### 1.A Ce que disent reellement les licences

| Jeu | Enregistrement | Redistribution | Usage commercial | Reidentification |
|-----|----------------|----------------|------------------|------------------|
| GSS / NORC | Compte requis sur le Data Explorer | Interdite : aucune partie du contenu ne peut etre reproduite, stockee ou transmise sans accord ecrit de NORC | Non traite explicitement dans les CGU du site | Non traite dans les CGU generales, traite dans les contrats de donnees sensibles |
| GSS via ICPSR | Compte, souvent adhesion institutionnelle | Interdite sans accord ecrit d'ICPSR | Non traite, mais l'usage est cadre comme statistique | Interdite explicitement |
| World Values Survey | Obligatoire | Interdite, licence dite de non redistribution | Reserve a un usage non lucratif | Non trouve en texte officiel |
| European Social Survey | Obligatoire | Autorisee sous CC BY-NC-SA 4.0, donc partage a l'identique | Interdit, la clause NC est explicite | Non trouve en texte officiel |
| Pew American Trends Panel | Compte Pew, CGU propres a l'ATP | Limitee a des extraits | Autorise sous conditions, licence non transferable et non sous licenciable | Interdite explicitement |
| Panels academiques via ICPSR | Compte, parfois accord institutionnel | Interdite sans accord ecrit | Usage cadre comme statistique et agrege | Interdite explicitement |

Sources :
- GSS, CGU NORC : reproduction, stockage et transmission interdits sans accord ecrit, citation
  obligatoire. [CONFIRME] https://gss.norc.org/us/en/gss/terms-and-conditions.html
- GSS, fichiers geographiques et sensibles sous contrat separe avec NORC. [CONFIRME]
  https://gss.norc.org/content/dam/gss/get-documentation/pdf/other/ObtainingGSSSensitiveDataFiles.pdf
- ICPSR, responsible use statement : utiliser les jeux de donnees uniquement pour l'analyse
  statistique et le rapport d'informations agregees, et non pour l'investigation d'individus ou
  d'organisations specifiques, sauf autorisation ecrite d'ICPSR ; ne faire aucun usage de l'identite
  d'une personne decouverte par inadvertance et en avertir ICPSR ; ne pas redistribuer le materiel
  telecharge sans accord ecrit. [CONFIRME]
  https://www.icpsr.umich.edu/web/ICPSR/studies/42/terms
  et https://www.icpsr.umich.edu/sites/icpsr/about/policies/redistribution
- ESS, donnees sous CC BY-NC-SA 4.0 et documentation sous CC BY-SA 4.0, disponibles sans
  restriction pour des usages non lucratifs. [CONFIRME]
  https://www.re3data.org/repository/r3d100010233
- WVS, licence de non redistribution, usage non lucratif, citation obligatoire, enregistrement
  obligatoire. [CONFIRME par sources secondaires convergentes, l'editeur de donnees de l'American
  Economic Association note qu'il n'existe pas de page unique de conditions d'usage referencable
  chez WVS] https://aeadataeditor.github.io/posts/2024-04-29-use-and-reuse-of-data
- Pew, conditions generales : engagement a ne pas chercher a determiner l'identite des repondants
  ni a en deduire des informations, licence non sous licenciable et non transferable, redistribution
  limitee a des extraits, l'American Trends Panel etant regi par ses propres conditions.
  [CONFIRME] https://www.pewresearch.org/about/terms-and-conditions/

**Les deux clauses qui mordent vraiment sur ce projet**

- La clause **non lucrative** de l'ESS et du WVS. Elle ne gene pas la recherche, elle gene la demo
  commerciale du pitch decrit dans CONTEXTE.md. Le jour ou une etude payante s'appuie sur des
  resultats ESS ou WVS, il faut une autre source ou une autorisation. Le GSS et le Pew ATP sont
  plus permissifs sur ce point. [PROBABLE] lecture directe des textes ci dessus.
- La clause ICPSR d'usage **agrege uniquement**. Elle est en tension frontale avec la these du
  projet, qui est justement de travailler au niveau individuel pour restituer la variance. Ce n'est
  pas redhibitoire, parce que la clause vise l'investigation d'individus reels identifies, pas la
  modelisation statistique au niveau de l'enregistrement. Mais c'est le point sur lequel un
  reviewer ou un data steward posera une question. [HYPOTHESE, lecture non validee par un juriste]

### 1.B Le point sous estime : envoyer des donnees sous licence academique vers une API commerciale

C'est le risque numero un a cet horizon, et il n'est pas theorique.

**Question 1 : est ce une redistribution ?**
Les licences interdisent la redistribution a d'autres individus, institutions ou organisations.
Un fournisseur d'API est une organisation, et l'envoi d'une ligne de microdonnees dans un prompt
est bien une transmission a cette organisation. La formulation Pew est la plus explicite :
licence non transferable et non sous licenciable. [PROBABLE]
Je n'ai trouve aucune decision, aucune position publiee d'ICPSR, de NORC ou de Pew, ni aucune
jurisprudence tranchant si un appel d'API constitue une redistribution au sens de ces contrats.
[CONFIRME comme absence de source, apres recherche]
Autrement dit : personne ne peut affirmer que c'est autorise, et personne ne peut affirmer que
c'est interdit. Dans un projet qui vise une publication avec le MIT, l'incertitude elle meme est
le probleme, parce qu'elle se transforme en question de reviewer.

**Question 2 : le fournisseur s'entraine t il sur ce qui est envoye ?**
La reponse depend du **palier exact**, pas du fournisseur. C'est le piege, et il tombe pile sur la
contrainte BUDGET ZERO, qui pousse vers les paliers gratuits, c'est a dire vers ceux qui
s'entrainent.

| Acces | Entrainement sur les entrees | Retention |
|-------|------------------------------|-----------|
| API Anthropic, conditions commerciales | Non par defaut | 30 jours |
| claude.ai Free, Pro, Max | **Oui par defaut depuis le 28 aout 2025**, sauf desactivation de "Help improve Claude" | 5 ans si l'entrainement est actif |
| API OpenAI | Non par defaut depuis le 1er mars 2023, opt in requis | 30 jours de logs d'abus, option zero retention |
| API Gemini, palier gratuit | **Oui**, les contenus peuvent servir a ameliorer les produits, avec revue humaine possible | Non verifie |
| API Gemini, palier payant | Non | Non verifie |
| Mistral La Plateforme, palier gratuit Experiment | **Oui par defaut**, desactivation manuelle dans la console | Non verifie |
| Modele ouvert execute en local | Sans objet, rien ne sort de la machine | Sans objet |

Sources :
- Anthropic, produits commerciaux dont l'API : pas d'entrainement par defaut sur les entrees et
  sorties. [CONFIRME]
  https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training
- Anthropic, mise a jour des conditions grand public du 28 aout 2025 : Free, Pro et Max choisissent
  si leurs conversations entrainent Claude, le reglage etant actif par defaut, avec une retention
  portee a 5 ans. [CONFIRME] https://www.anthropic.com/news/updates-to-our-consumer-terms
- OpenAI, controles de donnees de la plateforme. [CONFIRME]
  https://developers.openai.com/api/docs/guides/your-data
- Gemini palier gratuit et Mistral palier gratuit. [PROBABLE, sources secondaires convergentes,
  pages officielles non ouvertes lors de cette recherche]

**Ce que cela implique concretement**

1. Interdire absolument le passage de microdonnees d'enquete par une interface grand public
   (claude.ai, ChatGPT, Le Chat). C'est le scenario le plus probable d'accident, parce que c'est
   le geste le plus naturel quand on explore un fichier.
2. Le choix local contre API n'est donc pas seulement un choix de cout, c'est le seul choix qui
   supprime les deux questions d'un coup. Un modele ouvert execute en local ne transmet rien, donc
   ni redistribution, ni entrainement tiers, ni retention. Il est en plus le seul compatible avec
   BUDGET ZERO. [PROBABLE, raisonnement]
3. Si une API est indispensable pour la qualite du modele, la regle de proportionnalite est :
   envoyer des **derives non identifiants** plutot que des lignes brutes. Un persona reecrit en
   texte libre a partir d'une ligne GSS, sans identifiant d'enregistrement et sans la combinaison
   complete des variables rares, n'est pas la ligne de microdonnees. [HYPOTHESE, c'est une lecture
   defendable mais non validee]
4. Documenter le choix dans le depot, avec la date et la version des conditions consultees. Si la
   question est posee un jour, la trace vaut plus que l'argument.

### 1.C Reconstruire un individu a partir de donnees anonymisees, c'est une reidentification

Le projet consiste a fabriquer, a partir d'une ligne d'enquete, un agent qui repond comme la
personne derriere cette ligne. C'est exactement la definition d'un travail au niveau individuel
sur des donnees promises anonymes aux repondants.

- ICPSR l'interdit en toutes lettres : toute identification ou divulgation intentionnelle d'une
  personne viole les assurances de confidentialite donnees aux fournisseurs d'information.
  [CONFIRME] https://www.icpsr.umich.edu/web/NAHDAP/cms/2049
- Pew l'interdit egalement. [CONFIRME] lien ci dessus.
- L'ESS previent ses propres repondants qu'il est peu probable mais possible que la citoyennete,
  l'age, le pays de naissance, la profession, l'ascendance et la region se combinent d'une facon
  qui les identifie. [CONFIRME]
  https://europeansocialsurvey.org/about/privacy-and-data-protection/survey-participants

**Pourquoi l'eviter meme quand c'est techniquement possible.** Trois raisons, dans l'ordre ou elles
mordent :

1. Le RGPD revient par la fenetre. Le considerant 26 ne protege que si personne, y compris le
   responsable de traitement, ne peut reidentifier par des moyens raisonnables. Un pipeline qui
   reconstruit un individu est precisement un moyen raisonnable. Une donnee anonyme reidentifiee
   redevient une donnee personnelle, et tout le regime s'applique retroactivement. [PROBABLE]
2. La licence, elle, s'applique tout de suite et sans discussion. La sanction n'est pas une amende,
   c'est la revocation de l'acces, ce qui tuerait le projet.
3. La publication devient indefendable. Un papier qui montre qu'on sait reconstruire des individus
   a partir du GSS est un papier sur une faille de confidentialite du GSS, pas un papier sur la
   simulation de populations. Ce n'est pas le papier vise.

**La regle operationnelle qui evite tout ce debat**, et qui est aussi ce que Stanford a fait :
- Les agents construits sur donnees publiques sont des agents **demographiques**, tires d'une
  distribution, pas des reconstructions d'un repondant nomme. La banque d'agents ouverte de
  l'equipe Stanford est batie sur le GSS et est decrite comme demographique, pas comme individuelle.
  [CONFIRME] https://github.com/joonspk-research/genagents
- On ne conserve jamais, dans les artefacts publies, la cle qui relie un persona a un enregistrement
  source. On peut la conserver en interne pour l'evaluation, dans un fichier hors depot.
- On ne publie jamais un persona qui contient la combinaison complete des variables rares d'un
  enregistrement.

---

## HORIZON 2, plus tard : si des entretiens ont lieu

Rien de ce qui suit n'est a faire aujourd'hui. C'est a declencher le jour ou une premiere personne
est sollicitee, et une partie doit etre prete **avant** ce jour la.

### Checklist

| # | Action | Declencheur |
|---|--------|-------------|
| 2.1 | Choisir la base legale : consentement explicite, article 6.1.a et 9.2.a du RGPD | Avant le premier contact avec un participant potentiel |
| 2.2 | Faire signer le formulaire en annexe, version datee et versionnee | Avant l'enregistrement, jamais pendant ni apres |
| 2.3 | Pseudonymiser a la transcription : remplacement programmatique des noms propres par des pseudonymes stables | Dans les 24 h suivant l'entretien |
| 2.4 | Tenir un registre a deux colonnes, pseudonyme et personne, dans un fichier chiffre hors depot | Des le premier entretien |
| 2.5 | Definir la duree de conservation et l'inscrire dans le formulaire, pas ailleurs | Avant le premier entretien |
| 2.6 | Mettre en place la procedure de retrait, y compris la destruction du persona derive, avant d'en avoir besoin | Avant le premier entretien |
| 2.7 | Ne jamais envoyer un verbatim d'entretien vers un palier d'API qui s'entraine | Des la premiere transcription |
| 2.8 | Prevoir un canal pour informer les participants d'un changement majeur de capacite des modeles | A la fin de la phase de collecte |

Base legale, en une phrase : les entretiens du projet portent frontalement sur des opinions
politiques, qui sont des donnees sensibles au sens de l'article 9 du RGPD, et pour un projet non
adosse a un etablissement public le consentement explicite est en pratique la seule voie
praticable. [PROBABLE, raisonnement juridique non valide par un juriste]

### 2.A Anonymisation contre pseudonymisation, et l'effacement d'un jumeau derive

**La distinction, en deux lignes.** Une donnee pseudonymisee reste une donnee personnelle et reste
dans le champ du RGPD, parce qu'une table de correspondance permet de revenir a la personne. Une
donnee anonymisee en sort, a condition que la reidentification soit impossible par des moyens
raisonnables pour quiconque, y compris pour celui qui detient les donnees. [CONFIRME]
https://www.privacy-regulation.eu/fr/r26.htm

Un transcript d'entretien de deux heures n'est **pas** anonymisable. Stanford l'ecrit lui meme :
les donnees collectees, en particulier les donnees qualitatives d'entretien, sont difficiles a
anonymiser et posent un risque du fait de la nature potentiellement sensible du contenu.
[CONFIRME] materiel supplementaire de https://arxiv.org/abs/2411.10109
Ils ne se contentent pas de le dire, ils le font signer : les participants sont informes que malgre
le remplacement programmatique des noms par des pseudonymes, il reste possible que des elements
comme les details demographiques, l'histoire personnelle et les opinions politiques soient
divulgues par inadvertance, et ils acceptent que l'anonymat complet reste difficile a atteindre.
[CONFIRME] meme source.

**La vraie question : effacer les sources suffit il quand un persona a ete derive ?**

Non, et c'est un point que la litterature RGPD ne traite quasiment pas, parce qu'elle a ete ecrite
pour des bases de donnees, pas pour des artefacts derives.

Un jumeau numerique se decompose en au moins quatre objets, et le droit a l'effacement doit les
viser tous les quatre :

1. **L'enregistrement audio.** Effacement trivial.
2. **La transcription.** Effacement trivial.
3. **Le persona ou la memoire de l'agent**, c'est a dire le texte structure derive de la
   transcription et injecte dans le prompt. C'est ici que ca coince. Cet objet est une **donnee
   personnelle derivee** : il decrit une personne identifiable a l'echelle de son entourage, meme
   sans son nom. Effacer la transcription et garder le persona, c'est garder la donnee personnelle
   en ayant detruit la preuve de son origine. C'est la pire configuration possible, parce qu'elle
   donne l'illusion de la conformite. **Regle : le persona s'efface avec la source, pas apres.**
   [PROBABLE, raisonnement]
4. **Les traces d'usage** : sorties deja generees par l'agent, resultats de simulation deja
   agreges, et surtout **poids d'un modele affine sur les transcripts**. Un modele affine ne se
   desapprend pas ligne par ligne. Si un jour le projet passe du prompting au fine tuning, le droit
   au retrait devient impossible a honorer sans reentrainer le modele complet. **Consequence
   pratique : tant que le retrait est promis aux participants, rester sur du prompting avec
   contexte injecte, et ne pas affiner sur les transcripts.** C'est une contrainte d'architecture,
   pas une contrainte juridique, et elle doit etre decidee avant le premier entretien.
   [PROBABLE, raisonnement, c'est la consequence la plus importante de ce document pour la
   conception technique]

Sur les resultats deja publies : ils ne sont pas rappelables, et il est honnete de l'ecrire dans le
formulaire plutot que de promettre un effacement total. Stanford le formule en termes de moyens :
les demandes de suppression seront honorees pendant les 25 premieres annees suivant la fin de
l'etude, dans la mesure du possible. [CONFIRME] materiel supplementaire du papier.
Le formulaire en annexe reprend cette logique, avec une duree ramenee a l'echelle du projet.

---

## HORIZON 3, publication et usages sensibles

### Checklist

| # | Action | Declencheur |
|---|--------|-------------|
| 3.1 | Poser a Simon la question de l'instance d'approbation, IRB americain ou CER francais | Des la premiere discussion serieuse de publication conjointe, donc maintenant |
| 3.2 | Obtenir l'approbation ethique **avant** la premiere sollicitation d'un participant | Au plus tard 3 mois avant le premier entretien |
| 3.3 | Verifier la politique ethique de la revue ou conference visee avant de choisir la cible | Avant de fixer la cible de soumission |
| 3.4 | Rediger la charte d'usage du projet, section politique comprise | Avant la premiere demo a un tiers exterieur au projet |
| 3.5 | Decider du regime de diffusion des agents, ouvert agrege contre restreint individuel | Avant la mise en ligne de tout artefact |
| 3.6 | Ecrire le domaine de validite et l'afficher a cote de chaque resultat | Avant la premiere presentation au MIT |

### 3.A Quelle instance, et a partir de quand

Le point pratique d'abord, parce que c'est celui qui coute cher si on le rate : **une approbation
obtenue apres la collecte ne vaut rien.** La reglementation federale americaine ne prevoit aucune
approbation retroactive d'une recherche deja conduite. [CONFIRME, position standard des bureaux
IRB americains, par exemple https://www.skidmore.edu/irb/faq.php]
Concretement, si dix entretiens sont menes puis qu'une approbation est demandee, ces dix entretiens
sont inutilisables pour une publication qui exige une declaration ethique. Il faut recommencer.

Qui approuve, selon la configuration :

- **Si le MIT est co auteur ou co porteur.** Le comite competent est le COUHES, Committee on the
  Use of Humans as Experimental Subjects. Le MIT est considere engage dans la recherche des lors
  que ses employes ou agents obtiennent des donnees par interaction avec les sujets, des
  informations privees identifiables, ou le consentement eclaire des sujets. [CONFIRME]
  https://couhes.mit.edu/researchers/couhes-101
- **Si Amir mene les entretiens sans affiliation institutionnelle.** C'est le cas de figure reel
  aujourd'hui, et c'est la que le montage coince. Le MIT indique que pour un collaborateur non
  affilie a une institution, cet individu doit obtenir une nomination MIT pour que le COUHES puisse
  examiner et superviser ses activites de recherche ; et que si l'institution du collaborateur n'a
  pas d'IRB, le collaborateur doit recourir aux services d'un IRB commercial. [CONFIRME]
  https://couhes.mit.edu/guidelines/research-involving-non-mit-collaborators
  Traduction : soit une affiliation, soit un IRB commercial payant. Les deux ont un delai et l'un
  des deux a un cout, ce qui percute la contrainte BUDGET ZERO. C'est une question a poser a Simon
  maintenant, pas au moment des entretiens.
- **Cote francais.** La loi Jarde ne couvre pas les sciences humaines et sociales, et les
  etablissements ont cree des comites d'ethique de la recherche pour evaluer les projets hors RIPH.
  [CONFIRME] https://www.univ-lorraine.fr/luniversite-de-lorraine/ethique-deontologie-integrite-scientifique/ethique/la-loi-jarde-et-son-application/
  Un CER francais suppose un rattachement a un etablissement. Sans rattachement, il n'y a pas de
  guichet naturel.

**Le calendrier realiste.** L'equipe Stanford ecrit avoir travaille avec son IRB pendant plus de
six mois pour s'assurer que les participants conservent leur autonomie et donnent un consentement
eclaire. [CONFIRME] materiel supplementaire de https://arxiv.org/abs/2411.10109
C'est le chiffre a retenir : sur ce protocole precis, la construction d'un agent qui imite une
personne, six mois d'echanges ont ete necessaires. Trois mois est un plancher optimiste, pas une
cible confortable.

**Cote revue.** Beaucoup de revues attendent soit une approbation d'un comite d'ethique, soit une
explication claire de ce qui a ete fait quand un tel comite n'existe pas. [CONFIRME, pratique
editoriale standard, verifiee sur plusieurs sources secondaires, aucune politique de revue precise
ouverte lors de cette recherche] La consequence est simple : la declaration ethique doit exister
avant la soumission, et elle doit dire quelque chose de verifiable.

### 3.B Le use case politique : garde fous concrets

Le cadrage des auteurs de Stanford, a reprendre tel quel parce qu'il est deja public et defendable.
Ils identifient dans leur note de politique publique :
- le risque de **surconfiance** quand la precision de la simulation est faible, et la consigne que
  les decideurs ne doivent pas appliquer les agents generatifs au dela de l'eventail d'applications
  qui a ete valide ;
- le risque de **fuite** des donnees d'entretien, sensibles ;
- la **captation de l'apparence** des individus, ces agents pouvant repliquer de facon credible les
  reponses d'une personne ;
- le **prejudice reputationnel** si quelqu'un manipule les reponses d'un agent pour attribuer
  faussement des propos diffamatoires a une personne dont les donnees ont servi ;
- les questions ouvertes de l'agent simulant une personne decedee, de la gestion du consentement,
  et de l'usage frauduleux ;
- la recommandation d'etablir des **regles de ligne rouge** sur ce que les agents peuvent ou ne
  peuvent pas simuler.
[CONFIRME] https://hai.stanford.edu/assets/files/hai-policy-brief-simulating-human-behavior-with-ai-agents.pdf

Leurs garde fous effectifs : refus de diffuser publiquement les agents, acces API restreint a la
recherche, systeme a deux niveaux avec acces ouvert aux reponses agregees sur taches fixes et acces
restreint aux reponses individuelles sur taches ouvertes apres examen, audits d'usage, options de
retrait des participants, et accords d'usage non commercial, sur le modele des banques de genomes.
[CONFIRME] https://arxiv.org/abs/2411.10109 version 1, section Research Access for the Agent Bank.

**La charte a adopter pour popsim, formulee en trois listes.**

Ce qu'on accepte de faire :
- Estimer la distribution des reponses d'une population simulee a un message, au niveau agrege.
- Mesurer l'heterogeneite d'un effet entre sous populations, pour identifier les groupes pour
  lesquels une intervention ne fonctionne pas. C'est d'ailleurs l'usage que les auteurs mettent en
  avant. [CONFIRME] meme source.
- Pretester des libelles de questions et des designs d'enquete avant terrain reel.
- Publier les taux de precision par sous groupe, y compris ceux qui sont mauvais.

Ce qu'on refuse :
- Optimiser un message de persuasion contre une personne identifiable ou un micro segment reduit
  a quelques individus. La ligne est la difference entre comprendre une population et cibler une
  personne.
- Simuler une personnalite publique nommee, un candidat, un elu.
- Produire du contenu presente comme provenant d'une personne reelle, meme consentante.
- Livrer a un client un classement de messages persuasifs pour une campagne reelle en cours.
- Vendre ou ceder des reponses d'agents au niveau individuel.

Ce qu'on publie :
- Les resultats agreges, la methode, les prompts, le code, les metriques de validation avec leurs
  intervalles, et le domaine de validite explicite.
- Un enonce court et visible : ces agents predisent des reponses d'enquete, pas des comportements
  reels, et pas au dela des domaines evalues.

Ce qu'on ne publie pas :
- Les transcripts d'entretien, meme pseudonymises.
- Les fichiers de persona qui correspondent a une personne reelle.
- Les reponses individuelles d'agents sur des taches ouvertes.
- La cle qui relie un persona a un enregistrement source.

### 3.C Les autres risques, et la parade

- **Usurpation d'identite d'une personne simulee.** Un agent qui imite bien produit des propos
  credibles attribuables a la personne. Parade : ne jamais exposer un agent sous le nom reel de la
  personne, ne jamais offrir de generation libre non contrainte sur un agent individuel, journaliser
  toute requete adressee a un agent individuel. C'est le role de l'audit log propose par Stanford,
  qui permet a la personne de voir ce que son agent fait et d'exercer un controle dans la duree,
  une permission pouvant etre accordee un jour et retiree un mois plus tard. [CONFIRME] note HAI.
- **Publication de personas identifiables.** Parade : regle 1.8 et 3.B ci dessus, plus une relecture
  humaine de tout artefact publie, pas seulement un filtre automatique.
- **Usage clinique sans validation.** Le resultat de reference porte sur le GSS, le Big Five et des
  jeux economiques. Rien dans cette validation ne couvre un usage diagnostique ou therapeutique.
  Le use case recherche clinique figure dans CONTEXTE.md : il doit etre explicitement borne a la
  simulation de participants pour du design d'etude, jamais a la production d'un jugement sur une
  personne reelle, et jamais presente comme valide tant qu'aucune evaluation clinique n'a ete
  conduite. [PROBABLE, raisonnement fonde sur le perimetre d'evaluation du papier]

---

## Annexe. Formulaire de consentement eclaire, pret a l'emploi

A utiliser tel quel a l'horizon 2. A dater et versionner. A faire signer avant tout enregistrement.
Ce texte est redige pour ce projet precis. Il n'a pas ete relu par un juriste.

---

### FORMULAIRE DE CONSENTEMENT ECLAIRE

**Projet popsim, simulation d'attitudes par agents conversationnels**
Version 1.0. Date : ......................
Responsable du projet : Amir Kellous Idhoum. Contact : ......................
Encadrement scientifique : ......................

#### 1. Objet de l'etude

Cette etude cherche a savoir dans quelle mesure un modele de langage, alimente par un entretien
approfondi avec vous, peut anticiper les reponses que vous donneriez a des questionnaires d'opinion
et a des exercices de sciences sociales. Concretement, nous allons construire un programme
informatique qui essaie de repondre a votre place, puis nous comparerons ses reponses aux votres.

#### 2. Ce qui vous est demande

- Un entretien d'environ deux heures, en face a face ou a distance, conduit par un chercheur ou par
  un systeme d'entretien automatise. Vous parlez de votre parcours, de votre vie quotidienne, de vos
  opinions sur des sujets de societe.
- Le remplissage de questionnaires apres l'entretien.
- Eventuellement, un second passage des memes questionnaires environ deux semaines plus tard.

Vous pouvez refuser de repondre a n'importe quelle question, sans avoir a vous justifier, et
demander l'arret de l'entretien a tout moment.

#### 3. Enregistrement et transcription

- [ ] J'accepte que l'entretien soit enregistre en audio.
- [ ] J'accepte que cet enregistrement soit transcrit en texte.

La transcription est pseudonymisee : votre nom et les noms des personnes que vous citez sont
remplaces par des pseudonymes stables. Les lieux precis sont generalises.

Nous devons vous dire honnetement ceci : **un entretien de deux heures ne peut pas etre rendu
totalement anonyme.** L'ensemble forme par votre parcours, votre situation, votre region et vos
opinions peut, en theorie, permettre a quelqu'un qui vous connait de vous reconnaitre. Nous prenons
des mesures pour reduire ce risque, nous ne pouvons pas l'annuler.

#### 4. Creation d'un agent qui vous imite

- [ ] J'accepte qu'un programme informatique soit construit a partir de mon entretien, dans le but
      de simuler la facon dont je repondrais a des questions d'enquete ou dont je me comporterais
      dans certaines situations.

Ce que cet agent est : un modele de langage auquel on fournit le contenu de votre entretien et a qui
l'on demande de repondre comme vous le feriez.
Ce que cet agent n'est pas : ce n'est pas vous, il n'a pas acces a votre vie apres l'entretien, il
se trompera regulierement, et ses reponses ne vous engagent pas.

Vous devez savoir que les modeles utilises deviennent plus performants avec le temps, et qu'ils
pourraient a l'avenir deduire de votre entretien plus d'informations qu'aujourd'hui. Si un
changement significatif de ce type survient, nous nous engageons a vous en informer.

#### 5. Ce que nous nous interdisons

- Nous ne diffuserons jamais votre entretien, ni sa transcription, en dehors de l'equipe de
  recherche.
- Nous n'exposerons jamais l'agent construit a partir de votre entretien sous votre nom.
- Nous ne permettrons jamais a un tiers de faire tenir a cet agent des propos presentes comme les
  votres.
- Nous ne vendrons ni ne cederons vos donnees ni l'agent construit a partir d'elles.
- Nous n'utiliserons pas vos donnees a des fins de ciblage publicitaire ou de campagne electorale.

#### 6. Qui aura acces

- [ ] J'accepte que l'equipe de recherche utilise mes donnees et l'agent construit a partir d'elles.
- [ ] J'accepte, en plus, que des chercheurs exterieurs y accedent, uniquement a des fins
      academiques, apres examen de leur demande par l'equipe. (Cette case est facultative et son
      refus n'a aucune consequence sur votre participation.)

Vos donnees peuvent transiter par des services informatiques tiers necessaires au traitement. Nous
nous engageons a n'utiliser que des services dont les conditions excluent l'utilisation de vos
donnees pour entrainer leurs propres modeles.

#### 7. Duree de conservation

- Enregistrement audio : detruit apres transcription, et au plus tard ...... mois apres l'entretien.
- Transcription pseudonymisee et agent derive : conserves ...... ans a compter de la fin de l'etude,
  puis detruits.
- Table de correspondance entre votre identite et votre pseudonyme : conservee separement, sous
  protection, et detruite en meme temps que la transcription.

#### 8. Retrait

Vous pouvez retirer votre consentement a tout moment, y compris apres la fin de votre participation,
sans avoir a vous justifier, par simple message a l'adresse indiquee en tete de ce document.

En cas de retrait, nous supprimons, dans un delai de 30 jours :
- l'enregistrement audio,
- la transcription,
- **l'agent construit a partir de votre entretien, ainsi que tous les fichiers derives de celui ci**,
- la table de correspondance vous concernant.

Nous devons vous signaler deux limites, et nous preferons vous les dire plutot que de vous promettre
l'impossible :
1. Les resultats deja publies sous forme agregee ne peuvent pas etre retires. Ils ne permettent pas
   de remonter a vous.
2. Si des chercheurs exterieurs ont deja obtenu un acces au titre du point 6, nous leur transmettons
   votre demande de suppression et nous en assurons le suivi, dans la limite de nos moyens.

Nous nous engageons a honorer les demandes de suppression pendant ...... ans a compter de la fin de
l'etude.

#### 9. Publication

- [ ] J'accepte que les resultats de l'etude, sous forme agregee et anonyme, soient publies dans une
      revue scientifique, une conference ou un depot ouvert.
- [ ] J'accepte que des extraits courts et pseudonymises de mon entretien puissent etre cites dans
      une publication. (Facultatif.)

Aucune publication ne comportera votre nom.

#### 10. Vos droits

Conformement au reglement general sur la protection des donnees, vous disposez d'un droit d'acces,
de rectification, d'effacement, de limitation et d'opposition sur les donnees qui vous concernent.
La base legale de ce traitement est votre consentement explicite. Vous pouvez introduire une
reclamation aupres de la CNIL.

#### 11. Signature

J'ai lu ce document, j'ai eu la possibilite de poser des questions, et j'y ai obtenu des reponses.
Je participe volontairement.

Nom : ......................
Date : ......................
Signature : ......................

Un exemplaire signe vous est remis.

---

## Ce que je n'ai pas pu verifier

- **Le texte officiel des conditions d'usage du World Values Survey.** Il n'existe pas de page
  publique unique et referencable ; les conditions s'affichent au telechargement apres inscription.
  L'editeur de donnees de l'American Economic Association fait le meme constat. Il faut donc
  telecharger un fichier et capturer l'ecran des conditions pour disposer d'une preuve.
- **Le texte officiel des conditions d'usage de l'European Social Survey.** La licence
  CC BY-NC-SA 4.0 est confirmee par le registre re3data, mais je n'ai pas ouvert de page ESS
  enoncant une clause de non reidentification.
- **Les conditions propres a l'American Trends Panel de Pew.** Les conditions generales de Pew
  indiquent explicitement que l'ATP est regi par ses propres conditions, que je n'ai pas pu ouvrir.
  Le contenu extrait des conditions generales l'a ete par fragments de 125 caracteres, ce qui suffit
  a identifier les clauses mais pas a les citer integralement.
- **Les pages officielles de Google et de Mistral sur l'usage des donnees des paliers gratuits.**
  Les sources consultees sont secondaires et convergentes, mais ce sont des sources secondaires. A
  reverifier sur les pages officielles avant toute decision, car ces politiques changent.
- **La position officielle de NORC, d'ICPSR ou de Pew sur la question de savoir si un appel d'API
  constitue une redistribution.** Aucune position publiee, aucune jurisprudence, aucun avis. Le
  vide est reel, ce n'est pas un defaut de recherche.
- **La politique ethique precise de la revue ou conference visee.** Aucune cible n'est fixee dans
  CONTEXTE.md, donc aucune politique precise n'a pu etre verifiee.
- **La version courante du papier de Stanford a change de titre.** La version publique la plus
  recente sur arXiv 2411.10109 s'intitule "LLM Agents Grounded in Self-Reports Enable
  General-Purpose Simulation of Individuals" et sa section sur l'acces a la banque d'agents a ete
  reduite. Les citations sur les garde fous proviennent donc de la version 1 de novembre 2024 et de
  la note de politique publique HAI de mai 2025. Ce n'est pas un probleme de fiabilite, mais il faut
  citer la bonne version.
- **Tout le volet juridique de ce document n'a pas ete relu par un juriste.** Les lectures de clause
  sont des lectures de bon sens, pas des avis.

## Questions ouvertes pour Simon

1. **Le rattachement institutionnel.** Sans affiliation, il n'y a ni COUHES ni CER accessible, et un
   IRB commercial coute de l'argent que le projet n'a pas. Une affiliation, meme minimale et meme
   temporaire, cote MIT ou cote francais, est ce envisageable, et sous quel delai ? C'est la
   question la plus structurante de ce document, parce qu'elle conditionne toute la phase
   d'entretiens.
2. **Qui porte l'approbation ethique dans une publication conjointe MIT ?** Si le MIT est engage,
   le COUHES couvre t il l'ensemble du protocole, y compris les entretiens menes en France, ou
   faut il un double circuit ?
3. **La contrainte non lucrative de l'ESS et du WVS.** Elle est neutre pour le papier et bloquante
   pour la demo commerciale. Faut il des maintenant orienter les travaux vers le GSS et le Pew ATP,
   qui sont plus permissifs, pour ne pas avoir a refaire le travail au moment du go to market ?
4. **Le fine tuning est il exclu par principe ?** Si le droit au retrait est promis aux
   participants, le fine tuning sur transcripts le rend impossible a honorer. Peut on graver cette
   contrainte dans l'architecture des maintenant, ou faut il garder l'option ouverte ?
5. **Les contacts au MIT ont ils acces a la banque d'agents de Stanford ?** L'acces restreint aux
   reponses individuelles passe par une demande aupres des auteurs et un examen. Un contact chaud
   peut faire gagner des mois, et cela evite de reconstruire une collecte.
6. **Le use case politique doit il rester dans le pitch ?** Il est le plus vendeur et le plus
   sensible. La charte proposee en 3.B est defendable, mais elle interdit exactement ce qu'un
   acheteur de ce marche voudra acheter. Vaut il mieux l'assumer avec ses limites, ou le sortir de
   la vitrine tant que le papier n'est pas sorti ?
