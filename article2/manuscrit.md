# Squelette du second article — SANS CORPS DE TEXTE

> **Statut : squelette seulement.** Le corps n'est pas écrit et ne doit pas l'être tant que le
> protocole de recensement (`resultats/papier2-cadrage-2026-09-12.md`, § 3) n'a pas été exécuté et
> son résultat N obtenu. Chaque section ci-dessous indique **ce qu'elle affirmera** et **avec quelle
> preuve**. Les cases marquées `[N]`, `[N_bloqués]`, `[τ]` sont des emplacements : elles ne
> contiennent aucun chiffre aujourd'hui et ne doivent pas être remplies par extrapolation.
>
> **Rappel de discipline** (cf. § 0 du cadrage) : le seul chiffre constaté à ce jour est **trois**
> jeux vérifiés à la source. L'estimation « 4 à 8 » est un jugement d'expert de
> `resultats/pistes-jeux-apparies-2026-09-12.md`, pas un résultat, et n'a pas sa place dans le
> texte. Aucune lettre n'a été envoyée à aucune équipe.

---

## Titre

**Proposé :** *Auditable Digital Twins Are Rarer Than Digital Twins: A Census of Individually
Paired Human–LLM Survey Datasets*

**Variante plus sobre, à préférer si N est plus grand qu'attendu :** *Who Can Check? Redistribution
of Individually Paired Human–LLM Survey Data, 2022–2026*

Le titre ne doit contenir **aucun nombre** : un nombre dans le titre d'un recensement dont le
protocole autorise la révision est une promesse qu'on ne peut pas tenir.

---

## Résumé (à écrire en dernier)

Structure imposée, 6 phrases, une par élément :
1. La méthode — générer par modèle de langage une réponse par répondant humain réel, sur items à
   choix fermé — est en diffusion.
2. Vérifier ce que ces sorties révèlent des personnes exige le **fichier apparié ligne à ligne**.
3. Nous définissons quatre critères vérifiables à la source et un protocole de recensement
   reproductible, préenregistré avec ses seuils de réfutation.
4. Résultat : `[N]` jeux qualifient à la date de clôture ; `[N_bloqués]` autres possèdent
   l'appariement mais ne sont pas redistribuables.
5. Nous classons les causes de blocage en quatre types et montrons qu'elles appellent des remèdes
   différents.
6. Conséquence : le risque se crée à un rythme, sa vérification par un tiers à un autre — et un
   contre-exemple sous CC0 montre que l'écart n'est pas technique.

**Interdit dans le résumé :** tout verbe de reproche, toute revendication de vide bibliographique,
toute mention d'un refus qui n'a pas eu lieu.

---

## 1. Introduction

**Affirme :** qu'il existe un décalage entre la diffusion d'une méthode et la disponibilité des
données qui permettraient de l'auditer ; que ce décalage a une conséquence précise et non
rhétorique — un tiers ne peut ni reproduire ni réfuter une attaque de liaison sur ces jeux.

**Preuve :** aucune preuve nouvelle ici ; l'introduction pose la question et annonce le protocole.
Elle cite les trois jeux vérifiés comme existence, et la disqualification d'OSF `f7na8` comme
illustration que le critère décisif n'est pas lisible dans un résumé d'article.

**Piège à éviter :** ouvrir sur l'alarme. Le texte doit ouvrir sur la **définition** (qu'est-ce
qu'un fichier apparié auditable) ; l'alarme, si elle est méritée, viendra du tableau.

---

## 2. Ce qu'il faut pour auditer, et pourquoi c'est étroit

**Affirme :** que la vérification par un tiers d'une attaque de liaison sur jumeaux exige quatre
propriétés conjointes — humains réels identifiés (C1), sorties de modèle appariées **ligne à ligne
par identifiant commun** aux mêmes personnes (C2), réponses à choix fermé (C3), redistribution
autorisée sans démarche et sous licence explicite (C4) — et que C2 et C4 sont les deux contraintes
mordantes.

**Preuve :**
- pour C2, le **format positif** : en-tête réel de `anesgpt3_task3.csv` (Argyle et al., Dataverse
  `10.7910/DVN/JPV20K`), où `V160001_orig` est l'identifiant de cas ANES et chaque variable réelle
  a sa colonne jumelle `_gpt3` **sur la même ligne** — constaté par lecture directe du fichier
  (`resultats/chasse-jeux-apparies-2026-09-12.md`) ;
- pour C2, le **contre-format** : `06_match_prolific_tess.R` d'OSF `f7na8`, qui joint sur
  `race_recode`, `educ_recode`, `age_recode` (+ parti) puis **tire au hasard** une correspondance —
  appariement par cellule démographique, pas par identité, qui **ne qualifie pas**
  (`resultats/troisieme-jeu-2026-09-12.md`) ;
