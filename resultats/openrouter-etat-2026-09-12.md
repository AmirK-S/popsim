# État réel de la clé OpenRouter — 12 septembre 2026

Constaté, pas supposé : trois requêtes réelles contre l'API OpenRouter, exécutées le
12 septembre 2026 par un script jetable hors dépôt (aucun fichier du projet modifié,
aucun cache écrit dans `data/traces/`). La clé n'a été ni imprimée ni copiée ; seule sa
valeur masquée telle que rendue par l'API elle-même (`sk-or-v1-778...669`) apparaît ici.

## 1. Comment le projet lit la clé

`analyses/r6_oracle_distant.py::cle_api()` lit la ligne `OPENROUTER_API_KEY=` de `.env`
à la racine, ne l'imprime jamais, et la porte uniquement dans l'en-tête
`Authorization: Bearer …` construit par `entetes()`. `.env` existe (`-rw-------`, non
suivi par git). C'est cette même lecture que le script de vérification a reproduite,
sans passer par le CLI du projet pour éviter d'écrire dans `data/traces/` (catalogue,
registre) pendant que d'autres agents travaillent sur le dépôt.

Rappel de contexte : la clé portait auparavant une **limite de dépense au niveau de la
clé**, indépendante du solde du compte (HTTP 403 « Key limit exceeded (total limit) »).
Recharger le compte ne lève pas cette limite ; seul `GET /api/v1/key` le dit, et seul un
appel réel qui passe le dit avec certitude.

## 2. Les trois requêtes

**`GET /api/v1/credits` → HTTP 200**
```
total_credits: 165
total_usage:   158.644804176
```
Solde disponible ≈ **6.355195824 USD**.

**`GET /api/v1/key` → HTTP 200**
```
limit:           null
limit_reset:     null
limit_remaining: null
disabled:            false (absent, donc pas true)
is_management_key:   false
usage (mensuel):     9.421318131
```
Point décisif : `limit` est **null**, pas seulement élevée. La limite de dépense au
niveau de la clé qui produisait le 403 n'existe plus — c'est exactement l'observable qui
distingue « limite levée » de « compte rechargé », et il est constaté ici, pas déduit du
solde.

**`POST /api/v1/chat/completions` → HTTP 200** (l'appel réel, le seul qui prouve)
Modèle `deepseek/deepseek-v4-flash` (déjà désigné `MODELE_PILOTE` par le projet),
fournisseur imposé `DigitalOcean`, `temperature 0`, `max_tokens 3`, raisonnement
explicitement désactivé (`{"enabled": false, "exclude": true}`), une poignée de jetons
d'entrée.
```
finish_reason:      stop
prompt_tokens:       10
completion_tokens:    3
cost (usage.cost):    0.000001183 USD   (1.183e-6 USD, exact, annoncé par OpenRouter)
```
Aucun 403. Aucun incident de transport.

## 3. Conclusion

**La clé est utilisable.** La preuve n'est pas le solde (165 crédits, 158.64 utilisés) ni
la seule lecture de `/key` : c'est l'appel de complétion réel, qui est passé en HTTP 200
pour un coût exact de 0.000001183 USD, combiné à `limit: null` sur `/key`, qui confirme
que la limite de dépense propre à la clé a bien été supprimée (et pas seulement que le
compte a été rechargé).

**Budget restant.** Solde de compte disponible ≈ 6.36 USD. Le plafond interne du projet
pour la campagne R6 reste `LIMITE_CLE_R6 = 4.40 USD` (politique du dépôt, indépendante
d'OpenRouter) et la réserve de compte que le registre retient par prudence est de 1.50 USD
(`composantes_budget`) — soit un reste géré par le registre d'environ 4.86 USD après cette
réserve, borné de toute façon par le plafond de campagne à 4.40 USD. Rien dans cette
vérification ne consomme ce budget de façon significative : le seul appel réel a coûté
0.000001183 USD.
