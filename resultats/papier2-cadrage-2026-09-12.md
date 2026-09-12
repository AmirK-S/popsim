# Second papier — cadrage, lieu, protocole de recensement, conflit d'intérêts (12 septembre 2026)

statut: courant
mandat: cadrer un éventuel second article sur l'auditabilité des jeux appariés, et dire franchement s'il mérite d'exister
agent: Opus 5, Anthropic
ecriture: resultats/papier2-cadrage-2026-09-12.md
lecture_seule: tout le reste
interdits: appel payant sans GO, réseau, commit sur master, arrière-plan
cecite: n'a pas exécuté le protocole de recensement (§ 3) ; ne voit que les six rapports cités ci-dessous, aucune vérification nouvelle à la source
cout_reel_usd: 0.00

Écrit à partir de `resultats/chasse-jeux-apparies-2026-09-12.md`,
`resultats/pistes-jeux-apparies-2026-09-12.md`, `resultats/inventaire-donnees-2026-09-12.md`,
`resultats/troisieme-jeu-2026-09-12.md`, `resultats/positionnement-vie-privee-2026-09-12.md`,
`resultats/licences-sources-verification-2026-09-11.md` et `resultats/demandes-etat-2026-09-12.md`.
Aucun appel payant, aucune recherche web, aucun chiffre nouveau : tout ce qui est chiffré ici
remonte à l'un de ces rapports, et la provenance est donnée à chaque fois.

---

## 0. Trois corrections de fait à faire avant d'écrire quoi que ce soit

Elles ne sont pas cosmétiques : deux d'entre elles changent ce que le papier a le droit d'affirmer.

**0.1 — « 4 à 8 jeux au monde » n'est pas un résultat, c'est une estimation de fin de rapport.**
La formule exacte de `pistes-jeux-apparies-2026-09-12.md` (§ Récapitulatif) est : « **mon estimation
honnête** est qu'il n'existe aujourd'hui probablement qu'une poignée de jeux au monde (single digits,
sans doute 4 à 8) ». C'est un jugement d'expert formé après deux passes de recherche de quelques
heures, explicitement présenté comme tel par son auteur. Le seul chiffre **constaté** est le
plancher : **trois** jeux vérifiés à la source comme immédiatement téléchargeables et appariés
(Twin-2K-500, OSF `t6g7k`, Dataverse `10.7910/DVN/JPV20K`). Il n'existe aujourd'hui **aucune borne
supérieure établie**. Écrire « 4 à 8 » dans un article sans avoir exécuté le protocole de la
section 3 serait exactement la faute qui a produit les quatre rétractations du premier papier :
une conclusion séduisante écrite avant vérification. Tant que le recensement n'est pas fait, la
seule formulation autorisée est : « au moins trois, vérifiés à la source ; la borne haute est
inconnue ».

**0.2 — Aucune lettre n'a été envoyée à aucune équipe.**
`resultats/demandes-etat-2026-09-12.md` § 3 : « Toute décision d'envoi elle-même : rien n'a été
transmis. » Les lettres 13 (Wang et al., Buffalo), 14 (Choi et al., USC) et 15 (Kinzinger, TUM)
existent à l'état de brouillons avec adresses vérifiées ; elles ne sont pas parties.
`resultats/revue-popets-simulee-2026-09-12.md` (E1) et `resultats/conformite-popets-2026-09-12.md`
(§ 8) confirment le même état pour les lettres de divulgation du premier papier. **Nous ne pouvons
donc pas écrire que nous avons demandé ces données et qu'on nous les a refusées.** Cette
formulation, qui est celle de la commande, serait fausse — et c'est précisément le type de
phrase qu'un relecteur peut vérifier et qui détruirait la crédibilité de tout le reste.

**0.3 — Le décompte « trois équipes possèdent et ne publient pas, une quatrième ne le peut pas »
doit être reventilé.** Ce que les rapports établissent réellement, équipe par équipe :

