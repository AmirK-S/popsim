# r6, version 2. Page de plan et de depense : l'oracle des camps sur les modeles que le public utilise

Ecrite le 9 septembre 2026 apres 13:05, avant tout appel payant et sans aucun appel de modele.
Elle remplace `resultats/r6-preenregistrement.md` (v1, 10:20), qui n'est pas modifiee et reste
lisible a cote. Sources lues en entier : la v1, `r6-inventaire-openrouter.md`,
`verif-fournisseurs-2026-09-09.md`, `r5-resultats.md`, `r4-resultats.md`, `r1-resultats.md`,
`s1-resultats.md`, `s1-faisabilite.md`, `DECISIONS-CONSOLIDEES-2026-09-09.md`,
`protocoles/03-grille-d-audit.md`, `STRATEGIE-REFERENCE.md`, `analyses/r1_oracle_camps.py`, et
les traces `data/traces/r1-*.jsonl`, `r5-q4gab3.jsonl` pour les comptes de jetons.

Conventions : **[CONFIRME]** lu dans une source verifiee, **[MESURE]** calcule sur nos donnees
ou nos traces, **[PROBABLE]** interpretation etayee, **[HYPOTHESE]** proposition a tester.
Sans signes diacritiques, comme la v1.

---

## Verdict en trois lignes

**GO sous conditions, plafond dur 4,50 USD sur les 6 USD du solde, 1,50 USD de reserve non
engagee.** Conditions : (1) la verification locale de la voie `chat` sur Qwen3-4B passe, zero
euro ; (2) l'essai a blanc de dix cellules sur un modele `:free` passe, zero euro ; (3) chaque
modele payant n'entre qu'apres son essai de dix cellules facture et projete sous sa ligne de
budget. Le run est un run de description : rien du referent humain ne sort de la machine.

---

## Ce que la v1 disait et pourquoi ca change

1. **La v1 opposait « probabilites par lettre » et « dix tirages a temperature un ».** C'est un
   faux probleme importe du mode incarnation. **R1 n'a jamais lu une probabilite par jeton** :
   `MoteurR1.decrire` poste `temperature 0.0`, `top_k 1`, `n_predict 150`, et le parse lit un
   texte de K lignes `LETTRE: entier` dont la somme doit tomber dans [95 ; 105]
   [MESURE, `analyses/r1_oracle_camps.py`, lignes 143 a 146 et 361 a 371]. Le « troisieme mode
   moins cher » que la question 2 imagine, l'argmax a temperature zero, **est le mode de R1**.
   Il conserve 100 pour cent de R1 : meme invite systeme, meme bloc utilisateur, meme parse,
   meme evaluateur `r1_evaluer.py`. Les deux modes de la v1 sont tues ; l'inventaire des
   logprobs (`r6-inventaire-openrouter.md`, colonnes L et T) ne sert plus a choisir le panel.
2. **La v1 chiffrait 320 jetons d'entree et 0,6 million de jetons par modele.** Les traces disent
   autre chose : sous gabarit seul, 213 jetons d'entree en moyenne (mediane 202, maximum 496)
   et 23 de sortie sur Qwen3-4B, 209 et 16 sur gpt-oss-20b ; avec les trois exemples dans le
   tour utilisateur, 641 d'entree (mediane 634, maximum 829) et 19 de sortie
   [MESURE, `data/traces/r1-q4.jsonl`, `r1-oss20.jsonl`, `r5-q4gab3.jsonl`, comptes
   `tokens_prompt` et `tokens_generes` du serveur]. Le second format coute trois fois le premier
   a l'entree. La page v2 en tire un plan qui ne joue le format cher que la ou il est mesure.
3. **La v1 comptait un plafond de 25 EUR et quatre cles.** Le solde reel est d'environ 6 USD sur
   une seule cle OpenRouter [MESURE, `r6-inventaire-openrouter.md`, ligne 3 : 155 credits,
   148,96 utilises]. Toute la page est reecrite a cette echelle.
