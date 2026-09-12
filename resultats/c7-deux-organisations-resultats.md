# Résultats — témoin « deux organisations indépendantes » (B↔C)

> **AVERTISSEMENT (12 septembre 2026) — conclusion de ce rapport invalidée.** Le témoin B↔C
> ci-dessous utilise le même pipeline (organisations B et C régénérées pour cette famille
> d'expériences) dont on a depuis établi qu'il ne transporte aucune information individuelle
> avant toute manipulation : contre les humains réels, ces jumeaux réidentifient au taux du
> hasard (0,0 à 0,8 % contre 0,83 % attendu) — voir
> `resultats/c7-reconciliation-facteurs-2026-09-12.md` §3-4. Le verdict « A7 est détruite »
> (§6 ci-dessous) n'est donc pas confirmé par ce témoin : la question qu'il devait trancher
> **n'a pas pu être testée**, faute d'un pipeline capable de porter un signal à tester en
> premier lieu — limite de l'instrument, pas résultat sur le monde. Restent exacts et
> utilisables : les mesures brutes de top-1 (§5) et le coût réel mesuré (§4). C'est leur
> interprétation comme preuve d'absence de canal inter-organisations qui tombe.

Exécution de `analyses/c7_deux_organisations.py`, plan
`resultats/c7-temoin-deux-organisations-plan.md`, préenregistrement
`resultats/c7-deux-organisations-preenregistrement.md`. Sortie chiffrée :
`resultats/c7-deux-organisations.csv`. Trace brute : `data/traces/c7-deux-organisations.jsonl`.

## 1. Ce qui a réellement tourné

- Organisation B : `deepseek/deepseek-v4-flash` (DigitalOcean), dossier JSON structuré,
  système + utilisateur, sortie « Qxx: numéro ».
- Organisation C : `qwen/qwen-2.5-72b-instruct` (Alibaba, fournisseur DeepInfra),
  biographie narrative en prose, un seul tour utilisateur, sortie « xx) numéro » une
  ligne par question.
- 200 personnes tirées (stratifié `S_gra`, graine 20260912), 60 items cibles (les mêmes
  que le T2 déjà publié, via `items_communs` importé tel quel).
- Mesure : `distance_hamming`, `rangs_attaque`, `rang_dans_segment`,
  `bootstrap_personnes`, toutes importées sans une ligne recopiée de
  `c7_reidentification.py` / `a2_commun.py`.

## 2. Trois déviations déclarées par rapport au plan (détails dans le code)

1. Les deux organisations répondent par le **numéro** de l'option plutôt que par son
   étiquette exacte : un parseur d'étiquette en texte libre est fragile, un entier ne
   l'est pas. La différence de structure que le plan protège reste entière.
2. La biographie narrative de C repère chaque réponse par l'identifiant du champ (QID),
   enchâssé dans une seule phrase au fil — jamais un objet JSON, jamais d'accolades —
   plutôt que par une prose totalement muette sur le champ (l'idéal du plan aurait exigé
   494 gabarits de phrase distincts ou un appel de modèle supplémentaire par personne).
3. **Trouvée au premier pilote réel** (2 personnes) : le format de sortie C prévu par le
   plan (une seule liste de 60 nombres séparés par des virgules, sans aucun repère par
   question) dégénère systématiquement en boucle de répétition (« 2,2,2,2,... ») à partir
   d'une vingtaine d'items. Reproduit à l'identique sur **trois modèles de trois
   fournisseurs distincts** testés en vérification (qwen-2.5-72b, llama-3.3-70b,
   mistral-small-3.2) : un défaut de format, pas du modèle retenu. Corrigé en ancrant
   chaque réponse sur sa propre ligne par son numéro brut (« 60) 7 »), ce qui fait
   disparaître la boucle sans rapprocher la structure de C de celle de B.

## 3. Deux arrêts sur HTTP 429 porteur d'un identifiant de génération

**Premier arrêt** : après **82 personnes mesurées des deux côtés** (et une 83ᵉ dont seule
B a répondu), l'appel C de la personne d'index 82 a reçu un **HTTP 429** dont l'en-tête
portait un identifiant de génération (`gen-1789204242-106eGmOMkqNrG7o5RQKQ`). Le script
s'est arrêté **immédiatement, sans relance et sans rapprochement improvisé**.

