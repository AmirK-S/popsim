# Audit — le comparateur démographique de Twin-2K-500 : maigre par construction, ou réellement battu ?

statut: courant
mandat: Etablir depuis le code et les donnees sur quoi le comparateur demographique de Twin-2K-500 est conditionne, mesurer la fraction des 2 058 repondants seuls dans leur cellule demographique exacte et la comparer frontalement aux 98,86 % de Park, puis rejouer l'attaque A-LLR a bassin constant avec un comparateur ENRICHI d'autant d'attributs que Park en avait, pour trancher si le rapport de 29,88x s'effondre comme celui de Park ou tient.
agent: audit / Twin comparateur, 13/09
ecriture: analyses/c7_audit_twin_comparateur.py, resultats/audit-twin-comparateur-2026-09-13.md, resultats/c7-audit-twin-comparateur.csv
lecture_seule: tout le reste du depot
interdits: appel de modele paye, reseau, recherche web, arriere-plan, commit sur master, fusion, modification d'un script existant, toute ecriture dans article/manuscrit.md
cecite: Aucune verification reseau. Le paquet local `data/twin2k500` ne contient PAS les invites systeme par configuration : ce que recoit litteralement « Demographics Only - GPT4.1-mini » n'est donc pas verifiable ici, et le §1 le declare comme un angle mort nomme au lieu de le supposer. Les valeurs 23,2264 % / 0,7775 % / 29,88x / 98,86 % publiees par `audit-park-armement-egal-2026-09-13.md` ne servent qu'a la verification de raccordement ; aucune n'est recopiee dans un calcul.
cout_reel_usd: 0.00

---

> ## AVERTISSEMENT — POST HOC, NON PRÉENREGISTRÉ AU SENS DE C7
>
> Cet audit est déclenché **après** `audit-park-armement-egal-2026-09-13.md`, lui-même
> post-hoc. Le §0 ci-dessous fixe prédictions et critères de réfutation **avant le premier
> calcul**, mais pour une question **choisie après coup**. Il ne compte dans aucun
> dénominateur de multiplicité préenregistré et ne peut réfuter aucune prédiction
> préenregistrée d'origine.

---

## 0. PRÉENREGISTREMENT — écrit et commité avant le premier calcul

### 0.0 Ce que je savais déjà en écrivant ce préenregistrement

Déclaré pour que P2 ne soit pas lue comme une prédiction qu'elle n'est pas. **Avant**
d'écrire ce §0 j'ai lu `data/twin2k500/question_catalog_and_human_response_csv/question_catalog.json`
et compté les questions dont `BlockName` vaut `Demographics` : **quatorze**, `QID11` à
`QID24`. P2 est donc une **vérification de lecture**, pas une prédiction. Tout le reste du
§0 est écrit sans qu'aucun taux, aucune unicité et aucun rapport n'ait été calculé.

### 0.1 Conventions fixées d'avance

**Départage des ex æquo.** Convention reprise à l'identique de
`audit-park-armement-egal-2026-09-13.md` §0.1, pour que les deux audits soient comparables
chiffre à chiffre. Elle vaut **un facteur 1,32 sur Twin** sous l'attaque naïve et jusqu'à
130 ailleurs dans ce projet ; elle est donc fixée ici, avant tout calcul, et vaut pour
**toutes** les cellules, cible comme comparateurs :

- **Convention publiée, retenue pour tous les chiffres de tête** : espérance sous départage
  uniforme dans la classe d'ex æquo de tête, `1/|classe|` si la vraie personne est dans la
  classe de tête, 0 sinon. Calcul **exact et déterministe** (tolérance `1e-12`), jamais une
  moyenne de tirages.
- **Deux bornes encadrantes publiées à côté, pour chaque cellule** : `en_faveur` (compte dès
  que rien n'est strictement meilleur) et `contre` (compte seulement si la classe de tête
  est un singleton).

**Bassin strictement constant.** Un seul chargement de Twin. Mêmes personnes attaquées,
même pool de 2 058 candidats, mêmes colonnes d'items pour la cible et pour **chacun** des
comparateurs, enrichis compris. Conformité au chargeur canonique
`c7_fort_monde_ouvert_ic.charger_twin` vérifiée par assertion, arrêt si écart.

**Baseline.** Tout taux sort avec sa baseline recalculée dans **exactement** la condition où
elle sert : même bassin, mêmes items, même attaque, même convention de départage. Aucune
baseline n'est fournie en argument ni reprise d'un autre bassin.

**Contrôle d'interprétabilité** : `analyses/c7_controle_interpretabilite.py`, règle
inchangée — le candidat ne passe que si la borne basse de son IC est **strictement**
supérieure à la borne haute de l'IC du comparateur, les deux sous la **même** attaque et le
**même** bassin. Appliqué avant toute interprétation, contre **le comparateur le plus fort**,
pas contre le plus commode.

**Intervalles.** Bootstrap 2 000 sur les **personnes**, graine `20260913`. Pour les rapports
cible/comparateur : bootstrap **apparié**, les mêmes personnes rééchantillonnées
simultanément des deux côtés, 2 000 tirages.

**Aucune donnée individuelle** n'est calculée, imprimée ni écrite : ni identifiant, ni
appariement, ni cellule démographique d'une personne. Seuls des agrégats sortent.

### 0.2 Ce qu'« enrichir le comparateur » veut dire, fixé avant de mesurer