| équipe | appariement individuel | pourquoi le fichier n'est pas public | source |
|---|---|---|---|
| Wang, Hunt, Tang & Joseph (Buffalo) | confirmé (ρ_S publié, Table F.1) | **choix éditorial** : le `.gitignore` du dépôt exclut explicitement les « respondent-level raw data » ; seuls code et agrégats sont déposés | `pistes-...` § Piste A |
| Choi, Kim, Pugalenthi, Chen & Huang (USC) | confirmé (r_d, MAE_d publiés) | **absence de déclaration** : aucune section « Data Availability », aucun dépôt trouvé après lecture intégrale des 11 pages | `pistes-...` § Piste B |
| Kinzinger & Hartmann (TUM) | confirmé (corrélation de rang par item) | **interdiction de la source** : le SOEP est à accès contrôlé (DIW Berlin), affiliation institutionnelle obligatoire — « Individuals (without an institutional affiliation) are not permitted to use the SOEP data » | `pistes-...` § Kinzinger ; `demandes-etat-...` § 4 |
| Westwood (Dartmouth) | **non** — c'est l'inverse : 27 923 réponses synthétiques, aucun humain apparié | sans objet ; le fichier humain apparié, s'il existe, n'est pas déposé | `inventaire-donnees-...` § 2 |

Donc : **deux** équipes détiennent un fichier apparié et ne le déposent pas (Wang, Choi), **une**
troisième est empêchée par sa source (Kinzinger/SOEP), et Westwood est un quatrième cas de figure
distinct (moitié synthétique publiée, moitié humaine absente). C'est moins net que « trois
équipes le gardent », et plus intéressant : les causes de non-publication sont **hétérogènes**, et
cette hétérogénéité est le vrai contenu du papier.

**Ce qui est exact dans la commande, et vérifié :** l'archive la plus directement concernée par
notre premier papier, OSF `t6g7k` (Park et al., 1 052 personnes), a bien `node_license: null` —
aucune licence déclarée — et sa source sous-jacente, le GSS/NORC, interdit la reproduction sans
consentement écrit (`licences-sources-verification-2026-09-11.md` § 1 et § 2). Même régime
d'absence de licence pour OSF `hnq7j` (Moore-Berg) et OSF `f7na8` (Zhang, Xu & Alvero).

---

## 1. La thèse

### En une phrase

> Fabriquer des jumeaux numériques appariés à des répondants humains réels est devenu une méthode
> courante, mais les fichiers appariés qui permettraient à un tiers de vérifier ce que ces jumeaux
> révèlent de ces personnes sont, eux, presque jamais redistribuables — de sorte que le risque de
> vie privée se crée plus vite qu'il ne devient auditable.

### Ce qu'elle affirme

1. **Une asymétrie de rythme**, pas une accusation. La méthode (générer une réponse par personne
   réelle, sur des items à choix fermé) se diffuse : elle apparaît dans des équipes différentes,
   sur des populations différentes (ANES aux États-Unis, SOEP en Allemagne, une enquête Covid en
   Corée du Sud), avec des générateurs différents. La redistribution du fichier apparié ne suit pas.
2. **Que les causes de non-redistribution sont hétérogènes et cumulables** : choix éditorial de
   l'équipe (Wang et al.), simple absence de déclaration de disponibilité (Choi et al.), interdiction
   de la source humaine (SOEP, GSS/NORC), et absence de licence sur des archives pourtant publiques
   et citées (`t6g7k`, `hnq7j`, `f7na8`). Ces quatre mécanismes ne se soignent pas de la même façon.
3. **Que la conséquence est vérificationnelle, pas seulement pratique** : un tiers ne peut, sur ces
   jeux, ni reproduire une attaque de liaison, ni la réfuter. Notre premier papier en est
   l'illustration : sur deux jeux, dont l'un sans licence déclarée.
4. **Que le blocage n'est pas technique.** Argyle et al. (Dataverse `10.7910/DVN/JPV20K`) ont déposé
   un fichier apparié, à choix fermé, sous **CC0**, téléchargeable sans compte, avec l'identifiant
   ANES réel (`V160001_orig`) et les colonnes jumelles `_gpt3` sur la même ligne. Le contre-exemple
   existe, il est vérifié à la source, et il est publié depuis décembre 2022. Ce que fait une équipe,
   les autres le peuvent.

