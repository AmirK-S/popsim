# Audit : « famille d'items » et « nombre de modalités » sont-elles la même partition ? (13 septembre 2026)

statut: courant
note_statut: section 0 = préenregistrement, écrite et commitée SEULE avant tout calcul de ré-identification, non modifiée depuis
mandat: Recouper deux résultats de la même nuit — le facteur de la ré-identification est le nombre de modalités (audit-items-banals) et tout l'effet vit dans les 40 items d'achat (audit-contamination-persona) — pour établir si les deux variables désignent la même partition, et si non, laquelle porte l'effet.
agent: Claude Opus 5, Anthropic
ecriture: analyses/c7_audit_modalites_familles.py, resultats/audit-modalites-familles-2026-09-13.md, resultats/c7-audit-modalites-familles.csv
lecture_seule: tout le reste du dépôt
interdits: appel payant, réseau, recherche web, arrière-plan, commit sur master, fusion, écriture dans article/manuscrit.md, impression de toute donnée individuelle
cecite: les branches non fusionnées dans integration/nuit-2026-09-13 ; la prose de persona (non nécessaire ici) ; les jeux autres que Twin-2K-500
cout_reel_usd: 0.00

---

## 0. Préenregistrement, écrit et commité AVANT tout calcul de ré-identification

### 0.1 Le recoupement

Deux rapports de la nuit, produits par deux agents qui ne se sont pas parlé.

**A — `resultats/audit-items-banals-2026-09-13.md`.** Sur les 60 items toujours renseignés de
Twin, le vrai facteur de la ré-identification est le **nombre de modalités** : le classement par
nombre de modalités croissant restitue **99,8 %** du gain obtenu par le classement par entropie.
41 items sont binaires, 19 ont 4 à 7 modalités. Le balayage culmine à k = 40 (**36,4 %** hors pli)
contre 25,2 % avec les 60 items.

**B — `resultats/audit-contamination-persona-2026-09-13.md`.** Tout l'effet du jumeau vit dans
les **40 items d'achat** (33,2 %) et pas dans les **20 items d'heuristiques** (0,24 %, sous le
comparateur classique servi à 0,51 %). Contamination sémantique et prévisibilité différentielle
sont toutes deux écartées, et le rapport conclut que « le mécanisme de cette concentration reste
inexpliqué ».

**L'objection.** Le rapport B publie lui-même, dans son tableau de la section 4, « modalités par
item : 2,0 (achat) contre 5,6 (heuristiques) ». Le rapport A publie « 41 items binaires sur 60 ».
Arithmétiquement, 40 × 2,0 = 80 et 41 binaires impliquent qu'**au plus un** item d'heuristiques
est binaire. Les deux partitions ne sont donc pas seulement corrélées : elles sont, à un item
près, **identiques**. Si c'est le cas, le « mécanisme inexpliqué » de B est peut-être déjà nommé
par A, et l'article doit changer de formulation.

**Ce qui est déjà acquis avant tout calcul, et que je ne revendique pas comme découverte.** Le
tableau croisé famille × modalités est **dérivable des deux rapports publiés** par la seule
arithmétique ci-dessus. Je le vérifie sur les données (section 1), mais c'est une vérification,
pas une mesure nouvelle, et rien dans ce rapport n'en dépend comme d'un résultat propre. Les
prédictions ci-dessous portent **exclusivement** sur des mesures que je n'ai pas encore faites.

### 0.2 Les trois issues, fixées d'avance

- **Issue A — partition confondue, question indécidable.** Le tableau croisé est diagonal ou
  quasi diagonal, et **aucune** manipulation ne permet de séparer les deux variables. L'article
  doit alors écrire exactement cela : les deux descriptions sont empiriquement indiscernables sur
  ce jeu, et aucune donnée de Twin ne peut les départager. C'est un livrable de pleine valeur —
  « indiscernable » n'est pas « inexpliqué ».
- **Issue B — c'est le nombre de modalités.** Recoder les items d'heuristiques en binaire fait
  monter leur taux vers celui des items d'achat ; la famille n'ajoute rien.
