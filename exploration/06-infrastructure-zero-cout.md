# 06. Infrastructure a cout zero

Agent 6. Redige le 2 septembre 2026. Toutes les conditions commerciales citees ont ete
verifiees ce jour et sont volatiles : les quotas gratuits changent sans preavis, souvent
a la baisse. Toute valeur de ce document a plus de trois mois doit etre revue avant
d'etre utilisee dans une decision.

Question directrice : faire tourner des dizaines de milliers d'appels de modele, et
eventuellement du fine tuning, sans payer.

Reponse courte, etablie plus bas par le calcul : la machine de travail suffit. Les offres
gratuites d'API, toutes cumulees, plafonnent autour de 1 500 a 2 000 appels par jour en
contexte long. La machine locale, en utilisant le cache de prefixe et la lecture des
probabilites du token de reponse, en fait plus de cent mille dans le meme temps. Le local
n'est pas le plan de repli du budget zero, c'est le plan principal. Les API gratuites
deviennent un moyen de controle externe, pas le moteur de production.

---

## 1. La machine reelle

Releve fait le 2 septembre 2026 par `sysctl`, `sw_vers`, `df` et `system_profiler`.
[CONFIRME, mesure locale]

| Element | Valeur |
|---|---|
| Puce | Apple M5 |
| Identifiant machine | Mac17,3 |
| Coeurs CPU | 10 au total : 4 performance, 6 efficacite |
| Coeurs GPU | 10, Metal 4 |
| Memoire unifiee | 32 Gio (34 359 738 368 octets) |
| Disque libre | 593 Gio sur 926 Gio |
| Systeme | macOS 26.5.2, build 25F84, noyau Darwin 25.5 |

Outillage present : Python 3.14.7, pip 26.2.1, uv 0.11.25, git 2.55.0.
Outillage absent : ollama, llama.cpp, LM Studio, mlx, mlx_lm, git-lfs, dvc.
[CONFIRME, mesure locale] Rien n'est installe, la pile est a construire de zero, ce qui
est une bonne nouvelle : aucun choix hérite a defaire.

