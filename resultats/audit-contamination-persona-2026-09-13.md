# C7, audit : la persona contient-elle déjà, en langage naturel, les réponses d'achat de la vague 4 ? (13 septembre 2026)

statut: courant
mandat: Tester l'hypothese de contamination semantique : la persona des vagues 1-3, qui est de la prose, contient-elle deja en langage naturel les reponses d'achat de la vague 4 ? (1) Etablir le contenu reel de la persona depuis le catalogue et les donnees. (2) Mesurer le recouvrement semantique item par item, cote achats et cote heuristiques. (3) Un comparateur classique servi explicitement des predicteurs apparentes monte-t-il vers les 33,2 % du jumeau ? (4) Departager avec l'explication alternative innocente : la stabilite test-retest humaine des 40 items d'achat contre celle des 20 items d'heuristiques. Aucun appel payant, aucun reseau, aucun arriere-plan, aucune donnee individuelle imprimee.
agent: Claude Opus 5, Anthropic
ecriture: analyses/c7_audit_contamination.py, resultats/audit-contamination-persona-2026-09-13.md, resultats/c7-audit-contamination.csv
lecture_seule: tout le reste du depot, notamment analyses/c7_reidentification.py, analyses/c7_controle_interpretabilite.py, analyses/c7_audit_comparateur_conditionne.py (branche agent/audit/comparateur-conditionne), analyses/c7_controle_generateur.py (branche agent/mesures/controle-generateur)
interdits: appel payant, reseau, recherche web, arriere-plan, fusion sur master, ecriture dans article/manuscrit.md et resultats/article-synthese.md, impression de tout pid, extrait de persona, reponse ou appariement individuel
cout_reel_usd: 0.00

---

## 0. Préenregistrement — écrit et commité AVANT tout calcul

### 0.1 Ce qui est attaqué

L'audit `agent/audit/comparateur-conditionne` établit que les 60 items attaqués de Twin sont
**tous** de source `wave4_Q_wave1_3_A`, **aucun** de source `wave1_3_persona_json` —
intersection d'identifiants **nulle** — et conclut qu'« à information d'entrée strictement
égale, le meilleur générateur classique atteint 0,45 % contre 20,66 % pour le jumeau LLM ».
Il déclare lui-même que la concentration à 100 % de l'écart sur les 40 items d'achat
(LLM 33,2 % contre 0,06 % pour le classique ; et sur les 20 items d'heuristiques, LLM 0,25 %
**sous** le classique 0,51 %) est « le point non expliqué du dossier ».

**L'objection.** La disjonction établie est une disjonction d'**identifiants de questions**,
pas de **contenu**. La persona est de la prose (~95 000 caractères par personne). Si elle
décrit les habitudes de consommation — marques, magasins, budget, catégories achetées —,
alors les réponses d'achat de la vague 4 y sont **présentes en langage naturel** et le jumeau
ne devine rien : il **lit**. Le comparateur « équitable » ne l'était alors pas : il recevait
634 colonnes structurées et ne pouvait pas exploiter un contenu sémantique qu'un modèle de
langage lit sans effort. L'écart mesurerait la capacité à lire de la prose, et la
concentration exclusive sur les items d'achat s'expliquerait d'un coup.

### 0.2 Les deux explications concurrentes, et ce qui les départage

