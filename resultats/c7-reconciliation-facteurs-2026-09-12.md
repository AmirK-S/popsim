# Réconciliation des deux mesures « un seul facteur changé » — 12 septembre 2026

Calculé par `analyses/c7_reconciliation_facteurs.py`. **Aucun appel d'API, aucune dépense,
aucune recherche web.** Lecture seule sur `data/`. Sortie chiffrée :
`resultats/c7-reconciliation-facteurs.csv` (47 lignes).

Les deux séries en conflit portent sur la même question — que devient le canal de liaison
entre deux jumeaux d'une même personne quand on change **un seul** élément du pipeline ?

| | Mesure A (`c7-factoriel-resultats.md`) | Mesure B (`moonshot-2026-09-12.md`) |
|---|---|---|
| modèle seul | **0,67 %** [0,00 ; 1,75] | **15–19 %** |
| gabarit seul | **0,83 %** [0,00 ; 2,08] | **70,5 %** |
| persona seul | 2,65 % [0,50 ; 5,13] | non mesuré à 60 items |

---

## 1. Ce que chaque série mesure réellement (vérifié dans le code, pas dans les résumés)

Les deux séries mesurent **la même grandeur** : un top-1 de ré-identification jumeau contre
jumeau, distance de Hamming normalisée, ex æquo départagés par tirage, IC bootstrap sur les
personnes. Elles partagent les mêmes fonctions (`rangs_attaque`, `distance_hamming`,
`bootstrap_personnes`), les **mêmes 60 items** (`items_communs` sur `humains vague 4` et
`humains vagues 1-3`), et la même population source (Twin-2K-500, 2 058 personnes). Ce
n'est donc **ni** un accord brut contre un top-1, **ni** un item set différent.

Quatre différences de définition séparent réellement les deux séries :

1. **Bassin de candidats.** A : pool = 120. B : pool = 2 058 (ou 1 000). Le top-1 est
   mécaniquement plus élevé dans un petit bassin — **cette différence joue contre A**, pas
   pour elle : à bassin égal, A devrait être *plus haute* que B, pas 100 fois plus basse.
2. **Sens de l'attaque.** A : symétrique (moyenne des deux sens). B : lignes dirigées, que
   le résumé du moonshot cite par leur valeur d'un seul sens (« 83,6 % / 79,4 % »).
3. **Nature des jumeaux comparés.** A : jumeaux **régénérés par nous** (deepseek-v4-flash,
   qwen-2.5-72b, personas reconstruits à partir des 494 items de contexte). B : les
   **7 configurations publiées par l'équipe Twin**, mêmes fichiers de persona sources, même
   harnais.
4. **Ce que « un seul facteur » désigne.** A : modèle = deepseek → qwen (familles et
   fournisseurs différents) ; gabarit = structure de tours, format de sortie et parseur tous
   changés. B : modèle = GPT-4.1-mini → Gemini-Flash-2.5 dans le **même harnais** ; gabarit =
   variante « repeating questions » du même gabarit ; et un palier, le décodage (T = 0 contre
   température par défaut), qui n'a **aucun équivalent** dans A.

Le résumé de B contient par ailleurs deux inexactitudes de lecture : le CSV comporte
**56 paires dirigées**, pas 42, et les paliers cités ne sont pas des moyennes de paires mais
des lignes individuelles. Le résumé de A affirme une couverture « 60/60 items pour les trois
conditions » : la trace montre **une réponse M lue à 26/60** (effet négligeable, mais la
phrase est fausse).

## 2. Les deux séries ramenées à une échelle commune

Mêmes 120 personnes (`tirer_echantillon(S_gra, 200, 20260912)[:120]`, identique bit à bit à
celui de `c7_factoriel`), même bassin de 120, mêmes 60 items, même attaque symétrique, même
bootstrap. **C'est possible, et c'est le tableau ci-dessous.**

