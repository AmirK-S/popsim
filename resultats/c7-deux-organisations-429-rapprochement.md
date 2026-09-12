# Rapprochement du HTTP 429 — témoin « deux organisations » (C7)

Identifiant de génération concerné : `gen-1789204242-106eGmOMkqNrG7o5RQKQ`, reçu sur
l'appel C de la personne d'index 82 (83ᵉ personne), cf.
`resultats/c7-deux-organisations-resultats.md` section 3.

`analyses/c7_deux_organisations.py` est un script autonome qui n'implémente pas le
protocole de rapprochement 429 lui-même (il se contente d'arrêter proprement sur
`Arret429`). Le protocole appliqué ici est celui documenté dans
`analyses/r6_oracle_distant.py` (`etablir_ancre_429`, `rapprocher_429`,
`PREUVE_NON_FACTURE_429`, `DELAI_ANCRE_429`, `DELAI_AVANT_SONDE_429`, `DELAI_SONDE_429`,
`TOLERANCE_429_PLANCHER`), rejoué manuellement en dehors de la machinerie de registre
propre à R6 (sans objet ici : aucun autre appel n'a eu lieu pendant le rapprochement, donc
le terme de correction « coûts réglés depuis l'ancre » est nul par construction).

## 1. Ancre de crédits

Deux lectures `GET /credits` à 60 s d'écart (première tentative, stable) :

- `total_usage` identique aux deux lectures : **158.994768796 USD**
- Ancre retenue : `total_usage_ancre = 158.994768796`, `total_credits_ancre = 165`

## 2. Les deux sondes en lecture seule

Attente de 120 s après l'ancre avant la sonde 1 (délai de règlement retardé côté
OpenRouter, 15–40 s observés), puis 540 s entre la sonde 1 et la sonde 2.

| sonde | horodatage | `/generation` | `/generation/content` | `total_usage` (`/credits`) |
|---|---|---|---|---|
| 1 | 2026-09-12T11:19:51+02:00 | **404** | **404** | 158.994768796 |
| 2 | 2026-09-12T11:28:52+02:00 | **404** | **404** | 158.994768796 |

## 3. Critère (protocole R6, point B)

- 404 sur `/generation` et `/generation/content` aux deux sondes : **oui**
- `total_usage` stable entre les deux sondes : **oui** (158.994768796 = 158.994768796)
- Écart entre `total_usage` à la sonde 2 et l'ancre (corrigée de la variation des coûts
  réglés depuis l'ancre, ici nulle : aucun autre appel effectué) : **0,0 USD**
- Tolérance appliquée : `TOLERANCE_429_PLANCHER` = 1e-6 USD (le plancher du protocole
  domine ici : 10 % du plus petit coût réglé observé pour `qwen/qwen-2.5-72b-instruct`
  dans la trace C7, de l'ordre de 1e-4–1e-5 USD, est déjà inférieur au plancher, donc le
  `min(...)` du protocole retombe sur 1e-6 USD)
- Écart (0,0 USD) ≤ tolérance (1e-6 USD) : **critère rempli**

## 4. Conclusion

**Non facturé.** La génération `gen-1789204242-106eGmOMkqNrG7o5RQKQ` n'existe pas côté
OpenRouter (404 aux deux points de lecture, aux deux sondes) et le solde de crédits est
resté rigoureusement stable pendant toute la fenêtre de rapprochement (~11 minutes,
ancre + 120 s + 540 s). Aucune correction de coût n'est nécessaire.

## 5. Coût final imputable à l'expérience

Le coût cumulé de 165 appels réussis déjà comptabilisé dans
`resultats/c7-deux-organisations-resultats.md` (**0,3201277207 USD**) reste exact et
définitif pour cette portion du run : l'appel C ayant échoué en 429 n'a jamais été
facturé, donc rien à ajouter ni à soustraire. C'est ce montant qui sert de point de
départ (rechargé automatiquement depuis la trace par `analyses/c7_deux_organisations.py`)
pour la reprise éventuelle vers n = 200 (tâche 2).

---

# Rapprochement du second HTTP 429 — témoin « deux organisations » (C7)

