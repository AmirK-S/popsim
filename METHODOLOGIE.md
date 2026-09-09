# METHODOLOGIE

Protocole de reproduction consolide, pret a derouler. Version du 3 septembre 2026.
Detail complet et justifications dans `exploration/04-protocole-reproduction.md`.

Le protocole se lit en trois etages. L'etage 0 ne coute aucun appel de modele et se fait
en une journee. L'etage 1 est la reproduction proprement dite. L'etage 2 est la
contribution. La voie entretien est gelee, elle figure en annexe.

---

## Principes non negociables

1. **Rien ne sort de la machine tant que les licences ne sont pas lues.** Tout le pipeline
   tourne en local sur modeles ouverts. Les paliers gratuits des API s'entrainent sur les
   donnees envoyees, ce qui est incompatible avec des microdonnees d'enquete.
2. **Toute condition a une baseline non LLM.** Au minimum : tirage dans la marginale de la
   question, et regression logistique multinomiale sur les demographies. Un chiffre sans
   plancher ne veut rien dire.
3. **Aucun score n'est publie sans nommer trois choses :** qui est predit, par rapport a
   quoi on normalise, quelle erreur humaine sert de plancher.
4. **Les questions fermees sont evaluees sur les probabilites des tokens de reponse**, pas
   sur du texte genere. Ce n'est pas seulement mille fois moins cher, cela donne la
   distribution complete d'une reponse, donc la decomposition exacte de la variance sans
   bruit d'echantillonnage. Ce choix est a valider par Simon : si un relecteur exige des
   reponses en langage naturel, l'economie disparait.
5. **Rien n'est mesure sur des donnees ayant servi a construire le persona.** Le decoupage
   entre donnees d'entree et donnees d'evaluation est fixe avant le premier run et gele.

---

## Etage 0. La reanalyse, sans un seul appel de modele

Duree : une journee. Cout : zero. Deja amorce.

### E0.1 Donnees

Paquet de replication OSF, telechargement direct sans compte :

    curl -L -o replication.rar https://osf.io/download/s2u7c/

Dossier utile : `figure2/data/new_analysis_summaries/gss_filtered/preparation/`
Un fichier par condition, 1 052 lignes, 177 colonnes, reponses en clair.
Conditions presentes : humains vague 1, humains vague 2, agents enquete, agents composite,
et quatre variantes d'agents.

### E0.2 Ce qui est deja fait

`analyses/a0_diversite_osf.py` calcule l'entropie de reponse par item et par condition, et
la probabilite que deux repondants tires au hasard donnent la meme reponse. Resultat :
diversite preservee de 66,4 pour cent pour les agents les plus pauvres a 91,1 pour cent
pour le composite, contre 100,4 pour cent pour les memes humains reinterroges. Accord par
paires de 49,5 pour cent chez les humains contre 66,4 pour cent chez les agents
demographiques.

### E0.3 Ce qui reste a faire a cet etage

- **E0.3a Decomposition inter et intra.** Pour chaque item, decomposer la variance totale
  en variance entre segments demographiques et variance a l'interieur des segments.
  Calculer le couple de ratios (R_inter, R_intra) simule sur reel. Les publier **en valeur
  absolue et separement, jamais en ratio unique**, puisque les deux erreurs se compensent.
- **E0.3b La figure signature.** Placer chaque condition comme un point dans le plan
  (R_inter, R_intra). L'humain est en (1,1). Un simulateur qui compense ses deux erreurs se
  voit immediatement sur l'hyperbole. C'est l'actif de vocabulaire du projet.
- **E0.3c Score de silhouette** par condition, sur segmentation demographique, pour
  reproduire et etendre la mesure de 0,19 contre -0,02 relevee dans la litterature.
- **E0.3d Le plafond humain.** La vague 2 donne la consistance test retest par individu,
  champ `p_wave1__p_wave2__accuracy` dans `individual_level.csv`. C'est le denominateur.
  Verifier sa distribution et non seulement sa moyenne, car normaliser par une moyenne
  masque l'heterogeneite des personnes.

**Critere de fin de l'etage 0 :** une figure et un tableau, rejouables par un tiers en une
commande, qui disent ou se situe chaque condition d'agent publiee dans le plan de la double
distorsion. C'est deja montrable au MIT.