| ce qui change entre les deux jumeaux | famille | top-1 (pool 120) | IC 95 % |
|---|---|---|---|
| décodage seul (T = 0 vs température par défaut) | Twin | **93,33 %** | [89,29 ; 96,83] |
| gabarit seul (repeating questions) | Twin | **87,10 %** | [82,44 ; 91,31] |
| raisonnement seul | Twin | **53,54 %** | [44,98 ; 61,71] |
| format de persona seul (texte vs JSON, même modèle) | Twin | **48,74 %** | [39,82 ; 57,47] |
| modèle seul (GPT-4.1-mini vs Gemini-Flash-2.5) | Twin | **45,85 %** | [38,98 ; 53,02] |
| — | | | |
| persona seul (B↔P) | à nous | **2,46 %** | [0,50 ; 4,75] |
| tout différent (B↔C) | à nous | **2,56 %** | [0,65 ; 4,87] |
| gabarit seul (B↔G) | à nous | **0,94 %** | [0,00 ; 2,40] |
| modèle seul (B↔M) | à nous | **0,54 %** | [0,00 ; 1,50] |
| hasard (1/120) | | 0,83 % | |

La mesure A est **reproductible** : nos B↔M/G/P (0,54 / 0,94 / 2,46 %) retrouvent les
valeurs publiées (0,67 / 0,83 / 2,65 %) aux aléas de graine de départage près. Rien n'est
faux dans son calcul.

Mettre les deux séries à la même échelle **creuse l'écart au lieu de le combler** : à pool
120, B monte de 15–19 % à 45,85 % pour le seul changement de modèle, contre 0,54 % pour A.
La taille du bassin, la base de comparaison, le nombre d'items et le sens de l'attaque sont
maintenant identiques. **Il ne reste qu'une différence : les jumeaux eux-mêmes.**

## 3. Le témoin qui n'avait pas été interrogé : les jumeaux de A ne portent aucune personne

Question jamais posée dans la chaîne A : **ses jumeaux retrouvent-ils la vraie personne ?**
Même pool de 120 humains réels (vague 4), mêmes 60 items.

| jumeau | top-1 contre les humains réels (pool 120) | IC 95 % |
|---|---|---|
| **B** (deepseek, persona JSON) | **0,79 %** | [0,00 ; 2,17] |
| **C** (qwen, persona narrative) | **0,29 %** | [0,00 ; 0,87] |
| **M** (qwen, prompt de B) | **0,29 %** | [0,00 ; 0,87] |
| **G** (gabarit C sur JSON) | **0,00 %** | [0,00 ; 0,00] |
| **P** (gabarit B sur narrative) | **0,54 %** | [0,00 ; 1,62] |
| *hasard* | *0,83 %* | |
| Demographics Only (14 champs démographiques seulement) | 13,29 % | [7,50 ; 19,79] |
| Text Persona - GPT4.1-mini | 21,25 % | [14,46 ; 28,79] |
| JSON Persona - GPT4.1 | 38,92 % | [30,96 ; 47,08] |

**Les cinq jumeaux de la chaîne A sont au taux du hasard, ou en dessous.** Un jumeau de
l'équipe Twin qui ne connaît que quatorze champs démographiques (Demographics Only)
réidentifie la bonne personne 13,3 % du temps ; nos jumeaux, qui reçoivent **494 items de
contexte** de la même personne, la réidentifient 0,0 à 0,8 % du temps — c'est-à-dire jamais.

La décomposition de l'accord le confirme, et va plus loin :

| paire | accord au vrai jumeau | à un inconnu du même segment | **apport individuel** |
|---|---|---|---|
| B↔M | 51,1 % | 51,1 % | **−0,0 pts** |
| B↔G | 53,1 % | 50,3 % | +2,8 pts |
| B↔P | 52,5 % | 49,4 % | +3,1 pts |
| B↔C | 54,2 % | 52,0 % | +2,2 pts |
| Twin, décodage seul | 83,7 % | 54,5 % | **+29,3 pts** |
| Twin, gabarit seul | 78,7 % | 52,6 % | **+26,0 pts** |
| Twin, modèle seul | 58,1 % | 41,0 % | **+17,2 pts** |