4. **La v1 mettait Gemini AI Studio et Mistral en gratuits « verifies le jour meme ».** Verifie
   ce matin : le niveau gratuit Gemini entraine sur les entrees et ses quotas ne sont plus
   publies ; Mistral n'a plus de niveau gratuit a quotas, seulement 10 USD de credits par mois
   sur inscription [CONFIRME, `verif-fournisseurs-2026-09-09.md`, section 1]. Ni l'un ni l'autre
   n'est une cle que nous avons. Les gratuits de cette page sont les modeles `:free`
   d'OpenRouter, a 1 000 requetes par jour puisque plus de 10 USD de credits ont ete achetes
   [CONFIRME, meme fichier, section 1, ligne OpenRouter ; solde de l'inventaire].
5. **La v1 pariait H3 fausse avant R5.** R5 a depuis mesure que les trois exemples portent
   +0,382 [+0,200 ; +0,578] sur +0,482, soit 79 pour cent de l'effet de format, le gabarit
   +0,101 [MESURE, `r5-resultats.md`, section 1.1]. La prediction que R5 impose est ecrite en H3
   ci dessous, en deux parts, dont une qui coute.
6. **La v1 disait « les plus gros modeles ».** Les tailles des modeles fermes ne sont pas
   publiees ; H4 n'etait pas decidable. Elle est remplacee par un contraste de palier a
   l'interieur d'une famille.
7. **La v1 ne disait rien des jetons de raisonnement.** C'est le seul poste qui peut faire
   exploser la facture : un modele qui raisonne 500 jetons avant ses 20 jetons visibles coute
   25 fois plus a la sortie. Chez gpt-oss-20b, R1 avait fixe `Reasoning: low` dans le gabarit
   harmony [MESURE, `r1_oracle_camps.py`, ligne 293]. L'equivalent API est un parametre
   de raisonnement au minimum, inscrit au registre, et l'essai de dix cellules mesure les jetons
   factures, pas les jetons visibles.
8. **La v1 ne disait pas que le meme identifiant OpenRouter peut etre servi par plusieurs
   fournisseurs**, parfois a des quantifications differentes. Le registre de la grille exige
   « quantification et format des poids » [`protocoles/03-grille-d-audit.md`, section 3.2].
   Chaque reponse enregistre le champ `provider` rendu par OpenRouter, et l'appel fixe l'ordre
   des fournisseurs avec repli interdit quand l'API le permet. [PROBABLE que le parametre est
   accepte pour tous les modeles ; verifie a l'essai]

---

## Question

Les modeles que le public interroge decrivent ils l'ecart entre camps comme les modeles locaux
de R1, R4 et R5, c'est a dire en le deplacant hors du plancher humain, en inventant de la
variete interne et en changeant de portrait selon le demandeur ? Et l'effet des trois exemples,
79 pour cent du facteur trois du format chez Qwen3-4B, se retrouve t il chez eux ?

## Ce qui sort de la machine

Le mode description seulement : l'invite systeme de R1 (« You are a survey research
assistant... »), la phrase d'identite du demandeur, le libelle GSS de la question et de ses
modalites, le camp decrit, et pour le second format les trois exemples de R4 dont les vecteurs
n'ont aucun rapport avec un axe politique [MESURE, `r5-resultats.md`, question 5 a Simon].
Aucune reponse individuelle, aucune fiche de personne, aucune distribution humaine : le
referent `data/traces/r1-distributions-reelles.csv` et son empreinte `ea7cd93e...91c811`
restent sur la machine [MESURE, `r5-resultats.md`, criteres de chute].

Sur les modeles `:free`, OpenRouter peut router vers des fournisseurs qui entrainent sur les
entrees ; la documentation dit que le refus d'entrainement dans les reglages du compte coupe
ce routage, avec des reglages separes pour le gratuit et le payant, sans preciser le defaut
[CONFIRME, `verif-fournisseurs-2026-09-09.md`, section 1 et « ce que je n'ai pas pu verifier »
point 4]. **Decision ecrite d'avance** : sur le gratuit, l'entrainement est accepte, parce que
ce qui sort est un libelle public d'enquete et une invite que le papier publiera de toute
facon ; sur le payant, le refus d'entrainement est active avant le premier appel et la
capture d'ecran du reglage est jointe au registre.

---

## Les trois usages de 6 USD, compares avant de choisir