- **E1 — contamination sémantique.** La persona contient, en prose, l'information d'achat de
  la vague 4 (marques, catégories, comportement d'achat). Prédit : un **recouvrement
  sémantique fort côté achats et nul côté heuristiques**, et un comparateur classique qui
  **monte** dès qu'on lui sert explicitement les prédicteurs apparentés.
- **E2 — prévisibilité différentielle.** Les comportements d'achat sont simplement **plus
  stables chez les humains eux-mêmes** que les réponses à des tâches d'heuristiques et biais,
  lesquelles sont largement du bruit de réponse. Prédit : une **stabilité test-retest humaine
  bien plus forte** sur les 40 items d'achat que sur les 20 items d'heuristiques, **sans**
  recouvrement sémantique et **sans** gain du comparateur servi.
- **Ce qui les départage.** (i) Le recouvrement sémantique item par item ; (ii) le
  comparateur classique servi des bons prédicteurs ; (iii) la **fraction du plafond humain
  récupérée** par le jumeau, bloc par bloc. E2 explique **entièrement** la concentration si
  et seulement si le jumeau récupère la **même fraction** du plafond de retest humain sur les
  deux blocs ; si la fraction récupérée est très inégale, E2 explique une partie du
  phénomène et pas sa totalité.

E2 est l'explication **innocente** et elle est peut-être la bonne. Elle est testée avec le
même soin que E1, et le rapport le dit si elle l'emporte.

### 0.3 Mesures fixées avant calcul

Bassin **strictement constant** dans toute la section quantitative : 2 058 attaqués,
2 058 candidats, les 60 items de `c7_reidentification.items_communs`, attaque
`c7_reidentification.rangs_attaque` importée sans réimplémentation, graine 20260913,
IC à 95 % par `a2_commun.bootstrap_personnes` (2 000 tirages de personnes).

1. **Contenu de la persona** : blocs, QuestionID, colonnes du catalogue ; classement de
   chaque QuestionID persona en familles ; relevé explicite de tout item touchant à la
   consommation, aux achats, aux marques, au revenu ou au mode de vie.
2. **Recouvrement sémantique item par item** : pour chacun des 40 items d'achat, recherche
   dans la **prose de persona réellement donnée au modèle**
   (`wave_persona_chunk_001.parquet`) et dans les libellés des 171 QuestionID persona, de
   (a) la **marque** du produit, (b) le **nom de catégorie** du produit, (c) les têtes
   nominales du descriptif produit. Symétriquement pour les 20 items d'heuristiques
   (« anchoring », « redwood », « Linda », « sunk cost », « jacket », « calculator », etc.).
   Deuxième mesure, dite de **recouvrement de construit** : l'ensemble, déclaré et
   auditable, des colonnes de persona portant sur la disposition à dépenser
   (échelle tightwad–spendthrift), le revenu, la taille du foyer, l'emploi et l'intention
   alimentaire.
3. **Le test quantitatif** : comparateurs classiques servis explicitement des bons
   prédicteurs, hors pli (5 plis), mesurés sur le bloc d'achat et sur le bloc heuristiques,
   bassin de personnes inchangé.
   - **S1 « servi sur un plateau »** : modèle conditionnel par item sur le seul ensemble
     de construit consommation déclaré en 2.
   - **S2 « sélection par item »** : modèle conditionnel par item sur les **25** colonnes de
     persona de plus forte information mutuelle avec **cet item**, sélection calculée
     **dans les plis d'entraînement seuls** (réduction déclarée : 25 colonnes, 5 plis).
   - **S2s** : la version tirage de S2 (générateur véritable, pas prédicteur).
   - **S3 « niveau seul »** : attaque conduite sur le **seul nombre de « oui »** d'achat,
     pour tester la version faible de E1 (« la persona donne le niveau de dépense »).
   - **T+ témoin positif** : le même appareil, servi des réponses des vagues 1-3 **aux items
     attaqués eux-mêmes**. Si T+ ne monte pas, mon résultat négatif ne vaut rien.
4. **Stabilité test-retest humaine** : par item, accord brut et accord corrigé du hasard
   (kappa de Cohen) entre la réponse des vagues 1-3 et la réponse de la vague 4 du **même
   humain** ; moyennes par bloc ; nombre de modalités et entropie par item ; et **fraction
   du plafond de retest récupérée** par le jumeau, par bloc.

`analyses/c7_controle_interpretabilite.controle_avant_interpretation` est appelé sur chaque
comparateur avant toute interprétation, baseline recalculée par la fonction sur le bassin
réellement attaqué.

### 0.4 Prédictions, fixées avant calcul

- **P1 (contenu).** La persona ne contient **aucun** item de marque, de catégorie de produit
  ni d'historique d'achat. Son contenu lié à la consommation se limite à une disposition
  **générale** à dépenser (tightwad–spendthrift), au revenu, à la taille du foyer, à
  l'emploi et à une intention alimentaire : **moins de 15 colonnes sur 634**, aucune
  spécifique à un produit. *Prédiction : vraie.*
- **P2 (recouvrement, côté achats).** **0 des 40** items d'achat aura un item de persona
  portant sur le **même objet**. Aucune des 40 marques n'apparaîtra dans la prose de persona.
  *Prédiction : vraie.*
- **P3 (recouvrement, côté heuristiques — et c'est la prédiction qui peut retourner le
  dossier).** Les 20 items d'heuristiques n'auront eux non plus aucun item de persona du même
  objet, mais un recouvrement de **construit plus fort** que les items d'achat (loteries,
  montants en dollars, cadrage gain/perte : tout le bloc « Economic preferences »).
  L'asymétrie de recouvrement ira donc dans le sens **inverse** de ce dont E1 a besoin.
  *Prédiction : vraie.* **Si elle s'inverse, E1 est confirmée.**
