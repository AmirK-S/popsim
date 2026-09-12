# Vérification de conformité PoPETs 2027.3 — 2026-09-12

Portée : exigences officielles de soumission (recherche web, lecture seule) confrontées à
`article/manuscrit.md` (1 087 lignes, corps 7–926), `resultats/ethique-section-brouillon.md`,
`resultats/divulgation-responsable-brouillon.md`, `artefact/`. Aucune modification apportée à
`article/manuscrit.md` — c'est à l'orchestrateur de l'éditer.

## Sources consultées (lecture seule)

- Exigences détaillées (page limite, gabarit, anonymisation, éthique, IA, préimpression) :
  https://crysp.petsymposium.org/authors-2027.php
- Page de call for papers, calendrier des 4 échéances annuelles, artefact :
  https://petsymposium.org/cfp27.php
- Politique et calendrier d'évaluation d'artefact 2026 (référence, cycle antérieur mais même
  processus décrit) : https://petsymposium.org/artifacts.php

Information non trouvée malgré recherche : le texte intégral du gabarit LaTeX 2027 lui-même
(nom exact des balises de section telles qu'elles apparaissent dans le `.tex`, au-delà de la
prose des pages ci-dessus) n'est accessible que via le ZIP de gabarit sur le portail de
soumission (`submit.petsymposium.org`), non consultable en lecture seule ici. Je le signale
plutôt que d'inférer sa mise en page exacte.

---

## Liste de contrôle, par gravité décroissante (rejet de bureau d'abord)

