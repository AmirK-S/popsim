# Gabarit LaTeX PoPETs 2027 — mise en place et estimation de pages — 2026-09-12

statut: courant
mandat: mettre en place le gabarit LaTeX officiel PoPETs 2027, construire la chaîne de compilation et le mécanisme de transfert Markdown → LaTeX, et tenir la marge de pages du corps sous la limite de 12 pages jusqu'au PDF de soumission
agent: document collectif, tenu en série par un agent à la fois (Méthode v2 §1.1)
ecriture: article/latex/, resultats/latex-gabarit-2026-09-12.md
lecture_seule: tout le reste, en particulier article/manuscrit.md et article/references.bib
interdits: appel payant sans GO, réseau (lecture seule uniquement), commit sur master, arrière-plan
cout_reel_usd: 0.00

Portée : `article/latex/` (nouveau répertoire, écriture autorisée) et ce fichier. Aucune
modification de `article/manuscrit.md` ni de `article/references.bib` (lecture seule). Recherche
web en lecture seule uniquement ; aucun appel de modèle payant ; aucun calcul scientifique.

## 1. Gabarit récupéré

- **Source** : https://petsymposium.org/files/submission-template-2027.zip (lien trouvé sur
  https://crysp.petsymposium.org/authors-2027.php, page consultée le 2026-09-12).
- **Date de récupération** : 2026-09-12.
- **Cycle** : c'est bien le gabarit **2027** (le nom du zip et le contenu extrait le confirment :
  répertoire `PoPETS-2027-latex-template/`), donc pas de repli sur un cycle antérieur nécessaire.
- **Contenu du zip**, installé tel quel dans `article/latex/` : `acmart.cls`, `popets.sty`,
  `ACM-Reference-Format.bst`, `acmnumeric.bbx`/`acmnumeric.cbx`, `cc-by-4.pdf`,
  `sample-franklin.png`, `sample-base.bib`, et l'exemple officiel — renommé
  `exemple-gabarit-main.tex` (le zip le nommait `main.tex` ; renommé pour laisser `main.tex` à
  notre propre squelette, voir §3).
- **Structure du gabarit** : `\documentclass[sigconf,anonymous,review]{acmart}` +
  `\usepackage{popets}`. Confirme et lève l'incertitude notée dans
  `resultats/conformite-popets-2026-09-12.md` (point 6) sur le nommage exact des sections
  obligatoires : ce sont des **environnements**, pas des `\section*`, à utiliser mot pour mot :
  `\begin{acks}…\end{acks}`, `\begin{ethics}…\end{ethics}`, `\begin{openscience}…\end{openscience}`,
  `\begin{ai}…\end{ai}`, dans cet ordre, après `\appendix`, avant `\bibliography`. Le commentaire du
  gabarit le dit explicitement : titre et emplacement exacts requis « or risk desk rejection ».
  Limite confirmée dans le corps du fichier : **12 pages composées pour le corps, 13 pour une
  révision** — cohérent avec `authors-2027.php`.

## 2. Chaîne de compilation sur cette machine

**LaTeX est installé** : `pdflatex`, `xelatex`, `bibtex` présents (`/Library/TeX/texbin`, TeX Live
2026). **Absents** : `latexmk`, `biber` (non nécessaires ici : le gabarit utilise BibTeX, pas
Biber).

La distribution installée est un jeu **« basic »** (scheme minimal) : plusieurs paquets requis par
`acmart` manquaient. Je n'ai pas installé de nouvelle distribution ; j'ai complété les paquets
manquants via `tlmgr --usermode` (arborescence TeX **utilisateur**, sans droits admin, réversible,
propre à ce compte) :

```
tlmgr --usermode install xstring totpages ifmtarg comment ncctools xkeyval \
  fontaxes kastrup preprint libertine inconsolata newtx cm-super placeins
```

**Un paquet a résisté** : `hyperxmp` est marqué « non relocatable » par `tlmgr` et refuse
l'installation en mode utilisateur (message : *"package hyperxmp is not relocatable, cannot install
it in user mode"*). Contournement sans droits admin : le paquet CTAN
(`https://mirrors.ctan.org/macros/latex/contrib/hyperxmp.zip`) est distribué en source
(`.dtx`/`.ins`) ; `tex hyperxmp.ins` extrait `hyperxmp.sty`, copié directement dans
`article/latex/` (LaTeX cherche d'abord dans le répertoire courant). Le fichier est donc présent
dans `article/latex/hyperxmp.sty` et n'a besoin d'aucune installation système.

**Si l'utilisateur reconstruit cet environnement ailleurs** (autre machine, ou avec des droits
admin), la commande la plus simple est :

```
sudo tlmgr install xstring totpages ifmtarg comment ncctools xkeyval fontaxes \
  kastrup preprint libertine inconsolata newtx cm-super placeins hyperxmp
```

