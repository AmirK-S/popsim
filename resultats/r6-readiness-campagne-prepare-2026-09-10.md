# R6 — readiness de campagne, état PREPARE

> **Supplanté par `r6-readiness-campagne-prepare-v2-2026-09-10.md`.** Les commandes de ce
> premier état ne contiennent pas la garde `--plafond-modele` ajoutée ensuite et ne doivent
> plus être utilisées.

## Verdict

**READINESS BLOQUÉE. Aucun appel de campagne ne doit partir.** Le manifeste privé
`data/traces/reprise/GO-R6-campagne-PREPARE-20260910.json` est un inventaire en état
`PREPARE_BLOCKED`, pas un feu vert. `data/traces/STOP-R6` reste présent et
`data/traces/GO-R6` reste absent.

Le protocole scientifique de la campagne à une réponse par cellule est inchangé. Le blocage
vient de paramètres d’exécution que les documents locaux ne permettent pas de figer sans
les inventer : fournisseurs aval de tout le panel sauf DeepSeek, plafonds tarifaires et
bornes par appel correspondants, et plafond cumulé par modèle entre F1, F2 et plancher.

## Éléments scellés

Le panel garanti contient les trois gratuits, six ouverts payants, quatre fermés
économiques et `openai/gpt-5.4`; `anthropic/claude-sonnet-5` reste conditionnel. L’ordre et
les lignes v2 sont :

| ordre | modèle | ligne v2 USD | seuil de projection à 1,5× | fournisseur figé |
|---:|---|---:|---:|---|
| 0a | `google/gemma-4-31b-it:free` | 0 | — | non; nouveaux appels gratuits suspendus |
| 0b | `nvidia/nemotron-3-super-120b-a12b:free` | 0 | — | non; nouveaux appels gratuits suspendus |
| 0c | `nvidia/nemotron-3-ultra-550b-a55b:free` | 0 | — | non; nouveaux appels gratuits suspendus |
| 1 | `deepseek/deepseek-v4-flash` | 0,04 | 0,06 | DigitalOcean |
| 2 | `mistralai/mistral-small-2603` | 0,08 | 0,12 | non |
| 3 | `meta-llama/llama-4-maverick` | 0,10 | 0,15 | non |
| 4 | `qwen/qwen3.7-plus` | 0,16 | 0,24 | non |
| 5 | `moonshotai/kimi-k2.5` | 0,23 | 0,345 | non |
| 6 | `z-ai/glm-5` | 0,28 | 0,42 | non |
| 7 | `openai/gpt-5.6-luna` | 0,11 | 0,165 | non |
| 8 | `google/gemini-3.8-flash` | 0,39 | 0,585 | non |
| 9 | `anthropic/claude-haiku-4.5` | 0,52 | 0,78 | non |
| 10 | `x-ai/grok-4.3` | 0,55 | 0,825 | non |
| 11 | `openai/gpt-5.4` | 1,34 | 2,01 | non |
| 12 | `anthropic/claude-sonnet-5`, conditionnel | 1,03 | 1,545 | non |

Sonnet ne peut entrer que si l’usage R6 observé avant son lancement est au plus 3,37 USD.
La somme des lignes v2 garanties est 3,80 USD; avec les essais et planchers estimés dans le
plan, la projection est 3,90 USD. Avec Sonnet, ces montants deviennent 4,83 et 4,93 USD :
le plafond global décide donc réellement de son exclusion ou de son entrée.

Les cellules sont figées sans créer de nouvelle liste :

| passe | cellules | sceau |
|---|---:|---|
| F1 `q4` | 894 | SHA-256 canonique `9a70fa42e11ec1c29271253b2199a2c780a5937f624af744016fcf3f3a292dc9` |
| F2 `q4gab3` | 316 | SHA-256 canonique `a28dba31018f36f0a2d34814dee97767b1eeb27560b5b804bb04695d0c55f53b` |
| plancher machine F1 | 40 | fichier SHA-256 `dbe1e6e59553c6636ba1dcbac00cd4347cb1edfa241d7ebe4c18f5398b0c87bc` |
| essai | 10 par passe | fichier SHA-256 `0898b5e171e0825a3784a058c1dd490c22d73ff00f4dd3505bb80f3ff69710c5` |

Chaque payant conserve température 0, `max_tokens=150`, raisonnement `off`, parse strict,
aucun `stop`, aucune relance après rejet, fournisseur imposé et repli interdit. L’identité
globale inclut la passe; un suffixe différent ne rachète jamais une cellule. Le registre
contient 20 réservations DeepSeek toutes réconciliées, coût réglé 0,0003289566 USD et aucune
réservation ambiguë. Il reste au plus **4,3996710434 USD** de dépense R6 sous le plafond dur
de 4,40 USD. La borne réelle au prochain appel sera
`min(4,3996710434, crédits frais − 1,50, limite de clé restante)`.

## Critères conservés