### Ce qu'elle n'affirme pas

- **Pas** que les équipes qui ne publient pas ont tort, ni qu'elles cachent quoi que ce soit. Le cas
  SOEP est une protection de vie privée légitime ; l'exclusion du `respondent-level` par Wang et al.
  est même une précaution défendable. Le papier décrit un état, pas une faute.
- **Pas** que le nombre de jeux est petit « au monde ». Le recensement porte sur ce qui est
  **redistribuable et repérable par un protocole public**, pas sur ce qui existe. Des fichiers
  appariés existent certainement en nombre supérieur, en interne, chez les équipes et chez les
  panélistes commerciaux. C'est justement le propos.
- **Pas** que le risque de vie privée est démontré sur ces jeux-là. La mesure est le sujet du
  premier papier, sur deux jeux ; le second papier ne remesure rien.
- **Pas** que l'ouverture des données est la solution. Publier des fichiers appariés est aussi ce
  qui rend l'attaque possible ; le papier doit tenir les deux bouts et ne pas se transformer en
  plaidoyer pour l'open data.
- **Pas** que nous avons sollicité et essuyé des refus (cf. § 0.2).

### Ce qui la réfuterait — les seuils, écrits avant le comptage

À fixer **avant** d'exécuter le protocole, et à préenregistrer avec lui. La thèse tombe, ou se
réduit à une remarque, si l'un de ces faits est établi :

| # | fait réfutant | conséquence |
|---|---|---|
| R1 | Le protocole de la § 3, exécuté intégralement, retourne **plus de 15 jeux** satisfaisant les quatre critères | **La thèse tombe.** « Presque jamais redistribuable » devient faux ; il ne reste qu'une note sur l'hétérogénéité des licences. |
| R2 | Le protocole retourne **entre 9 et 15 jeux** | La thèse est **affaiblie au point d'être insuffisante pour un article** : le corpus auditable est étroit mais pas rare. À replier en section du premier papier. |
| R3 | Un tiers exécutant le protocole publié obtient un compte **différant de plus de 30 %** du nôtre | Le protocole n'est pas reproductible : le résultat n'est pas défendable, quel que soit le chiffre. |
| R4 | Les équipes qui ne déposent pas fournissent le fichier **sur simple demande dans un délai raisonnable** (à tester réellement, cf. § 5) | Le point bascule : ce n'est plus une pénurie mais une friction administrative. Thèse fortement réduite, mais pas nulle (la vérification par un tiers anonyme reste impossible). |
| R5 | Il existe un registre, catalogue ou index déjà publié qui recense ces jeux | Notre contribution de recensement est redondante ; reste au mieux un commentaire. |
| R6 | Le critère « choix fermé » s'avère non décisif pour l'attaque (un jeu en texte libre serait tout aussi exploitable) | Le dénominateur change : le corpus auditable est plus large que compté. À trancher par un test sur `f7na8`, pas par argument. |

Aucun de ces six seuils n'est atteint aujourd'hui, mais aucun n'est écarté non plus : c'est
exactement pour cela que le corps de l'article ne peut pas être écrit maintenant.

---

## 2. Lieu et format — recommandation, avec sa justification et son coût

### Le format naturel n'est pas un article de mesure

Ce texte n'apporte aucune mesure nouvelle. Son contenu est : un critère d'inclusion, un protocole,
un décompte, une typologie des causes de blocage, et une liste vérifiable. La forme qui correspond
à ce contenu est une **note courte adossée à un registre versionné**, pas un article de recherche
de 12 pages. Concrètement : un texte de 4 à 6 pages + un dépôt (Zenodo ou OSF, DOI, licence
explicite) contenant le tableau de recensement ligne à ligne, chaque requête horodatée, chaque
verdict avec sa citation probante. Le registre est la contribution ; le texte l'explique.

### Ce que je recommande, par ordre