### 1. Références bibliographiques — vérifiées à la source — **CONFORME** *(corrigé le 12/09)*
Le gabarit 2027 traite les références IA hallucinées comme motif de rejet de bureau direct
(« Hallucinated references are grounds for desk rejection », politique IA, source ci-dessus).
**Ce point n'est plus une non-conformité.** `article/references-verification.md` enregistre
l'audit des **45 entrées** de `article/references.bib` : 27 reprises d'une vérification à la
source antérieure (bloc A), 18 vérifiées à la source dans la passe du 12/09 (bloc B, pages
d'abstract arXiv, Crossref, actes officiels). L'audit a corrigé deux identifiants arXiv
erronés (`drechsler2024thirtyyears`, `dwork2015robust`) et deux attributions d'auteur
(`hu2023microdata`, `guepin2023synthetic`). Contrôle croisé effectué : **les 41 clés citées
dans le manuscrit correspondent toutes à un travail présent dans le `.bib`** — aucune
référence citée n'est absente, donc aucune hallucination.
**Reste à faire, et c'est mineur** : **13 des 41 clés** du manuscrit portent une orthographe
provisoire différente de la clé finale du `.bib` (ex. `toubia2025twin` →
`toubia2025twin2k500`, `giomi2023anonymeter` → `giomi2023unified`) ; le tableau complet des
correspondances est dans `article/references-verification.md`. C'est une réconciliation
mécanique de noms de clés, pas une vérification de fond. **Temps** : 15–30 min.

### 2. Longueur réelle — limite de 12 pages — **CONFORME, avec ~2 pages de marge** *(mis à jour le 12/09)*
Le gabarit fixe la limite à **12 pages typographiées pour le corps**, hors trois sections
obligatoires (« ethical considerations », « open science », « AI use »), remerciements,
bibliographie et annexes clairement identifiées ; tout dépassement entraîne un rejet de bureau
**sans possibilité d'appel** (source : crysp.petsymposium.org/authors-2027.php).
Décompte réel du fichier Markdown, au 12/09 après l'audit des chiffres :
- Corps (résumé + §1–§7, lignes 7–926, ce qui correspond au périmètre limité en pages) :
  **10 055 mots**.
- §8 Ethics Considerations (lignes 929–1000, exclu de la limite) : 780 mots.
- §9 Availability (lignes 1003–1037, équivalent de la section « open science », exclu de la
  limite) : 280 mots.
- §10 AI Use (lignes 1040–1068, exclu de la limite) : 294 mots.
- Références (lignes 1071–1087) : 73 mots.
**La question est désormais tranchée par la compilation, pas par extrapolation** : le texte a
été porté dans le gabarit LaTeX (`article/latex/main.tex`) et compile ; le corps rend
**10 pages sur 12**, soit une marge d'environ **2 pages**. Le taux implicite est d'environ
**1 005 mots par page** pour ce gabarit, figures et tableau compris. **Avertissement à
conserver** : un taux de **821 mots/page** a circulé cette nuit et **ne doit plus être
utilisé** — il avait été mesuré sur du texte de remplissage, et sous-estime la capacité d'une
page d'environ 20 %. Le corps inclut 2 figures pleine page et un tableau de 17 lignes
(Table 1, §7.1), déjà pris en compte dans la compilation. **Rien à faire sur la longueur** ;
la marge disponible autorise à privilégier l'exactitude (intervalles de confiance, limites)
sur la concision.

### 3. Section « AI use » obligatoire — **présente** — **CONFORME** *(corrigé le 12/09)*
Le gabarit 2027 impose une section nommée « AI use » (avec « ethical considerations » et
« open science », citation exacte : *« the three mandatory sections per the 2027 template
(ethical considerations, open science, and AI use) »*). Cette section **existe désormais** :
`## 10. AI Use`, lignes 1039–1067 du manuscrit, 294 mots. Elle divulgue explicitement que des
agents fondés sur des LLM ont écrit le code d'analyse, mené les expériences, rédigé le
manuscrit et conduit la relecture adverse ; elle nomme le responsable comme seul comptable de
l'exactitude et de l'intégrité, précise qu'aucun outil d'IA générative n'est listé comme
auteur, et décrit trois contrôles (préenregistrement daté, graines fixes et reproduction à
l'identique, passes de relecture adverse) ainsi que les deux défauts substantiels qu'ils ont
permis de trouver. C'est la divulgation complète exigée par *« Mandatory disclosure of AI
use »*. **Rien à faire.**

### 4. Gabarit LaTeX obligatoire — **migration faite et compilée** — **CONFORME sous réserve** *(mis à jour le 12/09)*
« Authors must use [the PoPETs 2027 LaTeX template] » ; le non-respect du gabarit (mise en
page, colonnes) est explicitement un motif de rejet de bureau. **La migration a eu lieu** :
`article/latex/main.tex` existe et compile (`main.pdf` produit le 12/09), le corps rendant
10 pages sur 12 (voir point 2). Le Markdown `article/manuscrit.md` reste la source de
rédaction, converti par `article/latex/md2latex.py`.
**Réserves, à traiter par l'agent LaTeX** (hors de mon périmètre d'écriture) : (a) la légende
du tableau des prédictions, `main.tex` l. 395, annonce « The **sixteen** preregistered
predictions » alors que le tableau porte **17 lignes et 15 réfutations** — cette chaîne est
écrite en dur par `md2latex.py` et ne sera **pas** réparée par la régénération ; (b) les
renvois « Table 3 » et l'inversion des contributions (6)/(5), eux, sont recopiés du Markdown
et **seront** corrigés à la prochaine régénération, le Markdown ayant été corrigé ; (c) les
renvois de tableau sont écrits en dur plutôt que via `\ref{tab:predictions}`, donc le problème
se reproduira à chaque changement de contenu.

### 5. Scories de rédaction interne — **retirées** — **CONFORME** *(corrigé le 12/09)*
La section `[OPEN ITEMS]` (notes de travail internes : « **[decision]** », statut d'items
numérotés) a été **supprimée du manuscrit** : `grep -n "OPEN ITEMS"` ne renvoie plus rien, et
le fichier s'achève désormais sur la section « References » (ligne 1086). Le suivi
correspondant vit dans `REPRISE-2026-09-12.md`, hors du dossier de soumission. **Rien à
faire.**

### 6. Nommage des sections obligatoires — **NON CONFORME (mineur)**
Le gabarit nomme les sections « ethical considerations » et « open science ». Le manuscrit a
« ## 8. Ethics Considerations » (ligne 930, écart de libellé mineur) et « ## 9. Availability »
(ligne 1001, probable équivalent du contenu « open science » — disponibilité des données, de
l'artefact, des préenregistrements — mais sous un intitulé différent de celui qu'exige le
gabarit). **À faire** : renommer en « Ethical Considerations » et « Open Science » (ou fusionner
le contenu de §9 sous l'intitulé exact du gabarit une fois celui-ci consulté). **Temps** :
5–15 min, sous réserve de vérifier l'intitulé exact dans le fichier `.tex` du gabarit
(non consulté ici, cf. section Sources).

### 7. Section éthique : détermination IRB — **CONFORME** *(corrigé le 12/09)*
Ce que dit réellement la politique PoPETs (citation exacte, crysp.petsymposium.org/authors-2027.php) :
*« a justification of the ethics of the work and information about whether the work was
submitted to an external ethics panel such as an IRB… A "no" answer is not a ground for
rejection as long as the authors provide a reasonable explanation. »* Aucune clause spécifique
aux données secondaires déjà publiques n'a été trouvée sur le site (recherche explicite menée,
sans résultat au-delà de ce texte général) — **je le signale plutôt que de l'inférer**. La
règle applicable est donc générale : un « non » à la question IRB n'est pas rédhibitoire s'il
est justifié par écrit. **Le cadrage a été corrigé.** Le manuscrit ne présente plus ce point comme un manque : la
sous-section « Ethics review and scope » (§8, fin) **affirme** la position — l'étude n'a pas
été soumise à un comité externe de type IRB, elle repose exclusivement sur des données
secondaires déjà rendues publiques par les équipes d'origine (Twin-2K-500 sous CC BY 4.0,
paquet de réplication Park), aucune donnée nouvelle n'a été collectée (« we surveyed no one,
interviewed no one, and had no contact with any data subject »), **et sur cette base l'étude
est jugée hors du champ de la recherche sur sujets humains**. La limite correspondante est
conservée juste à côté (les participants n'ont pas consenti spécifiquement à un test de
ré-identification). C'est exactement la « reasonable explanation » que la politique exige en
regard d'un « non » à la question IRB. **Rien à faire.**

