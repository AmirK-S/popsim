# Pré-mortem du moonshot 2, « le discours précède-t-il l'opinion ? », 11 septembre 2026

**Verdict : GO AVEC CORRECTIONS.** La version écrite dans `moonshots-2026-09-11.md` ne doit pas partir cette nuit. Sa mesure principale est viciée par construction (faille 0), son seuil de 65 % est inférieur à une antériorité non LLM déjà préenregistrée, et la cible 2020 mêle un changement de mode et deux chocs d'événement.

## 1. Faisabilité [vérifié sur le web et dans le dépôt]
- **ChronoGPT existe.** Hugging Face `manelalab`. Auteurs : Songrun He, Linying Lv, Asaf Manela et Jimmy Wu (WUSTL). Articles : arXiv 2502.21206 pour la base, 2510.11677 pour l'Instruct. Licence MIT. **26 coupures annuelles, du 31/12/1999 au 31/12/2024**, et non 11 : les coupures antérieures à 2014 existent aussi. Trois familles : `chrono-gpt-v1-AAAAMMJJ`, `chrono-gpt-instruct-v1-AAAAMMJJ` et `chrono-bert-v1`.
- **Taille et format.** Environ 1,5 B de paramètres, contexte de 1 792 tokens. HellaSwag passe de 37 % (1999) à 48 % (2024), soit le niveau de GPT-2 XL. L'Instruct obtient 12,6 à 16,8 % de victoires sur AlpacaEval LC face à Qwen1.5-1.8B-Chat. Chaque dépôt contient un `pytorch_model.bin` de **7,43 Go** et du code maison (`ChronoGPT_inference.py`, `ChronoGPT_instruct.py`), avec le tokenizer tiktoken.
- **Pas de GGUF ni de MLX.** L'architecture modded-nanogpt n'est pas prise en charge par llama.cpp, donc la conversion n'est pas réaliste.
- **Mac.** `requirements.txt` épingle une nightly de torch en cu126. Le code a pourtant un repli SDPA et des conversions bfloat16 sans appel CUDA obligatoire. Le CPU et MPS sont donc plausibles, **mais non testés** : prévoir une heure de mise au point du chargeur.
- **Alternative PIT (Kelly, Malamud, Schwab, Xu, arXiv 2607.11889).** HF `Diamegs`, licence Apache 2.0. Deux familles, 4B et 1B, en base et en FT, avec une coupure mensuelle de 2013-12 à 2024-12. Un modèle 4B pèse **17,76 Go**. Elle est inutilisable ici : aucune coupure avant 2013-12, donc aucune fenêtre de dérive antérieure à 2014, et la provenance des données du FT n'est pas documentée.
- **Distributions exploitables.** Aucune évaluation publiée des sorties d'enquête ou de persona à 1,5 B. Dans R1, Qwen3-4B donnait déjà la même distribution à la gauche et à la droite sur environ un tiers des items. À 1,5 B, la génération libre sera pire : il faut lire les log-probabilités des options.
- **GSS local** (`data/gss-panel/`, structure mesurée dans `resultats/a12-delai-de-retest.md`) :
  - Panel 2010-2014 : vagues 2010, 2012 et 2014 **sur les mêmes personnes**. « 2014 » est donc la cohorte 2010 vieillie et érodée, pas une coupe 2014.
  - Panel 2016-2020 : cohortes 2016 (2 867) et 2018 (2 348), c'est-à-dire des coupes transversales en face à face, réinterrogées en 2020 surtout par le web et le téléphone.
  - Items appariés : 137 sur 149 pour 2010-2014, 146 sur 149 pour 2016-2020.
  - **Manquent** : aucune coupe 2014 ni 2012 locale. La tendance 2006-2014 ne peut se construire qu'à partir des vagues 1 des panels 2006, 2008 et 2010.

