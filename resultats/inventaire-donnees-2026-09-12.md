# Inventaire des données pour un troisième jeu (12 septembre 2026)

Question posée par le responsable : l'article repose sur Twin-2K-500 et l'archive Park et al.
(OSF `t6g7k`) ; un troisième jeu serait l'amélioration la plus rentable contre l'objection
« vos résultats tiennent-ils ailleurs ? ». Le responsable pense s'être inscrit sur plusieurs
sites pour obtenir des données et croit qu'on a déjà ce qu'il faut. Ce document établit les
faits, sans supposer ce que sont ces inscriptions.

Sources consultées : `data/PROVENANCE.md` et les huit `PROVENANCE.md` de sous-dossiers,
`demandes/` (huit lettres), `resultats/c7-troisieme-jeu-inventaire-2026-09-12.md` (inventaire
de faisabilité déjà produit aujourd'hui même par une autre session), `resultats/d1-donnees-manquantes.md`,
`exploration/05-datasets-publics.md`, plus deux recherches web pour vérifier l'existence d'un
candidat externe. Aucune donnée individuelle n'a été lue ligne à ligne au-delà de ce que les
`PROVENANCE.md` documentaient déjà.

---

## 1. Les deux jeux de l'article

| jeu | où | téléchargé | taille | licence | contenu |
|---|---|---|---|---|---|
| **Twin-2K-500** | Hugging Face `LLM-Digital-Twin/Twin-2K-500` | oui, `data/twin2k500/` | 79 Mo sur disque | CC BY 4.0, accès libre | 2 058 personnes réelles, >500 questions, 4 vagues dont une de retest, **et** des sorties LLM déjà calculées par les auteurs (`llm/`, `llm_specs/`) pour ces mêmes personnes |
| **OSF `t6g7k`** (Park et al., matériel de réplication) | osf.io/t6g7k | oui, `data/osf-t6g7k-stanford/` | 27 Mo sur disque | **aucune licence déclarée** (`node_license: null`) ; conditions NORC du GSS sous-jacent interdisent la redistribution des réponses individuelles | 1 052 personnes réelles, GSS + BFI-44 + jeux économiques, 2 vagues, **et** sorties de cinq conditions d'agents pour ces mêmes personnes |

Les deux qualifient parce qu'ils ont la propriété décisive : **vraies réponses et sorties
synthétiques appariées aux mêmes individus.** Tout le reste de l'inventaire est jugé à cette
aune.

---

## 2. Tout ce qui est déjà sur la machine, au-delà de ces deux jeux

| dossier | source | téléchargé | taille | licence / conditions | contenu | sorties de jumeaux/agents pour les mêmes personnes ? |
|---|---|---|---|---|---|---|
| `data/sce-fed-ny/` | Survey of Consumer Expectations, Fed de New York | oui | 186 Mo | conditions FRBNY, redistribution autorisée avec attribution [CONFIRMÉ] | 82 535 observations utiles, ~9 700 `userid` distincts par fichier, anticipations économiques mensuelles | **non** — que des réponses humaines |
| `data/gss-panel/` | NORC, panels GSS 2006-2020 | oui | 94 Mo | conditions NORC : lecture et agrégats seulement, pas de redistribution [CONFIRMÉ] | 4 panels réels, mêmes personnes réinterrogées à 2-4 ans | **non** — que des réponses humaines |
| `data/ahler-sood-pcomp/` | Ahler & Sood 2018, Harvard Dataverse | oui | 5,1 Mo | **CC0 1.0**, aucune restriction [CONFIRMÉ] | ~1000 répondants YouGov, croyances de second ordre sur la composition des partis | **non** — que des réponses humaines ; le `readme.txt` réclame en plus `anes_timeseries_2012.dta`, absent de l'archive |
| `data/westwood-pnas-2025/` | Westwood 2025, PNAS, OSF `ektqr` | oui | 28 Mo | dépôt public, **aucune licence déclarée** [CONFIRMÉ] | 27 923 réponses **synthétiques** générées par 300 profils fabriqués (le répondant adverse le plus dur, il passe 99,8 % des contrôles d'attention) | **sens inverse du besoin** : sorties de jumeaux seules, **aucun répondant humain apparié** — noté explicitement dans sa propre `PROVENANCE.md` |
| `data/norc-mode/` | six rapports méthodologiques NORC/NBER, transcrits à la main | oui (régénéré par script) | 28 Ko | agrégats publics | ampleurs d'effet de mode par item, pas de ligne individuelle | sans objet — pas de donnée individuelle du tout |
| `data/anes-codebooks/` | SDA, UC Berkeley (miroir de l'ANES) | oui, **codebooks seulement** | 9,4 Mo | documentation publique | aucune microdonnée ANES | sans objet — pas de donnée du tout |

**Aucun de ces six dossiers ne contient de sorties de jumeaux ou d'agents appariées aux
réponses humaines qu'il contient.** C'est le verdict déjà posé aujourd'hui par
`resultats/c7-troisieme-jeu-inventaire-2026-09-12.md` : SCE et Ahler-Sood sont bien d'une
nature différente du GSS/Big Five et légalement publiables en agrégat, mais il faudrait
fabriquer nous-mêmes leurs jumeaux, ce qui introduirait notre propre méthode de génération
comme facteur confondu au lieu de tester la généralité du phénomène sur des jumeaux produits
par un tiers.

---

## 3. Les trois catégories

### Utilisable tout de suite
**Rien au-delà des deux jeux de l'article.** Tout ce qui est déjà sur la machine et qui
contiendrait un troisième jeu complet (humains + jumeaux appariés) n'existe pas dans
l'inventaire local.

### Demanderait une démarche
Huit lettres sont rédigées dans `demandes/` (nuit du 9 au 10 septembre 2026), **aucune n'est
signée ni envoyée** : chacune contient encore les trois champs à compléter,
`[AFFILIATION]`, `[NOM ET SIGNATURE]`, `[DATE]`. Ce qui s'y trouve :

| démarche | objet | ce que ça débloquerait pour un troisième jeu |
|---|---|---|
| Lettre 05, Sean Westwood (Dartmouth) | le fichier humain apparié au répondant synthétique d'OSF `ektqr` | s'il existe, ce serait exactement le troisième jeu recherché — même nature (adversarial), autre équipe |
| Lettre 01, ANES | compte pour les fichiers 2020/2024 | pas un troisième jeu jumeaux+humains en soi, mais débloquerait une deuxième population humaine de référence |
| Lettres 06 et 07, ELIPSS (CDSP) et SOEP (DIW Berlin) | accès à des panels européens réinterrogés | populations humaines de réference supplémentaires, pas de jumeaux |
| Lettres 03 et 04 | fichier réel à contamination documentée (procureur de NY / plateforme de panel) | pas des jumeaux LLM, mais un flux mêlé à taux vrai connu, pour un usage différent (C7/i3) |
| **LISS (Pays-Bas)** et **British Election Study** | signature en ligne (LISS, `liss.statements.centerdata.nl`) et téléchargement libre (BES) | **aucune lettre à écrire**, mais **aucun des deux dossiers n'existe sur la machine** — la démarche elle-même n'a pas été faite |

### Inutilisable pour notre question, et pourquoi
- `data/gss-panel/`, `data/sce-fed-ny/`, `data/ahler-sood-pcomp/` : vraies réponses humaines,
  **aucune sortie simulée existante** pour ces mêmes personnes.
- `data/westwood-pnas-2025/` : l'inverse — sorties synthétiques seules, **aucun fichier humain
  apparié**, disqualifié explicitement par sa propre documentation.
- `data/norc-mode/` et `data/anes-codebooks/` : pas de données individuelles du tout, l'un est
  fait d'agrégats publiés, l'autre de codebooks.

---

## 4. Trace des inscriptions mentionnées par le responsable

**Aucune trace dans le dépôt** d'un compte créé ou d'une inscription aboutie, sur aucun site
mentionné dans `demandes/README.md` ou ailleurs :
- Aucun dossier `data/liss*`, `data/bes*`, `data/elipss*`, `data/soep*`, `data/ess*` n'existe.
- Les huit lettres de `demandes/` sont toutes encore à l'état de brouillon avec champs vides.
- Aucun fichier du dépôt (recherché par mots-clés « inscri », « compte », « LISS », « British
  Election Study », « electionstudies », « dataverse.centerdata ») ne documente une inscription
  réalisée ou une réponse reçue d'un des destinataires.

Si le responsable a effectivement créé des comptes sur LISS, le British Election Study, l'ANES
ou ailleurs, **ce n'est consigné nulle part dans ce dépôt** et aucun fichier téléchargé n'en
atteste. C'est une réponse factuelle, pas une supposition sur ce qu'il a ou n'a pas fait.

---

## 5. Candidat externe vérifié pour combler le manque

Recherche web ciblée sur « troisième jeu, nature différente, humains + IA générative appariés »,
au-delà de ce que `exploration/05-datasets-publics.md` avait déjà recensé le 2 septembre (qui ne
contient aucun autre candidat avec pairage individuel humain/agent que les deux jeux déjà
utilisés).

**Zhang, Xu et Alvero, « Generative AI Meets Open-Ended Survey Responses: Research Participant
Use of AI and Homogenization », *Sociological Methods & Research*, 2025.**
- Matériel de réplication : OSF, nœud `f7na8`, https://osf.io/f7na8/ .
- Vérifié via l'API OSF (`https://api.osf.io/v2/nodes/f7na8/`) : **`public: true`**, créé le
  9 février 2025, **`node_license: null`** — le même régime que l'archive Park et al. : lecture
  et calcul local possibles, redistribution des réponses individuelles non couverte par une
  licence explicite. [CONFIRMÉ]
- Nature du jeu, d'après le résumé et les pages de l'éditeur (Stanford GSB, SAGE) : compare des
  réponses **humaines à des questions ouvertes** issues de trois enquêtes antérieures à ChatGPT
  avec des réponses **générées par un LLM**, et documente séparément que 34 % des répondants
  d'une enquête originale déclarent avoir utilisé un LLM pour répondre. C'est un domaine
  (réponses ouvertes, texte libre) et une équipe (Stanford/Cornell, pas Park et al. ni l'équipe
  Twin-2K-500) réellement distincts du GSS/Big Five.
- **Ce qui bloque, et n'a pas pu être vérifié à distance** : le dossier `aisurv_osf/` du dépôt
  OSF n'expose, via l'API, qu'un sous-dossier sans liste de fichiers accessible sans
  authentification du navigateur ; je n'ai pas pu confirmer si les réponses générées par le LLM
  sont **appariées individuellement** aux répondants humains (mêmes personnes, mêmes items,
  comme un jumeau) ou seulement des simulations agrégées par condition. C'est la question qui
  décide si ce jeu qualifie ou non, et elle reste **[NON VÉRIFIÉ]**. Il faudrait ouvrir le
  dossier OSF dans un navigateur ou lire le papier en entier (SAGE renvoie HTTP 403 sans
  abonnement ; passer par la version Stanford GSB ou SocArXiv).

Aucun autre candidat externe sérieux n'a été trouvé dans les deux recherches effectuées : les
autres résultats étaient soit les deux jeux déjà utilisés, soit des outils/frameworks (challenge
ICML 2026, `SurveyScope`) sans réponses humaines individuelles appariées à des sorties de
jumeaux.

---

## 6. Point de sécurité

`data/westwood-pnas-2025/solving_engine/secrets.yml` existe et contient des entrées qui
ressemblent à des clés d'accès de fournisseur de modèle (fichier utilisé par `provider.py` du
moteur de répondant synthétique de Westwood). Je n'ai pas divulgué son contenu ; je signale
seulement son existence.

---

## Réponse en une ligne

Deux jeux qualifient déjà (Twin-2K-500, 2 058 personnes, jumeaux inclus ; OSF `t6g7k`/Park et
al., 1 052 personnes, cinq conditions d'agents incluses) ; six autres jeux sont sur la machine
(SCE, GSS-panel, Ahler-Sood, Westwood, norc-mode, codebooks ANES) mais aucun n'a de sorties de
jumeaux appariées à des humains — Westwood a l'inverse, jumeaux sans humains ; huit démarches
sont rédigées mais aucune envoyée, dont la lettre à Westwood qui demanderait précisément le
fichier humain manquant, et LISS/BES ne demandent aucune lettre mais n'ont pas encore été faits
non plus ; le dépôt ne garde aucune trace d'un compte réellement créé sur un site quelconque ; un
candidat externe sérieux existe, OSF `f7na8` (Zhang, Xu, Alvero 2025, réponses ouvertes
humaines vs IA), même régime de licence que Park et al., mais le pairage individuel humain/IA
n'a pas pu être confirmé à distance.