- **P4 (le juge).** Le meilleur comparateur classique servi des prédicteurs apparentés
  restera **sous 1 % de top-1 sur le bloc d'achat**, borne haute de l'IC **sous 2 %**, très
  loin des 33,2 % du jumeau. *Prédiction : vraie.*
- **P5 (témoin positif).** Le même appareil servi des réponses v1-3 aux items attaqués
  dépassera **50 % de top-1 sur le bloc d'achat**. *Prédiction : vraie.*
- **P6 (E2, mesure directe).** Le kappa de retest humain moyen sera **au moins 2 fois plus
  élevé** sur les 40 items d'achat que sur les 20 items d'heuristiques. *Prédiction : vraie.*
- **P7 (arbitrage, et c'est celle que je peux perdre).** E2 expliquera une **partie** de la
  concentration mais **pas sa totalité** : la fraction du plafond de retest récupérée par le
  jumeau sera **au moins 5 fois plus grande** sur le bloc d'achat que sur le bloc
  heuristiques. *Prédiction : vraie.* Si ces deux fractions sont **comparables** (rapport
  < 2), **E2 explique tout** et c'est E2 qui l'emporte seule.

### 0.5 Critères de réfutation

- **E1 est confirmée** si (i) **≥ 5 des 40** items d'achat ont un item de persona du même
  objet (marque ou catégorie de produit nommée dans la persona), **ou** (ii) la **borne
  basse** de l'IC à 95 % du meilleur comparateur classique servi des prédicteurs apparentés
  atteint **5 %** de top-1 sur le bloc d'achat. Dans ce cas le résultat du jumeau est annulé
  et l'article doit le retirer.
- **E1 est réfutée** si (i) et (ii) sont tous deux nuls — et le résultat du jumeau s'en
  trouve **renforcé**.
- **E2 l'emporte seule** si E1 est réfutée **et** que la fraction du plafond récupérée est
  comparable entre les deux blocs (rapport < 2) : la concentration n'a alors rien à voir avec
  la contamination, et l'article doit écrire qu'elle reflète la stabilité inégale des items
  chez les humains eux-mêmes.
- **Aucune des deux ne suffit** si E1 est réfutée et que les fractions sont très inégales :
  le mécanisme reste ouvert et l'article doit le déclarer ouvert, sans le combler.
- **Mon propre audit est invalide** si **P5 échoue** : un appareil incapable de retrouver le
  signal quand il est présent ne peut pas prouver son absence. Dans ce cas, aucune conclusion
  négative n'est publiable depuis ce fichier.

### 0.6 Garde-fous

- Bassin strictement constant (2 058 / 2 058 / 60 items) pour toutes les conditions
  comparées, y compris les chiffres repris des branches voisines. Trois erreurs de ce projet
  portent déjà sur ce point.
- Graine fixée (20260913). Sélection de variables **hors pli**. Aucun modèle n'est ajusté sur
  la personne qu'il prédit.
- `controle_avant_interpretation` appelé sur chaque comparateur avant interprétation.
- **Aucune donnée individuelle imprimée.** Ce mandat manipule de la prose personnelle : le
  script ne calcule, n'imprime et n'écrit **jamais** un `pid`, un extrait de persona, une
  réponse ni un appariement. Les mesures lexicales ne sortent que sous forme de **comptes
  agrégés sur des termes venant du catalogue public des questions**, jamais de termes extraits
  de la prose des répondants.
- Aucun appel de modèle de langage, aucun réseau, aucune dépense, aucun arrière-plan.
- **Réductions déclarées** : la prose de persona n'est disponible localement que pour le
  `chunk_001` (294 personnes sur 2 058) — le balayage lexical porte donc sur 294 personas,
  et la mesure rapportée est le **nombre de personas sur 294** où le terme apparaît ; les
  libellés de questions, eux, sont balayés sur les **171 QuestionID persona complets**.
  S2 retient 25 colonnes par item et 5 plis.

---

## 1. Ce que contient réellement la persona

**Établi depuis le catalogue publié et les données, pas supposé.** Les 171 QuestionID de
source `wave1_3_persona_json` — **634 colonnes CSV**, intersection **nulle** avec les
126 colonnes de `wave4_Q_wave1_3_A` — se répartissent ainsi :

| bloc | QuestionID | colonnes | ce que c'est réellement |
|---|---:|---:|---|
| Personality | 49 | **338** | inventaires de traits, 24 valeurs de Schwartz, inventaires de symptômes dépressifs, trois rédactions libres de soi (soi idéal / soi dû / soi réel) |
| Economic preferences | 36 | **194** | jeux de laboratoire : dictateur, ultimatum, confiance ; listes de choix multiples d'actualisation temporelle ; équivalents certains de loteries en gain et en perte ; comptabilité mentale |
| Cognitive tests | 69 | 68 | CRT, matrices de Raven, rotations de cubes, synonymes / antonymes, syllogismes, littératie financière, numératie |
| Forward Flow | 1 | 20 | association libre de mots, avec consigne explicite de **ne pas employer de nom propre ni de marque** |
| Demographics | 14 | 14 | région, sexe, âge, études, origine, citoyenneté, religion, pratique, politique, **revenu**, **taille du foyer**, emploi |

**La réponse à la question du mandat est donc : non.** La persona ne contient **aucun**
historique d'achat, **aucune** marque, **aucune** catégorie de produit, **aucun** magasin,
**aucun** poste de budget. Ce qui, dans la persona, touche de près ou de loin à la
consommation se compte : **10 colonnes sur 634**, et ce sont des **dispositions générales**,
jamais un comportement d'achat observé —

| famille | QuestionID | colonnes | contenu |
|---|---|---:|---|
| disposition à dépenser | QID31-QID34 | 4 | échelle *tightwad–spendthrift* (« difficulté à dépenser » ↔ « difficulté à limiter ses dépenses »), et un scénario de deux acheteurs face à une promotion |
| foyer et revenu | QID21, QID23, QID24, QID13, QID14 | 5 | revenu familial en 5 tranches, taille du foyer, statut d'emploi, âge, études |
| intention alimentaire | QID148 | 1 | « je mange moins pour perdre du poids » |

En élargissant au maximum défendable — en versant **tout** le bloc des préférences
économiques, qui est la mesure de laboratoire du compromis prix / valeur —, l'entrée
« apparentée à l'achat » monte à **204 colonnes**. C'est cette entrée large qui est servie au
comparateur S1 en section 3, pour que la réfutation ne puisse pas être imputée à une entrée
avare.

**P1 est tenue.**

## 2. Le recouvrement sémantique, item par item

Les 40 items d'achat sont, mot pour mot, de la forme : *« catégorie de produit X ; vous voyez
en magasin le produit Y ; il est au prix Z ; l'achèteriez-vous ? »*, avec réponse binaire.
Les prix sont manifestement randomisés (jusqu'à 53,98 $ pour 450 g de jambon, 0,00 $ pour du
papier toilette) : répondre engage donc le rapport de la personne au **prix** autant qu'au
produit.

### 2.1 Un artefact de mesure, déclaré plutôt que caché

La première version de ce script cherchait, pour chaque item d'achat, **n'importe quel jeton**
du groupe de mots capitalisés de tête. Elle « trouvait » **32 marques sur 40** dans la
persona — et le verdict automatique basculait sur « contamination confirmée ». Diagnostic :
les 32 correspondances sont **toutes** des mots courants — *extra, ones, brand, complete,
great, whole, size, original, little, stable* — présents dans le **libellé même** des
questions de persona. Une deuxième version cherchait la phrase entière par sous-chaîne nue et
comptait « ARM » (de *ARM & HAMMER*) chez 294 personas sur 294, parce que « arm » est dans
« warm » et « harm ». La règle retenue est la recherche de la **phrase entière aux frontières
de mot**, et les deux nombres sont publiés côte à côte pour que l'artefact reste vérifiable.

### 2.2 Ce que la persona nomme, et ce qu'elle ne nomme pas

| mesure, appliquée à l'identique aux deux blocs | 40 items d'achat | 20 items d'heuristiques |
|---|---:|---:|
| couverture des jetons de contenu par les **libellés** de persona | 0,204 | 0,124 |
| couverture des jetons de contenu par la **prose** de persona | 0,679 | 0,681 |
| **jetons distinctifs** de l'item (présents dans aucun des 59 autres items) | 171 | 52 |
| ... dont présents dans les **libellés** de persona | 10 (5,8 %) | **20 (38 %)** |
| ... dont présents dans la **prose** de persona | 77 (45 %) | **36 (69 %)** |
| **marques** nommées comme phrase entière | **0 / 40** | — |
| **produits** nommés comme phrase entière | **0 / 40** | — |
| catégories nommées comme phrase entière | 3 / 40 | — |
| *(règle naïve par jeton isolé — artefact, pour mémoire)* | *32 / 40* | — |

Vérification directe, marque par marque, sur la prose réellement donnée au modèle :
*Tylenol, Purina, Coca-Cola, Doritos, Folgers, Hershey, Duracell, Chobani, Bounty, Haribo,
Oscar Mayer, ARM & HAMMER, baking soda* — **0 persona sur 294** pour chacune.
« supermarket » : **0 / 294**. « grocery store » : **1 / 294**. Le seul « appariement de
marque » restant est le trigramme *ARM*, qui correspond au mot anglais *arm* — présent
exactement deux fois dans le texte de chaque persona, c'est-à-dire dans le gabarit, non dans
une mention de marque. Les trois catégories « trouvées » sont les mots anglais *Beer*
(2 personas sur 294), *Soup* (5) et *Ice Cream* (7), qui apparaissent dans des rédactions
libres ou des associations de mots — pas dans un relevé d'achats.

**P2 est tenue : aucun des 40 items d'achat n'a, dans la persona, d'item portant sur le même
objet.**

**P3 est tenue, et c'est elle qui retourne l'objection.** L'asymétrie de recouvrement existe,
mais elle va **dans le sens inverse** de ce dont la contamination a besoin : la persona
partage **38 %** des jetons distinctifs du bloc d'heuristiques contre **5,8 %** de ceux du
bloc d'achat (libellés), et **69 %** contre **45 %** (prose). Les préférences économiques de
la persona parlent de loteries, de probabilités, de gains et de pertes, d'assurance, de
risque — exactement le vocabulaire des items d'heuristiques et biais. **Si la lecture
sémantique de la prose expliquait quoi que ce soit, elle devrait produire l'effet sur le bloc
d'heuristiques, où le jumeau est justement au plus bas.**

## 3. Le test quantitatif : le comparateur servi des bons prédicteurs

Bassin **strictement constant** : 2 058 attaqués, 2 058 candidats, attaque
`rangs_attaque` importée sans réimplémentation, graine 20260913, hasard top-1 = 0,049 %.

| condition | entrée | **top-1, bloc achat [IC 95 %]** | top-1, bloc heuristiques |
|---|---|---|---|
| Retest humain v1-3 aux items attaqués | *hors persona* | 74,67 % [72,87 ; 76,47] | 15,57 % [14,14 ; 17,01] |
| **T+ témoin positif** (même appareil, v1-3 aux items attaqués) | *hors persona* | **72,63 %** [70,66 ; 74,55] | 4,84 % [4,05 ; 5,68] |
| **LLM JSON Persona GPT4.1** | persona | **33,16 %** [31,29 ; 35,06] | **0,24 %** [0,07 ; 0,45] |
| LLM Demographics Only | segment seul | 5,95 % [5,06 ; 6,94] | 0,01 % |
| **S1 servi sur un plateau** (204 col. consommation) | persona | **0,08 %** [0,00 ; 0,20] | 0,00 % |
| **S2s** sélection 25 col./item hors pli, tirage | persona | 0,08 % [0,00 ; 0,21] | 0,02 % |
| **S2** sélection 25 col./item hors pli, argmax | persona | **0,00 %** [0,00 ; 0,00] | 0,04 % |
| **S3** jumeau, motif détruit / niveau conservé | persona | 0,13 % [0,02 ; 0,27] | 0,24 % |

**P4 est tenue, et bien plus durement que prédite.** Servi explicitement de tout ce que la
persona porte sur la dépense, le revenu, le foyer et le compromis prix / valeur, le meilleur
comparateur classique atteint **0,08 %** sur le bloc d'achat, borne haute de l'IC **0,21 %** —
contre un critère de confirmation préenregistré à 5 % et contre **33,16 %** pour le jumeau.
Lui donner les bons prédicteurs sur un plateau ne le fait **pas** monter : il fait même
**moins bien** que le modèle dilué sur les 550 colonnes de l'audit précédent (0,06 %, même
ordre). L'information d'achat n'est pas dans la persona sous une forme qu'une méthode
classique puisse manquer : elle n'y est pas.

