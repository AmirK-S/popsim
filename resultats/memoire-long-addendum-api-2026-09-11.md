# Mémoire long : addendum API (2026-09-11, avant tout appel de génération)

Étend `resultats/memoire-long-preenregistrement.md` à 4 modèles OpenRouter de familles distinctes, mêmes personnes/items/graine que le run local (gpt-oss-20b).

**Modèles** (raisonnement désactivé, `reasoning:{enabled:false,exclude:true}`) : `openai/gpt-4.1-nano` (OpenAI), `mistralai/mistral-nemo` (Mistral), `meta-llama/llama-3.1-8b-instruct` (Meta), `amazon/nova-micro-v1` (Amazon). Substitués à gpt-4.1-mini/Gemini Flash/Claude Haiku : mesurés 3 à 30x plus chers à ce volume d'appels (voir coût ci-dessous) ; pas d'étude C5-API antérieure à reprendre (`resultats/c5-addendum-api-2026-09-11.md` absent).

**Échantillon** : reproduction exacte du tirage complet par défaut du run local (mêmes ~133 personnes/panel, graine 20260911, même séquence numpy), puis sous-ensemble déterministe des 40 premières personnes par panel (triées par identifiant de ligne, aucun tirage supplémentaire) = 120 personnes, strict sous-ensemble des personnes du run local. 20 items cibles identiques (mêmes métadonnées, `choisir_items`). 2 horizons (+2, +4 ans) : 9 600 cellules/modèle, 38 400 au total.

**Coût** : mesuré sur 5 appels réels par candidat (profil ≈2 900-3 400 jetons). Coût/cellule moyen mesuré : gpt-4.1-nano ≈0,00009 $ (cache automatique OpenAI actif dès le 2e appel/personne), mistral-nemo ≈0,00006 $, llama-3.1-8b ≈0,00006-0,0001 $, nova-micro ≈0,00012 $. À 200 personnes (plancher demandé), le total estimé dépassait déjà 2,50 $ ; réduit à 120 personnes pour un total estimé ≈1,8 $, marge sous le **plafond dur de 2,00 USD** de l'étude entière (arrêt dur programmé dans `analyses/memoire_long_api.py`, partagé entre les 4 processus, + fichier STOP).

**Prédictions** (identiques au préenregistrement, par modèle et horizon) : P1 persistance > IA, écart plus petit à +4 ans ; P2 IA ne bat pas le mode du segment sur les cellules changées ; P3 AUC(désaccord→changement) < 0,62. Résumé prévu : combien des 5 modèles (gpt-oss-20b local + 4 API) confirment P1 aux deux horizons.

Traces : `data/traces/memoire-long-api/ml-<clé>.jsonl` (une par modèle), reprise par index, fournisseur noté par ligne.