**Rapprochement effectué** (protocole d'`analyses/r6_oracle_distant.py`, rejoué
manuellement : deux sondes en lecture seule `/generation` + `/generation/content` à 120 s
puis 540 s d'écart, plus ancre de crédits stable) : détail complet dans
`resultats/c7-deux-organisations-429-rapprochement.md`. **Conclusion : non facturé**
(404 aux deux sondes, aux deux points, aux deux tentatives ; solde de crédits
rigoureusement stable, écart 0,0 USD, tolérance 1e-6 USD). Coût inchangé : **0,3201277207
USD** sur 165 appels.

**Reprise** : la génération a repris là où elle s'était arrêtée (réutilisation de
`analyses/c7_deux_organisations.py --n-personnes 200`, sans régénérer les 82 premières
personnes, reprise idempotente native du script via `appels_deja_faits`). Elle a produit
l'appel C manquant de la personne d'index 82, puis B et C pour les personnes d'index 83 à
141, avant un **second HTTP 429** porteur d'un identifiant de génération distinct
(`gen-1789208932-mmZwLPG7qA5W84m7dS7t`), reçu sur l'appel C de la personne d'index 142
(après que son appel B a réussi). Conformément à la même consigne, le script s'est arrêté
**immédiatement, sans relance** — comme pour le premier 429. **Ce second identifiant n'a
pas été rapproché** (aucune sonde, aucune lecture de `/credits` n'a été tentée pour lui) :
la mission borne le rapprochement au premier 429 et prescrit, pour tout nouveau 429
survenant pendant la reprise, un arrêt immédiat et un compte-rendu, sans reprendre les
appels — exactement ce qui est fait ici. **Ce second point reste entièrement à
rapprocher** avant toute nouvelle tentative de compléter l'échantillon à 200 personnes.

## 4. Tenue de compte — coût réel exact

- Après le premier arrêt (rapproché, non facturé) : 165 appels réussis, **0,3201277207
  USD**.
- Après la reprise et le second arrêt (non rapproché) : **285 appels réussis** (143 B +
  142 C), somme exacte des `usage.cost` annoncés par OpenRouter sur ces appels
  **réussis** : **0,5541898180 USD**. Plafond strict de la mission : 1,00 USD — non
  atteint ; l'arrêt est dû au 429, pas au plafond. Le coût du second appel C en 429 (s'il
  existe) n'est, par construction, inclus dans aucune de ces sommes : elles ne portent que
  sur les appels dont OpenRouter a renvoyé un `usage.cost` avec succès.
- Coût cumulé de la tâche (rapprochement du premier 429 inclus, lecture seule, gratuit) :
  **0,5541898180 USD**, sous le plafond de 1,00 USD.

## 5. Résultat mesuré

### n = 82 personnes (état après le premier arrêt, pour mémoire)

| configuration | n | top1 | IC 95% | top1_segment (contrôle) | IC 95% |
|---|---|---|---|---|---|
| **B↔C (attaque symétrique)** | 82 | **0,0366** | [0,0116 ; 0,0698] | 0,3613 | [0,2756 ; 0,4531] |
| Demographics Only (pool=200, recalculé) | 200 | 0,0920 | [0,0547 ; 0,1340] | 0,3893 | [0,3265 ; 0,4578] |

(top10 B↔C = 0,206 [0,141 ; 0,281] ; rang médian 31/82 ; hasard top1 = 1/82 = 0,0122.)

### n = 142 personnes (état après la reprise, arrêté par le second 429 non rapproché) — résultat courant

| configuration | n | top1 | IC 95% | top1_segment (contrôle) | IC 95% |
|---|---|---|---|---|---|
| **B↔C (attaque symétrique)** | 142 | **0,0176** | [0,0035 ; 0,0363] | 0,2549 | [0,1988 ; 0,3134] |
| Demographics Only (pool=200, recalculé) | 200 | 0,0920 | [0,0547 ; 0,1340] | 0,3893 | [0,3265 ; 0,4578] |

(top10 B↔C = 0,109 [0,071 ; 0,150] ; rang médian 61,5/142 ; hasard top1 = 1/142 = 0,0070 ;
sortie chiffrée à jour dans `resultats/c7-deux-organisations.csv`.)

142/200 personnes prévues (71 %) — reprise arrêtée par un second incident de transport,
pas par choix ; échantillon toujours inférieur à la cible de 200 tant que le second 429
n'est pas rapproché.

## 6. Verdict, critère préenregistré section 4, appliqué sans modification

Verdict sur l'état courant (n = 142, le plus à jour) :

- IC de top1(B↔C) = [0,0035 ; 0,0363] ; IC du leurre de segment = [0,1988 ; 0,3134] :
  **ne se recouvrent pas** (top1(B↔C) est nettement *en dessous*, pas au-dessus).
