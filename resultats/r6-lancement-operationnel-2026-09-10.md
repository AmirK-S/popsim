# R6 — lancement opérationnel après dépôt OSF v2

État préparé le 10 septembre 2026. Aucun appel authentifié, paiement ou génération n'a
été effectué pendant cette préparation. Le parent a confirmé pour la clé R6 : limite
totale 4,40 USD, restant 4,40 USD, `reset: null`, usage 0. Le manifeste privé conserve
ce snapshot comme garde des nouveaux appels. Il ne l'utilise pas comme preuve historique
pour les incidents, faute d'identifiant non secret reliant l'ancienne clé à l'actuelle.

## Import historique

Le manifeste privé est `data/traces/reprise/r6-v2-import-manifeste.json`. Il scelle quatre
JSONL et la liste des dix cellules par SHA-256, puis exige exactement 40 lignes : 29
réponses distantes à coût annoncé nul et 11 incidents dont le coût par réponse est absent.
Les 40 lignes sont classées
`ancien-pilote`. Aucune n'est présentée comme une passe v2 postérieure au dépôt OSF.

Les 29 réponses ont un coût annoncé confirmé de 0 USD. Pour les 11 incidents, le registre
garde `cout_observe: inconnu` et une borne tarifaire distincte de 0 USD, fondée sur les
identifiants `:free` et le catalogue local archivé. Cette borne n'est pas une observation
de facturation. Aucun identifiant de clé n'est présent dans les traces ; les données
disponibles ne permettent donc pas de rapprocher l'ancienne clé du snapshot actuel.

Le registre privé a été initialisé avec 42 événements : initialisation, 29 coûts confirmés,
11 coûts historiques incertains avec borne, puis sceau de fin. Le total confirmé et la
borne cumulée valent chacun 0 USD. Commande reproductible, sans réseau ni lecture de clé :

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python analyses/r6_oracle_distant.py \
  --initialiser-registre \
  --manifeste-import data/traces/reprise/r6-v2-import-manifeste.json \
  --registre data/traces/reprise/r6-v2-registre-global.jsonl
```

## Séquence exacte après dépôt OSF

Le parent dépose d'abord `resultats/r6-preenregistrement-v2.md`, puis crée
`data/traces/GO-R6`. `data/traces/STOP` doit être absent. Le premier essai est la reprise
du gratuit existant. L'index de la trace interdit de rejouer ses dix cellules déjà écrites :

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python analyses/r6_oracle_distant.py \
  --modele nvidia/nemotron-3-super-120b-a12b:free \
  --plan f1 \
  --liste data/traces/r6-essai-cellules.txt \
  --essai 10 \
  --plafond 0.01 \
  --raisonnement off \
  --pause 3.5 \
  --suffixe r6essai2 \
  --manifeste-import data/traces/reprise/r6-v2-import-manifeste.json
```

Ensuite, un seul essai du premier modèle payant, sur les dix cellules pré-tirées :

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python analyses/r6_oracle_distant.py \
  --modele deepseek/deepseek-v4-flash \
  --plan f1 \
  --liste data/traces/r6-essai-cellules.txt \
  --essai 10 \
  --plafond 0.05 \
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

Le 10 septembre à 18:09 CEST, le catalogue public OpenRouter confirmait les deux
identifiants de modèle. L'endpoint public du modèle payant donnait `DigitalOcean`, prix
0,0679 USD par million de jetons d'entrée et 0,168 USD par million de jetons de sortie.
La borne dérivée pour 600 jetons d'entrée et 150 de sortie vaut 0,00006594 USD ; la
réservation de 0,001 USD par appel la couvre. Chaque cellule payante reprend sous verrou
un GET `/key` et `/credits`, exige limite ≤ 4,40 USD sans reset, réserve 1,50 USD sur le
compte, persiste la réservation avant l'envoi, fixe le fournisseur sans repli et refuse
la suite si coût, identifiant de facture ou fournisseur est ambigu.

Ces deux commandes ne créent aucune nouvelle passe implicite par suffixe. Le gratuit
reste un ancien pilote technique ; le payant devient `essai-1`, première vraie passe v2
après dépôt OSF. La deuxième passe, le plancher et la campagne ne sont pas autorisés par
ce mode opératoire.
