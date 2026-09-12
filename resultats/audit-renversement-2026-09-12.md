# Audit adverse du renversement C7 (nul de marge corrigé) — 12 septembre 2026

Auditeur adverse. Je n'ai pas produit ce résultat et je n'ai aucun intérêt à ce qu'il tienne.
Hypothèse de travail : le résultat est faux, et il est faux parce qu'il nous arrange.
Lecture seule sur tout le dépôt sauf ce fichier. Aucun appel de modèle, aucun réseau.
Tout recalculé en avant-plan ; scripts d'audit dans le scratchpad de session
(`audit2.py`, `audit_contre_nul.py`, `audit3.py`).

---

## VERDICT EN UNE LIGNE

**Le renversement ne tient pas** : les cinq témoins « corrigés » détruisent l'exactitude
contre la vérité (0,527 → 0,407–0,436), donc précisément la grandeur dont l'objection
affirmait qu'elle explique tout ; un témoin qui la conserve — et qui est purgé du seul
défaut réel du témoin d'origine — reproduit le couplage (**rho 0,974 [0,950 ; 0,993]
contre 0,965 observé**) et la réfutation publiée tient.

---

## 0. Avertissement de concurrence d'écriture

Pendant cet audit (11 h 25 – 11 h 36), `article/manuscrit.md` (11 h 34), 
`resultats/article-synthese.md` (11 h 35) et `analyses/figures_article.py` (11 h 34) ont été
modifiés par d'autres agents. Je n'en ai tiré **aucune** conclusion et ne les ai pas lus au
fond. **Si le §7 de `c7-nul-corrige-resultats.md` est en train d'être appliqué au manuscrit,
il faut l'arrêter maintenant** : le présent audit conclut que ces six modifications sont à
suspendre. `c7-nul-corrige.csv` (11 h 20) et `c7-nul-corrige-resultats.md` (11 h 23) étaient
stables et cohérents entre eux au moment de ma lecture.

## 0 bis. Ce que j'ai vérifié et qui tient

Avant les défauts, ce qui résiste — un audit doit le dire aussi.

* **Reproductibilité : confirmée indépendamment.** `md5(resultats/c7-nul-corrige.csv)` =
  `e994f8f31e8c6faf389ceb3a8baa09fe`, identique au md5 annoncé **et** identique à la copie
  de vérification `c7-nul-corrige-verif.csv` du scratchpad. La double exécution annoncée a
  bien eu lieu et donne le même octet.
* **Le défaut de `c7_disjoint.py` est réel, et il est bien à la ligne 133** (pas 134, voir
  §1.2 ci-dessous). L'auteur l'a vu, et il avait raison de le signaler.
* **Le code des cinq constructions fait ce qu'il dit** sur le point le plus sensible :
  aucune ne lit `y_ref[i]` pour écrire la ligne de i (vérifié ligne à ligne, §2).
* **Le rho du prédicteur réel est solide** : il ne repose sur aucun point particulier (§3).
* **Les chiffres du tableau §4 du rapport** (top-1 par configuration) sont, eux, un apport
  réel et non contesté par cet audit.

---

## DÉFAUT FATAL 1 — le témoin corrigé ne teste plus l'objection qu'il prétend trancher

**Gravité : fatale. C'est à lui seul le verdict.**

### 1.1 L'objection d'origine, et ce qu'un nul doit conserver pour la tester

L'objection de `c7_disjoint` (§ « nul de marge ») est : *fidélité et fuite sont deux
fonctions monotones de la même exactitude par personne ; leur corrélation sur 12 points ne
mesure qu'un axe de qualité globale.* Le nul qui teste cela doit **conserver l'exactitude
contre la vérité** — par personne et donc par configuration — et détruire tout le reste.