| usage | cout | ce qu'il rend | usages du resultat | information par dollar |
|---|---|---|---|---|
| **A. R6 v2**, description sur le GSS, 14 modeles dont 3 gratuits, deux formats | 3,9 USD projete, 4,5 plafond | la colonne « modele proprietaire » que la grille declare vide [`03-grille-d-audit.md`, section 5.3, derniere ligne] ; A1, A2 signe, A4 par modele ; la replication du 0,79 de R5 sur des modeles d'autres familles, que R5 nomme comme non verifiee [`r5-resultats.md`, point 4] | quatre : tableau du papier, carte de demonstration de l'outil par la voie « point d'acces compatible OpenAI » [`STRATEGIE-REFERENCE.md`, chantier 2], piece jointe des deux lettres, et le premier point du suivi mensuel de l'addendum 4 de `DECISIONS-CONSOLIDEES` | environ 3,5 lignes de tableau par dollar, chacune sur trois quantites et deux formats |
| **B. Replication de s1 en incarnation** sur Twin-2K-500, CC BY 4.0 [CONFIRME, `a6-double-distorsion-hors-gss.md`, ligne 682], configuration « demographies seules », 300 personnes par camp, blocs QID287 et QID290, 6 modeles | environ 1,7 USD [MESURE derivee : 1 200 appels par modele a 300 jetons d'entree, prix de l'inventaire] | l'amplification du second ordre, mediane 3,21 chez les auteurs de Twin [MESURE, `s1-resultats.md`], sur des familles que Twin n'a pas testees | deux : un chapitre et le billet ; ni la grille, dont le bloc A est en description, ni l'outil dans son perimetre actuel | forte en nouveaute, mais elle mele un protocole neuf a un modele neuf, ce que R4 et R5 interdisent de lire comme un effet de modele ; et elle exige un script d'incarnation et une page de plan qui n'existent pas |
| **C. Ne rien depenser**, faire OLMo en local, garder 6 USD pour un rejeu demande par un cosignataire | 0 | rien aujourd'hui | zero jusqu'a la demande | indefinie ; c'est de la thesaurisation, et le cout marginal de A est sous 5 USD pour quatre usages |
| **D. Instrument mensuel**, deux modeles bon marche audites chaque mois | 0,15 USD par mois | une derive publiee | un, dans un an | bonne a long terme, nulle pour le papier des huit semaines ; A construit gratuitement le script que D reutilisera |

**Choix** : A, avec le plafond a 4,50 USD ; B est le candidat nomme pour la reserve de 1,50 USD,
sous sa propre page de plan, jamais sous celle ci ; D herite du script de A. [PROBABLE pour
les rangs, MESURE pour les couts]

---

## Modeles et fournisseurs, dans l'ordre

Un seul fournisseur d'acces, OpenRouter, une cle dans `.env` hors git [MESURE, inventaire].
Trois etages, joues dans cet ordre, chacun conditionne par le precedent.

**Etage 0, zero euro, avant tout appel payant.**

- Verification locale de la voie `chat` : `llama-server` sur Qwen3-4B-Instruct-2507 Q4_K_M,
  40 cellules tirees d'avance (liste ecrite dans `data/traces/r6-verif-cellules.txt` avant le
  lancement), envoyees deux fois : par `/completion` avec le gabarit ChatML rendu a la main
  comme en R1, et par `/v1/chat/completions` avec le gabarit applique par le serveur, comme le
  feront les API. Seuil : **au moins 38 distributions identiques sur 40** ; sinon la voie
  `chat` est inscrite au registre comme un protocole distinct, « gabarit serveur », et aucune
  comparaison directe avec R1 n'est ecrite. Cette verification remplace la verification
  « logprobs contre tirages » de la v1, qui ne mesurait pas la bonne chose.
- Essai a blanc du client OpenRouter sur un modele `:free`, 10 cellules, fichiers separes
  (`r6-smoke.jsonl`), jamais melanges au run.
- Puis les trois gratuits, en arriere plan, a 20 requetes par minute et 1 000 par jour
  [CONFIRME, verif section 1] : 1 210 cellules par modele, environ deux jours chacun si la
  limite journaliere est par compte [PROBABLE], soit quatre a six jours pour les trois.

**Etage 1, ouverts payants, du moins cher au plus cher.** Ils valident le circuit facture et
donnent six lignes pour moins d'un dollar.

**Etage 2, fermes, palier economique de chaque famille.** Puis **etage 3**, un seul palier
superieur, et un second seulement si la depense reelle le permet, voir le plafond.

Lecture par modele, partout : **texte a temperature 0, un appel par cellule, `max_tokens`
150, parse strict de R1, sans relance** (regle de R5 : un echec de premiere tentative est un
rejet publie, jamais rejoue [MESURE, `r5-resultats.md`, tableau des rejets]). `top_k 1` n'existe
pas sur les API fermees ; la temperature 0 en tient lieu et l'ecart est inscrit au registre.
Aucune sequence d'arret a la main : le texte est coupe par le parse. Raisonnement regle au
minimum offert par le modele, valeur inscrite au registre, equivalent du `Reasoning: low` de
R1 sur harmony.

