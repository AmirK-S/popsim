# R6 — arrêt du smoke test Gemma après 429

Gemma était une alternative gratuite déjà inscrite au plan figé. Elle a été choisie avec Google AI Studio imposé et sans repli après les deux incidents 502 de Nvidia Super. Ce choix ne réconcilie, ne supprime et ne contourne aucun marqueur Super; son historique incertain reste conservé.

Une seule cellule était autorisée avant extension à dix. La première cellule n’a produit aucune réponse: trois tentatives de transport ont reçu HTTP 429. Le processus a été interrompu pendant l’attente précédant la quatrième tentative afin d’éviter une boucle. La trace principale contient zéro ligne, donc aucune cellule acquise ne pourra être rejouée par erreur. Le marqueur Gemma reste présent.

L’instrumentation a conservé trois `X-Generation-Id` privés. Les trois lectures de métadonnées ont répondu 404. Le GET de clé après l’arrêt indique usage 0 USD, plafond et restant 4,40 USD, reset nul. Le compte reste à 5,778548955 USD, au-dessus de la réserve de 1,50 USD. Le coût attribuable à cette clé est 0 USD; le coût individuel des tentatives n’est pas disponible.

La condition « première cellule valide » n’est pas satisfaite. Les neuf cellules Gemma restantes, les deux essais DeepSeek et les campagnes n’ont pas été lancés. Le GO actif a été retiré.
Diagnostic public : OpenRouter documente des limites et une disponibilité variables pour les variantes `:free`; un 429 indique une limitation de débit, mais les données disponibles ne permettent pas d’attribuer plus précisément celle observée ici. Aucun changement de compte, de clé, de plafond, de fournisseur ou de protocole n’est tenté.

## Reprise différée préparée

Aucune génération ne doit être retentée avant **20:47 CEST le 10 septembre 2026**. Le heartbeat parent annoncé à 20:53 est postérieur à cette borne. Les en-têtes conservés des trois 429 contiennent seulement les identifiants de génération; aucun `Retry-After` ou quota n’est disponible. Les GET publics et de clé n’apportent aucun en-tête de quota. Le champ `rate_limit` du corps de `/key` vaut `requests: -1`, `interval: 10s` et se déclare obsolète. Il n’existe donc pas de preuve d’un quota journalier atteint ni de motif pour reporter au jour suivant.

Le marqueur Gemma est archivé à l’identique dans `data/traces/reprise/` après rapprochement: zéro réponse, zéro ligne de trace, usage de la même clé inchangé à 0 USD. Le marqueur Super reste intact. La reprise utilisera la même trace, la même liste, le même modèle, Google AI Studio sans repli et les mêmes paramètres; aucune cellule acquise n’existe dans cette trace.

Commande exacte, à exécuter seulement après les contrôles frais inscrits dans le manifeste de reprise et après 20:47 CEST :

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python analyses/r6_oracle_distant.py \
  --modele google/gemma-4-31b-it:free \
  --plan f1 \
  --liste data/traces/r6-essai-cellules.txt \
  --essai 10 \
  --plafond 0.001 \
  --raisonnement off \
  --pause 3.5 \
  --suffixe r6v2-postosf-smoke-gemma \
  --fournisseur "Google AI Studio" \
  --manifeste-import data/traces/reprise/r6-v2-import-manifeste.json
```