## 2. Failles
0. **Fatale : le signe d'un modèle seul.** Le « changement prédit » par le modèle 2014 ne peut être que (modèle − vrai 2014). Or la TV attendue dépasse 0,20 et R1 montre une surdispersion : le signe reflète le biais de niveau (retour vers le milieu), pas une prévision. **Correctif** : prendre une différence entre coupures, Δtexte = M2014 − M2010, où le biais de niveau s'annule.
a. **Taux de base.** Strimling, Vartanova et Eriksson (2022) :
   - tendance extrapolée : 60 % de signes justes sur 60 items GSS entre 2018 et 2021 ;
   - avantage argumentatif : 68 %, et 76 % hors événements.

   Filtrer les items qui ont bougé de plus de 8 points sélectionne les items à tendance, et « tout glisse à gauche » dépassera probablement 65 % dans les camps de gauche et du centre. Un seuil absolu n'a donc pas de sens : il faut battre le meilleur nul, en test apparié.
b. **Dépendance.**
   - Les 149 items mêlent des variables factuelles ou comportementales (`hunt1`, `vote16`, `dwelown16`, `compuse`, `wrkgovt`) à des batteries (une vingtaine d'items `nat*`, sept items `ab*`).
   - Les trois camps d'un même item sont corrélés.
   - L'effectif réel tient en quelques dizaines de familles : il faut un bootstrap par famille (`resultats/a8-familles-gss.csv`).
c. **L'extrapolation n'est pas une faille si l'on vise le bon énoncé.** Le modèle 2014 a lu les rapports GSS et Pew : « le discours précède » ne se distingue pas de « il a lu les sondages ». Seule la valeur **ajoutée à la tendance** est un résultat, d'où une mesure sur le résidu.
d. **Bruit.** À 1,5 B, la variance due à l'invite (paraphrase, ordre des options) peut dépasser un écart entre coupures proches, car chaque modèle est un entraînement continu du précédent. Il faut un plancher de bruit (Δ entre années adjacentes, 2013 → 2014) et une porte de validité en échantillon.
e. **Fuite.**
   - Les tests des auteurs sont factuels : présidents, 0 sur 78 après la coupure contre 77 sur 78 avant ; événements, 0 sur 76. Ils reconnaissent des dates de publication inexactes.
   - **Instruct** : les paires viennent de Tulu-3 et de self-instruct, rédigées par des modèles récents, et un classifieur GPT-4.1 ne garde que le contenu daté d'avant 2000. **Les normes et valeurs des assistants de 2023-2024 ne sont pas filtrées**, ce qui crée un biais « à gauche » exactement sur la quantité testée. Le modèle de base évite ce biais.
   - Critère (iii), « l'erreur décroît avec la coupure » : confondu avec la capacité (HellaSwag passe de 37 à 48 %) et avec la lecture des GSS 2016 et 2018 par les modèles postérieurs. Il est trivial, à retirer ou à contrôler par une cible fixe antérieure.
f. **Mode et période.** 2020 = web contre face à face en 2014 (ampleurs de mode dans `data/norc-mode/`), plus le COVID et George Floyd. Strimling et al. excluent 14 items sur 60 pour cause d'événement. Cible principale : 2018, en face à face.
g. **Composition des camps.** Le tri idéologique entre 2014 et 2018 déplace qui se dit libéral ou conservateur : il faut rapporter aussi l'écart entre camps.

## 3. Antériorité
- **La plus proche sur la mesure : Strimling, Vartanova et Eriksson, *R. Soc. Open Sci.* 9:211068 (2022), préenregistrée.** Direction des changements GSS 2018 → 2021 : 68 % contre 60 % pour la tendance. Ce n'est pas un LLM. Les scores publics (github irinavrt/predict-gss-2020, 94 items) **servent de comparateur**.
- Kozlowski, Kwon et Evans, 2407.11190 : GPT-3 (données jusqu'en 2019) reproduit 84 % des écarts partisans sur le COVID. Un seul événement, un écart et non un changement, une coupure non stricte.
- Autres travaux :
  - Ozkan, 2607.18310 : trois items entre 2016 et 2022, avec des modèles de 2026.
  - Jiang et al., 2305.09620 : rétrodiction GSS, sans coupure stricte.
  - Modèles et biais de coupure, sans opinion : He et al. (finance), Kelly et al., DatedGPT (2603.11838, 1,3 B, coupures annuelles 2013-2024), TimeMachineGPT (2404.18543), Sarkar et Vafa (biais d'anticipation).
- **Aucun travail trouvé** n'oppose un modèle à coupure stricte à la tendance sur un changement d'opinion postérieur. La niche reste neuve, mais le repère à battre est de 68 %, pas de 65 %.
- **Probabilité d'un résultat « choc »** (Δtexte bat la tendance et l'avantage argumentatif hors échantillon, IC propre) : **environ 5 %**. Trois raisons : un modèle du niveau de GPT-2 XL, l'indifférence au camp déjà observée à 4 B, et des Δ entre points de sauvegarde voisins minuscules face au bruit. Un nul propre, publiable comme note de méthode (« les modèles à coupure stricte de 1,5 B ne portent pas de signal d'opinion »), est probable.

## Corrections exactes
1. Modèle de base et log-probabilités des options, pas de génération Instruct.
2. Prédicteur = Δtexte entre coupures ; ne jamais comparer le modèle au vrai.
3. Cible principale : le changement 2014 → 2018, tout en face à face ; 2020 seulement en secondaire, avec le mode signalé.
4. Coupes transversales pour 2010 et 2014 : télécharger le fichier cumulatif GSS (des données, pas un modèle ; taille à vérifier par HEAD) plutôt que la cohorte 2010 vieillie.
5. Items : les items attitudinaux orientés de `a37` (79), présents en 2010, 2014 et 2018. Exclure les items factuels. **Préenregistrer avant tout calcul du modèle** le sous-ensemble « surprise », où signe(Δ 2014→2018) ≠ signe(Δ 2010→2014) dans au moins un camp.
6. Comparateurs : persistance, tendance 2010-2014 et 2006-2014, glissement à gauche, avantage argumentatif (items moraux), Qwen3-4B en plafond contaminé.
7. Mesure primaire : la pente partielle de Δtexte dans Δobs(2014→2018) ~ Δtendance + Δtexte, par camp et sur l'écart entre camps, avec bootstrap par famille. Signes en secondaire, rapportés au meilleur nul.
8. Deux portes, avec arrêt et nul rapporté si l'une échoue :
   - validité contemporaine : corr(Δtexte 2010-2014, Δobs 2010-2014), IC strictement positif ;
   - Δtexte supérieur au plancher de bruit (paraphrases et années adjacentes).

## Conception corrigée à lancer cette nuit
- **Modèles** : `manelalab/chrono-gpt-v1-20101231`, `-20121231`, `-20141231`, et `-20131231` pour le plancher de bruit. 4 × 7,43 Go = **29,7 Go**. Pas d'Instruct ni de PIT cette nuit.
- **Données** : coupes GSS 2006, 2010, 2014 et 2018 (fichier cumulatif). Repli local si le téléchargement échoue : vague 1 des panels 2006 et 2010, cohortes 2016 et 2018 du panel 2016-2020, avec la cible Δ 2010 → 2018 annoncée comme chevauchant la coupure.
- **Invite** : « Among Americans who call themselves {liberal|moderate|conservative}, the most common answer to "…" is », puis log-probabilités normalisées sur les options. 3 paraphrases × 2 ordres × 3 camps × environ 70 items × 4 modèles ≈ 5 000 passes.
- **Prédiction chiffrée** : porte de validité r ≈ 0,1 avec un IC contenant 0 (arrêt probable) ; pente de Δtexte non significative (probabilité 0,8) ; signes de Δtexte de 50 à 58 % ; glissement à gauche de 60 à 75 % ; tendance autour de 60 %.
- **Durée** : 30 à 60 min de téléchargement, 1 h de chargeur MPS ou CPU, 30 à 90 min de calcul. **Trois à quatre heures au total.**
