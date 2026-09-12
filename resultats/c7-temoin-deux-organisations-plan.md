# Plan du témoin « deux organisations indépendantes » pour T2/A7

Conception seulement. Aucun appel réseau, aucune génération, aucune modification d'un
fichier existant n'a eu lieu pour produire ce plan. Il répond à F3 de
`resultats/revue-hostile-finale-2026-09-12.md` (lignes 131-169) : le T2 actuel
(`article/manuscrit.md` §5.4, lignes 491-526, chiffres dans `c7-transfert-resultats.md`
et `c7-transfert-stanford-resultats.md`) n'oppose que des configurations de la **même
équipe**, à partir des **mêmes fichiers de persona sources** — sur Twin-2K-500, les huit
configurations admissibles de `resultats/twin-ab-audit-provenance-2026-09-11.md` §2.4
varient le modèle et parfois le format de sortie, mais l'invite elle-même n'est même pas
observable localement (réserve R1 du même document) et le contenu-source du persona est
identique d'une configuration à l'autre. Le contrôle existant (leurre de même segment
démographique, ligne 499 du manuscrit) écarte la ressemblance de segment, pas la
ressemblance d'entrée. Ce plan fait varier ensemble les trois choses qu'une vraie
deuxième organisation ne partagerait pas : gabarit de prompt, modèle, format de la
persona — la personne restant seule chose commune.

Note distincte du témoin déjà jugé infaisable (revue, lignes 158-160) : celui-là exigeait
de **régénérer des jumeaux à fidélité comparable en permutant le contenu des personas
entre personnes** d'un même segment, ce que §5.7 dit hors de portée. Le plan ci-dessous
ne permute rien entre personnes : il construit deux pipelines de génération mutuellement
indépendants à partir des réponses brutes **de la même personne** dans les deux cas — une
exigence plus faible, dans les moyens actuels du projet.

## 1. Population et items

- **Source des personnes** : les réponses brutes des 494 items de contexte et des 14
  questions de démographie (`t1_commun.demographies_brutes`, vagues 1-3), déjà présentes
  localement pour les 2 058 personnes de Twin-2K-500. C'est la matière première à partir
  de laquelle chaque organisation simulée construit **son propre** persona — jamais le
  texte de persona déjà publié par Twin-2K-500, pour ne pas reconduire le biais dénoncé.
- **Échantillon pilote : n = 200 personnes**, tirées aléatoirement (graine fixe, écrite
  avant tout appel, comme `tirer_liste` dans `r6_oracle_distant.py`), stratifiées sur le
  segment `S_gra` pour que le contrôle anti-artefact par segment reste mesurable. Un pool
  de 200 donne un hasard de 0,5 % en top-1, loin sous les signaux attendus si le canal
  existe réellement.
- **Items cibles : les 60 items « toujours renseignés »** déjà isolés par
  `items_communs()` dans `analyses/c7_reidentification.py` (Product Pricing 40, False
  consensus 10, heuristiques non expérimentales 10) — le même sous-ensemble que celui
  qui donne 36,4 % dans le T2 actuel. Reprendre exactement ce sous-ensemble rend le
  nouveau chiffre directement comparable à l'ancien, chiffre pour chiffre.
- **Un seul appel de génération par personne et par organisation** (comme la méthodologie
  d'origine de Twin-2K-500, qui produit toutes les réponses d'une personne en un appel),
  demandant les 60 réponses en une fois — pas un appel par item.

## 2. Les deux organisations simulées

