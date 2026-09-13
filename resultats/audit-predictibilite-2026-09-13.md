# C7, audit : « la fuite suit la prédictibilité, non la rareté » — est-ce une découverte ou une tautologie ? (13 septembre 2026)

statut: courant
mandat: Attaquer l'affirmation établie sur `agent/mesures/equite-risque` selon laquelle le risque individuel de ré-identification décroît avec l'atypicité (ρ = −0,181) et croît avec la cohérence test-retest (+0,256). Déterminer si ce résultat survit (a) au contrôle du bruit de mesure, (b) à une autre définition de la rareté, (c) à l'analyse partielle rareté × stabilité, (d) au contrôle du nombre d'items, (e) au changement d'attaquant pour A-LLR pondéré par la rareté. Aucun appel payant, aucun réseau, aucun arrière-plan, aucune donnée individuelle imprimée.
agent: Claude Opus 5, Anthropic
ecriture: analyses/c7_audit_predictibilite.py, resultats/audit-predictibilite-2026-09-13.md, resultats/c7-audit-predictibilite.csv
lecture_seule: tout le reste du dépôt, notamment analyses/c7_reidentification.py, analyses/c7_attaquant_fort.py, analyses/c7_equite_risque.py (branche `agent/mesures/equite-risque`)
interdits: appel payant, réseau, recherche web, arrière-plan, fusion sur master, écriture dans article/manuscrit.md, impression de tout identifiant / réponse / combinaison individuelle
cout_reel_usd: 0.00

## 0. Préenregistrement — écrit et commité AVANT le premier calcul

### 0.1 Ce que je cherche à détruire

> ρ(risque, atypicité) = −0,181 [−0,225 ; −0,135] ; ρ(risque, cohérence test-retest) = +0,256 [+0,213 ; +0,293]. « La fuite suit la prédictibilité, pas la rareté. »

### 0.2 L'explication plate, et pourquoi elle est probablement la bonne

Le jumeau Twin-2K-500 est **construit à partir de la persona des vagues 1-3** (`data/twin2k500/README.md`, champs `wave1_3_persona_text` / `wave1_3_persona_json`) et l'attaque l'apparie contre les réponses **vague 4**. La « cohérence interne test-retest » est, par définition, l'accord entre v1-3 et v4 : c'est-à-dire **l'accord entre la source d'information de l'attaquant et sa cible**. Dire « les cohérents sont plus exposés » reviendrait alors à dire « on retrouve mieux quelqu'un quand les informations dont on dispose sur lui sont encore exactes » — un énoncé sur la **qualité de la donnée auxiliaire**, tautologique, sans rapport avec le jumeau LLM ni avec la vie privée.

### 0.3 Prédictions, fixées avant calcul

