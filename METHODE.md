# Méthode de recherche employée dans ce dépôt

Écrit le 12 septembre 2026, en lecture seule sur tout le dépôt à l'exception de ce fichier.
Aucun appel d'API, aucune recherche web, aucun commit, tout en avant-plan.

**Objet.** Ce document décrit *comment on travaille* : le processus complet, de l'idée à la
publication. Il ne fait ni le bilan des résultats, ni l'autopsie des échecs — `resultats/autopsie-methode-2026-09-12.md`
existe pour cela et n'est pas répété ici ; il est cité quand il établit un fait.

**Critère que je me donne.** Un chercheur extérieur doit pouvoir soit adopter ce processus, soit
démontrer qu'il est mauvais. Chaque règle est donc adossée à un cas réel du projet, daté, avec
son fichier, et chaque règle est classée **opposable** (un contrôle mécanique la fait respecter)
ou **souhaitée** (elle repose sur la discipline de celui qui l'applique). L'autopsie a établi le
fait qui gouverne tout le reste : « *les interdits nommés ont tenu ; les bonnes intentions non
nommées ont toutes cédé* » (§7.5). Une pratique décrite ici sans son contrôle est donc décrite
comme un vœu, pas comme une méthode.

**Ce que je n'ai pas vérifié.** Le coût en jetons et le temps-agent ne sont enregistrés nulle
part dans le dépôt ; je ne les invente pas. Les durées d'agent sont inférées des horodatages de
commit, qui bornent le travail par le haut. Les chiffres de comptage que je produis moi-même
sont accompagnés de leur commande ; ceux que je reprends sont attribués à leur fichier.

**État du dépôt au moment de l'écriture** : 139 commits, HEAD `af2384f` (12/09 19:29:15 +0200),
`origin/master` au même SHA — rien en retard de poussée. 62 fichiers dont le nom contient
`preenregistrement`, 1 043 fichiers dans `resultats/`, 254 fichiers Python dans `analyses/`.

---

## 1. Le cycle de travail, en huit temps

Le processus n'a pas été conçu puis appliqué ; il s'est stabilisé en trois jours, du 9 au
12 septembre, et l'ordre ci-dessous est celui qu'on peut lire dans l'historique. Chaque temps est
détaillé en §2 sous forme de fiche.

| # | Temps | Artefact produit | Qui peut l'écrire |
|---|---|---|---|
| 1 | Ouverture d'une piste | une ligne dans un document de tri (`resultats/tri-idees-2026-09-11.md`, `moonshots-2026-09-11.md`) | l'agent de tri |
| 2 | Pré-mortem, quand la piste est chère | `resultats/premortem-moonshot1-2026-09-11.md` | un agent qui n'a pas proposé l'idée |
| 3 | **Contrôle d'interprétabilité** de l'instrument | verdict `passe`/`EchecControleInterpretabilite` | le producteur, avant le préenregistrement |
| 4 | **Préenregistrement**, commis seul avant tout calcul | `resultats/X-preenregistrement.md` | le producteur |
| 5 | Exécution sous plafond et sous jeton de dépense | `data/traces/…`, `resultats/X.csv` | le producteur, seul |
| 6 | Résultats, y compris contraires | `resultats/X-resultats.md` | le producteur, seul |
| 7 | **Revue adverse** par un agent non producteur, avec recalcul | `resultats/…-audit-….md` | l'auditeur, qui n'écrit que son fichier |
| 8 | Entrée dans la **source unique de vérité**, puis dans le manuscrit | ligne dans `resultats/article-synthese.md`, puis `article/manuscrit.md` | un seul agent à la fois |

Deux temps s'ajoutent hors de cette chaîne : la **rétractation** (§2.7), qui peut intervenir à
n'importe quel point et remonte jusqu'aux documents déjà publics ; et le **sas humain** (§2.12),
qui retient toute action irréversible — envoi, dépôt, création de compte — hors du périmètre
d'écriture de tout agent.

La forme réelle de ce cycle, à l'échelle d'une journée, est lisible dans l'historique : 105
commits entre le 11/09 16:00 et le 12/09 08:00, avec un pic de 25 commits dans la seule heure de
01:00, puis 13 commits entre 16:46 et 18:50 « dont la quasi-totalité en réparation »
(`autopsie` §8.2). Le processus produit vite et répare longtemps ; c'est sa signature, et §4 en
tire les conséquences.

---

## 2. Les pratiques, une par une

Format de chaque fiche : ce qu'elle est — pourquoi elle existe — le cas réel qui l'a fait naître
— ce qu'elle coûte — comment on vérifie qu'elle a été respectée — **opposable ou souhaitée**.

### 2.1 Orchestration par agents parallèles sous mandat écrit

**Ce que c'est.** Le travail est découpé en tâches confiées à des agents lancés en parallèle.
Chaque agent reçoit un mandat autonome qui contient quatre éléments : (a) l'objectif, formulé
comme une question à trancher et non comme un livrable à produire ; (b) la liste des fichiers
qu'il peut écrire, et l'interdiction de tout le reste ; (c) les interdits de moyens — pas d'appel
payant, pas de réseau, pas de commit, tout en avant-plan ; (d) une conclusion courte, parce que
seul le texte final remonte à l'orchestrateur.

Le mandat n'existe pas comme fichier de configuration : il n'y a ni `CLAUDE.md`, ni `AGENTS.md`,
ni répertoire de consignes. **L'agent le ré-inscrit lui-même en tête de son propre rapport**, et
c'est cette réinscription qui en fait une trace auditable par un tiers qui n'a jamais vu les
instructions. Forme type, trois exemples réels :

- `resultats/audit-chiffres-2026-09-12.md` l.5-9 : « Aucun appel d'API, aucune recherche web,
  aucun commit. **Fichiers modifiés** : […] **Non touchés** : `article/latex/`, `resultats/c7-*`
  (**agents en cours**). »
- `resultats/audit-renversement-2026-09-12.md` l.5 : « **Lecture seule sur tout le dépôt sauf ce
  fichier.** Aucun appel de modèle, aucun réseau. »
- `resultats/troisieme-jeu-2026-09-12.md` : « Aucun compte créé, aucun formulaire rempli, aucune
  condition acceptée, **rien écrit hors de ce fichier**. »

**Pourquoi.** Le goulot d'étranglement n'est pas le calcul, c'est le nombre de questions qu'on
peut instruire en même temps. Un chantier comme C7 a produit 35 préenregistrements en une nuit ;
aucun agent séquentiel ne l'aurait fait.

**Ce que ça rapporte, chiffré.** Dans la fenêtre de 16 heures du 11/09 16:00 au 12/09 08:00 :
105 commits, 281 fichiers ajoutés sous `resultats/` dont 173 `.md`. Le dépôt compte 59 à 61
préenregistrements selon le périmètre de comptage (§2.3), dont 35 pour le seul chantier C7.

**Ce que ça coûte.** Trois coûts, tous documentés.
1. *La propagation d'erreur est parallélisée avec le reste.* Huit rapports périmés ont induit
   l'agent suivant en erreur dans la seule journée du 12/09 (`autopsie` §3.3), et dans trois de
   ces huit cas le document périmé était lui-même un rapport d'audit.
2. *L'orchestrateur ne voit que des conclusions.* Le coût de la journée lui a été annoncé
   « 0,32 $ » puis « 0,55 $ » alors qu'il s'agissait d'une seule ligne de dépense ; le total réel
   est d'environ 10,51 USD (`cout-api-2026-09-12.md` §2, repris par `autopsie` §8.1). Une
   conclusion courte est une compression, et une compression perd ce qu'elle ne sait pas être
   important.
3. *L'agent ne peut pas être joint pendant son travail.* Voir §2.2.

**Comment on vérifie.** Par lecture des en-têtes : un rapport sans déclaration de périmètre est
un rapport dont on ne peut pas savoir ce qu'il a touché. Aucun contrôle mécanique ne l'impose.

**Verdict : souhaitée.** Rien n'empêche un agent d'écrire hors de son périmètre ; le dépôt
contient un cas où c'est arrivé (§2.2).

### 2.2 Propriété exclusive des fichiers

**Ce que c'est.** Un fichier, un agent. Les autres l'ont en lecture seule, et ne recopient pas
une valeur détenue par un agent en vol — ils pointent sa source. `resultats/a-valider-2026-09-12.md`
§3 applique la règle explicitement : le recueil de préenregistrements est « **en cours de
modification par un autre agent** […] les chiffres exacts ne sont donc pas recopiés ici et
peuvent changer. **Se référer directement à ce fichier.** »

**Pourquoi, et le cas qui l'a fait naître.** Deux incidents distincts, de natures différentes.

*La collision de fichiers, 12/09 01:02.* Commit `f709645`, « Retire c7_generateur.py de mon commit
précédent (agent concurrent) », 2 fichiers, 341 suppressions. Son corps : « Ces deux fichiers […]
appartiennent au travail d'un **autre agent** […] et se sont retrouvés **indexés par accident**
au moment de mon commit précédent. Ce commit les retire du suivi git (les fichiers restent sur
disque, non modifiés, redevenus non suivis) sans toucher à leur contenu. » Le commit fautif était
signé Sonnet 5 ; le propriétaire légitime, Opus 5, a recommis son travail seul 21 secondes plus
tard (`2cb6874`, 341 insertions). Le contenu n'a rien perdu. Ce qui était en jeu est plus
subtil : commettre le préenregistrement d'un tiers dans un commit qui n'est pas le sien détruit
l'antériorité qui sert précisément d'argument anti-dragage (§2.3). C'est la seule collision de
fichiers de l'historique, sur 139 commits.

*La collision de verrous, 10/09 20:57:21.* `resultats/r6-incident-coordination-stop-2026-09-10.md` :
« `data/traces/STOP` a été créé pour empêcher le client R6 de poursuivre après les 429. **Ce
marqueur était global et partagé avec R7 ; il a donc arrêté Euler par effet de bord.** » Le
correctif est un cloisonnement de noms : R6 reconnaît désormais `STOP-R6` comme marqueur dédié et
continue de lire `STOP` global **en lecture seule** — « Le client ne crée ni ne supprime aucun de
ces marqueurs. » Validé par 197 contrôles, dont un test vérifiant qu'il ne modifie pas un témoin
R7.

**Ce que ça coûte.** L'isolement interdit la réparation. Un auditeur qui trouve une erreur ne
peut pas la corriger : il peut seulement l'écrire. Le 12/09 entre 11:25 et 11:36, l'auditeur de
`audit-renversement` a constaté que trois fichiers étaient modifiés par d'autres agents pendant
son audit (`article/manuscrit.md` 11:34, `article-synthese.md` 11:35, `figures_article.py` 11:34)
et n'a eu d'autre recours que d'écrire, en gras, dans son propre fichier : « **Si le §7 de
`c7-nul-corrige-resultats.md` est en train d'être appliqué au manuscrit, il faut l'arrêter
maintenant** ». Un ordre d'arrêt adressé à des agents injoignables, dans un fichier qu'ils ne
liraient peut-être pas.

**Ce que ça rapporte, et c'est le point le moins évident.** L'isolement ne sert pas seulement à
éviter les conflits : il **produit de la crédibilité**. L'autopsie l'isole comme l'une des quatre
conditions du seul dispositif qui ait attrapé une erreur fatale : « *l'auditeur ne pouvait pas
« réparer » et donc pas dissimuler* » (§7.1). Un audit qui a le droit de corriger peut effacer
la trace de ce qu'il a trouvé ; un audit en lecture seule ne le peut pas.

**Comment on vérifie.** *A posteriori seulement*, par `git show --stat` : un commit qui touche un
fichier hors du périmètre déclaré de son auteur est visible. C'est ainsi que `f709645` a été
détecté — à la main, après coup.

**Verdict : souhaitée pour les livrables, opposable pour l'argent.** Le seul verrou techniquement
contraignant du dépôt est `fcntl.flock` sur le grand livre de dépense partagé entre quatre
processus (`analyses/c5_api.py` l.112-144) — « valable entre threads et entre processus ».
Aucun `.lock` n'existe sur `article/manuscrit.md` ; la concurrence d'écriture y vit dans l'arbre
de travail, où git ne la voit pas (le manuscrit n'a que 9 commits au total, alors que plusieurs
agents y écrivaient simultanément).

### 2.3 Préenregistrement avant calcul

**Ce que c'est.** Avant tout calcul et avant tout appel payant, un fichier est commis **seul**,
contenant : les prédictions chiffrées, si possible avec leur intervalle *a priori* ; la règle de
décision, avec toutes les issues énumérées d'avance ; le résultat qui réfuterait ; les paramètres
figés ; le plafond de dépense ; et une clause anti-dragage.

Le meilleur exemplaire est `resultats/c7-factoriel-preenregistrement.md` (commit `ff90409`, 12/09
12:52:49). §4 prédit trois top-1 avec intervalle (M ≈ 20 % [0,08 ; 0,35], G ≈ 15 % [0,05 ; 0,30],
P ≈ 8 % [0,02 ; 0,20]) ; §5 énumère quatre issues dont un « rien montré » explicite, et ferme :
« **Aucun autre seuil n'est ajouté après coup. Le résultat rapporté est celui réellement obtenu,
quel qu'il soit, y compris s'il contredit les prédictions de la section 4.** » ; sa dernière
ligne est « **Aucun appel n'a encore eu lieu au moment où ce fichier est écrit et commité.** »

**La forme a évolué, et l'évolution est datable.** `resultats/r6-preenregistrement.md` (09/09
12:02) pariait de façon directionnelle — « H3 […] Pari : fausse […] **ce pari va contre la these
de R4 et peut couter** » — sans prédiction ponctuelle ni section « ce qui réfuterait ». Trois
jours plus tard, `c7-factoriel` porte prédiction ponctuelle, intervalle *a priori*, issues
énumérées, clause anti-ajout de seuil et tenue de compte. C'est le même dépôt, à 72 heures
d'écart.

