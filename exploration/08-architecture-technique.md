# 08. Existant reutilisable et architecture technique cible

Agent 8. Redige le 2 septembre 2026.
Phase exploratoire : ce document ne contient aucun code de production. Les extraits
sont illustratifs et n'ont pas ete ecrits sur disque.

Etat des dependances au moment de la redaction : le dossier `exploration/` etait
vide, `01-papiers-fondateurs.md` n'existait pas encore. Les arbitrages sur la
representation du persona reposent donc sur la description donnee dans la mission
et sur une verification directe du papier de 2024, pas sur le travail de l'agent 1.

---

## 0. Un resultat verifie qui change le cadrage

Avant l'inventaire, un fait que j'ai verifie moi-meme parce qu'il commande une
grande partie des choix qui suivent.

[CONFIRME] https://arxiv.org/abs/2411.10109 , soumis le 15 novembre 2024, derniere
revision v3 le 28 juin 2026, intitule a ce jour "LLM Agents Grounded in Self-Reports
Enable General-Purpose Simulation of Individuals". Resume verbatim des chiffres lus
dans le resume officiel :

- echantillon national de 1 052 Americains ;
- trois familles d'agents : entretiens semi structures de deux heures selon le
  protocole de l'American Voices Project, enquetes structurees (items du General
  Social Survey et inventaire Big Five), ou les deux combines ;
- sur des items du GSS tenus secrets, exactitudes de **83 % pour les agents
  construits sur entretien seul, 82 % sur enquete seule, 86 % sur les deux**,
  contre **74 % pour un agent construit sur les seules donnees demographiques** ;
- ces pourcentages sont normalises par **la consistance test retest des participants
  eux-memes a deux semaines**, ce qui est le plafond humain.

Trois consequences directes pour l'architecture.

**Premiere consequence, et c'est la plus importante.** L'agent construit sur
**enquete seule atteint 82 %, contre 83 % pour l'entretien de deux heures**. L'ecart
est d'un point. La contrainte 2 du projet, aucun humain recrute, ne bloque donc pas
la reproduction du resultat principal : elle coute environ un point de normalisation
si le chiffre du papier se transpose. Le pipeline doit etre concu enquete d'abord,
et l'entretien devient une variante de la meme abstraction, pas le chemin nominal.

**Deuxieme consequence.** Le baseline demographique a 74 % n'est pas un detail de
mise en page, c'est le point de comparaison qui rend les autres chiffres lisibles.
Il doit etre une condition experimentale de premiere classe dans le systeme, pas
un ajout tardif. Un resultat popsim publie sans ce baseline recalcule sur nos
donnees ne vaut rien.

**Troisieme consequence.** Le denominateur est un plafond test retest mesure sur
les memes personnes. Un jeu de donnees publiques qui ne fournit pas de retest ne
permet pas de calculer la metrique normalisee du papier. Il faut soit trouver un
jeu avec panel repete, soit publier l'exactitude brute en le disant, jamais
fabriquer un denominateur.

[HYPOTHESE, non verifiee] Le "papier de 2026" evoque dans la mission, avec ses trois
types de noeuds et sa grammaire d'aretes a quatre types, n'a pas ete identifie par
moi. Tout ce que ce document en dit reprend l'enonce de la mission sans verification
independante.

---

# PARTIE 1. INVENTAIRE DE L'EXISTANT, LE PIPELINE "DOUBLE"

Depot lu integralement : `/Users/amirkellousidhoum/Desktop/Code/Projets/research_app`.
6 089 lignes de Python dans `src/`, 17 fichiers de tests, une CI ruff plus pytest,
une documentation dense de dix fichiers dans `docs/` dont sept notes de recherche.

## 1.1 Carte du systeme

Double transforme la production publique d'une personne en base de connaissances,
puis en interlocuteur fidele a sa doctrine. Le principe structurant, enonce dans
`README.md` et `docs/DAT.md`, est une **frontiere stricte entre deux couches** :

- une **couche deterministe**, sans aucun appel de modele, gratuite, qui traite
  100 % du corpus (collecte, attribution de locuteur, segmentation, embeddings,
  index). La base est interrogeable des la fin de cette couche.
- une **couche semantique**, par LLM, qui enrichit un sous ensemble priorise
  (positions datees, principes durables, tensions). C'est un enrichissement, jamais
  un prerequis.

La consequence assumee est ecrite dans le README : "rien ne bloque sur un budget ou
une cle d'API". C'est exactement la discipline que popsim doit heriter.

### Le trajet d'une donnee

```
cible YAML (targets/*.yaml)
   |
   v
collecteurs (src/double/sources/*.py, tools/collect_*.py)     couche deterministe
   |  yt-dlp, scraping, API publiques
   v
documents en base (schema.sql : sources, documents, document_persons)
   |
   v
attribution de locuteur (normalize/speakers.py)  methode + confiance enregistrees
   |
   v
segmentation (normalize/chunk.py)  passages de 260 mots cible, 360 max, recouvrement 45
   |
   v
index (index/embed.py + index/store.py)  fastembed onnx local -> sqlite-vec + FTS5
   |                                     fusion par rang reciproque (RRF, K=60)
   +-----> recherche : CLI `double search`, MCP `search_kb`, API web
   |
   v
enrichissement (enrich/*.py)                                   couche semantique
   |  doctrine_extract.py : passages -> claims dates -> principes
   |  sujets.py           : regroupement des claims par le sens (clustering local)
   |  tensions.py         : drift / disagreement / nuance
   v
restitution (council/*.py)  plusieurs angles lisent le meme materiau, puis synthese
   |                        verification mecanique des URL citees
   v
cache semantique (council/cache.py) + serveur MCP (mcp/server.py) + web (web/app.py)
```

Transversal a tout le trajet : `runs.py` (tracage), `logging.py` (structlog),
`db.py` (acces SQLite), `config.py` (reglages).

### Modules, un par un

| Module | Chemin | Lignes | Ce qu'il fait reellement |
|---|---|---:|---|
| Configuration | `src/double/config.py` | 65 | Dataclass gelee, `lru_cache(maxsize=1)`, lecture de `.env`. Porte les cles, le chemin de base, le modele d'embedding et sa dimension, le nom du processeur. |
| Logs | `src/double/logging.py` | 49 | structlog, rendu console en local et JSON en production, selon `LOG_FORMAT`. |
| Base | `src/double/db.py` | 110 | Connexion SQLite avec `busy_timeout` a 60 s, chargement de l'extension sqlite-vec avec degradation propre si l'interpreteur l'interdit, `init_db` idempotent, `completer_colonnes` qui ajoute une colonne manquante sans detruire la table. |
| Schema | `src/double/schema.sql` | 240 | 13 tables. `persons`, `sources`, `documents`, `document_persons`, `segments` (+ FTS5 externe et triggers de synchronisation), `summaries`, `claims`, `tensions`, `runs`, `meta`, `principles`, `principle_claims`, `answers`. |
| Tracage | `src/double/runs.py` | 80 | Un gestionnaire de contexte `track` : insere une ligne `runs`, rend un compteur, et en sortie met a jour statut, volumes, tokens et valorisation. Statut `interrupted` distinct de `failed`. |
| Cibles | `src/double/targets.py` | 102 | Charge un fichier YAML declarant qui on modelise et ou trouver sa parole. Refuse un `kind` de source inconnu. |
| Collecteurs | `src/double/sources/*.py` | 1 440 | YouTube (listing + VTT), Apify, TikTok, YC Library, corpus local, Hacker News. |
| Segmentation | `src/double/normalize/chunk.py` | 181 | Deux regimes : texte long decoupe sur frontieres de paragraphe, et cues horodates regroupes en propageant les bornes temporelles. |
| Attribution | `src/double/normalize/speakers.py` | 128 | Cascade titre, description, auto presentation, sur une liste d'alias curee a la main de 28 figures YC. Enregistre toujours `method` et `confidence`. |
| Embeddings | `src/double/index/embed.py` | 71 | fastembed sur onnxruntime, sans PyTorch. Table de prefixes par famille de modele (BGE veut une consigne devant la requete, E5 veut `query:` et `passage:`). |
| Index et recherche | `src/double/index/store.py` | 327 | Indexation incrementale, garde fou `verifier_modele` qui refuse de melanger deux modeles d'embedding, contextual retrieval gratuit (le passage est prefixe de son locuteur, sa date et son titre avant vectorisation), recherche hybride vectoriel plus BM25 fusionnee par rang reciproque, elargissement adaptatif de k pour les locuteurs minoritaires, plafonne a 4 096. |
| Acces modele | `src/double/enrich/processor.py` | 302 | Classe de base `Processor` portant le reessai exponentiel et l'extraction JSON tolerante avec relance. Trois implementations : `ClaudeCodeProcessor` (sous processus `claude -p`, outils desactives), `ApiProcessor` (SDK Anthropic, streaming), `OpenRouterProcessor`. Selection par une variable d'environnement. |
| Tarifs | `src/double/enrich/tarifs.py` | 32 | Table de prix locale. Un modele inconnu est facture au tarif le plus eleve. |
| Extraction doctrine | `src/double/enrich/doctrine_extract.py` | 270 | Deux passes : document vers positions datees, puis positions vers principes durables. Incremental et reprenable. |
| Persistance doctrine | `src/double/enrich/store.py` | 216 | Ecrit positions, principes et tensions en JSONL sur disque. Le disque est la source de verite, la base une projection reconstructible. |
| Regroupement de sujets | `src/double/enrich/sujets.py` | 188 | Classification agglomerative en lien moyen sur les embeddings des enonces, seuil calibre a 0,62, ordre de groupes deterministe. |
| Tensions | `src/double/enrich/tensions.py` | 439 | Detection drift / disagreement / nuance. |
| Conseil | `src/double/council/*.py` | 672 | `router` classe la question par regex, `lenses` charge les angles declares en YAML dans `agents/`, `orchestrator` rassemble le materiau, evalue la couverture, consulte les angles en parallele, synthetise et coupe les URL inventees, `cache` memorise les reponses par similarite semantique. |
| Evaluation | `src/double/evaluation/*.py` | 131 | `dataset.py` charge et valide `evals/questions.yaml`, `metrics.py` calcule reussite, rappel@10, MRR, purete de locuteur, fuites d'attribution. |
| MCP | `src/double/mcp/server.py` | 205 | Six outils : `search_kb`, `list_people`, `get_principles`, `get_timeline`, `get_tensions`, `get_document`. |
| Web | `src/double/web/app.py` | 327 | FastAPI, une page unique, mode public qui plafonne les extraits. |
| CLI | `src/double/cli.py` | 503 | typer, sous commandes `db`, `ingest`, `index`, `enrich`, `target`, plus `search`, `ask`, `eval`, `serve`, `doctor`, `cache`. Chaque commande enveloppee dans `track`. |

### Modeles utilises

| Role | Modele | Ou | Cout |
|---|---|---|---|
| Embeddings | `BAAI/bge-small-en-v1.5`, 384 dimensions, fenetre 512 tokens | local, fastembed sur onnxruntime | nul |
| Traitement semantique v0 | binaire `claude` en mode `-p`, outils desactives | sous processus local | porte par l'abonnement, non facture |
| Traitement semantique deploiement | `claude-opus-5` via SDK Anthropic ou via OpenRouter | distant | facture, table de tarifs dans `tarifs.py` |

Point notable lu dans `docs/recherche/evaluation.md` : `config.py` annonce
`multilingual-e5-small` par defaut alors que la base a ete construite avec
`bge-small-en-v1.5`. La divergence est tracee dans la table `meta`, ce qui est le
comportement correct, mais elle signifie que la valeur par defaut du code n'est pas
ce qui tourne. Lecon a retenir pour popsim : la version reelle du modele doit etre
lue dans la trace, jamais dans la configuration.

### Stockage

Un seul fichier SQLite, `data/double.db`, en mode WAL, qui porte metadonnees,
textes, index plein texte FTS5 et vecteurs sqlite-vec. Zero serveur. `data/` n'est
pas versionne, pour une raison de droit ecrite dans `NOTICE.md` : un corpus collecte
n'appartient pas au projet et n'est pas redistribue. La doctrine extraite, elle,
est ecrite en JSONL sur disque parce que c'est la couche la plus chere a reproduire.

Cette derniere decision est excellente et transposable telle quelle : **ce qui coute
cher a produire vit sur disque, ce qui est rejouable gratuitement vit en base**.

## 1.2 Le harnais d'evaluation, ce qu'il est reellement