**Le plancher machine, obligatoire sur chaque modele payant.** Une API a temperature 0 n'est
pas reproductible au bit pres comme un serveur local [PROBABLE]. Les 40 cellules de la liste
ci dessus sont rejouees une seconde fois sur chaque modele, format gabarit seul ; la distance
de variation totale moyenne entre les deux passes est publiee a cote de A4. Regle : **A4 n'est
lisible que si la distance entre identites depasse deux fois la distance entre passes.**
Cout : 40 cellules par modele, moins de trois pour cent du run.

---

## Plan de cellules par modele, et pourquoi il n'est pas celui de la v1

| format | cellules | jetons d'entree par cellule | jetons de sortie | ce qu'il sert |
|---|---|---|---|---|
| F1, gabarit seul, invite de R1 au caractere pres | 149 items x 3 camps x 2 identites = **894** | 210 | 20 | A1, A2 non signe et signe, A4, comparables a `q4` de R1 |
| F2, gabarit plus trois exemples de R4 dans le tour utilisateur, invite de R5 | 79 items orientes x 2 camps (gauche, droite) x 2 identites = **316** | 641 | 19 | le contraste de format sur A2 signe, la quantite exacte de T1 de R5 |
| plancher machine | 40 cellules de F1 rejouees | 210 | 20 | le denominateur de A4 |
| essai | 10 cellules de F1, deux fois | 210 | 20 | cout facture, rejets, determinisme |

Total par modele : **1 270 appels, environ 0,41 million de jetons d'entree, 0,025 million de
sortie** [MESURE derivee des comptes de jetons ci dessus, tokenizer Qwen ; les autres tokenizers
s'en ecartent de 15 pour cent au plus, PROBABLE]. Contre 1 788 appels et 0,572 million
d'entree dans l'inventaire : **le cout par modele vaut 0,68 fois la colonne « USD campagne »
de `r6-inventaire-openrouter.md`** pour un modele dont la sortie coute cinq fois l'entree,
ce qui est le rapport de prix typique de l'inventaire [MESURE derivee]. La version « deux
formats complets » de la v1 aurait coute 1,25 fois l'inventaire ; elle n'apportait sur F2 que
le centre et 70 items non orientes, qui n'entrent dans aucun test de format.

---

## Panel nominatif et cout

Colonne « inventaire » : `r6-inventaire-openrouter.md`, prix du jour. Colonne « v2 » :
inventaire x 0,68, arrondi au centime superieur. Aucun de ces modeles ne rend de logprobs
utiles a cette page, puisque la page n'en lit pas ; la colonne L de l'inventaire est rappelee
pour memoire seulement.

**Gratuits, `:free`, entrainement accepte, description sans microdonnee.**

| ordre | modele | inventaire | v2 | logprobs | note |
|---|---|---|---|---|---|
| 0a | `google/gemma-4-31b-it:free` | 0 | 0 | non | famille Google ouverte |
| 0b | `nvidia/nemotron-3-super-120b-a12b:free` | 0 | 0 | non | 120 milliards, gratuit |
| 0c | `nvidia/nemotron-3-ultra-550b-a55b:free` | 0 | 0 | non | le plus gros du panel, gratuit |

**Ouverts payants, prix bas, du moins cher au plus cher.**

| ordre | modele | inventaire | v2 | logprobs | cumul v2 |
|---|---|---|---|---|---|
| 1 | `deepseek/deepseek-v4-flash` | 0,057 | 0,04 | oui | 0,04 |
| 2 | `mistralai/mistral-small-2603` | 0,107 | 0,08 | non | 0,12 |
| 3 | `meta-llama/llama-4-maverick` | 0,139 | 0,10 | oui | 0,22 |
| 4 | `qwen/qwen3.7-plus` | 0,229 | 0,16 | oui | 0,38 |
| 5 | `moonshotai/kimi-k2.5` | 0,338 | 0,23 | oui | 0,61 |
| 6 | `z-ai/glm-5` | 0,412 | 0,28 | oui | 0,89 |

**Fermes, palier economique de chaque famille, en tirages ? Non : en texte a temperature 0,
comme tout le monde.**

| ordre | modele | inventaire | v2 | logprobs | cumul v2 |
|---|---|---|---|---|---|
| 7 | `openai/gpt-5.6-luna` | 0,157 | 0,11 | non | 1,00 |
| 8 | `google/gemini-3.8-flash` (tarif promotionnel jusqu'au 31/12/2026 [CONFIRME, verif section 3]) | 0,563 | 0,39 | non | 1,39 |
| 9 | `anthropic/claude-haiku-4.5` | 0,751 | 0,52 | non | 1,91 |
| 10 | `x-ai/grok-4.3` | 0,805 | 0,55 | non | 2,46 |

**Fermes, palier superieur, un seul assure.**

| ordre | modele | inventaire | v2 | logprobs | cumul v2 |
|---|---|---|---|---|---|
| 11 | `openai/gpt-5.4` | 1,967 | 1,34 | non | 3,80 |
| 12, conditionnel | `anthropic/claude-sonnet-5` | 1,502 | 1,03 | non | 4,83, **hors plafond sauf economie constatee** |

Frais d'essai et de plancher machine sur les onze payants : environ 0,10 USD [MESURE derivee,
50 cellules par modele]. **Total projete avec le 11 : 3,90 USD. Plafond dur : 4,50 USD.** Le
12 n'entre que si, au moment de le lancer, la depense reelle lue sur le solde est inferieure
ou egale a 3,45 USD, ce qui suppose que les tokenizers ou les prix aient joue en notre faveur.
Sinon il attend la reserve ou un solde nouveau.

Ce que dit ce panel et ce qu'il ne dit pas. Il couvre quatre familles fermees (OpenAI, Google,
Anthropic, xAI) au palier economique et une au palier superieur, six familles ouvertes servies
en API (DeepSeek, Mistral, Meta, Qwen, Moonshot, Zhipu) et trois gros ouverts gratuits. Il ne
couvre pas les paliers les plus chers (`gpt-5.5` 3,93, `claude-opus-5` 3,76, `gemini-3.1-pro`
1,57 [inventaire]) : « dix phares » valent 20 a 25 USD [CONFIRME, verif section 3], quatre fois
le solde. Quel modele l'application grand public sert par defaut n'est pas verifiable d'ici ;
le choix du 11 comme « palier superieur » est une convention inscrite au registre.
[HYPOTHESE que `gpt-5.4` est proche de ce que le public voit]