Pour B↔M, l'apport individuel est **exactement nul** : deux modèles recevant le prompt
identique de la même personne ne partagent rien de cette personne. Les 120 vecteurs de
réponses sont pourtant tous distincts (120/120) et l'accord entre personnes différentes est
normal (0,507, comparable aux 0,556 de Twin) : le générateur n'est pas dégénéré au sens
d'une réponse constante. Il produit de la variation — mais cette variation est du **bruit
d'item et de décodage, pas de la personne**.

## 4. Verdict

**Aucune des deux séries n'est fausse au sens du calcul. C'est l'interprétation de A qui
l'est, et elle l'est entièrement.**

La mesure A a été lue comme « changer un seul élément du pipeline effondre le canal presque
autant que changer les trois ». Cette lecture suppose qu'un canal existait dans la
configuration de départ. **Il n'y en avait pas.** Le pipeline B ne transporte aucune
information individuelle avant qu'on change quoi que ce soit : ses contrastes B↔M, B↔G, B↔P
comparent deux sources de bruit, et un contraste entre deux bruits vaut le hasard quelle que
soit la variable manipulée. Les trois conditions atterrissent à 0,54–2,46 % pour un hasard
de 0,83 % parce que c'est le hasard — pas parce que le canal s'est effondré.

Le témoin manquant est celui-là, et il coûtait zéro dollar : **B contre les humains réels**,
qui aurait dû être exigé avant le premier appel payant. La mesure A n'a pas mesuré la
fragilité du canal ; elle a mesuré un générateur qui ne fonctionne pas, avec une précision
de 0,5 %.

La mesure B, elle, mesure un canal réel (apport individuel de 17 à 29 points, très au-dessus
du plancher entre inconnus). Mais elle reste **observationnelle** : sept configurations
d'une seule équipe, mêmes fichiers de persona, même harnais, fidélités individuelles
inégales (20,2 % à 38,9 % de top-1 contre les humains sur ce pool). Elle ne peut donc pas
répondre seule à la question du transfert **entre deux organisations indépendantes** : elle
décrit la distance entre deux configurations d'un même atelier.

**Conséquence collatérale à signaler** : le témoin « deux organisations » B↔C, sur lequel
repose la phrase « A7 est détruite » de `c7-deux-organisations-resultats.md`, utilise le
**même pipeline B** et est donc frappé par le même défaut. Son résultat (1,76 %) ne montre
pas qu'un canal inter-organisations n'existe pas ; il montre que ce dispositif-là n'a jamais
été capable d'en détecter un. Hors périmètre de cette note, mais bloquant pour l'article.

## 5. Quelle baseline s'applique à quelle série

La baseline démographique **dépend fortement du bassin**, et elle n'est pas comparable d'une
série à l'autre :

| baseline | bassin | valeur |
|---|---|---|
| Demographics Only → humains v4 | 2 058 | **2,13 %** (`c7-reidentification.csv`) |
| Demographics Only → humains v4 | 200 | **9,20 %** (`c7-deux-organisations`) |
| Demographics Only → humains v4 | 120 | **13,29 %** (recalculé ici : 13,25 %) |

Deux erreurs d'appariement sont à corriger :

- Le moonshot compare les paliers Twin (pool 2 058) à la baseline **9,2 %**, qui est celle
  d'un pool de 200. La baseline applicable à ses chiffres est **2,13 %** — ce qui *renforce*
  sa conclusion (45,9 % contre 2,1 %, pas contre 9,2 %).