Les cinq témoins corrigés font l'inverse. Ils apparient q_i contre une **cible de
substitution** (mode de segment, vecteur d'autrui, identité permutée), et l'exactitude
réellement obtenue **contre la vérité** s'effondre :

| construction | exactitude contre la VÉRITÉ (moy. 12 configs) | étendue inter-config |
|---|---|---|
| prédicteur réel | **0,5274** | 0,432 – 0,590 |
| N0 nul cassé | 0,5274 | 0,433 – 0,590 |
| N1 / N1b mode de segment | **0,4238** | 0,408 – 0,434 |
| N2 / N2b vecteur d'autrui | **0,4066** | 0,401 – 0,411 |
| N3 identités permutées | **0,4364** | 0,414 – 0,476 |

La grandeur sous test disparaît, et avec elle sa variation entre configurations : l'étendue
inter-configuration passe de 0,158 (réel) à 0,010 (N2). Un nul qui supprime la variable
explicative candidate ne peut pas réfuter l'explication par cette variable.

### 1.2 Le défaut d'origine était réel, mais ce n'était pas celui qui est décrit

Le rapport accuse la ligne 134 (`np.where(tirage_correct, y_ref, faux)`, « copie de la
cible »). C'est l'argument de `c7_tautologie`, et **`c7_tautologie` a raison** : écrire
`y_ref[i]` sur k_i positions **tirées au hasard indépendamment de la personne** n'est pas
une empreinte individuelle, c'est la définition arithmétique de « cette personne a k_i
items exacts ». Aucune construction ne peut fixer une exactitude par personne sans cela ;
le jumeau réel fait exactement la même chose sur les items qu'il devine juste.

Le vrai défaut est la **ligne 133** : `faux = faux + (faux >= y_ref)` fait éviter aux
cellules *fausses* la vraie réponse de la personne. Là, oui, il y a une information
individuelle de trop, et elle gonfle la fuite. Le rapport la mentionne comme « fuite
secondaire » alors que c'est **la seule qui en soit une**.

### 1.3 Le témoin manquant, construit et mesuré ici

J'ai construit le nul que ce dossier n'avait pas : **effectif exact de cellules justes
contre la vérité** (donc q_i atteint exactement, par personne et par configuration),
**positions tirées uniformément**, **cellules fausses tirées dans la marginale de population
de l'item** (rejet si elles tombent sur la vraie valeur — ce qui supprime le défaut de la
ligne 133). 12 configurations, 20 réplicats, mêmes mesures, mêmes graines, mêmes fonctions
importées que le script audité (`chute_par_personne`, `top1_par_personne`).

| nul à exactitude-vérité appariée | rho moyen | médiane | p5 | p95 | rho réel 0,965 le dépasse ? |
|---|---|---|---|---|---|
| remplissage **marginal** (défaut l. 133 corrigé) | **0,9741** | 0,9720 | 0,9500 | **0,9934** | **non** |
| remplissage **uniforme** (comme N0) | 0,9815 | 0,9860 | 0,9580 | 0,9930 | **non** |

Le rho observé (0,965) tombe **à l'intérieur** de la distribution nulle (entre p5 et p95)
dans les deux cas. Détail par configuration, remplissage marginal — la fuite y reste une
fonction monotone de l'exactitude, ce qui est tout le sujet :

| configuration | exactitude | chute | top-1 |
|---|---|---|---|
| JSON Persona - GPT4.1 | 0,5904 | +0,161 | 31,62 % |
| Text Persona - Gemini-Flash2.5 | 0,5596 | +0,133 | 19,63 % |
| Text Persona - GPT4.1-mini | 0,5582 | +0,129 | 18,23 % |
| JSON Persona - GPT4.1-mini | 0,5504 | +0,123 | 17,67 % |
| … | … | … | … |
| PMM k=10 | 0,4747 | +0,051 | 1,82 % |
| B0 tirage | 0,4323 | +0,010 | 0,15 % |

**Conséquence.** Le défaut réel (l. 133) fait passer la fuite du nul de 41,2 % à 31,6 % de
top-1 : il gonflait le **niveau** de fuite d'un facteur ~1,3. Il ne change **pas** le
verdict, parce que le verdict porte sur une **corrélation de rangs** entre 12 points, et la
monotonie fuite/exactitude survit à n'importe quel schéma de remplissage. Le renversement
publié n'est donc pas la conséquence de la réparation du défaut : il est la conséquence du
**changement de nul**.

### 1.4 Existait-il un résultat qui aurait fait échouer ce test ?

**Formellement oui, épistémiquement non.**