---

## Hypotheses, ecrites avant, et les paris

Quantites de la grille, bloc A [`protocoles/03-grille-d-audit.md`, section 2] : A1 dispersion
decrite sur reelle par camp ; A2 signe, ecart entre camps decrit sur reel, 79 items orientes,
plancher humain 1,009 ; A4 dependance au demandeur, plancher 1,00 par construction. Tous
calcules par `r1_evaluer.py --suffixe r6`, sans une ligne changee. Perimetre des fermes pour
les tests : les modeles 7 a 11, cinq modeles ; les ouverts et les gratuits sont descriptifs et
entrent dans le tableau sans test, sauf mention.

- **H1, la dispersion inter modeles.** Sur A2 signe, identite journaliste, parmi les cinq
  fermes : le rapport du maximum au minimum est superieur ou egal a 2 **et** les deux
  intervalles extremes sont disjoints ; ou bien un intervalle est entierement sous 1,009 et
  un autre entierement au dessus. Locaux de R1 : 0,245, 0,618, 1,268 [MESURE,
  `r1-resultats.md`, section 1.2]. Un test. **Pari : vraie.** En faveur de la these A5 de la
  grille ; ne coute rien.
- **H2, l'identite du demandeur.** Pour chacun des cinq fermes et pour les camps gauche et
  droite, A4 a une borne basse superieure a 2 et la distance entre identites depasse deux
  fois le plancher machine. Locaux : 2,74 a 4,23 [MESURE, `r1-resultats.md`, section 1.3] ;
  `q4gab3` : 2,92 a 3,23 [MESURE, `r5-resultats.md`, section 2.1]. Dix tests, Holm dans cette
  famille. **Pari : vraie sur au moins quatre modeles sur cinq.** En faveur.