La mission le designe comme la brique probablement la plus precieuse. Apres lecture,
il faut distinguer deux objets qui ne se valent pas du tout.

**Le code d'evaluation livre est mince : 131 lignes.** `evaluation/dataset.py`
definit une `Question` typee avec cinq familles (`locale`, `globale`, `temporelle`,
`attribution`, `hors_corpus`) et refuse a la construction une question dans le corpus
qui ne cite pas ses sources attendues. `evaluation/metrics.py` calcule, sur les
resultats de `rechercher()`, le rang du premier document attendu, la purete de
locuteur, les fuites d'attribution et les sources interdites, puis agrege en
reussite, rappel@10 et MRR. `evals/questions.yaml` compte 161 lignes, soit de
l'ordre de 25 a 30 questions.

Ce code est **entierement un harnais de retrieval**. Il mesure si le bon document
remonte et si on ne sert pas les propos de quelqu'un d'autre. Aucune de ses formules
n'a de sens pour popsim, qui ne cherche pas un document mais predit une reponse
tenue secrete.

**Le document de recherche `docs/recherche/evaluation.md` est un autre objet, et
c'est lui le tresor.** Cinquante kilo octets de methodologie raisonnee, largement
non implementee, dont voici ce qui transpose presque mot pour mot a popsim :

1. **Le decoupage par niveau selon le besoin en modele generatif.** N0 invariants
   sans aucun modele, N1 avec embeddings locaux, N2 avec un petit modele local sur
   CPU, N3 generation de bout en bout a la demande, N4 juge de style. Les trois
   quarts des metriques utiles n'ont besoin d'aucun modele. C'est la reponse
   structurelle a la contrainte de budget zero, et elle est directement applicable.
2. **La CI qui evalue sans jamais appeler de modele facture.** Le point subtil,
   cite verbatim : "evaluer une reponse ne demande pas de la generer". On garde en
   depot des reponses d'or produites localement, et la CI recalcule les metriques
   dessus a chaque changement du code de metrique.
3. **Le test de fraicheur.** Un test de CI compare le hash des fichiers de `prompts/`
   a celui enregistre dans le dernier rapport de campagne, et echoue si le prompt a
   change sans campagne correspondante. C'est ce qui empeche un dispositif
   d'evaluation de pourrir en silence. Pour popsim c'est une exigence de premier
   ordre, parce qu'un chiffre publie doit correspondre a un prompt identifie.
4. **Pas de score agrege unique, un plancher par metrique avec tolerance.** Cite
   verbatim : "Un score global masque exactement ce qu'on cherche : la purete de
   locuteur peut s'effondrer pendant que la moyenne monte parce que le rappel a
   progresse." Pour popsim, l'exactitude individuelle peut monter pendant que la
   variance s'ecrase. C'est exactement le meme piege, et c'est notre sujet.
5. **Le catalogue des biais du LLM juge et leurs correctifs.** Biais de position
   neutralise par permutation avec comptage des seuls verdicts stables, biais de
   verbosite sorti du juge et transforme en metrique deterministe, auto preference
   reconnue comme structurelle et non evitable, aveuglement du juge sur la
   configuration testee, calibration contre cinquante annotations humaines avec un
   kappa de Cohen sous lequel le juge est declare inutilisable, temperature zero et
   version de juge epinglee dans chaque rapport.
6. **La doctrine sur ce qu'un score veut dire.** Cite verbatim : "Aucun des deux ne
   produit un score absolu publiable. Ce sont des detecteurs de regression. 'La
   fidelite est passee de 0,81 a 0,74 apres ce changement' est exploitable. 'Notre
   fidelite est de 0,81' ne l'est pas." Pour popsim, ou l'ambition est justement de
   publier un chiffre absolu, cette phrase impose une exigence : le chiffre absolu
   n'est publiable que contre un plafond mesure (le test retest) et un plancher
   mesure (le baseline demographique). Le papier de 2024 fait exactement cela.
7. **Le releve d'activite des frameworks d'evaluation au 31 aout 2026**, avec dates
   de derniere publication et de dernier commit. Verdict retenu : RAGAS en perte de
   vitesse et tirant LangChain et le SDK OpenAI en dependances de coeur, DeepEval et
   promptfoo vivants, harnais maison recommande. Ce releve est utile a popsim, mais
   il a un an d'age au sens des depots et devra etre refait.
8. **La methode d'etablissement de la verite terrain a l'envers**, en partant du
   materiau plutot que de la question, avec deux filtres mecaniques : un filtre de
   fuite (poser la question sans contexte, ecarter si le modele repond juste de
   memoire) et un filtre de recouvrement lexical (Jaccard superieur a 0,6, la
   question est un copier coller deguise). Le filtre de fuite est **critique pour
   popsim** : un modele qui connait les distributions marginales du GSS peut repondre
   juste sans rien savoir de l'individu. Il faudra un equivalent, detaille en 2.6.

Verdict net : **le code d'evaluation de Double n'est pas reutilisable, sa
methodologie l'est presque integralement.**

## 1.3 Tableau de reutilisabilite, module par module

La difference de fond qui commande chaque verdict : Double modelise **une** personne
publique a partir de son discours produit, et est juge sur la fidelite doctrinale
avec citation des sources. Popsim modelise **des milliers** de personnes ordinaires
a partir de reponses d'enquete, et est juge sur la prediction de reponses tenues
secretes et sur la preservation de la variance entre individus.

Legende : **TQ** reutilisable tel quel, **AD** reutilisable avec adaptation,
**NON** inutile ici.

