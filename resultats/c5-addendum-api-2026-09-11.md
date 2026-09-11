# C5, addendum API : quatre familles distantes, avant tout appel de generation de l'etude

Ecrit AVANT tout appel de generation de l'etude API (les 5 appels de calibrage par
modele, mesure de jetons et de cout, precedent ce fichier). Protocole identique a
`resultats/c5-preenregistrement.md` : memes 22 formes, meme grammaire, meme parse
(`c5_formulation.parser`, importe), meme temperature 0 (`MoteurR1.decrire`).

- **Modeles** (raisonnement desactive) : `openai/gpt-4o-mini`,
  `google/gemini-2.5-flash-lite`, `anthropic/claude-3-haiku`,
  `meta-llama/llama-3.3-70b-instruct`.
- **Personas** : les memes 300 que le run local, meme graine `20260911`
  (`c5_formulation.charger_personas`, 100 par camp).
- **Predictions** (section 5, identiques par modele) : MAE ne bat pas 4,3 (65 %) ;
  >= 3 fausses alertes sur 5 (55 %) ; welfare bon signe et > 20 points (95 %) ;
  big cities bon signe dans au plus la moitie des cellules modele x camp.
- **Cout** : plafond dur partage 2,00 USD sur les 4 modeles (`usage.cost`), estime
  1,46 USD sur calibrage. Arret a `data/traces/c5-api/STOP`.
- **Analyse** : `c5_analyse.py --dossier data/traces/c5-api` par modele ; resume =
  nombre de modeles (sur 6 : 2 locaux + 4 API) avec >= 3 fausses alertes sur 5.