---

## Etage 1. La reproduction de bout en bout

Duree : une a deux semaines. Cout : zero en local, 35 a 70 dollars si verification sur
modele frontiere, depense a arbitrer.

### E1.1 Jeu de donnees

**Twin-2K-500**, depot Hugging Face `LLM-Digital-Twin/Twin-2K-500`, licence CC BY 4.0, sans
compte. 2 058 personnes, plus de 500 questions, quatre vagues dont une de retest, avec un
decoupage d'evaluation deja fourni et des baselines GPT-4.1 et Gemini deja calculees.

### E1.2 Dimension retenue

**Opinions politiques et sociales.** Recommandation argumentee, contre le comportement
d'achat, pour trois raisons : la litterature documente que le politique est le domaine ou
les LLM sont les meilleurs et la consommation celui ou ils sont les pires ; les donnees
publiques d'individus reels y sont abondantes ; et surtout les jeux economiques du papier
de Stanford, qui sont le proxy le plus proche du comportement d'achat, ne montrent **aucune
difference significative entre toutes les conditions**, F egal 1,63 et p egal 0,16. Ouvrir
sur l'achat, ce serait ouvrir sur le seul domaine ou la litterature constate deja l'absence
de signal. L'achat devient une etape ulterieure, apres validation de la methode.

### E1.3 Taille de l'experience

Calcul de puissance concordant entre deux agents independants : N egal 13 personas suffit
pour detecter un ecart de 0,09, N egal 42 pour 0,05, en mode logprobs avec 50 questions.
**Retenu : 150 personas, 30 a 50 questions.** Ce n'est pas la fidelite qui contraint, c'est
le sous score de variance par groupe demographique. Duree estimee : environ cinq heures sur
la machine locale.

### E1.4 Conditions experimentales

Toutes obligatoires, aucune n'est optionnelle.

| Code | Condition | Role |
|---|---|---|
| C1a | Tirage dans la marginale de la question | Plancher absolu |
| C1b | Regression logistique multinomiale sur demographies | La baseline qui bat les LLM dans la litterature |
| C2 | Persona demographique seul | Reproduction du 74 pour cent de Stanford |
| C3 | Persona construit sur les reponses d'enquete | Reproduction du 82 pour cent |
| C4 | Idem C3, avec exemples reels en contexte | Le regime ou le LLM gagne |
| C7 | Controle d'extraction | Isole ce qui est retrouve de ce qui est predit |

La condition C7 merite un mot. Une part de la performance de la condition entretien de
Stanford vient d'une extraction de reponses deja donnees, et non d'une simulation. Sans ce
controle, nous mesurerions de la memoire et l'appellerions de la prediction.

### E1.5 Injection

Ordre d'experimentation, on ne passe a l'etape suivante que si la precedente plafonne.

1. Profil condense en invite systeme.
2. Reponses d'enquete integrales en contexte long, avec cache de prefixe.
3. Recuperation ciblee sur les reponses de la personne.
4. Fine tuning leger, **et seulement sous conditions cumulatives**. Stanford l'a teste et a
   obtenu 0,79 contre 0,84 sans. La seule configuration qui merite d'etre exploree est un
   adaptateur entraine a **preserver la variance** plutot qu'a maximiser la precision, ce
   que personne n'a fait.

### E1.6 Metriques

Deux familles, publiees cote a cote, jamais fusionnees en un score unique.

**Fidelite individuelle.** Exactitude par personne sur les questions tenues secretes,
normalisee par la consistance test retest de la meme personne. Rapporter systematiquement
trois chiffres et non un seul : performance brute, performance sur items non contamines,
performance sur jeu posterieur a la date de coupure.

**Diversite preservee.** Indice compose de sous scores publies separement : ratio d'ecarts
types par item, entropie relative, distance de Wasserstein entre distributions, structure
de correlation inter items, accord par paires, et facteur d'amplification demographique. La
critique previsible d'un indice synthetique est l'arbitraire des poids : par defaut, publier
les sous scores separement et ne presenter l'indice qu'en resume.