- **P1 (tautologie du témoin trivial).** Un attaquant **trivial** qui utilise, comme « jumeau », les **réponses v1-3 de la personne elle-même** — aucun modèle de langage — produira une corrélation risque ~ cohérence **au moins aussi forte** que celle du jumeau LLM : ρ_trivial ≥ +0,60. *Prédiction : vraie.*
- **P2 (médiation).** La corrélation partielle ρ(risque_LLM, cohérence | risque_trivial) **tombera sous +0,10 en valeur absolue**, c'est-à-dire que l'effet « cohérence » du jumeau LLM est entièrement porté par la qualité de la donnée auxiliaire. *Prédiction : vraie.*
- **P3 (rareté et stabilité confondues).** ρ(atypicité, cohérence) sera **négative et non nulle** (|ρ| ≥ 0,15) : les réponses rares sont aussi les moins stables. En conséquence, la corrélation **partielle** ρ(risque, atypicité | cohérence) sera **d'au moins 40 % plus faible** en valeur absolue que la corrélation brute −0,181. *Prédiction : vraie.*
- **P4 (définition de la rareté).** Le signe négatif **survivra** à un changement de définition de la rareté (rareté moyenne `−log q_j(x_ij)` sous les marginales de population hors pli ; et log-vraisemblance hors pli sous un modèle de classes latentes ajusté sur les **autres** personnes). *Prédiction : vraie — le signe est robuste à la définition, ce n'est pas là que l'affirmation casse.*
- **P5 (prédictibilité sans retest).** Une mesure de prédictibilité **n'utilisant pas le retest** — log-vraisemblance hors pli sous le modèle de classes latentes — corrélera **positivement** au risque, ρ ≥ +0,10. *Prédiction : vraie.* Mais je préenregistre aussi le point conceptuel : sous un modèle de population, « prédictible » et « typique » sont **la même variable**, donc P5 vraie ne sépare pas prédictibilité et rareté — elle montre qu'elles coïncident, et donc que l'opposition « prédictibilité *contre* rareté » est mal posée.
- **P6 (attaquant, le test décisif).** Sous **A-LLR pondéré par la rareté** (`c7_attaquant_fort.scores_hors_pli`, hors pli, bassin strictement identique), le signe de ρ(risque, atypicité) **s'inversera ou deviendra non significatif** : ρ_A-LLR ≥ −0,05. *Prédiction : vraie.* A-LLR est construit pour récompenser l'accord sur les modalités rares ; si le signe dépend de l'attaquant, le résultat n'est pas une propriété des données.
- **P7 (nombre d'items).** Le contrôle du nombre de réponses non manquantes (108 items) ne changera **pas** les conclusions (|Δρ| < 0,03) : sur les 60 items retenus, tout le monde est renseigné par construction. *Prédiction : vraie, c'est un confondant nul ici.*

### 0.4 Critère de réfutation de mon propre audit

**Mon audit est réfuté, et l'affirmation de l'agent tient**, si **toutes** les conditions suivantes sont réunies :
1. la corrélation partielle ρ(risque_LLM, cohérence | risque_trivial) **reste ≥ +0,15** (l'effet n'est pas médié par la qualité de la donnée auxiliaire) ; **et**
2. la corrélation partielle ρ(risque, atypicité | cohérence, prédictibilité hors retest) **reste ≤ −0,10** (la rareté protège au-delà de la stabilité) ; **et**
3. le signe reste **négatif et significatif sous A-LLR** (ρ_A-LLR ≤ −0,10).

Si (3) échoue seul, le résultat est **dépendant de l'attaquant** : l'article doit le dire ainsi, pas le présenter comme une propriété des données. Si (1) échoue, le corrélat « cohérence » est **tautologique** et doit sortir de la phrase.

### 0.5 Garde-fous

Bassin **strictement constant** entre toutes les conditions : les 2 058 humains vague 4, les mêmes 60 items toujours renseignés, les mêmes personnes attaquées (celles couvertes par `JSON Persona - GPT4.1`), risque `p_i(B = 100)` par la transformation déterministe du rang de `c7_equite_risque.risque_a_bassin_constant`. Graine fixée 20260913. Aucune donnée individuelle imprimée, aucun groupe de moins de 20 personnes. Le modèle de classes latentes et les marginales de rareté sont estimés **hors pli** (5 plis), jamais sur la personne évaluée.

<!-- FIN DU PREENREGISTREMENT — tout ce qui suit a été écrit après les calculs -->

---

Script `analyses/c7_audit_predictibilite.py`, données `resultats/c7-audit-predictibilite.csv`.
Durée totale 58 s, **aucune réduction de calcul n'a été nécessaire**. Aucun appel de modèle,
0,00 USD, aucun réseau. Bassin strictement constant partout : pool de 2 058 humains vague 4,
2 058 personnes attaquées, les 60 items toujours renseignés, `B = 100`. Graine 20260913.
Seule réduction déclarée : bootstrap à 1 000 tirages au lieu de 2 000, les corrélations
partielles étant recalculées à chaque tirage.

## 1. Verdict

**L'affirmation est à affaiblir, et sa seconde moitié est à réécrire.** Elle n'est ni
solide telle qu'écrite, ni entièrement tautologique. Précisément :

- **La moitié « rareté » tient, et tient au test le plus dangereux.** Le signe négatif
  survit à une autre définition de la rareté, au contrôle du nombre d'items, et surtout
  **au changement d'attaquant pour A-LLR pondéré par la rareté**. Ma prédiction P6, qui
  était le pari central de cet audit, est **réfutée**.
- **La moitié « prédictibilité » est en grande partie tautologique, et elle est mal
  nommée.** 58 % du corrélat de cohérence disparaît quand on contrôle un témoin sans aucun
  modèle de langage ; et la seule mesure de prédictibilité qui n'utilise pas le retest ne
  porte **aucun** signal propre.
- **Les deux coefficients bruts sont gonflés d'environ moitié** par la confusion entre
  rareté et stabilité (ρ = −0,423 entre elles).
- **Et rien de tout cela n'est propre au jumeau LLM** : toute la structure de corrélats se
  reproduit, en plus fort, chez un attaquant qui n'utilise aucun modèle.

## 2. Réplication exacte, d'abord

| quantité | branche attaquée | ici |
|---|---|---|
| top-1, attaque naïve, `JSON Persona - GPT4.1` | 0,2069 | **0,2071** |
| risque moyen `p(B = 100)` | 0,454 | **0,4542** |
| ρ(risque, atypicité) | −0,181 | **−0,181** [−0,222 ; −0,135] |
| ρ(risque, cohérence test-retest) | +0,256 | **+0,256** [+0,215 ; +0,295] |
| ρ(risque, nombre de réponses non manquantes) | +0,033 | **+0,034** [−0,008 ; +0,078] |
| top-1 A-LLR hors pli (`c7-attaquant-fort`) | 0,232 | **0,2323** |

La réplication est exacte à la troisième décimale, y compris pour A-LLR rejoué
indépendamment. Ce qui suit n'est donc pas un désaccord de calcul.

## 3. Le témoin qui tranche la question principale : un attaquant sans aucun LLM

Le jumeau Twin-2K-500 est construit sur la persona des **vagues 1-3** et l'attaque
l'apparie contre la **vague 4**. J'ai donc construit l'attaquant **trivial** : on remplace
le jumeau par les **réponses v1-3 de la personne elle-même**. Aucun modèle de langage,
aucune génération, même bassin, mêmes items, même `B`.

| | jumeau LLM | **attaquant trivial (v1-3)** |
|---|---|---|
| top-1 | 20,7 % | **81,6 %** |
| risque moyen `p(B = 100)` | 45,4 % | **91,8 %** |
| ρ(risque, **cohérence** test-retest) | +0,256 | **+0,646** [+0,619 ; +0,672] |
| ρ(risque, **atypicité**) | −0,181 | **−0,216** [−0,255 ; −0,173] |
| ρ(risque, rareté moyenne) | −0,213 | −0,167 |
| ρ(risque, nb de réponses non manquantes) | +0,034 | −0,001 |

**Deux lectures, toutes deux gênantes pour la phrase de l'article.**

1. **Le corrélat de cohérence est massivement une propriété de la donnée, pas du jumeau.**
   Un attaquant qui ne fait rien d'autre que comparer les réponses passées d'une personne à
   ses réponses présentes obtient +0,646 — deux fois et demie le coefficient attribué au
   jumeau LLM. C'est la tautologie annoncée : le score de cet attaquant **est** la cohérence.
   Prédiction P1 (ρ ≥ +0,60) : **confirmée**.
2. **Le corrélat d'atypicité n'est pas propre au jumeau non plus** — il est même plus
   négatif sans LLM (−0,216 contre −0,181). Le phénomène « les atypiques sont moins
   retrouvés » est donc une propriété de **tout appariement de réponses d'enquête bruitées**,
   pas une découverte sur les jumeaux LLM.

**Médiation (P2).** En tenant constante l'exposition sous l'attaquant trivial :

> ρ(risque_LLM, cohérence | risque_trivial) = **+0,107 [+0,063 ; +0,147]**, contre +0,256 brut.

**58 % de l'effet disparaît**, mais l'intervalle exclut encore zéro : ma prédiction P2
(chute sous +0,10) est **manquée de peu, donc non confirmée**. Je l'écris plutôt que de
l'arrondir. *Robustesse :* le contrôle précédent est saturé — 79,9 % des personnes sont à
`p_trivial = 1` — donc potentiellement trop faible. Refait sur le **rang** trivial, qui n'a
pas de plafond, le résultat est **identique à trois décimales** (+0,107 [+0,063 ; +0,150]).
Le sous-ajustement n'explique pas le résidu.

**Conclusion de la section.** Le corrélat de cohérence est, aux deux tiers, l'énoncé
« on retrouve mieux quelqu'un quand ce qu'on croit savoir de lui est encore exact ». Le
tiers restant est réel mais petit, et il ne soutient pas le mot « prédictibilité ».

## 4. Rareté et stabilité sont la même chose vue deux fois — pour moitié

| paire | ρ de Spearman |
|---|---|
| atypicité ↔ **cohérence test-retest** | **−0,423** |
| atypicité ↔ rareté moyenne (−log marginale, leave-one-out) | +0,599 |
| atypicité ↔ prédictibilité hors pli (classes latentes) | −0,482 |
| cohérence ↔ prédictibilité hors pli | +0,370 |
| **rareté moyenne ↔ prédictibilité hors pli** | **−0,702** |

Les réponses rares sont bien les moins stables (−0,423) : P3 est **confirmée**. Les deux
corrélats de l'article ne sont donc pas deux axes indépendants. À l'autre tenue constante,
sous l'attaque naïve :

| corrélation partielle | valeur | brut |
|---|---|---|
| risque ~ **atypicité \| cohérence** | **−0,082 [−0,123 ; −0,039]** | −0,181 |
| risque ~ atypicité \| cohérence + nombre d'items | −0,082 [−0,123 ; −0,038] | −0,181 |
| risque ~ atypicité \| cohérence + prédictibilité hors pli | −0,082 [−0,127 ; −0,037] | −0,181 |
| risque ~ **cohérence \| atypicité** | **+0,202 [+0,161 ; +0,242]** | +0,256 |
| risque ~ cohérence \| atypicité + nombre d'items | +0,202 [+0,162 ; +0,242] | +0,256 |
| risque ~ **prédictibilité hors pli \| cohérence** | **+0,018 [−0,028 ; +0,060]** | +0,111 |
| risque ~ prédictibilité hors pli \| atypicité | +0,028 [−0,016 ; +0,071] | +0,111 |

**Le coefficient d'atypicité perd 55 % de son amplitude** (−0,181 → −0,082) dès que la
stabilité est tenue constante. P3 est confirmée dans sa partie quantitative (chute ≥ 40 %).
L'effet ne disparaît pas — l'intervalle exclut zéro — mais un ρ de −0,08 ne porte pas une
« contribution conceptuelle majeure » contre la k-anonymité.

**Le nombre de réponses non manquantes n'est pas un confondant ici** : ρ brut +0,034, et
les partielles ne bougent pas d'un millième. P7 **confirmée**. C'était attendu : sur les 60
items retenus, tout le monde est renseigné par construction.

## 5. La prédictibilité sans retest ne dit rien — et elle n'est pas séparable de la rareté

La mesure demandée, sans aucun recours au retest : la log-vraisemblance des réponses v4 de
la personne sous un **modèle de classes latentes ajusté sur les autres personnes, hors pli**
(12 classes, 5 plis, 80 itérations EM). Brute : ρ = **+0,111 [+0,067 ; +0,154]** — P5
confirmée à la lettre. Mais **+0,018 [−0,028 ; +0,060]** une fois la cohérence tenue
constante : **elle ne porte aucun signal propre**.

Et surtout, le point conceptuel préenregistré est confirmé par les chiffres : ρ(rareté,
prédictibilité hors pli) = **−0,702**. Sous un modèle de population, « prédictible » et
« typique » sont **la même variable au signe près**. L'opposition « la fuite suit la
prédictibilité, *non* la rareté » **oppose donc deux choses qui ne sont pas opposables** :
ce que l'article appelle prédictibilité est en fait la **stabilité individuelle**, et ce
qu'il appelle rareté est la **typicité de population**. Ce sont deux axes distincts, mais
aucun des deux ne s'appelle « prédictibilité ».

## 6. Le test décisif : A-LLR pondéré par la rareté — et ma prédiction est réfutée

A-LLR récompense explicitement l'accord sur une modalité **rare** (`log(a_j / q_j)`) : c'est
l'attaquant **construit pour exploiter la rareté**. Rejoué hors pli, bassin strictement
identique, top-1 0,2323 (conforme au 0,232 publié) :

| corrélat | naïf (Hamming) | **A-LLR (hors pli)** |
|---|---|---|
| **atypicité (distance au mode)** | −0,181 [−0,222 ; −0,135] | **−0,185 [−0,228 ; −0,138]** |
| **rareté moyenne (−log marginale, LOO)** | −0,213 [−0,255 ; −0,173] | **−0,237 [−0,275 ; −0,198]** |
| prédictibilité hors pli | +0,111 | +0,089 [+0,043 ; +0,132] |
| cohérence test-retest | +0,256 | +0,245 [+0,205 ; +0,286] |
| nombre de réponses non manquantes | +0,034 | +0,017 [−0,024 ; +0,060] |
| **partielle atypicité \| cohérence** | −0,082 | **−0,093 [−0,138 ; −0,048]** |
| partielle atypicité \| cohérence + prédictibilité | −0,082 | −0,101 [−0,146 ; −0,057] |
| partielle cohérence \| atypicité | +0,202 | +0,187 [+0,143 ; +0,232] |

**Ma prédiction P6 est réfutée, et réfutée franchement.** J'avais prédit ρ ≥ −0,05, c'est-à-dire
une inversion ou une disparition du signe. Le signe ne bouge pas : il est **identique
(−0,185 contre −0,181), et il est plus fort encore sur la définition alternative de la
rareté (−0,237 contre −0,213)**. Donner à l'attaquant les moyens d'exploiter la rareté ne
lui permet pas d'exposer davantage les atypiques. Le signe négatif n'est **pas** un artefact
du choix d'attaquant. C'est le seul élément qui protège l'affirmation, et il la protège bien.

**Stratification** par quintile de cohérence (aucun groupe < 20), en complément des
partielles : ρ(risque, atypicité) intra-quintile vaut en moyenne −0,095 sous Hamming (min
−0,296, max +0,064 — une strate change de signe) et −0,100 sous A-LLR (min −0,235, max
−0,016). Même ordre de grandeur que les partielles, et **hétérogène** sous Hamming.

**P4 confirmée** : le signe survit au changement de définition de la rareté, dans les deux
attaquants. Ce n'est pas là que l'affirmation casse.

## 7. Verdict contre mon propre préenregistrement

| prédiction | résultat |
|---|---|
| **P1** ρ_trivial(cohérence) ≥ +0,60 | **confirmée** : +0,646 |
| **P2** médiation sous +0,10 | **non confirmée, de peu** : +0,107 [+0,063 ; +0,147] (58 % de chute) |
| **P3** ρ(atyp, cohérence) ≤ −0,15 et chute ≥ 40 % de la partielle | **confirmée** : −0,423 ; chute de 55 % |
| **P4** signe robuste à la définition de la rareté | **confirmée** (−0,213 ; −0,237 sous A-LLR) |
| **P5** prédictibilité sans retest ρ ≥ +0,10 | **confirmée brute** (+0,111), **annulée en partielle** (+0,018) |
| **P6** signe inversé ou nul sous A-LLR | **RÉFUTÉE** : −0,185, inchangé, plus fort sur la rareté moyenne |
| **P7** nombre d'items non confondant | **confirmée** : +0,034, partielles inchangées |

**Mon critère de réfutation (§0.4)** exigeait les trois conditions pour que l'affirmation
tienne : (1) médiation ≥ +0,15 — **échoue** (+0,107) ; (2) partielle atypicité ≤ −0,10 —
**échoue sous Hamming** (−0,082), **passe de justesse sous A-LLR** (−0,101) ; (3) signe
négatif et significatif sous A-LLR — **passe nettement** (−0,185).

Deux conditions sur trois ne sont pas réunies : **l'affirmation ne tient pas telle qu'elle
est écrite**. Mais la condition décisive, celle que j'avais moi-même désignée comme la plus
dangereuse, tient : **l'affirmation ne doit pas être retirée, elle doit être affaiblie et
renommée.**

## 8. La formulation exacte que l'article doit employer

La phrase actuelle — « la fuite suit la prédictibilité, non la rareté » — doit **disparaître**.
Elle est fausse sur trois points : elle appelle « prédictibilité » ce qui est de la
stabilité ; elle oppose deux quantités qui sont corrélées à −0,70 quand on les mesure
proprement ; et elle attribue au jumeau LLM une structure qui se reproduit en plus fort
sans aucun LLM. Remplacement défendable, chaque chiffre vérifié ci-dessus :

> Les personnes les plus exposées ne sont pas les plus atypiques : le risque individuel
> décroît avec la distance au mode (ρ = −0,181 [−0,222 ; −0,135]) et avec la rareté moyenne
> des réponses sous les marginales de population (−0,213 [−0,255 ; −0,173]), et ce signe est
> **inchangé sous un attaquant par rapport de vraisemblance explicitement pondéré par la
> rareté** (−0,185 [−0,228 ; −0,138] et −0,237 [−0,275 ; −0,198]) : il ne s'agit donc pas
> d'un artefact du choix d'attaquant. L'exposition croît en revanche avec la **stabilité
> test-retest** de la personne (+0,256 [+0,215 ; +0,295]). Ces deux corrélats ne sont pas
> indépendants — rareté et instabilité vont de pair (ρ = −0,423) — et chacun perd environ la
> moitié de son amplitude quand l'autre est tenu constant (atypicité : −0,082
> [−0,123 ; −0,039] ; stabilité : +0,202 [+0,161 ; +0,242]) ; le nombre de réponses
> renseignées n'y contribue pas (+0,034 [−0,008 ; +0,078]). Le corrélat de stabilité
> **n'est pas une propriété du jumeau LLM** : un attaquant qui remplace le jumeau par les
> réponses antérieures de la personne elle-même, sans aucun modèle de langage, atteint
> 81,6 % de top-1 et un corrélat de stabilité de +0,646 ; à exposition triviale tenue
> constante, il ne reste au jumeau que +0,107 [+0,063 ; +0,147]. Il faut donc lire ce
> résultat comme un énoncé sur l'appariement de réponses d'enquête bruitées en général —
> l'attaquant réussit quand l'information auxiliaire dont il dispose est encore exacte — et
> non comme une propriété des jumeaux LLM. Une mesure de prédictibilité qui n'utilise pas le
> retest (log-vraisemblance hors pli sous un modèle de classes latentes ajusté sur les autres
> personnes) ne porte aucun signal propre (+0,018 [−0,028 ; +0,060] à stabilité constante) et
> est elle-même colinéaire à la typicité (ρ = −0,702 avec la rareté moyenne) : nous
> n'opposons donc pas « prédictibilité » et « rareté », qui ne sont pas séparables sous un
> modèle de population.

