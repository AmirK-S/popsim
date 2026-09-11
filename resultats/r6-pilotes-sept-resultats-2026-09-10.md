# R6 — résultat des sept pilotes autorisés

Autorisation: pilotes uniquement, fondés sur la registration OSF `6yj8x` et le manifeste READY de SHA-256 `dc7482c982df7fc80f1fd8298d1421cbe75ac0053dd5a211c2cf43c0b61028fc`. Aucune campagne n'a été lancée. DeepSeek est resté en vérification locale et n'a reçu aucun nouvel appel.

Les sept pilotes ont produit 123 POST au total: 20 pour chacun des modèles sauf Kimi, arrêté après 3 réponses. Le coût attribuable à ces sept pilotes est **0,03390455 USD**, sous le plafond agrégé absolu de 0,18 USD. Le total du ledger R6, pilote DeepSeek antérieur inclus, est **0,0342335066 USD**. Toutes les réservations sont réconciliées ou annulées; il n'en reste aucune ambiguë.

| Modèle | Fournisseur fixé | Résultat | Réponses | Coût USD | Rejets | Raisonnement moyen/max | Exactes sur 10 |
|---|---|---|---:|---:|---:|---:|---:|
| Mistral Small 2603 | Mistral | passe | 20 | 0,00059544 | 0 | 0 / 0 | 9 |
| Qwen 3.7 Plus | Alibaba | passe | 20 | 0,00192640 | 0 | 0 / 0 | 8 |
| Kimi K2.5 | SiliconFlow | **retiré** | 3 | 0,02253195 | 0 | 3 285 / 3 835 | n.d. |
| GLM-5 | StreamLake | passe | 20 | 0,00287376 | 0 | 0 / 0 | 9 |
| Gemini 3.8 Flash | Google AI Studio | **retiré** | 0 sur 20 tentatives | 0 | n.d. | n.d. | n.d. |
| Claude Haiku 4.5 | Anthropic | passe | 20 | 0 | 0 | 0 / 0 | 10 |
| Grok 4.3 | xAI | passe, **non déterministe** | 20 | 0,00597700 | 0 | 0 / 0 | 4 |

Kimi a renvoyé trois réponses réglées, chacune au-dessus de la réservation unitaire de 0,001 USD, avec des milliers de jetons de raisonnement malgré `reasoning=off`. Après la troisième réponse, le cumul réglé atteignait 0,02253195 USD; le préflight a refusé la quatrième cellule avant réservation et avant POST. Le dépassement réel du plafond pilote de 0,02 USD est conservé sans le tronquer. Le modèle est retiré et n'aura pas de campagne.

Gemini a reçu exactement deux séries de dix tentatives. Le fournisseur fixé a renvoyé HTTP 404 à chaque fois. Aucune réponse n'a été acquise, aucune somme n'a été facturée dans le ledger et toutes les réservations ont été annulées avec preuve HTTP. Aucun fallback ou rejeu n'a été utilisé. Le modèle est retiré.

Grok a quatre distributions strictement identiques sur dix entre les deux passes, sous le seuil de sept. Conformément au plan, il est marqué non déterministe et A4 ne pourrait être interprété qu'avec le plancher machine. Cette conséquence n'autorise aucune campagne dans le présent GO.

Les GO one-shot réussis et les GO des deux retraits sont archivés dans `data/traces/reprise`. `STOP-R6` a été recréé immédiatement après le dernier pilote. Le STOP global n'a pas été modifié.