| Brique | Chemin | Verdict | Justification tiree du code lu |
|---|---|:---:|---|
| Logs structures | `src/double/logging.py` | **TQ** | 49 lignes, structlog, une seule dependance vers `settings()`. Rendu console en local, JSON en production. Rien de specifique au corpus. Copiable en changeant le nom du paquet. |
| Tracage des etapes | `src/double/runs.py` | **AD** | Le gestionnaire de contexte `track` est exactement la bonne forme : statut `interrupted` distinct de `failed`, compteurs `items_in/out`, `tokens_in/out`, `valorisation_eur`, `meta` en JSON, et mise a jour dans un `finally` donc une interruption laisse une trace exploitable. Mais il est **au niveau de l'etape, pas de l'appel**. Il ne porte ni graine, ni version de prompt, ni version de modele, ni duree par appel. Popsim exige les cinq. A etendre en deux niveaux, voir 2.7. |
| Acces SQLite | `src/double/db.py` | **AD** | `busy_timeout` a 60 s, WAL, `init_db` idempotent, `completer_colonnes` qui ajoute une colonne sans recreer la table (commentaire du code : "recreer la table detruirait la doctrine"). Tout cela transpose. Le chargement de sqlite-vec ne sert popsim que si on garde un index vectoriel, ce qui n'est pas acquis. |
| Schema du corpus | `src/double/schema.sql` | **NON** pour les tables, **AD** pour trois d'entre elles | Les tables `sources`, `documents`, `document_persons`, `segments`, `claims`, `principles`, `tensions` decrivent un corpus de parole publique. L'entite centrale de popsim n'est pas un document mais un triplet (individu, item, reponse). En revanche `runs` et `meta` transposent, et la table `meta` porte une idee precieuse : le garde fou qui refuse de melanger deux modeles d'embedding dans la meme table de vecteurs, parce que "melanger deux modeles rend la similarite fausse sans lever la moindre erreur". |
| Abstraction du modele | `src/double/enrich/processor.py` | **AD, forte valeur** | La deuxieme brique la plus precieuse du depot. Une classe de base qui porte le reessai exponentiel et la relance sur JSON malforme, une seule methode `_appeler` a implementer, trois fournisseurs derriere la meme interface, selection par `PROCESSOR=claude_code|api|openrouter`. Sous budget zero, `ClaudeCodeProcessor` (sous processus `claude -p`, `--disallowed-tools all`) est un vrai actif deja eprouve. A adapter : ajouter la duree, la graine, l'identifiant exact de modele et les logprobs dans la dataclass `Reponse`, et ajouter une quatrieme implementation locale. Limite structurelle a l'echelle, voir 2.9. |
| Table de tarifs | `src/double/enrich/tarifs.py` | **TQ dans l'esprit, AD dans les valeurs** | 32 lignes qui portent une lecon chere : le champ `cost` renvoye par OpenRouter vaut zero sur des appels reels, donc "un plafond de depense branche dessus ne se declenche jamais, et il est d'autant plus dangereux qu'il donne l'illusion d'une protection". Le commit `12e2a2b fix: le plafond de depense recevait zero et ne se declenchait jamais` confirme que le bug a reellement eu lieu. Un modele inconnu est facture au tarif le plus eleve : bon sens de l'erreur, a garder. |
| Cibles declaratives | `src/double/targets.py` + `targets/*.yaml` | **AD, forte valeur conceptuelle** | Le docstring dit l'essentiel : "ajouter une personne ne demande pas d'ecrire du code, seulement de declarer ses sources". Popsim a besoin du meme mecanisme, applique a une etude : quel jeu, quelle vague, quels items construisent le persona, quels items sont tenus secrets. Le code lui meme (102 lignes de chargement YAML avec un `SOURCES_CONNUES` de collecteurs web) ne se reprend pas, c'est le motif qui se reprend. |
| Angles declaratifs | `src/double/council/lenses.py` + `agents/*.yaml` | **AD** | Meme motif : un lecteur specialise se declare en YAML avec ses besoins valides contre `BESOINS_CONNUS` et son schema de sortie. Popsim s'en sert pour declarer les **variantes de representation du persona** et leurs versions, ce qui est exactement l'experience scientifique a mener. Le contenu des angles, lui, ne sert a rien ici. |
| Segmentation | `src/double/normalize/chunk.py` | **AD, seulement pour la branche entretien** | 181 lignes soigneuses, avec recouvrement, recollage des reliquats courts et propagation des bornes temporelles. Utile pour decouper un transcript d'entretien de deux heures. Les constantes (260 mots cible, 360 max) sont calibrees sur une fenetre de 512 tokens et sur l'anglais a 1,27 token par mot : a recalibrer. Pour une enquete, inutile, il n'y a rien a decouper. |
| Attribution de locuteur | `src/double/normalize/speakers.py` | **NON pour le code, AD pour le motif** | `ALIAS_YC` est une liste curee a la main de 28 figures de Y Combinator, avec des regex sur le titre et la description. Rien de tout cela n'existe dans une enquete. Le motif qui transpose est la cascade qui enregistre toujours sa `method` et sa `confidence`, avec le commentaire "une attribution faible se revise, elle ne se devine pas". Dans la branche entretien, distinguer l'enqueteur du repondant est le meme probleme et merite le meme traitement. |
| Embeddings locaux | `src/double/index/embed.py` | **AD** | fastembed sur onnxruntime, sans PyTorch, choisi parce que la machine cible est un MacBook Air sans refroidissement actif. La table `PREFIXES` / `PREFIXES_PASSAGE` par famille de modele est un savoir dur : oublier la consigne devant la requete d'un modele BGE "degrade silencieusement le rappel". Utile a popsim pour le regroupement de libelles et pour l'eventuelle recuperation dans une memoire brute longue. |
| Recherche hybride | `src/double/index/store.py` | **NON en majorite, AD pour deux details** | La fusion par rang reciproque, `_filtre_personne`, l'elargissement adaptatif de k : tout cela repond au probleme "retrouver le bon passage d'un corpus", que popsim n'a pas. Deux details transposent : `verifier_modele`, qui refuse de melanger deux modeles d'embedding dans le meme index, et `_texte_a_indexer`, qui prefixe le passage de son locuteur, sa date et son titre avant vectorisation, "du contextual retrieval sans payer un seul appel de modele". |
| Regroupement par le sens | `src/double/enrich/sujets.py` | **AD, meilleure surprise de l'inventaire** | Classification agglomerative en lien moyen sur les embeddings des enonces, seuil 0,62 calibre par mesure (mediane des paires a 0,48, neuvieme decile a 0,59), avec le raisonnement explicite du refus du lien simple qui "enchaine" et fait tout absorber par un groupe. C'est **exactement la machinerie que demande la generalisation des etiquettes du graphe de 2026**. Attention a l'echelle : `matrice_similarite` construit une matrice pleine en O(n^2), acceptable sur les quelques centaines de claims d'une personne, impraticable sur les noeuds de 10 000 personas. |
| Extraction de doctrine | `src/double/enrich/doctrine_extract.py` | **AD, avec une reserve de fond** | Le motif en deux passes (document vers positions datees, positions vers principes durables) est le squelette d'une construction de graphe de persona : elle appelle un prompt, valide la sortie, ne retient que ce qui pointe vers du materiau reel (`appuis = [i for i in claim_ids if i in ids_valides]`, et un principe avec moins de deux appuis est jete), et ecrit sur disque au fil de l'eau pour qu'une interruption ne perde qu'un document. Tout cela transpose. La reserve de fond : cette extraction cherche **ce qui tient dans le temps**, c'est a dire ce qui est stable et general. Appliquee a 10 000 individus, une extraction qui privilegie le stable et le general est un mecanisme d'homogeneisation. C'est precisement le risque a mesurer, pas a subir. |
| Persistance sur disque | `src/double/enrich/store.py` | **TQ dans le principe** | "Le disque devient la source de verite, la base une projection reconstructible", parce que la couche la plus chere etait la seule non durable et "disparaissait a la premiere migration de schema". Pour popsim, les personas construits par LLM sont exactement cette couche chere. JSONL append only, document par document. A reprendre sans discussion. |
| Detection de tensions | `src/double/enrich/tensions.py` | **NON** | 439 lignes pour distinguer drift, desaccord et nuance chez une personne publique dont on a date chaque prise de position. Une enquete donne une reponse par item et par vague : il n'y a ni chronologie fine ni contradiction a arbitrer. Deviendrait pertinent seulement sur des panels longitudinaux, et ce n'est pas la v0. |
| Conseil, deliberation | `src/double/council/orchestrator.py` | **NON, et c'est un piege actif** | Plusieurs angles lisent le meme materiau en parallele puis sont synthetises en une reponse. C'est un dispositif de fidelite doctrinale. Transpose a popsim il serait **contre productif** : faire deliberer et converger plusieurs lectures est exactement le mecanisme qui ecrase la variance, c'est a dire le defaut que le projet vise a corriger. A ne pas reprendre. |
| Porte de couverture | `evaluer_couverture` dans `orchestrator.py` | **AD** | Trois etats couverte / mince / absente, sur des seuils de similarite cosinus calibres par mesure (0,74 et 0,68, avec le releve : question couverte entre 0,79 et 0,84, hors sujet entre 0,59 et 0,70), et surtout le refus de depenser un appel de modele quand la couverture est absente. Le principe transpose en "cet individu n'a pas fourni de quoi repondre a cet item", ce qui est necessaire pour modeliser honnetement un "ne sait pas". |
| Verification des sources | `verifier` dans `orchestrator.py` | **NON** | Coupe toute URL absente du materiau rassemble. Popsim produit des codes de modalite, pas des citations. Redeviendrait utile seulement dans une variante entretien ou l'agent doit ancrer sa reponse dans un verbatim. |
| Routage de question | `src/double/council/router.py` | **NON** | Regex francais et anglais pour classer une question en locale, temporelle, globale ou comparative. Un item d'enquete est deja type par son codebook. |
| Cache semantique | `src/double/council/cache.py` | **AD, avec inversion du principe** | Le code a raison sur le point dur : "Le filtre sur la personne est strict : la meme question adressee a deux voix differentes n'a pas la meme reponse, et confondre les deux serait le pire defaut possible pour ce produit." Le seuil 0,82 est calibre par mesure et le commentaire documente qu'un seuil a 0,93 "choisi au doigt mouille" ne touchait jamais. Mais pour popsim, un cache **semantique** est un danger de reproductibilite : deux items proches ne sont pas le meme item, et un cache qui les confond fabrique de la fausse coherence. Popsim veut un cache **litteral** sur la cle exacte (representation, empreinte du persona, item, prompt, modele, temperature, graine, repetition). Meme mecanique de stockage, principe inverse. |
| Evaluation, le code | `src/double/evaluation/*.py` | **NON pour les formules, AD pour la forme** | Les metriques sont du retrieval pur (rang du document attendu, purete de locuteur, fuites d'attribution). Aucune ne transpose. Ce qui transpose : une `Question` est un objet **type et valide a la construction**, qui leve une exception si elle est mal formee ("une question dans le corpus doit citer ses sources"), et elle est **ancree sur des identifiants qui survivent a une reingestion**, pas sur des identifiants de base volatils. Les deux idees doivent etre reprises. |
| Evaluation, la methodologie | `docs/recherche/evaluation.md` | **AD, valeur la plus haute du depot** | Detaille en 1.2. Niveaux N0 a N4, CI sans API facturee, reponses d'or figees, test de fraicheur des prompts, planchers par metrique avec tolerance, catalogue des biais de juge et protocoles correctifs, filtres de fuite et de recouvrement sur les questions generees. |
| Serveur MCP | `src/double/mcp/server.py` | **AD, priorite basse** | Six outils qui exposent la base a Claude Code. Excellent pour l'inspection qualitative d'un persona ("montre moi ce que l'agent 4127 sait de lui meme"), a cout marginal nul puisque le client est l'abonnement. Mauvaise interface pour interroger 10 000 agents en lot. |
| Interface web | `src/double/web/app.py` + `static/` | **NON pour la v0** | 327 lignes de FastAPI et une page unique, avec un mode public qui plafonne les extraits pour des raisons de droit. Popsim livre un rapport d'experience, pas un chat. Redevient utile pour une demonstration commerciale. |
| Collecteurs | `src/double/sources/*`, `tools/collect_*.py` | **NON** | Environ 1 900 lignes de collecte web (yt-dlp, Apify, TikTok, scraping d'essais, API Hacker News). Popsim charge des fichiers d'enquete SPSS, Stata ou CSV, ce qui est un autre monde. Seul le motif `upsert_documents` idempotent est a retenir. |
| CLI | `src/double/cli.py` | **AD pour le motif** | typer avec sous applications, et surtout **chaque commande est enveloppee dans `track`**, donc rien ne tourne sans laisser de trace. C'est la discipline a reprendre, pas les commandes. |
| Tests et CI | `tests/`, `.github/workflows/ci.yml` | **TQ comme pratique** | Le fichier de CI fait 20 lignes (ruff check, ruff format check, pytest avec couverture) et est copiable tel quel. Les tests eux memes sont specifiques. Observation : le README annonce 104 tests, mon comptage de `def test` sur les 17 fichiers en donne 125. L'ecart n'est pas explique et n'a pas d'importance ici. |
| Squelette de depot | `pyproject.toml`, `CONTRIBUTING.md`, `.mcp.json`, `NOTICE.md` | **TQ comme modele** | En particulier `NOTICE.md` et la regle "`data/` n'est pas versionne, un corpus collecte n'est pas a nous". Popsim manipule des micro donnees d'enquete sur des individus reels : la meme regle s'applique, en plus strict. |
| Plan d'industrialisation | `docs/INDUSTRIALISATION.md` | **AD, idee non implementee** | Le document annonce lui meme "rien de ce qui suit n'est implemente". L'idee la plus utile est la **sonde** : avant d'engager une collecte complete, un echantillon de vingt a cinquante items repond a six questions (volume, langue, periode, une voix ou plusieurs, densite, cout attendu) et le resultat est rendu comme "un devis, pas un rapport d'echec". Transpose a popsim : avant de lancer 10 000 agents, echantillonner vingt individus, mesurer le cout par agent, la duree, et la variance des items tenus secrets. |

### Synthese chiffree de la reutilisabilite

Sur les 6 089 lignes de `src/`, en comptant genereusement :

- **reutilisable tel quel ou presque** : environ 260 lignes (`logging.py`, `tarifs.py`,
  `runs.py`, la mecanique de `db.py`), soit 4 % ;
- **reutilisable avec adaptation reelle** : environ 1 200 lignes (`processor.py`,
  `sujets.py`, `chunk.py`, `embed.py`, `targets.py`, `lenses.py`, `cache.py`,
  `enrich/store.py`, motifs de `cli.py` et `mcp/server.py`), soit 20 % ;
- **inutile ici** : environ 4 600 lignes (collecteurs, recherche hybride, conseil,
  tensions, web, attribution de locuteur), soit 76 %.

Ce ratio est normal et ne devalue pas Double. Ce qui se transporte d'un projet a
l'autre n'est presque jamais le code metier, c'est le socle et surtout les lecons.
La valeur reelle de Double pour popsim est ailleurs que dans les lignes : elle est
dans `docs/recherche/evaluation.md`, dans la discipline de la frontiere deterministe
contre semantique, dans le tracage systematique, et dans une quinzaine de commits
de correction qui documentent des pieges que popsim rencontrera a l'identique.

### Les pieges de Double qui attendent popsim, deja documentes

Ces commits sont a lire comme une liste de pieges connus, pas comme de l'histoire.

| Commit | Piege | Ou il se represente dans popsim |
|---|---|---|
| `ad2470f` les documents longs n'etaient pas decoupes, invisibles a 95 % | Un transcript de 13 815 tokens vectorise sur une fenetre de 512, sans aucune erreur levee | Un transcript d'entretien de deux heures injecte dans un modele dont la fenetre effective est plus courte que la fenetre annoncee. Silencieux. |
| `8a31e50` l'index plein texte etait vide, la recherche n'etait pas hybride | Une moitie du systeme ne faisait rien et la fusion par rang "se contentait de reecrire le rang" | Une condition experimentale qui ne fait pas ce qu'elle annonce et rend quand meme un chiffre plausible. |
| `9b8c6fd` le filtre par locuteur servait les propos des autres | 21 % seulement des passages rendus pour Garry Tan etaient de lui | La contamination entre individus : un persona qui repond avec la matiere d'un autre. Meme forme, memes consequences. |
| `24e7edc` vecteurs orphelins | Une reingestion avait laisse 17 233 vecteurs orphelins qui occupaient des places parmi les k plus proches, degradant le rappel sans aucune erreur | Des appels d'un run precedent melanges a un run courant dans la meme table de trace. |
| `12e2a2b` le plafond de depense recevait zero | Le champ `cost` du fournisseur valait zero, le plafond ne se declenchait jamais | Identique, et sous budget zero le plafond est vital. |
| `b963251` la colonne cout ne mesurait pas un cout | Les tokens lus depuis le cache n'etaient pas comptes en entree | Sous estimer d'un facteur dix le cout d'une campagne. |
| `1ccfb37` la doctrine ne survivait pas a une reconstruction de la base | La couche la plus chere etait la seule non durable | Les personas construits par LLM, si on les garde seulement en base. |

Le fil commun de ces sept incidents : **des defauts qui ne levent aucune erreur et
produisent un resultat plausible**. C'est le mode d'echec dominant de ce genre de
systeme, et c'est ce qui justifie de commencer popsim par la trace et par les
invariants, pas par la modelisation.

## 1.4 Les briques manquantes pour popsim

Absentes de Double, a construire, par ordre de difficulte croissante.

1. **Lecture de fichiers d'enquete.** Formats SPSS `.sav` et Stata `.dta`, plus CSV.
   `pyreadstat` est la bibliotheque de reference et lit les deux, y compris les
   etiquettes de valeur [CONFIRME https://pypi.org/project/pyreadstat/ repond 200].
   Aucun equivalent dans Double.
2. **Modele de codebook.** Un item d'enquete n'est pas une chaine : c'est un libelle,
   une echelle, une liste de modalites codees, des codes manquants distincts
   ("refus", "ne sait pas", "non applicable"), et parfois un filtre conditionnel.
   Rien dans Double n'approche cela, et c'est la ou passera le plus de travail
   ingrat. C'est aussi la ou se logent les erreurs les plus couteuses : confondre
   un code 8 "ne sait pas" avec une valeur 8 sur une echelle en 10 points ruine
   silencieusement toute une colonne.
3. **Protocole de decoupage.** Quels items construisent le persona, quels items sont
   tenus secrets, avec une graine, une version, et une garantie qu'aucun item tenu
   secret ne fuit dans le contexte. Double n'a pas de notion de secret : tout son
   corpus est visible.
4. **Runner en lot sur N agents.** Concurrence bornee, reprise apres interruption,
   idempotence par (run, individu, item, repetition), plafond de cout effectif,
   limitation de debit par fournisseur. Double appelle le modele document par
   document, en sequentiel, avec un `ThreadPoolExecutor` de six pour les angles du
   conseil. Cela ne monte pas a 10 000.
5. **Metriques individuelles.** Exactitude sur items tenus secrets, exactitude
   normalisee contre le plafond test retest, kappa de Cohen par individu, matrice
   de confusion par item. Aucun equivalent.
6. **Metriques distributionnelles.** C'est le coeur scientifique et Double n'a
   strictement rien. Detaille en 2.6.
7. **Ponderations d'enquete.** Une enquete reelle est ponderee. Comparer une
   distribution simulee non ponderee a une distribution reelle ponderee produit un
   ecart qui n'a rien a voir avec le modele. Absent de Double, qui n'a pas de
   population.
8. **Statistique inferentielle.** Intervalles de confiance par bootstrap sur les
   individus, correction pour comparaisons multiples sur des dizaines d'items.
   Double s'en passe legitimement, popsim ne le peut pas.
9. **Controle du determinisme.** Graine, temperature, et surtout la reconnaissance
   explicite qu'un modele distant n'est pas reproductible au bit pres. Detaille
   en 2.8.
10. **Gouvernance des micro donnees.** Double a deja la bonne posture (`data/` non
    versionne, `NOTICE.md`), mais popsim manipule des reponses individuelles de
    personnes reelles, ce qui est une categorie de donnee differente. La question
    de savoir si une trace contenant les vraies reponses tenues secretes peut etre
    versionnee doit etre tranchee avant le premier run, pas apres.

---

# PARTIE 2. ARCHITECTURE CIBLE DE POPSIM

Contraintes qui commandent tout ce qui suit : budget zero, donnees publiques
d'abord, aucun humain recrute, phase de conception sans code de production.

## 2.1 Le pipeline en sept etages

```
  S1  SOURCE
      enquete publique (GSS, ESS, WVS...)  |  transcript d'entretien
      lecture pyreadstat ou texte, empreinte sha256 du fichier source
      |
  S2  NORMALISATION vers le format Personne
      un codebook + N fichiers Personne, format unique, source oubliee ensuite
      |
  S3  REPRESENTATION du persona            <-- LE POINT D'ARBITRAGE SCIENTIFIQUE
      interface unique, trois implementations interchangeables :
        demographique@1   (baseline obligatoire)
        memoire_brute@1   (approche 2024)
        graphe@1          (approche 2026)
      sortie : un Persona + son empreinte sha256
      |
  S4  INSTANCIATION de l'agent
      pas un processus, une fonction pure :
      (contexte, item, prompt, modele, parametres, graine) -> reponse codee
      |
  S5  HARNESS D'INTERROGATION EN LOT
      produit cartesien declare en YAML, concurrence bornee, reprise,
      idempotence par (run, individu, item, repetition), plafond de cout
      |
  S6  METRIQUES
      individuelles (exactitude, exactitude normalisee, kappa)
      populationnelles (distance de distribution, ratio d'ecart type,
                        entropie, part modale, structure de correlation)
      intervalles par bootstrap, comparaison au baseline demographique
      |
  S7  RAPPORT REPRODUCTIBLE
      un dossier par run, chaque chiffre porte son run_id,
      aucune valeur saisie a la main dans le papier
```

Le principe de Double est conserve et durci : **frontiere stricte entre ce qui ne
coute rien et ce qui coute**. S1, S2, S6 et S7 sont entierement deterministes et
gratuits. S3 coute selon la representation choisie (zero pour la memoire brute et
le baseline, non nul pour le graphe). S5 est le seul poste de depense reel.

## 2.2 Le format unique de personne

Deux fichiers seulement, plus un manifeste de decoupage. Format JSON Lines, une
personne par ligne, plus un codebook a part parce qu'il est partage.

**Codebook**, un fichier par jeu de donnees :

```json
{
  "jeu_id": "gss-2022",
  "version": "1",
  "langue": "en",
  "items": [
    {
      "item_id": "polviews",
      "libelle": "Think of self as liberal or conservative",
      "type": "categoriel_ordonne",
      "modalites": [
        {"code": "1", "libelle": "Extremely liberal", "rang": 1},
        {"code": "7", "libelle": "Extremely conservative", "rang": 7}
      ],
      "codes_manquants": [
        {"code": ".d", "sens": "ne sait pas"},
        {"code": ".n", "sens": "non applicable"},
        {"code": ".i", "sens": "non pose"}
      ],
      "domaine": "politique"
    }
  ]
}
```

**Personne**, une ligne par individu :

```json
{
  "person_id": "gss-2022-0004127",
  "jeu_id": "gss-2022",
  "poids_sondage": 0.8123,
  "provenance": {
    "fichier": "GSS2022.sav",
    "sha256": "…",
    "extrait_le": "2026-09-05",
    "licence": "a renseigner"
  },
  "reponses": [
    {"item_id": "age",      "code": "47",  "libelle": "47"},
    {"item_id": "polviews", "code": "5",   "libelle": "Slightly conservative"}
  ],
  "tours": []
}
```

Quatre decisions dans ce format, chacune pour une raison.

**Le codebook est separe des personnes.** Un libelle d'item recopie 10 000 fois est
10 000 occasions de divergence. Le fichier Personne ne porte que des codes, la
lisibilite vient du codebook au moment du rendu.

**Le decoupage n'est pas dans le fichier Personne.** Il vit dans un manifeste
separe qui liste, par role, les `item_id`. Raison : un fichier Personne ne doit
jamais etre reecrit entre deux experiences, sinon son empreinte change et la
comparaison de deux runs devient impossible. Le manifeste :

```yaml
split_id: gss-2022-split-a
graine: 20260902
version: 1
contexte: [age, sex, educ, race, income, region, marital, ... ]   # entrent dans le persona
cible:    [polviews, partyid, abany, cappun, grass, ... ]         # tenus secrets
exclus:   [id, year, ballot, wtssall]                             # techniques, jamais soumis
```

**Le champ `tours` est vide pour une enquete et rempli pour un entretien.** C'est ce
qui rend le format reellement unique : la branche entretien n'est pas un autre
format, c'est le meme avec une liste non vide. Un `Tour` porte `locuteur`
(`enqueteur` ou `repondant`), `texte`, et optionnellement des bornes temporelles.
Le `Processor` en aval ne sait pas d'ou vient la matiere.

**La ponderation est portee des la normalisation.** Ajouter les poids apres coup est
la garantie de calculer trois metriques sur des distributions non ponderees avant de
s'en apercevoir.

## 2.3 La representation du persona, l'arbitrage central

C'est l'experience scientifique que le projet veut mener. Le systeme doit permettre
de tester les deux representations sans etre reecrit.

### Les deux approches, ce qu'elles coutent et ce qu'elles risquent

| Critere | A. Memoire brute, approche 2024 | B. Graphe de connaissances, approche 2026 |
|---|---|---|
| Contenu | Le materiau tel quel, rendu en texte : transcript d'entretien, ou liste des reponses de contexte lues comme des phrases | Noeuds de trois types (sujets, faits, interpretations), aretes d'une grammaire restreinte a quatre types, fusion priorisee, generalisation des etiquettes |
| Cout de construction | **Nul.** Deterministe, aucun appel de modele. Reproductible au bit pres. | **Non nul, par agent.** Des appels de modele pour extraire et fusionner. A 10 000 agents c'est un poste de depense a part entiere. |
| Cout par interrogation | Croit avec le materiau. Un entretien de deux heures pese de l'ordre de 20 000 a 33 000 tokens [PROBABLE, calcul en 2.9] | Faible et borne : on ne charge que le sous graphe pertinent pour l'item |
| Perte d'information | Nulle par construction | Reelle et voulue. C'est le point sensible. |
| Inspectabilite | Faible : on ne peut pas dire ce que l'agent "sait" autrement qu'en relisant le transcript | Forte : le graphe s'ouvre, se compte, s'edite, et surtout **s'ablate** |
| Surface d'ablation | Quasi nulle | Riche : retirer les interpretations, retirer un type d'arete, desactiver la generalisation, et mesurer chaque fois |
| Risque principal | Le cout et la fenetre de contexte | **L'homogeneisation.** La generalisation des etiquettes pousse vers un vocabulaire partage entre individus. Si deux personnes finissent avec le meme noeud generalise, on a detruit precisement la variance qu'on veut preserver. |
| Adosse a un resultat publie | Oui, 83 % sur entretien et 82 % sur enquete [CONFIRME arXiv 2411.10109] | Non verifie par moi |

**[HYPOTHESE, c'est la these testable du projet]** La representation en graphe, avec
generalisation des etiquettes, ameliore l'exactitude individuelle moyenne et degrade
la preservation de la variance inter individuelle, parce que generaliser consiste
a remplacer un idiome propre a une personne par une categorie partagee. Si cette
hypothese se verifie, elle est en elle meme un resultat publiable, et elle designe
une troisieme representation a construire : un graphe **sans** generalisation, ou
avec une generalisation bornee aux seuls noeuds de type sujet.

### L'abstraction qui permet de tester les deux

Une seule interface. Tout ce qui est en aval (instanciation, harness, metriques,
rapport) ne connait que cette interface, jamais une implementation concrete.

```python
# Extrait illustratif. Aucun fichier n'a ete cree.

class Representation(Protocol):
    nom: str        # "memoire_brute"
    version: str    # "1"  -> identifiant complet "memoire_brute@1"

    def construire(self, personne: Personne, split: Split,
                   codebook: Codebook, rng: Generator,
                   proc: Processor | None) -> Persona:
        """Materiau de contexte -> persona. Deterministe si proc est None."""

    def contexte_pour(self, persona: Persona, item: Item) -> Contexte:
        """Ce qui entrera dans le prompt pour CET item. Pas une chaine : un objet."""

    def empreinte(self, persona: Persona) -> str:
        """sha256 du contenu canonicalise. C'est ce qui va dans la trace."""

    def statistiques(self, persona: Persona) -> dict:
        """Taille, nombre de noeuds, tokens estimes. Alimente la sonde."""
```

Cinq points de conception, chacun pour une raison precise.

**`contexte_pour` rend un objet, pas une chaine.** Le rendu final en texte est fait
par un gabarit de prompt versionne separement. Sans cette separation, changer la
formulation du prompt oblige a reconstruire tous les personas, et on ne peut plus
distinguer un effet de representation d'un effet de formulation. Avec, la matrice
representation x prompt est un simple produit cartesien.

**`empreinte` est obligatoire.** C'est elle qui rend une trace rejouable : deux runs
qui declarent la meme representation mais dont les empreintes different n'ont pas
compare la meme chose, et il faut que le systeme puisse le dire.

**`construire` recoit un `Processor` optionnel.** `None` signifie "cette
representation est deterministe et gratuite", ce qui est vrai pour la memoire brute
et le baseline demographique, et faux pour le graphe. Le harness lit cette
information pour savoir s'il doit budgeter une phase de construction.

**`construire` recoit un generateur aleatoire explicite**, jamais un aleatoire
global. C'est la condition de la reproductibilite, et c'est la premiere chose qu'on
oublie.

**Trois implementations obligatoires en v0**, pas deux :

| Identifiant | Contenu | Cout de construction | Role |
|---|---|---|---|
| `demographique@1` | age, sexe, education, revenu, region, et rien d'autre | nul | **Plancher obligatoire.** 74 % dans le papier de 2024. Sans lui, aucun autre chiffre n'est interpretable. |
| `memoire_brute@1` | toutes les reponses de contexte rendues en texte, ou le transcript | nul | Reproduction de l'approche 2024 |
| `graphe@1` | trois types de noeuds, quatre types d'aretes, fusion priorisee, generalisation | non nul, par agent | Approche 2026, la contribution |

Et une quatrieme, a construire des que le graphe existe, parce qu'elle isole la
variable la plus suspecte : `graphe_sans_generalisation@1`.

La declaration d'une experience devient alors un fichier, et l'experience entiere
est ce fichier :

```yaml
# experiences/repro-2024.yaml
experience: repro-2024
graine: 20260902
jeu: gss-2022
split: gss-2022-split-a
echantillon: {n: 200, methode: stratifie, strates: [age_classe, sex, educ_classe]}
representations: [demographique@1, memoire_brute@1, graphe@1]
prompt: interrogation@3
modeles:
  - {fournisseur: local,  modele: "qwen2.5-32b-instruct-q4", temperature: 1.0}
  - {fournisseur: groq,   modele: "llama-3.3-70b-versatile", temperature: 1.0}
repetitions: 5
plafond_cout_usd: 0.0
```

`plafond_cout_usd: 0.0` n'est pas decoratif. Sous budget zero, le harness doit
refuser de demarrer si un fournisseur declare est facture et que le plafond est a
zero. C'est la lecon du commit `12e2a2b` de Double retournee en garde fou.

## 2.4 L'instanciation de l'agent

**Un agent n'est pas un processus, ni une conversation. C'est une fonction pure.**

```
repondre(contexte, item, gabarit_prompt, modele, parametres, graine) -> ReponseCodee
```

Trois raisons, et la deuxieme est scientifique avant d'etre technique.

1. **Echelle.** 10 000 sessions conversationnelles vivantes est impossible sous
   budget zero. Un appel sans etat est le seul objet qui monte.
2. **Validite de la mesure.** Si un agent repond aux trente items dans une meme
   conversation, ses reponses tardives sont conditionnees par ses reponses
   precoces. On mesure alors la coherence interne du modele, pas sa fidelite a
   l'individu. Un vrai repondant a de l'incoherence, et l'ecraser est exactement
   le mecanisme d'ecrasement de variance que le projet denonce.
3. **Rejouabilite.** Une fonction pure est cacheable par sa cle exacte et rejouable
   depuis la trace.

L'effet d'ordre du questionnaire est un vrai sujet de recherche. Il devient alors
une **condition experimentale declaree** (`mode: session`, avec une liste d'items
ordonnee et sa graine de permutation), jamais le comportement par defaut.

### Le format de reponse, et pourquoi c'est le point technique le plus important

Un item d'enquete a un ensemble fini de modalites. Trois strategies, par ordre de
valeur scientifique decroissante.

**1. Distribution sur les modalites via les logprobs.** Quand le fournisseur expose
les probabilites des premiers jetons, on obtient non pas une reponse mais **la
distribution de l'agent sur les modalites**. C'est de tres loin le plus riche :
il devient possible d'echantillonner dans cette distribution plutot que de prendre
son maximum, et de mesurer separement l'incertitude de l'agent et sa reponse.
[A VERIFIER] quels fournisseurs gratuits exposent les logprobs en 2026.

**2. Decodage contraint par grammaire, en local.** llama.cpp accepte une grammaire
GBNF, vLLM accepte un decodage guide. La sortie est garantie dans l'ensemble des
modalites, sans aucun reessai, et on peut lire les probabilites.
[CONFIRME https://github.com/ggml-org/llama.cpp et https://github.com/vllm-project/vllm repondent 200]

**3. Contrat JSON strict avec relance.** Le motif `Processor.json` de Double, qui
relance une fois avec un rappel explicite du format. Fonctionne partout, coute des
jetons, et introduit un biais : un item dont la sortie echoue systematiquement
disparait des donnees si on ne compte pas les echecs. La trace doit donc porter
`tentatives` et `statut`, comme le fait deja `runs` chez Double.

**[HYPOTHESE, centrale pour le projet]** Prendre l'argmax de la distribution du
modele est une cause majeure d'ecrasement de la variance inter individuelle :
l'argmax de dix mille distributions differentes mais toutes centrees sur la
modalite majoritaire rend dix mille fois la meme reponse. Echantillonner dans la
distribution a temperature 1 devrait preserver davantage de variance au prix d'un
peu d'exactitude individuelle. C'est un arbitrage mesurable avec le dispositif
propose, et c'est peut etre le resultat le plus vendable du projet. Il faut donc
que `temperature`, `top_p` et la strategie de decodage soient des colonnes de la
trace, pas des constantes du code.

## 2.5 Le harness d'interrogation en lot

Ce que le harness doit garantir, dans l'ordre.

**Idempotence.** Un index unique sur `(run_id, person_id, item_id, repetition)`.
La reprise apres interruption devient gratuite : on relance, ce qui existe est
saute. C'est le meme principe que `track` chez Double, descendu d'un cran.

**Concurrence bornee et un seul ecrivain.** N workers qui appellent le modele,
une file, un unique thread qui ecrit dans SQLite. C'est le point precis ou le
systeme casse a l'echelle (voir 2.9), et le design le neutralise d'emblee.

**Limitation de debit par fournisseur.** Un seau a jetons par fournisseur, et un
disjoncteur : au dela de K erreurs 429 consecutives, le fournisseur est mis en
pause plutot que sature de reessais. Sans cela, un plafond gratuit se transforme
en echec total du run.

**Plafond de cout effectif.** Calcule sur nos propres tarifs, jamais sur le champ
`cost` du fournisseur. Lecon directe de `tarifs.py` et du commit `12e2a2b`.

**Cache litteral, jamais semantique.** Cle exacte :
`(representation@version, empreinte_persona, item_id, prompt@version, fournisseur,
modele, temperature, top_p, graine, repetition)`. Deux items differents ne partagent
jamais une entree. C'est l'inversion assumee du choix de `council/cache.py`.

**Sonde avant lancement.** Reprise de `docs/INDUSTRIALISATION.md` : sur vingt
individus, mesurer les jetons par appel, la duree, le cout extrapole et la variance
observee sur les items cibles, puis rendre un devis. Un run de 10 000 agents ne se
lance pas sans devis.

## 2.6 Les metriques

Deux familles qui ne doivent **jamais** etre agregees en un chiffre unique. C'est
la lecon la plus directement transposable de `docs/recherche/evaluation.md` : un
score global masque exactement ce qu'on cherche.

### Famille 1, individuelle : "cet agent est il cette personne"

| Metrique | Definition | Remarque |
|---|---|---|
| `exactitude` | part des items cibles ou la reponse codee de l'agent egale la reponse reelle | Sur echelle ordonnee, definir explicitement si l'egalite est stricte ou a un cran pres, et publier les deux |
| `exactitude_normalisee` | `exactitude / plafond_test_retest` | **Ne se calcule que si le jeu fournit un retest.** Sinon on publie l'exactitude brute en le disant. C'est le denominateur du 83 / 82 / 86 % du papier de 2024. |
| `kappa` | kappa de Cohen par individu, sur ses items cibles | Corrige l'accord du au hasard, indispensable sur des items binaires ou une piece de monnaie fait 50 % |
| `erreur_ordinale` | ecart absolu moyen en rangs, sur les echelles ordonnees | Distingue "se trompe d'un cran" de "se trompe de tout" |
| `taux_echec_format` | part des appels ou aucune modalite valide n'a pu etre extraite | Non nul et jamais zero : un item systematiquement illisible qui disparait silencieusement fausse tout |

### Famille 2, populationnelle : "cette population simulee est elle cette population"

C'est ici que se joue la contribution annoncee du projet. Toutes ces metriques sont
calculees **par item**, jamais moyennees a l'aveugle, et **ponderees** par les poids
de sondage.

| Metrique | Definition | Ce qu'elle attrape |
|---|---|---|
| `ratio_ecart_type` | sigma(simule) / sigma(reel) sur les items ordonnes | **La metrique phare du projet.** Un ratio de 0,6 dit que la population simulee est 40 % moins dispersee que la vraie. C'est le chiffre qui doit figurer en tete du papier. |
| `distance_variation_totale` | demi somme des ecarts absolus entre les deux distributions de modalites | Distance de distribution pour un item nominal, bornee entre 0 et 1, lisible |
| `distance_wasserstein` | distance de transport optimal entre les deux distributions | Pour les echelles ordonnees, ou l'ordre des modalites porte du sens |
| `ratio_entropie` | H(simule) / H(reel) | Detecte l'appauvrissement du repertoire de reponses, complementaire de l'ecart type |
| `part_modale` | part des agents qui donnent la modalite la plus frequente, comparee au reel | **Detecteur d'effondrement modal.** Si 90 % des agents repondent pareil quand 35 % des humains le font, tout est dit en un chiffre. |
| `ecart_marginal` | ecart entre la moyenne simulee et la moyenne reelle | La metrique que la litterature dit deja bonne. A publier pour montrer qu'on la reproduit avant de montrer ou ca casse. |
| `distance_correlation` | norme de Frobenius de la difference entre matrice de correlation simulee et reelle | **Sous estimee et decisive.** Une population qui reproduit chaque marginale mais aucune correlation entre items n'est pas une population, c'est une collection de generateurs independants. |
| `couverture_modalites` | part des modalites reelles jamais produites par la simulation | Le modele n'utilise il jamais les extremes de l'echelle |
| `variance_intra_agent` | dispersion des R repetitions du meme agent sur le meme item | Distingue l'incertitude du modele de la diversite entre individus. Sans cette metrique, on ne sait pas si la variance observee vient des personnes ou du bruit d'echantillonnage. |

**La decomposition qui est le vrai resultat.** La variance totale observee se
decompose en variance inter agents plus variance intra agent. Un systeme peut
afficher une belle variance totale qui n'est que du bruit d'echantillonnage sur des
agents identiques. Mesurer les deux separement, grace aux `repetitions`, est ce qui
transforme une affirmation en resultat. C'est la raison pour laquelle `repetitions`
est un parametre de premiere classe de l'experience et non une option.

### Ce qui encadre tout chiffre publie

- **Bootstrap sur les individus**, 1 000 tirages, pour un intervalle de confiance.
  Vectorise en numpy, ce qui reste calculable sur CPU.
- **Comparaison systematique au baseline `demographique@1`.** Un resultat s'ecrit
  "X contre Y pour le baseline", jamais "X".
- **Correction pour comparaisons multiples** quand on teste des dizaines d'items.
- **Un filtre de fuite**, transpose de `docs/recherche/evaluation.md` : soumettre
  chaque item cible a un agent **sans aucun contexte individuel**, et mesurer son
  exactitude. Un item ou l'agent nu fait deja 80 % ne teste pas la simulation
  d'individu, il teste la connaissance des marginales du GSS acquise pendant le
  pre entrainement. Ces items doivent etre identifies et rapportes a part. **C'est
  la menace de validite numero un du projet entier**, parce que le GSS est
  massivement present dans les corpus d'entrainement publics.

## 2.7 Observabilite, des le premier jour

Exigence explicite de la mission : trace de chaque run, cout et duree par appel,
graine, version de prompt, version de modele.

### Le schema de trace, en deux niveaux

Un niveau `run` (une execution d'experience) et un niveau `appel` (un appel de
modele). SQLite, un fichier par run, dans le dossier de sortie du run.

```sql
-- Extrait illustratif. Aucun fichier n'a ete cree.

CREATE TABLE runs (
  run_id            TEXT PRIMARY KEY,   -- ULID, sert aussi de nom de dossier
  experience        TEXT NOT NULL,      -- nom du fichier d'experience
  config_sha256     TEXT NOT NULL,      -- empreinte du YAML resolu, apres defauts
  git_sha           TEXT NOT NULL,
  git_propre        INTEGER NOT NULL,   -- 0 si l'arbre de travail etait sale
  graine            INTEGER NOT NULL,
  jeu_id            TEXT NOT NULL,
  jeu_sha256        TEXT NOT NULL,      -- empreinte du fichier de personnes
  codebook_sha256   TEXT NOT NULL,
  split_id          TEXT NOT NULL,
  split_sha256      TEXT NOT NULL,
  n_individus       INTEGER NOT NULL,
  n_items           INTEGER NOT NULL,
  repetitions       INTEGER NOT NULL,
  verrou_sha256     TEXT NOT NULL,      -- empreinte de uv.lock
  python            TEXT NOT NULL,
  machine           TEXT NOT NULL,
  demarre_le        TEXT NOT NULL,
  termine_le        TEXT,
  statut            TEXT NOT NULL CHECK (statut IN ('en_cours','ok','echec','interrompu')),
  cout_usd_estime   REAL NOT NULL DEFAULT 0,
  duree_totale_ms   INTEGER,
  erreur            TEXT
);

CREATE TABLE personas (
  run_id            TEXT NOT NULL REFERENCES runs(run_id),
  person_id         TEXT NOT NULL,
  representation    TEXT NOT NULL,      -- "graphe@1"
  persona_sha256    TEXT NOT NULL,      -- empreinte du contenu canonicalise
  construit_le      TEXT NOT NULL,
  duree_ms          INTEGER,
  tokens_in         INTEGER NOT NULL DEFAULT 0,
  tokens_out        INTEGER NOT NULL DEFAULT 0,
  cout_usd          REAL NOT NULL DEFAULT 0,
  stats             TEXT NOT NULL DEFAULT '{}',  -- JSON : noeuds, aretes, tokens estimes
  PRIMARY KEY (run_id, person_id, representation)
);

CREATE TABLE appels (
  appel_id          INTEGER PRIMARY KEY,
  run_id            TEXT NOT NULL REFERENCES runs(run_id),
  person_id         TEXT NOT NULL,
  item_id           TEXT NOT NULL,
  repetition        INTEGER NOT NULL DEFAULT 0,
  representation    TEXT NOT NULL,
  persona_sha256    TEXT NOT NULL,      -- redondant avec `personas`, et c'est voulu
  prompt_id         TEXT NOT NULL,      -- "interrogation@3"
  prompt_sha256     TEXT NOT NULL,      -- empreinte du gabarit rendu
  fournisseur       TEXT NOT NULL,      -- local | groq | openrouter | claude_code
  modele            TEXT NOT NULL,      -- identifiant exact, jamais un alias
  modele_revision   TEXT,               -- sha256 des poids en local, en tete de version en distant
  temperature       REAL NOT NULL,
  top_p             REAL,
  decodage          TEXT NOT NULL,      -- logprobs | grammaire | json
  graine_appel      INTEGER NOT NULL,   -- derivee de (graine, person_id, item_id, repetition)
  demarre_le        TEXT NOT NULL,
  duree_ms          INTEGER NOT NULL,
  tokens_in         INTEGER NOT NULL DEFAULT 0,
  tokens_out        INTEGER NOT NULL DEFAULT 0,
  cout_usd          REAL NOT NULL DEFAULT 0,
  reponse_brute     TEXT,               -- la sortie telle quelle, jamais nettoyee
  reponse_code      TEXT,               -- le code de modalite apres analyse
  distribution      TEXT,               -- JSON des probabilites par modalite, si disponibles
  tentatives        INTEGER NOT NULL DEFAULT 1,
  statut            TEXT NOT NULL CHECK (statut IN ('ok','format_invalide','erreur','abandon')),
  erreur            TEXT
);

CREATE UNIQUE INDEX idx_appels_cle
  ON appels(run_id, person_id, item_id, repetition, representation, modele);
CREATE INDEX idx_appels_item ON appels(run_id, item_id);
```

Sept choix a justifier.

- **`reponse_brute` est conservee telle quelle.** Si le code d'analyse change, on
  recalcule `reponse_code` depuis la trace sans relancer un seul appel. C'est le
  "evaluer ne demande pas de generer" de Double applique a la reponse plutot qu'a
  la metrique. C'est aussi ce qui permet de corriger un bug d'analyse apres coup
  sans invalider une campagne entiere.
- **`graine_appel` est derivee, pas globale.** Elle se calcule comme un hash de
  `(graine du run, person_id, item_id, repetition)`. Consequence : rejouer un seul
  appel isole donne le meme resultat que dans le run complet, ce qui serait faux
  avec un compteur global sensible a l'ordre d'execution.
- **`git_propre`.** Un run lance sur un arbre de travail modifie n'est pas
  reproductible. Le systeme ne doit pas l'interdire (on experimente), mais il doit
  le marquer, et le generateur de rapport doit refuser de produire une figure
  publiable depuis un run sale.
- **`persona_sha256` est duplique dans `appels`.** Redondance assumee : elle permet
  de detecter qu'un persona a change entre deux runs qui se disent comparables.
- **`modele_revision` est distinct de `modele`.** "llama-3.3-70b" chez un
  fournisseur n'est pas une version, c'est un alias. En local, l'empreinte du
  fichier de poids est une vraie version.
- **`distribution`** est le champ qui rend possible tout le travail sur la variance.
  Vide quand le fournisseur ne l'expose pas, et le rapport doit dire lesquelles des
  metriques deviennent alors incalculables.
- **`statut` distingue `format_invalide` de `erreur` et d'`abandon`.** Reprise
  directe de la distinction `failed` / `interrupted` de `runs.py`, qui existe chez
  Double pour une bonne raison : un run interrompu reste exploitable, un run echoue
  ne l'est pas.

### La solution gratuite

**SQLite plus structlog, rien d'autre en v0.** Justification :

- cout nul, aucune inscription, aucune limite de retention, fonctionne hors ligne ;
- **le fichier de trace est lui meme l'artefact scientifique** a archiver a cote du
  papier, ce qu'aucune plateforme hebergee ne garantit sur le long terme ;
- c'est le motif deja eprouve dans Double, avec ses garde fous connus (WAL,
  `busy_timeout` a 60 s) ;
- une requete SQL repond a "combien a coute le run 3, et quels items ont echoue"
  sans aucun outil.

Si le besoin d'une interface visuelle apparait, deux options gratuites et
auto hebergeables, a evaluer a ce moment la et pas avant :

- **MLflow**, le plus proche du besoin "comparer des dizaines de runs avec leurs
  parametres et leurs metriques", fonctionne sur un magasin de fichiers local sans
  serveur [CONFIRME https://mlflow.org/ repond 200, licence Apache 2.0 a reverifier] ;
- **Langfuse** ou **Arize Phoenix**, orientes trace d'appels LLM, tous deux
  proposant une version auto hebergeable [CONFIRME https://langfuse.com/ et
  https://phoenix.arize.com/ repondent 200 ; les conditions exactes de la version
  gratuite sont [A VERIFIER]].

Recommandation ferme : **ne rien adopter au depart**. La trace SQLite est
suffisante, et une dependance a un outil tiers introduit un risque de perte de
l'artefact qui fonde le papier. Le rapport de Double sur les frameworks
d'evaluation montre d'ailleurs qu'un outil "de reference" peut cesser d'etre
maintenu en six mois (le cas RAGAS).

## 2.8 Reproductibilite

L'objectif : un tiers, a partir du depot, regenere un chiffre du papier.

**Sept regles, dont une est un aveu.**

1. **Aucun chiffre n'est saisi a la main dans le papier.** Chaque tableau et chaque
   figure est produit par un script qui lit une trace et porte son `run_id` et son
   `figure_id`. Un chiffre sans `run_id` n'existe pas.
2. **Environnement verrouille.** `uv.lock` versionne, version de Python epinglee,
   empreinte du verrou dans la trace [CONFIRME https://docs.astral.sh/uv/ repond 200].
3. **Les donnees ne sont pas versionnees, leur empreinte l'est.** Reprise directe
   de la posture `NOTICE.md` de Double, et rendue plus stricte parce qu'il s'agit
   de micro donnees individuelles. Le depot contient un script de recuperation qui
   telecharge le fichier officiel et **refuse de continuer si le sha256 ne
   correspond pas**. Un jeu de donnees mis a jour en silence est un mode d'echec
   documente des enquetes publiques.
4. **Une seule graine, propagee explicitement.** Elle gouverne l'echantillonnage,
   le decoupage, les permutations et l'echantillonnage des reponses. Aucun appel a
   un aleatoire global nulle part.
5. **Versions de modele exactes**, jamais un alias, et l'en tete de version du
   fournisseur relevee quand elle existe.
6. **Test de fraicheur, repris de Double.** Un test de CI compare l'empreinte des
   gabarits de `prompts/` et des fichiers d'experience a celles enregistrees dans
   le dernier rapport. Si un prompt a change sans campagne correspondante, la CI
   echoue. Sans ce garde fou, le dispositif pourrit en silence et un chiffre publie
   finit par ne plus correspondre a aucun prompt existant.
7. **L'aveu, et il doit figurer dans le papier.** [PROBABLE, comportement largement
   observe, mecanisme exact variable selon le fournisseur] Un modele servi par une
   API distante **n'est pas reproductible au bit pres**, meme a temperature 0 avec
   une graine : les fournisseurs changent les poids et la pile de service sans
   preavis, et le regroupement dynamique des requetes introduit du non determinisme
   dans les reductions en virgule flottante. La consequence pratique :
   - l'artefact reproductible est **la trace**, qui contient chaque appel et chaque
     reponse, et depuis laquelle toutes les metriques se recalculent a l'identique
     pour toujours ;
   - la **re execution** ne reproduit le chiffre que dans un intervalle, qu'il faut
     mesurer et publier (relancer le meme run deux fois et publier l'ecart) ;
   - le seul chemin vers une reproductibilite au bit pres est un **modele ouvert
     execute en local**, avec empreinte des poids, graine fixee et nombre de fils
     d'execution fixe. **Recommandation : faire tourner au moins une condition en
     local exactement pour cela**, et l'ecrire dans le papier. C'est un argument de
     serieux methodologique, pas une contrainte subie, et il coute zero euro.

**Le point d'entree du tiers** : `make reproduire`, qui va d'un clone propre au
rapport. Et un job de CI qui l'execute sur vingt individus avec un **modele
bouchon** deterministe (une fonction qui rend une modalite selon une regle fixe).
Aucun appel de modele, quelques secondes, cout nul, et le pipeline entier est
verifie a chaque commit. C'est la transposition exacte du "evaluer une reponse ne
demande pas de la generer".

## 2.9 Passage a l'echelle : ce qui casse, et ou

De 10 a 10 000 agents, sept choses cassent, dans cet ordre d'apparition.

**1. Le cout, en premier et de tres loin.** Le volume est le produit
`agents x items x repetitions x representations x modeles`. Un exemple chiffre :
10 000 agents, 30 items cibles, 5 repetitions, 3 representations, 2 modeles fait
**9 millions d'appels**. Sous budget zero, c'est hors d'atteinte par API facturee,
quel que soit le tarif. Ce qui survit :
- l'inference locale, dont le cout est en temps machine et non en argent ;
- les paliers gratuits (Groq, Google AI Studio, modeles gratuits d'OpenRouter),
  bornes par des limites de debit [A VERIFIER, ces limites changent souvent] ;
- `claude -p` sous abonnement, le motif de Double, qui n'est pas facture a l'appel
  mais qui n'a jamais ete concu pour ce volume.

La consequence de conception est qu'il faut **reduire le produit, pas esperer un
budget**. Leviers, du plus sur au plus dangereux : echantillon stratifie de 500 a
2 000 individus avec ponderation plutot que 10 000 (un echantillon pondere correct
donne une estimation valide, c'est le metier meme du sondage), moins d'items cibles
mais choisis pour couvrir les domaines, moins de repetitions sauf sur un
sous echantillon dedie a la mesure de la variance intra agent.

**2. Le regroupement d'items dans un meme appel.** C'est le plus gros levier de
cout (poser trente items en un appel divise le nombre d'appels par trente) et
**c'est aussi un danger scientifique**. Repondre a trente items d'un coup cree une
coherence interne artificielle et peut a lui seul reduire la variance mesuree. Ce
doit etre une **condition experimentale declaree avec son ablation** (un
sous echantillon interroge item par item, et l'ecart mesure), jamais une
optimisation silencieuse.

**3. La longueur de contexte, pour la memoire brute.** Un entretien de deux heures
represente de l'ordre de 15 000 a 25 000 mots [PROBABLE, sur la base de 130 a 160
mots par minute de parole spontanee], soit environ 20 000 a 33 000 jetons a
1,3 jeton par mot. Multiplie par le nombre d'appels, c'est la totalite du cout.
Deux attenuations : la **mise en cache de prompt**, puisque le persona est constant
sur tous les items d'un individu et que seul l'item change (a chainer par individu,
pas par item, ce qui impose que le harness ordonne son travail par individu), et le
passage a la representation en graphe, dont la compacite est le principal argument
d'echelle. Sur enquete plutot que sur entretien, ce probleme est bien plus petit,
ce qui est un argument de plus pour commencer par l'enquete.

**4. Le cout de construction des personas, pour le graphe.** C'est un poste que la
memoire brute n'a pas du tout. A 10 000 agents, construire un graphe par agent est
une campagne d'appels a part entiere, avant meme la premiere interrogation.
Mitigation obligatoire : construire une fois, mettre en cache par
`(person_id, split_id, representation@version)`, ne jamais reconstruire. Et
budgeter cette phase separement dans la sonde, sans quoi le devis est faux d'un
facteur important.

**5. Les ecritures SQLite. C'est le point de rupture technique precis.** Les
lectures montent sans probleme, les ecritures concurrentes non. Double a deja
rencontre ce mur et y a repondu par WAL plus `busy_timeout` a 60 s, ce qui suffit a
deux processus et pas a trente deux workers. Le design correct des le depart : les
workers ne touchent pas la base, ils poussent dans une file, **un seul thread
ecrit**, par lots de quelques centaines de lignes dans une transaction. Variante si
cela ne suffit toujours pas : un fichier SQLite par fragment, fusionnes a la fin.
Ne pas attendre la panne pour le faire.

**6. Le O(n^2) cache dans `sujets.py`.** `matrice_similarite` construit une matrice
pleine. Sur les quelques centaines de claims d'une personne c'est instantane. Si
la generalisation d'etiquettes du graphe est appliquee **entre** individus, sur des
centaines de milliers de noeuds, la matrice ne tient pas en memoire. Regle a poser
tout de suite : **toute operation entre individus doit etre en O(n log n)**, donc un
index approche de plus proches voisins et non une matrice pleine. Et se poser la
question de fond avant : generaliser entre individus est peut etre exactement ce
qui detruit la variance.

**7. La memoire du runner.** Ne jamais charger 10 000 personas en RAM. Lecture en
flux, un individu a la fois, et le persona libere des ses items traites.

**Deux points qui ne cassent pas**, contrairement a l'intuition : le calcul des
metriques (numpy vectorise, un bootstrap de 1 000 tirages sur 10 000 individus reste
rapide, a condition de ne pas l'ecrire en boucles Python), et le stockage (9 millions
de lignes d'appels avec reponses courtes reste de l'ordre de quelques gigaoctets,
ce que SQLite gere sans difficulte).

## 2.10 La pile technique, sous budget zero

| Brique | Choix | Cout | Verification |
|---|---|---|---|
| Langage et verrou | Python 3.12, `uv` | nul | [CONFIRME] https://docs.astral.sh/uv/ repond 200 |
| Stockage | SQLite (trace, resultats) plus JSONL ou parquet (personnes) | nul | motif eprouve dans Double |
| Lecture d'enquetes | `pyreadstat` pour SPSS et Stata | nul | [CONFIRME] https://pypi.org/project/pyreadstat/ repond 200 |
| Calcul | numpy, scipy | nul | [CONFIRME] https://numpy.org/ et https://scipy.org/ repondent 200 |
| Embeddings (regroupement) | fastembed sur onnxruntime, repris de Double | nul | deja eprouve sur la machine cible |
| Inference exploratoire | `claude -p`, motif `ClaudeCodeProcessor` | porte par l'abonnement | deja eprouve dans Double |
| Inference en volume | paliers gratuits : Groq, Google AI Studio, modeles gratuits OpenRouter | nul dans la limite des quotas | [CONFIRME] les trois consoles repondent 200 ; **les limites exactes sont [A VERIFIER]** |
| Inference reproductible | modele ouvert local via llama.cpp ou Ollama, poids epingles par sha256 | nul en argent, non nul en temps machine | [CONFIRME] https://ollama.com/ et le depot llama.cpp repondent 200 |
| Observabilite | SQLite plus structlog | nul | voir 2.7 |
| CI | GitHub Actions, palier gratuit, modele bouchon | nul | le fichier de CI de Double fait 20 lignes et est copiable |
| Suivi des donnees | empreintes sha256 dans le depot, donnees hors depot | nul | DVC evalue et ecarte pour la v0 : il resout un probleme (stockage distant versionne) que nous n'avons pas encore [CONFIRME] https://dvc.org/ repond 200 |

**Sources de donnees publiques, disponibilite verifiee au 2 septembre 2026 par une
simple requete HTTP** (un code 200 prouve que le site repond, **pas** que les
donnees sont librement telechargeables ni redistribuables) :

| Source | URL | Code | Interet |
|---|---|:---:|---|
| General Social Survey | https://gss.norc.org/ | 200 | **Le jeu du papier de 2024.** Priorite absolue. |
| European Social Survey | https://www.europeansocialsurvey.org/ | 200 | Comparaison transnationale, et un terrain europeen pour le volet francais |
| World Values Survey | https://www.worldvaluessurvey.org/wvs.jsp | 200 | Couverture mondiale, vagues repetees |
| Roper Center | https://ropercenter.cornell.edu/ | 200 | Archives de sondages d'opinion |
| INSEE | https://www.insee.fr/fr/statistiques | 200 | Terrain francais |
| data.europa.eu | https://data.europa.eu/ | 200 | Portail ouvert europeen |
| ANES | https://electionstudies.org/ | **403** | Le 403 sur une requete curl nue signale un filtrage anti robot, pas une absence. [A VERIFIER dans un navigateur] |
| ICPSR | https://www.icpsr.umich.edu/ | **403** | Idem |
| Eurobarometre via GESIS | https://www.gesis.org/en/eurobarometer | **403** | Idem |

**Point de droit non tranche, et il est bloquant avant le premier run.** Le fait
qu'un jeu de donnees soit accessible publiquement ne dit rien de la possibilite de
redistribuer des reponses individuelles dans un depot ou dans une trace archivee.
Or notre trace contient, par construction, les vraies reponses tenues secretes des
individus. Position par defaut a adopter en attendant la reponse, calquee sur
`NOTICE.md` de Double : **les donnees sources ne sont pas versionnees, seules leurs
empreintes le sont, et la trace publiee est expurgee des reponses reelles, qui sont
remplacees par un identifiant renvoyant au fichier officiel**. Cela suffit a
reproduire toutes les metriques pour qui a obtenu le fichier par la voie officielle.

---

# PARTIE 3. ARBORESCENCE DE DEPOT PROPOSEE

```
popsim/
  README.md                    ce qu'est le projet, et comment regenerer un chiffre
  CONTEXTE.md                  (existe deja) contexte et regles de redaction
  NOTICE.md                    position sur les donnees, licences, ce qui n'est pas redistribue
  CONTRIBUTING.md              installer, lancer, conventions
  Makefile                     `make reproduire`, `make eval`, `make sonde`
  pyproject.toml
  uv.lock                      verrouille, versionne
  .github/workflows/ci.yml     ruff, pytest, `make reproduire` sur modele bouchon

  exploration/                 la phase actuelle, documents des agents
    01-papiers-fondateurs.md
    ...
    08-architecture-technique.md   ce document

  donnees/                     NON VERSIONNE (.gitignore), sauf les empreintes
    brut/                      fichiers officiels tels que telecharges
    normalise/                 <jeu>/personnes.jsonl + codebook.json
    empreintes/                <jeu>.sha256  <-- versionne, lui

  jeux/                        declaration des jeux de donnees, versionne
    gss-2022.yaml              ou trouver le fichier, quel lecteur, quelles variables
    ess-11.yaml
  splits/
    gss-2022-split-a.yaml      contexte / cible / exclus, avec graine et version
  experiences/
    repro-2024.yaml            le produit cartesien a executer
    ablation-generalisation.yaml
  prompts/
    interrogation@1.md         gabarits versionnes dans le nom du fichier
    interrogation@3.md
    construction-graphe@1.md
  representations/
    demographique@1.yaml       parametres declaratifs de chaque representation
    memoire_brute@1.yaml
    graphe@1.yaml

  src/popsim/
    config.py                  motif repris de Double : dataclass gelee, lru_cache
    logging.py                 repris de Double presque tel quel
    trace.py                   schema runs / personas / appels, gestionnaire `track`
    modele/
      personne.py              Personne, Reponse, Tour, Codebook, Item, Split
      valider.py               refuse un fichier non conforme, comme `Question.__post_init__`
    chargeurs/
      enquete_spss.py          pyreadstat
      enquete_csv.py
      entretien_texte.py       branche entretien, plus tard
    representations/
      base.py                  le Protocol Representation
      demographique.py
      memoire_brute.py
      graphe.py
    agent/
      processor.py             adapte de Double : base + local + groq + openrouter + claude_code
      bouchon.py               modele deterministe pour la CI, aucun appel reseau
      decodage.py              logprobs / grammaire / json, et l'analyse de la reponse
    harness/
      runner.py                concurrence bornee, file, un seul ecrivain, reprise
      cache.py                 cache LITTERAL sur la cle exacte
      debit.py                 seau a jetons et disjoncteur par fournisseur
      sonde.py                 le devis avant un run complet
    metriques/
      individuelles.py
      populationnelles.py      ratio d'ecart type, TV, Wasserstein, entropie, correlations
      fuite.py                 agent nu sur les items cibles, menace de validite n.1
      bootstrap.py
    rapport/
      generer.py               trace -> tableaux et figures, chaque sortie porte son run_id
      comparer.py              deux runs cote a cote
    cli.py                     typer, chaque commande enveloppee dans `track`
    mcp/server.py              inspection qualitative d'un persona, priorite basse

  runs/                        NON VERSIONNE, sauf rapports/
    <run_id>/
      config-resolue.yaml
      trace.db
      journal.jsonl
  rapports/                    VERSIONNE : les rapports commites, historique des campagnes
    2026-09-20-repro-2024.json
    2026-09-20-repro-2024.md

  tests/
    test_personne.py           le validateur refuse ce qu'il doit refuser
    test_split.py              aucun item cible ne fuit dans le contexte
    test_trace.py              idempotence et reprise
    test_representations.py    empreinte stable, meme entree = meme empreinte
    test_metriques.py          sur des distributions construites a la main
    test_reproduire.py         `make reproduire` de bout en bout, modele bouchon
```

Trois regles portees par cette arborescence.

**La version est dans le nom.** `interrogation@3.md`, `graphe@1.yaml`. Un prompt ne
se modifie pas en place, il se duplique en incrementant. C'est laid et c'est ce qui
rend un chiffre publie retrouvable trois mois plus tard.

**`rapports/` est versionne, `runs/` ne l'est pas.** Reprise directe de la
proposition de `docs/recherche/evaluation.md`. L'historique des campagnes est du
contenu scientifique, les traces brutes sont des artefacts lourds a archiver a part.

**`donnees/empreintes/` est versionne alors que `donnees/` ne l'est pas.** C'est la
posture `NOTICE.md` de Double, rendue operationnelle.

---

# PARTIE 4. BACKLOG V0, ORDONNE PAR DEPENDANCE

Chaque tache porte son critere de fin. L'ordre est contraint par les dependances,
pas par l'interet. Les estimations sont donnees en heures de travail effectif et
sont [HYPOTHESE].

### Socle, rien ne peut demarrer avant

| # | Tache | Depend de | Critere de fin | Est. |
|---|---|---|---|---|
| **T1** | **Format Personne et Codebook, gele.** Definir les dataclasses `Personne`, `Reponse`, `Tour`, `Codebook`, `Item`, `Split`, et un validateur qui refuse a la construction un fichier non conforme, sur le motif de `Question.__post_init__` chez Double. | rien | Trois fichiers Personne ecrits a la main couvrent les trois cas (enquete categorielle, enquete numerique, entretien) et passent le validateur. Trois contre exemples volontaires (modalite absente du codebook, item cible present dans le contexte, code manquant non declare) sont **refuses avec un message qui nomme le defaut**. Le format est fige et tout changement ulterieur incremente sa version. | 6 h |
| **T2** | **Trace et protocole de run.** Schema `runs`, `personas`, `appels` de la section 2.7. Gestionnaire `track` a deux niveaux, adapte de `runs.py`. Index unique qui rend la reprise gratuite. Modele bouchon deterministe. | T1 | Un run factice sur 20 individus x 10 items x 3 repetitions avec le modele bouchon ecrit 600 lignes d'appels. **Relance : zero appel refait, run termine en moins d'une seconde.** Interruption au milieu puis relance : le run se termine et le total est exactement 600. `git_propre`, `graine`, `config_sha256` et `prompt_sha256` sont renseignes sur chaque ligne. | 8 h |
| **T3** | **Chargeur d'une enquete publique reelle vers le format Personne.** Cible : GSS. Lecture pyreadstat, construction du codebook depuis les etiquettes, traitement explicite des codes manquants. | T1 | N individus du GSS charges et valides par T1. Le sha256 du fichier source est enregistre. Un **rapport de chargement** liste les variables ignorees et pourquoi, les codes manquants rencontres par variable, et le nombre d'individus ecartes. Un test rejoue le chargement et retrouve **le meme sha256 du fichier de sortie**. | 10 h |

### Premiere boucle complete, sur le baseline

| # | Tache | Depend de | Critere de fin | Est. |
|---|---|---|---|---|
| T4 | **Protocole de decoupage.** Manifeste `splits/*.yaml`, avec la garantie qu'aucun item cible n'entre dans un contexte. | T1, T3 | Un test verifie sur le jeu reel que l'intersection contexte et cible est vide, et qu'aucun libelle d'item cible n'apparait dans le texte rendu d'un persona (verification textuelle, pas seulement structurelle). Le decoupage est reproductible depuis sa graine. | 4 h |
| T5 | **Abstraction `Representation` plus `demographique@1`.** Le Protocol, l'empreinte canonicalisee, le registre par identifiant versionne. | T4 | La meme personne rend deux fois la meme empreinte. Deux personnes differentes rendent deux empreintes differentes. Une representation inconnue leve une erreur qui liste celles qui existent, sur le motif de `targets.charger`. | 6 h |
| T6 | **`Processor` popsim.** Adapte de `enrich/processor.py` : base avec reessai, quatre implementations (bouchon, local, palier gratuit, `claude -p`), dataclass `Reponse` etendue a la duree, la graine, la revision de modele et la distribution. Table de tarifs locale. | T2 | Le bouchon et une implementation reelle passent le meme test de contrat. Le plafond de cout **se declenche reellement** sur un test qui simule un fournisseur annoncant un cout nul, ce qui est le bug `12e2a2b` de Double reproduit puis attrape. | 8 h |
| T7 | **Runner en lot.** Concurrence bornee, file, ecrivain unique, limitation de debit, disjoncteur, reprise. | T2, T5, T6 | 2 000 appels bouchons avec 16 workers, aucune erreur "database is locked", et le nombre de lignes est exactement 2 000. Un fournisseur simule qui rend 429 en rafale met le run en pause au lieu de le faire echouer. | 10 h |
| T8 | **Metriques individuelles.** Exactitude, exactitude normalisee (avec refus explicite de calculer sans plafond test retest), kappa, erreur ordinale, taux d'echec de format. | T7 | Calculees sur des jeux construits a la main dont le resultat est connu a l'avance, y compris les cas degeneres (un seul item, agent toujours identique, aucune reponse valide). Sans plafond test retest, l'exactitude normalisee **n'est pas produite** et le rapport le dit. | 6 h |
| T9 | **Metriques populationnelles.** Ratio d'ecart type, distance de variation totale, Wasserstein, entropie, part modale, distance de correlation, couverture de modalites, decomposition inter et intra agent, ponderation, bootstrap. | T7 | Toutes verifiees sur des distributions synthetiques a resultat connu, dont **un cas d'effondrement modal construit exprès** (tous les agents repondent la modalite majoritaire) que le ratio d'ecart type et la part modale doivent tous deux signaler. La ponderation est testee contre un calcul a la main. | 12 h |
| T10 | **Rapport reproductible.** Generation des tableaux et figures depuis une trace, chaque sortie portant `run_id` et `figure_id`. Refus de produire une figure publiable depuis un run marque sale. Comparaison de deux runs. | T8, T9 | `make reproduire` va d'un clone propre au rapport avec le modele bouchon. Deux executions rendent des fichiers **identiques a l'octet**. Un run avec `git_propre = 0` produit un rapport visiblement marque comme non publiable. | 8 h |

A la fin de T10, le systeme est complet de bout en bout sur le baseline
demographique, sans avoir depense un centime ni appele un vrai modele. C'est le
jalon a atteindre avant toute science.

### La science

| # | Tache | Depend de | Critere de fin | Est. |
|---|---|---|---|---|
| T11 | **Filtre de fuite.** Interroger un agent **sans aucun contexte individuel** sur chaque item cible, et rapporter son exactitude par item. | T7, T8 | Un tableau par item classe les items en "discriminant" et "connu du modele nu", avec un seuil declare. Les items connus du modele nu sont exclus du chiffre principal et rapportes a part. **Aucun chiffre principal n'est publie avant que ce tableau existe.** | 5 h |
| T12 | **`memoire_brute@1`.** Rendu en texte des reponses de contexte, et branche transcript. | T5 | L'empreinte est stable. Le nombre de jetons du contexte est mesure et remonte par `statistiques`. Un test verifie qu'aucun item cible n'y apparait. | 5 h |
| T13 | **Sonde.** Sur 20 individus, mesurer jetons, duree, cout extrapole et variance observee, puis rendre un devis avant un run complet. | T7, T12 | La sonde tourne en moins de deux minutes et rend un devis. Le cout reel du run complet correspondant s'ecarte de moins de 30 % du devis. | 4 h |
| T14 | **Premiere campagne reelle : reproduction du papier de 2024.** `demographique@1` contre `memoire_brute@1`, sur un echantillon stratifie du GSS, avec un modele gratuit. | T10, T11, T12, T13 | Un rapport commite dans `rapports/` donne l'exactitude des deux representations avec intervalles de confiance, **plus toutes les metriques populationnelles**, plus le tableau de fuite. Le resultat attendu, a confronter au papier : memoire brute nettement au dessus du baseline sur l'exactitude individuelle. Si l'ecart n'apparait pas, c'est le pipeline qui est en cause, pas le resultat de Stanford. | 8 h |
| T15 | **Condition locale bit reproductible.** Une condition entiere rejouee sur un modele ouvert local, poids epingles par sha256, graine et nombre de fils fixes. | T14 | Deux executions de la meme condition rendent **des reponses identiques a l'octet**. Une ligne du papier devient exactement reproductible par un tiers. | 6 h |
| T16 | **`graphe@1`.** Trois types de noeuds, quatre types d'aretes, fusion priorisee, generalisation des etiquettes (en reutilisant le regroupement agglomeratif de `enrich/sujets.py`), avec mise en cache par `(person_id, split_id, representation@version)`. | T5, T12, et la lecture de `01-papiers-fondateurs.md` | Un graphe se construit, s'inspecte, se serialise et rend une empreinte stable. Le cout de construction par agent est mesure et figure dans `personas`. Le graphe se reconstruit a l'identique depuis la meme personne et la meme graine. | 14 h |
| T17 | **`graphe_sans_generalisation@1`** et campagne d'ablation. | T16, T14 | Une campagne compare graphe avec et sans generalisation sur les metriques populationnelles. **Le chiffre attendu est le ratio d'ecart type.** Que l'hypothese d'homogeneisation se confirme ou non, le resultat est publiable. | 6 h |
| T18 | **Test de fraicheur en CI.** Empreinte des prompts et des experiences comparee au dernier rapport. | T10, T14 | Modifier un prompt sans relancer de campagne fait echouer la CI avec un message qui nomme le prompt et le dernier rapport concerne. | 3 h |

**Chemin critique jusqu'au premier chiffre publiable :**
T1 -> T2 -> T3 -> T4 -> T5 -> T6 -> T7 -> T8 -> T9 -> T10 -> T11 -> T12 -> T13 -> T14.
Environ 100 heures. Les taches T15 a T18 sont la contribution differenciante et non
la reproduction.

**Une seule regle d'ordonnancement a ne pas violer**, reprise verbatim de
`docs/recherche/evaluation.md` de Double : "ne pas corriger les defauts avant
d'avoir ecrit la mesure. Un correctif sans mesure prealable ne se prouve pas."
Appliquee ici : ne construire aucune representation sophistiquee avant que T9, les
metriques populationnelles, existe et tourne. Sinon on optimisera au jugement, sur
des reponses toutes plausibles.

---

## Ce que je n'ai pas pu verifier

- **`exploration/01-papiers-fondateurs.md` n'existait pas** au moment de la
  redaction, le dossier `exploration/` etait vide. Tout ce que ce document dit du
  "papier de 2026" (trois types de noeuds, grammaire d'aretes a quatre types,
  fusion priorisee, generalisation des etiquettes) reprend l'enonce de la mission
  **sans aucune verification independante**. Je n'ai pas identifie ce papier, je ne
  connais ni ses auteurs, ni sa date, ni ses resultats. La section 2.3 est a
  reprendre des que ce document existe.
- **Le lien donne dans CONTEXTE.md, https://arxiv.org/html/2603.28066v1, n'a pas ete
  teste.** J'ai verifie a la place arXiv 2411.10109, qui correspond au resultat
  decrit. Le rapprochement entre les deux references reste a faire par l'agent 1.
- **Les licences des jeux de donnees.** J'ai verifie que les sites repondent, rien
  d'autre. Je ne sais pas si le GSS, l'ESS ou le WVS autorisent la redistribution de
  reponses individuelles dans une trace publiee. **C'est bloquant avant le premier
  run**, parce que la trace contient par construction les vraies reponses tenues
  secretes.
- **ANES, ICPSR et GESIS ont repondu 403** a une requete curl nue. C'est
  vraisemblablement un filtrage anti robot et non une indisponibilite, mais je ne
  l'ai pas confirme dans un navigateur.
- **Les limites exactes des paliers gratuits** de Groq, Google AI Studio et
  OpenRouter en septembre 2026. Les consoles repondent, je n'ai lu aucune grille de
  quota. Tout dimensionnement de campagne qui en depend est provisoire.
- **Quels fournisseurs gratuits exposent les logprobs**, ce qui commande la
  strategie de decodage la plus interessante scientifiquement.
- **La capacite reelle de la machine.** `docs/DAT.md` de Double indique que la
  machine cible est un MacBook Air sans refroidissement actif. Je n'ai pas mesure ce
  qu'elle peut soutenir en inference locale, ce qui est pourtant la condition de
  T15 et le seul chemin vers un chiffre bit reproductible.
- **Je n'ai execute aucun code de Double.** Lecture seule. Je n'ai pas lance
  `double eval`, je n'ai donc aucun chiffre mesure par moi sur ce systeme. Les
  chiffres cites (purete de 0,21 pour Garry Tan, 10 942 documents, 5,8 M mots)
  viennent de son README et de ses documents de recherche, dates d'aout 2026.
- **L'ecart sur le nombre de tests** : le README annonce 104 tests, mon comptage de
  `def test` en donne 125. Sans importance ici, mais signale plutot que lisse.
- **Les chiffres de tokens par mot et de mots par minute de parole** utilises en 2.9
  sont des ordres de grandeur usuels, non mesures sur notre materiau.
- **Le comportement non deterministe des API distantes** est donne comme [PROBABLE].
  Je n'ai pas de source primaire a citer, seulement un comportement largement
  observe dont le mecanisme exact varie par fournisseur. A etayer ou a retirer avant
  publication.

## Questions ouvertes pour Simon

1. **Le denominateur.** Le papier de 2024 normalise par la consistance test retest
   des participants a deux semaines. Quel jeu de donnees public fournit un retest
   exploitable ? Si aucun, acceptes tu qu'on publie une exactitude brute face au
   baseline demographique, en disant explicitement que la normalisation du papier
   n'est pas calculable sur nos donnees ?
2. **De quelle variance parle t on exactement ?** Trois choses differentes se
   cachent sous ce mot, et elles font trois papiers differents : la dispersion inter
   individuelle sur un item donne, la structure de correlation entre items dans la
   population, et l'instabilite intra individuelle au retest. Laquelle est la
   contribution visee ? Ma proposition, a valider : la premiere en chiffre de tete,
   la deuxieme comme resultat secondaire fort et sous estime par la litterature.
3. **Le baseline demographique est il obligatoire dans le protocole ?** Je le tiens
   pour indispensable (74 % dans le papier de 2024, et un chiffre sans plancher ne
   veut rien dire). Confirmes tu qu'il devient une condition de premiere classe,
   avec le cout d'ingenierie que cela implique ?
4. **Ethique et droit sur les micro donnees.** Peut on faire figurer les vraies
   reponses tenues secretes d'individus reels dans une trace versionnee ou archivee
   a cote du papier ? Ma position par defaut, en attendant : non, la trace publiee
   est expurgee et renvoie au fichier officiel par identifiant. Cela suffit a la
   reproductibilite mais complique la vie d'un tiers.
5. **Argmax ou echantillonnage.** Cote psychologie, y a t il une position sur le fait
   qu'un agent doive repondre de facon deterministe ou etre echantillonne ? C'est
   probablement le levier numero un sur la variance, et c'est un arbitrage
   theorique autant que technique.
6. **Le regroupement d'items dans un meme appel.** C'est le plus gros levier de cout
   sous budget zero, et il cree une coherence interne qu'un vrai repondant n'a pas.
   Est ce disqualifiant pour un papier, ou acceptable comme condition declaree avec
   son ablation ?
7. **La reference en psychiatrie publiee dans Nature**, mentionnee dans CONTEXTE.md,
   reste a identifier. As tu la reference exacte ? Elle pourrait fournir un
   precedent methodologique sur la validation contre un plafond humain.
8. **L'acces MIT ouvre t il du calcul ?** Un acces a un cluster academique ne leverait
   pas la contrainte de budget zero sur les API facturees, mais il changerait
   completement l'echelle atteignable en inference locale, et c'est le chemin vers la
   condition bit reproductible.
9. **La branche entretien.** Vu que l'enquete seule atteint 82 % contre 83 % pour
   l'entretien, faut il encore concevoir le protocole d'entretien a 10 personnes
   maintenant, ou le geler jusqu'a ce que la reproduction sur enquete soit acquise ?
   Ma recommandation : le geler, et concevoir le format Personne de facon a
   l'accueillir sans reecriture, ce que fait le champ `tours`.
10. **Le chiffre de tete du papier.** Ma proposition est le ratio d'ecart type
    simule sur reel, par item, avec son intervalle de confiance, presente contre le
    baseline demographique et contre l'approche 2024. Est ce le bon chiffre a mettre
    en avant, ou la communaute attend elle autre chose ?