**Proportion réelle des cas conformes.** Deux comptages coexistent, et je donne les deux avec
leur périmètre plutôt qu'un chiffre unifié :

| Périmètre | Méthode | Avant | Même commit | Après |
|---|---|---|---|---|
| 29 paires « Tier 1 » (C7 + Twin A→B) | `resultats/preenregistrements-recueil-2026-09-12.md` §2 | 24 propres + 1 prouvée | 3 | **0** |
| 61 fichiers `*preenregistrement*.md`, toutes paires confondues | `git log --diff-filter=A` sur chaque paire, recomputé pour ce document | **32** | **12** | **0** |

Les 17 fichiers restants du second comptage publient leurs résultats sous un autre nom (par ex.
`a44-generateur-nul.md`) ; un seul, `tab2`, n'a jamais produit de résultat.

**Aucune inversion nulle part.** Mais l'antériorité *de mise en git* n'est pas l'antériorité tout
court. Le dépôt le dit lui-même dans les messages de commit `5c4cef4` et `24cc79d` : « l'ordre des
commits établit une antériorité faible, pas une preuve ». **Un seul cas a une antériorité
prouvée** : `c7-factoriel`, parce que `git show ff90409:analyses/c7_factoriel.py` échoue — le
script producteur n'existait pas dans le dépôt au moment du préenregistrement. Je l'ai revérifié
pour ce document : le script est bien absent à ce commit.

**Régression à signaler, postérieure au recueil.** Les deux expériences commises après lui —
`c7-loi-distance` (`4ada4ac`, 18:42) et `c7-argyle` (`0000515`, 18:49) — mettent script,
préenregistrement et résultats dans un seul commit, c'est-à-dire exactement l'anti-patron que le
recueil désignait comme irréparable. La pratique du préenregistrement prouvé n'est donc pas
acquise : elle a été appliquée une fois, recommandée, puis non suivie deux fois le même soir.

**Ce que ça coûte.** Quelques dizaines de minutes d'écriture par expérience, et une contrainte
réelle : le préenregistrement de `c7-nul-corrige` contenait en §8 la réserve qui a détruit son
propre résultat, écrite avant tout calcul. Le coût est donc parfois de devoir publier contre soi.

**Ce que ça ne coûte pas, et c'est le fait le plus important de cette fiche.** Le seul
préenregistrement dont l'antériorité soit prouvée est celui de l'expérience la plus inutile de la
journée. `autopsie` §4.1 : « La discipline de préenregistrement, exécutée parfaitement, n'a rien
empêché. » Le préenregistrement protège contre le dragage de seuils ; il ne protège de rien
d'autre, et surtout pas d'un instrument qui ne mesure rien (§2.9).

**Comment on vérifie.** Mécaniquement, pour l'ordre (`git log --diff-filter=A`) ; mécaniquement,
pour l'antériorité forte (`git show <sha_prereg>:<script>` doit échouer et
`git show --stat <sha_prereg>` ne contenir qu'un `.md`).

**Verdict : opposable dans sa forme faible, souhaitée dans sa forme forte.** L'ordre des commits
est un fait public. L'absence du script au commit de préenregistrement, seule preuve réelle, n'est
imposée par aucun contrôle : c'est la porte G0.1, écrite et non câblée.

#### 2.3 bis — Amendements : le préenregistrement ne se retouche jamais

Pratique découverte au recensement, et non listée dans la commande : **un préenregistrement n'est
jamais édité**. On ajoute un fichier daté qui (i) nomme le commit ou le SHA du parent, (ii)
déclare s'il est écrit avant ou après le calcul concerné, (iii) délimite ce qu'il ne touche pas,
(iv) déclare sa non-rétroactivité. Dix-neuf fichiers `amendement|avenant|addendum` existent dans
`resultats/`. Trois régimes :

- *Avenant avant calcul* — `resultats/c7-bits-preenregistrement-avenant.md` (`26aaff4`, 12/09
  00:54:32) : « Le fichier principal […] (**commit 7ddb1c1**) reste inchangé ; cet avenant ajoute
  quatre points, écrits avant leur calcul. » Le résultat suit à 01:06:25.