(avec les droits admin, `hyperxmp` s'installe normalement — le contournement ci-dessus n'est
nécessaire qu'en mode utilisateur strict.)

**Confirmation de compilation** : l'exemple officiel du gabarit compile sans erreur —
`article/latex/exemple-gabarit-main.tex` → `exemple-gabarit-main.pdf`, **4 pages**, cycle complet
`pdflatex → bibtex → pdflatex → pdflatex`. Avertissements restants, tous bénins (données de
l'exemple, pas du gabarit) : rappels que le format de référence ACM et les CCS concepts sont
attendus, et quelques entrées BibTeX de démonstration mal formées dans `sample-base.bib` (fichier
d'exemple, sans rapport avec notre bibliographie).

## 3. Squelette de notre article

`article/latex/main.tex` reprend :
- le **titre exact** du manuscrit ;
- la **structure de sections** (1 à 7.5, plus les trois sections obligatoires et les
  remerciements) avec la même hiérarchie `\section`/`\subsection` que `article/manuscrit.md` ;
- les **deux figures réelles** (`article/latex/figures/fig1-monde-ouvert.png` et
  `fig2-couplage.png`, copiées depuis `article/figures/`), chacune dans un environnement
  `figure` réel avec `\Description{}` (obligatoire dans ce gabarit pour l'accessibilité) ;
- le **Tableau 3 (§7.1) réel dans sa forme** : 16 lignes de données × 4 colonnes, en
  `table*` (pleine largeur) comme la longueur des cellules l'impose ;
- `article/references.bib` **copié** dans `article/latex/references.bib` (pas de chemin
  fragile vers `../references.bib`), appelé par `\bibliographystyle{ACM-Reference-Format}` +
  `\bibliography{references}` + `\nocite{*}` pour forcer l'impression de toutes les entrées
  actuellement dans le fichier (utile pour l'estimation de pages ; à remplacer par les vrais
  `\cite{}` une fois les clés réconciliées, cf. `resultats/conformite-popets-2026-09-12.md`
  point 1, hors de mon périmètre).

**Ce qui n'est PAS transcrit** : le corps de chaque section est un **texte de remplissage**
(latin factice, aucune donnée scientifique) dont le nombre de mots est calculé pour **égaler
exactement** celui de la section correspondante du Markdown (comptage fait section par section,
en-têtes inclus, avec un script Python appliqué à `article/manuscrit.md` — voir méthode ci-dessous).
Les légendes des deux figures sont également du remplissage, mais dont le nombre de mots égale
celui de la légende réelle (295 mots pour la Fig. 1, 182 pour la Fig. 2), extraite du bloc
`> **Figure N —…**` du Markdown, pour ne pas compter ces mots deux fois. La section « AI Use »
n'existe dans aucune version du manuscrit (absente, comme relevé dans
`resultats/conformite-popets-2026-09-12.md` point 3) : l'environnement `\begin{ai}…\end{ai}` est
présent dans le squelette (obligatoire structurellement) mais contient une note de substitution
explicite, pas un texte inventé faisant croire à un contenu réel.

**Méthode de comptage** : le corps du Markdown (résumé + §1–§7.5, lignes 1–927) fait **9 853
mots**, exactement le chiffre déjà relevé dans `resultats/conformite-popets-2026-09-12.md`. Le
découpage par en-tête (`#`, `##`, `###`) donne le nombre de mots de chaque section/sous-section ;
c'est ce chiffre qui a servi de cible pour le texte de remplissage correspondant.

## 4. Résultat de la compilation du squelette — estimation de pages

Cycle complet `pdflatex → bibtex → pdflatex → pdflatex`, aucune erreur, aucun fichier manquant.

| | Résultat |
|---|---|
| Pages totales du document | **15** |
| **Corps (§1 à §7.5, limité à 12 pages)** | **12 pages, très exactement à la limite** |
| Ethics + Open Science (hors limite) | ~1 page (page 13) |
| AI Use + Références (hors limite) | ~2 pages (pages 14–15, ~45 entrées bibliographiques) |

**Nous ne débordons pas actuellement, mais la marge est nulle.** Le corps occupe l'intégralité des
12 pages autorisées, pas une de plus, pas une de moins. Cela veut dire que toute expansion lors du
passage au texte réel — une phrase de plus, une reformulation moins compacte, un ajustement de
taille de figure, un habillage de tableau légèrement différent — risque de faire passer le corps à
13 pages, motif de **rejet de bureau sans appel**. Ce n'est pas un verdict de dépassement, c'est un
verdict d'absence totale de coussin.

**Piège méthodologique identifié et corrigé en cours de route** : dans une première passe, les
deux figures avaient « flotté » (mécanisme normal de LaTeX pour les flottants) jusqu'à la page 12,
*après* la fin de la section 7 — ce qui aurait fait croire à un corps de seulement 10 pages (2
pages de marge illusoire), alors que les figures appartiennent structurellement au corps. Le
squelette utilise donc `\usepackage{placeins}` avec un `\FloatBarrier` juste avant `\appendix`,
pour forcer les deux figures à se résoudre **dans** le corps plutôt qu'après. Sans cette précaution,
l'estimation de pages du corps est fictivement optimiste.

### Où se trouve la marge de réduction, si le contenu réel dépasse

Expérience contrôlée (deux variantes du squelette, même texte de remplissage, comparées au
squelette de référence à 15 pages / 12 pages de corps) :

- **Retirer les deux figures** (en gardant leurs légendes comme texte de remplissage, donc à
  nombre de mots inchangé) : le document tombe à **13 pages totales, 11 pages de corps**. Les
  deux figures ensemble coûtent donc environ **1 page de corps** au-delà de ce que leur seul texte
  de légende occuperait — un coût purement lié à l'image (mise en page, flottant), pas au texte.
- **Retirer en plus la structure réelle du Tableau 3** (même texte, remplacé par un paragraphe
  continu de même nombre de mots) : **aucune économie supplémentaire** (toujours 13 pages). Le
  tableau, en `table*` pleine largeur, ne coûte pas plus de place que son volume de mots ne
  l'exigerait en prose habillée sur deux colonnes — contrairement à l'intuition de départ
  (`resultats/conformite-popets-2026-09-12.md` point 2), **ce n'est pas le tableau qui pèse**,
  ce sont **les figures**.

**Sections les plus longues du corps** (par nombre de mots, cible du remplissage) — à surveiller en
priorité si une coupe devient nécessaire à contenu réel : §5.7 « The risk depends on the recipe »
(614 mots, le plus long), §5.3 « Open world » (574 mots dont 295 de légende Fig. 1), §7.1 « The
sixteen refuted preregistered predictions » (557 mots, tableau inclus), §1.2 « Contributions » (541
mots), §5.4 (383), §5.2 (377), §7.5 (374), §5.1 (354), §1.1 (353), §6.2 (331), §5.9 (328 dont 182 de
légende Fig. 2).

**Limite de cette estimation** : le texte de remplissage est du latin factice à densité de mots
homogène ; le manuscrit réel contient beaucoup de nombres courts (pourcentages, intervalles de
confiance), des appels `\cite{clé}` qui s'affichent en quelques caractères (« [12] »), et des
`\texttt{}` de code — probablement plus compacts, ligne à ligne, que ma prose de remplissage. Le
résultat réel une fois le vrai texte transféré pourrait donc être légèrement en dessous de 12
pages plutôt qu'au-dessus, mais rien ne garantit ce sens : c'est une estimation structurellement
fiable (vrai gabarit, vraies figures, vrai tableau, vrai décompte de mots par section), pas une
certitude au mot près. À recompiler avec le texte réel dès qu'il sera figé.

## 5. Marche à suivre pour compiler

```bash
cd article/latex
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
# → main.pdf
```

Si des paquets manquent sur une autre machine, voir §2 ci-dessus (installation `tlmgr --usermode`
ou `sudo tlmgr install …`, plus le contournement manuel pour `hyperxmp` si mode utilisateur
strict).

## 6. Ce qu'il reste à faire pour transférer le contenu réel (hors de mon périmètre d'écriture)

1. **Remplacer chaque bloc de remplissage par le texte réel** de la section correspondante de
   `article/manuscrit.md`, section par section — la structure (`\section`/`\subsection`, ordre,
   titres) est déjà en place et n'a pas besoin d'être recréée.
2. **Recompiler et revérifier le nombre de pages** après chaque section substantielle transférée,
   étant donné l'absence de marge constatée ici (12/12).
3. **Réconcilier les clés bibliographiques** : `article/references.bib` copié ici est celui qui
   existait le 2026-09-12 (en cours de vérification par un autre agent, cf.
   `resultats/conformite-popets-2026-09-12.md` point 1) ; retirer le `\nocite{*}` de secours une
   fois les vrais appels `\cite{}` insérés dans le texte transféré, et re-synchroniser
   `article/latex/references.bib` avec la version finale de `article/references.bib`.
4. **Rédiger la section AI Use** (actuellement un texte de substitution explicite dans
   `\begin{ai}…\end{ai}`) — décision du responsable du projet, cf.
   `resultats/conformite-popets-2026-09-12.md` point 3.
5. **Renseigner auteurs, affiliations, ORCID, remerciements** au moment de la levée de l'anonymat
   (retirer les options `anonymous,review` de `\documentclass` pour la version finale/caméra-ready
   uniquement, jamais avant).
6. **Rédiger de vraies descriptions d'accessibilité (`\Description{}`)** pour les deux figures — le
   squelette contient des textes de substitution explicites, pas des descriptions réelles.
7. **Purger les artefacts de compilation** (`*.aux`, `*.log`, `*.blg`, `*.out`, `*.bbl`) avant tout
   dépôt — laissés hors de ce répertoire par ce squelette, mais seront régénérés à chaque
   compilation locale.

## 7. Sources consultées (lecture seule)

- https://crysp.petsymposium.org/authors-2027.php — limite de 12 pages (13 en révision), sections
  obligatoires, lien du gabarit, exigence CC-BY-4.0 sur la première page.
- https://petsymposium.org/files/submission-template-2027.zip — gabarit lui-même, récupéré le
  2026-09-12.
- https://petsymposium.org/cfp27.php — dates du cycle 2027.3 (dépôt 30 novembre 2026 ferme,
  notification 1 février 2027).
- https://mirrors.ctan.org/macros/latex/contrib/hyperxmp.zip — paquet `hyperxmp`, contournement
  d'installation en mode utilisateur (voir §2).

---

## 8. Complément — ce qui compte réellement dans les 12 pages (2026-09-12, suite)

Question posée par l'orchestrateur : le contenu va grossir (intervalles de confiance
supplémentaires, réécriture du résultat central, section « AI Use », passage éthique reformulé) et
la marge est nulle (12/12). Ce qui suit répond avec la règle officielle citée mot pour mot, jamais
par déduction — source unique pour ce complément :
https://crysp.petsymposium.org/authors-2027.php (revérifiée en direct le 2026-09-12).

### 8.1 Ce qui entre dans la limite de 12 pages, et ce qui en sort

**Citation exacte** : *« The main body excludes the three mandatory sections per the 2027 template
(ethical considerations, open science, and AI use) as well as any acknowledgements, the
bibliography, and any clearly-marked appendices contained in the submission. »*

Réponse aux quatre points posés :

1. **Bibliographie** : **hors limite**, nommément citée dans la phrase ci-dessus (« the
   bibliography »). Le nombre d'entrées (46) est donc sans effet sur la limite de 12 pages, quel
   que soit son propre nombre de pages.
2. **Annexes** : **hors limite** (« any clearly-marked appendices »), mais avec deux
   restrictions citées mot pour mot : *« appendices should only be used to provide supplementary
   information that falls outside of the stated contribution of the paper or to provide extended
   details that would not be of interest to most readers »*, et surtout : *« PC members are not
   required to read the appendices during review. »* Conséquence directe pour la recommandation de
   réduction (§8.3) : tout ce qui est nécessaire pour juger la contribution — un résultat, un
   chiffre cité dans l'abstract ou la discussion, une limite substantielle — **ne doit pas** partir
   en annexe, puisqu'un relecteur n'est pas tenu de l'y lire. Seul du matériel véritablement
   secondaire (détail procédural, log d'exécution) s'y prête.
3. **Sections obligatoires** (éthique, AI Use, open science) : les trois sont **hors limite**,
   explicitement nommées dans la citation du point 1, avec confirmation redondante trouvée
   ailleurs sur la même page : *« There is no page limit for the three mandatory final sections per
   the 2027 template (ethical considerations, open science, and AI use), acknowledgements,
   bibliography, and clearly-marked appendices. »* Placement dans notre structure : la divulgation
   responsable et la position IRB font partie du contenu de la section « Ethical Considerations »
   (`\begin{ethics}`) — donc hors limite elle aussi, comme tout ce qu'elle contient. La
   disponibilité du code et des données correspond à la section « Open Science »
   (`\begin{openscience}`, notre §9 Availability) — également hors limite. Aucune des quatre
   choses citées par l'orchestrateur (déclaration éthique, AI Use, divulgation responsable,
   disponibilité) ne pèse donc sur les 12 pages.
4. **Sévérité de la limite** : **stricte, sans tolérance**. Citation exacte : *« Submissions
   exceeding 12 typeset pages for the main body of the paper will be automatically desk-rejected
   without consideration of appeal. »* Aucune marge d'une page n'existe à la soumission (la page
   supplémentaire — 13 pages — n'est accordée qu'au stade de la révision post-notification, pas au
   dépôt initial, cf. §1 ci-dessus). Je n'ai pas trouvé de mention explicite d'une vérification
   *automatique* du nombre de pages par le serveur de soumission (`submit.petsymposium.org`) sur
   cette page — **inconnu**, à ne pas déduire.

### 8.2 Conséquence directe, avant toute recompilation

Sur les quatre sources de croissance listées par l'orchestrateur, **deux ne coûtent structurellement
rien sur les 12 pages** : la section AI Use et le passage éthique reformulé tombent tous deux dans
une zone hors limite par construction du gabarit. Les deux sources qui *peuvent* réellement faire
déborder le corps sont les deux autres : « de nouveaux intervalles de confiance partout » et « une
réécriture de fond du résultat central » — parce que ce sont, par hypothèse, des ajouts *à
l'intérieur* des sections 1 à 7.5.

### 8.3 Squelette mis à jour, recompilé

Le texte de remplissage des sections `\begin{ethics}` et `\begin{ai}` a été recalé sur les comptes
de mots réels des deux textes prêts à coller dans
`article/sections-a-inserer-2026-09-12.md` (et non plus une estimation) :

- **AI Use** : 297 mots (comptés sur le Texte 1 du fichier ci-dessus), contre l'estimation
  initiale de ~400 mots de l'orchestrateur.
- **Ethics — passage IRB reformulé** : le nouveau texte (Texte 2) fait 320 mots contre 75 pour le
  paragraphe qu'il remplace (« IRB determination: a declared gap »), soit **+245 mots nets** dans
  la section Ethics, qui passe de 737 à 982 mots au total — toujours un texte de remplissage
  (aucune transcription), seul le compte de mots cible a changé.

Recompilation complète (`pdflatex → bibtex → pdflatex → pdflatex`), aucune erreur :

| | Avant (§4) | Après (ce complément) |
|---|---|---|
| Pages totales | 15 | **15** (inchangé) |
| **Corps (§1–§7.5, limité à 12)** | 12 | **12 (inchangé)** |
| Ethics + Open Science + AI Use + Références | pages 13–15 | pages 13–15 (réparties différemment, même total) |

**Confirmation empirique de la règle** : faire grossir l'Ethics de +245 mots et l'AI Use de
~+200 mots (par rapport au texte de substitution précédent) n'a déplacé **aucune** page du corps —
exactement ce que prédit la citation du §8.1. La frontière corps/annexe reste au même endroit
(les deux figures se résolvent toujours en page 12, « Ethical Considerations » commence toujours en
page 13).

### 8.4 Chiffrer la réduction nécessaire

**Ce que je peux chiffrer avec les éléments disponibles.** Le corps actuel (9 853 mots, §1–§7.5,
deux figures, un tableau de 16 lignes) occupe déjà l'intégralité des 12 pages autorisées — **la
marge est nulle avant même toute croissance**. Taux de conversion mesuré sur ce document :
9 853 mots ⁄ 12 pages ≈ **821 mots par page** de corps.

**Ce que je ne peux pas chiffrer, et pourquoi je ne l'invente pas.** L'ampleur de « nouveaux
intervalles de confiance partout » et de « une réécriture de fond du résultat central » n'est
donnée nulle part dans les fichiers auxquels j'ai accès en lecture (ni
`article/sections-a-inserer-2026-09-12.md`, qui ne contient que les deux textes Ethics/AI Use, ni
le manuscrit, ni les `[OPEN ITEMS]`) : **inconnu**. Toute estimation chiffrée de ce delta serait une
invention. Dès que ce delta sera connu (nombre de mots ajoutés dans §1–§7.5), il suffit de le
diviser par ≈ 821 pour obtenir le nombre de pages à couper en face.