Le comparateur de Park est un **agent de langage** conditionné sur onze attributs. Twin ne
peut pas être traité de la même façon : rejouer un agent de langage coûterait un appel payé,
qui est interdit. Le comparateur enrichi est donc construit **sans modèle de langage**, à
partir des seuls attributs que le jeu offre à quiconque le télécharge, par la recette déjà
canonique du dépôt (`c7_monde_ouvert.pmm_depuis_demo`, plus proches voisins sur les
attributs, la personne elle-même exclue). C'est un **choix conservateur pour nous** : un
comparateur qui recopie les réponses réelles d'humains démographiquement voisins est au
moins aussi fort qu'un agent de langage nourri des mêmes attributs. Trois familles sont
construites, toutes sur le **même** bassin :

| famille | conditionnement | rôle |
|---|---|---|
| **D0** | le `Demographics Only - GPT4.1-mini` publié par l'équipe Twin | le comparateur actuel de l'article |
| **Dm** | voisins sur les **m premiers attributs démographiques**, m = 4, 8, 11, 14 | la montée en armement, m = 11 est l'égalité stricte avec Park |
| **D14+ctx** | voisins sur les 14 attributs **plus** les items de contexte des vagues 1-3 | la borne haute : tout ce que le jeu offre légitimement |

La **convention de départage, le bassin et l'attaque sont identiques** pour les trois.

### 0.3 Prédictions et critères de réfutation

| # | Prédiction (avant calcul) | Ce qui la réfute |
|---|---|---|
| **P1** | Je reproduis, indépendamment, le top-1 monde fermé de Twin à armement égal : cible **23,2264 % ± 0,50 pt**, comparateur `Demographics Only` **0,7775 % ± 0,20 pt**, rapport **29,88× ± 2,00**. | Un écart au-delà de ces tolérances. **Si P1 est réfutée je m'arrête là**, le livrable est cette non-reproduction, et je ne conclus rien d'autre. |
| **P2** | *(vérification, cf. §0.0)* Le bloc démographique disponible de Twin compte **quatorze** attributs, soit **plus** que les onze de Park, et couvre idéologie politique, parti, région, revenu, éducation, race, genre et âge. | Un compte différent de 14, ou l'absence d'idéologie ou de parti. Alors la thèse « Twin est maigre là où Park est riche » est vraie et l'article est en danger immédiat. |
| **P3** | La fraction des 2 058 répondants **seuls dans leur cellule démographique exacte** sur les quatorze attributs est **supérieure à 90 %**, donc du même ordre que les **98,86 %** de Park. Autrement dit : le bloc de quasi-identifiants **n'est pas** ce qui sépare les deux jeux. | Moins de **50 %**. Alors Twin est bien structurellement différent de Park, le comparateur y est maigre par construction, et le 29,88× est flatteur pour cette raison-là — ce qui est exactement le risque que cet audit cherche. |
| **P4** | **La question qui décide.** Comparateur enrichi à **onze attributs ou plus**, armé d'A-LLR, bassin constant : le rapport cible/comparateur sur Twin **reste au-dessus de 5,0×**. | Le rapport tombe **sous 5,0×**. |
| **P5** | Le meilleur comparateur enrichi reste **sous 5 %** de top-1 en monde fermé, là où celui de Park atteint 85,17 %. | Au-dessus de 5 %. |
| **P6** | *(l'inverse, pour être complet)* Le comparateur actuel de Twin n'est **pas** trop riche : il ne reçoit aucune réponse de vague 4 et son taux armé ne dépasse pas celui du meilleur comparateur enrichi. | `Demographics Only` **dépasse** tous les comparateurs enrichis. Alors il reçoit plus que des démographies, notre 29,88× est **conservateur**, et il faut le dire. |

### 0.4 Le seuil d'effondrement, déclaré avant de calculer

C'est la ligne que le mandat exige et c'est la seule qui décide :

- **rapport ≥ 5,0×** — Twin tient. La chute de Park n'est pas un défaut de notre méthode,
  c'est une propriété du jeu Park, et nous l'avons établi en **tentant** de reproduire la
  chute sur l'autre jeu et en échouant. C'est un argument plus fort qu'aujourd'hui.
- **2,0× ≤ rapport < 5,0×** — Twin est **entamé**. L'article doit publier le rapport réduit,
  pas le 29,88×, et dire dans la même phrase qu'un comparateur mieux armé le divise.
- **rapport < 2,0×** — **effondrement**. Twin ne vaut pas mieux que Park (qui tombe à
  1,06×). L'article perd son dernier jeu porteur et **doit l'écrire**. Aucune reformulation
  ne sauve la démonstration dans ce cas.

### 0.5 Règle d'arrêt et interdiction de conclure en faveur de l'article

Si P1 est réfutée, l'audit s'arrête au §1, sans tableau et sans interprétation.

**Aucune conclusion en faveur de l'article par défaut.** Si le rapport enrichi tombe sous
5,0×, le chiffre publié devient le rapport enrichi, jamais le 29,88×, et le §0.4 s'applique à
la lettre. Le comparateur retenu pour le rapport de tête est **le plus fort des comparateurs
mesurés**, pas le plus commode. Cinq conclusions ont été retirées dans la nuit du 12 au 13,
dont quatre flatteuses ; une sixième ne coûte rien.

### 0.6 Formulations interdites respectées

Les treize interdictions de `resultats/marqueurs-canoniques-2026-09-13.md` §3 (I1 à I12)
s'appliquent à ce rapport. Aucune n'est employée, ni en assertion ni en citation non
indentée.
