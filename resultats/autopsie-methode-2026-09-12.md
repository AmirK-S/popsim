# Autopsie de la méthode — journée du 11-12 septembre 2026

Document d'autopsie, pas de bilan. Écrit en lecture seule sur tout le dépôt à l'exception de
ce fichier. Aucun appel d'API, aucune recherche web, aucun commit, tout en avant-plan.
Reconstitution faite à partir de l'historique git (`git log --format='%h %ad %s' --date=iso`),
des en-têtes de rétractation, des CSV et des rapports datés — pas à partir des récits de
synthèse.

**Critère de réussite que je me suis donné** : qu'un lecteur hostile puisse dire « oui, c'est
là que ça a cassé, et voilà ce qu'il fallait faire ». Là où une défaillance signalée n'est pas
réelle, je le dis (§4). Là où j'en ai trouvé une plus grave, je la mets en tête (§3.0).

**Limites de cette autopsie.** Je ne peux pas mesurer le coût en jetons des agents : le dépôt
n'en conserve aucune trace (§4.2). Les durées d'agent sont inférées des horodatages de commit,
qui bornent le travail par le haut et non par le bas. Aucun chiffre de ce document n'est
calculé par moi : tous sont recopiés d'une source nommée, et quand deux sources divergent je
donne les deux.

---

## 1. Chronologie factuelle de la journée

Reconstituée aux horodatages de commit. Les heures sont locales (+02:00).

| Heure | Événement | Preuve |
|---|---|---|
| 11/09 14:24 | Dernière lecture `total_usage` avant la nuit : 149,259526975 | `cout-api-2026-09-12.md` §1 |
| 11/09 20:11–20:18 | Préenregistrements C7, C5, B123 commis, puis leurs résultats | `0fd3c16`, `e2c6865`, `bb952d3`, `931916c`, `a4ca147` |
| 11/09 22:53 – 12/09 01:43 | Six expériences payantes (C5-API, mémoire long, C7-gen, C7-recette) | `cout-api-2026-09-12.md` §2 |
| 12/09 00:33 – 02:31 | ~20 préenregistrements C7 commis, chacun avant son résultat | `git log` |
| 12/09 06:51–07:14 | C7-fort, 4,9949 USD | `c7-fort-resultats.md` |
| 12/09 ~11:20–11:23 | `c7-nul-corrige.csv` et `-resultats.md` produits sur disque | `audit-renversement` §0 |
| 12/09 11:25–11:36 | Audit adverse ; `manuscrit.md` modifié à 11:34 **pendant** l'audit | `audit-renversement` §0 |
| 12/09 11:39 | Trois préenregistrements commis « horodatage séparé des résultats » | `5c4cef4` |
| 12/09 12:46 / 12:52 | Préenregistrements « deux organisations » puis « factoriel » | `24cc79d`, `ff90409` |
| 12/09 13:25 | **Manuscrit révisé et commis avec « A7 détruite », T2 « réfutée »** | `09b18d7` |
| 12/09 16:46 | Résultats du plan factoriel | `ee73f70` |
| 12/09 17:00 | **Arbitrage : les deux bras payés mesuraient du bruit** | `5f6da6e` |
| 12/09 17:06 / 17:08 / 17:12 | Rétractation de 3 rapports publics ; suspension de A7 ; compteur à 14 | `d8e0daf`, `d11e670`, `8df4e68` |
| 12/09 17:11 | Le contrôle gratuit est écrit — **après** | `28405b2` |
| 12/09 17:30 / 17:48 | Reproductibilité : trou bloquant, puis sauvetage des scripts | `547655a`, `d5980b1` |
| 12/09 17:35 / 17:44 | Un intervalle unifié ; lettres vérifiées trois fois | `7f22fce`, `aa97d1f` |

La forme de cette journée est lisible d'un coup d'œil : **tout ce qui a été produit entre
00:33 et 13:25 a été écrit, publié et poussé sur GitHub ; tout ce qui s'est passé entre 17:00
et 18:50 est de la réparation.** Cinquante minutes d'arbitrage ont annulé dix-sept heures de
production.

---

## 2. La défaillance la plus coûteuse, et celle qui a failli l'être davantage

### 2.0 En tête : le contrôle gratuit écrit six heures après les deux expériences qu'il aurait arrêtées

**Ce qui s'est passé.** Deux campagnes payantes — le témoin « deux organisations » (B↔C) et le
plan factoriel un-facteur-à-la-fois (B↔M, B↔G, B↔P) — ont mesuré un contraste entre jumeaux
que nous avions régénérés, sans que personne ne vérifie d'abord que ces jumeaux portaient une
personne. Ils n'en portaient aucune.

**La preuve, chiffrée.** `c7-reconciliation-facteurs-2026-09-12.md` §3, sur le pool de 120
humains réels de la vague 4, mêmes 60 items :

| jumeau | top-1 contre les humains réels | IC 95 % |
|---|---|---|
| B (deepseek, persona JSON) | 0,79 % | [0,00 ; 2,17] |
| C (qwen, persona narrative) | 0,29 % | [0,00 ; 0,87] |
| M, G, P | 0,29 / 0,00 / 0,54 % | — |
| *hasard (1/120)* | *0,83 %* | |
| Demographics Only (14 champs) | 13,29 % | [7,50 ; 19,79] |
| JSON Persona - GPT4.1 (équipe Twin) | 38,92 % | [30,96 ; 47,08] |