**P5 est tenue, et sans elle rien de ce qui précède ne vaudrait.** Le **même** appareil —
mêmes plis, même sélection hors pli, même régression, même attaque — servi des réponses des
vagues 1-3 **aux items attaqués eux-mêmes** atteint **72,63 %**. Il est d'ailleurs le **seul**
des cinq comparateurs à **passer** `controle_avant_interpretation` ; S1, S2, S2s et S3
échouent tous, c'est-à-dire n'atteignent pas la baseline Demographics Only. L'appareil
retrouve donc le signal **quand il est là**, et à un niveau très élevé. Son silence sur la
persona est une mesure, pas une faiblesse.

**La version faible de la contamination tombe aussi.** S3 conserve, chez chaque personne,
le **nombre de « oui »** produit par le jumeau et en **détruit le motif** par permutation
intra-personne. Le taux passe de **33,16 % à 0,13 %**. Ce que la persona pourrait
raisonnablement livrer — un **niveau** de propension à dépenser, que l'échelle
tightwad–spendthrift mesure explicitement — ne porte **rien** : tout le pouvoir
ré-identifiant vit dans le motif produit par produit, que la persona ne contient sous aucune
forme.

**E1 est réfutée sur ses deux critères préenregistrés**, et le résultat du jumeau s'en trouve
renforcé, non affaibli.

