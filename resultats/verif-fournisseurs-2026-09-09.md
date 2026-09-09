# Vérification de faits, fournisseurs et voies de publication

Date de consultation de toutes les sources : 2026-09-09.
Méthode : lecture directe des pages officielles (WebFetch) et du code source public (raw.githubusercontent, API GitHub). Aucun modèle lancé, aucun appel d'API payant, aucune donnée du projet transmise.

Charge de référence utilisée dans tout le document : 894 requêtes par modèle et par format, 2 formats, soit 1 788 requêtes, 320 jetons d'entrée et 20 jetons de sortie par requête. Total par modèle : 572 160 jetons d'entrée (0,572 M) et 35 760 jetons de sortie (0,036 M), environ 608 000 jetons au total.

---

## 1. Niveaux gratuits d'API

| Fournisseur | Quotas du niveau gratuit | Modèles | Entrées utilisées pour l'entraînement ? | Source | Consulté |
|---|---|---|---|---|---|
| Google AI Studio (Gemini) | Les quotas RPM, TPM et RPD par modèle **ne sont plus publiés** dans la doc. La page dit : « View your active rate limits in AI Studio », les limites sont propres au projet. Le RPD se réinitialise à minuit heure du Pacifique. Limites appliquées par projet, pas par clé. Palier Free : plafond de facturation N/A, pas de limite de dépense sur 10 minutes | Free tier disponible sur Gemini 3.8 Flash, 3.7 Flash, 3.5 Flash, 3.5 Flash-Lite, 2.5 Flash, 2.5 Flash-Lite, 2.5 Pro | **Oui.** La grille tarifaire indique pour chaque modèle, niveau gratuit : « Content used to improve our products ». Niveau payant : « Content not used » | [ai.google.dev/gemini-api/docs/rate-limits](https://ai.google.dev/gemini-api/docs/rate-limits) (page datée « Last updated 2026-09-02 UTC »), [ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing) | 2026-09-09 |
| Groq | 30 RPM, 1 000 RPD, 8 000 TPM, 200 000 TPD pour la plupart des modèles texte. Orpheus : 10 RPM, 100 RPD. Whisper : 20 RPM, 2 000 RPD | gpt-oss-120b, gpt-oss-20b, gpt-oss-safeguard-20b, qwen3.6-27b, qwen3.8-27b, groq/compound, groq/compound-mini, llama-prompt-guard-2, whisper | **Non établi.** Les CGU du site renvoient au « Groq Services Agreement », la politique de confidentialité exclut explicitement les « Customer Data » de son périmètre | [console.groq.com/docs/rate-limits](https://console.groq.com/docs/rate-limits), [groq.com/terms-and-conditions](https://groq.com/terms-and-conditions/), [groq.com/privacy-policy](https://groq.com/privacy-policy/) | 2026-09-09 |
| Cerebras | Free Trial : 5 RPM, 30 000 TPM, 1 M TPH, 1 M TPD. Le palier Developer annonce « 10x higher rate limits than free tier », accessible dès 10 dollars | gpt-oss-120b et qwen-3.8-27b sur le Free Trial | Non établi sur les pages consultées | [inference-docs.cerebras.ai/support/rate-limits](https://inference-docs.cerebras.ai/support/rate-limits), [cerebras.ai/pricing](https://www.cerebras.ai/pricing) | 2026-09-09 |
| OpenRouter (modèles `:free`) | 20 RPM et **50 requêtes par jour** si moins de 10 dollars de crédits achetés. 20 RPM et **1 000 requêtes par jour** au delà de 10 dollars achetés. « Making additional accounts or API keys will not affect your rate limits, as we govern capacity globally » | Tous les modèles dont l'identifiant finit par `:free` | Réglage par compte, « There are separate settings for paid and free models » ; « If you opt out of training in your account settings, OpenRouter will not route to providers that train ». Le comportement par défaut des points d'accès gratuits n'est pas précisé dans la doc | [openrouter.ai/docs/api-reference/limits](https://openrouter.ai/docs/api-reference/limits), [openrouter.ai/docs/features/privacy-and-logging](https://openrouter.ai/docs/features/privacy-and-logging) | 2026-09-09 |
| Mistral (La Plateforme) | **Il n'y a plus de niveau gratuit à quotas.** Le plan Free donne « $10 /mo in API credits ». Aucune page de limites par palier n'a été trouvée en accès public | Mistral Medium 3.5, Small 4, Large 3, Ministral 3 (3B, 8B, 14B), GLM 5.2, Codestral, etc. | Non établi, le centre juridique ne sert qu'un index, le texte des CGU n'est pas rendu | [mistral.ai/pricing](https://mistral.ai/pricing), [docs.mistral.ai/getting-started/models/models_overview](https://docs.mistral.ai/getting-started/models/models_overview/) | 2026-09-09 |

**Faisabilité de la charge sur les niveaux gratuits, calcul dérivé des quotas ci dessus :**

| Voie gratuite | Goulot | Durée par modèle (2 formats) |
|---|---|---|
| Groq | TPD 200 000 | 608 000 / 200 000, soit environ 3 jours |
| Cerebras Free Trial | RPM 5 | 1 788 / 5, soit environ 6 heures ; TPD 1 M largement suffisant |
| OpenRouter sans crédits | 50 RPD | environ 36 jours, inutilisable |
| OpenRouter avec 10 dollars de crédits | 1 000 RPD | environ 2 jours |
| Gemini free tier | inconnu | non chiffrable, à lire dans AI Studio une fois le projet créé |

---

## 2. Probabilités par jeton (logprobs)

| API | Disponible ? | Détail | Source | Consulté |
|---|---|---|---|---|
| OpenAI | Oui | `logprobs` booléen, `top_logprobs` « an integer between 0 and 20 ». `logprobs` doit valoir `true` si `top_logprobs` est utilisé. La doc précise que « parameter support can differ depending on the model used », en visant les modèles de raisonnement. Le cookbook, plus ancien, mentionne une borne de 0 à 5 et des exemples sur gpt-4o et gpt-4o-mini | [developers.openai.com/api/docs/api-reference/chat/create](https://developers.openai.com/api/docs/api-reference/chat/create), [developers.openai.com/cookbook/examples/using_logprobs](https://developers.openai.com/cookbook/examples/using_logprobs) | 2026-09-09 |
| Google Gemini | Oui | `GenerationConfig.response_logprobs` (booléen) et `GenerationConfig.logprobs` (entier, « Number of top candidate tokens to return the log probabilities for at each generation step »). Réponse : `logprobs_result` et `avg_logprobs` sur le candidat. Champs présents dans le SDK officiel `google-genai` | code source : [googleapis/python-genai, google/genai/types.py](https://raw.githubusercontent.com/googleapis/python-genai/main/google/genai/types.py), lignes 6507, 6513, 8291, 8299 | 2026-09-09 |
| Anthropic | **Non** | La liste complète des paramètres du corps de `/v1/messages` ne contient ni `logprobs` ni `top_logprobs` : max_tokens, messages, model, cache_control, container, inference_geo, metadata, output_config, service_tier, stop_sequences, stream, system, thinking, tool_choice, tools, temperature, top_k, top_p | [platform.claude.com/docs/en/api/messages](https://platform.claude.com/docs/en/api/messages) | 2026-09-09 |
| xAI (Grok) | **Non sur les modèles récents** | « logprobs and top_logprobs are not supported by models grok-4.20 and newer », les paramètres « will be silently ignored if set ». Le tableau des modèles marque « No » pour grok-4.6, 4.5, 4.3, 4.20 | [docs.x.ai/docs/models](https://docs.x.ai/docs/models) | 2026-09-09 |
| Mistral | **Non** | La liste des paramètres de `/v1/chat/completions` ne contient ni `logprobs` ni `top_logprobs` | [docs.mistral.ai/api](https://docs.mistral.ai/api/) | 2026-09-09 |
| OpenRouter | Oui, en théorie | `logprobs` booléen, `top_logprobs` entier de 0 à 20, `logprobs` doit valoir `true`. La doc renvoie à la section du fournisseur pour savoir si le modèle visé les accepte | [openrouter.ai/docs/api-reference/parameters](https://openrouter.ai/docs/api-reference/parameters) | 2026-09-09 |
| DeepSeek | Non vérifié, voir la dernière section | | | |

**Conséquence pour la lecture d'une distribution sur des lettres de réponse :** seules OpenAI, Gemini et OpenRouter (selon le fournisseur en aval) permettent la mesure directe. Anthropic, xAI récent et Mistral imposent la voie indirecte, par échantillonnage répété.

---

## 3. Tarifs par million de jetons et coût de la charge

Coût par modèle et par campagne complète : 0,572 M jetons d'entrée et 0,036 M jetons de sortie.

| Modèle | Entrée / M | Sortie / M | Coût de la campagne | Source | Consulté |
|---|---|---|---|---|---|
| gpt-6-astra | 10,00 | 50,00 | 7,51 USD | [developers.openai.com/docs/pricing](https://developers.openai.com/docs/pricing) | 2026-09-09 |
| gpt-5.6-sol | 4,00 | 20,00 | 3,00 USD | idem | 2026-09-09 |
| gpt-5.6-terra | 2,00 | 12,00 | 1,57 USD | idem | 2026-09-09 |
| gpt-5.6-luna | 0,20 | 1,20 | 0,16 USD | idem | 2026-09-09 |
| gpt-5.4 | 2,50 | 15,00 | 1,97 USD | idem | 2026-09-09 |
| gpt-5.4-mini | 0,75 | 4,50 | 0,59 USD | idem | 2026-09-09 |
| gpt-5.4-nano | 0,20 | 1,25 | 0,16 USD | idem | 2026-09-09 |
| gpt-5.1 et gpt-5 | 1,25 | 10,00 | 1,07 USD | idem | 2026-09-09 |
| gpt-5-mini | 0,25 | 2,00 | 0,21 USD | idem | 2026-09-09 |
| gpt-5-nano | 0,05 | 0,40 | 0,04 USD | idem | 2026-09-09 |
| gpt-4.1 | 2,00 | 8,00 | 1,43 USD | idem | 2026-09-09 |
| gpt-4o-mini | 0,15 | 0,60 | 0,11 USD | idem | 2026-09-09 |
| Claude Opus 5 | 5,00 | 25,00 | 3,75 USD | [claude.com/pricing](https://claude.com/pricing) | 2026-09-09 |
| Claude Sonnet 5 | 2,00 | 10,00 | 1,50 USD | idem | 2026-09-09 |
| Claude Haiku 4.5 | 1,00 | 5,00 | 0,75 USD | idem | 2026-09-09 |
| Gemini 3.8 Flash (tarif promotionnel jusqu'au 31/12/2026) | 0,75 | 3,75 | 0,56 USD | [ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing) | 2026-09-09 |
| Gemini 3.8 Flash (tarif après promotion) | 1,50 | 7,50 | 1,12 USD | idem | 2026-09-09 |
| Gemini 3.5 Flash | 1,50 | 9,00 | 1,18 USD | idem | 2026-09-09 |
| Gemini 3.5 Flash-Lite | 0,30 | 2,50 | 0,26 USD | idem | 2026-09-09 |
| Gemini 2.5 Flash-Lite | 0,10 | 0,40 | 0,07 USD | idem | 2026-09-09 |
| Gemini 2.5 Pro (jusqu'à 200k) | 1,25 | 10,00 | 1,07 USD | idem | 2026-09-09 |
| grok-4.6 (moins de 200k de contexte) | 2,00 | 6,00 | 1,36 USD | [docs.x.ai/docs/models](https://docs.x.ai/docs/models) | 2026-09-09 |
| grok-4.3 (moins de 200k de contexte) | 1,25 | 2,50 | 0,80 USD | idem | 2026-09-09 |
| deepseek-v4-flash (heures pleines, cache miss) | 0,44 | 1,32 | 0,30 USD | [api-docs.deepseek.com/quick_start/pricing](https://api-docs.deepseek.com/quick_start/pricing/) | 2026-09-09 |
| deepseek-v4-flash (heures creuses) | 0,22 | 0,66 | 0,15 USD | idem | 2026-09-09 |
| deepseek-v4-pro (heures pleines) | 1,32 | 3,96 | 0,90 USD | idem | 2026-09-09 |
| Mistral Medium 3.5 | 1,50 | 7,50 | 1,13 USD | [mistral.ai/pricing/api](https://mistral.ai/pricing/api) | 2026-09-09 |
| Mistral Large 3 | 0,50 | 1,50 | 0,34 USD | idem | 2026-09-09 |
| Mistral Small 4 | 0,15 | 0,60 | 0,11 USD | idem | 2026-09-09 |
| Ministral 3 (14B) | 0,20 | 0,20 | 0,12 USD | idem | 2026-09-09 |

Remarques tarifaires vérifiées : DeepSeek applique un tarif heures creuses à la moitié du tarif heures pleines, les heures pleines étant 01:00 à 04:00 et 06:00 à 10:00 UTC du lundi au vendredi. OpenAI applique 50 pour cent de remise en mode Batch et en mode Flex, et une majoration de 10 pour cent pour les points d'accès à résidence des données sur les modèles publiés à partir du 5 mars 2026. Mistral annonce jusqu'à 90 pour cent de remise sur les jetons d'entrée mis en cache et 50 pour cent en traitement par lots.

**Ordre de grandeur pour un panel de dix modèles phares payants : environ 20 à 25 USD.** Un panel de dix modèles économiques (nano, mini, lite, flash) coûte moins de 2 USD. Le budget de 100 EUR n'est pas le facteur limitant, la contrainte réelle est la disponibilité des logprobs.

---

## 4. OLMo (Allen AI)

| Point | Constat | Source | Consulté |
|---|---|---|---|
| Familles existantes | **Olmo 3** en 7B et 32B. **OLMo 2** en 7B et 13B (et une variante 32B Instruct diffusée en GGUF officiel). Une famille Olmo-Hybrid 7B et une famille OLMoE 1B-7B existent aussi | [allenai.org/olmo](https://allenai.org/olmo), [huggingface.co/allenai](https://huggingface.co/allenai/models?search=olmo) | 2026-09-09 |
| Tailles 1B et 13B | **Pas de 1B ni de 13B dans Olmo 3.** Le 13B existe dans OLMo 2. Le 1B n'existe que sous la forme OLMoE 1B-7B (mélange d'experts) | [huggingface.co/allenai/Olmo-3-32B-Think](https://huggingface.co/allenai/Olmo-3-32B-Think), [huggingface.co/allenai/OLMo-2-1124-7B](https://huggingface.co/allenai/OLMo-2-1124-7B) | 2026-09-09 |
| Points de contrôle par étape, Olmo 3 | Quatre étapes publiées et séparées, pour chaque branche Instruct et chaque branche Think : Base (Olmo-3-1025-7B, Olmo-3-1125-32B), SFT (Olmo-3-7B-Think-SFT, Olmo-3-32B-Think-SFT), DPO (Olmo-3-7B-Think-DPO, Olmo-3-32B-Think-DPO), final RLVR (Olmo-3-7B-Think, Olmo-3-32B-Think). Plus une série RL-Zero en 7B : Math, Code, IF, General, Mix | [huggingface.co/allenai/Olmo-3-32B-Think](https://huggingface.co/allenai/Olmo-3-32B-Think), [huggingface.co/allenai/Olmo-3-7B-Instruct](https://huggingface.co/allenai/Olmo-3-7B-Instruct) | 2026-09-09 |
| Points de contrôle intermédiaires de préentraînement | Publiés comme révisions git, nommées `stepXXX-tokensYYYB`. Chargement : `AutoModelForCausalLM.from_pretrained("allenai/OLMo-2-1124-7B", revision="step1000-tokens5B")` | [huggingface.co/allenai/OLMo-2-1124-7B](https://huggingface.co/allenai/OLMo-2-1124-7B) | 2026-09-09 |
| Licence et dates | Apache 2.0. OLMo 2 : décembre 2024, arXiv 2501.00656. Olmo 3 : rapport technique arXiv 2512.13961, daté du 15 décembre 2025 | idem | 2026-09-09 |
| GGUF et llama.cpp | **Pris en charge nativement.** Trois architectures dans llama.cpp : `olmo`, `olmo2`, `olmoe`. Le convertisseur enregistre `Olmo3ForCausalLM` sur l'architecture `OLMO2`, avec pour exemple officiel `allenai/Olmo-3-7B-Instruct`, et gère la fenêtre glissante propre à Olmo 3 (« Olmo3 defaults to using sliding window for all layers except every 4th ») | code source : [llama-arch.cpp](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/src/llama-arch.cpp), [conversion/olmo.py](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/conversion/olmo.py) | 2026-09-09 |
| GGUF déjà publiés | `unsloth/Olmo-3-7B-Think-GGUF` (mis à jour le 21/11/2025). Pour OLMo 2 32B Instruct, GGUF officiel `allenai/OLMo-2-0325-32B-Instruct-GGUF`, plus unsloth, mradermacher, MaziyarPanahi, tensorblock, DevQuasar | [huggingface.co/models?search=Olmo-3+GGUF](https://huggingface.co/models?search=Olmo-3+GGUF) | 2026-09-09 |

**Conséquence :** les étapes SFT, DPO et RLVR d'Olmo 3 sont directement comparables sur une même famille, et convertibles en GGUF sur le MacBook Air M5 pour le 7B. Le 32B en quantification basse reste possible sur 32 Go, mais serré.

---

## 5. arXiv, endossement et solutions de repli

| Point | Constat | Source | Consulté |
|---|---|---|---|
| Qui doit être endossé | Tout nouveau déposant, avant sa première soumission, et à chaque nouvelle catégorie. Le système « verifies that arXiv contributors belong to the scientific community » | [info.arxiv.org/help/endorsement.html](https://info.arxiv.org/help/endorsement.html) | 2026-09-09 |
| Adresse académique | Elle n'exempte pas automatiquement. L'endossement automatique suppose d'avoir revendiqué la propriété d'articles antérieurs. Sans adresse institutionnelle, il faut un endossement personnel | idem | 2026-09-09 |
| Auteur sans affiliation | Rien n'interdit de déposer, mais il faut obtenir l'endossement d'un auteur arXiv établi du domaine | idem | 2026-09-09 |
| Qui peut endosser | Un auteur ayant publié un nombre suffisant d'articles dans le domaine d'endossement de la catégorie, seuil variable et calibré pour que « any active scientist who has been working in their field for a few years should be able to endorse ». Seuls comptent les articles déposés entre trois mois et cinq ans avant | idem | 2026-09-09 |
| Nature de l'endossement | « Endorsement is not peer review ». L'endosseur vérifie l'adéquation au domaine et la maîtrise des notions de base, sans examiner l'article en détail | idem | 2026-09-09 |
| Seuils propres à cs.CL, cs.CY, stat.AP | Non publiés, voir la dernière section | | |
| SocArXiv | Gratuit, sans affiliation exigée, DOI et URL pérenne attribués. Modération sous deux jours environ, sur sept critères : caractère scientifique et complet, domaine couvert, catégorisation correcte, absence de fraude, attribution correcte, langue prise en charge, format cherchable (PDF ou DOCX). Ce n'est pas une évaluation par les pairs | [socopen.org/frequently-asked-questions](https://socopen.org/frequently-asked-questions/), [socopen.org](https://socopen.org/) | 2026-09-09 |
| OSF Preprints | DOI et URL pérenne à l'acceptation. Affiliation institutionnelle non requise, elle n'est qu'un habillage optionnel. Prémodération : la soumission reste privée jusqu'à décision du modérateur | [help.osf.io/article/376-preprint-faqs](https://help.osf.io/article/376-preprint-faqs) | 2026-09-09 |

**Conséquence :** SocArXiv est la voie sans friction et sans endossement, avec DOI. Un endossement arXiv reste souhaitable pour la visibilité en cs.CL, et Simon est le levier naturel s'il a déposé dans la catégorie visée dans les cinq dernières années.

---

## 6. OSF, préenregistrement horodaté

| Question | Réponse vérifiée | Source | Consulté |
|---|---|---|---|
| Sans affiliation institutionnelle ? | Oui. Un compte OSF suffit, aucune condition d'affiliation n'est posée. L'affiliation est un champ de métadonnées facultatif | [help.osf.io/article/145-preregistration](https://help.osf.io/article/145-preregistration), [help.osf.io/article/330-welcome-to-registrations](https://help.osf.io/article/330-welcome-to-registrations) | 2026-09-09 |
| Quel formulaire | Plus de treize modèles. Les plus pertinents ici : « OSF Preregistration » (formulaire général et complet), « Secondary Data Preregistration » (adapté à une réanalyse de données d'enquête existantes), « Simulation Studies », « AsPredicted.org », « Open-Ended Registration », « Registered Report Protocol » | [help.osf.io/article/145-preregistration](https://help.osf.io/article/145-preregistration) | 2026-09-09 |
| Horodatage public et vérifiable | Oui. « the date created will be the date submitted », quelle que soit la date d'approbation, et cet horodatage est visible publiquement sur la page de la registration acceptée | [help.osf.io/article/330-welcome-to-registrations](https://help.osf.io/article/330-welcome-to-registrations) | 2026-09-09 |
| Immuabilité | Oui. Une registration est « a frozen version of your project that can never be edited or deleted » | idem | 2026-09-09 |
| DOI | Attribué automatiquement aux registrations publiques. Pas de DOI tant qu'un embargo court | idem | 2026-09-09 |
| Embargo | Possible jusqu'à quatre ans, publication automatique à l'expiration | [help.osf.io/article/145-preregistration](https://help.osf.io/article/145-preregistration) | 2026-09-09 |
| Retrait | Possible mais irréversible. Le formulaire et les fichiers disparaissent, les métadonnées (titre, contributeurs, DOI, date de création) et la justification du retrait restent visibles | [help.osf.io/article/330-welcome-to-registrations](https://help.osf.io/article/330-welcome-to-registrations) | 2026-09-09 |
| Délai d'approbation | Approbation automatique au bout de 48 heures si les administrateurs n'agissent pas | [help.osf.io/article/145-preregistration](https://help.osf.io/article/145-preregistration) | 2026-09-09 |

---

## 7. Financement d'une expérience en ligne

| Point | Constat | Source | Consulté |
|---|---|---|---|
| Tarif Prolific, rémunération participant | Recommandé : 9,00 GBP ou 12,00 USD de l'heure. Minimum autorisé : 6,00 GBP ou 8,00 USD de l'heure | [prolific.com/pricing](https://www.prolific.com/pricing) | 2026-09-09 |
| Frais de plateforme Prolific | 42,8 pour cent en tarif à la consommation pour les clients entreprise, **33,3 pour cent en tarif académique ou association** | idem | 2026-09-09 |
| Coût d'une étude de 10 minutes, calcul dérivé | Au tarif recommandé : 1,50 GBP de récompense, plus 33,3 pour cent, soit **2,00 GBP par participant**. Au minimum autorisé : 1,00 GBP plus 33,3 pour cent, soit 1,33 GBP | dérivé des chiffres ci dessus | 2026-09-09 |
| Budget total dérivé | 200 participants : 400 GBP au tarif recommandé, 266 GBP au minimum. 2 000 participants : **4 000 GBP** au tarif recommandé, 2 666 GBP au minimum. La fourchette 900 à 9 000 GBP de la question suppose donc soit une étude plus longue que 10 minutes, soit une rémunération supérieure à 9 GBP de l'heure | dérivé | 2026-09-09 |
| Programme de bourses Prolific | **Aucune page publique trouvée.** Les URL candidates renvoient 404 | tentatives sur prolific.com/research-grants, prolific.com/prolific-grants, prolific.com/academia | 2026-09-09 |
| Center for Open Science | **Aucun programme de bourse ou de prix ouvert aux chercheurs externes n'est présenté** sur la page consultée. COS met à disposition l'OSF gratuitement, préenregistrement et Registered Reports compris | [cos.io/grants](https://www.cos.io/grants) | 2026-09-09 |
| Emergent Ventures (Mercatus) | Programme de bourses à faible bureaucratie pour « entrepreneurs and brilliant minds with highly scalable, zero to one ideas », dirigé par Tyler Cowen depuis 2018. Candidature apparemment au fil de l'eau, aucune date limite affichée, âge minimum 13 ans. Ni le montant type ni une condition d'affiliation ne sont indiqués sur la page | [mercatus.org/emergent-ventures](https://www.mercatus.org/emergent-ventures) | 2026-09-09 |
| Manifund | « the market for grants », plateforme de financement de projets avec certificats d'impact. Les conditions d'éligibilité et les montants ne figurent pas sur la page d'accueil | [manifund.org](https://manifund.org/) | 2026-09-09 |
| Political Analysis, frais de publication | APC en libre accès : **2 610 GBP ou 3 655 USD**, taxes en sus. Aucune politique de dispense n'est mentionnée sur la page des tarifs | [cambridge.org, Political Analysis, fees and pricing](https://www.cambridge.org/core/journals/political-analysis/information/author-instructions/fees-and-pricing) | 2026-09-09 |
| Political Analysis, préprints | Autorisés : « deposition of a preprint on the author's personal website, in an institutional repository, or in a preprint archive shall not be viewed as prior or duplicate publication » | [cambridge.org, Political Analysis, preparing your materials](https://www.cambridge.org/core/journals/political-analysis/information/author-instructions/preparing-your-materials) | 2026-09-09 |
| PNAS Nexus, frais | Un calculateur de frais est fourni, sans grille publique. Remises pour les auteurs des pays à revenu faible et intermédiaire, avec une politique de dispense et de remise d'APC | [academic.oup.com/pnasnexus, general instructions](https://academic.oup.com/pnasnexus/pages/general-instructions) | 2026-09-09 |
| PNAS Nexus, préprints | Autorisés sans restriction : l'auteur conserve le droit de diffuser la version préprint, et cela n'empêche pas la soumission. Mise à jour du DOI publié exigée après acceptation | idem | 2026-09-09 |
| PNAS Nexus, délais | Pas de délai de première décision annoncé. Publication en « Accepted Manuscript » sous environ 48 heures après acceptation, version finale sous 30 jours | idem | 2026-09-09 |

---

## 8. Location de GPU à l'heure

| Fournisseur | A100 80 Go | H100 | Source | Consulté |
|---|---|---|---|---|
| RunPod, Community Cloud | 1,19 USD/h (PCIe), 1,39 USD/h (SXM) | 1,99 USD/h (PCIe), 2,69 USD/h (SXM) | [runpod.io/pricing](https://www.runpod.io/pricing) | 2026-09-09 |
| RunPod, Secure Cloud | 1,59 USD/h | 2,89 USD/h (PCIe), 3,49 USD/h (SXM) | idem | 2026-09-09 |
| Lambda, à la demande | 2,79 USD/h par GPU (SXM, instance 8 GPU) | 3,99 USD/h par GPU (SXM) | [lambda.ai/service/gpu-cloud](https://lambda.ai/service/gpu-cloud) | 2026-09-09 |
| Vast.ai | prix dynamiques, non publiés en texte sur les pages consultées | idem | [vast.ai/pricing](https://vast.ai/pricing) | 2026-09-09 |

**50 EUR suffisent ils pour un LoRA sur un modèle de 8 milliards, environ 100 000 exemples courts ?** Estimation dérivée, non sourcée : 100 000 exemples d'environ 256 jetons représentent environ 25,6 M jetons par époque. Sur un A100 80 Go, un LoRA sur un modèle de 8B tient largement en mémoire et traite couramment 3 000 à 6 000 jetons par seconde, soit une à trois heures par époque, deux à six heures pour deux ou trois époques, plus une marge d'installation et de mise au point. À 1,19 USD/h en Community Cloud RunPod, cela représente **7 à 15 USD**, et jusqu'à 25 USD sur H100 SXM avec un temps plus court. **Oui, 50 EUR suffisent, avec une marge d'environ un facteur trois.** La partie sourcée de cette réponse est le prix horaire, le débit d'entraînement est une estimation à vérifier sur un essai court avant de réserver.

---

## 9. Conférences et revues

| Voie | Dates et règles | Source | Consulté |
|---|---|---|---|
| **ICLR 2027** | Résumé : **18 septembre 2026** AOE. Article : **25 septembre 2026** AOE. Retour des évaluations : 5 novembre 2026. Décisions : 16 décembre 2026. Conférence : 26 au 30 avril 2027. Double aveugle. arXiv autorisé : « Having papers on arxiv is allowed per the dual submission policy » | [iclr.cc/Conferences/2027/CallForPapers](https://iclr.cc/Conferences/2027/CallForPapers) | 2026-09-09 |
| **NeurIPS 2026, piste Datasets and Benchmarks** | **Échéances passées.** Résumé : 4 mai 2026. Article : 6 mai 2026. Évaluations : 22 juillet 2026. Notifications : 24 septembre 2026. Conférence : Sydney 6 au 12 décembre 2026, Atlanta et Paris 9 au 13 décembre 2026. La piste porte le nom « Evaluations/Datasets » et partage les dates de la piste principale | [neurips.cc/Conferences/2026/Dates](https://neurips.cc/Conferences/2026/Dates) | 2026-09-09 |
| **ACL Rolling Review, cycles** | Cycle mars 2026 : dépôt 16 mars, engagement EMNLP 2026 et AACL 2026 le 2 août. Cycle mai 2026 : dépôt 25 mai, même engagement. Cycle août 2026 : dépôt 3 août, engagement EACL 2027 le 11 octobre. **Cycle octobre 2026 : dépôt 12 octobre 2026, engagement NAACL 2027 et COLING 2027 le 23 décembre 2026.** Cycle janvier 2027 : ACL 2027 | [aclrollingreview.org/dates](https://aclrollingreview.org/dates) | 2026-09-09 |
| **ARR, anonymat** | Politique en vigueur depuis le 15 février 2024 : les auteurs « are free to post and discuss non-anonymous preprints at any time ». La restriction d'un mois avant la date limite a été supprimée. Réserve : une diffusion large « will make it harder to recruit reviewers » | [aclrollingreview.org/anonymity](https://aclrollingreview.org/anonymity) | 2026-09-09 |
| **EMNLP 2026** | Budapest, 24 au 29 octobre 2026. Dépôt ARR 25 mai 2026, engagement 2 août 2026, notification 20 août, version finale 30 août. **Échéances passées.** | [2026.emnlp.org](https://2026.emnlp.org/) | 2026-09-09 |
| **ACL 2026** | San Diego, 2 au 7 juillet 2026. Engagement ARR au 14 mars 2026. **Échéances passées.** | [2026.aclweb.org](https://2026.aclweb.org/) | 2026-09-09 |
| Political Analysis | APC 2 610 GBP ou 3 655 USD, préprint autorisé, délai de première décision non publié | voir point 7 | 2026-09-09 |
| PNAS Nexus | Frais par calculateur, préprint autorisé sans restriction, délai de première décision non publié | voir point 7 | 2026-09-09 |

**Fenêtres réellement ouvertes à ce jour :** ICLR 2027 dans neuf jours pour le résumé, ARR cycle octobre 2026 dans trente trois jours. Aucune des deux ne pose de condition d'affiliation dans les documents consultés.

---

## Ce que je n'ai pas pu vérifier

1. **Quotas chiffrés du niveau gratuit Gemini.** Google a retiré la table RPM/TPM/RPD par modèle de sa documentation publique. La page (mise à jour le 2026-09-02) renvoie à la page Rate Limit d'AI Studio, qui exige une connexion. Seul le fait que le palier Free existe et que le RPD se réinitialise à minuit heure du Pacifique est établi.
2. **Politique d'entraînement de Groq sur les entrées.** Les CGU du site excluent explicitement l'usage de GroqCloud, et la politique de confidentialité exclut les « Customer Data » de son périmètre en renvoyant au « Groq Services Agreement » et au « Data Processing Addendum », documents que je n'ai pas pu ouvrir.
3. **Politique d'entraînement de Cerebras et de Mistral.** Le centre juridique de Mistral (legal.mistral.ai/terms) ne sert qu'un index de liens, sans le texte des conditions. Aucune page de conditions Cerebras n'a été atteinte.
4. **Comportement par défaut d'OpenRouter sur les points d'accès gratuits.** La doc confirme l'existence de « separate settings for paid and free models » et la possibilité de refuser l'entraînement, mais ne dit pas si les modèles `:free` exigent d'accepter la journalisation ou l'entraînement.
5. **Limites par palier de La Plateforme (Mistral).** Aucune page de quotas publique atteinte, trois URL candidates en 404. Seul le fait établi : le plan Free donne 10 USD de crédits par mois, il n'y a plus de quota gratuit en jetons.
6. **Logprobs chez DeepSeek.** La page de référence de l'API n'a pas été ouverte, seule la grille tarifaire l'a été. À vérifier avant de compter DeepSeek dans le protocole de mesure directe.
7. **Restrictions de modèles pour les logprobs OpenAI.** La doc dit que la prise en charge des paramètres varie selon le modèle et renvoie à la documentation des modèles de raisonnement, sans liste. Il faut tester `logprobs=true` sur chaque modèle du panel avant de figer le protocole. La borne de `top_logprobs` diffère entre la référence de l'API (0 à 20) et le cookbook (0 à 5) : c'est la référence de l'API qui fait foi, mais le point mérite un test.
8. **Seuils d'endossement arXiv propres à cs.CL, cs.CY et stat.AP.** arXiv indique explicitement que les seuils varient par domaine et ne les publie pas.
9. **Prix Vast.ai.** Les pages produit ne rendent pas les prix en texte, ils sont servis dynamiquement par la console.
10. **Programme de bourses Prolific.** Aucune page publique trouvée sur trois URL candidates, il se peut qu'il n'existe pas ou qu'il ait été retiré.
11. **Montants et éligibilité d'Emergent Ventures et de Manifund.** Les pages d'accueil ne portent ni montant type ni condition d'affiliation.
12. **Barème d'APC de PNAS Nexus.** Servi par un calculateur, pas par une grille en texte.
13. **Délais de première décision de Political Analysis et de PNAS Nexus.** Non publiés sur les pages d'instructions aux auteurs.
14. **Longueur de contexte d'Olmo 3.** Non indiquée sur les cartes de modèle consultées.
15. **Recherche par mots clés.** Le budget de recherche web de la session était épuisé, toute la vérification s'est faite par accès direct aux URL canoniques et au code source. Des programmes de financement 2026 sans URL canonique connue de moi n'ont donc pas pu être découverts.