- **H3, le format, ce que R5 impose.** Contraste apparie F2 moins F1 sur A2 signe, 79 items,
  identite journaliste, par modele ferme, bootstrap sur les items, permutation de signe
  appariee, cinq tests, Holm dans cette famille.
  H3a, direction : le contraste est positif, avec intervalle excluant zero, sur au moins trois
  fermes sur cinq. **Pari : vraie.** C'est la prediction que R5 impose : les exemples ouvrent
  l'ecart, +0,382 chez Qwen3-4B [MESURE, `r5-resultats.md`, section 1].
  H3b, ampleur : le contraste est superieur ou egal a +0,30 sur au moins trois fermes sur
  cinq. **Pari : fausse.** Les fermes partent de plus haut que Qwen3-4B, comme gpt-oss-20b a
  0,618 et Qwen3-30B a 1,268, et la marche sera plus courte ; un modele deja au dessus de 1
  peut meme etre pousse plus loin du plancher par les exemples. **Ce pari coute** : s'il est
  tenu, le « facteur trois du format » de la vitrine du papier est un fait de petit modele, et
  la contribution se reecrit « le registre du format est necessaire parce que l'effet varie
  d'un modele a l'autre », ce qui est moins vendeur. [HYPOTHESE]
- **H4, le palier dans une famille**, remplace « les plus gros modeles ». Pour chaque paire
  jouee, `gpt-5.4` contre `gpt-5.6-luna`, et `claude-sonnet-5` contre `claude-haiku-4.5` si le
  12 est joue : le palier superieur est plus proche de 1,009 sur A2 signe, contraste apparie
  sur la distance absolue au plancher, intervalle excluant zero. Un ou deux tests. **Pari :
  fausse**, le couple protocole et modele domine le palier. Ce pari va contre la monotonie
  observee en local (distances au plancher 0,755, 0,382, 0,268 pour 4, 20 et 30 milliards
  [MESURE derivee, `r1-resultats.md`, section 1.2]) et peut couter aussi. Si une seule paire est
  jouee, H4 est rendue « un test, non generalisable ».

Quatre familles de Holm : F1 un test, F2 dix, F3 cinq pour H3a et cinq pour H3b comptes
ensemble comme dix, F4 un ou deux. Jamais de correction entre familles. Aucun autre test.
Toute cellule des ouverts et des gratuits est descriptive et se lit sans p.

**Prediction annexe, hors familles, tranchee au comptage.** Les rejets de R5 etaient tous
arithmetiques et tous sur K superieur ou egal a 5 [MESURE, `r5-resultats.md`, rejets]. Chez les
fermes, le taux de rejet de premiere tentative est sous 1 pour cent sous les deux formats, et
aucun rejet ne touche un item a K egal a 2 ou 3. Si elle est fausse sur un modele, la lecture
de ce modele est marquee « format non tenu » dans le tableau.

---

## Depense

**Estimation avant essai**, par modele, ci dessus. **Essai**, par modele payant, avant sa
campagne : 10 cellules de F1 tirees d'avance, envoyees deux fois. L'essai mesure quatre
choses et arrete sur chacune.

| mesure | comment | seuil d'arret pour ce modele |
|---|---|---|
| cout reel par cellule | jetons factures lus dans `usage` de la reponse, jetons de raisonnement compris, et cout en USD relu par l'appel de generation d'OpenRouter ; projection sur 1 270 cellules | projection superieure a **1,5 fois** la ligne v2 : une seule correction autorisee, le raisonnement au minimum, puis nouvel essai ; si encore au dessus, le modele est retire et la ligne du registre le dit |
| jetons de raisonnement | `completion_tokens` moins jetons visibles | moyenne superieure a 50 : meme regle, une correction puis retrait |
| taux de rejet du parse | parse strict de R1 sur les 10 | plus de 2 rejets sur 10 : retrait, aucune reformulation d'invite n'est permise, l'invite est celle de R1 au caractere pres |
| determinisme a temperature 0 | distributions identiques entre les deux passes | moins de 7 sur 10 identiques : le modele est marque « non deterministe » et A4 n'y est lisible qu'a travers le plancher machine des 40 cellules |
| latence et refus de debit | erreurs 429 et duree par appel | plus de 3 erreurs sur 20 appels : attente d'une heure puis reprise ; jamais de seconde cle, la doc dit que cela ne change rien [CONFIRME, verif section 1] |

