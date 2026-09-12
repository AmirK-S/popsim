# C7-fort, préenregistrement : la fuite revient-elle avec un modèle fort, appel par item ?
Écrit AVANT tout appel payant (aucun calibrage encore fait).
**Hypothèse** : modèle fort + granularité Twin (un appel/item) font monter la fidélité et
revenir la fuite, contrairement à nos jumeaux bon marché (0-0,83 %, `c7-gen-resultats.md`)
et au test de granularité à modèle faible (`c7-recette-resultats.md`, n=10, non conclu).
**Modèle/recette** : `openai/gpt-4.1` (classe Twin), raisonnement off, température 0
(celle de R1 dans `c7_gen.py`). Tarif via `GET /models` (gratuit, 12/09) : 2,0/8,0 USD
par M jetons prompt/completion, contre 0,4/1,6 pour gpt-4.1-mini (x5). Recette **reprise
sans modification** de `c7_recette.construire_prompt_item`/`parser_item`/`SYSTEME_ITEM`
(persona texte R1, 1 appel/item), mêmes 60 items/personnes que C7 (graine 20260912).
**Taille** : coût réel mesuré (item, gpt-4.1-mini) 0,000525 USD/appel ; estimation x5 pour
gpt-4.1 : ~0,0026 USD/appel, ~0,158 USD/personne. Cible **30 personnes** (~4,7 USD),
minimum garanti **25**, ajustée à la baisse si le calibrage réel (5 appels) dépasse
l'estimation, jamais sous 25. Si 25 ne tient pas sous 5 USD, repli annoncé sur le
meilleur modèle qui le permet.
**Mesures obligatoires + fuite** : exactitude (`c7_gen_analyse.exactitude_propre`) ;
fidélité = chute sous permutation intra-segment (S_gra) normalisée au plancher humain
(`t1_mesures.chute`+`t1_commun`, convention `c7-compromis.csv`, non modifiés) ; fuite
top-1/top-10 via `c7_reidentification.rangs_attaque` (non modifié), IC 95 % bootstrap
personnes (2000 tirages), pool des 2 058 humains.
**Prédictions chiffrées** : 1. exactitude > 0,55. 2. fidélité (part du plancher humain)
> 0,10. 3. top-1 > 5 %, bien au-dessus de nos 0,83 % actuels.
**Limite de puissance** : 25 à 40 cibles, hasard = 0,049 % → IC bootstrap du top-1 large
(probablement plusieurs points de %) ; un résultat non significatif n'écarterait pas
l'hypothèse.
**Comparateurs/éthique** : Twin JSON Persona GPT-4.1 = exactitude 0,574, fidélité 0,708,
top-1 20,68 % (`c7-compromis.csv`) ; nos jumeaux faibles 0-0,83 %. Aucun identifiant ni
appariement individuel : seuls des taux agrégés sortent dans `resultats/`.