**Ce qui est déjà mesuré et mobilisable comme réserve de compression, par ordre de priorité** :

1. **Les deux figures (≈ 1 page récupérable, mesuré empiriquement au §4)**. Rappel de
   l'expérience contrôlée : retirer les deux figures en conservant leurs légendes en texte (mêmes
   mots) fait passer le corps de 12 à 11 pages. C'est la réserve la plus sûre scientifiquement :
   aucune perte de résultat, seulement une mise en page plus dense (réduire la largeur d'image,
   fusionner les deux panneaux empilés de la Figure 1 en un format plus compact, ou passer l'une
   des deux figures en position `[H]`/plus petite). **Priorité 1**, car c'est un coût de mise en
   page, pas de contenu.
2. **Le paragraphe « Method note » de §5.7 (52 mots)** — détail procédural pur (erreurs HTTP 402,
   stratégie de relance à concurrence décroissante) : c'est très exactement ce que la règle des
   annexes autorise à déplacer (« extended details that would not be of interest to most
   readers », §8.1 point 2) sans risque, puisqu'aucun résultat n'y est énoncé. **Priorité 2**,
   candidat direct pour un déplacement en annexe plutôt qu'une coupe.
3. **Trois passages spéculatifs identifiés, visés par l'objection du relecteur hostile sur
   l'extrapolation au-delà des mesures** (candidats à la coupe ou à la réduction à une phrase,
   compression totale ≈ 193 mots, non testée en compilation) :
   - §5.2 : l'hypothèse non testée sur la « copie du donneur » expliquant le contraste top-1/top-10
     (87 mots, se termine explicitement par « We have not tested this »).
   - §5.9 : le paragraphe sur l'ajustement loi de puissance / loi logarithmique au-delà de
     N ≈ 4 000 (60 mots, commence par « We extrapolate no value beyond… » — l'aveu même
     d'extrapolation que le relecteur hostile viserait).
   - §7.3 (O2) : l'hypothèse de « l'effet de bloc » présentée comme non testée (46 mots, « not as a
     result »).
   Ce sont des coupes **de contenu**, hors de mon périmètre d'écriture (`article/manuscrit.md` est
   en lecture seule) — signalées ici pour le responsable de la rédaction, pas exécutées.
4. **Les plus longues sous-sections du corps, si une compression plus large est nécessaire** :
   §5.7 (614 mots, le plus long dans son ensemble — la partie narrative sur la tentative de
   reproduction ratée dépasse le strict compte-rendu de résultat), §5.3 (574 mots dont 295 de
   légende Fig. 1), §7.1 (557 mots, tableau inclus — la colonne « Source » du Tableau 3, qui ne
   fait que citer des noms de fichiers internes comme `c7-disjoint-resultats.md §2`, est
   compressible ou déplaçable en note sans perte pour le lecteur), §1.2 Contributions (541 mots).

**Recommandation classée** : (1) comprimer/retailler les deux figures avant toute autre coupe — récupère
≈ 1 page pour un coût scientifique nul ; (2) déplacer le paragraphe « Method note » de §5.7 en
annexe ; (3) une fois le delta réel des nouveaux intervalles de confiance et de la réécriture
connu, le diviser par ≈ 821 mots/page et combler prioritairement avec les trois passages
spéculatifs (§8.4.3) avant de toucher aux sections de résultats factuels ; (4) si la coupe
nécessaire dépasse ce total, resserrer §5.7 et §1.2 en dernier recours, en préservant tout chiffre
cité ailleurs dans le papier (abstract, table 3, discussion) pour ne rien rendre incohérent.

---

## 9. Page mise en banque — compression de la mise en page des figures (2026-09-12, suite)

Demande : réaliser dans le squelette le gain d'≈ 1 page identifié au §8.4.1, mesurer le gain réel,
ne toucher qu'à la mise en page (largeur, placement, compacité), pas au contenu scientifique des
figures, rester robuste à la regénération prochaine de la Figure 2, et écarter toute piste qui
dégraderait la lisibilité en le disant.

### 9.1 Ce qui a été changé — uniquement la mise en page

Deux changements dans `article/latex/main.tex`, tous deux réversibles et localisés aux figures :