**Regle d'arret globale.** Avant chaque modele, le solde du compte est relu et inscrit ; le
modele n'est lance que si solde moins projection reste au dessus de 6,00 moins 4,50, soit
1,50 USD. La v1 acceptait un depassement de deux fois l'estimation ; a 6 USD ce n'est plus
acceptable, la marge est 1,5. Les criteres de chute 1 a 7 de R1 s'appliquent par modele, et
le critere 2, recopie de l'exemple de relance, est sans objet puisqu'il n'y a plus de relance.

**Alternative gratuite epuisee avant ?** Oui : les trois `:free` tournent d'abord et servent
d'essai a blanc du client. Ils ne remplacent pas les fermes, qui sont la question.

**Usages du resultat.** Tableau du papier, colonne « modele proprietaire » de la grille ; carte
de demonstration de l'outil, voie « point d'acces compatible OpenAI » ; piece jointe des deux
lettres ; premier point de l'instrument mensuel. Traces dans `data/traces/r6-<modele>.jsonl`,
memes cles que R1 (`version_prompt`, `cle_modele`, `modele`, `quantification` recevant le
fournisseur aval, `gabarit` valant `api-chat`, ...), jamais rachetees.

---

## Analyse

Meme evaluateur que R1, R4 et R5, memes 79 items orientes et leur pole declare avant, memes
149 items pour A1 et A4, bootstrap sur les items 2 000 tirages, permutation de signe appariee
20 000 tirages, estimateur de Phipson et Smyth, Holm dans les quatre familles ci dessus et
jamais entre elles. Pour comparer les fermes aux locaux sur A1 et A4, les valeurs locales sont
celles de R1 telles quelles ; pour le contraste de format, la valeur de reference est le
lambda de R5, 0,79 [0,60 ; 0,97], recopie, jamais recalcule.

Un script neuf, `analyses/r6_frontiere.py`, qui importe `systeme`, `utilisateur`, `parser` et
le bloc d'exemples de R4 sans recopier une ligne, et remplace `MoteurR1` par un client
OpenRouter a la meme signature `decrire(prompt, n_predict, arrets)`. Il refuse de lancer un
modele payant si `data/traces/GO-R6` n'existe pas, si l'empreinte du referent a change, ou si
le solde relu est sous la ligne. Dry run et verification hors ligne avant tout appel.

---

## Plafond et registre

**Plafond dur : 4,50 USD, toutes lignes confondues, sur un solde d'environ 6 USD lu avant le
premier appel et inscrit.** Reserve : 1,50 USD, non engagee par cette page, candidat nomme
l'usage B sous sa propre page. Aucun rechargement n'est demande par cette page ; si Amir en
decide un, la page ne change pas, seul le 12 entre.

Ligne a ecrire dans `resultats/registre-depenses.md` **avant** chaque appel payant, une ligne
par modele, completee apres :

```
| 2026-09-09 | OpenRouter, <id du modele>, fournisseur aval <provider> | solde avant <x,xx> USD, projection <y,yy>, plafond cumule 4,50 | <n> cellules, <r> rejets, cout facture <z,zz> | r6-resultats.md, tableau <A1/A2/A4>, ligne <modele> |
```

Et une premiere ligne, avant tout, pour l'etage 0 : « 2026-09-09, OpenRouter `:free`, 0 USD,
essai a blanc et trois gratuits, entrainement accepte sur le gratuit, refus active sur le
payant, capture jointe ».

---

## Ce que ce run ne pourra jamais dire

1. **Ce que l'application grand public repond.** Le run interroge une API avec notre invite
   systeme ; l'application a la sienne, inconnue, et peut-etre un autre modele. La phrase « ce
   que ChatGPT dit des camps » est interdite ; la phrase autorisee est « ce que le modele X,
   servi par Y, repond a cette invite ».
2. **Rien a la temperature de service.** La grille exige une seconde passe a la temperature
   servie au public avec 20 repetitions [`03-grille-d-audit.md`, section 3.3] ; elle
   multiplierait le cout par 20, soit environ 78 USD pour ce panel. Elle n'est pas jouee.