Point technique determinant : la bande passante memoire du M5 de base est de 153 Go/s,
contre 120 Go/s sur M4, soit +28 pour cent.
[CONFIRME, https://machinelearning.apple.com/research/exploring-llms-mlx-m5]
C'est ce chiffre, et non le nombre de coeurs GPU, qui plafonne la vitesse de generation.
Apple ecrit explicitement dans la meme page que la production du premier token est bornee
par le calcul, et celle des tokens suivants par la bande passante memoire.

Attention a ne pas confondre avec les variantes : M5 Pro a 307 Go/s, M5 Max 460 Go/s en
14 pouces et 614 Go/s en 16 pouces.
[CONFIRME, sources secondaires concordantes, notamment
https://contracollective.com/blog/apple-silicon-memory-bandwidth-local-llm-tokens-per-second-m5-2026]
La machine du projet est la version de base. Toute annonce de debit lue sur internet a
propos du "M5" doit etre divisee par deux ou par quatre si elle vient d'un M5 Pro ou Max.

Budget memoire exploitable : macOS reserve par defaut environ 75 pour cent de la memoire
unifiee au GPU, soit environ 24 Gio ici, relevable via `iogpu.wired_limit_mb`.
[PROBABLE, comportement documente de longue date sur Apple Silicon, non re-verifie sur
macOS 26] Budget de travail prudent retenu pour la suite : 22 Gio pour les poids plus le
cache KV.

---

## 2. Ce qui tourne en local

### 2.1 Ce qui tient en memoire

Les tailles marquees [CONFIRME] viennent des mesures publiees par Apple sur un MacBook Pro
M5 24 Gio, donc sur la meme puce que la notre avec moins de memoire.

| Modele | Format | Poids | Tient ? | Commentaire |
|---|---|---|---|---|
| Qwen 1.7B | BF16 | 4,40 Gio [CONFIRME Apple] | oui, large | trop faible pour du raisonnement de persona |
| Qwen3 4B | 4 bits | ~2,3 Gio [PROBABLE, calcul] | oui, large | candidat pour la passe de degrossissage |
| Llama 3.1 8B / Qwen3 8B | 4 bits | ~4,5 Gio [PROBABLE, calcul] | oui, large | cheval de bataille |
| Qwen 8B | BF16 | 17,46 Gio [CONFIRME Apple] | oui, serre | reference de qualite non quantifiee |
| Mistral / Qwen 14B | 4 bits | ~8 Gio [PROBABLE, calcul] | oui | bon compromis |
| gpt-oss-20b | MXFP4 | ~12 Gio [PROBABLE, calcul] | oui | ~3,6B parametres actifs |
| Qwen3 30B-A3B (MoE) | 4 bits | 17,31 Gio [CONFIRME Apple] | oui, serre | 3B actifs, le meilleur rapport qualite/debit |
| Gemma 3 27B | 4 bits | ~15 Gio [PROBABLE, calcul] | oui, serre | dense, donc lent |
| Llama 3.3 70B | 4 bits | ~40 Gio [PROBABLE, calcul] | NON | hors d'atteinte sur 32 Gio |
| DeepSeek R1 / V3 complets | toute quantification | > 200 Gio | NON | seules les distillations 7B a 32B sont accessibles |

Le cache KV n'est pas negligeable et se calcule exactement. Pour une architecture de type
Llama 3 8B, 32 couches, 8 tetes KV, dimension de tete 128, en 16 bits :
2 (cles et valeurs) x 32 x 8 x 128 x 2 octets = 131 072 octets par token, soit 128 Kio par
token. [CONFIRME, arithmetique directe a partir de la configuration publiee du modele]

Consequence chiffree, decisive pour notre usage :

| Contexte | Cache KV en 16 bits | En 8 bits |
|---|---|---|
| 8 000 tokens | 1,0 Gio | 0,5 Gio |
| 32 000 tokens | 4,0 Gio | 2,0 Gio |
| 8 000 tokens x 8 requetes paralleles | 8,0 Gio | 4,0 Gio |

Autrement dit, sur un 8B en 4 bits, huit personas en parallele avec 8 000 tokens de
contexte chacun consomment 4,5 Gio de poids plus 8 Gio de cache. C'est tenable. Seize
personas en parallele avec 16 000 tokens de contexte ne le seraient pas sans quantifier
le cache KV. La quantification du cache KV en 8 bits est donc un levier de premier ordre
et elle est disponible dans llama.cpp et dans MLX.

Fenetre de contexte utilisable, recommandation : 8 000 a 16 000 tokens par persona.
Un entretien de deux heures transcrit fait de l'ordre de 18 000 a 25 000 mots, soit
25 000 a 35 000 tokens. [PROBABLE, ratio usuel d'environ 1,3 token par mot en francais
et 1,3 en anglais pour de l'oral transcrit] Il faudra donc condenser la transcription,
ce qui est de toute facon un choix methodologique a documenter, pas seulement une
contrainte materielle.

### 2.2 Le debit a attendre

Deux methodes independantes, qui convergent.

Methode 1, par la bande passante. Le decodage lit l'integralite des poids actifs a chaque
token. Donc tokens par seconde = bande passante utile divisee par les octets lus par token.
L'efficacite reelle observee sur Apple Silicon est de l'ordre de 70 a 85 pour cent de la
bande passante theorique. [PROBABLE, regle empirique largement reprise dans la
litterature communautaire]

Methode 2, par proportionnalite. Un M5 Pro a 307 Go/s produit 50 a 60 tokens par seconde
sur Llama 3.1 8B en 4 bits.
[CONFIRME comme chiffre publie, source secondaire :
https://www.promptquorum.com/local-llms/m5-pro-max-llm-benchmarks-2026]
A bande passante moitie, on attend la moitie.

| Modele et format | Octets lus / token | Debit theorique | Debit attendu [PROBABLE] |
|---|---|---|---|
| Qwen3 4B, 4 bits | ~2,3 Gio | 66 t/s | 45 a 55 t/s |
| Llama 3.1 8B, 4 bits | ~4,5 Gio | 34 t/s | 24 a 29 t/s |
| Qwen 8B, BF16 | 17,5 Gio | 9 t/s | 6 a 8 t/s |
| 14B, 4 bits | ~8 Gio | 19 t/s | 14 a 17 t/s |
| Qwen3 30B-A3B, 4 bits | ~2 Gio actifs | ~75 t/s | 50 a 70 t/s |
| Gemma 3 27B dense, 4 bits | ~15 Gio | 10 t/s | 7 a 9 t/s |

Les deux methodes donnent 24 a 29 t/s pour le 8B en 4 bits. Je retiens 27 t/s comme
valeur de travail. Elle reste a mesurer sur la machine, ce n'est pas un chiffre mesure.

Le point remarquable est la ligne du 30B MoE : un modele de 30 milliards de parametres
tourne plus vite qu'un modele dense de 8 milliards, parce que seuls 3 milliards de
parametres sont lus par token. Pour notre usage, qui demande de la qualite de
raisonnement social sur des reponses tres courtes, c'est le meilleur choix disponible
gratuitement sur cette machine. [PROBABLE, la lecture effective sur une architecture MoE
depend de la dispersion des experts sollicites, le chiffre peut se degrader]

Le prefill, lui, est borne par le calcul et c'est la que le M5 apporte son gain reel.
Apple mesure un temps jusqu'au premier token 1,19 a 4,06 fois plus rapide que sur M4,
avec Qwen 14B en 4 bits sous 10 secondes et Qwen3 30B MoE sous 3 secondes.
[CONFIRME, https://machinelearning.apple.com/research/exploring-llms-mlx-m5]
Apple ne precise pas la longueur du prompt utilise, ce qui rend ces valeurs
inexploitables telles quelles. Pour les calculs qui suivent je retiens une hypothese
prudente de 800 tokens par seconde en prefill sur un 8B en 4 bits.
[HYPOTHESE, a mesurer en priorite, c'est le parametre le plus incertain du document et
celui qui pese le plus sur les durees annoncees]

### 2.3 Le calcul qui decide de tout : 10 000 appels en local

Scenario de reference retenu, representatif de popsim : 100 personas, 100 questions par
persona. Chaque appel comporte un prefixe de persona de 8 000 tokens (biographie
condensee, instructions, format de reponse) et une question de 100 tokens.

**Cas A. Naif : pas de cache, un appel a la fois, reponse generee de 30 tokens.**

- Prefill : 8 100 tokens a 800 t/s = 10,1 s
- Decodage : 30 tokens a 27 t/s = 1,1 s
- Total par appel : 11,2 s
- **10 000 appels : 112 000 s, soit 31 heures.**

C'est le chiffre que la plupart des gens obtiennent, et c'est celui qui fait conclure a
tort que le local ne passe pas a l'echelle.

**Cas B. Cache de prefixe par persona.** Le prefixe de 8 000 tokens n'est calcule qu'une
fois par persona, puis restaure pour les 99 questions suivantes.

- Cout des prefixes : 100 personas x 10,0 s = 1 000 s
- Par appel : prefill du delta de 100 tokens = 0,12 s, plus decodage 1,1 s = 1,2 s
- **10 000 appels : 1 000 + 12 200 = 13 200 s, soit 3 h 40. Facteur 8,5.**

**Cas C. Cache de prefixe plus batch continu.** Le papier vllm-mlx mesure un gain de
debit de 2,6x sur les gros modeles et 3,7x sur les petits a 16 requetes simultanees, sur
un M4 Max 128 Gio. [CONFIRME, arXiv:2601.19139v2, 29 janvier 2026] Sur un M5 de base la
bande passante sature plus tot, je retiens un gain de 2x. [PROBABLE]

- **10 000 appels : environ 1 h 50.**

**Cas D. Cache de prefixe, batch, et lecture des probabilites du token de reponse plutot
que generation.** Un seul passage avant, aucune generation. Le cout se reduit au prefill
du delta.

- Cout des prefixes : 1 000 s
- Par appel : 0,12 s de prefill du delta plus environ 0,04 s de passage avant = 0,16 s
- Sequentiel : 1 000 + 1 600 = 2 600 s, soit **43 minutes**
- Avec batch, gain 2x sur la partie repetee : **environ 25 minutes**

**Recapitulatif. De 31 heures a 25 minutes pour la meme experience, soit un facteur
d'environ 75, sans depenser un euro.** C'est le resultat central de ce document. Les
trois leviers, dans l'ordre d'importance : la lecture des logprobs plutot que la
generation, le cache de prefixe, le batch.

Capacite hebdomadaire qui en decoule. En laissant la machine travailler 8 heures par
nuit, 7 nuits sur 7, soit 56 heures :

- en mode D (logprobs, cache, batch) : de l'ordre de **1,3 million d'appels par semaine**
- avec une marge de securite de 3 pour tenir compte des erreurs d'estimation du prefill,
  de la thermique du portable et des reprises : **plus de 400 000 appels par semaine**
- en mode B (generation de 30 tokens, cache, sans batch) : environ **150 000 appels par
  semaine**

[PROBABLE, calcul entierement derive des hypotheses ci-dessus, dont le prefill a 800 t/s
qui n'est pas mesure]

A comparer avec la section 3 : toutes les offres gratuites d'API cumulees plafonnent
autour de 12 000 appels par semaine en contexte long.

### 2.4 Comparaison des moteurs d'execution

Notre usage est tres particulier : beaucoup d'appels, generations tres courtes, et un
long contexte partage par tous les appels d'un meme persona. Le critere qui domine tous
les autres est donc la reutilisation du cache de prefixe entre appels.

| Outil | Batch continu | Cache de prefixe entre requetes | GPU Apple | Acces aux logits | Verdict pour popsim |
|---|---|---|---|---|---|
| mlx-lm (Apple) | `batch_generate`, pas d'ordonnanceur continu | Oui : `mlx_lm.cache_prompt`, `make_prompt_cache`, cache serialisable sur disque [CONFIRME, README mlx-lm] | Natif, le plus rapide | Complet | Socle de reference. Le cache de prefixe persiste sur disque, donc reutilisable entre sessions |
| vllm-mlx | Oui, continu, 2,6x a 3,7x a 16 requetes [CONFIRME arXiv:2601.19139v2] | Oui, par hachage de contenu | Natif | A verifier | Le meilleur techniquement pour notre profil, mais jeune, donc a valider avant d'en dependre |
| llama.cpp / llama-server | Oui, `--parallel` | Oui : `--cache-prompt` actif par defaut, plus `--cache-reuse N` qui decale le cache au lieu de recalculer [CONFIRME, doc du serveur] | Oui, via Metal | Complet, `--logits-all` | Le plus robuste et le mieux documente. 21 a 87 pour cent plus lent que MLX sur Apple Silicon [CONFIRME arXiv:2601.19139v2] |
| Ollama | Oui, `OLLAMA_NUM_PARALLEL`, mais la RAM est multipliee par le nombre de slots | Oui, par hachage de prefixe, exigence d'identite octet par octet | Oui | Partiel, expose mal les logits | Pratique pour demarrer, opaque et gourmand en RAM pour du batch serieux |
| LM Studio | Oui | Oui, moteur MLX ameliore pour les charges agentiques | Oui | Via API compatible OpenAI, logprobs selon le moteur | Utile pour explorer a la main, pas pour un pipeline scripte |
| vLLM amont | Oui, la reference du domaine | Oui, prefix caching automatique | Non sur Metal, CPU seulement sur Mac | Complet | A reserver aux GPU gratuits de Kaggle, Colab ou Jean Zay |

Piege commun et couteux : le cache de prefixe exige une identite stricte du prefixe. Une
date, un horodatage, un identifiant de session ou un ordre de dictionnaire non
deterministe dans le prompt suffit a le faire echouer silencieusement, et l'experience
repasse du cas B au cas A, donc de 3 h 40 a 31 h.
[CONFIRME, comportement documente pour llama.cpp et pour Ollama]
Regle a graver : **le persona en tete, fige et canonique ; la question en queue.**

Limite connue de MLX a verifier avant de choisir un modele : la reutilisation du cache de
prefixe ne fonctionne que pour les modeles a attention pleine. Les modeles a fenetre
glissante ou a couches SSM retombent silencieusement sur un recalcul complet du prompt.
[CONFIRME comme signalement, https://github.com/ml-explore/mlx-lm/issues/980, statut de
correction non verifie au 2 septembre 2026]
Cela concerne potentiellement Gemma et Mistral recents. A tester explicitement : mesurer
le temps du deuxieme appel sur le meme prefixe, il doit etre dix fois plus rapide que le
premier. Si ce n'est pas le cas, changer de modele ou de moteur.

### 2.5 Fine tuning leger en local

Etat des lieux au 2 septembre 2026.

- **MLX-LM propose LoRA et QLoRA nativement** sur Apple Silicon. [CONFIRME, README mlx-lm]
- **Unsloth ne supporte pas le fine tuning sur Apple Silicon.** Son moteur repose sur
  CUDA. Un portage MLX est annonce comme en cours, et des projets communautaires
  (`unsloth-mlx`, `mlx-tune`) offrent une API compatible.
  [PROBABLE, https://unsloth.ai/docs/get-started/fine-tuning-for-beginners/unsloth-requirements
  et https://github.com/unslothai/unsloth/discussions/5903, statut mouvant]
  Conclusion pratique : Unsloth sur les GPU gratuits Kaggle, MLX-LM sur le Mac.

Ordre de grandeur pour un QLoRA sur 7B, 5 000 exemples : environ 90 minutes et un pic de
7 Gio de RAM sur un M2 Max 32 Gio. [PROBABLE, source secondaire
https://insiderllm.com/guides/fine-tuning-mac-lora-mlx/, non reproduit] Le M5 de base a
une bande passante inferieure au M2 Max mais dispose d'accelerateurs matriciels dans le
GPU, et l'entrainement est nettement plus borne par le calcul que le decodage. Estimation
pour la meme charge sur notre machine : 1 h 30 a 4 h. [HYPOTHESE]

Verdict par taille de modele sur cette machine :

| Taille | LoRA | QLoRA 4 bits | Recommandation |
|---|---|---|---|
| 1B a 4B | oui, confortable | oui | ideal pour iterer vite, plusieurs runs par jour |
| 7B a 8B | serre mais faisable | oui, ~7 a 10 Gio | cible principale du fine tuning local |
| 13B a 14B | non | oui, serre | faisable de nuit, une iteration par jour |
| 27B a 32B | non | tres serre, risque de swap | a deporter sur Kaggle |
| 70B | non | non | hors sujet sans credits de calcul |

Recommandation : ne pas fine-tuner tant que le prompting avec logprobs n'a pas ete
epuise. Le fine tuning est le levier le plus couteux en temps de mise au point et le plus
difficile a defendre dans un papier, parce qu'il melange la contribution du modele et
celle de l'ajustement. Si un adaptateur devient necessaire pour attaquer l'ecrasement de
la variance, l'entrainer sur 3B ou 8B en local, et ne monter en taille que sur GPU
gratuit.

---

## 3. Offres gratuites d'API

Tous les chiffres ci-dessous ont ete verifies le 2 septembre 2026. La colonne "Donnees"
est la plus importante pour un projet de publication : elle dit si le fournisseur
s'autorise a entrainer sur ce qu'on lui envoie.

| Fournisseur | Quota gratuit | Contexte | Logprobs | Donnees | Verdict popsim |
|---|---|---|---|---|---|
| **Google AI Studio / Gemini** | Environ 15 RPM et 1 500 requetes/jour sur les modeles Flash, 1M TPM ; les modeles Pro sont passes derriere facturation en mai 2026 [PROBABLE, sources secondaires concordantes, la doc officielle renvoie desormais au tableau de bord AI Studio] | Long, jusqu'a 1M tokens selon modele | Oui, `responseLogprobs` et `logprobs`, support variable selon modele et selon l'API utilisee [CONFIRME comme fonctionnalite, disponibilite par modele non verifiee] | **"Content used to improve our products : Yes"** sur le niveau gratuit [CONFIRME, https://ai.google.dev/gemini-api/docs/pricing]. Relecture humaine possible. Ne pas soumettre d'information sensible ou personnelle [CONFIRME, https://ai.google.dev/gemini-api/terms] | Le plus genereux en requetes. Utilisable seulement sur des donnees publiques |
| **Cerebras** | 5 RPM, 30K TPM, 1M tokens/heure, **1M tokens/jour**, sur `gpt-oss-120b` et `gemma-4-31b` [CONFIRME, https://inference-docs.cerebras.ai/support/rate-limits] | Une source secondaire annonce un plafond de 8 192 tokens sur le niveau gratuit [PROBABLE, non confirme par la doc officielle] | Non verifie | Non verifie | Excellent debit, mais 1M tokens/jour = environ 123 appels/jour a 8 100 tokens de contexte. Le plafond de tokens, pas de requetes, est le mur |
| **Groq** | 30 RPM, 1 000 requetes/jour, **8K TPM et 200K tokens/jour** par modele sur `gpt-oss-120b`, `gpt-oss-20b`, `qwen3.6-27b`, `qwen3.8-27b` [CONFIRME, https://console.groq.com/docs/rate-limits] | Limite de fait par le TPM | **Non. `logprobs`, `top_logprobs` et `logit_bias` renvoient une erreur 400** [CONFIRME, https://console.groq.com/docs/openai] | Non verifie | **Disqualifie pour notre methode principale.** 200K tokens/jour = 24 appels/jour en contexte long. Les tokens en cache ne comptent pas dans les limites, ce qui aide un peu [PROBABLE] |
| **OpenRouter, modeles `:free`** | 20 RPM, 50 requetes/jour sans achat, 1 000/jour apres un achat unique de 10 dollars [PROBABLE, sources secondaires concordantes] | Variable | Variable | **Il faut activer "free endpoints that may train on request data" et "free endpoints that may publish prompts"** [CONFIRME, https://openrouter.ai/docs/guides/privacy/provider-logging] | **Ecarte.** La publication des prompts est incompatible avec des donnees d'enquete sous licence. Et le palier utile suppose une depense |
| **Mistral, niveau Experiment** | Environ 1 requete/seconde ; Mistral ne publie plus les chiffres exacts et renvoie a la console admin [PROBABLE, https://help.mistral.ai/en/articles/698531] | Long | Non verifie | Les donnees peuvent servir a l'amelioration du modele sauf refus explicite [PROBABLE, non confirme sur le texte contractuel] | A tester, verification par telephone requise. Fournisseur europeen, argument utile pour un projet francais |
| **Cloudflare Workers AI** | 10 000 "neurons" par jour, remis a zero a 00:00 UTC, partages entre tous les modeles [CONFIRME, sources secondaires concordantes] | Variable | Non | Non verifie | Le neuron est une unite de calcul normalisee, pas un token. Impossible de convertir en nombre d'appels sans mesure. A tester avant d'y compter |
| **NVIDIA NIM / build.nvidia.com** | 1 000 credits a l'inscription, environ 1 credit par appel ; 4 000 credits supplementaires avec une adresse professionnelle [PROBABLE, sources secondaires concordantes et forum NVIDIA] | Variable | Selon modele | Non verifie | Reserve non renouvelable de 5 000 appels. A garder pour une validation ponctuelle, pas pour de la production |
| **Hugging Face Inference Providers** | 0,10 dollar/mois en gratuit, 2 dollars/mois en PRO a 9 dollars [PROBABLE, sources secondaires concordantes] | Variable | Variable | Depend du fournisseur route | Negligeable en volume |
| **GitHub Models** | Facturation a l'usage depuis le 1er juin 2026 via les GitHub AI Credits ; le niveau gratuit Copilot est de 2 000 completions et 50 requetes de chat par mois [PROBABLE, sources secondaires] | Variable | Non | Non verifie | Negligeable, et sans rapport avec un usage API programmatique |
| **Together AI** | 5 dollars de credit a l'inscription, pas de niveau gratuit permanent annonce [PROBABLE, sources secondaires contradictoires entre 1, 5 et 25 dollars] | Long | Oui en general | Non verifie | Reserve ponctuelle |
| **Kaggle Notebooks** | **30 heures de GPU par semaine** (P100 16 Go, ou 2x T4), sessions de 12 h max, plus 20 h/semaine de TPU [PROBABLE, sources secondaires concordantes] | Sans objet | Complet, on execute le modele | Le notebook peut etre prive | **La meilleure ressource gratuite apres le Mac.** vLLM avec prefix caching y tourne, et Unsloth pour le fine tuning |
| **Google Colab, niveau gratuit** | T4 16 Go, sessions jusqu'a 12 h, plafond hebdomadaire flottant de l'ordre de 15 a 30 h, sans garantie d'obtenir un GPU [PROBABLE, Google indique lui-meme que les limites fluctuent] | Sans objet | Complet | Notebook prive | Utile en complement de Kaggle, mais trop imprevisible pour un plan de production |

### Lecture d'ensemble

Budget d'appels gratuits par jour, en contexte long de 8 100 tokens :

| Source | Appels/jour realisables |
|---|---|
| Gemini Flash gratuit | ~1 500 (borne par les requetes, pas les tokens) |
| Cerebras | ~123 (borne par 1M tokens/jour) |
| Groq | ~24 par modele, soit ~96 sur quatre modeles (borne par 200K tokens/jour) |
| Cloudflare | inconnu, probablement faible |
| **Total realiste** | **environ 1 700 par jour, soit 12 000 par semaine** |

Face aux **400 000 appels par semaine** estimes en local, le rapport est de 1 a 33. Et
les appels gratuits les plus abondants, ceux de Gemini, sont ceux dont les donnees
alimentent l'entrainement de Google.

**Consequence sur la conception du protocole.** Les offres gratuites d'API ne sont pas le
moteur de production. Elles servent a trois choses precises :

1. **Controle de generalisation.** Rejouer un sous-echantillon de 500 a 1 500 items sur
   un modele proprietaire de generation courante permet d'ecrire dans le papier que le
   resultat ne tient pas a un artefact d'un modele ouvert donne. C'est un argument
   attendu par les relecteurs et il coute zero.
2. **Borne haute de qualite.** Mesurer l'ecart entre le meilleur modele local et un
   modele frontiere sur le meme protocole donne une idee du plafond atteignable.
3. **Etalonnage des juges.** Si une etape d'evaluation automatique est necessaire, la
   faire arbitrer par un modele different de celui qui genere.

**Consequence sur les donnees.** Le point de vigilance juridique est reel. Le tableau de
prix officiel de Google indique explicitement que le contenu du niveau gratuit sert a
ameliorer leurs produits [CONFIRME]. Cependant, les conditions d'utilisation de l'API
Gemini prevoient que, pour les utilisateurs de l'EEE, de Suisse et du Royaume-Uni, les
protections du niveau payant s'appliquent a l'ensemble des services, y compris gratuits.
[PROBABLE, https://ai.google.dev/gemini-api/terms, formulation rapportee mais non citee
mot a mot, et en tension apparente avec le tableau de prix] Le projet etant opere depuis
la France, cette clause change potentiellement tout. **C'est le point le plus important a
faire trancher avant d'envoyer quoi que ce soit de non public a Google.** Tant qu'il
n'est pas tranche : n'envoyer aux API gratuites que des donnees deja publiques.

---

## 4. Credits et programmes

Classes par rapport entre effort et gain, du meilleur au moins bon pour popsim
aujourd'hui.

| Programme | Ce qu'on obtient | Eligibilite | Delai | Effort | Verdict |
|---|---|---|---|---|---|
| **GENCI / Jean Zay, Acces Dynamique** | Jusqu'a **50 000 heures GPU equivalent V100** sur un an, gratuit, sur un supercalculateur national [CONFIRME, https://www.edari.fr/ et modalites GENCI] | **Appartenir ou etre associe a une structure de recherche francaise** [CONFIRME, edari.fr]. Le responsable scientifique peut etre permanent, ou etudiant en M2, doctorant ou post-doctorant | Quelques jours [PROBABLE, formulation "dans les quelques jours" reprise par plusieurs sources] | Un dossier court sur le portail eDARI | **De loin le meilleur rapport effort/gain, si et seulement si le projet trouve un rattachement a un laboratoire francais.** 50 000 h GPU rendent le passage a 20 000 agents trivial. C'est la question numero un a poser a Simon |
| **GENCI, Acces Regulier** | Au dela de 50 000 h GPU | Meme condition d'affiliation | Deux campagnes par an, evaluation par un comite | Dossier scientifique complet | La campagne 2026 se clot le **7 septembre 2026 a 10 h** [CONFIRME, edari.fr], soit dans cinq jours. Irrealiste pour cette phase. A viser pour la campagne suivante |
| **OpenAI, programme academique lance en juillet 2026** | Acces gratuit aux modeles avances pour 100 000 chercheurs academiques jusqu'en 2027, chaque beneficiaire pouvant inviter quatre collaborateurs **de son institution** [PROBABLE, source Axios du 29 juillet 2026, page inaccessible directement, contenu rapporte par les resultats de recherche] | Chercheur academique | Non verifie | Faible si on passe par un beneficiaire | **A explorer via le contact MIT de Simon.** La restriction "de son institution" est le point bloquant a verifier |
| **Google Cloud Research Credits** | Jusqu'a **5 000 dollars** pour un enseignant-chercheur ou post-doctorant, jusqu'a **1 000 dollars** pour un doctorant, une fois par an [CONFIRME, https://edu.google.com/programs/credits/research/] | Etablissement d'enseignement superieur accredite ou institut de recherche a but non lucratif, dans un pays eligible | 6 a 8 semaines [PROBABLE, source secondaire] | Proposition de recherche plus estimation budgetaire via le calculateur | **Excellent si affiliation academique.** Les credits couvrent Vertex AI, donc Gemini sans la clause d'entrainement |
| **Microsoft for Startups Founders Hub** | 1 000 dollars au palier de base, jusqu'a 5 000 apres verification d'entreprise, davantage avec un investisseur [PROBABLE, sources secondaires concordantes] | **Ouvert aux projets auto-finances, sans investisseur ni accelerateur**, mais il faut construire un produit logiciel | Rapide | Inscription en ligne | **Le plus accessible sans affiliation ni societe investie.** A tenter des qu'une entite existe |
| **AWS Activate, palier Founders** | Environ **1 000 a 5 000 dollars** [PROBABLE, sources secondaires concordantes] | Startup auto-financee, moins de 10 ans, moins de 10 salaries, moins de 1M de revenus ou de levee, pre-Serie B, jamais beneficiaire du palier Founders | Rapide | Inscription en ligne | Utile, mais AWS est le moins adapte a de l'inference LLM gratuite |
| **Anthropic, External Researcher Access Program** | Typiquement **1 000 dollars** de credits API, davantage dans de rares cas [CONFIRME, https://support.claude.com/en/articles/9125743] | Recherche sur la surete et l'alignement des IA, sur des sujets juges prioritaires par Anthropic | Evaluation le premier lundi de chaque mois [CONFIRME] | Un formulaire | **Sujet mal aligne.** popsim n'est pas un projet d'alignement. A moins de reformuler l'angle "les populations simulees ecrasent la variance" comme un probleme de representation fidele des groupes, ce qui est defendable mais pas evident |
| **OpenAI Researcher Access Program** | Jusqu'a **1 000 dollars** de credits API, valables 12 mois, non renouvelables [CONFIRME, https://openai.smapply.org/prog/openai_researcher_access_program/] | Chercheurs en debut de carriere, priorite aux ressources limitees | Revue trimestrielle en mars, juin, septembre, decembre, puis environ 4 semaines [CONFIRME] | Un dossier | **Sujet bien aligne.** Deux des sept axes prioritaires listes sont "equite et representation dans les modeles de langage" et "mesure de l'impact societal". C'est exactement notre contribution. La prochaine revue est en septembre 2026 |
| **NVIDIA Inception** | Adhesion gratuite, credits cloud de partenaires sans montant garanti, 30 pour cent sur DGX Cloud, jusqu'a 100 000 dollars de credits DGX Cloud sur demande selon des sources secondaires [PROBABLE, NVIDIA ne publie pas de montant] | **Societe immatriculee**, moins de 10 ans, au moins un developpeur, site web fonctionnel. Les societes de conseil sont exclues | Quelques jours a quelques semaines | Formulaire | **Bloque tant qu'il n'y a pas d'entite juridique.** A remettre sur la table apres constitution |
| **Anthropic AI for Science** | Credits API gratuits pour des projets scientifiques a fort impact, orientation biologie et sciences du vivant [CONFIRME, https://www.anthropic.com/news/ai-for-science-program] | Projet scientifique | Non verifie | Un dossier | Orientation disciplinaire eloignee, mais les sciences sociales quantitatives ne sont pas explicitement exclues. Faible cout de tentative |

### Ce que change le contact MIT de Simon

Le contact MIT est le pivot de toute cette section, et pas pour la raison qu'on croit.
Son interet principal n'est pas l'acces aux auteurs de Stanford, c'est **l'affiliation
academique**. Concretement :

1. **Google Cloud Research Credits** exige une institution accreditee. Une co-signature
   MIT debloque jusqu'a 5 000 dollars, soit l'equivalent de plusieurs dizaines de
   millions de tokens sur Gemini Flash, avec les protections du niveau payant sur les
   donnees.
2. **Le programme academique OpenAI** permet a un beneficiaire d'inviter quatre
   collaborateurs de son institution. Si le contact MIT est beneficiaire et si la
   restriction institutionnelle peut etre satisfaite par un statut de visiting ou
   d'affilie, l'acces est gratuit jusqu'en 2027.
3. **Weights and Biases** offre la licence Pro complete gratuitement a toute adresse
   academique. [CONFIRME, https://wandb.ai/site/pricing/]
4. **GENCI n'est pas debloque par le MIT.** L'exigence est une structure de recherche
   **francaise** [CONFIRME]. C'est un canal separe, qui demande un rattachement en
   France : laboratoire d'un ancien encadrant, equipe INRIA, laboratoire de psychologie
   quantitative, ou co-encadrement de these. **C'est le levier le plus puissant du
   document et il ne depend pas du MIT.**

Ordre de priorite recommande : d'abord chercher un rattachement francais pour GENCI,
ensuite l'affiliation academique pour Google Cloud Research Credits et W&B, ensuite le
dossier OpenAI Researcher Access en septembre. Les programmes startup viennent apres,
quand une entite existe.

---

## 5. Le reste de la pile, gratuitement

| Besoin | Option retenue | Ce qui est gratuit | Limite a connaitre |
|---|---|---|---|
| **Code** | Git plus GitHub, depot public ou prive | Depots illimites, prives inclus | Depot recommande sous 1 Gio, fichier unique sous 100 Mio |
| **Donnees volumineuses** | **Hugging Face Datasets** | **1 To de stockage gratuit pour les depots publics** [PROBABLE, https://huggingface.co/docs/hub/storage-limits] ; au dela de 300 Gio il faut ecrire a HF | Depots publics. Pour du prive, la limite est bien plus basse |
| **Donnees volumineuses, variante** | DVC avec stockage sur HF ou Google Drive | DVC est libre et gratuit | Necessite un stockage distant, qui est le vrai cout |
| **A eviter** | Git LFS sur GitHub | Sources contradictoires entre 1 Gio et 10 Gio de stockage et de bande passante par mois pour un compte gratuit [non tranche] | Historiquement le poste qui declenche une facturation surprise. **Ne pas y mettre les jeux de donnees** |
| **Base de resultats** | **DuckDB** en fichier local, plus SQLite pour le cache d'appels | Entierement libre | Aucune. DuckDB lit et agrege des dizaines de millions de lignes sur cette machine sans effort |
| **Execution des experiences** | Un script Python pilote par un fichier de configuration, avec reprise sur erreur et memoisation | Gratuit | La discipline de reprise est a coder soi-meme |
| **Observabilite des runs** | **Langfuse auto-heberge** (licence MIT) via Docker | Fonctionnalites completes, pas de plafond d'evenements, pas de limite de retention [PROBABLE, sources secondaires concordantes] | Consomme de la RAM sur le Mac. Alternative : Langfuse Cloud Hobby, 50 000 unites par mois, 30 jours de retention, 2 utilisateurs, sans Playground ni Experiments |
| **Observabilite, variante minimale** | Une table DuckDB `calls` avec prompt hache, modele, parametres, latence, tokens, cout theorique | Gratuit, zero dependance | Pas d'interface. Suffisant pour la phase exploratoire |
| **Suivi des experiences** | **MLflow local** (`mlflow ui` sur un dossier) | Entierement libre | Pas de partage distant sans serveur |
| **Suivi, si affiliation academique** | **Weights and Biases, licence Pro academique** | Heures de suivi illimitees, 200 Go de stockage, jusqu'a 25 Go/mois d'ingestion Weave, jusqu'a 100 sieges [CONFIRME, https://wandb.ai/site/pricing/] | Exige une adresse academique et une recherche non liee a une entite a but lucratif. Ce dernier point merite attention si popsim devient une societe |
| **Suivi, sans affiliation** | W&B plan gratuit personnel | Experiences illimitees, heures de suivi illimitees, 5 Go de stockage par mois | 5 Go suffisent pour des metriques, pas pour des artefacts |
| **Demonstration** | **Hugging Face Spaces, CPU gratuit** | 2 vCPU, 16 Go de RAM, illimite et non mesure [PROBABLE, sources secondaires] ; ZeroGPU H200 avec un quota d'environ 3,5 minutes par jour pour les comptes authentifies | Mise en veille apres 48 h d'inactivite. Le CPU gratuit ne fait pas tourner un LLM correct, il doit appeler une API |
| **Demonstration, variante** | Streamlit Community Cloud | 3 applications par compte, 1 Gio de ressources par application | Mise en veille apres 12 h sans trafic. Ressources augmentables sur demande pour un projet a but non lucratif ou open source |
| **Calcul GPU d'appoint** | Kaggle Notebooks | 30 h/semaine de P100 ou 2x T4, 20 h/semaine de TPU, sessions de 12 h | Le meilleur complement gratuit au Mac |

Pile de stockage recommandee, en une phrase : le code sur GitHub, les jeux de donnees sur
Hugging Face Datasets, les resultats dans un fichier DuckDB versionne par un manifeste,
et rien de lourd dans Git.

---

## 6. Doctrine de frugalite

Sept regles, chiffrees. Appliquees ensemble, elles font passer une experience de 10 000
appels de 31 heures a environ 25 minutes sur la machine du projet, et permettent de
travailler sur des dizaines de milliers d'agents sans budget.

### Regle 1. Le persona en tete, la question en queue, le prefixe fige

Le cache de prefixe ne fonctionne que sur une identite stricte, octet par octet. Toute
construction dynamique du prompt le casse silencieusement.

Gain mesure par le calcul : facteur **8,5** sur le cas de reference (31 h vers 3 h 40),
en supposant 100 questions par persona.

Regle de conception associee : **maximiser le nombre de questions par persona avant de
changer de persona.** Le gain du cache est proportionnel au nombre de questions par
prefixe. Avec 10 questions par persona le gain tombe a environ 3,5. Avec 100 questions il
est de 8,5. Avec 300 questions il plafonne vers 10. L'ordonnancement de la boucle
d'experience est donc une decision de performance, pas une commodite.

Test de non-regression a ecrire une fois pour toutes : appeler deux fois le meme prefixe
et verifier que le second appel est au moins cinq fois plus rapide. S'il ne l'est pas, le
cache ne fonctionne pas et l'experience va durer huit fois plus longtemps que prevu.

### Regle 2. Lire les probabilites du token de reponse au lieu de generer du texte

C'est le point central pour popsim, et il merite d'etre developpe, parce qu'il resout
simultanement le probleme du cout et le probleme scientifique du projet.

**Le mecanisme.** Sur une question a choix multiple a K modalites, on contraint le format
de reponse, par exemple `Reponse : ` suivi d'une lettre. Au lieu de laisser le modele
generer, on execute un seul passage avant et on lit la distribution de probabilite sur le
vocabulaire a la position de la reponse. On restreint aux K tokens correspondant aux
modalites et on renormalise. On obtient p(A), p(B), ..., p(K).

**Le gain en cout.** Generer du texte donne **un** tirage. Pour estimer la distribution
de reponse d'un persona a temperature non nulle, il faudrait N tirages, donc N appels.
Pour atteindre une erreur standard de 0,01 sur une proportion, N vaut environ 2 500.
La lecture des logprobs donne la distribution complete, exacte, sans bruit
d'echantillonnage, en **un** passage avant. Le facteur est de l'ordre de **1 000 a
2 500** sur cette question precise. Meme si l'on ne compare qu'a un unique tirage genere,
on economise le decodage : dans le cas de reference, 1,1 s de generation contre 0,04 s de
passage avant, soit un facteur 27 sur la partie decodage.

**Le gain scientifique, qui compte davantage.** La contribution visee par popsim est de
montrer que les LLM reproduisent la moyenne des opinions mais ecrasent la variance
inter-individuelle. Cette affirmation se decompose exactement :

```
Var_totale = E_persona[ Var_intra(persona) ]  +  Var_persona[ E(reponse | persona) ]
             \_______ bruit du modele _______/    \___ heterogeneite reproduite ___/
```

- Le terme de gauche est la variance **a l'interieur** d'un persona : le modele hesite.
- Le terme de droite est la variance **entre** personas : le modele differencie.

Le diagnostic de la litterature revient a dire que le terme de droite est trop petit et
que le terme de gauche est trop gros : le modele produit du bruit la ou il devrait
produire de l'heterogeneite. Or **les logprobs donnent directement les deux termes, par
persona et par question, sans aucun echantillonnage.** Pour un persona et une question,
la distribution p(.) donne son esperance et sa variance exactement. Il suffit ensuite
d'agreger sur les personas.

Avec du texte genere, il faut estimer les deux termes par echantillonnage, ce qui ajoute
un troisieme terme de bruit d'estimation qui se melange au premier et rend la
decomposition beaucoup plus fragile. **La methode des logprobs n'est donc pas seulement
moins chere, elle est methodologiquement superieure pour la question exacte que le projet
veut traiter.** C'est un argument a mettre dans le papier, pas seulement dans le plan de
budget.

Corollaire immediat : elle permet aussi de calculer des mesures de distance entre la
distribution simulee et la distribution observee dans l'enquete (divergence de
Kullback-Leibler, distance de variation totale, distance de Wasserstein sur des echelles
ordonnees), qui sont des statistiques bien plus informatives qu'un simple taux d'accord.

**Les pieges, tous evitables.**

1. **Tokenisation.** La lettre `A` precedee d'une espace n'est pas le meme token que `A`
   colle. Il faut identifier les identifiants de tokens exacts pour le format retenu et
   verifier que les K modalites correspondent a K tokens distincts et uniques. Sur une
   echelle de Likert a 7 points, utiliser les chiffres 1 a 7 est plus sur que des
   libelles.
2. **Biais de position.** Les modeles favorisent systematiquement certaines positions
   dans une liste. Il faut permuter l'ordre des modalites sur plusieurs passages et
   moyenner. Cela multiplie le cout par le nombre de permutations testees, typiquement 2
   a 4, ce qui reste negligeable au regard du facteur 1 000 gagne.
3. **Calibration.** Les probabilites du token ne sont pas des probabilites de population.
   Elles sont une statistique du modele, a recalibrer sur un jeu de validation avant
   toute interpretation quantitative. Ne jamais ecrire "le modele predit que 34 pour cent
   des gens repondront B" sans etape de calibration documentee.
4. **Disponibilite.** L'acces aux logprobs est **complet et gratuit en local** (MLX,
   llama.cpp). Il est **partiel chez Gemini** (`responseLogprobs`, support variable selon
   le modele et selon l'API). Il est **absent chez Groq**, qui renvoie une erreur 400.
   [CONFIRME] C'est un argument technique supplementaire, independant du cout, pour faire
   du local le moteur principal.

### Regle 3. Memoiser tous les appels, et journaliser les distributions, pas les decisions

Cle de cache = empreinte de (identifiant de modele, quantification, graine, temperature,
tous les parametres d'echantillonnage, tokens du prompt). Valeur = la distribution
complete sur les K modalites, plus les metadonnees.

Deux benefices distincts :

- **Rejouer une experience coute zero.** Toute correction d'analyse, tout changement de
  metrique, toute demande d'un relecteur se traite sans reappeler le modele. Sur un
  projet de recherche, ou l'analyse est reprise dix a vingt fois, c'est un facteur 10 a
  20 sur le budget total, plus important que n'importe quelle optimisation d'inference.
- **Journaliser la distribution, jamais seulement l'argmax.** Enregistrer `p(A)=0,41,
  p(B)=0,38, ...` plutot que `reponse=A`. La deuxieme forme detruit l'information dont
  le projet a precisement besoin, et la reconstituer exigerait de tout relancer.

Stockage : SQLite pour le cache d'appels en ecriture concurrente, DuckDB pour l'analyse.
Une distribution sur 7 modalites en flottant 32 bits pese 28 octets ; un million d'appels
tient dans quelques centaines de mega-octets avec les metadonnees.

### Regle 4. Dimensionner par un calcul de puissance, pas par prudence

La reflexe "il faut 10 000 agents" est une intuition commerciale, pas une exigence
statistique. Les chiffres :

- **Estimer un taux de reproduction autour de 85 pour cent avec un intervalle de
  confiance a 95 pour cent de plus ou moins 3 points** demande
  n = 1,96² x 0,85 x 0,15 / 0,03² = **544 items**. [CONFIRME, arithmetique directe]
- Mais les items d'un meme persona sont correles. L'effet de plan vaut
  DEFF = 1 + (m - 1) x ICC. Avec 30 items par persona et une correlation
  intra-classe de 0,10, DEFF = 3,9, donc **2 122 items reels, soit environ 71 personas
  a 30 items**. [PROBABLE, l'ICC est a estimer sur les premieres donnees, c'est
  l'inconnue de ce calcul]
- **Detecter un ecart de 5 points entre deux conditions**, alpha 0,05, puissance 0,80 :
  n = 2 x (1,96 + 0,84)² x 0,25 / 0,05² = **1 570 items par groupe**. [CONFIRME,
  arithmetique directe]
- **Detecter un ecart de 10 points** dans les memes conditions : **392 items par
  groupe**. [CONFIRME]
- **Detecter une correlation de 0,30** avec une puissance de 0,80 : environ **85
  observations**. [CONFIRME, valeur classique]

Conclusion operationnelle, qui devrait changer le plan de travail : **la phase 1 de
reproduction du resultat de Stanford ne demande pas 10 000 agents, elle en demande de
l'ordre de 70 a 100, sur 30 a 50 questions.** Soit 2 000 a 5 000 appels, soit **moins de
dix minutes de calcul local**. Le passage a 10 000 ou 20 000 agents n'est justifie que
pour la phase de simulation de sondage a l'echelle, ou l'objectif n'est plus d'estimer un
taux mais de reproduire une distribution de population stratifiee.

Corollaire budgetaire : le facteur limitant de la phase 1 n'est pas le calcul, c'est la
matiere humaine, qui est aujourd'hui indisponible par decision. Le calcul n'est un
probleme qu'a partir de la phase 2.

### Regle 5. Cascade petit modele, puis grand modele sur les cas litigieux

- **Passe 1.** Un modele de 4B en 4 bits traite l'integralite des items en mode logprobs,
  a environ 50 tokens par seconde de decodage et un prefill rapide. Cout : quelques
  minutes pour 10 000 items.
- **Critere de litige.** Un item est litigieux si la probabilite maximale sur les
  modalites est inferieure a un seuil (0,6 par exemple), ou si l'entropie normalisee de
  la distribution depasse un seuil. Ces criteres sont directement disponibles puisqu'on a
  la distribution complete, ce qui est un benefice supplementaire de la regle 2.
- **Passe 2.** Le modele 30B MoE, ou un appel a Gemini Flash gratuit, ne traite que les
  10 a 20 pour cent d'items litigieux.
- **Gain.** Le cout du grand modele est divise par **5 a 10**.
- **Garde-fou obligatoire.** Tirer au hasard 5 pour cent des items **non** litigieux et
  les passer aussi au grand modele. Si le taux de desaccord y est comparable a celui
  observe sur les litigieux, le critere de routage ne discrimine rien et la cascade
  introduit un biais. Sans ce controle, la cascade est une optimisation non publiable.

### Regle 6. Batcher, et quantifier le cache KV pour pouvoir batcher

Le batch continu apporte 2,6x a 3,7x de debit a 16 requetes simultanees.
[CONFIRME, arXiv:2601.19139v2, mesure sur M4 Max 128 Gio] Sur un M5 de base a 153 Go/s,
compter plutot 2x. [PROBABLE]

Le facteur limitant du batch sur cette machine n'est pas le calcul, c'est le cache KV :
128 Kio par token et par requete sur un 8B. Quantifier le cache KV en 8 bits divise cette
consommation par deux et permet de doubler le nombre de requetes simultanees a memoire
constante. C'est donc une condition du batch, pas une optimisation independante.

Regle de composition du batch : **grouper les requetes par prefixe partage.** Un batch de
16 questions du meme persona partage un seul cache de prefixe. Un batch de 16 questions
de 16 personas differents en exige 16, soit 16 Gio de cache pour 8 000 tokens de
contexte, ce qui ne tient pas. L'ordonnanceur d'experience doit donc trier par persona
avant de batcher, ce qui est trivial mais facile a oublier.

### Regle 7. Traiter les niveaux gratuits comme du controle, pas comme de la production

Detaille en section 3. Deux consequences concretes de conception :

- Ecrire le code contre une interface unique compatible OpenAI, avec le modele et
  l'adresse du serveur en configuration. llama.cpp, LM Studio, vllm-mlx, Groq, Gemini,
  Cerebras et NVIDIA NIM exposent tous cette interface. Changer de fournisseur devient
  une ligne de configuration, ce qui protege contre les baisses de quota, qui sont
  frequentes.
- Definir des le depart, dans le schema de donnees, un champ `data_policy` par appel
  (`local`, `api_no_training`, `api_may_train`). Sans lui, il sera impossible d'affirmer
  dans le papier quelles donnees sont sorties de la machine. C'est le genre d'omission
  qui coute une publication.

---

## 7. Pile recommandee par defaut

**Moteur principal.** llama.cpp / `llama-server` avec Metal, cache de prefixe par slot
(`--cache-prompt`, `--cache-reuse 256`), cache KV en 8 bits, batch parallele. Raison du
choix : c'est le plus robuste, le mieux documente, il donne un acces complet aux logits,
et son API est compatible OpenAI. Il est 20 a 40 pour cent plus lent que MLX, ce qui est
un prix acceptable pour la fiabilite en phase exploratoire.

**Moteur d'acceleration, a evaluer en parallele.** mlx-lm, avec `make_prompt_cache` et
des caches de prefixe serialises sur disque, un par persona. Basculer dessus si le gain
mesure justifie la moindre maturite. Verifier imperativement que le modele choisi n'est
pas a fenetre glissante, sinon le cache de prefixe est inoperant.

**Modeles.** Qwen3 4B en 4 bits pour la passe de degrossissage, Qwen3 30B-A3B en 4 bits
pour la passe de qualite. Le second offre le meilleur rapport qualite sur debit
accessible sur 32 Gio, parce que seuls 3 milliards de parametres sont lus par token.
Llama 3.1 8B en 4 bits comme troisieme famille, pour verifier que les resultats ne
dependent pas d'un fournisseur de modele.

**Methode d'appel.** Logprobs sur le token de reponse, jamais de generation de texte pour
les questions fermees. Permutation de l'ordre des modalites, deux a quatre passages.

**Stockage.** SQLite pour le cache d'appels, DuckDB pour l'analyse, Hugging Face Datasets
pour les jeux de donnees volumineux, GitHub pour le code seul. Pas de Git LFS.

**Suivi.** MLflow local en phase exploratoire. Weights and Biases avec la licence
academique des qu'une affiliation existe. Langfuse auto-heberge seulement si le besoin de
tracer des chaines d'appels devient reel, sinon une table `calls` dans DuckDB suffit.

**Calcul d'appoint.** Kaggle, 30 heures de GPU par semaine, pour tout ce qui demande
CUDA : vLLM avec prefix caching, Unsloth pour du fine tuning au dela de 8B, et les
bibliotheques qui ne tournent pas sur Metal.

**API gratuites.** Gemini Flash pour le controle de generalisation, sur donnees publiques
uniquement tant que la question EEE n'est pas tranchee. Cerebras pour verifier la
sensibilite au fournisseur. Groq ecarte pour la methode principale faute de logprobs.
OpenRouter ecarte pour cause de publication des prompts.

**Demarches a lancer, dans cet ordre.** Un rattachement a une structure de recherche
francaise pour GENCI, qui est le seul levier capable de debloquer des dizaines de
milliers d'heures GPU. Puis l'affiliation academique pour Google Cloud Research Credits
et Weights and Biases. Puis le dossier OpenAI Researcher Access, dont la revue de
septembre 2026 est imminente et dont deux axes prioritaires correspondent exactement a la
contribution visee.

**Volume d'experience realisable gratuitement par semaine, avec cette pile :** de l'ordre
de **400 000 appels de modele**, en retenant une marge de securite de 3 sur les
estimations. Contre environ **12 000** pour la totalite des offres gratuites d'API
cumulees.

---

## Ce que je n'ai pas pu verifier

1. **Le debit de prefill reel sur cette machine.** C'est l'hypothese la plus lourde du
   document. Toutes les durees des sections 2.3 reposent sur 800 tokens par seconde en
   prefill sur un 8B en 4 bits, valeur non mesuree. Apple publie des accelerations
   relatives (1,19x a 4,06x contre M4) sans donner la longueur des prompts, ce qui les
   rend inexploitables. **Si le prefill reel est de 300 t/s, toutes les durees sont
   multipliees par environ 2,5.** Premiere mesure a faire, elle prend dix minutes.
2. **Le debit de decodage reel.** 27 tokens par seconde sur un 8B en 4 bits est une
   estimation par deux methodes concordantes, pas une mesure.
3. **Les limites exactes du niveau gratuit de Gemini.** La documentation officielle ne
   publie plus de tableau et renvoie au tableau de bord AI Studio, inaccessible sans
   compte. Les valeurs de 15 RPM et 1 500 requetes par jour viennent de sources
   secondaires concordantes mais non officielles. Plusieurs sources signalent en outre
   que les limites affichees ne sont pas garanties et que la capacite reelle varie.
4. **La contradiction sur les donnees Gemini en Europe.** Le tableau de prix officiel dit
   que le contenu du niveau gratuit sert a ameliorer les produits Google. Les conditions
   d'utilisation prevoient une exception pour l'EEE, la Suisse et le Royaume-Uni. Je n'ai
   pas pu citer la clause mot a mot ni verifier laquelle prime. **A trancher avant tout
   envoi de donnees non publiques.**
5. **Le plafond de contexte du niveau gratuit de Cerebras.** Une source secondaire
   annonce 8 192 tokens, la documentation officielle ne le mentionne pas. Si c'est exact,
   Cerebras est inutilisable pour un persona de 8 000 tokens plus une question.
6. **La conversion des "neurons" Cloudflare en appels.** Impossible sans mesure sur un
   modele donne. Le quota de 10 000 neurons par jour est peut-etre negligeable, peut-etre
   utile.
7. **Les limites exactes du niveau Experiment de Mistral.** Mistral ne publie plus de
   chiffres et renvoie a la console admin, qui exige un compte verifie par telephone.
8. **Le programme academique OpenAI de juillet 2026.** L'article d'Axios qui le decrit
   renvoie une erreur 403. Toutes les informations le concernant viennent d'extraits de
   recherche, y compris la clause "quatre collaborateurs de son institution" qui est
   precisement le point qui deciderait de son utilite pour nous.
9. **Le delai reel d'un Acces Dynamique GENCI.** La formulation "quelques jours" vient de
   sources secondaires. Je n'ai pas trouve de statistique officielle sur les delais
   d'instruction ni sur le taux d'acceptation.
10. **Le support des logprobs par modele chez Gemini.** La fonctionnalite existe, mais
    des utilisateurs rapportent des erreurs "Logprobs is not enabled" selon les modeles,
    et l'API "Interactions" de nouvelle generation semble avoir omis ces champs. A tester
    modele par modele.
11. **La disponibilite des logits dans vllm-mlx.** Le papier ne le precise pas et je n'ai
    pas lu le code.
12. **Le quota Git LFS gratuit sur GitHub.** Sources contradictoires entre 1 Gio et
    10 Gio. Sans importance puisque la recommandation est de ne pas l'utiliser.
13. **Le statut de l'issue MLX sur le cache de prefixe des modeles a fenetre glissante.**
    Signalee, statut de correction non verifie.
14. **L'ICC entre items d'un meme persona**, qui pilote entierement le calcul de taille
    d'echantillon de la regle 4. C'est une quantite a estimer sur les premieres donnees,
    pas une constante.

---

## Questions ouvertes pour Simon

1. **Existe-t-il, dans ton reseau ou celui d'Amir, un rattachement possible a une
   structure de recherche francaise ?** Laboratoire universitaire, equipe INRIA, unite
   CNRS, ou un co-encadrement. C'est la seule condition pour un Acces Dynamique GENCI,
   qui vaut jusqu'a 50 000 heures GPU gratuites obtenues en quelques jours. Aucun autre
   levier de ce document n'a le meme rapport effort sur gain, et le contact MIT ne le
   debloque pas.
2. **Le contact MIT peut-il porter une affiliation academique nominative pour Amir ?**
   Visiting researcher, affilie, co-auteur declare. Cela conditionne Google Cloud
   Research Credits (jusqu'a 5 000 dollars), la licence Pro academique de Weights and
   Biases, et potentiellement le programme academique OpenAI.
3. **Est-il beneficiaire du programme academique OpenAI lance en juillet 2026, et la
   clause "quatre collaborateurs de son institution" peut-elle nous inclure ?** Si oui,
   c'est un acces gratuit aux modeles OpenAI jusqu'en 2027.
4. **Acceptes-tu que la phase 1 soit dimensionnee a 70 a 100 personas et 30 a 50
   questions, plutot qu'a 10 000 agents ?** Le calcul de puissance de la regle 4 montre
   que c'est suffisant pour estimer un taux de reproduction a plus ou moins 3 points. Le
   passage a l'echelle devient une phase 2, justifiee par la stratification de population
   et non par la precision statistique. Cela change le plan de travail.
5. **Confirmes-tu que la mesure de variance intra et inter personas par les probabilites
   du token de reponse est defendable pour la publication visee ?** C'est le pari
   methodologique central du document : il divise le cout par un facteur superieur a
   1 000 et donne la decomposition de variance exactement plutot que par echantillonnage.
   Si un relecteur exige des reponses generees en langage naturel, l'economie disparait
   et le budget de calcul est multiplie par mille. Cette question doit etre tranchee
   avant d'ecrire une ligne de pipeline.
6. **Quelles donnees pourront sortir de la machine ?** Les jeux d'enquete de type GSS ont
   des conditions de licence qu'il faut lire avant d'envoyer quoi que ce soit a une API
   gratuite. Tant que ce n'est pas tranche, le pipeline doit tourner integralement en
   local, ce qui est possible mais interdit les controles croises externes.
7. **Le precedent en psychiatrie publie dans Nature que tu evoques : as-tu la reference
   exacte ?** Le type de mesure de variance qu'ils utilisent determinerait directement
   quel format de reponse nous devons produire, donc le budget de calcul.
8. **Y a-t-il un horizon de constitution d'une entite juridique ?** NVIDIA Inception,
   Microsoft for Startups et AWS Activate sont accessibles a un projet auto-finance, mais
   exigent une societe immatriculee. Sans entite, ces trois canaux restent fermes.
9. **Weights and Biases reserve sa licence academique gratuite a une recherche non liee a
   une entite a but lucratif.** Si popsim devient une societe, cette licence tombe. Vaut-il
   mieux batir le suivi d'experiences sur MLflow local des le depart pour eviter cette
   dependance ?