- **Issue C — c'est bien la famille.** Le recodage en binaire laisse les items d'heuristiques au
  plancher. Le nombre de modalités est alors un **corrélat** de la partition, pas sa cause, et le
  mystère de B est réel.

### 0.3 Protocole, et les deux pièges que ce projet a déjà manqués trois fois

**Bassin strictement constant.** Le bassin de `c7_audit_items_banals.preparer()`, repris sans
réimplémentation : 2 058 personnes, candidat `JSON Persona - GPT4.1`, baseline
`Demographics Only - GPT4.1-mini` **recalculée dans chaque condition sur exactement les mêmes
colonnes et le même pool**. Attaque `c7_reidentification.rangs_attaque`, importée telle quelle.

**Nombre d'items apparié entre conditions.** Le top-1 dépend mécaniquement du nombre d'items
*et* de leur nature. Toute comparaison de la section 3 se fait à **20 items** de part et d'autre.
Les 40 items d'achat ne sont donc jamais comparés directement aux 20 items d'heuristiques : ils
sont ramenés à 20 par tirage (10 tirages, moyenne et étendue publiées).

Graine 20260913. Réduction déclarée, identique à celle des deux branches recoupées : 5 tirages de
départage des ex æquo au lieu de 20 ; bootstrap 2 000 personnes.
`c7_controle_interpretabilite.controle_avant_interpretation` appelé avant toute interprétation,
sur les colonnes natives réellement en jeu. Aucune donnée individuelle n'est calculée, imprimée
ou écrite : taux agrégés seuls.

**V1 — le tableau croisé.** Famille (achat / heuristiques, par le suffixe `_Q295` du catalogue,
règle de B reprise telle quelle) × nombre de modalités observées. V de Cramér. Identification
nominale des cases hors diagonale.

**V2 — le recoupement des deux rapports.** L'ensemble « 40 premiers items du classement par
nombre de modalités » de A est-il, ou non, l'ensemble des 40 items d'achat de B ? Si oui, les
chiffres 36,4 % et 33,2 % mesurent la même chose sur le même ensemble.

**V3 — décidabilité observationnelle.** Ré-identification mesurée dans chaque case du croisement,
à bassin constant et à 20 items partout. Si une case est vide ou tient en un item, la question
n'est pas décidable observationnellement et il faut manipuler.

**V4 — le test propre, manipulation du nombre de modalités à famille constante.**
- **V4a — dichotomisation des 20 items d'heuristiques.** Deux règles déclarées d'avance :
  (i) *mode contre non-mode* (réponse modale humaine vague 4 = 1, tout le reste = 0) ;
  (ii) *coupure à la médiane* pour les items ordinaux (codes ≤ médiane = 0, sinon 1), règle (i)
  pour les items non ordinaux. La règle est estimée sur les **réponses humaines** et appliquée à
  l'identique au jumeau et au pool. Variante hors pli déclarée : règle estimée sur une moitié des
  personnes, taux mesuré sur l'autre.
- **V4b — dégradation symétrique des items d'achat, sans fabriquer de données.** On ne peut pas
  ajouter des modalités factices à un item binaire. On peut en revanche **apparier les 40 items
  d'achat deux à deux** en 20 items composites à 4 modalités (le couple de réponses observées
  devient une modalité unique). L'information est **exactement conservée** — la transformation
  est bijective — seul le **grain de la métrique** change : un désaccord sur un seul des deux
  sous-items coûte désormais autant qu'un désaccord sur les deux. C'est la manipulation du nombre
  de modalités à information constante. Appariement par permutation de graine fixe, 5 appariements
  différents, moyenne publiée.

**V5 — les autres variables confondues avec la famille.** Position dans le questionnaire (rang de
colonne au catalogue), longueur du libellé, taux de non-réponse, entropie par item, kappa
test-retest par item. Deux lectures : (i) leur écart entre familles ; (ii) leur corrélation avec
le gain normalisé par item **à l'intérieur du bloc d'achat**, où la famille et le nombre de
modalités sont tous deux constants — c'est le seul endroit où ces variables peuvent parler seules.

### 0.4 Prédictions, et ce qui les réfute