## 4. L'explication innocente : les items d'achat sont-ils simplement plus prévisibles ?

Mesure directe de la stabilité **chez les humains eux-mêmes**, entre leur réponse des vagues
1-3 et leur réponse de la vague 4 au **même item** :

| | 40 items d'achat | 20 items d'heuristiques |
|---|---:|---:|
| modalités par item | 2,0 | 5,6 |
| entropie par item | 0,99 bit | **2,06 bits** |
| accord brut test-retest | 0,839 | 0,556 |
| accord attendu par hasard | 0,508 | 0,277 |
| **kappa de Cohen moyen** | **0,672** | **0,389** |
| kappa min / médian / max | 0,621 / 0,670 / 0,704 | 0,252 / 0,365 / 0,528 |
| items sous kappa 0,20 | 0 | **0** |

**P6 est RÉFUTÉE.** J'avais préenregistré un rapport de kappa d'au moins 2 ; il vaut **1,73**.
L'effet existe — les achats sont plus stables — mais il est **nettement plus faible que je ne
l'avais prédit**, et surtout : **la prémisse de E2 est fausse telle qu'énoncée**. Les items
d'heuristiques ne sont **pas** « largement du bruit de réponse » : **aucun** des 20 n'est sous
kappa 0,25, leur kappa médian est 0,365, et ils portent **deux fois plus d'information par
item** que les items d'achat (2,06 bits contre 0,99). Chez l'humain, ces items sont
parfaitement ré-identifiants : le retest atteint **15,57 %** sur 20 items seulement, soit
320 fois le hasard.