**Critere transversal, gratuit et absent de la litterature :** un gain de variance ne compte
que s'il **correle aux vraies differences entre les personnes reelles**. Sinon c'est du
bruit, donc une astuce de temperature deguisee. Ce test separe une contribution d'un
artefact et s'applique a toute intervention.

### E1.7 Le test existentiel, a faire en premier

Deux jours, zero euro, et il conditionne tout le reste. Question : **existe t il un regime
ou le LLM bat une regression logistique ?** Deux experiences decisives.

- **Les questions jamais posees.** Aucune baseline ne peut etre entrainee sur une question
  absente de l'enquete d'origine. C'est structurellement le terrain du LLM.
- **La courbe de croisement selon la taille d'echantillon.** Si le croisement se situe a
  2 000 repondants, il n'y a pas de marche. S'il est a 300, le produit d'extension
  d'enquete est justifie.

Si aucun regime ne donne d'avantage net au LLM, le projet devient un papier de resultat
negatif propre. C'est une issue acceptable et il faut l'acter maintenant.

---

## Etage 2. La contribution

Le correctif vise est un **transport de variance a somme constante**, de l'inter vers
l'intra. Aucune methode a bouton unique ne peut y parvenir, puisqu'il faut augmenter un
terme en diminuant l'autre. La piste la plus specifique, sans precedent trouve, est le
**retrecissement calibre des ecarts inter groupes** : tout le champ cherche a augmenter la
variance, il faut au contraire degonfler la composante inter. Cout : zero appel nouveau,
deux jours de post traitement sur les sorties de l'etage 1.

Les vingt six pistes evaluees, chacune avec son experience de validation la moins chere,
sa metrique, son critere de reussite chiffre et sa baseline a battre, sont dans
`exploration/09-angles-de-contribution.md`, et les plus prometteuses sont reprises dans
`BRAINSTORM.md`.

---

## Observabilite, des le premier run

Non negociable, et c'est la premiere tache technique du backlog.

Trace a deux niveaux, run et appel. Chaque appel enregistre : identifiant de persona,
identifiant de question, condition, graine aleatoire, version d'invite, version et
quantification de modele, duree, et distribution complete de la reponse. Index unique, de
sorte qu'une relance ne refasse aucun appel deja calcule.

**Point a trancher avant le premier run :** la trace contient par construction les vraies
reponses tenues secretes d'individus reels. Position par defaut retenue en attendant
l'arbitrage : la trace publiee est expurgee et renvoie au fichier officiel par identifiant.
Cela suffit a la reproductibilite et complique la vie d'un tiers, ce qui est le bon
compromis tant que le point de droit n'est pas tranche.

Pre enregistrement du protocole sur l'OSF avant le premier run de l'etage 1 : recommande.
Cout une journee. Un travail publie montre qu'on peut faire varier la correlation de 0,23 a
0,84 par les seuls choix de pipeline, ce qui rend le pre enregistrement decisif pour une
equipe sans antecedent. Stanford a pre enregistre ses metriques.

---

## Annexe. La voie entretien, gelee

Elle reste concue et prete, mais elle est **differee** et non abandonnee. Justification :
l'enquete seule obtient 82 pour cent contre 83 pour cent pour l'entretien de deux heures.
Le rendement de la collecte humaine est d'un point.

Elle se declenche si, et seulement si, l'une de ces trois conditions est remplie : un acces
aux transcripts de l'American Voices Project est obtenu, une affiliation institutionnelle
rend un comite d'ethique accessible, ou l'etage 1 montre un plafond que seule de la matiere
d'entretien peut lever.

Le format de donnees de l'etage 1 doit accueillir un transcript sans reecriture. C'est une
contrainte de conception a respecter des maintenant, pas une fonctionnalite a developper.

Le protocole detaille, le script d'entretien adapte de celui de Stanford, le modele de
formulaire de consentement eclaire et la checklist de conformite par horizon sont dans
`exploration/04-protocole-reproduction.md` et `exploration/07-ethique-conformite.md`.

Rappel de calendrier : une approbation ethique obtenue apres la collecte ne vaut rien, et
Stanford a mis plus de six mois avec son comite sur ce protocole precis. Sans affiliation
institutionnelle, aucun comite n'est accessible. C'est la vraie contrainte de la voie
entretien, avant l'argent et avant le recrutement.