1. **Largeur et hauteur déclarées par des longueurs nommées** (`\figwidth`, `\figmaxheight`),
   appliquées aux deux `\includegraphics` avec `keepaspectratio`, au lieu d'un `width=\linewidth`
   ligne à ligne. **Robustesse à la Figure 2 à venir** (point 1 de la demande) : quand le fichier
   sera remplacé, ces deux longueurs s'appliquent sans toucher au code ; seul le rapport
   largeur/hauteur du nouveau PNG changera l'effet de `keepaspectratio`, à revérifier visuellement
   (voir §9.3).
2. **`\FloatBarrier` (paquet `placeins`, déjà installé en mode utilisateur, §2) déplacé de
   « une seule fois, juste avant `\appendix` » à « une fois juste après chaque figure »** — Fig. 1
   se résout maintenant immédiatement après sa propre sous-section (§5.3), Fig. 2 immédiatement
   après la sienne (§5.9), au lieu que les deux dérivent ensemble vers une page dédiée en fin de
   section 7. C'est un changement de **placement**, pas de taille ni d'espacement : `\FloatBarrier`
   ne modifie ni `\floatsep`, ni `\textfloatsep`, ni aucune longueur de mise en page — il force
   seulement l'ordre de résolution des flottants déjà en attente. Je n'ai délibérément touché à
   aucun paramètre d'espacement (`\floatsep`/`\textfloatsep`/`\vspace`) ni à aucune taille de
   police de légende : le gabarit officiel désigne explicitement ce type de manipulation comme
   motif de rejet de bureau (*« manipulate other document properties (e.g., page layout, spacing,
   use the \vspace command, fonts, figures and tables, headings) … will be desk-rejected »*,
   `exemple-gabarit-main.tex` ligne ~149) — d'où le choix de ne jouer que sur le placement et la
   taille déclarative des images, un choix éditorial ordinaire, pas une manipulation.

**Piste explicitement écartée pour cause de lisibilité.** J'ai testé un plafond de hauteur
contraignant (`0.40\textheight`, motivé par l'idée de forcer un gabarit plus compact) : il aurait
réduit la Figure 1 d'environ 25 % en largeur (calcul : à `\linewidth` ≈ 243 pt la Fig. 1 attein-
drait 333 pt de haut, plafonnée à 250 pt par ce réglage, donc ramenée à ≈ 182 pt de large). Or,
mesuré en compilant les deux variantes, **ce plafond ne changeait strictement rien au nombre de
pages** — le gain venait entièrement du placement, pas de la taille. Un plafond contraignant aurait
donc dégradé la lisibilité de la Fig. 1 (déjà dense : deux panneaux empilés, échelle
logarithmique, légende) **pour un gain nul**. Écarté. Le plafond conservé
(`0.85\textheight`) est un garde-fou qui ne se déclenche pour aucune des deux figures actuelles :
leur taille affichée est **strictement identique** à celle du squelette précédent.

**Piste envisagée puis écartée : fusionner les deux figures côte à côte dans un seul flottant
`figure*`** pour partager une même ligne. Calcul de faisabilité : à largeur pleine page partagée
(~3,4 po chacune), la taille par figure serait quasi identique à la largeur de colonne actuelle
(~3,3 po) — donc pas de perte de lisibilité par la taille. Mais les deux figures n'ont **aucun
rapport de contenu** (Fig. 1 : détection en monde ouvert ; Fig. 2 : couplage qualité-fuite) et sont
discutées à six sous-sections d'écart (§5.3 et §5.9) : les rapprocher artificiellement dans un même
bloc pour gagner de la place, sans lien scientifique entre elles, s'apparente à la manipulation de
présentation que le gabarit proscrit plutôt qu'à un choix éditorial ordinaire. Écarté par prudence,
d'autant que le placement seul a déjà donné le gain visé.

### 9.2 Gain mesuré

Recompilation complète (`pdflatex → bibtex → pdflatex → pdflatex`), aucune erreur, aucune figure
tronquée ni redimensionnée par rapport à l'original :

| | Avant compression (§8.3) | Après compression |
|---|---|---|
| Pages totales | 15 | **14** |
| **Corps (§1–§7.5, limité à 12)** | 12 | **11** |
| Position de la Fig. 1 | page 12 (dérivée, isolée) | **page 6** (dans §5.3, entourée de texte) |
| Position de la Fig. 2 | page 12 (dérivée, isolée) | **page 8** (dans §5.9, entourée de texte) |

**Le corps passe de 12 à 11 pages : un plein point de marge acquis, mesuré, pas espéré.** Au taux
de 821 mots/page établi au §8.4, cela équivaut à **≈ 821 mots de marge réelle** avant tout ajout de
contenu. Contrairement à la crainte initiale (« si le gain est nettement inférieur à une page,
dis-le franchement »), le gain mesuré est la pleine page anticipée, obtenu uniquement par un
meilleur placement des flottants — la cause du problème n'était pas la taille des figures, mais le
fait qu'elles dérivaient ensemble loin de leur point de citation, jusqu'à occuper une page presque
vide en fin de corps (diagnostiqué au §8 : c'est exactement le même mécanisme que « l'illusion des
deux pages » repérée avant l'ajout du premier `\FloatBarrier`, réapparu sous une forme plus discrète
avec un `\FloatBarrier` unique mal placé).

### 9.3 À revérifier quand la Figure 2 sera remplacée

1. **Rapport largeur/hauteur du nouveau fichier.** Si le nouveau PNG est nettement plus haut que
   large (contrairement à l'actuel, ≈ carré, 1039×1005), `\figmaxheight` (0.85\textheight, soit
   environ 7,4 po) pourrait cette fois se déclencher et réduire la largeur effective — vérifier
   visuellement après remplacement, et si cela se produit, juger si la lisibilité est encore
   acceptable avant de relever le plafond.
2. **Position de la Fig. 2 après recompilation.** Le `\FloatBarrier` local la maintient près de
   §5.9, mais un fichier de poids ou de proportions très différent peut changer la page exacte
   (actuellement 8) et, en cascade, le nombre total de pages du corps — recompiler et refaire le
   pointage par en-tête (méthode `pdftotext -layout` + recherche de marqueurs de section, décrite
   aux §4/§8) plutôt que de supposer que 11 pages tient encore.
3. **Lisibilité en noir et blanc et légende autoportante** (déjà validées par
   `resultats/conformite-popets-2026-09-12.md` point 10 sur les fichiers actuels) : à
   revérifier sur le nouveau fichier, puisque cette validation portait sur les PNG remplacés
   depuis dans `article/figures/` — pas sur celui qui va arriver.

---

## 10. Correction majeure — les figures étaient invisibles dans le PDF (2026-09-12, repointage après régénération de la Fig. 2)

**Ce qui a déclenché la découverte.** En repointant, comme demandé, la page d'atterrissage de la
Fig. 2 après son remplacement, j'ai pour la première fois **rendu les pages en image et regardé**
plutôt que de me fier au comptage de mots-clés (`pdftotext` + recherche de « Figure 2 ») utilisé
jusque-là. Les deux figures étaient **absentes des pages rendues** — seule la légende (texte
normal) apparaissait. Vérification par `pdfimages -list main.pdf` sur l'ancien PDF : **zéro image
détectée dans tout le document**, alors même que `main.log` rapportait avoir traité les deux
fichiers PNG.

**Cause exacte, dans `main.log`** : `(pdftex.def) Requested size: 0.0pt x 0.0pt.` — les deux
figures étaient demandées à une taille nulle. En relisant le squelette introduit à la section
« page mise en banque » (§9) : `\figwidth` et `\figmaxheight` étaient fixées une fois pour toutes
via `\setlength{...}{\linewidth}` / `\setlength{...}{0.85\textheight}` **dans le préambule, avant
`\begin{document}`** — à cet endroit, `\linewidth` et `\textheight` n'ont pas encore leur valeur
finale de mise en page (acmart les fixe plus tard) : les deux longueurs se figeaient donc à 0 pt,
gelées pour tout le document. **Les deux figures étaient invisibles depuis la modification du
§9, sans qu'aucune vérification antérieure (comptage de pages, recherche de légende) ne le
révèle** — un comptage de pages fondé sur du texte seul ne peut pas détecter une image absente.

**Correction appliquée** : suppression des longueurs nommées figées dans le préambule ; les deux
`\includegraphics` utilisent maintenant directement `width=\linewidth,
height=0.85\textheight, keepaspectratio`, évalués par TeX au bon moment (à l'intérieur du flux
deux colonnes, là où `\linewidth` vaut effectivement la largeur de colonne). Toujours aucune
longueur codée en dur sur les pixels de l'image — la robustesse au remplacement de fichier
demandée reste garantie.

### 10.1 Conséquence : la page « mise en banque » au §9 était une illusion

