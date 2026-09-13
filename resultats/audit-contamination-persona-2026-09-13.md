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

*(Sections 1 et suivantes écrites après calcul.)*