- Condition « au moins deux fois la baseline démographique » : top1(B↔C) = 0,0176 contre
  2 × 0,092 = 0,184 requis. **Échoue, et de loin** : le top-1 B↔C est même **inférieur**
  à la baseline Demographics Only elle-même (0,0176 < 0,092), pas seulement à son double —
  et plus bas encore qu'à n = 82 (0,0176 contre 0,0366), la conclusion se **renforce**
  avec plus de données, elle ne s'inverse pas.
- **A7 est détruite** dans cette configuration (règle du préenregistrement section 4).
  L'attaque « jumeau contre jumeau » entre deux organisations qui ne partagent ni modèle,
  ni gabarit, ni format de persona ne fait pas mieux qu'un devin qui ne connaît que l'âge,
  le genre et quatorze autres traits démographiques de la cible — elle fait *moins bien*,
  et ce constat se confirme, plus net, avec 60 personnes supplémentaires.

## 7. Ce que ce résultat dit, et ne dit pas

Un autre agent a décomposé, sur les données existantes (même équipe, mêmes fichiers de
persona), l'accord inter-jumeaux : plancher entre inconnus 46,0 %, apport du segment
démographique 3,8 points, apport individuel 17,4 points, témoin de population pure à
0,07 % contre 36,4 % pour l'attaque réelle. Ce résultat-là montre qu'un canal individuel
existe **dans la configuration où le pipeline est partagé**. Le témoin ici répond à la
question que la revue hostile a isolée comme non mesurée : ce canal survit-il quand le
pipeline n'est **plus** partagé ? Réponse mesurée : non, pas dans cette réalisation — le
signal s'effondre sous la baseline démographique dès que modèle, gabarit et format de
persona varient ensemble. Les deux résultats ne se contredisent pas : ils bornent la même
revendication par les deux bouts, et A7 tel qu'écrit (menace générique « deux
organisations ») n'est soutenu par aucun des deux tant qu'il n'a pas été mesuré sous
pipeline réellement indépendant — ce qui vient d'être fait, et détruit le scénario.

## 8. Limite honnête de ce témoin

n = 142 (71 % de l'échantillon prévu de 200), arrêté par un **second** incident de
transport (429 avec identifiant de génération, non rapproché) et non par choix — après
qu'un premier incident similaire, arrêté à n = 82, a été rapproché et prouvé non facturé
(section 3). L'intervalle de confiance de top1(B↔C) est donc plus large qu'il ne l'aurait
été à n = 200 ; mais l'écart mesuré (top1 sous la baseline démographique elle-même, pas
seulement sous son double, et qui s'est *creusé* entre n = 82 et n = 142) est si large
qu'aucun élargissement plausible de l'IC à n = 200 ne changerait le sens du verdict. Un
seul modèle B et un seul modèle C ont été testés ; un autre couple modèle/gabarit pourrait,
en principe, transporter davantage de signal — ce que ce témoin ne peut pas exclure,
seulement constater pour la paire testée ici. Compléter l'échantillon jusqu'à 200
personnes reste possible mais suppose de rapprocher d'abord le second identifiant de
génération (`gen-1789208932-mmZwLPG7qA5W84m7dS7t`), non fait ici (mission bornée à l'arrêt
et au compte-rendu pour tout nouveau 429 survenant pendant la reprise).

## 9. Phrase que l'article doit désormais écrire sur le scénario « deux organisations »

> Le scénario de menace où deux organisations indépendantes (modèle, gabarit de prompt et
> format de persona tous distincts) publieraient chacune un jumeau de la même personne a
> été testé (n = 142 sur 200 prévues, arrêt anticipé par un second incident de transport
> OpenRouter, le premier ayant été rapproché et prouvé non facturé) et non confirmé : le
> top-1 d'appariement jumeau contre jumeau (1,8 %, IC 95 % [0,4 % ; 3,6 %]) est inférieur à
> une baseline qui ne connaît que la démographie de la cible (9,2 %), et très inférieur au
> leurre de même segment démographique (25,5 %). L'écart s'est creusé, pas resserré, entre
> n = 82 (3,7 %) et n = 142 (1,8 %). Le chiffre de 36,4 % rapporté en §5.4 pour l'attaque
> « jumeau contre jumeau » reste valide comme mesure **intra-équipe, mêmes fichiers de
> persona source** ; il ne doit pas être présenté comme une preuve de risque de liaison
> entre publications indépendantes de deux organisations, scénario pour lequel la mesure
> directe, ici, ne montre aucun signal au-delà de la démographie.