Une fois les figures réellement visibles, à leur vraie taille : **le corps revient à 12 pages sur
12**, exactement le compte initial d'avant toute optimisation de placement (§4). Le gain d'une
page rapporté au §9 (12 → 11) était entièrement un artefact du bug — les deux images occupaient
0 pt × 0 pt, donc strictement aucune des deux pages qu'elles auraient dû remplir. **Je corrige
formellement l'affirmation du §9 : elle était fausse.** Le `\FloatBarrier` localisé par figure
(placement près de sa propre sous-section plutôt qu'un dépôt groupé en fin de section 7) reste en
place — c'est une amélioration de placement légitime et sans risque — mais, une fois les images
correctement dimensionnées, il ne suffit pas à dégager une page entière : le corps est bien à
12/12, marge nulle.

### 10.2 Repointage demandé, avec la Figure 2 régénérée (1056×1005 px, rapport 1,051)

Recompilation complète (`pdflatex → bibtex → pdflatex → pdflatex`), aucune erreur :

1. **Compte de pages du corps** : **12 sur 12** (pas 11). Page 12 contient à la fois la fin de
   §7.5 et le Tableau 3 ; « Ethical Considerations » commence page 13.
2. **Page d'atterrissage de la Fig. 2** : **page 10** (et non plus 8) — elle a reculé de deux
   pages du seul fait que les deux figures pèsent maintenant leur vrai poids visuel (Fig. 1 en
   page 7, contre 6 auparavant).
3. **Plafond de hauteur `0.85\textheight`** : **ne se déclenche pas**, vérifié plutôt que déduit.
   `main.log` : taille demandée pour la Fig. 2 = 241,16 pt × 229,51 pt ; le plafond
   (0,85 × 626 pt ≈ 532 pt) n'intervient pas, c'est la largeur de colonne qui borne l'image. Le
   nouveau rapport largeur/hauteur (1,051, quasiment identique à l'ancien 1,034) ne change rien à
   ce diagnostic.

**Lisibilité en noir et blanc des deux bandes de témoin.** Page rendue et **zoomée
visuellement** (`pdftoppm` 250 dpi puis recadrage) : l'encart montre une bande claire (gris
pâle, ~[-0,3 ; 0,6] sur l'axe Spearman rho) et, à l'intérieur, une bande plus sombre **avec
hachures diagonales** (~[0,12 ; 0,21]) — les deux se distinguent nettement à la fois par le
niveau de gris et par la texture (hachure), ce qui est robuste même si l'impression réduit le
contraste entre les deux gris. Le point observé (rho ≈ 0,97) apparaît clairement **au-dessus**
des deux bandes, sans chevauchement, conforme à la description du contenu régénéré. **Lisible.**
Aucune piste écartée sur ce point : la figure régénérée passe le contrôle visuel tel quel, sans
retouche de mise en page nécessaire.

### 10.3 Marge réelle en mots

**Nulle.** Le corps occupe exactement 12 pages sur 12 ; il n'y a, à ce stade, aucun mot de marge
acquis — ni les 821 mots annoncés au §9, ni une fraction. Le seul acquis réel de l'exercice de
placement (§9) est que les deux figures se résolvent maintenant chacune près de sa propre
sous-section plutôt qu'ensemble en fin de corps, ce qui est une amélioration de lisibilité de la
mise en page pour le relecteur, mais ne libère plus de page une fois le bug corrigé.

### 10.4 Leçon methodologique pour la suite

Le comptage de pages par recherche de marqueurs textuels (`pdftotext` + repérage de « Figure N »,
utilisé du §4 au §9) **détecte la légende, pas l'image** : une figure invisible ou mal
dimensionnée passe inaperçue tant qu'on ne rend pas au moins une fois chaque page contenant une
figure en image et qu'on ne vérifie pas `pdfimages -list` sur le PDF final. Je m'y astreins
désormais à chaque repointage impliquant une figure.

---

## 11. Script de conversion réel et premier essai à blanc sur contenu réel (2026-09-12, suite)

Mission distincte de celle des §1–10 : ne plus estimer le nombre de pages avec du texte de
remplissage, mais **construire le mécanisme de transfert réel** Markdown → LaTeX, l'éprouver sur
le contenu actuel de `article/manuscrit.md` (lecture seule, en cours de réécriture par un autre
agent pendant cette session — attendu, signalé dans la mission), et rapporter honnêtement ce qui
casse.

### 11.1 Outil retenu : un script Python, pas pandoc

**pandoc n'est pas installé** sur cette machine (`which pandoc` → rien ; pas de formule Homebrew
en cache). L'installer aurait exigé un accès réseau (`brew install pandoc` télécharge une
bottle), exclu par la consigne « local uniquement, aucun appel d'API, aucune recherche web » de
cette mission. Un script Python (bibliothèque standard uniquement, aucune dépendance externe) est
donc l'outil le plus sûr disponible : il ne nécessite aucune installation, et — argument qui
aurait justifié le choix même si pandoc avait été disponible — il donne un contrôle explicite,
étape par étape, sur exactement les points que cette mission demande de vérifier plutôt que de
supposer (résolution des clefs de citation avec liste des échecs, détection des tableaux et
figures avec garde-fous qui échouent bruyamment plutôt que d'inventer, journal des caractères
Unicode non convertis). Un pipeline pandoc générique aurait fait ces mêmes choix silencieusement,
avec ses propres conventions.

Le script est `article/latex/md2latex.py`. **Rejouable** : `python3 md2latex.py` régénère trois
zones explicitement marquées de `article/latex/main.tex`
(`% === GENERATED:ABSTRACT/BODY/BACKMATTER BEGIN...END ===`) à partir de l'état courant de
`article/manuscrit.md`, sans toucher au reste du fichier (préambule, métadonnées ACM, titre,
`\maketitle`, `\appendix`, `\begin{acks}`, bibliographie) — ces parties restent éditées à la main,
car elles ne dérivent pas du Markdown. Il recopie aussi `article/references.bib` vers
`article/latex/references.bib` à chaque exécution (source figée, jamais modifiée).

### 11.2 Citations : correspondance établie, aucune mention non reliée à ce jour