- projection pilote supérieure à 1,5 fois la ligne v2 : une correction au raisonnement
  minimum, nouvel essai, puis retrait au second dépassement;
- moyenne de raisonnement supérieure à 50 : même correction puis retrait;
- plus de deux rejets de parse sur dix : retrait sans reformulation;
- moins de sept distributions identiques sur dix : marque « non déterministe » et A4
  lisible seulement par le plancher machine;
- plus de trois 429 sur vingt appels : arrêt du run, attente d’une heure, reprise sans
  seconde clé.

DeepSeek a passé coût, transport, parse et raisonnement, mais échoué le déterminisme à
1/10. Il reste donc dans le panel comme non déterministe selon la lecture de conformité,
avec la restriction A4 prévue. Tous les autres payants doivent encore passer leur propre
essai deux fois dix avant leur campagne.

## Commandes exactes disponibles

Les seules commandes de campagne entièrement déterminables hors ligne concernent
DeepSeek/DigitalOcean. Elles sont préparées ci-dessous, mais **ne sont pas autorisées à
être exécutées** tant que la readiness reste bloquée, `STOP-R6` présent et `GO-R6` absent.
Les plafonds de trace sont répartis de façon que leur somme, ajoutée au pilote réglé, reste
sous 0,06 USD : 0,04267 + 0,01508 + 0,00190 + 0,0003289566 = 0,0599789566 USD.

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python analyses/r6_oracle_distant.py \
  --modele deepseek/deepseek-v4-flash --plan f1 --plafond 0.04267 \
  --max-tokens 150 --raisonnement off --suffixe r6v2-campagne-f1 \
  --fournisseur DigitalOcean --max-price-prompt 0.11 \
  --max-price-completion 0.22 --max-prompt-tokens 600 --borne-appel 0.001 \
  --passe campagne \
  --manifeste-import data/traces/reprise/r6-v2-import-manifeste.json \
  --registre data/traces/reprise/r6-v2-registre-global.jsonl

PYTHONDONTWRITEBYTECODE=1 .venv/bin/python analyses/r6_oracle_distant.py \
  --modele deepseek/deepseek-v4-flash --plan f2 --plafond 0.01508 \
  --max-tokens 150 --raisonnement off --suffixe r6v2-campagne-f2 \
  --fournisseur DigitalOcean --max-price-prompt 0.11 \
  --max-price-completion 0.22 --max-prompt-tokens 1000 --borne-appel 0.001 \
  --passe campagne \
  --manifeste-import data/traces/reprise/r6-v2-import-manifeste.json \
  --registre data/traces/reprise/r6-v2-registre-global.jsonl

PYTHONDONTWRITEBYTECODE=1 .venv/bin/python analyses/r6_oracle_distant.py \
  --modele deepseek/deepseek-v4-flash --plan f1 \
  --liste data/traces/r6-verif-cellules.txt --plafond 0.00190 \
  --max-tokens 150 --raisonnement off --suffixe r6v2-plancher \
  --fournisseur DigitalOcean --max-price-prompt 0.11 \
  --max-price-completion 0.22 --max-prompt-tokens 600 --borne-appel 0.001 \
  --passe plancher \
  --manifeste-import data/traces/reprise/r6-v2-import-manifeste.json \
  --registre data/traces/reprise/r6-v2-registre-global.jsonl
```

Le `max-prompt-tokens=1000` de F2 est une borne financière prudente dérivée du maximum local
829 et de la marge tokenizer de 15 %; il n’est pas envoyé au modèle et ne change pas
l’invite. Les trois commandes restent néanmoins non exécutables dans la readiness globale,
car le client ne cumule pas lui-même ces trois plafonds comme un plafond par modèle. Leur
répartition doit être scellée et vérifiée par un lanceur transactionnel avant activation.

Aucune commande exacte ne peut être produite honnêtement pour les autres modèles : le
champ obligatoire `--fournisseur`, ses prix maximaux et la borne d’appel sont inconnus dans
les preuves locales. Les remplacer par le nom de l’éditeur ou le prix agrégé du cache serait
inventer le fournisseur aval.

## Vérification hors ligne

Commandes exécutées :

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python analyses/test_r6_client.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python analyses/test_r6_evaluer.py
```

Résultat : 220 contrôles client et 16 tests évaluateur passent. Le client vérifie les
cellules 894/316, la reprise sans doublon, le STOP-R6 dédié, le GO, le registre append-only,
la clé finie sans reset, le plafond effectif, la réserve, les ambiguïtés et la garde 429.
Ces tests ne résolvent ni les fournisseurs manquants ni le plafond cumulé par modèle.

La readiness ne pourra passer à `READY` qu’après résolution documentée de ces deux écarts,
achèvement des pilotes requis dans l’ordre, et autorisation opérationnelle distincte. Le
manifeste `PREPARE` ne doit jamais être renommé ou copié vers `data/traces/GO-R6`.