**P7 est tenue, et c'est elle qui tranche.** Rapportée au plafond que l'humain lui-même fixe,
la performance du jumeau est **inégale d'un facteur 29** :

| bloc | plafond (retest humain) | jumeau | **fraction du plafond récupérée** |
|---|---:|---:|---:|
| items d'achat | 74,67 % | 33,16 % | **44,4 %** |
| items d'heuristiques | 15,57 % | 0,24 % | **1,5 %** |

La même lecture **par item**, qui ne dépend pas de la non-linéarité du top-1 vis-à-vis du
nombre d'items, dit la même chose. Gain d'exactitude au-dessus du taux modal, normalisé par
la marge disponible :

| | achat | heuristiques |
|---|---:|---:|
| retest humain | +0,635 | +0,287 |
| **jumeau LLM** | **+0,357** (56 % du plafond) | **−0,077** (*sous* le taux modal) |
| Demographics Only | +0,065 | −0,125 |
| S2 servi | −0,113 | −0,085 |

Sur les items d'heuristiques, le jumeau ne se contente pas d'échouer : il fait **moins bien
que prédire partout la réponse modale**, alors que l'information est là et que le retest
humain en récupère 29 % de la marge.

**E2 explique donc une partie du phénomène et pas sa totalité.** Les achats sont réellement
plus stables (kappa 0,672 contre 0,389) et cela contribue. Mais un facteur de stabilité de
1,73 ne produit pas un facteur 29 sur la fraction de plafond récupérée, et il n'explique
surtout pas que le jumeau tombe **sous la ligne de base** sur un bloc où les humains sont
mesurablement fidèles à eux-mêmes.