Identifiant de génération concerné : `gen-1789208932-mmZwLPG7qA5W84m7dS7t`, reçu sur
l'appel C de la personne d'index 142 (après que son appel B a réussi), pendant la reprise
qui a suivi le rapprochement du premier 429 ci-dessus, cf.
`resultats/c7-deux-organisations-resultats.md` section 3. Le script s'est arrêté
immédiatement, sans relance, exactement comme pour le premier 429 ; ce second identifiant
était resté hors périmètre de l'agent précédent et est rapproché ici, à froid, en
lecture seule, sans relancer aucun appel.

Même protocole que ci-dessus, rejoué manuellement en dehors de la machinerie de registre
propre à R6 : aucun autre appel n'a eu lieu entre l'ancrage et la seconde sonde (aucune
génération payante n'a été lancée pendant tout le rapprochement), donc le terme de
correction « coûts réglés depuis l'ancre » est nul par construction, comme pour le
premier identifiant.

## 1. Ancre de crédits

Deux lectures `GET /credits` à 60 s d'écart (première tentative, stable) :

- `total_usage` identique aux deux lectures : **159.228830862 USD**
  (`lecture 1` 2026-09-12T12:33:11+02:00, `lecture 2` 2026-09-12T12:34:11+02:00)
- Ancre retenue : `total_usage_ancre = 159.228830862`, `total_credits_ancre = 165`

## 2. Les deux sondes en lecture seule

Attente de 120 s après l'ancre avant la sonde 1, puis 540 s entre la sonde 1 et la
sonde 2, comme prescrit par `DELAI_AVANT_SONDE_429` et `DELAI_SONDE_429`.

| sonde | horodatage | `/generation` | `/generation/content` | `total_usage` (`/credits`) |
|---|---|---|---|---|
| 1 | 2026-09-12T12:36:14+02:00 | **404** | **404** | 159.228830862 |
| 2 | 2026-09-12T12:45:18+02:00 | **404** | **404** | 159.228830862 |

## 3. Critère (protocole R6, point B)

- 404 sur `/generation` et `/generation/content` aux deux sondes : **oui**
- `total_usage` stable entre les deux sondes : **oui** (159.228830862 = 159.228830862)
- Écart entre `total_usage` à la sonde 2 et l'ancre (corrigée de la variation des coûts
  réglés depuis l'ancre, ici nulle : aucun autre appel effectué pendant la fenêtre de
  rapprochement) : **0,0 USD** (159.228830862 − 159.228830862)
- Tolérance appliquée : `TOLERANCE_429_PLANCHER` = 1e-6 USD (même raisonnement que pour
  le premier identifiant : le plancher du protocole domine, 10 % du plus petit coût réglé
  observé pour les modèles de la trace C7 étant déjà inférieur à 1e-6 USD)
- Écart (0,0 USD) ≤ tolérance (1e-6 USD) : **critère rempli**

## 4. Conclusion

**Non facturé.** La génération `gen-1789208932-mmZwLPG7qA5W84m7dS7t` n'existe pas côté
OpenRouter (404 aux deux points de lecture, aux deux sondes) et le solde de crédits est
resté rigoureusement stable pendant toute la fenêtre de rapprochement (ancre à
12:33–12:34, sonde 1 à 12:36, sonde 2 à 12:45, ~12 minutes), avec la même valeur de
`total_usage` aux trois lectures (ancre, sonde 1, sonde 2) : 159.228830862 USD. Aucune
correction de coût n'est nécessaire.

## 5. Coût final imputable à l'expérience

Le second appel C en 429 n'a jamais été facturé : rien à ajouter au chiffre déjà établi
dans `resultats/c7-deux-organisations-resultats.md` pour les 285 appels réussis
(143 B + 142 C), **0,5541898180 USD**. Ce montant reste le coût total réellement
imputable à l'expérience « deux organisations » à ce stade (n = 142/200), sous le
plafond strict de 1,00 USD de la mission. Les deux 429 rencontrés pendant cette
expérience (premier et second identifiant) sont désormais tous deux rapprochés et
prouvés non facturés ; plus aucune incertitude de coût n'est ouverte sur ce run. Une
éventuelle reprise vers n = 200 peut repartir de ce montant sans aucune correction.
