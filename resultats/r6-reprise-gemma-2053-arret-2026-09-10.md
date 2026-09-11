# R6 — reprise Gemma de 20:53, arrêt sur 429

La reprise a utilisé la même trace, la même liste et les mêmes invites, avec `google/gemma-4-31b-it:free`, Google AI Studio imposé et aucun repli. Le marqueur Super et son incertitude sont restés intacts.

Résultat : une réponse valide unique, aucun rejet de parse, raisonnement compté à zéro et coût annoncé nul. La cellule suivante a épuisé la borne du plan avec quatre HTTP 429 et a été classée non jouée. Le client a engagé automatiquement la cellule suivante; `STOP` a été posé pendant son backoff après trois 429, empêchant une quatrième tentative et toute poursuite. Total de session : une cellule acquise, une non jouée, huit incidents 429. L’essai est non propre.

La génération réussie est attribuée à Google AI Studio et ses métadonnées donnent coût total, usage et coût amont égaux à 0 USD. Les huit identifiants d’erreur sont conservés en privé; `/generation` répond 404 pour chacun. Après arrêt, la clé reste à usage 0 USD, plafond et restant 4,40 USD, reset nul; le compte reste à 5,778548955 USD, au-dessus de la réserve de 1,50 USD.

La condition de passage du gratuit n’est pas satisfaite. Le GO a été retiré et `STOP` reste présent. Aucun essai DeepSeek, aucune campagne et aucun modèle fermé n’ont été lancés.