### 8. Lettres de divulgation responsable non envoyées — **NON CONFORME (risque modéré, pas un motif de rejet de bureau)**
`resultats/divulgation-responsable-brouillon.md` confirme qu'aucun message n'a été envoyé.
Le manuscrit (lignes 950–954, 992–997 ; `[OPEN ITEMS]` #1, lignes 1060–1064) présente cela
comme devant être réglé « before any preprint posting ». Ce n'est **pas** une exigence formelle
de soumission PoPETs : la soumission est en aveugle, non publique, donc distincte d'une
« publication » ou d'un « preprint posting ». Ce qui est réellement en jeu : (a) la politique de
préimpression de PoPETs *décourage* (sans l'interdire) la mise en ligne publique d'un preprint
pendant l'évaluation, précisément pour ne pas compromettre l'anonymat — donc le délai de 30
jours n'a pas besoin d'être clos avant le 30 novembre 2026, mais devrait l'être avant toute mise
en ligne publique ultérieure (preprint ou dépôt de code/artefact public, qui n'intervient de
toute façon qu'après acceptation, l'artefact étant soumis ~10 jours après l'échéance de
révision) ; (b) rien n'empêche d'envoyer les lettres dès maintenant, ce qui est recommandé pour
sécuriser la fenêtre de 30 jours bien avant toute publication. **Décision** requise du
responsable du projet (signature, pièces jointes) — hors de mon périmètre d'action.

### 9. Anonymisation du manuscrit — **CONFORME**
Recherche systématique (grep) dans tout `article/manuscrit.md` : aucune occurrence de
« our previous/prior work », aucun nom d'institution, aucune adresse électronique, aucun
chemin de fichier personnel (`/Users/…`), aucun nom d'auteur, aucune URL de dépôt GitHub
personnel, aucune section de remerciements. Les identités réelles (Joon Sung Park, Michael
Bernstein, `msb@cs.stanford.edu`) figurent uniquement dans les brouillons de lettres de
`resultats/divulgation-responsable-brouillon.md`, qui n'est pas un fichier destiné à la
soumission. Auto-citation en 3e personne déjà respectée (« Toubia et al. », jamais « our prior
dataset »). Rien à corriger sur ce point à ce jour.

### 10. Métadonnées des figures — **CONFORME**
`article/figures/fig1-monde-ouvert.png` (1364×1872 px) et `fig2-couplage.png` (1039×1005 px) :
seul un tag `tEXt Software = Matplotlib version 3.11.1` est présent (chaîne générique), aucun
nom d'utilisateur ni chemin (`strings` sur les deux fichiers). Résolution suffisante pour
impression. Lisibilité en noir et blanc : les deux figures utilisent uniquement des niveaux de
gris et des marqueurs de forme distincte (cercle/carré/triangle/losange/étoile), pas de code
couleur — conforme à un rendu N&B. Légendes autoportantes : les légendes intégrées au corps du
texte (lignes 467–489 pour la Fig. 1, lignes 671–686 pour la Fig. 2) rappellent explicitement
les chiffres clés et l'échelle logarithmique, et précisent les limites de lecture (« a reader
should not read a curve into the diamonds »). **Conforme.**

### 11. Structure attendue (déclaration éthique, divulgation responsable) — **PRÉSENTE mais à mettre aux normes**
Une section « Ethics Considerations » (§8) et un contenu de divulgation responsable existent
bel et bien dans le corps du texte (lignes 930–997) — voir points 3, 6 et 7 pour les
non-conformités précises de forme et de cadrage.

### 12. Artefact : capacité d'attaque contre des personnes réelles — **CONFORME (aucune donnée réelle livrée)**
`artefact/README.md` (lignes 65–101) et le code (`garde.py`) confirment : 600 personnes
**fictives**, générées par graine fixe (`numpy.random.default_rng`, `config.GRAINE =
20260912`), aucune donnée réelle. Le garde-fou `garde.py` refuse explicitement de démarrer si
un chemin vers `data/` est détecté (argv ou variables d'environnement). Les vraies données
(Twin-2K-500, archive Park/OSF) ne sont ni redistribuées ni lues par l'artefact ; seules leurs
sources externes sont documentées (Hugging Face CC BY 4.0, page OSF). Les chiffres produits par
l'artefact sont explicitement marqués comme illustratifs, jamais comme résultats de l'étude
(lignes 1019–1022 du manuscrit, et le README lui-même). **L'artefact ne permet pas de mener
l'attaque contre de vraies personnes.**

---

## Politique d'artefact PoPETs, pour mémoire

Soumission d'artefact **après acceptation**, sur invitation : dépôt de l'artefact environ 10
jours après l'échéance de révision, cycle d'évaluation interactif (préliminaire à ~3 semaines,
mise à jour à ~4 semaines, finalisation à ~7 semaines). Non obligatoire mais fortement
encouragée ; un « non » avec justification n'est pas un motif de rejet. Source :
crysp.petsymposium.org/authors-2027.php, petsymposium.org/artifacts.php.