Un jumeau qui ne connaît que quatorze champs démographiques retrouve la bonne personne 13,3 %
du temps ; les nôtres, qui recevaient **494 items de contexte de la même personne**, la
retrouvaient au taux du hasard. Pour B↔M, l'apport individuel mesuré est **exactement nul**
(51,1 % d'accord au vrai jumeau, 51,1 % à un inconnu du même segment). Les contrastes
comparaient deux générateurs de bruit.

**Le coût réel.**

- **Dépense rendue nulle : 1,0928 USD** — `c7-deux-organisations` 0,5541898180 USD
  (`c7-deux-organisations-resultats.md`) + `c7-factoriel` 0,5385601250 USD
  (`c7-factoriel-resultats.md`). Soit **10,4 % de la dépense de la journée** (§7).
- **Trois rapports publics rétractés**, déjà poussés sur GitHub, qui affirmaient sans
  avertissement des conclusions invalidées (`d8e0daf`).
- **Une contribution retirée du manuscrit** : A7/T2 passe de « réfutée » à « non testable —
  limite de notre instrument, pas résultat sur le monde » (`d11e670`, `8df4e68`).
- **Une lettre de divulgation à Columbia annonçait une réduction de menace** fondée sur ce
  témoin, et a dû être remplacée par une rétractation (`d11e670` : « La lettre a Columbia
  annoncait une reduction de la menace que nous leur avions signalee, fondee sur un temoin que
  l'arbitrage a invalide »). C'est le coût le plus lourd : il était sorti du dépôt.
- **Sept requalifications** dans le document de positionnement et autant dans le document
  d'entrée ; le compteur de réfutations redescendu de 15 à 14.
- **Temps** : 12:52 → 17:12, soit **4 h 20** entre le préenregistrement du bras factoriel et sa
  requalification, dont l'arbitrage, la note de réconciliation, l'écriture et le test du
  contrôle, et quatre commits de rétractation.

**Quand cela pouvait être détecté.** Avant le premier appel payant, pour zéro dollar. Le
contrôle appliqué rétrospectivement arrête **5 jumeaux sur 5**
(`controle-interpretabilite-2026-09-12.md` §5 : « les cinq lèvent
`EchecControleInterpretabilite` »). Il coûte un pilote de quelques dizaines de personnes et
une fonction de trente lignes.

**Pourquoi il ne l'a pas été — cause structurelle, pas négligence.** Le préenregistrement du
bras factoriel est **le meilleur du dépôt** : commis seul, avant tout appel payant, et le
script producteur de résultats n'existait pas dans le dépôt à ce commit — c'est le seul cas
dont l'antériorité soit *prouvée* et non déclarée (`preenregistrements-recueil` §2.4). La
discipline a donc été parfaitement respectée, **et n'a servi à rien**, parce que le
préenregistrement préenregistrait l'hypothèse et jamais l'instrument. Il projetait des top-1
de 20 %, 15 % et 8 % pour les trois conditions, a mesuré 0,67 %, 0,83 % et 2,65 %, et a lu ces
valeurs comme trois réfutations. Aucune ligne du préenregistrement ne demandait : *ce
générateur transporte-t-il quoi que ce soit de la personne ?*

Second mécanisme, documenté deux fois dans la même nuit : **la baseline dépend du bassin** —
2,13 % à 2 058 personnes, 9,20 % à 200, 13,29 % à 120
(`c7-reconciliation-facteurs` §5). Le factoriel a comparé un top-1 **jumeau↔jumeau** à une
baseline **jumeau→humain** (13,29 %), alors que la baseline homogène au même bassin vaut
23,69 à 34,42 % ; le moonshot a comparé des paliers à pool 2 058 à la baseline d'un pool de
200. Une comparaison à la baseline d'un autre bassin suffit à inverser une conclusion, et
c'est arrivé.

### 2.1 Le quasi-sinistre plus grave que tous les autres : le chiffre qui porte le titre n'existait que dans un répertoire temporaire

Je le place ici parce que sa gravité potentielle dépasse tout le reste, et qu'il n'était pas
dans la liste.

**Ce qui s'est passé.** Le couple « témoin corrigé rho 0,974 [0,950 ; 0,993] contre 0,965
observé » fonde la réfutation de la prédiction (b), donc la contribution centrale, donc le
titre de l'article. `article-synthese.md` le désigne comme « chiffre qui fait autorité ». Les
scripts qui le produisent — `audit2.py`, `audit3.py`, `audit_contre_nul.py` — **n'ont jamais
été commis** : ils n'existaient que dans le scratchpad d'une session.

**La preuve.** `reproductibilite-chaine-2026-09-12.md` §5 : `git ls-files | grep -iE
"audit2|audit3|audit_contre_nul"` → vide. Et `audit-renversement` le dit lui-même en deuxième
ligne : « scripts d'audit dans le scratchpad de session ».

**Le coût.** Nul, parce qu'il a été rattrapé — mais par accident de calendrier. Le sauvetage
(`sauvetage-scripts-temoin-2026-09-12.md`) a retrouvé les trois scripts dans **un seul**
répertoire de session, celui qui était encore vivant. Un relecteur d'artefact PoPETs clonant le
dépôt public n'aurait pas pu rejouer le calcul le plus important de l'article, et les fichiers
« auraient disparu avec la session » (`547655a`). C'est la seule défaillance de la journée dont
la conséquence aurait été irréversible.

**Pourquoi.** Même cause que §2.0 vue d'un autre angle : un nombre pouvait faire autorité sans
qu'aucune règle n'exige qu'il ait un producteur versionné. Le contrôle « ce chiffre est-il
rejouable depuis un clone nu ? » n'existait nulle part, et n'a été exécuté qu'une fois, tard,
parce qu'un agent en avait reçu la mission explicite.

---

## 3. Les autres défaillances, avec preuve, coût, et cause

### 3.1 Deux conclusions écrites dans le manuscrit avant d'être auditées, donc deux annulations complètes

**Épisode A — le renversement du nul de marge.** `c7-nul-corrige-resultats.md` §7 prescrivait
six modifications de l'article : le **titre**, le **résumé**, le **tableau 3**, la **figure 2**,
et le passage de seize à quinze réfutations. L'audit adverse a été contraint d'écrire, en
section 0 de son propre rapport, un ordre d'arrêt à des agents qu'il ne pouvait pas joindre :
« **Si le §7 de `c7-nul-corrige-resultats.md` est en train d'être appliqué au manuscrit, il
faut l'arrêter maintenant** » — pendant que `manuscrit.md` (11:34), `article-synthese.md`
(11:35) et `figures_article.py` (11:34) étaient modifiés par d'autres agents.

L'auteur du renversement a concédé intégralement : « **Mon renversement tombe** »
(`c7-nul-corrige-reponse-audit.md`). Et il a concédé le point le plus dur : « Le §8 de mon
préenregistrement disait qu'un nul correct détruit les deux axes, donc que le dépasser était
presque acquis d'avance. […] **Un test qui ne peut pas échouer ne démontre rien.** » Autrement
dit, **l'objection qui détruisait le résultat était écrite par son auteur dans son propre
préenregistrement, avant le calcul, et le résultat a été publié quand même**
(`audit-renversement` §5 : « L'auteur a écrit l'objection qui détruit son propre résultat, puis
a publié le résultat quand même »).

*Annulé* : les six modifications du §7, l'« issue B », la « thèse soutenue faiblement ».
*Coût de calcul brûlé* : **deux exécutions complètes de `c7_nul_corrige.py` à 3 977 s chacune**
(`c7-nul-corrige-resultats.md`, en-tête de reproductibilité), soit **2 h 12 de calcul** pour un
rapport rétracté — la double exécution ayant servi à prouver la reproductibilité bit à bit d'un
résultat faux.
*Traces résiduelles* : `revue-hostile-gel` D1 montre que le manuscrit a fini par porter **les
deux paires de chiffres à la fois** — 0,984/0,969 en introduction et dans le tableau 1,
0,974/0,965 au résumé et en §5.1 — et la revue qualifie ce défaut de « le plus humiliant du
lot », parce que §10 met en avant, comme preuve de sérieux, la découverte de ce défaut précis.

**Épisode B — « A7 détruite ».** Le manuscrit a été révisé et commis à 13:25 (`09b18d7`) avec
« Seul resultat neuf, et il est negatif : le scenario "deux organisations" (A7/T2) a ete teste
et refute » — et la lettre à Columbia est partie en brouillon sur cette base. L'arbitrage
l'invalide à 17:00. *Annulé* : la contribution, la ligne 17 du tableau, la phrase de la lettre,
sept requalifications dans deux documents, le compteur de réfutations.

**Pourquoi.** Dans les deux cas, l'écriture dans le livrable était **concurrente** de la
vérification, et non postérieure : cinq agents écrivaient simultanément dans `manuscrit.md`
(`preenregistrements-recueil` §1), sans verrou, sans registre, sans état de fraîcheur. Un
auditeur ne disposait d'aucun moyen d'arrêter une propagation en cours autre que d'écrire une
phrase en majuscules dans un fichier que les autres agents ne liraient peut-être pas. C'est un
défaut d'outillage, pas de vigilance.

### 3.2 Des chiffres propagés de rapport en rapport sans source unique de vérité

**La preuve la plus nette** : la même grandeur — top-1 du jumeau JSON Persona GPT4.1 sur
Twin-2K-500 — portait **quatre intervalles de confiance incompatibles** issus de quatre
exécutions de bootstrap : [19,1 ; 22,5] au §5.2 du manuscrit, [19,0 ; 22,4] au §6,
[18,96 ; 22,43] dans le CSV source, [19,0 ; 22,5] dans la lettre de divulgation
(`contre-verification-lettres` ligne 1 ; `7f22fce`). Et le taux lui-même s'écrivait de trois
façons : 20,68 %, 20,69 %, 20,7 % (`revue-hostile-gel` D8).

**Comment un chiffre non sourcé entre dans la chaîne — le mécanisme, en trois pas, tous
documentés :**

1. **Chaque ré-implémentation refait son propre bootstrap** et publie sa propre valeur, sans
   que rien ne désigne laquelle fait autorité. Le témoin corrigé vaut 31,62 % chez l'auditeur
   (20 réplicats) et 31,15 % chez l'auteur (10 réplicats) ; `audit-chiffres` §3.4 conclut :
   « **rien dans le dépôt ne réconcilie les deux implémentations** ». Aucun CSV ne porte ce
   témoin : il n'existe que sous forme de deux tableaux dans deux rapports
   (`contre-verification-lettres` §5).
2. **Une valeur est ensuite recopiée depuis le rapport le plus proche, pas depuis la source.**
   La lettre 1 cite le PMM à 0,21 % — « la seule des trois valeurs qui vient d'un rapport
   **rétracté** » — alors que le manuscrit dit 0,23 % (`contre-verification-lettres` ligne 4).
   Même mécanisme pour l'IC de 0,965 : repris d'un CSV rétracté, alors que le manuscrit réserve
   cet intervalle à une autre grandeur (0,969, items disjoints).
3. **Les valeurs se croisent entre sources et fabriquent un chiffre qui n'existe nulle part.**
   La lettre annonçait un témoin « rho 0,974–0,985 » : borne basse prise chez l'auditeur, borne
   haute chez l'auteur. « **Aucun document ne contient "0,974–0,985"** »
   (`contre-verification-lettres` ligne 15).

**Le coût, mesuré.** Trois passes de vérification indépendantes avant envoi (`aa97d1f`) : une
passe locale (`contre-verification-lettres`, 39 affirmations remontées à leur CSV ou à leur
rapport), une contre-vérification par un second modèle qui ne voyait pas la première, une
vérification externe des sources (`verification-externe-lettres` : arXiv 2411.10109, API OSF,
pages institutionnelles). Solde de la passe locale : **27 conformes, 5 écarts, 4 ambiguës,
1 réserve manquante, 2 invérifiables localement** — soit **12 affirmations non conformes sur
39**. Le commit de correction énumère **neuf corrections chiffrées** et **quatre corrections de
fond**, ces dernières plus graves (annonce de réduction de menace, 20,7 % attribué aux mauvais
items, affirmation sur un scénario non mesuré, défense « à faible coût » jamais testée sur les
données du destinataire).

**Vérification de l'affirmation « onze valeurs fausses ».** Je ne la retrouve pas sous cette
forme. Les comptes que le dépôt soutient sont : **9** corrections chiffrées listées par
`aa97d1f`, **12** affirmations non conformes sur 39 dans la passe locale, **20** corrections
dans `audit-chiffres-2026-09-12.md` (dont 4 touchent un chiffre, 16 sont des erreurs de renvoi,
de compte ou de statut périmé). « Onze » n'est corroboré par aucun de ces trois décomptes. Le
fait reste : **des valeurs fausses ont atteint des lettres destinées à des chercheurs
extérieurs, et il a fallu trois passes pour les sortir.** C'est le nombre exact qui ne tient
pas — ce qui est, ironiquement, exactement la défaillance décrite ici.

**Symptôme jumeau, à lui seul suffisant pour le diagnostic : le compteur de réfutations a pris
quatre valeurs dans la journée.** 16 au départ ; **14** après requalification de deux IC
bootstrap dégénérés (`audit-chiffres` §1.2) ; **15** après ajout de T2 réfutée ; **14** de
nouveau après que T2 est requalifiée non testable (`8df4e68` : « Le texte affichait quinze a
quatre endroits - corrige »). À aucun moment un fichier ne détenait ce compte : il se
recomptait à la main dans chaque document. Troisième symptôme, mineur mais parlant : le nombre
de fichiers de l'artefact a été écrit « nine » dans la lettre, recompté « 10 » par la
contre-vérification (`ls artefact/` hors dossiers), corrigé en « onze » à l'envoi (`git ls-files
artefact/` = 11, `.gitignore` inclus). Trois comptes, trois méthodes, aucune déclarée.

### 3.3 Rapports périmés laissés sans avertissement, qui ont induit les agents suivants en erreur

Le dépôt lui-même a tiré la leçon (`REPRISE-2026-09-12.md`, « Pièges pratiques appris cette
nuit » : « Un rapport laissé sans avertissement induit les suivants en erreur »). Voici les cas,
comptés.

| # | Rapport périmé | Ce qu'il a produit chez le suivant | Preuve |
|---|---|---|---|
| 1 | `c7-nul-corrige-resultats.md` (rétracté) | Son CSV a fourni à la lettre de divulgation l'IC du PMM et l'IC de 0,965 | `contre-verification-lettres` lignes 4, 16 |
| 2 | `conformite-popets-2026-09-12.md` | **Quatre à six verdicts « NON CONFORME » faux** (biblio, longueur, section AI use, scories, IRB) — corrigés en constatant qu'aucun n'était plus vrai | `audit-chiffres` §1.3 |
| 3 | `REPRISE-2026-09-12.md` | Annonçait « coût réel dépasse 0,55 USD, aucun total fiable » alors que 9,969 USD étaient consolidés ; et « 16 à 14, pas encore appliqué » | `audit-chiffres` §1.4, §1.2 |
| 4 | `c7-fort-resultats.md`, `c7-recette-resultats.md` | Publient encore « [0 ; 0] » ; le manuscrit les cite pour des valeurs Clopper-Pearson **qu'ils ne contiennent pas** — « Le manuscrit est juste, sa traçabilité ne l'est pas » | `audit-chiffres` §3.3 |
| 5 | `revue-hostile-gel` D3 (1,47 point) | Constat déjà périmé ; `cout-d4-propagation` a dû **mettre en garde contre sa réouverture** | `revue-hostile-gel`, note d'état |
| 6 | La note qui signalait « 31.15 % » gravé dans `fig2-couplage.png` | La figure affichait bien 31,6 % : « **Le rapport qui signalait 31,15 % etait en retard, pas l'image** » | `7f22fce` |
| 7 | La fourchette « 20,7 % à 65,7 % » | Toujours portée par trois fichiers de travail, alors qu'A6 **interdit** de comparer ces deux mesures et que le chiffre Park est passé à 90,40 % | `audit-chiffres` §1.1 |
| 8 | `c7-factoriel-resultats.md`, `c7-deux-organisations-resultats.md` | **Déjà poussés sur GitHub**, affirmaient sans avertissement des conclusions invalidées, jusqu'au commit de rétractation | `d8e0daf` |

**Huit cas documentés dans une seule journée.** Le pire n'est pas le nombre, c'est le motif :
dans les cas 2, 5 et 6, le document périmé était un **rapport d'audit** — c'est-à-dire
l'instrument censé attraper les erreurs — et il a fait perdre du temps à corriger des choses
justes. `audit-chiffres` en tire la règle explicite : « **ne corriger que ce qui est faux**
s'applique aussi à un rapport qui accuse à tort ».

**Cause structurelle.** Un rapport est un fichier plat sans état. Rien dans le dépôt ne relie
un rapport à sa validité courante, et la rétractation est une action volontaire que quelqu'un
doit penser à faire, dans un commit séparé, plusieurs heures après. Entre l'invalidation
(17:00) et la pose des avertissements (17:06), les documents faux étaient publics.

### 3.4 Une même quantité portant plusieurs intervalles, et des baselines comparées entre bassins différents

**Confirmé, deux fois, et ce sont deux défauts différents.**

*Plusieurs intervalles pour une quantité* : traité au §3.2 — quatre IC pour 20,7 %, réglé par
`7f22fce` qui tranche sur preuve ([19,0 ; 22,4] du CSV préenregistré, corroboré par une seconde
dérivation indépendante à [19,04 ; 22,41]) et déclare explicitement ce qui n'est **pas**
fusionné (le 20,7 % [20,7 ; 20,8] de l'étude d'échelle, qui est un rééchantillonnage sur
20 répétitions et non un bootstrap sur les personnes). C'est le bon geste, appliqué tard.

*Baselines entre bassins différents* : confirmé. `c7-reconciliation-facteurs` §5 liste les
trois valeurs (2,13 % à 2 058, 9,20 % à 200, 13,29 % à 120) et les **deux** erreurs
d'appariement — le moonshot comparant à la baseline d'un pool de 200 des paliers mesurés à
2 058, le factoriel comparant un top-1 jumeau↔jumeau à une baseline jumeau→humain. `28405b2`
confirme : « **deux conclusions ont ete faussees cette nuit en comparant un top-1 a la baseline
d'un autre bassin** ». Le correctif adopté est bon parce qu'il est structurel et non
disciplinaire : `controle_avant_interpretation()` **ne prend aucun paramètre de baseline**, elle
la recalcule sur les mêmes indices que le candidat — « il n'existe structurellement aucun moyen
de comparer un candidat à la baseline d'un bassin différent »
(`controle-interpretabilite` §3). C'est le modèle à imiter pour toutes les portes du §6 : rendre
la faute **impossible à exprimer**, pas interdite.

**Une nuance à charge, que le dépôt assume déjà** : la correction de baseline nous
*défavorise*. La baseline homogène à bassin 120 vaut 23,69 à 34,42 %, pas 13,29 % ; « le mauvais
choix flattait ces bras » (`8df4e68`).

---

## 4. Ce que le responsable m'a signalé et qui n'est pas exact

### 4.1 « Préenregistrements commis après leurs résultats, sauf un seul » — **inexact tel que formulé**

Vérification mécanique sur l'historique complet, `git log --diff-filter=A` pour chaque paire
`X-preenregistrement.md` / `X-resultats.*` :

- **Aucune inversion nulle part.** Dans **aucune** des 29 paires Tier 1 le fichier de résultats
  n'apparaît dans l'historique avant son préenregistrement. `preenregistrements-recueil` §2.5
  le dit et je le reproduis indépendamment.
- **33 paires** ont leur préenregistrement dans un commit **strictement antérieur** à celui de
  leurs résultats (écarts de 2 minutes à 4 heures).
- **12 paires** ont préenregistrement et résultats dans le **même commit** — antériorité non
  vérifiable par git, dont 3 du chantier C7 (`c7-dp`, `c7-utilite-aval`, `c7-attaquant-fort`,
  tous le 12/09 vers 07:10).
- **4 paires** (`c7-nul-corrige`, `c7-tautologie`, `c7-temoin-prompt`, `c7-deux-organisations`)
  ont un préenregistrement commis seul **alors que les fichiers de résultats existaient déjà
  sur le disque** — et les messages de commit le déclarent eux-mêmes, mot pour mot :
  « l'ordre des commits établit une antériorité faible, pas une preuve » (`5c4cef4`, `24cc79d`).
- **1 seule paire** a une antériorité **prouvée** et non simplement déclarée : `c7-factoriel`.
  `git show ff90409:analyses/c7_factoriel.py` échoue — le script producteur n'existait pas dans
  le dépôt au moment du préenregistrement.

**La formulation juste est donc l'inverse de celle qui m'a été donnée** : les préenregistrements
ont massivement été commis avant leurs résultats ; ce qui n'existe qu'une fois, c'est la
*preuve* de cette antériorité. Et c'est une critique qui reste sévère — sur 29 paires, 4 ne
s'appuient que sur notre propre parole, 3 sur rien, et l'argument anti-dragage que le dossier
compte opposer à un relecteur repose sur une discipline attestée, pas démontrée.

**Ce qui est vraiment grave ici, et qui n'est pas un problème d'horodatage** : le seul
préenregistrement dont l'antériorité soit prouvée est celui de l'expérience la plus inutile de
la journée (§2.0). La discipline de préenregistrement, exécutée parfaitement, n'a rien empêché.
C'est le fait le plus important de cette autopsie et il doit être retenu contre toute tentation
de répondre à cette journée par « plus de préenregistrement ».

### 4.2 « Des agents qui attendaient un calcul en arrière-plan et ne se réveillaient jamais : quantifie le coût en jetons » — **le phénomène est réel, le chiffrage est impossible**

Le phénomène est documenté en toutes lettres (`REPRISE-2026-09-12.md`) : « un agent qui lance un
calcul long et attend son réveil **ne se réveille jamais** dans ce mode de travail — tout doit
tenir en avant-plan, quitte à réduire les réplicats ».

**Le coût en jetons n'est mesurable nulle part dans le dépôt** : aucun fichier n'enregistre la
consommation de jetons d'un agent, et je n'inventerai pas ce chiffre. Ce que je peux chiffrer,
c'est le **coût en précision**, qui est réel et traçable :

| Calcul | Ce qui a été perdu | Preuve |
|---|---|---|
| Bootstrap commun de la multiplicité | **Abandonné**, ~170-200 s jugés trop longs — « aucun essai » | `c7-multiplicite-globale-2026-09-12.md` |
| `c7_nul_corrige.py` (audit de reproductibilité) | **Interrompu deux fois**, N2/N2b/N3 jamais atteints | `reproductibilite-chaine` §3, §5 |
| `c7_disjoint.py` | Rejoué à `--splits 10 --nul 20` au lieu de 50/100 : moyenne obtenue **« pas directement comparable »** à la valeur publiée | `reproductibilite-chaine` §3 |
| Vérification du témoin par son auteur | 10 réplicats au lieu de 100, **bits sur 1 réplicat** | `c7-nul-corrige-reponse-audit.md` |

La dernière ligne est la plus coûteuse, et elle referme la boucle : c'est cette réduction à 10
réplicats qui produit le 31,15 % face au 31,62 % de l'auditeur, écart que « rien dans le dépôt
ne réconcilie » (`audit-chiffres` §3.4), qui est arrivé tel quel dans une lettre de divulgation
(`contre-verification-lettres` ligne 17), et dont le seul chiffre de bits d'identité (4,63)
repose sur **un seul réplicat**. **La contrainte d'avant-plan n'a pas coûté des jetons : elle a
fabriqué des chiffres discordants dans un livrable externe.** C'est plus grave que ce qui m'a
été signalé, et la parade n'est pas de rétablir l'arrière-plan mais d'exiger que tout script
long expose un paramètre de réduction *et* que toute valeur publiée déclare son effectif de
réplicats (porte G1.2, §6).

---

## 5. La cause commune : l'hypothèse examinée, puis corrigée

**L'hypothèse soumise** : *la vérification arrivait systématiquement en aval de l'engagement —
on écrivait puis on vérifiait.*

**Verdict : exacte pour la rédaction, fausse pour l'expérimentation, et la partie fausse est
celle qui a coûté le plus cher.**

*Là où elle tient.* Le manuscrit a été révisé et commis à 13:25 avec « A7 détruite », invalidée
à 17:00. Les six modifications du §7 étaient en cours d'application pendant que l'audit qui les
démolissait s'écrivait. `revue-hostile-gel` D1 constate que l'introduction et le tableau 1
publiaient encore les chiffres du témoin que l'article déclare défectueux trois pages plus loin.
Sur le livrable, oui : l'écriture précédait la vérification, et parfois lui était concurrente.

*Là où elle ne tient pas.* Le dépôt contient **59 préenregistrements**, dont 35 pour le seul
chantier C7, aucun postérieur à ses résultats, écrits avec seuils chiffrés et règles de décision
avant calcul. La vérification était massivement **en amont**. Elle n'a rien empêché. Le contre-
exemple est dirimant : `c7-factoriel` a le meilleur préenregistrement du dépôt et c'est
l'expérience la plus inutile de la journée. Et `c7-nul-corrige` avait préenregistré un
garde-fou (§8) contre l'exact défaut qui l'a tué — un garde-fou opérationnalisé comme
`len(set(np.round(f, 12))) < 2`, c'est-à-dire un axe *exactement constant*, « ce qu'un bruit
continu ne produit jamais » : il annonce « 0/100 réplicats dégénérés », chiffre
« **exact et sans valeur** » (`audit-renversement` §1.4).

**La cause commune que je retiens, en trois propositions, chacune adossée à une preuve :**

**(1) On préenregistrait l'hypothèse, jamais la validité de l'instrument.** Chaque
préenregistrement décrit ce qu'on s'attend à mesurer et à quel seuil on conclura. Aucun ne
demande si l'appareil mesure quelque chose. D'où : un plan factoriel impeccable sur des jumeaux
vides ; un témoin dont le contrôle d'exactitude était **tautologique** — « `sortie_effectif_exact`
écrit `round(q_i · n_obs_i)` cellules égales à la cible, puis le contrôle mesure l'exactitude
contre **cette même cible** […] le contrôle ne peut pas échouer » (`audit-renversement` §3) ; un
garde-fou qui ne peut pas se déclencher. **Un contrôle qui ne peut pas échouer n'est pas un
contrôle, et rien dans le protocole n'obligeait à le montrer en train d'échouer.**

**(2) Aucune valeur n'avait de propriétaire.** Pas de registre, pas de source unique, pas d'état
de fraîcheur. D'où : quatre IC pour une grandeur, quatre valeurs pour le compteur de
réfutations, deux implémentations irréconciliées à 31,15/31,62 %, trois comptes pour onze
fichiers, un chiffre faisant autorité dont le producteur n'était pas versionné, et huit rapports
périmés lus comme courants.

**(3) L'écriture était concurrente et non verrouillée.** Cinq agents sur `manuscrit.md`,
l'auditeur réduit à crier dans un fichier, et un rapport public rétracté six heures après son
invalidation.

**Formulation d'une ligne** : *on vérifiait ce qu'on affirmait, jamais avec quoi on le mesurait
ni d'où venait le nombre.* La correction n'est donc pas « vérifier plus tôt » — nous vérifiions
déjà tôt — mais **déplacer l'objet de la vérification de l'affirmation vers l'instrument et vers
la provenance**, et la rendre mécanique pour qu'elle ne dépende d'aucune vigilance.

---

## 6. Protocole corrigé : portes obligatoires, chacune exécutable

Une porte n'est une porte que si un script sort avec un code non nul. Aucune des règles
ci-dessous n'est une intention ; chacune nomme sa commande. Trois sont déjà écrites dans le
dépôt et n'attendent que d'être câblées en obligation.

### Porte 0 — avant de dépenser un centime (`analyses/garde_depense.py`, exit ≠ 0 = arrêt)

| # | Ce qui doit être vrai | Contrôle mécanique | État |
|---|---|---|---|
| G0.1 | Le préenregistrement est commis **seul**, et le script producteur de résultats **n'existe pas dans le dépôt** à ce commit | `git show <sha_prereg>:<script>` doit échouer ; `git show --stat <sha_prereg>` ne contient qu'un `.md` | Fait une fois (`ff90409`) — à imposer |
| G0.2 | Le pipeline candidat porte une personne : pilote, puis `controle_avant_interpretation()` | `analyses/c7_controle_interpretabilite.py` ; `EchecControleInterpretabilite` ⇒ aucun appel | **Écrit et testé** (`28405b2`, 19 vérifications) |
| G0.3 | Une lecture `total_usage` est **commise avant** le premier appel | `GET /credits` → fichier horodaté dans le commit de préenregistrement | Manquant : aucune lecture entre le 11/09 14:24 et 22:53 (`cout-api` §5) |
| G0.4 | Le plafond de dépense est déclaré dans le préenregistrement et lu par le script | Comparaison `plafond_prereg == LIMITE` avant le premier appel | Pratiqué (`c7-factoriel` : 1,00 USD dur, arrêt interne 0,90) |
| G0.5 | Tout contrôle préenregistré est montré **en train d'échouer** sur un cas fabriqué | Test unitaire obligatoire « ce contrôle rejette X » ; un contrôle sans test d'échec ne passe pas | Manquant — c'est le défaut du §8 de `c7-nul-corrige` |

G0.5 est la porte la plus importante du dispositif et elle ne coûte rien : appliquée,
elle aurait tué le garde-fou `len(set(...)) < 2` et le contrôle d'exactitude tautologique
avant le calcul.

### Porte 1 — avant d'écrire une ligne dans le manuscrit (`analyses/verifie_chiffres.py`)

Repose sur un fichier à créer, `resultats/registre-chiffres.csv`, une ligne par grandeur
publiée : `grandeur | valeur | IC | n_replicats | script | commit | csv_source`.

| # | Ce qui doit être vrai | Contrôle mécanique |
|---|---|---|
| G1.1 | Tout nombre du manuscrit correspond à une ligne du registre | Extraction de tous les littéraux numériques du `.md`, jointure sur le registre, échec si orphelin |
| G1.2 | **Une grandeur, un intervalle, un effectif** | Le registre refuse deux lignes de même `grandeur` avec IC ou `n_replicats` différents ; deux mesures légitimement distinctes doivent porter deux noms distincts |
| G1.3 | Aucun nombre ne provient d'un fichier rétracté ou périmé | `grep -l "RÉTRACTÉ\|PÉRIMÉ"` sur les `csv_source`/`script` du registre ⇒ échec |
| G1.4 | Tout chiffre publié est rejouable depuis un **clone nu** | Pour chaque ligne : `git ls-files <script>` non vide, puis rejeu et comparaison à la précision publiée |
| G1.5 | Les formulations interdites sont absentes | La liste d'interdits de `article-synthese.md` (« 25× », « 26,11 », minorant, causalité fidélité→fuite…) passée en `grep -F -f interdits.txt` |
| G1.6 | Les renvois internes pointent juste | Chaque `§N.M`, `Table N`, `Figure N` résolu contre sa cible |

G1.4 aurait détecté le §2.1 le jour même. G1.2 aurait rendu impossible les quatre IC de 20,7 %,
les quatre valeurs du compteur et le couple 31,15/31,62 %. G1.6 a été fait à la main une fois
(`audit-chiffres` §4 : 60 renvois vérifiés un à un, 3 faux) — c'est exactement le genre de
travail qu'aucun humain ne doit refaire.

### Porte 2 — avant d'envoyer un courriel

| # | Ce qui doit être vrai | Contrôle mécanique |
|---|---|---|
| G2.1 | Le contenu chiffré de la lettre passe la Porte 1, registre compris | Même script, appliqué au `.md` de la lettre |
| G2.2 | Trois passes indépendantes : audit adverse par un agent **non producteur**, contre-vérification par un **modèle différent aveugle à la première**, contrôle des sources externes | Trois rapports datés, nommés dans le commit d'envoi (ce qui a été fait — `aa97d1f`) |
| G2.3 | Aucune affirmation sur un scénario non mesuré | Liste d'expressions proscrites (« reduces the risk », « has not increased », « small utility cost ») en `grep` ; toute occurrence exige une ligne de registre |
| G2.4 | L'adresse de signature est l'adresse d'envoi | Comparaison du champ signature au compte connecté (faute réelle, trouvée à 17:55, `8d43f1c`) |
| G2.5 | Toute citation d'un document tiers est vérifiée à la source primaire | Passe externe obligatoire (faite : arXiv 2411.10109, API OSF, pages institutionnelles) |

### Porte 3 — permanente, sur le dépôt

| # | Ce qui doit être vrai | Contrôle mécanique |
|---|---|---|
| G3.1 | Un rapport invalidé porte son en-tête de rétractation **dans le commit qui l'invalide**, pas six heures après | Hook `pre-commit` : si le message contient « invalide/rétract/requalifi », le commit doit modifier l'en-tête des rapports nommés |
| G3.2 | Un fichier livrable n'est écrit que par un agent à la fois | Verrou `article/manuscrit.md.lock` versionné ; écriture refusée si le verrou appartient à un autre |
| G3.3 | Aucun calcul en arrière-plan ; tout script > 60 s expose un paramètre de réduction et déclare sa durée pleine échelle | `reproductibilite/USAGE.md` doit contenir une durée pour chaque script du registre (aujourd'hui : aucune) |
| G3.4 | Aucune baseline n'est un paramètre d'appel | Revue de signature : toute fonction de comparaison dérive sa baseline des mêmes indices que le candidat (modèle déjà appliqué, `controle-interpretabilite` §3) |

---

## 7. Ce qui a bien fonctionné, et la condition exacte qui l'a rendu possible

Même exigence que pour les échecs : un succès qu'on ne sait pas reproduire délibérément est un
coup de chance.

**(1) La revue adverse par un agent qui n'a pas produit le résultat — le seul dispositif qui ait
attrapé une erreur fatale.** `audit-renversement-2026-09-12.md` a démoli un renversement qui
allait changer le titre de l'article. Quatre conditions l'ont rendu possible, toutes
reproductibles :

- *Un mandat hostile écrit noir sur blanc* : « Hypothèse de travail : le résultat est faux, et
  il est faux **parce qu'il nous arrange**. » Ce n'est pas une posture, c'est une instruction
  qui oriente la recherche de preuve.
- *L'obligation de recalculer, pas de relire* : l'auditeur a construit lui-même le témoin
  manquant, 12 configurations × 20 réplicats, « mêmes graines, mêmes fonctions importées que le
  script audité ». Une relecture n'aurait rien trouvé : le défaut était dans le choix du nul,
  pas dans le code.
- *L'isolement d'écriture* : lecture seule sur tout le dépôt sauf son propre fichier. L'auditeur
  ne pouvait pas « réparer » et donc pas dissimuler.
- *Le devoir de dire aussi ce qui tient* : son §0 bis liste cinq choses qui résistent avant
  d'énoncer le verdict. C'est ce qui rend le reste crédible — et, mécaniquement, c'est ce qui a
  fait qu'aucun bon résultat n'a été jeté avec le mauvais.

**(2) La concession de l'auteur, vérifiable donc indiscutable.** « Mon renversement tombe […]
**Le chiffre était dans mon CSV et dans le tableau que j'ai moi-même imprimé ; je ne l'ai pas
traité comme disqualifiant.** » La condition n'est pas la vertu de l'auteur : c'est que
l'auditeur a pointé **une colonne existante de son propre CSV**. Une objection formulée dans les
données de l'autre ne se négocie pas. À exiger de tout audit : *nommer le fichier et la colonne
de l'audité qui contiennent déjà la réfutation.*

**(3) La double vérification par deux modèles indépendants, le second aveugle au premier.**
Elle a trouvé ce qu'une seule passe ne trouve pas : un IC accolé à la mauvaise valeur, et une
borne (« 0,985 ») fabriquée en croisant deux sources et présente dans aucune. La condition est
la **cécité mutuelle** — le second modèle ne voyait pas la première passe — plus une troisième
passe sur les sources *externes* (arXiv, API OSF, pages institutionnelles), qui seule pouvait
trancher ce qu'aucune lecture du dépôt ne peut trancher. Trois passes, trois périmètres
disjoints : le dépôt, le dépôt revu en aveugle, le monde extérieur.

**(4) Le refus de fusionner des chiffres proches.** `contre-verification-lettres` §3 énumère
**huit couples à ne pas fusionner** (31,15/31,6 ; 0,21/0,22/0,23 ; 65,7/65,51 ; 20,7/33,1 ;
0,965/0,969 ; 0,974/0,982/0,978/0,985 ; 9,2/13,29 ; 3,55/3,56). Et `7f22fce` montre le geste
inverse fait proprement : unifier quand deux dérivations indépendantes convergent
([19,0 ; 22,4] confirmé par [19,04 ; 22,41]), **et déclarer ce qu'on ne fusionne pas** et
pourquoi. La condition : une règle qui oblige à traiter la proximité numérique comme un signal
d'alerte, jamais comme une preuve d'identité. C'est un registre embryonnaire — le §6 ne fait que
l'industrialiser.

**(5) La discipline « jamais un taux sans son nombre d'items communs ».** Validée par la revue
hostile comme « exemplaire » (`revue-hostile-gel`), avec le 26,11 % explicitement retiré. Ce qui
l'a rendue possible : la règle est écrite dans `article-synthese.md` sous forme d'**interdit
nommé**, donc grep-able. Les interdits nommés ont tenu ; les bonnes intentions non nommées ont
toutes cédé. C'est l'argument central en faveur du §6.

**(6) `c7-factoriel` comme modèle procédural, malgré son résultat nul.** L'antériorité y est
prouvée parce que le script producteur n'existait pas encore dans le dépôt. Le succès n'est pas
dans l'intention mais dans le **fait vérifiable a posteriori par un tiers** : c'est G0.1.

**Et une chose qui a marché sans qu'on l'ait voulue** : la double exécution complète de
`c7_nul_corrige.py` (deux fois 3 977 s, md5 identique) a prouvé la reproductibilité bit à bit
d'un résultat par ailleurs faux, et l'auditeur l'a vérifiée indépendamment. Leçon à froid : la
reproductibilité est une propriété du calcul, **pas une preuve de validité**. Elle mérite d'être
maintenue, jamais d'être invoquée comme argument.

---

## 8. Le coût total de la journée, chiffré

### 8.1 Dollars d'API

| Poste | Montant | Source |
|---|---|---|
| Compteur fournisseur, ancre 11/09 14:24 → lecture en direct du 12/09 (nuit + queue R6) | **9,969303887 USD** | `cout-api-2026-09-12.md` §1 |
| Somme des coûts déclarés, 6 expériences de la nuit | 9,9212898180 USD | §2 |
| Idem + queue R6 | 9,9284383006 USD | §4 |
| Écart compteur − déclaré | 0,0408655864 USD (**0,4 %**) | §4, attribué aux arrondis à 4 décimales |
| Recoupement indépendant `GET /key` | cohérent à 0,03 USD près | §4 |
| Plan factoriel, 12:52–16:46, **après** cette consolidation | **0,5385601250 USD** | `c7-factoriel-resultats.md` §2 |
| **Total de la journée** | **≈ 10,51 USD** | somme des deux lignes en gras |
| Solde restant sur la clé | ≈ 5,77 USD sur 165 | `cout-api` §6 |

*Réserve honnête* : le total de 10,51 USD suppose que le factoriel n'est pas déjà compris dans
la lecture en direct du compteur ; s'il l'était partiellement, le total réel est entre 9,97 et
10,51 USD. Et `cout-api` §5 déclare qu'**aucune lecture `total_usage` n'existe entre le 11/09
14:24 et 22:53** : rien ne prouve indépendamment que rien d'autre n'a été facturé dans cet
intervalle. C'est précisément la porte G0.3.

**Dépense rendue nulle par le défaut d'instrument** : 0,5541898180 + 0,5385601250 =
**1,0928 USD**, soit **10,4 % de la dépense de la journée**, pour deux expériences qu'un
contrôle à zéro dollar arrêtait 5 fois sur 5.

*Précision de méthode, qui est elle-même une leçon* : le coût de la journée a été annoncé au
responsable comme « 0,32 $ » puis « 0,55 $ » alors qu'il s'agissait d'**une seule ligne** ; le
vrai total est vingt fois plus élevé. `cout-api` §2 le consigne sans se ménager. Le coût
lui-même n'avait pas de source unique de vérité — même défaillance qu'au §3.2, appliquée à
l'argent.

### 8.2 Travail refait, en unités mesurables

| Poste | Quantité | Source |
|---|---|---|
| Calcul brûlé sur un rapport rétracté | 2 × 3 977 s = **2 h 12** | `c7-nul-corrige-resultats.md`, en-tête |
| Expériences payantes rendues non interprétables | 2 (360 + 165 appels) | `c7-factoriel`, `c7-deux-organisations` |
| Rapports publics rétractés | **3** (+ 1 préenregistrement) | `d8e0daf` |
| Modifications d'article gelées après application partielle | **6** (titre, résumé, tableau, figure 2, compteur) | `c7-nul-corrige-resultats.md` §7 |
| Corrections appliquées dans la seule passe « audit des chiffres » | **20** (16 de référence/statut, 4 de valeur) | `audit-chiffres` §2 |
| Corrections dans les lettres avant envoi | **9 chiffrées + 4 de fond**, sur 12 affirmations non conformes / 39 | `aa97d1f`, `contre-verification-lettres` §5 |
| Passes de vérification des lettres | **3** indépendantes | `aa97d1f` |
| Valeurs successives du compteur de réfutations | **4** (16 → 14 → 15 → 14) | `audit-chiffres` §1.2, `8df4e68` |
| Rapports périmés ayant induit un agent suivant en erreur | **8 cas** | §3.3 |
| Scripts sauvés d'un répertoire temporaire | **3** (dont celui du résultat central) | `sauvetage-scripts-temoin` |
| Rejeu de reproductibilité depuis un clone nu | 6 scripts, ≈ 1 800 s, 2 interruptions, 1 rejeu réduit non comparable | `reproductibilite-chaine` §2-3 |
| Commits de la fenêtre 16:46 → 18:50 | **13**, dont la quasi-totalité en réparation | `git log` |

**Non chiffrable depuis le dépôt** : le coût en jetons des agents, et le temps-agent total. Je
ne le fabrique pas (§4.2).

---

## 9. Les trois phrases à retenir

1. **La discipline de préenregistrement a été respectée, et elle n'a rien empêché** : on
   préenregistrait l'hypothèse, jamais la validité de l'instrument. Un plan factoriel
   irréprochable sur des jumeaux vides a coûté 0,54 USD, une contribution, et une lettre à
   Columbia.
2. **Aucun nombre n'avait de propriétaire** : quatre intervalles pour une grandeur, quatre
   valeurs pour un compteur, deux implémentations irréconciliées, et le chiffre qui porte le
   titre produit par un script jamais commis. Un registre à une ligne par grandeur rend tout
   cela impossible à exprimer.
3. **Ce qui a attrapé les erreurs n'était jamais de la vigilance, toujours un dispositif** :
   un mandat hostile écrit, une cécité mutuelle entre deux modèles, un interdit grep-able, un
   script absent du dépôt au moment d'un commit. Les bonnes résolutions non nommées ont toutes
   cédé le même jour.