- *Amendement instrumental prospectif scellé* — `resultats/r6-amendement-429-v2-2026-09-11.md` :
  « Il **ne modifie ni** le préenregistrement R6 […] ni les estimands, invites, cellules,
  fournisseurs, plafonds ou règles d'analyse […] Il **ne s'applique pas rétroactivement** ». Le
  scellement est mécanique : `r6-preuve-activation-amendement-429-v2-2026-09-11.md` consigne le
  SHA-256 du texte de l'amendement, et le drapeau `amendement_429_actif` ne passe à `true` que si
  `--amendement-429-sha256` correspond — vérifié sur 6 modèles, 136 vérifications, 0 échec. **Le
  code refuse de tourner sous un amendement dont le texte a bougé d'un octet.** C'est le seul
  endroit du dépôt où un texte de protocole est contraignant pour une exécution.
- *Amendement explicitement non préenregistré* — `resultats/r2b-amendement-regle-memoire.md` :
  « **Ecrit […] APRES avoir vu la premiere mesure et APRES que la regle preenregistree a fait
  feu.** Ce document n'est donc **pas** preenregistre […] pour que `r2b-preenregistrement.md`
  reste tel qu'il a ete horodate […] **sans une seule retouche.** Quiconque lit R2b doit lire les
  deux pages, et savoir que celle ci est venue apres. »

