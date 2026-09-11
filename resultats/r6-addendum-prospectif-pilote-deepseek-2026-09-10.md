# Addendum prospectif R6 — pilote DeepSeek payant

**Statut : projet non déposé, non revu et non figé. Aucun GO actif.** Ce texte ne modifie pas le plan R6 enregistré ni ses invites. Il prépare uniquement un amendement OSF prospectif à examiner avant tout appel. Les modèles fermés restent interdits.

Après suspension des gratuits défaillants, le pilote proposé porte sur `deepseek/deepseek-v4-flash`, deux passes de dix cellules sur la liste déjà scellée. DigitalOcean est imposé et tout repli est interdit. Chaque requête conserve `max_tokens=150`, raisonnement désactivé, au plus 600 jetons d’entrée, prix maximaux de 0,0679 USD/M en entrée et 0,168 USD/M en sortie, et une réservation maximale de 0,001 USD.

Le registre global impose désormais simultanément : vingt opérations pilote au maximum pour `essai-1` et `essai-2`; coût réservé ou réglé cumulé au plus égal à 0,02 USD; inclusion de ce coût dans le plafond R6 toutes lignes de 4,40 USD; réserve de compte de 1,50 USD. Ces contrôles sont repris sous verrou avant chaque appel avec les gardes fraîches existantes. Le vingt-et-unième appel et toute réservation qui ferait dépasser 0,02 USD sont refusés avant envoi.

Il n’existe aucune relance automatique payante. Une erreur portant un identifiant de génération conserve la réservation et le marqueur comme ambigus; toute nouvelle réservation et tout second POST sont bloqués jusqu’à rapprochement. Une erreur établie sans génération peut annuler sa réservation avec preuve et reste une cellule non jouée. Pour arrêter R6, l’opérateur utilise `data/traces/STOP-R6`; ni Gödel ni le client R6 ne doivent créer ou retirer le STOP global partagé.

Après dépôt de cet addendum, revue et nouveau GO explicite, les commandes proposées sont :

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python analyses/r6_oracle_distant.py \
  --modele deepseek/deepseek-v4-flash \
  --plan f1 \
  --liste data/traces/r6-essai-cellules.txt \
  --essai 10 \
  --plafond 0.02 \
  --max-tokens 150 \
  --raisonnement off \
  --suffixe r6v2-essai1 \
  --fournisseur DigitalOcean \
  --max-price-prompt 0.0679 \
  --max-price-completion 0.168 \
  --max-prompt-tokens 600 \
  --borne-appel 0.001 \
  --passe essai-1 \
  --manifeste-import data/traces/reprise/r6-v2-import-manifeste.json \
  --registre data/traces/reprise/r6-v2-registre-global.jsonl
```

Puis, seulement si la première passe ne produit aucune ambiguïté :

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python analyses/r6_oracle_distant.py \
  --modele deepseek/deepseek-v4-flash \
  --plan f1 \
  --liste data/traces/r6-essai-cellules.txt \
  --essai 10 \
  --plafond 0.02 \
  --max-tokens 150 \
  --raisonnement off \
  --suffixe r6v2-essai2 \
  --fournisseur DigitalOcean \
  --max-price-prompt 0.0679 \
  --max-price-completion 0.168 \
  --max-prompt-tokens 600 \
  --borne-appel 0.001 \
  --passe essai-2 \
  --manifeste-import data/traces/reprise/r6-v2-import-manifeste.json \
  --registre data/traces/reprise/r6-v2-registre-global.jsonl
```

Le passage à une campagne reste soumis aux critères déjà enregistrés et au budget global résiduel; cet addendum ne l’autorise pas à lui seul.