Sous N1/N2/N3, les deux axes tombent au plancher pour *toutes* les configurations. Mesuré :
la dispersion inter-configuration rapportée au bruit interne (demi-largeur d'IC bootstrap)
vaut 14,8 (fidélité) et 7,5 (top-1) pour le réel, contre **0,45 – 2,0** et **0,16 – 0,23**
pour les nuls corrigés. Autrement dit, sous les nuls corrigés, la variation entre
configurations est **plus petite que le bruit d'estimation d'une seule configuration** :
les 12 points sont du bruit pur.

Le Spearman de 12 points de bruit est la loi de Spearman sous H0 : je l'ai simulée
(200 000 tirages, n = 12) → p95 = **0,4965**. Les p95 observés des cinq nuls corrigés :
0,547 – 0,594. La distribution nulle « corrigée » **est**, à un léger décalage près, la
distribution nulle d'absence totale d'information.

Donc le test préenregistré se réduit à : *« rho_reel dépasse-t-il 0,55 ? »*, c'est-à-dire
*« la corrélation observée est-elle significative à 5 % pour n = 12 ? »*. Un résultat
concevable le faisait échouer : rho_reel ≤ 0,55. Mais rho ≈ 0,96–0,97 était **déjà établi et
publié** (`c7-disjoint-resultats.md` §1 : 0,969 ; ici 0,965, p = 3,9·10⁻⁷). L'issue était
donc connue avant l'exécution. **Le test ne discrimine pas l'hypothèse qu'il annonce
discriminer ; il re-teste rho ≠ 0.** Je le dis sans ménagement : sous cette forme, il ne
vaut rien comme témoin de l'objection d'exactitude.

Le préenregistrement avait prévu ce risque (§8) et posé un garde-fou : « si plus de la
moitié des réplicats ont un axe dégénéré, l'issue B est faiblement informative ». Ce
garde-fou **ne peut pas se déclencher** : il est opérationnalisé comme
`len(set(np.round(f, 12))) < 2`, c'est-à-dire un axe *exactement constant*, ce qu'un bruit
continu ne produit jamais. Résultat annoncé : 0/100 réplicats dégénérés — chiffre exact et
sans valeur. Le garde-fou juste était « la dispersion inter-configuration dépasse-t-elle le
bruit intra ? » : réponse **non**, d'un facteur 5.

**Ce qu'il faudrait faire.** Publier le nul à exactitude-vérité appariée et remplissage
marginal (§1.3) comme témoin principal ; présenter N1–N3 comme ce qu'ils sont, un plancher
« aucune information individuelle », utile mais non probant sur l'objection d'exactitude.
**Coût** : le script d'audit existe et tourne en **~130 s** pour 20 réplicats × 12
configurations ; il faut le porter en script préenregistré du dépôt, soit une demi-journée.

---

## DÉFAUT FATAL 2 — la conclusion publiée inverse un verdict que les mesures ne renversent pas

**Gravité : fatale (c'est la conséquence rédactionnelle du défaut 1).**

`c7-nul-corrige-resultats.md` §6 conclut « Issue B », retire la réfutation, et §7 prescrit
six modifications de l'article dont le **titre**, le **résumé**, le **tableau 3** et la
**figure 2**, plus le passage de « seize prédictions réfutées » à quinze. Sur la base du §1
ci-dessus, ces six modifications sont à **suspendre**, et la figure 2 en particulier ne doit
pas être rebasculée sur `construction == "N2 vecteur d'autrui"` : la bande ainsi tracée
serait la bande d'un nul sans information, que le point observé dépasse trivialement.

**Ce qu'il faudrait faire** : geler les modifications §7, conserver la formulation
`c7-disjoint-resultats.md` §Verdict (« qualité globale et fuite montent ensemble »), et
ajouter la correction du défaut l. 133 comme un raffinement qui ne change pas le verdict.
**Coût** : nul en calcul ; une demi-journée de rédaction et la coordination avec les agents
qui écrivent en ce moment dans le manuscrit.

---

## DÉFAUT 3 — le contrôle d'exactitude est vacant là où il compte

**Gravité : de méthode (n'invalide pas les chiffres, invalide la garantie annoncée).**

Le rapport §2 annonce « exactitude visée atteinte **exactement** pour N1/N2 (écart moyen
0,00000) ». Vérifié dans le CSV : exact. Mais c'est **tautologique** :
`sortie_effectif_exact` écrit `round(q_i · n_obs_i)` cellules égales à la cible, puis le
contrôle mesure l'exactitude contre **cette même cible**. `ecart_max = 0,0000` et
`z_max = 0,000` pour N1, N2 et N3 : le contrôle ne peut pas échouer.

Et surtout, il ne mesure pas ce qui compte. La quantité que ces témoins prétendent
reproduire — et que la mission appelle « la marge d'exactitude par personne » — est
l'exactitude **contre la vérité**. Contre la vérité, l'écart n'est pas nul : il est de
**−0,10 à −0,12 en moyenne** (§1.1). Le contrôle publié valide l'échantillonneur, pas
l'appariement de la marge.

**Ce qu'il faudrait faire** : ajouter, à côté, le contrôle non trivial
`|exactitude(out[i], y[i]) − q_i|` et le publier. **Coût** : trois lignes, quelques minutes ;
il aurait fait apparaître le défaut 1 tout seul.

---

## DÉFAUT 4 — le mécanisme invoqué au §5 pour le « minorant » est faux, le fait ne l'est pas

**Gravité : formulation (le fait est vrai, l'explication publiée est fausse).**

Le rapport §5 explique le c = 0,432 (réel) contre 0,409 (N0) par : « les **erreurs** du
jumeau réel tombent sur des réponses de population, si bien qu'elles coïncident aussi avec
les leurres ». J'ai décomposé c par type de cellule (JSON Persona - GPT4.1, 60 items) :

| | c global | c sur cellules **justes** | c sur cellules **fausses** |
|---|---|---|---|
| jumeau **réel** | 0,4319 | **0,4776** | **0,3660** |
| nul exact-vérité, remplissage uniforme | 0,4097 | 0,4328 | **0,3763** |
| nul exact-vérité, remplissage marginal | 0,4250 | 0,4328 | 0,4138 |

**Les erreurs du jumeau réel sont *moins* typiques de la population que celles du nul
uniforme (0,366 contre 0,376), pas plus.** L'écart global vient **entièrement des cellules
justes** : 0,478 contre 0,433. Le jumeau réel a raison **préférentiellement sur les items
banals** — c'est un effet de *où il est exact*, pas de *comment il se trompe*. La phrase
« le jumeau converge vers la moyenne là où il se trompe » est démentie par la mesure.

Le **fait**, lui, tient et je le reproduis : à exactitude égale, un témoin synthétique fuit
davantage que le jumeau réel — 39,6 % (remplissage uniforme) et **31,6 %** (remplissage
marginal, défaut l. 133 corrigé) contre 20,73 % pour le jumeau réel. Le chiffre 31,6 %
recoupe indépendamment les 31,9 % de `c7_tautologie`.

**Le « minorant » n'est pas démontré, il est mal nommé.** Ce qui est démontré : *il existe
des prédicteurs synthétiques, à exactitude par personne identique, qui fuient 1,5 à 1,9 fois
plus que nos jumeaux*. Ce qui n'est pas démontré, et que « nos jumeaux sont un minorant »
laisse entendre : qu'un jumeau LLM futur ou meilleur atteindrait ce niveau. Les témoins qui
fuient davantage sont construits **à partir des réponses de la cible** ; ils bornent ce que
l'attaque peut extraire d'une exactitude donnée, pas ce qu'un générateur peut produire.

**Ce qu'il faudrait faire** : remplacer l'explication du §5 par la décomposition ci-dessus,
et remplacer « minorant » par « borne de ce que l'attaque extrait à exactitude égale ».
**Coût** : rédaction seule, la mesure est faite (script `audit3.py`, ~10 s).

---

## DÉFAUT 5 — le seuil z recalibré : ajustement postérieur, mais sans conséquence

**Gravité : de procédure (aucune sur le résultat).**

Les faits, vérifiés dans le CSV : le seuil préenregistré était 5 ; l'exécution a échoué sur
N1b (z max **5,203**) ; le seuil a été porté à √(2 ln M)+2 = 7,42 **après** cet échec.

C'est un ajustement postérieur à l'observation, et il doit être jugé comme tel. Deux choses
le sauvent :

1. **Il est dérivé, pas ajusté sur la valeur gênante.** Le maximum attendu de M = 2,36·10⁶
   gaussiennes vaut √(2 ln 2M) ≈ **5,45** > 5,203 : le seuil de 5 rejetait un
   échantillonneur **correct**. C'était une fausse alarme, et la même erreur de calibrage
   que celle déjà corrigée au préenregistrement. La marge « +2 » reste arbitraire et aurait
   dû être justifiée.
2. **Il ne change pas le verdict.** Avec le seuil initial de 5 (recalculé) :

| construction | z max | sort au seuil 5 |
|---|---|---|
| N1 mode de segment | 0,000 | passe (vacant, cf. défaut 3) |
| N1b (Bernoulli) | 5,203 | **rejetée** |
| N2 vecteur d'autrui | 0,000 | passe (vacant) |
| N2b (Bernoulli) | 5,237 | **rejetée** |
| N3 identités permutées | 0,000 | passe (vacant) |
| N4 mode global | 16,816 | rejetée (hors témoins) |
| N0 nul cassé | 4,950 | passe |

Trois des cinq témoins corrigés survivent au seuil préenregistré et donnent le même
verdict : la déviation est **immatérielle**. Elle n'est donc pas ce qui fait tomber ce
résultat — le défaut 1 l'est.

**Ce qu'il faudrait faire** : conserver la déviation, déclarée telle quelle, et ajouter la
phrase « le verdict est inchangé au seuil préenregistré, trois témoins sur cinq le
passant ». **Coût** : une phrase.

---

## DÉFAUT 6 — la divergence 0,118–0,206 est du bruit, mais N1 fuit réellement un peu

**Gravité : mineure.**

Sur 100 réplicats, l'écart-type du rho nul vaut 0,26–0,30 ; l'écart-type de la **moyenne**
est donc ~0,027. Les cinq moyennes (0,118 à 0,206) s'étalent sur ~3 écarts-types : ce n'est
**pas** du pur bruit, et le rapport a raison d'en donner l'explication (résidu d'information
non individuelle). Mesuré :

| témoin | top-1 (hasard = 0,0486 %) | δ | bits |
|---|---|---|---|
| N1 / N1b mode de segment | **0,061–0,063 %** | +0,0067 | +0,008 |
| N2 / N2b vecteur d'autrui | 0,040–0,042 % | +0,0016 | +0,000 |
| N3 identités permutées | 0,051 % | +0,0032 | +0,001 |

N1 fuit au-dessus du hasard (0,063 % contre 0,0486 %) : le mode de segment porte un reste
de signal de segment. Le rapport le dit et recommande N2 : **c'est le bon arbitrage**, il ne
change rien à la conclusion de cet audit. À noter aussi : les cinq distributions nulles sont
décalées positivement par rapport à la loi de Spearman sous H0 (moyennes +0,12 à +0,21,
Kolmogorov-Smirnov p < 10⁻³), ce qui est cohérent avec ce résidu.

---

## DÉFAUT 7 — points de reproductibilité et d'exactitude descriptive

**Gravité : mineure, mais à corriger avant publication.**

1. **rho porte sur 12 points, pas 13.** `spearman12` n'utilise que `noms_12` ; le 13ᵉ point
   (retest humain) est calculé et exclu, conformément au préenregistrement §2. Le rapport ne
   l'écrit pas explicitement dans le tableau §3, et la table §4 en montre 13 : le lecteur
   conclura naturellement 13. À préciser d'un mot. (Le jackknife du §3 ci-dessous est donné
   dans les deux lectures.)
2. **Chemin de cache non reproductible.** `analyses/c7_nul_corrige.py` l. 108-111 code en dur
   un chemin de scratchpad propre à une session
   (`/private/tmp/.../ed6061e6-.../c7-nul-corrige-baselines-60.pkl`). Sur toute autre
   machine, le script recalcule silencieusement les baselines : pas faux, mais l'« identité
   bit à bit » annoncée n'est vérifiable que sur cette session. À déplacer sous
   `resultats/` ou `data/`. **Coût** : une ligne.
3. **Comparaison de rho hétérogène (héritée, signalée par l'auteur).** Le rho réel de
   `c7-disjoint` (0,969) est mesuré sur items **disjoints** A/B ; celui-ci (0,965) sur items
   **entiers**. L'auteur a eu raison de tout recalculer sur le même plan et de le déclarer.
   Rien à corriger, à conserver.

---

## §3 de la mission — le rho lui-même : retrait point par point

rho de Spearman du prédicteur réel = **0,9650** sur les 12 configurations (p = 3,9·10⁻⁷).
Retrait de chaque point à tour de rôle :

* **12 points → 11 points : rho ∈ [0,9545 ; 0,9818], étendue 0,027.**
  Trois points seulement le font monter (B1 argmax, B2 argmax, PMM k=10 → 0,9818) ; sept le
  laissent à 0,9545 ; deux à 0,9636.
* 13 points (retest humain inclus) → 12 : rho de départ 0,9725, étendue **[0,9650 ; 0,9860]**.

**Aucun point aberrant ne porte le coefficient.** Le retrait le plus défavorable laisse
0,9545. C'est la partie la plus solide du dossier, et elle n'est pas en cause ici :
l'incertitude réelle de rho vient de n = 12 (la loi sous H0 a un écart-type de 0,30), pas
d'un point particulier. La troisième décimale reste ininterprétable, comme le dit le
rapport.

---

## §5 de la mission — la prudence de la conclusion est-elle exacte ?

La formulation publiée est : *« établi que le couplage n'est pas produit par la seule marge ;
non établie la causalité fidélité → identifiabilité »*.

**Elle est trop forte sur la première moitié, et à peu près juste sur la seconde.**

* « le couplage n'est pas produit par la seule marge » — **non établi**. Établi seulement :
  *le couplage n'est pas produit par un prédicteur dépourvu de toute information
  individuelle*, ce qui est vrai mais vide (un tel prédicteur ne peut pas fuir, donc ne peut
  pas coupler). Sur la marge **contre la vérité**, la mesure va dans l'autre sens (§1.3).
* « la causalité n'est pas établie » — exact, et à conserver.
* « soutenue — faiblement » (§6) — **à retirer**. La thèse n'est pas faiblement soutenue :
  elle reste réfutée par un témoin qui conserve la grandeur sous test.
* En revanche le rapport mérite d'être crédité : sa réserve §8/§6 (« dépasser un tel nul
  était presque acquis d'avance ») **est exactement le défaut fatal 1**. L'auteur a écrit
  l'objection qui détruit son propre résultat, puis a publié le résultat quand même. C'est
  l'honnêteté du dossier, et c'est aussi ce qui aurait dû arrêter la publication.

---

## Récapitulatif, par gravité

| # | défaut | nature | ce qu'il faut faire | coût |
|---|---|---|---|---|
| 1 | Les témoins corrigés détruisent l'exactitude contre la vérité ; un témoin qui la conserve reproduit le couplage (0,974 vs 0,965) | **FATAL** | Publier le nul à exactitude-vérité appariée, remplissage marginal, comme témoin principal | ~130 s de calcul, ½ journée de portage |
| 2 | Les six modifications de l'article prescrites au §7 inversent un verdict non renversé | **FATAL** | Geler §7 ; ne pas rebasculer la figure 2 sur N2 | ½ journée, coordination urgente |
| 3 | Le contrôle d'exactitude est vacant (mesuré contre la cible de substitution) | méthode | Ajouter le contrôle contre la vérité | minutes |
| 4 | Le mécanisme du « minorant » (§5) est démenti par la décomposition de c | formulation | Corriger l'explication, renommer « minorant » | rédaction |
| 5 | Seuil z recalibré après échec | procédure | Déclarer + « verdict inchangé au seuil 5 » | une phrase |
| 6 | N1 fuit au-dessus du hasard (0,063 % vs 0,0486 %) | mineure | Retenir N2, déjà recommandé | néant |
| 7 | rho sur 12 et non 13 points ; cache non reproductible | descriptive | Préciser ; déplacer le cache | une ligne |

---

## LA PHRASE EXACTE QUE L'ARTICLE A LE DROIT D'ÉCRIRE

> Le témoin de marge d'origine comportait un défaut réel — ses cellules fausses évitaient la
> vraie réponse de la personne (`c7_disjoint.py` l. 133), ce qui gonflait sa fuite d'un
> facteur 1,3 (top-1 41,2 % contre 31,6 % une fois les valeurs fausses tirées dans la
> marginale de population) ; ce défaut corrigé, le témoin continue de reproduire le
> couplage (rho 0,974, 5ᵉ–95ᵉ centiles [0,950 ; 0,993], contre 0,965 observé), et la
> prédiction (b) reste donc réfutée : la corrélation entre qualité d'imitation et
> ré-identifiabilité n'exige, pour être reproduite, qu'une exactitude par personne appariée
> et des positions exactes tirées au hasard. Cinq témoins supplémentaires, qui apparient
> cette exactitude contre une cible de substitution et non contre la personne, tombent au
> hasard sur les deux axes (top-1 0,040–0,063 % contre 0,049 %, 0,00 bit, exactitude contre
> la vérité 0,41–0,44 contre 0,53) ; le rho observé les dépasse, mais ce dépassement ne
> porte sur rien, leur distribution nulle étant celle du Spearman sous absence totale
> d'information à n = 12 (95ᵉ centiles 0,547–0,594 contre 0,497 attendu).

Rien de plus, rien de moins. En particulier, l'article **n'a pas** le droit d'écrire que la
réfutation est retirée, que la prédiction (b) est confirmée, ni que le couplage n'est pas
produit par la seule marge d'exactitude.