- pour C4, le cas OSF `t6g7k` : `node_license: null` relevé via l'API OSF, et conditions NORC du
  GSS sous-jacent interdisant la reproduction sans consentement écrit
  (`resultats/licences-sources-verification-2026-09-11.md`, § 1-2). Même régime de licence absente
  relevé sur OSF `hnq7j` (Moore-Berg) et OSF `f7na8`.

**C'est la section la plus réutilisable du papier** : elle survit même si le décompte est réfuté.

---

## 3. Protocole de recensement

**Affirme :** que le décompte est reproductible par un tiers.

**Preuve :** le protocole lui-même, publié intégralement — quatre familles de sources avec requêtes
littérales, fenêtre du 1er juin 2022 à la date de clôture, trois étages (capture / tamisage /
vérification à la source avec citation probante), double codage avec taux de désaccord `[τ]` publié
et arbitrages motivés. Reprend `resultats/papier2-cadrage-2026-09-12.md`, § 3, sans y ajouter.

**Doit contenir explicitement :** la date de clôture ; le préenregistrement du protocole **et de
ses seuils de réfutation** avant exécution ; la règle qu'aucune ressource découverte après la
clôture n'entre dans le décompte principal.

**À ne pas faire :** décrire le protocole après coup en le calquant sur ce qui a été trouvé. S'il
n'est pas préenregistré, cette section est une reconstruction et le papier ne vaut rien.

---

## 4. Résultats du recensement

**Affirmera :** `[N]` jeux satisfont les quatre critères à la date de clôture.

**Preuve :** le registre publié — une ligne par ressource examinée à l'étage 3, avec URL, date de
consultation, verdict par critère, **citation probante**, et cause de blocage le cas échéant. Le
tableau du papier est un extrait du registre, pas l'inverse.