| | prédiction | réfutée si |
|---|---|---|
| **P1** | Le tableau croisé est quasi diagonal : les 40 items d'achat sont tous binaires, et **au plus deux** des 20 items d'heuristiques le sont. V de Cramér > 0,90. | plus de deux items d'heuristiques binaires, **ou** au moins un item d'achat non binaire |
| **P2** | Le recouvrement entre « les 40 items à plus faible nombre de modalités » de A et « les 40 items d'achat » de B est d'**au moins 39 sur 40**. Les deux rapports mesurent le même ensemble. | recouvrement inférieur à 39/40 |
| **P3** | La question n'est **pas** décidable observationnellement : au moins une case du croisement contient moins de 5 items, donc aucun contraste à nombre d'items apparié ne peut y être mesuré. | les quatre cases contiennent chacune ≥ 5 items |
| **P4** | **C'est la prédiction centrale, et elle va contre le confort de l'article.** Le recodage en binaire des 20 items d'heuristiques (V4a) fait **monter** leur taux d'au moins un facteur 10 (de 0,24 % vers ≥ 2,4 %) et le fait **passer au-dessus** de la baseline démographique recalculée sur les mêmes colonnes. Autrement dit : **issue B**, le nombre de modalités est le facteur, et le mystère de B se dissout. | le taux des items d'heuristiques binarisés reste sous 2,4 %, **ou** ne passe pas au-dessus de la baseline (borne basse de l'IC sous la borne haute de la baseline) — auquel cas c'est **issue C** |
| **P5** | La dégradation symétrique (V4b) **fait chuter** le taux des items d'achat d'au moins 30 % en relatif par rapport aux 40 items natifs, à information pourtant identique. | chute inférieure à 10 % en relatif |
| **P6** | Le taux de non-réponse est **structurellement nul** sur les 60 items (ils sont choisis comme toujours renseignés) : ce confondant est exclu par construction, pas par mesure. Parmi les autres, **aucune** ne corrèle au gain normalisé par item à l'intérieur du bloc d'achat à \|r\| > 0,40. | une variable dépasse \|r\| = 0,40 à l'intérieur du bloc d'achat |
| **P7** | Le contrôle d'interprétabilité **passe** sur les 20 items d'achat et **échoue** sur les 20 items d'heuristiques natifs (le jumeau y est sous la baseline, B l'établit déjà). Son verdict sur les items d'heuristiques binarisés est le résultat de P4 et n'est pas prédit séparément. | le contrôle échoue sur les items d'achat, ou passe sur les items d'heuristiques natifs |

### 0.5 Critère de verdict, fixé d'avance

- **Issue B (le nombre de modalités)** si P4 est confirmée. L'article doit alors retirer
  « le mécanisme reste inexpliqué » et écrire que la concentration est un effet du grain de
  réponse, pas de la famille d'items.
- **Issue C (la famille)** si P4 est réfutée, c'est-à-dire si les items d'heuristiques binarisés
  restent au plancher. Le mystère de B est alors réel, mais il est **mieux borné** qu'avant : le
  nombre de modalités est exclu comme explication.
- **Issue A (indécidable)** si, et seulement si, V4a et V4b sont tous deux inexploitables — par
  exemple si le recodage détruit tant d'information que la comparaison ne signifie plus rien, ou
  si le contrôle d'interprétabilité échoue partout, y compris du côté achat.
- **Issue mixte, à déclarer telle quelle** si P4 est réfutée mais P5 confirmée : le nombre de
  modalités agirait alors dans un seul sens (en ajouter nuit, en retirer ne répare pas), ce qui
  n'est ni B ni C et doit être écrit comme tel.

Je note d'avance que ma prédiction centrale P4 **dissout** un mystère que l'article présente
comme une découverte, et que c'est une bonne nouvelle pour l'article et non une mauvaise : un
mécanisme nommé vaut mieux qu'un mécanisme ouvert. Je note aussi que c'est la prédiction que je
suis le plus susceptible de perdre, parce que le recodage en binaire **détruit de l'information**
et pourrait faire baisser le taux pour cette seule raison — la section 4 devra distinguer les
deux effets. Les sections 1 et suivantes sont écrites après exécution, sans modification de la
présente section 0.