- Le factoriel compare un top-1 **jumeau↔jumeau** à une baseline **jumeau→humain**
  (13,29 %). La baseline homogène, jumeau↔jumeau au même pool de 120, est bien plus haute :
  Demographics Only ↔ Text Persona = **23,69 %**, Demographics Only ↔ JSON Persona 4.1 =
  **34,42 %**. Utiliser 13,29 % a donc *avantagé* les conditions M/G/P, sans les sauver.

Dans les deux cas la correction de baseline ne change pas le sens de la conclusion. Ce qui
la change, c'est la fidélité des jumeaux (§3).

## 6. Phrase exacte que l'article a le droit d'écrire sur cette question

> Sur les jumeaux publiés par une même équipe (Twin-2K-500, sept configurations partageant
> les mêmes fichiers de persona et le même harnais), le canal jumeau-contre-jumeau s'atténue
> par paliers selon ce qui change dans le pipeline, mais ne s'éteint pas : à échantillon,
> bassin et items strictement identiques (120 personnes, bassin de 120, 60 items communs,
> attaque symétrique), le top-1 de ré-identification vaut 93,3 % [89,3 ; 96,8] quand seul le
> décodage change, 87,1 % [82,4 ; 91,3] pour le seul gabarit, 53,5 % [45,0 ; 61,7] pour le
> seul raisonnement, 48,7 % [39,8 ; 57,5] pour le seul format de persona et 45,9 %
> [39,0 ; 53,0] pour le seul modèle — contre 13,3 % [7,5 ; 19,8] pour un adversaire qui ne
> connaît que la démographie de la cible. Ces cinq paliers sont observationnels : ils
> mesurent la distance entre deux configurations d'un même atelier, non le transfert entre
> deux organisations indépendantes. Notre plan factoriel randomisé (n = 120, modèle, gabarit
> ou format de persona changés un à la fois) ne permet pas de trancher cette seconde
> question : les jumeaux qu'il génère ne réidentifient la personne réelle qu'au taux du
> hasard (top-1 de 0,0 % à 0,8 % contre 0,83 % attendu par hasard, là où les jumeaux
> Twin atteignent 20,2 % à 38,9 % sur le même bassin), de sorte que ses trois contrastes
> comparent deux sources de bruit et non deux jumeaux porteurs d'une personne. L'effet d'un
> changement isolé de pipeline sur des jumeaux réellement fidèles à la personne reste donc
> non mesuré, et la question reste ouverte.

## 7. Ce qu'il faudrait pour la refermer

Un bras randomisé n'est interprétable qu'après un **contrôle de fidélité préalable et
gratuit** : tout pipeline candidat doit d'abord dépasser nettement la baseline
Demographics Only (≈ 13 % à pool 120) en top-1 contre les humains réels, **avant** le
premier appel payant sur le contraste. Le pipeline B n'aurait pas passé ce filtre. Tant
qu'aucun pipeline régénéré ne le passe, les contrastes randomisés de la chaîne A (y compris
B↔C) ne peuvent porter aucune conclusion, ni positive ni négative.

## 8. Limites de cette note

- Les paliers Twin sont recalculés ici sur 120 personnes seulement (pour être comparables à
  A) : leurs IC sont donc plus larges que les valeurs publiées à 2 058, et les 120 personnes
  sont les 120 premiers index du tirage stratifié de 200, pas un re-tirage propre.
- Le palier « format de persona seul » (texte vs JSON, même modèle mini) repose sur 97
  personnes couvertes des deux côtés et sur les items communs de `JSON Persona - GPT4.1-mini`
  (48,5 items lus en moyenne sur ce pool, contre 60 pour les autres) : il est indicatif, pas
  au même niveau de preuve que les quatre autres.
- Cette note ne rejoue aucun appel payant et ne peut donc pas dire *pourquoi* le pipeline B
  échoue (persona de 494 champs ignorée, décalage de parsing, ou modèle qui répond par item
  sans lire le dossier). Elle établit seulement, et de manière dirimante, **qu'il échoue**.