3. **Rien sur les personnes.** La description ne produit aucune reponse individuelle ; le
   bloc B n'y a pas de sens, et A2 est une quantite de gabarit que le generateur nul reproduit
   a 100,0 pour cent [MESURE, `03-grille-d-audit.md`, A2, « ce qu'elle rate »].
4. **Rien sur la contamination.** Le GSS est dans les corpus ; aucune coupure d'entrainement ne
   tranche, et la seule attaque de cette objection est OLMo en local
   [`DECISIONS-CONSOLIDEES-2026-09-09.md`].
5. **Rien de causal** sur ce que lire une description fait a un lecteur.
6. **Rien sur la direction du deplacement selon le demandeur.** A4 est une distance ; la
   direction etait nulle apres Holm en R1 [MESURE, `r1-resultats.md`, section 1.3], et ce run
   ne l'ajoute pas a ses familles.
7. **Rien sur la taille des modeles.** Les tailles des fermes ne sont pas publiees ; H4 parle de
   palier tarifaire, pas de parametres.
8. **Rien sur un second jeu, une autre langue, un autre pays.** GSS, anglais, Etats Unis.
9. **Rien qui survive a une mise a jour du modele.** Une ligne vaut pour un identifiant, un
   fournisseur aval et une date ; c'est pour cela que le registre porte les trois.
10. **Rien sur les probabilites par jeton.** Aucune quantite de cette page n'en depend ;
    quiconque voudra une lecture par logprobs ecrira une autre page et mesurera une autre
    quantite.
11. **Aucune valeur de reference unique.** Quatre conditions locales donnent deja 0,245, 0,566,
    0,627 et 0,727 sur la meme quantite [MESURE, `r5-resultats.md`, section 2] ; ce run ajoute
    des colonnes a une dispersion, il ne designe pas « la » valeur.

---

## Ce que je n'ai pas pu verifier

1. **Que le solde de 6 USD est integralement depensable en jetons.** Lu comme « environ 6 USD »
   dans l'inventaire ; les frais d'achat de credits d'OpenRouter, s'il y en a, ont ete preleves
   a l'achat [PROBABLE]. Le solde exact est a relire avant le premier appel.
2. **Que la limite de 1 000 requetes par jour sur le gratuit est par compte et non par modele.**
   La doc verifiee dit que la capacite est gouvernee globalement ; l'echelle du compteur n'est
   pas ecrite [verif section 1].
3. **Que le parametre de raisonnement au minimum est accepte par chacun des cinq fermes** via
   OpenRouter, et que les jetons de raisonnement apparaissent bien dans `usage`. C'est ce que
   l'essai mesure ; je ne l'ai pas lu dans une doc.
4. **Que le fournisseur aval peut etre fixe sans repli pour chaque modele.** Le champ existe
   dans la doc des parametres [verif section 2, ligne OpenRouter] ; qu'il soit honore pour les
   fermes n'est pas verifie.
5. **La longueur en jetons chez les autres tokenizers.** Les 210 et 641 sont comptes par le
   serveur local sur Qwen ; l'ecart de 15 pour cent est une estimation, pas une mesure.
6. **Quel modele l'application grand public sert par defaut.** Aucune source ouverte ici ; le
   choix du palier superieur est une convention.
7. **Le determinisme des API a temperature 0.** Je le suppose imparfait ; c'est l'essai qui
   dira combien.
8. **Le prix promotionnel de `gemini-3.8-flash`** est lu dans la verif de ce matin ; l'inventaire
   le reflete a 0,563 ; qu'il soit encore en vigueur a l'heure du run n'est pas verifie.
9. **La reponse d'Amir.** Cette page attend deux lignes : la page est validee ; le plafond de
   4,50 USD est valide. Et le depot OSF avant le premier appel payant, comme pour R5.

## Questions ouvertes pour Simon

1. Cinq modeles fermes et dix tests dans F2, cinq dans F3a et F3b : la puissance apres Holm
   est elle suffisante avec des intervalles de bootstrap sur 79 items larges comme ceux de R1
   (0,245 [0,056 ; 0,437]) ? Faut il reduire F2 aux seuls camps de gauche et de droite, cinq
   tests, ou accepter l'indecidabilite et publier les intervalles ?
2. Le plancher machine des 40 cellules est il le bon denominateur pour A4 sur une API, ou
   faut il le mesurer sur les 894 et payer un run double sur au moins un modele ?
3. Le palier tarifaire est il une variable defendable a la place de la taille, ou vaut il
   mieux retirer H4 et ne garder que la description ?
4. La replication de s1 en incarnation sur Twin, usage B, merite t elle la reserve de
   1,50 USD, sachant qu'elle mele un protocole neuf a des modeles neufs ?
5. Un modele `:free` dont le fournisseur entraine sur nos invites, avec des libelles publics
   d'enquete et une invite publiee, pose t il un probleme que je ne vois pas ?