**Option A (recommandée aujourd'hui) — ne pas faire d'article séparé pour l'instant : publier le
registre, et intégrer le constat comme section du premier papier.**
Coût : nul. Risque de rejet : nul. Le premier papier a déjà besoin d'une section honnête sur les
limites de généralisation (il repose sur deux jeux, dont un sans licence déclarée) ; ce constat
**est** cette section, et il y est plus fort qu'isolé, parce qu'il y est adossé à une mesure réelle.
Le registre, lui, part immédiatement sur Zenodo avec un DOI citable : il rend service tout de suite,
il est falsifiable tout de suite, et il établit l'antériorité si nous voulons en faire un article
plus tard. Cette option est réversible ; l'inverse ne l'est pas.

**Option B (si et seulement si le recensement exécuté confirme un corpus étroit, c.-à-d. ≤ 8) —
note courte, soumise à un lieu déjà vérifié dans `positionnement-vie-privee-2026-09-12.md`.**
Je ne propose que des lieux dont les frais et le cycle sont **déjà établis dans ce dépôt** ; tout
autre candidat (revue de méta-recherche, *Scientific Data*, etc.) serait une supposition de ma part
et doit être vérifié avant d'être cité.

| lieu | pertinence pour ce texte | frais | remarque |
|---|---|---|---|
| **Journal of Privacy and Confidentiality** | **la meilleure des trois.** Le rapport de positionnement note lui-même que « sa culture éditoriale valorise la rigueur méthodologique et l'exhaustivité d'un résultat borné, honnêtement rapporté, davantage qu'un jury de conférence cherchant l'effet de nouveauté » — c'est la description exacte de ce texte | 500 USD à l'acceptation | au fil de l'eau, ~24 semaines ; le coût est un vrai obstacle à trancher par le responsable |
| *Transactions on Data Privacy* | repli diamant, gratuit | 0 | lectorat plus étroit ; à retenir si les 500 USD sont rédhibitoires |
| PoPETs | **à écarter pour ce texte.** C'est le lieu du **premier** papier (rang 1, dépôt 30 novembre 2026). Soumettre deux textes du même auteur au même cycle dilue le premier, et un constat de disponibilité de données n'est pas un papier PoPETs | 0 | garder PoPETs pour la mesure |
| Journal of Official Statistics | mauvais ajustement : ancrage statistique officiel, pas disponibilité de corpus IA | 0 | — |

**Ce que je déconseille explicitement :** viser PoPETs avec les deux textes au cycle 2027.3. Le
premier papier a déjà une contribution rétrécie deux fois (A7 borné puis retiré) et un taux
d'acceptation de 26 % ; lui adjoindre un second texte mince du même auteur au même moment est un
mauvais calcul.

---

## 3. Protocole de recensement — le cœur de la crédibilité

C'est ce qui transforme « nous avons cherché quelques heures et trouvé peu » en « voici un compte
qu'un tiers peut refaire ». Il doit être **préenregistré avec ses seuils de réfutation (§ 1) avant
d'être exécuté**, sinon le compte est pilotable.

### 3.1 Objet du recensement — la définition, avant tout

Est recensée toute **ressource** (dépôt, archive, jeu de données) satisfaisant **les quatre
critères**, chacun vérifié **à la source** et non déduit :

| critère | énoncé | preuve exigée |
|---|---|---|
| **C1 — humains réels** | contient les réponses de répondants humains identifiés individuellement | en-tête de fichier ou documentation citée verbatim |
| **C2 — appariement individuel** | contient, pour **les mêmes personnes**, des réponses produites par un modèle de langage, reliables **ligne à ligne** par un identifiant commun | l'en-tête réel du fichier, cité (modèle : `V160001_orig` + colonnes `_gpt3`, cf. `chasse-jeux-apparies`). Un appariement **par cellule démographique** ne qualifie pas — critère qui a disqualifié `f7na8` sur constat du code (`06_match_prolific_tess.R`, jointure sur race/éducation/âge puis tirage au hasard) |
| **C3 — choix fermé** | les réponses sont des codes, catégories ou échelles, pas du texte libre | inspection des valeurs (entiers, modalités), pas la description du papier |
| **C4 — redistribuable sans démarche** | téléchargeable par un tiers sans compte, sans demande, sans habilitation, **et** sous licence explicite permettant la redistribution | champ licence de l'API du dépôt, cité. `node_license: null` **ne qualifie pas** : par défaut, droits réservés |

Les deux derniers critères sont ceux qui font le décompte. Un jeu qui passe C1–C2–C3 mais échoue
C4 n'est pas exclu du papier : il est classé dans la **typologie des blocages** (§ 3.5), qui est la
seconde contribution et probablement la plus intéressante.

### 3.2 Fenêtre temporelle

Publications et dépôts entre le **1er juin 2022** (antériorité d'Argyle et al., premier travail
vérifié à produire un fichier apparié LLM/répondant réel) et la **date de clôture du recensement**,
qui doit être fixée, écrite, et non rouverte ensuite. Toute ressource découverte après la clôture
va dans un addendum daté du registre, jamais dans le décompte principal.

### 3.3 Sources à balayer — la liste est exhaustive et publiée, ou le compte ne vaut rien

Quatre familles, chacune avec ses requêtes littérales consignées :

1. **Préprints et littérature** : arXiv (cs.CL, cs.CY, cs.HC, cs.AI, stat.AP, econ.GN), plus un
   moteur bibliographique à graphe de citations (OpenAlex ou Semantic Scholar) **amorcé sur les
   trois jeux connus** — toutes les publications citant Argyle et al. 2023, Park et al. 2024 et
   Twin-2K-500 sont examinées. C'est le balayage qui donne le rappel : la méthode se diffuse par
   citation de ces trois travaux.
2. **Dépôts de données** : Hugging Face (`datasets`), OSF, Harvard Dataverse, Zenodo, ICPSR,
   figshare. Requêtes littérales à consigner (p. ex. `digital twin survey`, `simulated respondents`,
   `LLM respondents`, `silicon sampling`, `synthetic survey respondents`).
3. **Code** : GitHub, GitLab, `anonymous.4open.science` — pour repérer les cas Wang, où le code est
   public et la donnée exclue. C'est cette famille qui alimente la typologie des blocages.
4. **Littérature grise** : thèses (theses.fr, HAL, ProQuest), actes d'ateliers, et — puisque deux
   passes en anglais l'ont déjà explorée sans résultat — au moins deux langues non anglophones,
   avec les requêtes consignées telles quelles.

### 3.4 Procédure en trois étages, et la reproductibilité

- **Étage 1 — capture.** Chaque requête est exécutée à une date consignée ; le nombre de résultats
  bruts et la liste complète des identifiants capturés sont enregistrés, avant tout filtrage.
- **Étage 2 — tamisage sur titre/résumé.** Critère unique et volontairement large : « le travail
  produit-il, ou pourrait-il produire, des réponses de modèle appariées à des répondants réels
  nommés individuellement ? » En cas de doute, on garde. Chaque exclusion est motivée en une ligne.
- **Étage 3 — vérification à la source.** Pour chaque survivant : ouvrir le dépôt, lire l'en-tête
  réel du fichier, lire le champ licence via l'API du dépôt, et consigner **la citation probante**.
  C'est l'étage qui coûte cher et c'est le seul qui compte. Un jeu n'est **jamais** classé
  qualifiant sur la foi du texte de l'article : `pistes-jeux-apparies` montre trois travaux dont
  la méthode prouve l'existence d'un fichier apparié interne sans qu'il soit déposé nulle part.
- **Double codage.** Les étages 2 et 3 sont exécutés indépendamment par deux codeurs (ou deux
  sessions aveugles l'une à l'autre) ; le taux de désaccord est publié, les désaccords sont
  arbitrés et le motif d'arbitrage écrit. Sans ce chiffre, le compte n'est qu'un avis.
- **Trace.** Le registre publié contient une ligne par ressource examinée à l'étage 3 : nom, URL,
  date de consultation, verdict C1/C2/C3/C4, citation probante, cause de blocage le cas échéant.
  Un tiers refait le compte en rejouant les requêtes et en relisant les mêmes en-têtes.

### 3.5 Ce que produit le protocole

Deux sorties, pas une :
- **N**, le nombre de jeux qualifiants à la date de clôture, avec son intervalle de confiance
  qualitatif (les sources non balayées, les langues non couvertes, ce qui est derrière un paywall).
- **La typologie des blocages** pour les jeux qui échouent au seul C4 : choix éditorial / absence de
  déclaration / interdiction de la source / absence de licence sur dépôt public. C'est cette
  typologie, et non le nombre, qui dit quoi faire — et c'est elle qui survit même si N est plus
  grand qu'attendu.

### 3.6 Coût honnête

L'étage 3 est le poste lourd : ouvrir, télécharger un en-tête, interroger une API de licence, pour
chaque survivant. Sur la base des deux passes déjà faites (qui ont vérifié à la source une dizaine
de candidats en quelques heures), un recensement complet à deux codeurs est de l'ordre de plusieurs
jours-machine, sans appel payant. Ce n'est pas gratuit. C'est l'argument principal en faveur de
l'option A : ne payer ce coût que si le premier papier est déposé et que le registre a de la valeur
en soi.

---

## 4. Plan de l'article

Voir `article2/manuscrit.md` : titre, résumé, sections, et pour chacune ce qu'elle affirme et avec
quelle preuve. Le corps n'est pas écrit, le recensement n'étant pas fait.

---

## 5. « Vous êtes juge et partie » — la réponse

### L'objection, énoncée dans sa version la plus dure

« Vous avez cherché un troisième jeu pour votre propre papier, vous ne l'avez pas trouvé, vous avez
sollicité trois équipes, et vous érigez votre frustration en constat sur l'état du domaine. Votre
chiffre est bas parce que vous aviez intérêt à ce qu'il le soit : un corpus rare excuse le fait que
votre mesure ne repose que sur deux jeux. »

C'est une objection sérieuse et elle vise juste sur l'origine : l'observation **est** née d'un
échec de recherche de données pour notre propre papier. Nier la généalogie serait absurde.

### La réponse, en cinq points — dont un rectificatif

**5.1 — Rectifier d'abord le fait.** Nous n'avons **rien demandé à personne**. Les trois lettres
sont des brouillons non envoyés (§ 0.2). Nous ne pouvons donc pas dire « on nous a refusé », et
nous ne le dirons pas. Le papier écrira exactement : nous avons identifié ces trois équipes,
rédigé des demandes, et voici leur statut à la date de soumission. Paradoxalement, cela **réduit**
le conflit d'intérêts : nous ne sommes pas des demandeurs éconduits, nous sommes des lecteurs de
dépôts publics.

**5.2 — Rendre l'intérêt inopérant par la falsifiabilité, pas par la dénégation.** Toute la
section 3 existe pour cela : le protocole publié, les requêtes littérales, les critères écrits
avant le comptage, les seuils de réfutation (§ 1) préenregistrés, le double codage et son taux de
désaccord. Un critique qui pense le chiffre motivé n'a pas à nous croire : il rejoue les requêtes.
Un constat qu'on ne peut pas refaire est une impression ; un constat qu'on peut refaire n'a pas
besoin que son auteur soit désintéressé. **C'est la seule réponse qui tienne vraiment** ; les
quatre autres sont des précautions d'accompagnement.

**5.3 — La preuve est documentaire, pas évaluative.** Un champ `node_license` vaut `null` ou il ne
le vaut pas. Un `.gitignore` exclut `respondent-level raw data` ou il ne l'exclut pas. Une page du
DIW écrit que les chercheurs sans affiliation ne sont pas autorisés, ou elle ne l'écrit pas. Aucun
de ces faits ne passe par notre jugement, et chacun est vérifiable en une minute par un tiers. Le
seul endroit où notre jugement intervient est la **définition des critères** — donc c'est là qu'il
faut être le plus explicite, et c'est pourquoi C2 et C4 sont énoncés avec leur preuve exigée.

**5.4 — Publier le contre-exemple aussi fort que le constat.** Argyle et al. ont déposé un fichier
apparié sous CC0, sans compte, depuis décembre 2022. Un texte qui voudrait maximiser la plainte
enterrerait ce cas ; nous en faisons un point de la thèse (§ 1, affirmation 4). C'est la meilleure
démonstration que nous ne cherchons pas à établir « personne ne partage » : nous établissons
« c'est faisable, et ce n'est presque jamais fait ».

**5.5 — Déclarer le conflit en clair, dans le papier, à sa place.** Une section « Conflit
d'intérêts et genèse » : nous sommes une équipe qui a cherché ces données pour son propre travail
et ne les a pas trouvées ; nous avons deux jeux, dont un sans licence déclarée ; nous avons un
intérêt à ce que la rareté soit établie, puisqu'elle excuse l'étroitesse de notre base empirique.
Le déclarer ne neutralise pas l'intérêt, mais il enlève au relecteur le plaisir de le découvrir, et
il oblige le texte à rester dans le registre descriptif.

**5.6 — Et une manœuvre honnête qui renverserait l'objection : envoyer les trois lettres et
publier ce qui revient.** Aujourd'hui nous affirmons que les fichiers ne sont pas publics ; nous
n'avons pas testé s'ils sont **obtenables**. Envoyer les demandes, attendre un délai fixé d'avance
et écrit dans le préenregistrement, puis rapporter les réponses telles quelles — y compris si
elles sont positives et rapides, auquel cas R4 s'applique et la thèse se réduit — transformerait
la faiblesse en donnée. C'est la seule façon de répondre « ils le donneraient si vous demandiez »
autrement que par une conjecture. Décision au responsable : envoyer des courriels est hors du
périmètre de cette session.

### Ce qui resterait indéfendable, et qu'il faut donc ne pas écrire

- Écrire ou laisser entendre que des équipes ont **refusé** (faux, § 0.2).
- Présenter « 4 à 8 » comme un résultat de recensement (c'est une estimation, § 0.1).
- Faire du texte un plaidoyer pour l'ouverture des fichiers appariés : ce serait, venant des auteurs
  d'une attaque de ré-identification sur ces mêmes fichiers, à la fois incohérent et dangereux.
- Nommer des équipes dans un registre de reproche. Le SOEP protège des personnes ; l'exclusion du
  `respondent-level` par Wang et al. est une précaution. Le papier décrit un système, pas des
  coupables.

---

## 6. Mon avis franc

**Le constat est réel, mais il est aujourd'hui trop mince pour un article séparé, et il le restera
tant que le protocole de la § 3 n'aura pas été exécuté.** Ce que nous avons est : trois jeux
vérifiés, trois pistes tranchées, une estimation non bornée, et deux passes de recherche de
quelques heures. Ce n'est pas un recensement, c'est le pilote d'un recensement. Écrire l'article
maintenant reproduirait à l'identique le mécanisme des quatre rétractations du premier papier.

**Ce que je recommande, dans cet ordre :**
1. Publier **le registre** (Zenodo, DOI, licence explicite) avec ce qui est déjà vérifié et le
   protocole écrit : coût quasi nul, utile immédiatement, antériorité établie, falsifiable.
2. Intégrer le constat comme **section du premier papier** — il y renforce la discussion des
   limites au lieu d'y être une faiblesse.
3. Ne décider d'un article séparé **qu'après** exécution du protocole, et seulement si N ≤ 8 et si
   la typologie des blocages tient. Dans ce cas seulement : *Journal of Privacy and Confidentiality*
   (500 USD), ou *Transactions on Data Privacy* si le coût est rédhibitoire. Pas PoPETs, qui est
   le lieu du premier papier.

La partie du constat qui mérite le plus d'être publiée n'est d'ailleurs pas le nombre — un nombre
vieillit en quelques mois dans un domaine qui bouge à cette vitesse — mais la **typologie des
causes de non-redistribution** et le **critère C2** (appariement ligne à ligne par identifiant
commun, opposé à l'appariement par cellule démographique). Ce critère est ce qui a permis de
disqualifier `f7na8` sur constat de code alors que son résumé semblait qualifier. Il est
réutilisable par n'importe qui, il ne vieillit pas, et il ne dépend d'aucun décompte.
