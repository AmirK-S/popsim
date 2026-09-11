# C7-recette, resultats : la granularite de l'appel n'explique pas la fuite
Preenregistre dans `c7-recette-preenregistrement.md`, calcule par `c7_recette.py`.
Modele unique `openai/gpt-4.1-mini`, memes 40 personnes/60 items que l'attaque C7
(graine 20260912), profil R1 (8000 car.). Aucun pid ecrit, taux agreges seulement.
## Deviation majeure, non prevue : plafond de la CLE, pas du script
Le script n'a jamais approche notre plafond de 1,00 USD (cumul reel : **0,4428 USD**).
La cle OpenRouter a renvoye HTTP 403 « Key limit exceeded (total limit) » a 0,4392 USD
sur CE run : plafond CUMULE avec `c7_gen` d'hier soir (0,5055 USD), ~0,95 USD au total
sur la cle, pas par script. L'« appel unique » (40/40) a fini avant le mur ; l'« appel
par item » s'est arrete a 9 personnes completes + 1 partielle (14/60) sur 40 prevues,
les 30 suivantes a 0/60 (aucun cout facture).
## Resultats
| configuration | n | top-1 | IC 95 % | top-10 | rang median / 2058 |
|---|---|---|---|---|---|
| Appel unique (60 items, 1 appel/pers.) | 40 | 0,00 % | [0 ; 0] | 7,50 % | 852,9 |
| Appel par item (1 appel/question) | 10 (9 complets) | 0,00 % | [0 ; 0] | 0,00 % | 834,8 |
| Demographics Only (repere, n=40) | 40 | 5,88 % | [0 ; 13,37] | 14,62 % | 243,4 |
Reperes : hasard = 0,0486 % ; JSON Persona GPT4.1 (Twin) = 20,68 %.
## Verdict sur la prediction preenregistree
**Rejetee.** Predit : item >= 5x unique en top-1. Les deux sont a 0,00 % (facteur non
calculable sur un plancher nul) et le top-10 va dans le sens INVERSE (0 % vs 7,5 %). Sur
n=10, la puissance est faible, mais rien ne va dans le sens de la prediction.
## Conclusion pour l'article
A modele egal (GPT4.1-mini, classe Twin) et memes personnes/items, ni l'appel unique ni
l'appel par item (prompt proche du leur) ne reproduisent leur fuite (20,7 %) : la
granularite seule n'est PAS la cause. Avec `c7-gen-resultats.md`, la fuite tient a
quelque chose de plus specifique au pipeline Twin (format de persona exact, ou GPT4.1
complet plutot que mini) qu'un simple choix d'appel unique vs par item. A documenter
comme limite, pas comme cause identifiee.
**En clair** : demander a un modele bon marche de repondre question par question, comme
le fait l'equipe Twin, ne fait pas plus « fuiter » nos jumeaux qu'un seul gros appel --
ce n'est pas cette recette-la qui explique leur resultat.
Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
