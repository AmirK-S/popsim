# R6, preuve de revue GO-QUEUE

Date locale: 10 septembre 2026. Revue indépendante entièrement hors ligne.

## Verdict

**GO-QUEUE-AB** pour les six modèles de la file, dans l'ordre exact du manifeste:

1. `deepseek/deepseek-v4-flash`, descriptif, non déterministe, plancher machine requis pour A4;
2. `mistralai/mistral-small-2603`, descriptif;
3. `qwen/qwen3.7-plus`, descriptif;
4. `z-ai/glm-5`, descriptif;
5. `anthropic/claude-haiku-4.5`, confirmatoire;
6. `x-ai/grok-4.3`, confirmatoire, non déterministe, plancher machine requis pour A4.

Kimi, Gemini, Llama 4 Maverick, GPT-5.6 Luna, GPT-5.4 et Claude Sonnet 5 restent exclus.
La non-détermination de Grok ne change pas le rôle confirmatoire de ses autres analyses.

## Artefacts contrôlés

- runner de campagne: `a49370a37feffe072fdf317a4da8f3027b0b92643fddc195402582cbe32dffa8`;
- tests du runner: `72d3abdd70313a36f2480ee2dc1d8163518ee68ef62ad854074d0f78b02bfa15`;
- manifeste QUEUE_PREPARED: `6ac75dd477659c280aed9e3a6a96c265917f29a4397419242a1149e75bde7598`;
- manifeste READY parent: `dc7482c982df7fc80f1fd8298d1421cbe75ac0053dd5a211c2cf43c0b61028fc`;
- ledger inchangé: `197f79cb8bf8bc47ba228e652ce63a7edbb0c177dfbefa04496562a7a75a23cb`;
- rapport de préparation: `afbfad3c05ca3db6d087a87d6b1a9ee720a307cced3f3835a87193cfd39b3e8f`.

Les fournisseurs, prix maximaux, plafonds unitaires et par modèle, coûts pilotes réglés,
formats, bornes de prompt et cellules correspondent au plan et aux pilotes audités. Les
plafonds modèle totalisent 2,445 USD et chacun inclut les trois plafonds de trace plus le
pilote déjà réglé. Le ledger totalise 0,0342335066 USD et ne contient aucune réservation
ambiguë.

Les trois corrections demandées sont présentes: ordre et rôles indépendants de la
détermination pilote; marqueurs A4 explicites; prédécesseurs limités à 1 250 opérations
`reglee` réparties 894 `campagne/q4`, 316 `campagne/q4gab3` et 40 `plancher/q4`, avec ordre
exact des cellules. Les traces courantes sont validées contre la même séquence complète.

Les quatre suites locales passent: client R6, runner de pilotes, 16 tests de l'évaluateur et
runner de campagnes avec serveur factice loopback. Les six commandes `--verifier` passent
et rendent `QUEUE_PREPARED`, `executable=false`, le rôle et les marqueurs attendus sans lire
de clé ni créer de client distant.

## Dérivation de QUEUE_READY

Conserver le manifeste QUEUE_PREPARED comme preuve immuable. Créer un fichier distinct par
copie exacte, puis changer uniquement les deux champs de contrôle de premier niveau:

- `state`: `QUEUE_PREPARED` devient `QUEUE_READY`;
- `executable`: `false` devient `true`.

Aucun ordre, rôle, marqueur, fournisseur, prix, plafond, coût pilote, étape, cellule,
exclusion, chemin, hash parent ou règle de reprise ne doit changer. Calculer ensuite le
SHA-256 du nouveau fichier. Chaque GO mono-modèle devra porter ce nouveau hash, ainsi que
`state=GO`, `scope=R6-campaign-one-model`, le modèle exact, `one_shot=true` et
`socrates_reviewed=true`.

Cette preuve ne crée aucun GO et ne retire aucun STOP. Au moment de la revue,
`data/traces/STOP-R6` est présent, `data/traces/GO-R6` est absent et aucun GO de campagne
mono-modèle n'existe. Le verrou exclusif de la file et les gardes de prédécesseur restent
obligatoires à chaque lancement.