**Acquis aujourd'hui (plancher, à confirmer par le protocole) :** trois jeux vérifiés à la source —
Twin-2K-500 (Hugging Face, CC BY 4.0, 2 058 personnes), OSF `t6g7k` / Park et al. (1 052 personnes,
**licence non déclarée** : qualifie sur C1–C3, échoue sur C4), et Dataverse `10.7910/DVN/JPV20K` /
Argyle et al. (CC0, appariement confirmé par lecture de l'en-tête).

**Doit rapporter aussi :** les nombres de chaque étage (bruts capturés → survivants du tamisage →
vérifiés), sans quoi `[N]` est un chiffre sans dénominateur.

---

## 5. Typologie des blocages

**Affirmera :** que les jeux qui possèdent l'appariement mais ne sont pas redistribuables échouent
pour **quatre raisons distinctes**, qui n'appellent pas le même remède :

| type | cas documenté | remède correspondant |
|---|---|---|
| choix éditorial de l'équipe | Wang, Hunt, Tang & Joseph — `.gitignore` excluant explicitement les « respondent-level raw data », code et agrégats seuls déposés | norme de dépôt sous accès contrôlé plutôt qu'exclusion pure |
| absence de déclaration | Choi, Kim, Pugalenthi, Chen & Huang — aucune section « Data Availability », aucun dépôt, après lecture intégrale des 11 pages | exigence éditoriale d'un *data availability statement* |
| interdiction de la source humaine | Kinzinger & Hartmann — SOEP à accès contrôlé, « Individuals (without an institutional affiliation) are not permitted to use the SOEP data » | négociation au niveau du fournisseur de panel, pas de l'équipe |
| licence absente sur dépôt public | OSF `t6g7k`, `hnq7j`, `f7na8` — `node_license: null` relevé par API | champ licence obligatoire à la publication du dépôt |

**Preuve :** pour les trois premiers, `resultats/pistes-jeux-apparies-2026-09-12.md` (appariement
confirmé par les statistiques individuelles publiées : ρ_S pour Wang et al., r_d/MAE_d pour Choi
et al., corrélation de rang par item pour Kinzinger & Hartmann — chacune arithmétiquement
impossible sans fichier apparié interne). Pour le quatrième, les relevés d'API cités en § 2.

**Un cinquième cas de figure, à traiter séparément et non comme un blocage :** Westwood (OSF
`ektqr`) publie 27 923 réponses **synthétiques** sans aucun humain apparié — l'inverse du problème,
documenté par sa propre provenance (`resultats/inventaire-donnees-2026-09-12.md`).

**C'est probablement la contribution la plus durable du papier** : elle ne dépend pas de `[N]` et
ne vieillit pas au même rythme.

---

## 6. Le contre-exemple : ce n'est pas un obstacle technique

**Affirmera :** qu'une équipe a déposé un fichier apparié à choix fermé, sous **CC0**,
téléchargeable sans compte, depuis décembre 2022 — donc que la non-redistribution relève de la
norme et de la contrainte de source, non de l'impossibilité.

**Preuve :** Argyle, Busby, Fulda, Gubler, Rytting & Wingate (2023), Dataverse
`10.7910/DVN/JPV20K` ; licence CC0 confirmée dans le champ `license` de l'API Dataverse ; accès
direct sans inscription ; appariement constaté par lecture de l'en-tête
(`resultats/chasse-jeux-apparies-2026-09-12.md`).

**Réserve à écrire telle quelle :** la clause de redistribution propre à l'ANES pour les variables
publiques utilisées n'a pas été vérifiée à la source primaire ; seul le fait général que les
fichiers de diffusion publique de l'ANES sont libres d'accès l'a été. Cette réserve figure déjà
dans le rapport ; elle doit figurer dans le papier.

---

## 7. Ce que le constat ne dit pas

**Affirmera :** les bornes, énoncées avant qu'un relecteur ne les trouve.
- Le recensement porte sur ce qui est **repérable par un protocole public et redistribuable**, pas
  sur ce qui **existe** : des fichiers appariés existent certainement en plus grand nombre en
  interne et chez les panélistes commerciaux — c'est le propos, pas une lacune.
- Aucune mesure de risque n'est produite ici ; la mesure est ailleurs (premier papier, deux jeux).
- Le papier ne plaide pas pour l'ouverture : publier un fichier apparié est aussi ce qui rend
  l'attaque possible. Les deux bouts doivent être tenus dans la même section.
- Les causes de non-publication ne sont pas des fautes : le SOEP protège des personnes, l'exclusion
  du `respondent-level` est une précaution.

**Preuve :** aucune — c'est une section de bornes, et elle doit le rester.

---

## 8. Conflit d'intérêts et genèse

**Affirmera, en clair et sans atténuation :** l'observation est née d'un échec — nous cherchions un
troisième jeu pour notre propre travail de mesure et ne l'avons pas trouvé ; notre base empirique
est de deux jeux, dont un sans licence déclarée ; nous avons donc un intérêt à ce que la rareté
soit établie.

**Ce qui doit y figurer, factuellement :** trois demandes ont été **rédigées** (Wang/Buffalo,
Choi/USC, Kinzinger/TUM) ; leur statut réel à la date de soumission est rapporté tel quel. À la
date de ce squelette, **aucune n'a été envoyée** (`resultats/demandes-etat-2026-09-12.md`). Le
papier ne doit en aucun cas laisser entendre qu'un refus a été opposé.

**La réponse à l'objection, et elle seule tient :** le protocole préenregistré, les requêtes
littérales, les seuils de réfutation écrits avant le comptage, le double codage et son taux de
désaccord. Un constat reproductible n'a pas besoin que son auteur soit désintéressé. Le
développement complet est en § 5 de `resultats/papier2-cadrage-2026-09-12.md`.

---

## 9. Conditions de réfutation

**Affirmera :** ce qui ferait tomber la thèse, énoncé avant le comptage et préenregistré avec le
protocole. Reprend intégralement le tableau R1–R6 du cadrage :
- R1 — plus de 15 jeux qualifiants : **la thèse tombe** ;
- R2 — entre 9 et 15 : insuffisant pour un article séparé ;
- R3 — un tiers obtient un compte différant de plus de 30 % : protocole non reproductible ;
- R4 — les fichiers sont fournis sur simple demande dans un délai raisonnable : friction, pas
  pénurie ;
- R5 — un registre équivalent existe déjà : contribution redondante ;
- R6 — le critère « choix fermé » n'est pas décisif pour l'attaque : le dénominateur change.

**Preuve :** le préenregistrement horodaté lui-même.

---

## Annexes

- **A. Registre complet** (fichier séparé, déposé avec DOI) : une ligne par ressource examinée à
  l'étage 3.
- **B. Requêtes littérales et dates d'exécution**, par source.
- **C. Désaccords de codage et arbitrages**, avec motifs.
- **D. Extraits probants** : en-têtes de fichiers, champs de licence, extraits de `.gitignore` et de
  pages d'accès, cités verbatim avec date de consultation.

---

## Journal des décisions de rédaction

- **12/09/2026** — squelette créé. Corps volontairement non écrit : le recensement n'est pas fait.
- **12/09/2026** — aucun chiffre inséré hors des trois jeux vérifiés à la source ; « 4 à 8 » écarté
  du texte comme estimation non bornée.
- **12/09/2026** — décompte « trois équipes possèdent et ne publient pas » corrigé en deux (Wang,
  Choi) + une empêchée par sa source (Kinzinger) + un cas inverse (Westwood).
- **12/09/2026** — recommandation en vigueur (cadrage, § 6) : **ne pas lancer cet article
  maintenant**. Publier d'abord le registre et intégrer le constat au premier papier ; ne décider
  d'un texte séparé qu'après exécution du protocole et seulement si N ≤ 8.
