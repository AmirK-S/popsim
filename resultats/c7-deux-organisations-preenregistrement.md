# Préenregistrement — témoin « deux organisations indépendantes » (B↔C)

Écrit le 12 septembre 2026, **avant tout appel payant**, en exécution du plan déjà figé
dans `resultats/c7-temoin-deux-organisations-plan.md` (conception seule, aucun appel).
Ce fichier ajoute uniquement ce que le plan laissait à la décision de lancement :
les prédictions chiffrées et la confirmation opérationnelle des deux modèles.

## 1. Ce qui est repris du plan sans changement

- Population : 200 personnes de Twin-2K-500, tirage stratifié sur `S_gra`, graine fixe
  `20260912`, à partir des réponses brutes de démographie + contexte (jamais le texte de
  persona déjà publié par Twin-2K-500).
- Items cibles : les 60 items « toujours renseignés » de
  `analyses/c7_reidentification.items_communs(codes, [REF_V4, REF_V13])` — exactement le
  sous-ensemble qui donne 36,4 % dans le T2 déjà publié.
- Organisation B : `deepseek/deepseek-v4-flash`, fournisseur imposé DigitalOcean, persona
  en dossier JSON structuré, sortie `identifiant: option` une ligne par question.
- Organisation C : persona en biographie narrative en prose (premher personne), sortie en
  liste de nombres séparés par des virgules, sans identifiant de question.
- Mesure : `a2_commun.distance_hamming`, `c7_reidentification.rangs_attaque`,
  `c7_reidentification.rang_dans_segment` (contrôle `S_gra`), `a2_commun.bootstrap_personnes`
  (2000 tirages) — tous importés tels quels, sans une ligne recopiée.
- Baseline Demographics Only : recalculée sur le même sous-échantillon de 200 personnes et
  le même pool de 200, à partir de `Demographics Only - GPT4.1-mini` déjà publié (coût nul,
  aucune génération à refaire).

## 2. Confirmation opérationnelle (lecture seule, gratuite, faite avant ce préenregistrement)

`GET /api/v1/models` et `GET /api/v1/models/qwen/qwen-2.5-72b-instruct/endpoints` :

- Modèle B confirmé : `deepseek/deepseek-v4-flash`, prix déjà vérifié dans
  `resultats/openrouter-etat-2026-09-12.md` (0,11 $ / 1M entrée, 0,22 $ / 1M sortie,
  fournisseur DigitalOcean).
- Modèle C confirmé disponible : `qwen/qwen-2.5-72b-instruct` (Alibaba, architecture et
  fournisseur distincts de DeepSeek), prix catalogue ≈ 0,36 $ / 1M entrée, 0,40 $ / 1M
  sortie. Fournisseur retenu : **DeepInfra** (uptime 99,97 % sur 30 jours, endpoint le
  moins cher des deux vus). Ce prix est plus élevé que l'estimation indicative du plan
  (0,15 $/0,60 $) mais reste du même ordre de grandeur ; le coût total estimé en tient
  compte ci-dessous.
- Coût réestimé avec le prix réel de C : B ≈ 0,000473 $/personne (inchangé) ; C ≈
  (3 000 × 0,36 + 400 × 0,40) / 1 000 000 ≈ 0,00124 $/personne. Total ≈ 0,0017 $/personne
  × 200 ≈ **0,34 $**, toujours largement sous le plafond strict de 1,00 $ fixé pour cette
  tâche.

## 3. Prédiction chiffrée, écrite avant tout appel

Le T2 déjà publié (même équipe, mêmes fichiers de persona sources, deux configurations
Twin-2K-500) donne un top-1 de **36,4 %** sur ces mêmes 60 items. Ce témoin retire tout ce
que ce chiffre partageait : le modèle, le gabarit de prompt, le format de persona.

Ma prédiction, avant tout appel :

- **Point central : top-1 B↔C ≈ 0,15** (soit environ 4 fois moins que le T2 publié), parce
  que je m'attends à ce qu'une part réelle mais minoritaire du signal survive au
  changement des trois canaux (les traits de fond d'une personne — verbosité de ses choix,
  cohérence idéologique, sensibilité au prix — devraient transparaître même sous un
  gabarit et un modèle différents), tout en perdant l'essentiel de ce qui tenait à des
  conventions de sortie ou de formulation partagées.
- **Intervalle jugé plausible a priori : [0,05 ; 0,30]**. En dessous de 0,05, je
  m'attendrais à ce que le canal soit essentiellement bruité ; au-dessus de 0,30, je
  m'attendrais à ce que la personne elle-même porte presque autant d'information qu'avec
  un pipeline partagé.
- Baseline Demographics Only recalculée sur le pool de 200 : j'attends un ordre de
  grandeur de 0,02–0,06 (contre 0,021 sur les 2 058 personnes complètes ; un pool 10 fois
  plus petit devrait faire monter un peu le hasard et donc la baseline).
- Contrôle de segment (`top1_segment`, S_gra) recalculé sur 200 personnes stratifiées : sur
  la population complète il valait 0,140 [0,125 ; 0,155] ; avec seulement 200 personnes
  réparties sur 40 niveaux de `S_gra`, les segments seront plus petits et je m'attends à ce
  que ce chiffre soit *plus haut*, peut-être 0,20–0,40.

Ces trois derniers ordres de grandeur sont des attentes, pas des garde-fous : les garde-fous
sont les règles de décision ci-dessous, qui ne dépendent que des valeurs réellement
mesurées sur le même pool.

## 4. Règles de décision, fixées par le plan section 5, reprises mot pour mot

- **A7 survit** si l'intervalle de confiance à 95 % du top-1 B↔C (sur les 200 personnes et
  le pool de 200) NE RECOUVRE PAS celui du contrôle de segment (`top1_segment`) ET reste au
  moins deux fois la baseline Demographics Only recalculée sur le même pool.
- **A7 est détruite** si le top-1 B↔C tombe dans l'intervalle du contrôle de segment, OU
  sous deux fois la baseline démographique. Dans ce cas T2 doit être retitré, cette fois
  faute de preuve et non faute de mesure.
- Aucun autre seuil n'est ajouté après coup. Le résultat rapporté est celui réellement
  obtenu, quel qu'il soit.

## 5. Tenue de compte

Plafond strict de la tâche : 1,00 $ USD. Coût attendu : ≈ 0,34 $. Le script arrête tout
appel supplémentaire si le cumul mesuré (`usage.cost` annoncé par OpenRouter, jamais une
estimation) dépasse 0,90 $, et rapporte le coût exact cumulé en fin de run.

Aucun appel n'a encore eu lieu au moment où ce fichier est écrit.