## 5. Verdict, et ce que l'article doit écrire

**E1 (contamination sémantique) est réfutée**, sur les deux critères préenregistrés et par
une marge large : 0 marque, 0 produit, 0 même-objet sur 40 ; et un comparateur classique
servi des prédicteurs apparentés qui plafonne à 0,08 % [0,00 ; 0,20] là où le jumeau fait
33,16 %, pendant que le témoin positif du même appareil atteint 72,63 %. **L'hypothèse la
plus spectaculaire est fausse, et le résultat du jumeau en sort renforcé.**

**E2 (prévisibilité différentielle) est réelle mais insuffisante**, et ma propre prédiction
P6 sur son ampleur est **réfutée** : l'écart de stabilité est de 1,73, pas ≥ 2, et les items
d'heuristiques ne sont pas du bruit.

**Aucune des deux explications ne suffit.** Le mécanisme de la concentration reste **ouvert**,
et l'article doit le déclarer ouvert plutôt que le combler. Ce que cet audit ajoute au
dossier, c'est que trois explications commodes sont maintenant **exclues** : la contamination
sémantique, la fuite du seul niveau de dépense, et le bruit de réponse des items
d'heuristiques.

**Limites.** (i) La prose de persona n'est publiée localement que pour le `chunk_001` : le
balayage lexical porte sur **294 personas sur 2 058** (réduction déclarée au
préenregistrement). Le balayage des **libellés**, lui, est complet. (ii) Mes comparateurs
restent des estimateurs **faibles** du contenu identifiant de la persona ; leur silence borne
par le bas, il ne prouve pas qu'aucune méthode classique n'y arriverait — mais le témoin
positif à 72,63 % montre qu'ils ne sont pas silencieux par construction. (iii) Le
recouvrement sémantique est mesuré lexicalement ; deux items peuvent porter sur le même
construit sans partager un mot. C'est précisément pourquoi le test quantitatif de la
section 3 est le juge, et pourquoi S1 reçoit les 204 colonnes de construit et non les seuls
mots.

### La phrase exacte que l'article doit écrire sur la concentration de l'effet

> L'écart est entièrement porté par les 40 items d'achat : le jumeau y ré-identifie 33,2 %
> [31,3 ; 35,1] des personnes, contre 0,08 % [0,00 ; 0,20] pour le meilleur comparateur
> classique explicitement nourri des colonnes de persona apparentées à la consommation et au
> prix ; sur les 20 items d'heuristiques et biais, le jumeau (0,24 %) ne dépasse pas ce
> comparateur. Cette concentration n'est pas un effet de contenu : la persona ne nomme
> aucune des 40 marques ni aucun des 40 produits, et son vocabulaire recouvre moins le bloc
> d'achat (5,8 % de ses jetons distinctifs) que le bloc d'heuristiques (38 %). Elle ne
> s'explique pas non plus par la seule instabilité des items d'heuristiques, qui restent
> fidèles chez les humains (kappa test-retest médian 0,365, aucun item sous 0,25, contre
> 0,672 sur les items d'achat) : rapporté au plafond que fixe le retest humain, le jumeau
> récupère 44 % de l'information d'identité disponible sur les items d'achat et 1,5 % sur les
> items d'heuristiques. Le mécanisme de cette concentration reste inexpliqué.
