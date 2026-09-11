# C7-gen, preenregistrement : la fuite de C7 survit-elle a NOS propres jumeaux ?
**Ecrit le 12 septembre 2026, avant tout appel de la campagne des 1 400 appels.** Etude
de vie privee sur Twin-2K-500 (deja public). Aucun pid imprime ni ecrit dans resultats/.
**Transparence de sequence** : avant ce texte, 10 appels de calibrage (llama31-8b, R1,
format seul, parse 100 %) et 12 appels de compatibilite (3 personnes x 4 combinaisons),
cout 0,0084 USD. `openai/gpt-5-nano` rejette le raisonnement desactive (HTTP 400,
"Reasoning is mandatory") et est remplace par `deepseek/deepseek-v4-flash` avant lecture
d'aucune reponse substantielle : aucune hypothese n'a ete ajustee sur du contenu. Repris
(jamais rejoues) dans la campagne par la reprise de trace.
## Conception
200 personnes (graine 20260912) parmi les 294 dont le profil texte vagues 1-3 existe
localement (`wave_persona_chunk_001.parquet`). Items : les 60 items categoriels de C7
(`c7_reidentification.items_communs`, repris tel quel). R1 = profil riche Twin, **tronque
a 8000 caracteres** (risque assume : coupe parfois une question en cours de bloc). R2 =
bloc Demographics seul. Trois modeles bon marche, familles distinctes, raisonnement
desactive, temp. 0 : `meta-llama/llama-3.1-8b-instruct`, `qwen/qwen3.7-flash`,
`deepseek/deepseek-v4-flash`. Plus R1 x temp. 1 x `qwen3.7-flash`. Un appel/personne, 60
reponses d'un coup, format `N) k` strict. Total : 200 x (3x2 + 1) = 1 400 appels.
## Mesures et comparateurs
Top-1/top-10 de reidentification parmi 2 058 humains vague 4 (Hamming sur 60 items,
`rangs_attaque` repris tel quel), exactitude brute. Comparateurs : hasard (1/2058), R2,
et les jumeaux GPT4.1/Gemini de l'autre equipe (`resultats/c7-resultats.md`).
## Predictions chiffrees
1. R1 : top-1 >= 10 % sur au moins 2 modeles sur 3.  2. R2 reste sous 3 % partout.
3. Temp. 1 reduit le top-1 (meme modele/recette) d'au moins un tiers vs temp. 0.
## Controle de contamination
Twin-2K-500 public depuis le 23 mai 2025 (arXiv 2505.17479). `llama-3.1-8b-instruct` :
coupure decembre 2023 (fiche Meta), **avant** cette date, temoin negatif. `qwen3.7-flash`
et `deepseek-v4-flash` (doc. technique publiee 2026-04-27) : coupures posterieures a mai
2025 (dates exactes non publiees, deduites de la date de sortie). Prediction : si la
fuite vient du profil et non de la memorisation, le modele ancien fuit AUTANT (+/- un
tiers) que les deux recents. Sonde (~50 appels, meme plafond) : completion VERBATIM d'un
extrait tronque d'un vrai profil vs un questionnaire fictif de meme forme ; taux de
completion verbatim (>= 20 caracteres consecutifs) par modele et condition. La date de
generation des jumeaux GPT4.1/Gemini de l'autre equipe n'est pas etablie ici ; seule la
date de publication du jeu (23 mai 2025) est sourcee.
## Ce que ce plan ne dira pas
Rien sur des modeles chers/proprietaires ; un seul jeu, une seule metrique de similarite,
une seule troncature de profil.
Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