**Verdict : opposable pour R6 (scellement SHA-256 vérifié à l'exécution), souhaitée ailleurs.**

### 2.4 Revue adverse

**Ce que c'est.** Tout résultat favorable est confié à un agent qui ne l'a pas produit, avec un
mandat hostile explicite et l'obligation de **recalculer** plutôt que de relire. Le mandat type,
dans sa formulation la plus complète (`resultats/audit-renversement-2026-09-12.md` l.3-7) :

> « Auditeur adverse. Je n'ai pas produit ce résultat et je n'ai aucun intérêt à ce qu'il tienne.
> **Hypothèse de travail : le résultat est faux, et il est faux parce qu'il nous arrange.**
> **Lecture seule sur tout le dépôt sauf ce fichier.** […] Tout recalculé en avant-plan. »

La formule a des variantes stables : « relecteur senior en vie privée, **avis par défaut le
rejet** » (`revue-hostile-gel`), « relecteur hostile de NeurIPS, PNAS ou Political Analysis.
**Objectif : trouver avant lui ce qu'il trouvera** » (`a17-relecture-adverse.md`), « qui cherche
la phrase qui ne survit pas » (`a45-relecture-adverse-2.md`).

**Quatre obligations qui font la différence entre un audit et une relecture.**

1. *Recalculer, pas relire.* `r6-revue-adverse-instabilite.md` : l'auditeur contrôle le CSV et son
   rapport « **sans reprendre leurs résultats comme données d'entrée** ». Écart maximal avec les
   valeurs publiées : 4,68 × 10⁻⁷.
2. *Construire ce qu'on reproche.* `audit-renversement` §1.3 ne dit pas « ce témoin est mauvais » :
   il **fabrique le témoin manquant**, 12 configurations × 20 réplicats, « mêmes graines, mêmes
   fonctions importées que le script audité », et mesure. Coût : environ 130 secondes de calcul.
   Une relecture n'aurait rien trouvé — le défaut était dans le choix du nul, pas dans le code.
3. *Nommer la colonne de l'audité qui contient déjà la réfutation.* La concession de l'auteur
   (`c7-nul-corrige-reponse-audit.md`) tient en une phrase : « **Le chiffre était dans mon CSV et
   dans le tableau que j'ai moi-même imprimé ; je ne l'ai pas traité comme disqualifiant.** » Une
   objection formulée dans les données de l'autre ne se négocie pas.
4. *Dire aussi ce qui tient.* `audit-renversement` §0 bis : « **un audit doit le dire aussi** » ;
   `revue-hostile-gel` : « C'est **la partie la plus utile de ce rapport** » ;
   `revue-hostile-finale` : « **Ce qui survit — même si toutes les objections ci-dessus sont
   accordées.** C'est la partie qui importe. » Mécaniquement, c'est ce qui évite de jeter les bons
   résultats avec les mauvais.

**Deux pratiques annexes, découvertes et non listées dans la commande.**

- *L'échelle de preuve typée.* `a17` et `a45` imposent à chaque objection un statut : « **[VERIFIE]**
  si l'objection a ete reproduite par calcul […] **[PROBABLE]** si elle vient d'une lecture
  attentive des rapports sans recalcul, **[HYPOTHESE]** sinon. » Un auditeur qui ne peut pas
  recalculer doit le dire, au lieu de laisser croire qu'il l'a fait.
- *Le verdict est livré avec son coût et son texte de remplacement.* « D1 15 min, D3 20 min, D6
  1 h » ; « R1 *(minutes)*, R2 *(demi-journée)*, R6 *(une journée)* ». Et le texte :
  « LA PHRASE EXACTE QUE L'ARTICLE A LE DROIT D'ÉCRIRE », « Titre honnête », « Texte exact proposé
  pour le nouvel addendum OSF ». Un audit qui n'écrit pas le remplacement reporte le travail sur
  celui qu'il vient de contredire.

**Le cas fondateur.** 12/09, 11:25-11:36. `audit-renversement-2026-09-12.md` démolit un
renversement qui allait changer le titre de l'article, et gèle six modifications déjà prescrites
(titre, résumé, tableau 3, figure 2, compteur de réfutations). L'auteur concède intégralement :
« **Mon renversement tombe** », et concède le point le plus dur : « **Un test qui ne peut pas
échouer ne démontre rien.** »

**La revue adverse est aussi un instrument de blocage, pas seulement de correction.** Trois cas :
`r7-revue-independante-bloquante.md` bloque le lancement d'un pilote et **compile ses garde-fous
dans le code** (exclusivité de processus, mémoire ≥ 15 % vérifiée chaque minute, SHA-256 du
modèle final, hash des séquences d'IDs des tokenizers), avec un verdict conditionnel et
auto-exécutant : « AUTORISÉ CÔTÉ TECHNIQUE **DÈS DÉPÔT DU PLAN ET DE L'ADDENDUM** » ;
`r6-revue-adverse-readiness-v3.md` prononce un « **NO-GO** » et rédige lui-même le texte de
l'addendum à déposer avant tout GO ; `r6-revue-adverse-instabilite.md` interdit à une campagne de
partir « sous le GO consommé ».

**La confirmation est un livrable, pas un silence.** Le dépôt contient un commit entier dont la
conclusion est *rien à signaler* : `9b5d156` (12/09 07:27, Sonnet 5), « C7 : audit de cohérence
des chiffres Park - RAS », dont le corps recense les occurrences vérifiées et conclut « toutes
sont déjà des comparaisons légitimes ». Diff : 1 fichier, 2 insertions, 1 suppression.
`audit-chiffres` §4 contient le bloc de confirmations le plus dense : « les **60 renvois `§N.M`**
[…] vérifiés un à un contre leur cible. **Trois étaient faux** » ; « **environ 110 valeurs**
remontées jusqu'à leur rapport ou leur CSV source. **Aucune erreur de valeur ni d'arrondi** hors
les quatre corrigées ».

**Ce que ça coûte.** Le temps de recalculer, qui est d'un ordre de grandeur inférieur à celui de
produire (130 s pour démolir un résultat qui a coûté 2 × 3 977 s de calcul), plus le temps de
réparer ce que l'audit trouve — et c'est là que le coût est réel : 13 commits de réparation entre
16:46 et 18:50 le 12/09.

**Comment on vérifie.** L'audit est un fichier commis, avec son mandat en tête et le nom de
l'audité ; un résultat favorable sans fichier d'audit associé est visible par simple inspection de
`resultats/`.

**Verdict : souhaitée.** Rien n'oblige à confier un résultat favorable à un auditeur, et rien ne
distingue mécaniquement un audit qui a recalculé d'un audit qui a relu — sauf l'honnêteté de la
déclaration [VERIFIE]/[PROBABLE]/[HYPOTHESE], qui est elle-même déclarative.

### 2.5 Double vérification aveugle, par deux modèles différents, pour ce qui sort du dépôt

**Ce que c'est.** Tout ce qui quitte le dépôt — lettres de divulgation, manuscrit soumis —
traverse trois passes à périmètres disjoints : **le dépôt**, **le dépôt revu en aveugle par un
modèle différent**, **le monde extérieur**.

**Le cas fondateur et sa raison, énoncée sans détour** (commit `aa97d1f`, 12/09 17:44, 3 fichiers,
+303/−50) : « **Le responsable ayant indique qu'il ne les relirait quasiment pas**, ces lettres
ont ete verifiees trois fois de facon independante avant tout envoi : **une passe Opus, une
contre-verification Fable qui ne voyait pas la premiere, puis un controle externe des sources.** »

| Passe | Fichier | Qui | Périmètre | Réseau |
|---|---|---|---|---|
| 1 | rédaction + auto-vérification | Opus 5 | le dépôt | non |
| 2 | `resultats/contre-verification-lettres-2026-09-12.md` | **Fable, aveugle à la passe 1** | 39 affirmations remontées au CSV primaire | non |
| 3 | `resultats/verification-externe-lettres-2026-09-12.md` | — | les 3 points que le dépôt ne peut pas trancher | **oui, lecture seule** |

**Ce que la cécité mutuelle a trouvé et qu'une seule passe ne trouve pas.** Deux défauts d'un
genre particulier : un intervalle de confiance accolé à la mauvaise valeur (« le même intervalle
[0,937 ; 0,993] est, dans le manuscrit, celui de **0,969** ; la lettre l'accroche à **0,965** ») ;
et une borne fabriquée en croisant deux sources, présente dans aucune — « Aucun document ne
contient "0,974–0,985" ». Ce sont des erreurs qu'un relecteur qui a vu la première passe reproduit
au lieu de les voir, parce qu'il lit la valeur comme déjà vérifiée.

**Bilan chiffré de la passe 2** : 39 affirmations vérifiées (23 lettre 1, 16 lettre 2) ; 27
conformes ; 5 écarts ; 4 ambiguës ; 2 introuvables localement ; 1 réserve manquante. Soit 12 non
conformes sur 39. **Rendement des trois passes** : 9 corrections chiffrées et 4 corrections de
fond, ces dernières explicitement qualifiées « plus graves que les chiffres » (annonce de
réduction de menace, chiffre attribué aux mauvais items, affirmation sur un scénario non mesuré,
défense « à faible coût » jamais testée sur les données du destinataire).

**La passe 3 est la seule à toucher le réseau, et elle est bornée aux points que le dépôt ne peut
pas trancher** : le texte de consentement dans le PDF arXiv 2411.10109 (5 passages recopiés
verbatim, verdicts « Conforme au mot près » ×2), la licence OSF `t6g7k` vérifiée par deux sources
croisées (API : `"node_license": null` ; page publique : « No License »), les conditions NORC/GSS,
et quatre adresses de destinataires — dont une laissée en conflit non résolu (« **cet agent ne
tranche pas entre les deux** ») et une introuvable, la lettre n'en attribuant aucune : « **c'est
la bonne posture, à conserver.** »

**Ce que ça coûte.** Trois rédactions complètes de vérification pour deux lettres ; en pratique,
l'essentiel d'une fin d'après-midi.

**Comment on vérifie.** Les trois rapports sont datés et nommés dans le commit d'envoi.

**Verdict : souhaitée, mais la condition critique — la cécité — est vérifiable.** Le fichier de la
passe 2 déclare ce qu'il n'a pas vu : « un autre agent le modifie en parallèle, **ses corrections
ne sont pas prises en compte ici** ».

### 2.6 Source unique de vérité, par revendication

**Ce que c'est.** `resultats/article-synthese.md` (173 lignes) tient, pour chacune des **15
revendications A1–A15**, six champs dans un ordre stable : la thèse en une phrase ; `Autorisé :`
la formulation exacte entre guillemets (16 occurrences) ; `Chiffres :` valeur **toujours avec son
IC à 95 %**, effectif, et fichier source avec son § ; les réserves obligatoires ;
`INTERDIT :` les formulations proscrites (**32 occurrences dans le fichier**) ; `Limite :`.
S'y ajoute un journal de révision en ligne (`*Corrigé après… du 12/09*`).

Une entrée complète, verbatim, pour donner la densité réelle :

> **A10 — Échelle : ce que la taille du pool change.** Autorisé : « de N = 50 à N = 2 058, le
> rapport jumeau/démographie croît de 2,8 à 9,7. » Chiffres : top-1 53,2 % [50,0 ; 56,3] à N = 50
> → **20,7 % [20,7 ; 20,8]** à N = 2 058 ; part du plafond humain 57,0 % → 25,4 %
> (`c7-echelle-resultats.md`). INTERDIT, absolument : toute valeur au-delà de N ≈ 4 000 — loi
> puissance et loi logarithmique ajustées sur les mêmes 6 points donnent déjà 18,1 % contre 13,9 %
> à 2× la plage […] Limite : le modèle de Pitman-Yor […] n'a pas été implémenté, sa formule
> n'ayant pas pu être vérifiée de façon fiable.

**Pourquoi.** Sans propriétaire, une grandeur se met à exister en plusieurs exemplaires. Le cas
fondateur est documenté : le même top-1 de 20,7 % portait **quatre intervalles incompatibles**
([19,1 ; 22,5] au §5.2 du manuscrit, [19,0 ; 22,4] au §6, [18,96 ; 22,43] dans le CSV,
[19,0 ; 22,5] dans la lettre) et **trois graphies** (20,68 / 20,69 / 20,7 %). Le compteur de
réfutations a pris quatre valeurs successives dans la même journée (16 → 14 → 15 → 14). Le nombre
de fichiers de l'artefact a été compté trois fois par trois méthodes non déclarées (« nine », 10,
onze).

**Deux règles complémentaires, trouvées et à retenir.**

- *Le refus de fusionner des chiffres proches.* `contre-verification-lettres` §3 énumère **huit
  couples à ne jamais fusionner** : 31,15 vs 31,6 % ; 0,21/0,22/0,23 % ; 65,7 vs 65,51 % ; 20,7 %
  sur 60 items vs 33,1 % sur 40 ; 0,965 vs 0,969 ; 0,974/0,982/0,978/0,985 ; 9,2 vs 13,29 % ;
  3,55 vs 3,56 bits. La proximité numérique est un signal d'alerte, jamais une preuve d'identité.
- *Le geste inverse, fait proprement.* Commit `7f22fce` unifie 20,7 % sur [19,0 ; 22,4] parce que
  **deux dérivations indépendantes convergent** ([19,04 ; 22,41]), et **déclare ce qui n'est pas
  fusionné** : le 20,7 % [20,7 ; 20,8] de l'étude d'échelle, qui est un rééchantillonnage sur
  20 répétitions et non un bootstrap sur les personnes.

**Ce que ça coûte.** Une ligne à tenir par grandeur publiée, et l'obligation de donner deux noms
distincts à deux mesures distinctes.

**Comment on vérifie — et c'est le point faible.** `article-synthese.md` est une **source unique
de vérité éditoriale, pas mécanique** : c'est de la prose structurée par convention typographique,
qu'aucun script ne peut joindre à un manuscrit. Le registre tabulaire recommandé par l'autopsie
(`resultats/registre-chiffres.csv`, une ligne par grandeur : `grandeur | valeur | IC |
n_replicats | script | commit | csv_source`) **n'existe pas**. `resultats/registre-depenses.md`
existe mais est un tableau vide, en-têtes seuls, alors que le dépôt documente au moins
4,9949 USD (A9) et 0,5386 USD (factoriel) de dépenses réelles.

**Verdict : souhaitée.** Avec une nuance qui compte : la liste des 32 interdits est *grep-able*,
donc à un script d'une heure de devenir opposable. Ce script n'est pas écrit.

### 2.7 Rétractation sans effacement

**Ce que c'est.** Un rapport invalidé reçoit un bandeau en tête — blockquote inséré entre le titre
H1 et la première ligne du corps — qui porte : la date, la qualification en gras, **qui l'invalide
et quel document fait foi à la place**, et la distinction entre ce qui tombe (l'interprétation) et
ce qui reste (les mesures brutes, les coûts). **Rien n'est supprimé.**

Bandeau type, `resultats/c7-nul-corrige-resultats.md` :

> ## AVERTISSEMENT DE RÉTRACTATION — 12 septembre 2026
> **Ce rapport a été réfuté le 12 septembre 2026. Ses conclusions […] NE DOIVENT PAS ÊTRE
> APPLIQUÉES.** Il est conservé uniquement pour la traçabilité de l'historique scientifique du
> projet — rien n'y a été effacé.
> Font foi, à la place de ce document : `resultats/audit-renversement-2026-09-12.md` […] et
> `resultats/c7-nul-corrige-reponse-audit.md` (la concession de l'auteur de ce rapport lui-même :
> « Mon renversement tombe »).

Suit un bloc « **Ce qui est vrai à la place, en trois lignes** ». Le bandeau de
`c7-factoriel-preenregistrement.md` est plus intéressant encore, parce que le document n'est pas
fautif : « **rien à corriger dans ce texte, mais sa suite est invalidée** […] La discipline du
préenregistrement a donc été respectée, et elle n'a pas suffi. »

**La preuve que rien n'est effacé.** Commit `d8e0daf` (12/09 17:06:53), vérifié pour ce
document : **4 fichiers, 59 insertions, 0 suppression**. Son message déclare la propriété
lui-même — « Insertion pure, aucune mesure ni texte existant modifie (0 suppression) » — et motive
l'urgence : « Ces rapports sont deja pousses sur GitHub et affirmaient, sans avertissement, des
conclusions que l'arbitrage a invalidees. »

**Sur 139 commits, trois fichiers seulement ont jamais été supprimés**, dans deux commits, aucun
pour cause de conclusion gênante : `f709645` (retrait du travail d'un autre agent, fichiers
intacts sur disque) et `1d362d4` (un CSV d'extrapolation remplacé par un CSV de diagnostic, avec
le motif dans le message).

**Consignes préfixées plutôt que réécrites.** La même règle s'applique aux documents de pilotage :
`REPRISE-2026-09-12.md` l.7 « Ce fichier remplace la version du 11/09, **périmée** », et
`REPRISE-2026-09-10.md` reste sur disque. Le fichier s'auto-critique : « **Un rapport laissé sans
avertissement induit les suivants en erreur** […] Ce fichier lui-même en est un exemple : la
version du 11/09 se disait « largement périmée » sans dire par quoi. » Et un préenregistrement se
corrige par addendum daté en queue, jamais par réécriture : `c7-echelle-preenregistrement.md`,
« ## Addendum, 12 septembre 2026 (avant tout recalcul supplémentaire) […] **Portée corrigée** ».

**Ce que ça coûte.** Peu à l'écriture, beaucoup à la lecture : le dépôt contient des rapports
faux qu'il faut lire jusqu'à leur bandeau pour savoir qu'ils le sont. Et la latence est le vrai
coût : entre l'invalidation (17:00, commit `5f6da6e`) et la pose des avertissements (17:06), les
documents faux étaient publics sur GitHub.

**Comment on vérifie.** `git show --numstat` sur le commit de rétractation : une rétractation
correcte n'a que des insertions.

**Le marqueur de rétractation (12/09/2026).** Un rapport qui en invalide un autre **le déclare
explicitement**, par une ligne entière, à la colonne 0, dans le corps du rapport qui invalide :

    RETRACTE: resultats/<fichier>.md
    INVALIDE: resultats/<fichier>.md      (synonyme strict)

Rien d'autre sur la ligne, un seul fichier, chemin complet, mot-clé en capitales. La porte P4
(`outils/portes/entetes.py --retractation`) ne reconnaît **que** cette forme, et exige alors que
le fichier nommé reçoive `retracte_par:`/`fait_foi:` **dans le même commit** — le toucher sans
poser l'en-tête ne suffit pas. Un marqueur mal formé, ou nommant un fichier inexistant, fait
échouer la porte : une faute de frappe ne doit pas désarmer la règle en silence. Forme complète
dans `gabarits/entete.md` ; pour citer le marqueur sans le déclencher, l'indenter ou l'encadrer
de backticks.

**Pourquoi une déclaration et non une détection.** La porte a d'abord *deviné* l'invalidation
dans la prose — un mot d'invalidation et un nom de fichier à proximité. En une journée, quatre
faux positifs, quatre PR bloquées à tort : un renvoi `§N` attribué au mauvais fichier ; un
identifiant de registre CSV pris pour une déclaration ; un mot et un nom de fichier distants de
360 caractères dans le même paragraphe ; et, le plus net, la phrase « **ils ne sont pas
invalidés** », lue comme une invalidation faute de savoir lire une négation. Les trois premiers
ont été corrigés par raffinements successifs ; le quatrième montre que le raffinement ne suffira
jamais, parce que tout document qui *parle* de rétractation déclenche une porte qui devine.

**Ce que ça coûte, et c'est le vrai arbitrage.** La porte ne voit plus rien d'une invalidation
écrite en prose sans marqueur : ce faux négatif est silencieux, et la règle n'est opposable qu'à
qui pose le marqueur. On échange une détection large et bruyante contre une détection étroite et
fiable — le pari étant qu'une porte qui crie à tort quatre fois par jour finit désarmée, donc
qu'elle ne protège déjà plus rien. `--indice-prose` rejoue l'ancien filet large en **notes non
bloquantes**, seul rattrapage possible de ce faux négatif, à l'usage d'un relecteur humain.

**Verdict : opposable pour la moitié déclarée, souhaitée pour l'autre.** Poser le marqueur reste
une action volontaire — ça, rien ne le force, et c'est le trou qui subsiste. Mais une fois le
marqueur posé, la rétractation dans le même commit n'est plus négociable : la porte P4 tourne en
CI sur chaque PR, et ses cas d'échec ont été vus en rouge (`tests/portes/test_p4_entetes.py`).

### 2.8 Traçabilité publique

**Ce que c'est.** Tout est commis et poussé, y compris les échecs, et les messages de commit
racontent aussi ce qui est tombé. Vérifié pour ce document : `origin` = `https://github.com/AmirK-S/popsim.git`,
HEAD et `origin/master` au même SHA `af2384f`, zéro commit en retard.

**La forme des messages.** Sur 139 commits, hors lignes de co-signature : **75 commits (54 %) ont
un corps d'au moins 5 lignes**, 42 en ont au moins 10, moyenne 7,6 lignes. Environ un sujet sur
sept annonce un échec, une rétractation ou une auto-réfutation. Exemples de sujets :
« Arbitrage : deux experiences payantes mesuraient du bruit » (`5f6da6e`) ; « T2 requalifiee en
non testable : le compteur tombe a 14 » (`8df4e68`) ; « Article : réfuter l'axe unique
fidélité/identifiabilité après **auto-réfutation** C7 » (`0a12011`) ; « C7 : […] la loi
d'unification proposée est **réfutée** » (`19095cc`) ; « Reproductibilite : six scripts rejoues a
l'identique, **un trou bloquant** » (`547655a`).

**Le message de commit fait office de compte rendu d'arbitrage.** `5f6da6e` (12/09 17:00) tient en
sept paragraphes : le constat (« Ses jumeaux ne reidentifient la personne reelle qu'au taux du
hasard »), le dégât collatéral (« T2 n'est pas refutee - elle n'a pas pu etre testee. C'est une
limite de notre instrument, pas un resultat sur le monde »), ce qui tient malgré tout (les cinq
paliers du canal), la règle adoptée, et le piège associé (« la baseline depend du bassin »). Deux
autres méritent d'être lus comme des modèles : `8df4e68`, qui documente une correction qui
défavorise ses auteurs (« Baselines corrigees, et la correction nous defavorise […] Le mauvais
choix flattait ces bras ») ; et `af2384f`, qui laisse une question ouverte en clair (« A trancher
avant depot : deux compilations successives placent la frontiere du corps a la page 13 puis a la
page 12 »).

**Les entorses sont déclarées dans le commit qui les commet.** Deux cas : `f709645` (retrait des
fichiers d'un autre agent) ; et `0fba857`, « Veille d'anteriorite : **forcee malgre la regle
.gitignore** resultats/veille-*.md », avec son motif — « la regle visait des notes de veille
internes, pas un livrable ».

**Ce que la traçabilité ne couvre pas, par décision explicite.** `.gitignore` est commenté par
intention : « Microdonnees d'enquete : JAMAIS versionnees. Les licences ICPSR, NORC, Pew et
assimilees interdisent la redistribution, **et un commit git est une redistribution.** » Il pose
l'exception exactement inverse pour les résultats agrégés : `!resultats/*.csv` — « Ils ne
contiennent ni ligne individuelle ni identifiant […] et c'est ce qui rend les chiffres du projet
verifiables par un tiers sans acces aux microdonnees. » Licences (`e29a536`) : MIT pour le code,
CC BY 4.0 pour les textes, microdonnées hors périmètre.

**Ce que ça coûte.** L'écriture des corps de commit, et un risque réel : ce qui est poussé est
public avant d'avoir été audité. C'est ce qui a rendu nécessaire `d8e0daf`.

**Verdict : opposable pour l'état de publication (`git log origin/master..master`), souhaitée pour
la qualité des messages.**

### 2.9 Contrôle d'interprétabilité

**Ce que c'est.** La règle, telle qu'elle est écrite dans `article-synthese.md` A14 : « **aucun
bras expérimental n'est interprétable tant que son pipeline candidat n'a pas battu la baseline
démographique en top-1 contre les vraies réponses humaines**, sur le bassin et les items
réellement attaqués, baseline **recalculée sur ces lignes-là** et jamais reprise comme constante ».

Opérationnalisation, `resultats/controle-interpretabilite-2026-09-12.md` §2 : « Un candidat passe
seulement si la borne basse de son IC bootstrap à 95 % […] est strictement supérieure à la borne
haute de l'IC à 95 % de la baseline Demographics Only, calculée sur EXACTEMENT le même bassin et
les mêmes items. » Jamais une comparaison de points.

**Le cas qui l'a fait naître.** Deux campagnes payantes du 12/09 — le témoin « deux
organisations » et le plan factoriel — ont mesuré des contrastes entre jumeaux que nous avions
régénérés, sans vérifier d'abord qu'ils portaient une personne. Ils n'en portaient aucune : top-1
de 0,00 à 0,79 % contre 0,83 % attendu par hasard, là où un jumeau ne connaissant que quatorze
champs démographiques atteint 13,3 %. Coût : 1,0928 USD rendus nuls, trois rapports publics
rétractés, une contribution retirée du manuscrit, et une lettre à Columbia annonçant une réduction
de menace qu'il a fallu remplacer par une rétractation.

**Ce qui rend ce contrôle bon, et qui est généralisable.** Il ne rend pas la faute interdite : il
la rend **impossible à exprimer**. `controle_avant_interpretation()` **ne prend aucun paramètre de
baseline** ; elle la recalcule sur les mêmes indices que le candidat.

```python
def controle_avant_interpretation(indices_personnes, indices_items, codes_candidat,
                                   nom_candidat, paq=None):
    ...
    # Le bassin humain ET la baseline sont tranches sur EXACTEMENT les memes indices que
    # le candidat : c'est ce qui rend impossible de comparer a la baseline d'un autre
    # bassin (le second piege identifie cette nuit).
    humains = paq["codes"][REF_V4][indices_personnes][:, indices_items]
    demo    = paq["codes"][DEMO][indices_personnes][:, indices_items]
    ...
    passe = bool(r_candidat["top1_bas"] > r_baseline["top1_haut"])
```

L'exception `EchecControleInterpretabilite(RuntimeError)` porte dans sa docstring l'interdiction
de la rattraper : « *Ne JAMAIS attraper cette exception pour continuer a interpreter le contraste
qui en depend* ». Le module est conservateur par construction, et le dit : « *le sinistre de cette
nuit est un FAUX POSITIF […] en cas de doute, ce controle doit refuser de laisser interpreter,
jamais l'inverse* ».

**Le contrôle est montré en train d'échouer.** `analyses/test_controle_interpretabilite.py` :
**19 vérifications**, dont 15 sur les cinq jumeaux payés réellement rejetés (3 assertions chacun),
2 sur des cas synthétiques dégénérés, et 2 sur la contre-épreuve qui doit passer (`JSON Persona -
GPT4.1`, 38,92 % [30,96 ; 47,08] contre baseline 13,25 % [7,92 ; 19,46]). C'est l'application de
la règle « un contrôle qu'on n'a jamais vu échouer n'est pas un contrôle ».

**Ce que ça coûte.** « **Zéro appel, zéro dépense.** » Le coût est statistique, pas monétaire : à
bassin 120, l'IC de la baseline est large, et 6 des 7 jumeaux Twin non démographiques sont refusés
alors qu'ils portent un signal réel. La parade déclarée est d'agrandir le bassin, jamais
d'assouplir la règle.

**Ses limites, déclarées en §6 du rapport** : passer ne garantit pas l'interprétabilité, seulement
la non-disqualification ; le conservatisme produit des faux négatifs à petit bassin ; le contrôle
ne dit rien du mécanisme ; la reproduction exacte dépend de l'étiquette de graine de départage des
ex æquo (13,25 % ici contre 13,29 % dans l'arbitrage — écart signalé, non corrigé) ; la portée est
limitée au seul risque « générateur sans information individuelle ».

**Comment on vérifie, et la mauvaise nouvelle.** `grep -rn "controle_avant_interpretation" analyses/`
ne trouve que quatre fichiers : le module, ses tests, `c7_loi_distance.py` — où le contrôle est
véritablement éliminatoire, avec les configurations exclues tracées en CSV — et `c7_argyle.py`, qui
**ré-implémente la fonction localement** au lieu de l'importer, avec sa propre classe d'exception
et une signature différente. **Aucun script effectuant des appels payants ne l'importe** :
`c7_fort.py`, `c7_factoriel.py`, `c7_deux_organisations.py`, `c7_gen.py` — zéro occurrence.

**Verdict : opposable là où il est branché, souhaitée partout ailleurs.** Et la double
implémentation rouvre exactement le risque « deux implémentations irréconciliées » que l'autopsie
impute au sinistre. C'est la pratique la mieux conçue du dépôt et la moins câblée.

### 2.10 Les portes issues de l'autopsie

**Correction de comptage préalable.** La commande parlait de « sept portes ». L'autopsie n'en
définit pas sept : elle définit **quatre portes** (0 : avant de dépenser ; 1 : avant d'écrire dans
le manuscrit ; 2 : avant d'envoyer un courriel ; 3 : permanente sur le dépôt) contenant **vingt
contrôles** (G0.1-G0.5, G1.1-G1.6, G2.1-G2.5, G3.1-G3.4). Je le signale plutôt que de fabriquer
un compte à sept, parce que c'est exactement la défaillance décrite en §2.6 : une grandeur qui
prend plusieurs valeurs selon qui la recompte.

**Principe directeur, formulé par l'autopsie elle-même** (§6) : « *Une porte n'est une porte que
si un script sort avec un code non nul.* » Et (§3.4) : « rendre la faute **impossible à exprimer**,
pas interdite ».

**État réel des vingt contrôles, au 12/09 19:29.**

| Contrôle | Ce qu'il exige | État vérifié |
|---|---|---|
| G0.1 | préenregistrement commis seul, script absent du dépôt à ce commit | fait une fois (`ff90409`), **non câblé**, et non suivi deux fois le soir même |
| **G0.2** | le pipeline candidat porte une personne | **écrit et testé** (`28405b2` : 641 lignes, 19 vérifications), branché dans 1 script sur ~250 |
| G0.3 | lecture `total_usage` commise avant le premier appel | **manquant** : aucune lecture entre le 11/09 14:24 et 22:53 |
| G0.4 | plafond déclaré dans le préenregistrement et lu par le script | **pratiqué** : `c7-factoriel` plafond dur 1,00 USD, `ARRET_INTERNE_USD = 0,90`, et « `usage.cost` annoncé par OpenRouter, jamais une estimation » |
| **G0.5** | tout contrôle est montré en train d'échouer | **écrit, et appliqué pour la première fois 21 minutes après l'autopsie** — voir ci-dessous |
| G1.1-G1.6 | registre de chiffres, un intervalle par grandeur, rejeu depuis un clone nu, interdits grep-és, renvois résolus | **aucun n'existe** : ni `resultats/registre-chiffres.csv`, ni `analyses/verifie_chiffres.py` |
| G2.1-G2.5 | les cinq contrôles avant envoi d'un courriel | **pratiqués une fois à la main** (`aa97d1f`, dont G2.4 : « Lettres : signature alignee sur l'adresse d'envoi reelle », `8d43f1c` 17:55) ; aucun script |
| G3.1-G3.4 | rétractation dans le commit qui invalide ; verrou sur le livrable ; durée déclarée de tout script long ; aucune baseline en paramètre | G3.4 appliqué dans un module ; **G3.1 câblée** (porte P4 `--retractation`, sur déclaration par marqueur — §2.7) ; G3.2, G3.3 **absents** (`reproductibilite/USAGE.md` ne contient aucune durée) |

**Le cas frais de G0.5, et il est daté à la minute.** L'autopsie est commise à 19:08 (`c012828`).
À 19:29, `af2384f` applique sa porte la plus importante à un objet qui n'a rien à voir avec C7 —
la génération du titre LaTeX :

> « Eprouve dans les deux sens, conformement a la porte issue de l'autopsie - **un controle qu'on
> n'a jamais vu echouer n'est pas un controle** : titre bidon avec accent, %, deux-points :
> apparait bien dans le PDF compile et dans les metadonnees, verifie par pdfinfo et pdftotext ;
> titre vide ou sans H1 : sys.exit, code 1, main.tex bit-a-bit inchange. »

C'est le seul élément de preuve, à ce jour, que les portes se transmettent au-delà du chantier qui
les a fait naître. Un seul cas, vingt et une minutes après. Il ne prouve pas une habitude.

**Verdict global : deux contrôles sur vingt sont opposables, et un seul est branché.** Le protocole
corrigé est, à l'heure où j'écris, un document, pas un dispositif.

### 2.11 Gestion de la dépense : plafond déclaré, jeton à usage unique, verrou de grand livre

Pratique non listée dans la commande, et qui est pourtant la mieux outillée du dépôt.

**Trois couches.**
1. *Le plafond est déclaré dans le préenregistrement et lu par le script.* Exemples datés :
   `r6-preenregistrement-v2.md` (09/09) « **Plafond dur : 4,50 USD** […] sur un solde d'environ
   6 USD lu avant le premier appel et inscrit. Reserve : 1,50 USD » ;
   `c7-deux-organisations-preenregistrement.md` (12/09) « Plafond strict de la tâche : 1,00 $ USD.
   Coût attendu : ≈ 0,34 $. Le script arrête tout » ; `c5-addendum-api` (11/09) « plafond dur
   partage 2,00 USD sur les 4 modeles (`usage.cost`) […] Arret a `data/traces/c5-api/STOP` ». La
   projection est comparée au réel après coup : le factoriel projetait ≈ 0,60 USD et a coûté
   0,5385601250 USD.
2. *Le jeton de dépense à usage unique.* Aucun appel payant ne part sans son fichier GO, et le GO
   est lié à ce qu'il autorise : `data/traces/GO-R6-campagne-deepseek-deepseek-v4-flash.json`
   porte `"model"`, `"queue_manifest_sha256"`, `"one_shot": true`. Consommé, il est archivé en
   `.consomme`. `STOP-R6` est recréé immédiatement après le dernier pilote.
3. *Le verrou de grand livre.* `analyses/c5_api.py` l.112-144 : `fcntl.flock` sur
   `LEDGER + ".lock"`, « valable **entre threads et entre processus** » ; dès que le plafond est
   atteint, le fichier STOP est posé. **C'est la seule exclusion mutuelle réellement contraignante
   du dépôt.**

**Ce que ça protège, et ce que ça ne protège pas.** Cela protège du dépassement de budget : la
comptabilité reconstruite indépendamment par `r6-revue-adverse-sept-pilotes.md` retombe
exactement sur le total publié (0,0342335066 USD), sans reste ni doublon. Cela ne protège pas de
dépenser correctement pour rien : les 1,0928 USD du §2.9 ont été dépensés **sous plafond, dans les
règles, et rendus nuls**.

**Verdict : opposable.** C'est, avec le contrôle d'interprétabilité branché et `artefact/garde.py`,
l'un des trois seuls dispositifs mécaniques du dépôt. Il est révélateur que le mieux protégé soit
l'argent, et le moins protégé le manuscrit.

### 2.12 Le sas humain : les actions irréversibles restent hors du périmètre de tout agent

Pratique non listée, et structurante. Aucun agent n'envoie un courriel, ne crée un compte,
n'accepte une condition d'utilisation, ne dépose sur OSF. Ces actions sont rassemblées dans une
file d'attente unique, `resultats/a-valider-2026-09-12.md`, dont l'en-tête définit le rôle :
« Une seule page pour les quatre actions que le responsable doit accomplir lui-même. Rien n'a été
envoyé, rien n'a été déposé en ligne, aucun compte n'a été créé. »

Chaque entrée porte sa durée estimée, ce qu'elle débloque, et sa dépendance à un agent encore en
vol — par ex. « **Attendre que le recueil de préenregistrements soit stabilisé par l'agent qui le
modifie**, puis le déposer soi-même auprès d'un tiers horodateur ». Son pendant amont,
`resultats/demandes-etat-2026-09-12.md`, établit les faits avant la décision, et corrige sans
effacer : le répertoire ne contient « pas huit lettres […] mais **sept** », et une lettre obsolète
est signalée comme telle sans être supprimée.

Le même principe borne la seule passe qui touche le réseau : « Vérification en lecture seule
(recherche web read-only, **aucun envoi, aucun formulaire soumis, aucun compte créé**) ».

**Verdict : opposable par construction dans ce mode de travail** (les agents n'ont pas les
capacités d'envoi), **souhaitée si ces capacités existent**.

### 2.13 Reproductibilité : le rejeu depuis un clone nu

**Ce que c'est.** Un agent clone le dépôt public dans un répertoire temporaire, recrée
l'environnement d'après `reproductibilite/ENVIRONNEMENT.md` (Python 3.13.14, versions épinglées),
lie `data/` en lecture seule, et rejoue les scripts qui produisent les chiffres de tête.

**Résultats, `resultats/reproductibilite-chaine-2026-09-12.md`** : `py_compile` sur les **254
fichiers** de `analyses/` → 0 erreur ; **6 scripts rejoués, code de sortie 0** ; **9 chiffres de
tête et 5 chiffres du canal A7 reproduits à l'identique, écart « aucun »**. Et un échec bloquant :
les trois scripts produisant le chiffre qui porte le titre n'étaient **pas versionnés** —
« *Ce n'est pas un script qui « ne tourne plus » : c'est un script qui n'a jamais été publié.* »

**Le sauvetage** (`sauvetage-scripts-temoin-2026-09-12.md`) les a retrouvés dans un seul des six
répertoires de session du scratchpad, celui encore vivant, et les a intégrés à `analyses/` sans
réécriture du code de calcul. Rejeu depuis le dépôt : rho marginal 0,9741, p5 0,9500, p95 0,9934 —
identiques aux valeurs publiées ; 148 s au total.

**Deux artefacts complémentaires.** `reproductibilite/` (5 fichiers, dont un aveu : « *Il ne
constitue pas encore une reproduction fraiche : il n'y a ni lockfile complet, ni manifeste de
sorties* »), et `artefact/` — un paquet autonome de relecture qui rejoue attaque et défense **en
une commande, en ~25 secondes, sans aucune donnée réelle ni personne réelle**, en important les
fonctions réelles de l'article. Son `garde.py` refuse de démarrer si `data/` est atteignable après
résolution des liens symboliques, de `..`, des barres inverses et de la casse — écrit après qu'un
rapport eut démontré **quatre contournements** de la version antérieure fondée sur des motifs de
chaîne.

**Verdict : opposable là où `garde.py` s'applique ; souhaitée pour le rejeu lui-même**, qui
dépend d'un agent recevant la mission explicite. G1.4 (« tout chiffre publié est rejouable depuis
un clone nu ») n'est pas automatisé.

---

## 3. Ce qui est opposable, ce qui est seulement souhaité

C'est la section que je considère comme la plus utile de ce document, et elle est courte.

**Opposable — un mécanisme fait échouer la faute :**

1. `fcntl.flock` sur le grand livre de dépense (`analyses/c5_api.py`) — entre processus.
2. Le jeton GO à usage unique lié au SHA-256 du manifeste de file, et le STOP en lecture seule.
3. Le scellement SHA-256 de l'amendement R6 : le code refuse de tourner si le texte a changé d'un
   octet (136 vérifications, 6 modèles).
4. `controle_avant_interpretation()` — impossible de fournir une baseline d'un autre bassin, parce
   qu'il n'y a pas de paramètre pour le faire ; **mais seulement là où la fonction est appelée**.
5. `artefact/garde.py` — résolution du chemin réellement atteint, pas de motif de chaîne.
6. `analyses/verifier_paquet_public.py` — refus d'archiver `data/`, traces, ledger, `.env`.
7. L'ordre des commits (`git log --diff-filter=A`) et l'état de poussée
   (`git log origin/master..master`) : des faits publics, non négociables.
8. G3.1 — porte P4 `--retractation` : **une fois le marqueur `RETRACTE:` posé**, le commit qui
   ne retracte pas le rapport visé échoue en CI. Opposable à la déclaration, pas au silence :
   une invalidation écrite en prose sans marqueur reste invisible (§2.7).

**Souhaité — rien n'empêche de ne pas le faire :** le respect du périmètre d'écriture d'un agent ;
la propriété exclusive d'un livrable ; l'appel du contrôle d'interprétabilité avant un appel
payant ; la revue adverse d'un résultat favorable ; le recalcul plutôt que la relecture ; la
cécité de la seconde passe ; l'unicité de la source de vérité ; **la pose du marqueur de
rétractation** (et donc, par ricochet, celle du bandeau) ; la qualité du corps de commit ; le
rejeu depuis un clone nu ; quinze des vingt contrôles du protocole corrigé — G3.1 quitte cette
colonne pour moitié seulement : son déclenchement reste volontaire, ses conséquences ne le sont
plus (§2.7).

**Le fait qui doit gouverner la lecture de ce tableau.** L'autopsie l'établit et je n'y ajoute
rien : les règles nommées et grep-ables ont tenu (les 32 interdits de `article-synthese.md` :
« Aucune violation », les six occurrences trouvées étant des retraits explicites) ; les intentions
non nommées ont toutes cédé le même jour. Une pratique de la colonne « souhaité » n'est pas une
règle faible : c'est une règle dont on sait, par observation, qu'elle cédera sous charge.

---

## 4. Limites de la méthode

### 4.1 Ce qu'elle ne protège pas

**Elle ne protège pas contre un instrument qui ne mesure rien.** Le préenregistrement décrit ce
qu'on s'attend à mesurer et à quel seuil on conclura ; il ne demande jamais si l'appareil mesure
quelque chose. Le meilleur préenregistrement du dépôt couvre l'expérience la plus inutile de la
journée. Le contrôle d'interprétabilité comble ce trou pour un risque précis — un générateur sans
information individuelle — et pour lui seul.

**Elle ne protège pas contre un contrôle qui ne peut pas échouer.** Deux cas dans la même nuit :
un garde-fou opérationnalisé comme `len(set(np.round(f, 12))) < 2`, c'est-à-dire un axe exactement
constant, « ce qu'un bruit continu ne produit jamais » — annonçant « 0/100 réplicats dégénérés »,
chiffre « exact et sans valeur » ; et un contrôle d'exactitude tautologique, qui mesurait la
sortie contre la cible qu'il venait lui-même d'écrire.

**Elle ne protège pas contre la propagation d'un chiffre entre rapports.** Trois mécanismes
documentés : chaque ré-implémentation refait son bootstrap et publie sa valeur sans que rien ne
désigne laquelle fait autorité ; une valeur est recopiée depuis le rapport le plus proche plutôt
que depuis la source, y compris depuis un rapport rétracté ; et deux sources se croisent pour
fabriquer une borne qui n'existe nulle part.

**Elle ne protège pas contre l'écriture concurrente dans un livrable**, parce que la concurrence
vit dans l'arbre de travail, où git ne la voit pas.

**Elle ne remplace pas une réplication externe.** `revue-hostile-programme-2026-09-11.md` §8 le
dit contre son propre camp : « Les « revues adverses/indépendantes » sont produites par **le même
dispositif d'agents** ; **elles ne valent pas réplication externe.** » Toute la construction de
crédibilité repose sur des agents du même modèle ou de modèles voisins, lisant le même dépôt.

### 4.2 Ce qu'elle coûte

**En argent** : environ 10,51 USD pour la journée du 12/09, dont 1,0928 USD (10,4 %) rendus nuls
par un défaut qu'un contrôle à zéro dollar arrêtait cinq fois sur cinq. Le solde restant sur la
clé est d'environ 5,77 USD sur 165.

**En calcul** : 2 h 12 (2 × 3 977 s) brûlées sur un rapport rétracté — la double exécution ayant
servi à prouver la reproductibilité bit à bit d'un résultat faux. Leçon à froid : la
reproductibilité est une propriété du calcul, pas une preuve de validité.

**En travail refait, sur une seule journée** : 3 rapports publics rétractés ; 6 modifications
d'article gelées après application partielle ; 20 corrections dans une seule passe d'audit des
chiffres ; 9 corrections chiffrées et 4 de fond dans les lettres ; 3 passes de vérification pour
deux courriers ; 8 cas de rapport périmé ayant induit l'agent suivant en erreur ; 4 valeurs
successives pour un même compteur ; 13 commits de réparation en deux heures.

**En proportion** : « tout ce qui a été produit entre 00:33 et 13:25 a été écrit, publié et poussé
sur GitHub ; tout ce qui s'est passé entre 17:00 et 18:50 est de la réparation. Cinquante minutes
d'arbitrage ont annulé dix-sept heures de production. »

**En jetons et en temps-agent** : non mesurable. Le dépôt n'en conserve aucune trace, et je ne
fabrique pas ce chiffre.

### 4.3 Le cas où la méthode a produit l'erreur suivante

C'est le point le plus instructif du document, et il concerne une contrainte de procédé, pas une
règle scientifique.

**La règle.** Aucun calcul en arrière-plan : « un agent qui lance un calcul long et attend son
réveil **ne se réveille jamais** dans ce mode de travail — tout doit tenir en avant-plan, quitte à
réduire les réplicats » (`REPRISE-2026-09-12.md`). La règle est correcte : sans elle, des agents
se perdent en attendant un réveil qui n'arrive pas.

**Ce qu'elle a produit.** L'auteur du témoin, vérifiant son résultat sous cette contrainte, a
réduit son calcul à **10 réplicats au lieu de 100, et les bits sur un seul réplicat** — réduction
honnêtement déclarée dans son rapport. Cette réduction produit **31,15 %** là où l'auditeur, qui
avait fait 20 réplicats, obtenait **31,62 %**. `audit-chiffres` §3.4 : « **rien dans le dépôt ne
réconcilie les deux implémentations** ». Les deux valeurs ont ensuite vécu côte à côte, et l'une
d'elles est arrivée telle quelle dans une lettre de divulgation destinée à des chercheurs
extérieurs. Le seul chiffre de bits d'identité publié (4,63) repose sur un réplicat unique.

**La leçon, et elle n'est pas « rétablir l'arrière-plan ».** Une contrainte de procédé légitime, en
l'absence de règle de déclaration, se transforme en divergence numérique dans un livrable. La
parade est double et elle n'est pas appliquée : tout script long doit exposer un paramètre de
réduction, **et toute valeur publiée doit déclarer son effectif de réplicats**. C'est le champ
`n_replicats` du registre qui n'existe pas.

**Deux autres exemples de la même famille.** Le bootstrap commun de la multiplicité, abandonné
parce que 170-200 s étaient jugées trop longues — « aucun essai ». Et `c7_disjoint.py`, rejoué à
`--splits 10 --nul 20` au lieu de 50/100 lors de l'audit de reproductibilité, donnant une valeur
« pas directement comparable » à la valeur publiée : le contrôle de reproductibilité a lui-même
produit un chiffre non comparable.

---

## 5. Ce qu'un critique attaquerait en premier

Écrit du point de vue de quelqu'un qui veut démontrer que cette méthode ne vaut rien. Les six
objections sont classées par ordre de dangerosité décroissante.

**1. « Vous vous auditez vous-mêmes, et vous appelez ça une revue indépendante. »** C'est la
critique la plus forte, et le dépôt l'a déjà formulée contre lui-même sans y répondre. L'auditeur
et l'audité sont des instances du même modèle, ou de deux modèles du même fournisseur, lisant le
même dépôt, avec le même contexte, et partageant les mêmes angles morts par construction. Que
l'auditeur trouve une erreur prouve seulement qu'un agent peut trouver l'erreur d'un autre agent ;
cela ne prouve rien sur les erreurs qu'aucun d'eux ne peut voir. L'« hypothèse hostile » est une
consigne de prompt, pas une divergence d'intérêt : personne n'y gagne rien à ce que le résultat
tombe. **Aucune des pratiques décrites ici n'a jamais été mise à l'épreuve par quelqu'un qui avait
intérêt à ce que le projet échoue.** La seule réponse honnête est que la méthode produit de la
vérifiabilité par un tiers, pas de l'indépendance ; et qu'un tiers, à ce jour, n'a rien vérifié.

**2. « Votre préenregistrement est déclaratif : vous certifiez vous-mêmes l'heure. »** Sur 29 à 61
paires selon le périmètre, une seule a une antériorité *prouvée*. Tout le reste repose sur l'ordre
des commits, que l'auteur contrôle entièrement — il suffit d'écrire les résultats puis de commettre
le préenregistrement seul, ce qui est **exactement ce que quatre fichiers du dépôt déclarent avoir
fait**, dans leurs propres messages de commit. Rien n'est déposé chez un tiers horodateur ; le
recueil qui sert de preuve n'est lui-même pas commis. Et le soir même où le recueil recommandait le
patron prouvé, deux expériences l'ont ignoré. Un relecteur peut donc légitimement refuser le mot
« préenregistré » dans le résumé — ce que deux revues internes ont déjà demandé.

**3. « Votre protocole corrigé est une liste de vœux : deux contrôles sur vingt existent. »** Le
document qui définit les portes a été commis à 19:08 ; à 19:29 une seule d'entre elles avait servi,
sur un objet mineur. Il n'y a ni registre de chiffres, ni script de vérification des chiffres, ni
verrou sur le manuscrit, ni hook de rétractation, ni durée déclarée pour un seul script. Le
contrôle d'interprétabilité, présenté comme le correctif central, **n'est importé par aucun script
qui dépense de l'argent** — et il existe déjà en deux implémentations divergentes, ce qui est la
pathologie même que l'autopsie dénonce. Un critique dira, avec raison, que ce dépôt est
remarquablement bon à écrire des règles et médiocre à les câbler, et que la fiche §2.10 le
concède au lieu de le réfuter.

**4. « Votre volume est votre problème, pas votre force. »** 105 commits en 16 heures, 1 043
fichiers dans `resultats/`, 59 préenregistrements, 254 scripts dont 6 rejoués. Un critique
soutiendra que la méthode est optimisée pour produire des artefacts, et que la plupart des
défaillances de la journée — huit rapports périmés lus comme courants, quatre valeurs pour un
compteur, quatre intervalles pour une grandeur — sont des **maladies du débit**, pas des accidents.
Ralentir aurait supprimé les erreurs que la méthode dépense ensuite son énergie à rattraper. La
réponse du dépôt (« c'est un défaut d'outillage, pas de vigilance ») est peut-être une façon de
refuser la conclusion la plus simple : trop d'agents écrivent trop vite dans trop de fichiers.

**5. « Vous confondez traçabilité et fiabilité. »** Le dépôt est intégralement public, les
rétractations sont visibles, les commits racontent les échecs — et il reste vrai que des chiffres
faux ont atteint des lettres destinées à des chercheurs extérieurs, que trois rapports ont affirmé
publiquement des conclusions invalidées pendant six heures, et que le chiffre portant le titre de
l'article a été produit par un script qui n'a jamais été publié et n'a été retrouvé que par accident
de calendrier. La transparence documente la faute ; elle ne l'empêche pas. Un critique
ajoutera que la rétractation sans effacement rend le dépôt honnête et **difficile à lire
correctement** : rien ne distingue, dans une liste de fichiers, un rapport valide d'un rapport
rétracté, et huit fois en une journée un agent a lu un périmé comme courant.

**6. « Vos mesures d'assurance produisent leurs propres erreurs. »** La contrainte d'avant-plan a
fabriqué deux valeurs irréconciliées dont une est partie dans un courrier. L'audit de
reproductibilité a rejoué un script en mode réduit et produit une valeur non comparable. Trois des
huit rapports périmés ayant induit un agent en erreur étaient des rapports d'audit, dont l'un
accusait à tort et a fait perdre du temps à corriger des choses justes. Le dispositif de
vérification a donc, de façon mesurable, une **contribution propre au taux d'erreur** — et aucune
des pratiques décrites ici ne mesure cette contribution.

**Ce qu'un critique ne pourra pas attaquer, et qu'il faut donc mettre en avant en premier** : la
méthode publie contre elle-même. Un commit annonce que deux expériences payées mesuraient du
bruit ; un autre que la correction de baseline défavorise ses auteurs ; un rapport d'autopsie
établit que la discipline centrale du projet n'a rien empêché ; le présent document classe seize
de ses vingt contrôles comme inexistants. Aucun de ces énoncés n'a été produit par une pression
extérieure. C'est la seule chose que la méthode démontre de façon non contestable, et ce n'est pas
une garantie de justesse : c'est une garantie que les erreurs, quand elles sont trouvées, sont
écrites.