Et la portée, en une phrase, qui reste une contribution réelle :

> Une défense de type k-anonymité, qui protège les combinaisons rares, ne vise pas la
> population ici la plus exposée ; mais l'effet est modeste une fois la stabilité
> individuelle tenue constante (ρ ≈ −0,08 à −0,10), et il n'est pas spécifique aux jumeaux
> LLM.

## 9. Ce que ce travail ne montre pas

1. **Un seul jeu.** Tout est mesuré sur Twin-2K-500. La branche attaquée répliquait le
   signe d'atypicité sur Park et al. (−0,154) ; je n'ai pas rejoué le témoin trivial ni
   A-LLR là-bas — Park n'a pas de structure v1-3 / v4 comparable, le témoin trivial n'y est
   donc pas définissable à l'identique.
2. **Une seule cible de jumeau** (`JSON Persona - GPT4.1`) et un seul bassin de référence
   (humains vague 4). Les sept autres configurations ne sont pas rejouées.
3. **Monde fermé seulement.** Aucune de ces corrélations n'est mesurée dans le régime de
   décision en monde ouvert.
4. **Aucune causalité.** Rien n'établit que rendre une personne moins stable la protégerait ;
   la stabilité test-retest est ici une caractéristique observée, pas un levier.
5. **La corrélation partielle n'est pas un contrôle parfait** : elle résidualise linéairement
   des rangs. Un effet non monotone de la rareté passerait au travers. La stratification par
   quintile (§6) est le garde-fou, et elle montre une hétérogénéité réelle sous Hamming.