| | Organisation B | Organisation C |
|---|---|---|
| Modèle | `deepseek/deepseek-v4-flash` (fournisseur DigitalOcean — déjà vérifié fonctionnel, voir `resultats/openrouter-etat-2026-09-12.md`) | `qwen/qwen-2.5-72b-instruct` (ou tout modèle d'un vendeur distinct, architecture distincte — à confirmer sur `GET /models` avant lancement, prix indicatif ci-dessous à rafraîchir) |
| Format de persona | Dossier JSON structuré, clé/valeur, un objet par item de contexte | Biographie narrative en prose, première personne, rédigée à partir des mêmes réponses brutes mais sans structure clé/valeur visible |
| Format de sortie demandé | `QID: option` une ligne par question, ordre imposé | Liste de nombres séparés par des virgules, un par question, **sans** identifiant de question dans la réponse |
| Style d'invite | Formel, impératif, système/utilisateur en deux tours | Conversationnel, mise en situation, un seul tour utilisateur qui inclut son propre système |

Aucun élément n'est partagé entre B et C hors la personne. Même le parseur de sortie
diffère (un parse par motif `QID: valeur` contre un parse de liste positionnelle), pour
qu'aucune convention de mise en forme commune ne puisse elle-même devenir le canal.

## 3. Les deux gabarits, écrits

**Gabarit B — dossier structuré (système + utilisateur, deux tours) :**

```
[système]
Tu es un simulateur de réponses d'enquête. On te donne un dossier JSON structuré
décrivant une personne à partir de ses réponses à une enquête antérieure. À partir de
ce seul dossier, tu dois prédire comment cette personne répondrait à une nouvelle liste
de questions. Réponds à CHAQUE question par l'étiquette exacte d'une option proposée,
rien d'autre, une ligne par question, préfixée par l'identifiant de question fourni.
Aucune explication, aucune phrase, aucune question omise.

[utilisateur]
DOSSIER (JSON) :
{ "Q_age": "...", "Q_genre": "...", "Q_revenu": "...", ... (494 champs) }

QUESTIONS :
Q317: Aimeriez-vous acheter ce produit à 4,99 $ ? Options : [1 Oui, 2 Non]
Q318: Aimeriez-vous acheter ce produit à 7,99 $ ? Options : [1 Oui, 2 Non]
... (60 questions)

Réponds avec « identifiant: option choisie » pour chacune, dans l'ordre donné, une par
ligne.
```

**Gabarit C — biographie narrative (un seul tour, aucune structure visible) :**

```
[utilisateur]
Mets-toi à la place de la personne suivante et réponds comme elle le ferait.

Tu as 34 ans, tu es mariée, tu vis en zone périurbaine. Tu as déclaré gagner entre
50 000 et 75 000 dollars par an. Tu passes en moyenne deux heures par jour sur internet
en dehors du travail. Interrogée sur tes habitudes d'achat, tu as dit préférer comparer
les prix avant d'acheter et ne jamais acheter sur un coup de tête. [... paragraphe
continuant à restituer en prose les 494 réponses brutes, sans étiquette de champ ...]

Voici maintenant une série de courtes questions. Pour chacune, une seule option te
correspond : donne uniquement le numéro de cette option, sans rien ajouter.

1) Achèterais-tu ce produit à 4,99 $ ? (1) oui (2) non
2) Achèterais-tu ce produit à 7,99 $ ? (1) oui (2) non
... (60 questions)

Réponds par une liste de 60 nombres séparés par des virgules, dans l'ordre des
questions, rien d'autre.
```

Les deux gabarits partagent le même contenu factuel (les réponses brutes de la même
personne) et le même ensemble de 60 questions cibles ; ils ne partagent ni la structure,
ni le vocabulaire, ni la langue de registre (impératif technique contre mise en situation
narrative), ni le format de réponse attendu.

## 4. Protocole de mesure — repris de `analyses/c7_reidentification.py`

Sans une ligne recopiée, réutilisés tels quels :

- `a2_commun.distance_hamming` pour l'accord normalisé entre deux vecteurs catégoriels
  masqués (les 60 items cibles).
- `rangs_attaque` (appariement par rang, bruit i.i.d. pour départager les ex æquo,
  ordre des candidats mélangé avant tout calcul), mais avec un changement d'un seul
  argument : le **pool** n'est plus un pool humain, c'est la matrice des réponses de
  l'organisation C (ou B) pour les mêmes 200 personnes, dans le même ordre d'index —
  c'est exactement l'attaque T2 « jumeau contre jumeau » que le manuscrit revendique,
  sans qu'aucune réponse humaine n'entre dans le calcul de score, conformément à la
  définition de T2 (ligne 278 du manuscrit : « holding no human answer at all »).
- `rang_dans_segment` sur `S_gra`, comme contrôle anti-artefact déjà en place — mais
  cette fois il ne suffit plus à lui seul : voir critère de destruction ci-dessous.
- `bootstrap_personnes`, 2000 tirages, graine fixe, pour l'intervalle de confiance du
  top-1 et du top-10, exactement comme `resume_taux`.
- **Baseline Demographics Only, recalculée sur le même sous-échantillon de 200
  personnes et le même pool de 200**, à partir de `Demographics Only - GPT4.1-mini`
  (déjà publié par Twin-2K-500, coût nul, aucune génération à refaire) — pas la valeur
  publiée sur les 2 058 personnes, pour rester une comparaison à pool égal.
- Sortie : un `c7-transfert-organisations.csv` de même forme que `c7-reidentification.csv`
  (configuration, cible, n_attaques, n_pool, top1 + IC, top10 + IC, rang médian,
  top1_segment + IC), publié dans `resultats/`.

## 5. Le résultat qui détruirait A7

Critère préenregistré, sur le modèle du critère « on fonce » déjà écrit dans
`c7_reidentification.py` (`top1 >= 0.10 and top1 >= 2 * demo_top1`) :

- **A7 survit** si le top-1 d'appariement B↔C, sur les 200 personnes et le pool de 200,
  a un intervalle de confiance à 95 % qui ne recouvre PAS celui du contrôle de segment
  (`top1_segment`) et qui reste au moins deux fois celui de la baseline Demographics
  Only recalculée sur le même pool.
- **A7 est détruite** si le top-1 B↔C tombe dans l'intervalle du contrôle de segment, ou
  sous deux fois la baseline démographique : cela montrerait que le signal T2 déjà publié
  (36,4 % sur les 60 items communs) tenait à la parenté de gabarit, de modèle ou de
  format de persona entre les configurations Twin-2K-500 d'origine — un artefact de
  pipeline partagé — et non à une empreinte propre à la personne qui traverse deux
  générations réellement indépendantes. Dans ce cas, T2 devrait être retitré, comme la
  revue le demande déjà pour la version actuelle, mais cette fois faute de preuve et non
  faute de mesure.

## 6. Coût estimé

Hypothèses de dimensionnement, à confirmer par `GET /models` avant tout lancement (lecture
seule, gratuite) :

- Gabarit B (JSON) : ≈ 3 500 jetons d'entrée (dossier de contexte + 60 questions),
  ≈ 400 jetons de sortie (60 réponses courtes).
- Gabarit C (narratif) : contexte condensé en prose, ≈ 3 000 jetons d'entrée, même
  ≈ 400 jetons de sortie.
- Prix modèle B (`deepseek/deepseek-v4-flash`, mesuré le 12 septembre 2026, voir
  `resultats/openrouter-etat-2026-09-12.md`) : 0,11 $ / 1M jetons d'entrée, 0,22 $ / 1M
  de sortie (`MAX_PRICE_PILOTE` du projet).
- Prix modèle C (indicatif, à vérifier — ordre de grandeur d'un modèle ouvert de taille
  comparable) : ≈ 0,15 $ / 1M d'entrée, ≈ 0,60 $ / 1M de sortie.

Coût par personne :
- B : (3 500 × 0,11 + 400 × 0,22) / 1 000 000 ≈ 0,000473 USD
- C : (3 000 × 0,15 + 400 × 0,60) / 1 000 000 ≈ 0,000690 USD
- Total par personne (B + C) ≈ 0,00116 USD

**Pilote, n = 200 personnes : ≈ 200 × 0,00116 ≈ 0,23 USD**, largement dans le solde
disponible constaté (≈ 6,36 USD, voir tâche 1) et sous le plafond de campagne R6
(4,40 USD, sans lien avec ce témoin qui est une expérience distincte).

**Passage à l'échelle, n = 2 058 (toute la population Twin) : ≈ 2 058 × 0,00116 ≈ 2,39
USD** — si le pilote montre un signal net (ou son absence nette), avant de décider s'il
est utile de le mesurer sur la population entière.

Ce plan ne lance rien : les deux gabarits sont écrits, le protocole de mesure est
entièrement défini par réutilisation de `c7_reidentification.py`, et le critère de
destruction est fixé avant tout appel, comme l'exige la pratique de préenregistrement du
projet. La décision de lancer appartient à l'orchestrateur.