Le script charge les clefs réelles de `references.bib` et une table de correspondance
clef-provisoire → clef-finale recopiée à la main depuis `article/references-verification.md`
(13 entrées, ex. `toubia2025twin` → `toubia2025twin2k500`). Pour chaque mention `[clef]` ou
`[clef1, clef2]` du manuscrit (distinguée par regex des renvois internes type
`[c7-xxx-resultats.md §2]` et des intervalles numériques `[21.5 ; 25.0]`, qui ne matchent pas le
motif), il résout vers la clef finale ou, à défaut, **insère littéralement
`[[CITATION NON RESOLUE: clef]]` en gras dans le PDF et le liste sur stderr** — jamais
d'invention. Sur l'état actuel du manuscrit (41 clefs citées, en légère baisse par rapport aux 41
listées le 12/09 au matin par un autre agent, le contenu ayant été réécrit entre-temps) :
**aucune mention non résolue**. Les 4 entrées de `references.bib` non citées dans le texte
(`ahn2026itemmean`, `wang2026digitaltwins`, `chen2026syntheticusers`, `choi2026beyondmean` — la
« veille d'antériorité » mentionnée en prose sans clef formelle) sont désormais absentes de la
bibliographie imprimée, puisque `\nocite{*}` a été retiré (il n'a plus d'utilité : les vrais
`\cite{}` existent). Point à trancher : faut-il leur ajouter une clef formelle dans le texte ?
Hors de mon périmètre de décision.

### 11.3 Figures : bogue trouvé et corrigé par la compilation, pas supposé

Deux bogues réels ont été trouvés en compilant, exactement comme la leçon du §10 le recommande :

1. **Un vrai bogue de script** (pas de contenu) : la conversion des variables indicées en prose
   (`q_i`, `a_j`, `q_j`, hors blocs de code) s'exécutait *avant* l'échappement générique du
   souligné, si bien que le `_` fraîchement inséré par `$a_{j}$` se faisait lui-même échapper au
   passage suivant, produisant `$a\_{j}$` dans le PDF (rendu cassé, repéré en lisant le `.tex`
   généré, pas en le supposant correct). Corrigé en inversant l'ordre : échapper d'abord, puis
   reconnaître le motif déjà-échappé `lettre\_alnum`.
2. **Un tableau entier absent, pas un bogue** : le petit tableau à 3 colonnes du §5.1 (comparaison
   des témoins corrigés) présent lors de ma première lecture du manuscrit avait disparu de sa
   version actuelle au moment où j'ai recompilé — l'autre agent l'a réécrit entre-temps (1205 →
   1077 lignes, `git diff --stat` : 259 insertions / 290 suppressions sur ce seul fichier pendant
   cette session). Vérifié par `grep` direct sur le Markdown courant, pas supposé : ce n'est pas
   une régression du script, c'est un contenu qui a changé sous mes yeux, comme annoncé dans la
   mission. Le code de rendu de ce tableau reste en place et se redéclenchera automatiquement s'il
   réapparaît (garde-fou : le script échoue bruyamment, `ValueError`, sur tout tableau à un nombre
   de colonnes qu'il ne reconnaît pas — 3 ou 4 — plutôt que de deviner un rendu).

Les deux figures réelles ont été vérifiées **par rendu d'image et `pdfimages -list`**, jamais par
le seul comptage textuel (leçon du §10 appliquée) : les deux sont détectées à une taille non
nulle (Fig. 1 : 1364 × 1872 px, page 6 du PDF ; Fig. 2 : 1056 × 1005 px, page 8), et une inspection
visuelle des deux pages rendues (`pdftoppm` 120–150 dpi) confirme des légendes complètes, lisibles,
avec les pourcentages, crochets d'intervalle, symboles `→`/`×` et tirets correctement typographiés.
**Décision signalée, non tranchée** : le manuscrit ne fournit qu'une seule légende par figure ; le
script réutilise cette légende convertie comme texte de `\Description{}` (accessibilité), faute
d'une description distincte dans la source. Une vraie description d'accessibilité, différente de
la légende, reste à rédiger par le responsable éditorial si souhaité.

### 11.4 Tableau de 16 lignes (Table 3, §7.1) : débordement de colonne trouvé et corrigé

Un vrai débordement a été observé, pas supposé : la première version du tableau (colonnes
`p{0.018}/p{0.30}/p{0.52}/p{0.10}` de `\textwidth`, sans réduire `\tabcolsep`) faisait déborder la
colonne « Source » — qui contient des noms de fichiers `\texttt{}` longs et non coupables par
défaut (ex. `c7-attaquant-fort-resultats.md`, 31 caractères) — **dans la marge des numéros de
ligne** du mode `review` d'acmart, visible par rendu d'image à 300 dpi (six lignes concernées :
#2, #3, #4, #12, #13). Deux causes cumulées, diagnostiquées par compilation réelle : (a) la somme
des largeurs de colonnes ne laissait pas de place pour l'espacement `\tabcolsep` par défaut entre
colonnes ; (b) `\texttt{}` ne coupe jamais un identifiant sans espace, même aux tirets qu'il
contient (l'césure normale de TeX y est désactivée par cette police).

**Corrections appliquées, toutes vérifiées par recompilation** : `\tabcolsep` resserré à 3pt pour
ce tableau ; colonne Source élargie (0.10 → 0.135 puis confirmée suffisante) ; chaque colonne
passée en `>{\raggedright\arraybackslash}p{...}` (nécessite `\usepackage{array}`, absent d'acmart/
popets — ajouté à la main dans le préambule de `main.tex`, seule modification manuelle du
préambule de cette session, documentée en commentaire à cet endroit) ; un point de coupure
autorisé (`\allowbreak`) inséré après chaque `-`, `/` et `_` échappé à l'intérieur de tout
`\texttt{}` généré, en sortie du script (fonction `_escape_texttt`). Résultat : plus aucun
chevauchement avec la marge (vérifié par rendu d'image à 300 dpi après correction) ; le nombre
total de boîtes `Overfull \hbox` du document est passé de 29 à 11, toutes désormais mineures
(< 33 pt, soit < 0,5 cm, dans le corps du texte courant — voir §11.6).

### 11.5 Caractères spéciaux : testé par compilation isolée avant d'écrire la règle

Avant d'écrire la moindre règle de conversion, un fichier `.tex` minimal (même préambule
`acmart`+`popets` que `main.tex`) a été compilé avec chacun des symboles non-ASCII réellement
présents dans le manuscrit (`→ ≈ ≥ − × κ ∞ · §`, tirets cadratin/demi-cadratin, guillemets droits,
lettres accentuées). **Résultat mesuré, pas supposé** : `pdflatex` refuse en erreur fatale
`≈` (U+2248) tel quel (« Unicode character not set up for use with LaTeX ») — et vraisemblablement
`≥ − × κ ∞ ·` pour la même raison, ce format `pdflatex` (pas `xelatex`) n'ayant pas de support
Unicode natif pour les symboles mathématiques. Compile en revanche sans erreur si chaque symbole
est remplacé par sa commande LaTeX (`$\approx$`, `$\geq$`, etc.) — d'où la table de correspondance
`_UNICODE_MATH_MAP` du script. `é`/`è` et `§` compilent tels quels sans conversion. Les tirets
cadratin/demi-cadratin sont convertis en `---`/`--` (ligatures TeX natives, plus sûres qu'un glyphe
Unicode direct) ; les guillemets droits en `` ``/'' `` typographiques ; les pourcentages et
`&`/`#`/`_` restants échappés. Un cas isolé (« 4·10⁻⁴ » en exposant Unicode dans l'ancienne légende
de la Figure 1) a été traité par un remplacement littéral ciblé plutôt qu'un analyseur d'exposants
général — documenté dans le script comme un point fragile : si ce fragment disparaît du manuscrit
(ce qui est arrivé pendant cette session même), le remplacement ne fait simplement rien, sans
erreur ; s'il réapparaît sous une autre forme, il ne serait pas reconnu.

**Garde-fou de bout de chaîne** : après conversion, le script scanne le texte produit et signale
sur stderr tout caractère non-ASCII qui ne soit ni une lettre latine accentuée usuelle ni déjà
retombé dans une commande LaTeX — sur l'état actuel du manuscrit, **aucun caractère non mappé**.
Si une future révision introduit un nouveau symbole (ex. un vrai ρ grec hors des mots « Spearman
rho » épelés, ou un nouvel opérateur), ce garde-fou l'annoncera au lieu de le laisser passer en
silence vers une éventuelle erreur de compilation ou pire, un caractère mal rendu et non détecté.

### 11.6 Sections hors limite : conforme, vérifié une nouvelle fois

`\begin{ethics}…\end{ethics}`, `\begin{openscience}…\end{openscience}` et `\begin{ai}…\end{ai}`
sont générés par le script mais **restent placés après `\appendix`**, comme le squelette du §3
l'avait déjà établi — le script ne fait qu'y injecter le texte réel des sections 8, 9 et 10 du
Markdown, sans déplacer l'ancrage structurel. Repointé sur le contenu réel actuel :
« Ethical Considerations » commence en page 11 (confirmé par recherche textuelle *et* par
cohérence avec le nombre total de pages, qui ne bouge pas entre deux recompilations identiques).

### 11.7 Premier essai à blanc complet sur contenu réel : mesure honnête

Cycle complet (`pdflatex → bibtex → pdflatex → pdflatex`), sans erreur, sur l'état de
`article/manuscrit.md` tel qu'il se trouvait au moment de cette compilation (12/09, environ
11h50 — **un instantané, pas une valeur figée**, le fichier étant réécrit par un autre agent
pendant cette session même : 1205 lignes lors de ma première lecture, 1077 lignes au moment de
cet essai) :

| | Résultat |
|---|---|
| Pages totales | **14** |
| **Corps (§1 à §7.5, limité à 12 pages)** | **10 pages** (« Ethical Considerations » commence en page 11) |
| Ethics + Open Science + AI Use | pages 11–12 |
| Bibliographie (41 entrées citées, sur 46 disponibles) | pages 13–14 |

**Le corps tient à 10 pages sur 12, avec 2 pages de marge apparente** — à lire avec deux réserves
honnêtes plutôt qu'un satisfecit : (1) c'est une mesure sur un contenu *en cours de rédaction*,
pas figé, qui peut encore grossir ou rétrécir d'ici le dépôt ; (2) contrairement à l'essai à blanc
du §4–§10 (texte de remplissage densité homogène), ceci est le **texte réel**, avec ses propres
retours à la ligne, ses tableaux et son vocabulaire — la seule mesure qui compte vraiment, mais
qui doit être refaite à chaque révision substantielle, pas supposée stable.

### 11.8 Dix points à trancher (liste honnête, rien de bricolé en douce)

1. **4 entrées de `references.bib` non citées** (`ahn2026itemmean`, `wang2026digitaltwins`,
   `chen2026syntheticusers`, `choi2026beyondmean`) : la « veille d'antériorité » les mentionne en
   prose sans clef `\cite{}` formelle. Sans `\nocite{*}`, elles n'apparaissent plus dans la
   bibliographie imprimée. À décider : leur donner une clef formelle dans le texte, ou les laisser
   hors bibliographie.
2. **`gouweleeuw1998pram` sans DOI** — déjà signalé dans `article/references-verification.md`,
   toujours ouvert, non résolu par ce travail (hors de mon périmètre : je n'ai pas fait de
   recherche web).
3. **`\Description{}` des deux figures = légende réutilisée**, faute d'une description
   d'accessibilité distincte dans le manuscrit. À rédiger séparément si souhaité.
4. **Le petit tableau à 3 colonnes du §5.1** (comparaison des témoins) a disparu du manuscrit
   pendant cette session (réécriture concurrente) ; le mécanisme de rendu n'a donc été éprouvé de
   bout en bout, sur du contenu réel, que sur le tableau à 16 lignes — pas sur celui-là. Il se
   redéclenchera automatiquement s'il revient sous la même forme (3 colonnes), mais ce n'est pas
   vérifié sur son contenu réel actuel.
5. **11 boîtes `Overfull \hbox` résiduelles**, toutes mineures (0,2 pt à 33 pt, soit jusqu'à
   ~0,5 cm), réparties entre le corps (ex. la liste des contributions en gras du §1.2, ligne
   103–106 du `.tex` généré ; une phrase avec `erreur_correlations_hum` au §6.3) et l'arrière-texte
   (`Availability`, listes de fichiers de préenregistrement). Aucune ne chevauche visiblement la
   marge après les corrections du §11.4, mais un dernier passage visuel page par page est
   recommandé une fois le contenu figé.
6. **Auteurs/affiliation encore « Anonymous Author(s) »** — correct pour la relecture en double
   aveugle (`anonymous,review` dans `\documentclass`), à lever uniquement à la version finale.
7. **Artefacts de compilation** (`main.aux`, `.bbl`, `.blg`, `.log`, `.out`) laissés dans
   `article/latex/` après cet essai — à purger avant tout dépôt (ils se régénèrent à chaque
   compilation).
8. **Le script suppose qu'un seul type de contenu se cache derrière chaque marqueur Markdown**
   (tout bloc `>` est une figure, tout tableau a 3 ou 4 colonnes) et échoue bruyamment sinon
   (`ValueError` explicite) plutôt que de deviner. Si le manuscrit final introduit une vraie
   citation en bloc, un tableau à un autre nombre de colonnes, ou une troisième figure, le script
   s'arrêtera avec un message clair — c'est voulu, mais cela veut dire qu'il faudra l'étendre à ce
   moment-là, pas juste le relancer.
9. **Le manuscrit change pendant que ce rapport est écrit** (un autre agent le réécrit en ce moment
   même). Chaque nombre de ce §11 est donc un instantané daté, pas une mesure finale. Aucune
   décision de contenu (couper, reformuler) n'a été prise ici : mon périmètre s'arrête à la
   mécanique de transfert.
10. **`popets.sty`/`acmart.cls` génèrent eux-mêmes plusieurs avertissements BibTeX bénins**
    (champs `pages`/`volume`/`publisher` manquants sur une quinzaine d'entrées, ex.
    `park2024agents`, `toubia2025twin2k500`) — déjà présents dans le `.bib` fourni, non liés à la
    conversion, listés ici pour mémoire plutôt que traités (hors de mon périmètre d'écriture sur
    `references.bib`).

### 11.9 Marche à suivre pour rejouer le transfert (dans l'ordre)

```bash
cd article/latex

# 1. Regenerer les trois zones marquees de main.tex depuis l'etat courant du
#    manuscrit, et copier references.bib. Lire le rapport stderr avant de
#    continuer : il doit annoncer 0 citation non resolue et 0 caractere non
#    mappe, sinon corriger CITATION_RENAME ou _UNICODE_MATH_MAP en premier.
python3 md2latex.py

# 2. Cycle de compilation complet (necessaire a chaque fois : les cles de
#    citation et les numeros de page ne se stabilisent qu'apres ce cycle).
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex

# 3. Nombre de pages du corps -- PAS le total : chercher la page ou commence
#    "Ethical Considerations", pas se fier au seul compteur de pages total.
pdftotext -layout main.pdf /tmp/main.txt
python3 -c "
pages = open('/tmp/main.txt', encoding='utf-8').read().split('\x0c')
for i, p in enumerate(pages, 1):
    if 'Ethical Considerations' in p:
        print('Ethical Considerations begins on page', i, '-> corps =', i - 1, 'pages')
"

# 4. Figures : ne jamais se fier au texte seul (lecon du §10). Verifier une
#    taille reellement non nulle, ET regarder l'image.
pdfimages -list main.pdf                 # doit lister 2 images, largeur/hauteur > 0
pdftoppm -png -r 150 -f <page_fig1> -l <page_fig1> main.pdf /tmp/fig1
pdftoppm -png -r 150 -f <page_fig2> -l <page_fig2> main.pdf /tmp/fig2
# puis inspecter les deux PNG visuellement.

# 5. Tableau(x) : rendre la page contenant Table 3 (et le petit tableau du
#    §5.1 s'il est revenu) a 300 dpi et verifier a l'oeil qu'aucune colonne
#    ne chevauche la marge des numeros de ligne (mode review).
pdftoppm -png -r 300 -f <page_table> -l <page_table> main.pdf /tmp/table

# 6. Boites Overfull/Underfull : relever celles au-dessus de ~20pt et les
#    verifier visuellement (la plupart sont cosmetiques, mais pas toutes).
grep -c "Overfull\|Underfull" main.log

# 7. Avant tout depot : purger les artefacts de compilation.
rm -f main.aux main.bbl main.blg main.log main.out comment.cut
```

Trancher les dix points du §11.8 (en particulier le placeholder `\Description{}`, les 4 entrées
bibliographiques non citées, et l'auteur anonyme à lever) reste un choix éditorial, pas un défaut
de la mécanique — celle-ci est maintenant éprouvée de bout en bout sur du contenu réel.

---

## 12. Manuscrit figé : compte de pages tranché, finitions de mise en page, contrôle d'anonymat sur le PDF (2026-09-12, suite)

Mission distincte : le manuscrit est déclaré figé et vérifié trois fois ; il s'agit de produire le
PDF de soumission, de trancher sans ambiguïté le compte de pages du corps, de soigner la mise en
page (jamais le texte), et de refaire le contrôle d'anonymat directement sur le PDF plutôt que sur
le Markdown. Cycle complet (`python3 md2latex.py` puis `pdflatex → bibtex → pdflatex → pdflatex`),
sans erreur, sur l'état actuel de `article/manuscrit.md` (1195 lignes, arbre de travail propre,
dernier commit `edbc445`).

### 12.1 Le compte de pages, tranché par rendu, pas par recherche textuelle

**12 pages, pas 11.** Méthode : `pdftotext -layout` a d'abord signalé « Ethical Considerations »
en page 12 (recherche par page isolée, `-f N -l N`, pour éviter tout risque de mauvaise attribution
de page par l'extracteur) — mais la leçon du §10 interdit de s'arrêter là. Page 12 rendue en image
(`pdftoppm` 150 dpi) et regardée : elle contient la fin de §7.3, la totalité de §7.4 (deux
paragraphes complets, dont un bloc en gras), remplissant toute la colonne de gauche et les deux
tiers de la colonne de droite, avant que « Ethical Considerations » ne commence. Ce n'est donc pas
une page où le corps déborde de deux lignes perdues : c'est une page dont l'essentiel du contenu
est le corps.

**Ce qui explique l'écart 11/12 rapporté par l'orchestrateur.** Le script du §11.9 (§3, commande
finale) calcule le compte de pages du corps par `i - 1`, où `i` est la page où commence « Ethical
Considerations » — une formule correcte **seulement si** cette section démarre en haut d'une page
neuve. Ici, ce n'est pas le cas : elle démarre au milieu de la page 12. Appliquer `i - 1` avec
i = 12 donne 11, un chiffre **faux** dans ce cas précis, puisqu'il prétend que la page 12 n'appartient
pas au corps alors qu'elle en contient l'essentiel. Le compte juste est `i` lui-même dès que la page
`i` contient du texte de corps réel (vérifié par rendu, pas supposé) : **12**. C'est un vice de la
formule de raccourci, pas un vice de la mesure sous-jacente — les deux précédentes valeurs
rapportées par l'orchestrateur (13 puis 12) reflètent, elles, deux états différents du manuscrit à
deux moments différents (avant/après les corrections de placement des figures des §9-10), pas une
erreur de méthode.

**Règle PoPETs applicable, déjà établie au §8.1 et reconfirmée ici sans nouvelle recherche
(aucune recherche web dans cette mission)** : la bibliographie, les annexes et les trois sections
obligatoires (éthique, open science, AI use) sont hors limite ; le corps (résumé inclus, §1 à §7.5,
figures et tableaux compris) ne doit pas dépasser 12 pages composées, sous peine de rejet de bureau
automatique et sans appel. **Verdict : 12 pages sur 12, marge nulle** — exactement la situation
déjà caractérisée au §10.3, inchangée par les finitions de mise en page de cette session (aucune
n'a déplacé la frontière corps/annexe, voir §12.3).

### 12.2 Vérifications par rendu réel (pas par comptage textuel)

- **Citations** : `md2latex.py` rapporte 0 citation non résolue ; confirmé par recherche du jeton
  `CITATION NON RESOLUE` sur le texte extrait du PDF final — 0 occurrence.
- **Figures** : `pdfimages -list` sur le PDF final liste bien 2 images de taille non nulle
  (Fig. 1 : 1350 × 1872 px, page 6 ; Fig. 2 : 1062 × 1005 px, page 9), et les deux pages ont été
  rendues et regardées (`pdftoppm` 150 dpi) : légendes complètes, lisibles, chiffres et symboles
  corrects. Les deux figures tombent dans la sous-section qui les discute (Fig. 1 en §5.2/§5.3,
  Fig. 2 en §5.8/§5.9), pas dérivées en fin de section.
- **Tableau** (Table 1, dix-sept lignes de prédictions, §7.1) : rendu et regardé en page 11 — tient
  entièrement sur une page, en-têtes lisibles, colonne Source enveloppée proprement sur les traits
  d'union, aucun débordement dans la marge des numéros de ligne (mode `review`).
- **Renvois** : aucun `Rerun to get cross-references right` dans le journal final (3 passes
  `pdflatex` suffisent, cycle stable) ; aucune étiquette `Undefined` trouvée par grep sur
  `main.log`.
- **15 pages au total**, inchangé par les finitions ci-dessous.

### 12.3 Finitions de mise en page appliquées (dans `md2latex.py`, jamais dans le texte)

Toutes vérifiées par recompilation complète et, pour les deux premières, par rendu d'image avant/
après — aucune n'a déplacé la frontière du corps (toujours page 12) ni la position des figures
(toujours pages 6 et 9).

1. **Espace insécable avant `%`.** Le manuscrit écrit systématiquement « 20.7 % » avec un espace
   normal, donc coupable en fin de ligne (le « % » pouvait atterrir seul en début de ligne
   suivante). `_escape_latex_specials` insère maintenant un `~` (`re.sub(r"(\d) %", r"\1~%", text)`)
   avant l'échappement du caractère — mise en page seulement, aucune valeur numérique changée.
2. **Intervalles `[a ; b]` rendus insécables.** Même défaut potentiel autour du « ; » séparant les
   deux bornes d'un intervalle de confiance (84 occurrences dans le manuscrit actuel, toutes de la
   forme exacte `[NUM ; NUM]`, vérifié par grep avant d'écrire la regex). `convert_inline` applique
   maintenant `[\1~;~\2]` sur ce motif, avant toute autre transformation — un intervalle ne peut
   plus se couper entre ses deux bornes.
3. **`Overfull \hbox` : de 9 à 7, les deux plus grosses éliminées.** Les neuf boîtes déjà signalées
   par l'orchestrateur ont été mesurées une à une (`grep -n Overfull main.log` puis contexte). Sept
   sont mineures (1.1 pt à 5.3 pt, moins de 0,1 mm à 0,7 mm — invisibles à l'œil, dans la tolérance
   normale de justification à 9 pt sur deux colonnes) et laissées telles quelles : les réduire à zéro
   exigerait de reformuler des phrases, hors de mon périmètre. Les deux grosses (32.65 pt et
   32.29 pt, dans la section Open Science, sur l'énumération des cinq fichiers de préenregistrement
   en `\texttt{}`) ont été corrigées en deux temps : (a) un point de coupure autorisé ajouté avant
   chaque `.` à l'intérieur d'un `\texttt{}` (comme déjà fait pour `-` et `/` au §11.4) — premier
   essai rejeté après rendu d'image, car il coupait `.md` en deux (`.` en fin de ligne, `md` seul au
   début de la suivante) ; corrigé en plaçant la coupure **avant** le point plutôt qu'après, pour
   que l'extension reste un seul bloc ; (b) la section Open Science entière enveloppée dans
   `\begin{sloppypar}...\end{sloppypar}` (assouplissement local de la tolérance de justification,
   aucun mot ni caractère modifié), qui a fait disparaître les deux dernières grosses boîtes. Résultat
   final : 7 boîtes, toutes sous 5,3 pt, vérifiées par rendu d'image de la page concernée (aucune
   ne mange l'espace inter-colonnes visible).
4. **Liens et renvois** : `acmart.cls` fixe déjà `colorlinks` avec `linkcolor=ACMPurple`,
   `citecolor=ACMPurple`, `urlcolor=ACMDarkBlue` — pas de soulignement, palette sobre imposée par le
   gabarit. Non modifié (le gabarit est imposé, voir consigne de cadrage).
5. **Veuves/orphelines et titres de section isolés** : recherché par lecture de page rendue sur les
   15 pages du document (pas seulement les pages déjà citées ailleurs dans ce rapport) — aucun
   titre de section ou sous-section trouvé seul en bas de colonne, aucune ligne isolée flagrante
   repérée. `acmart`/`popets` héritent des réglages `\clubpenalty`/`\widowpenalty` standards d'ACM,
   non modifiés.

### 12.4 Contrôle d'anonymat, refait sur le PDF

Page de titre rendue et regardée : **« Anonymous Author(s) »**, aucune affiliation, aucun ORCID ;
en-tête courant **« Anon. »** sur toutes les pages impaires, nom du papier seul sur les pages
paires — cohérent avec `\documentclass[sigconf,anonymous,review]{acmart}`, non modifié. Aucune URL
personnelle ni identifiant nominatif trouvé dans le corps. Le seul lien de la page de titre est la
licence CC BY générique et un DOI placeholder (`10.XXXXXXX.XXXXXXX`), tous deux non identifiants.
**Anonymat du corps intact.**

### 12.5 Deux problèmes de contenu trouvés en vérifiant le rendu, signalés et non corrigés

Hors de mon périmètre d'écriture (`article/manuscrit.md` et `article/references.bib` sont en
lecture seule) — signalés pour décision de l'orchestrateur, pas forcés.

1. **48 renvois internes `[c7-xxx-resultats.md §N]` imprimés tels quels dans le corps du PDF**,
   confirmé par rendu d'image (visibles pages 1, 6, 9, 12 entre autres, pas seulement par grep sur
   le Markdown). Ce sont des noms de fichiers internes du dépôt (dont plusieurs datés
   `2026-09-1x.md`), pas des citations académiques : un relecteur PoPETs sans accès au dépôt ne peut
   rien en faire, et leur présence expose la mécanique de travail interne (dates, arborescence de
   fichiers `resultats/`) dans un document qui doit rester anonyme et fini. Cela ne révèle aucune
   identité, mais nuit à la présentation professionnelle attendue d'une soumission. Décision hors de
   mon périmètre : les convertir en notes de bas de page génériques, les retirer, ou les assumer
   comme choix éditorial délibéré (traçabilité interne).
2. **13 entrées de `references.bib` portent un champ `note={}`, dont au moins 7 sont des notes de
   vérification interne de l'auteur plutôt que des précisions bibliographiques usuelles** — certaines
   rédigées en français dans un article en anglais (ex. `drechsler2024thirtyyears` : « L'identifiant
   2409.04257 donné initialement désigne un autre article (Raab, 2024) ; corrigé ici en
   2304.02107 » ; `hu2023microdata` : « Premier auteur Hu, non Bowen ; cité comme "Bowen et al."
   dans resultats/article-travaux-connexes.md » ; `guepin2023synthetic`, `dwork2015robust`,
   `shafieinejad2026diffusion`, `gouweleeuw1998pram`, `aapor2026responsibleai` de même nature).
   Confirmé par rendu de page (page 14 et page 15 du PDF, section References) : ces notes
   s'impriment mot pour mot dans la bibliographie soumise. Les 6 autres notes (`chen2026...`,
   `park2024agents`, `zhang2024satml`, `das2024blind`, `bun2014fingerprinting`,
   `peng2026funhouse`) sont des précisions bibliographiques usuelles (statut de préprint, titre de
   version, venue secondaire) et ne posent pas ce problème. Décision hors de mon périmètre : retirer
   ou déplacer hors du champ `note` les 7 annotations de vérification avant dépôt.

### 12.6 PDF final

`article/latex/main.pdf` — **15 pages au total, corps = 12 pages (marge nulle), 0 erreur de
compilation, 0 citation non résolue, 2 figures à taille réelle et bien positionnées, anonymat
intact**. Régénérable à l'identique par la marche à suivre du §11.9 (`python3 md2latex.py` puis le
cycle de compilation en 4 commandes) ; les artefacts de compilation (`main.aux`, `.bbl`, `.blg`,
`.log`, `.out`, `comment.cut`) sont actuellement présents dans `article/latex/` pour traçabilité et
restent, comme déjà noté au §11.8 point 7, à purger juste avant tout dépôt effectif.
