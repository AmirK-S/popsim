# Variance de génération du chiffre de titre — résultats — L'ÉCHEC DE LA FAMILLE B BORNÉ le 13 septembre 2026

statut: provisoire
borne_par: resultats/c7-pilote-regeneration-resultats.md
fait_foi: resultats/c7-variance-generation.csv (pour les chiffres de ce rapport) ; resultats/c7-pilote-regeneration-resultats.md §2.4 (pour la portée de l'échec de la famille B)
note_statut: en-tete et bandeau de bornage poses a l'integration du 13/09 par Claude Opus 5, sous-agent integration seconde vague ; le corps d'origine est conserve mot pour mot
mandat: Établir si le taux de ré-identification publié pour Twin-2K-500 (20,7 %) est un tirage unique d'un procédé de génération dont la variabilité n'est pas bornée par nos intervalles bootstrap sur les personnes, et appliquer les seuils S1 et S2 fixés au préenregistrement.
agent: Claude Opus 5, Anthropic — sous-agent variance de génération
ecriture: analyses/c7_variance_generation.py, resultats/c7-variance-generation-preenregistrement.md, resultats/c7-variance-generation-resultats.md, resultats/c7-variance-generation.csv
lecture_seule: tout le reste
interdits: appel payant, réseau, recherche web, commit sur master, fusion, arrière-plan, régénération de jumeaux, article/manuscrit.md
cecite: je n'ai pas lu article/manuscrit.md ni resultats/article-synthese.md au-delà des lignes citant « 20,7 % » ; je n'ai pas relancé c7_reidentification.py (je réutilise son CSV tel quel, après avoir vérifié son protocole dans le code) ; je n'ai pas ouvert les invites réellement envoyées par l'équipe amont — elles ne sont pas observables localement, donc je ne peux pas vérifier que deux bras nommés différemment diffèrent bien par ce que leur nom annonce ; je n'ai pas mesuré la variabilité de re-génération à condition constante, parce qu'aucun réplicat n'existe sur disque
cout_reel_usd: 0.00

> ## BORNÉ, le 13/09/2026 — l'échec de la famille B ne dit rien de la reproductibilité du bras de titre
>
> **État : BORNÉ** (le fait tient dans un périmètre plus étroit, et le périmètre est nommé).
> Fait foi : `resultats/c7-pilote-regeneration-resultats.md`, §2.4.
>
> **L'inférence bornée** (§9) : « l'échec complet de la famille B — sept bras dont pas un ne
> dépasse le hasard — montre que reproduire un pipeline de génération qui porte réellement la
> personne n'est pas acquis ». Le **fait** tient : ces bras échouent au contrôle
> d'interprétabilité. Sa **portée** est retirée. La famille B n'a jamais tenté de reproduire le
> pipeline amont et ne le pouvait pas : ses propres invites (`CONSIGNE`, `analyses/c7_gen.py`
> l. 216-224), trois modèles ouverts distincts, une persona **tronquée à 8 000 caractères** et
> une sortie en texte brut, là où le pipeline amont envoie **44 348 jetons** en un seul appel.
> Elle était **une autre expérience**, pas une régénération manquée du bras de titre : son échec
> ne peut servir d'argument ni pour ni contre la reproductibilité de ce bras.
>
> **Ce qui tient entièrement** : S1 (étendue **5,3513 fois** la largeur de l'intervalle
> publié), S2 (**99,07 %** de la variabilité imputable au bras, **0,93 %** aux personnes), R2
> (le bras de titre est le maximum des huit, et le plus fidèle), et le fait qu'**aucun
> réplicat** du bras de titre n'existe. La recommandation du §9 — conditionner toute dépense au
> passage préalable du contrôle d'interprétabilité — tient aussi, pour une raison désormais plus
> forte : la configuration du bras de titre n'est pas reconstituable depuis les sources
> publiques (`c7-pilote-regeneration-resultats.md` §2).
>
> **Compte non réconcilié, signalé sans être tranché** : le préambule ci-dessous parle de
> « cinq jumeaux régénérés » sur un bassin de 120, le §9 et le pilote de « sept bras ».

Contrôle préalable exécuté avant toute interprétation, comme le mandat l'exige :
`analyses/c7_controle_interpretabilite.py`. Verdict sur le bassin de 120 personnes —
`JSON Persona - GPT4.1` **PASSE** (top-1 38,92 % [30,96 ; 47,08] contre baseline
démographique 13,25 % [7,92 ; 19,46], IC disjoints). Les cinq jumeaux régénérés localement
de la nuit du 11 au 12 échouent tous (0,00-0,54 %, hasard 0,83 %). Le bras de titre est donc
interprétable ; les bras locaux ne le sont pas, et le §2 en tire la conséquence.

---

## 1. Le verdict, en trois lignes

**Les deux seuils préenregistrés sont franchis, et largement.**

- **S1** — l'étendue entre bras vaut **5,3513 fois** la largeur de l'intervalle bootstrap
  publié (18,5544 points contre 3,4673). Le seuil était à 2. **Les intervalles publiés sont
  trop étroits.**
- **S2** — **99,07 %** de la variabilité observée est imputable au bras, **0,93 %** aux
  personnes. Le seuil « l'IC ne borne pas l'incertitude » était à 90 %.
- **R2** — le bras de titre est le **maximum** des huit bras mesurés. Il est aussi le plus
  fidèle des huit. Les deux faits doivent être écrits ensemble.

Et le fait qui commande tous les autres : **aucun réplicat du bras de titre n'existe**, dans
aucune famille, sous aucune graine. La variabilité de re-génération à condition constante
n'est pas mesurée par ce travail. Elle est seulement **encadrée**, très lâchement.

## 2. L'inventaire réel, établi depuis les données

Le dépôt contient **vingt jeux de sorties de jumeaux** sur disque, ce qui est beaucoup, et
**zéro réplicat**, ce qui est le seul chiffre qui compte.

**Famille A — 13 configurations publiées par l'équipe amont**
(`data/twin2k500/llm_specs/`, 2 058 personnes, 108 items). Les répertoires `llm/` et
`llm_specs/` sont deux copies identiques octet pour octet du même contenu : ce ne sont pas
26 bras mais 13. Sur ces 13, `c7_reidentification.py` en retient **8** comme admissibles
(les 5 autres écartés par l'audit de provenance : masque d'items défaillant ×2, exposition
par entraînement, deux `Persona Summary` suspects). **Deux familles de modèles seulement** y
sont représentées : GPT-4.1 / GPT-4.1-mini pour 12 bras, Gemini-Flash2.5 pour un seul. Le
reste de la variation est de l'invite, pas du modèle.

**Famille B — 7 bras régénérés localement** (`data/traces/c7-gen/`, 3 modèles × 2 recettes,
plus une condition de température, 200 personnes chacun). **Inutilisables**, et pas par
commodité : le contrôle d'interprétabilité les disqualifie. Leurs jumeaux ré-identifient
entre 0,0 et 0,8 % contre un hasard de 0,83 % et une baseline démographique de 9,20 % sur le
même bassin. Un contraste entre eux comparerait deux générateurs de bruit — c'est exactement
le sinistre que ce contrôle existe pour empêcher. C'est aussi la seule famille où nous
contrôlons modèle, invite et température, et elle est perdue.

**Famille C — 3 bras auxiliaires de granularité** (30 à 40 personnes). Effectifs trop
faibles pour porter une mesure de variance.

**Le point décisif.** Dans les trois familles, **aucune condition n'a deux exécutions**.
La famille B a une graine unique par condition (`GRAINE = 20260912`). La famille A ne
documente aucune répétition. Le bras de titre `JSON Persona - GPT4.1` est seul de son espèce :
il n'existe pas d'autre exécution de JSON Persona sous GPT-4.1, ni sous une autre graine, ni
sous une autre température. **Le chiffre de titre repose sur une génération unique, et le
dépôt ne contient rien qui permette de savoir de combien une seconde génération l'aurait
déplacé.**

## 3. La dispersion entre bras, à bassin strictement constant

Protocole vérifié dans le code avant d'adopter le CSV (`c7_reidentification.py`, l. 144-175) :
bassin de candidats invariant à 2 058 pour tous les bras ; les 60 items communs calculés
**une seule fois, hors de la boucle sur les bras et depuis les références humaines seules**,
donc aucun bras ne peut déplacer le bassin d'items ; même distance de Hamming ; même
convention de départage des ex æquo (20 tirages) pour tous ; graine fixée. La convention de
départage n'est pas neutre — le mandat rappelle qu'elle vaut un facteur 1,32 sur Twin — mais
elle est ici **identique d'un bras à l'autre**, ce qui est la condition pour que la
comparaison ait un sens.

Cible : `humains vague 4`. Taux top-1, valeurs du CSV non arrondies :

| bras | n attaquées | top-1 | IC bootstrap (personnes) | exactitude |
|---|---:|---:|---|---:|
| **JSON Persona - GPT4.1** | 2 058 | **20,6803 %** | **[18,9600 ; 22,4272]** | **0,5740** |
| Text Persona - Gemini-Flash2.5 | 2 058 | 13,1171 % | [11,7783 ; 14,5045] | 0,5506 |
| *JSON Persona - GPT4.1-mini* | *1 000* | *12,2550 %* | *[10,2749 ; 14,2901]* | *0,5451* |
| Text Persona (Reasoning) - GPT4.1-mini | 2 058 | 9,3416 % | [8,1875 ; 10,6074] | 0,5437 |
| Text Persona (Repeating Questions) - GPT4.1-mini | 2 058 | 7,3542 % | [6,2948 ; 8,3508] | 0,5490 |
| Text Persona (Default Temperature) - GPT4.1-mini | 2 058 | 5,5807 % | [4,6404 ; 6,5016] | 0,5480 |
| Text Persona - GPT4.1-mini | 2 058 | 5,5272 % | [4,6331 ; 6,4578] | 0,5531 |
| Demographics Only - GPT4.1-mini | 2 058 | 2,1259 % | [1,5597 ; 2,7478] | 0,4998 |

*En italique : `JSON Persona - GPT4.1-mini` n'attaque que 1 000 personnes. Le bassin de
candidats reste 2 058, mais l'échantillon attaqué diffère : écarté du calcul principal par la
règle E2 du préenregistrement, reporté ici pour information.*

**Application de S1** (`L` = 22,4272 − 18,9600 = **3,4673 points**) :

| périmètre | étendue `E` | `E / L` | écart type inter-bras | verdict S1 |
|---|---:|---:|---:|---|
| 7 bras au bassin d'attaque plein | **18,5544 pt** | **5,3513** | 6,1527 pt | **franchi** |
| 6 bras riches (sans la baseline démographique) | **15,1531 pt** | **4,3703** | 5,8366 pt | **franchi** |

Le seuil est franchi dans les deux périmètres, par un facteur deux à plus de deux fois et
demie au-delà de la barre. Retirer la baseline démographique — le bras le plus dégradé, dont
on pourrait dire qu'il gonfle l'étendue — ne change pas le verdict.

## 4. La décomposition : ce qui vient des personnes, ce qui vient de la génération

Estimateur préenregistré (§4 du préenregistrement), effets aléatoires :
`V_gen = max(0, V_obs − V_intra)`, où `V_intra` est la variance d'échantillonnage moyenne
déduite des IC bootstrap par `SE = largeur / (2 × 1,96)`.

| périmètre | `V_obs` | `V_intra` (personnes) | `V_gen` | part génération | part personnes |
|---|---:|---:|---:|---:|---:|
| 7 bras | 0,00378559 | 0,00003509 | 0,00375050 | **99,07 %** | **0,93 %** |
| 6 bras riches | 0,00340655 | 0,00003941 | 0,00336714 | **98,84 %** | **1,16 %** |

La variabilité entre personnes est, à ce niveau, **un détail** : elle pèse environ un
centième de la variabilité totale. Nos intervalles publiés mesurent avec soin le centième et
ne disent rien des quatre-vingt-dix-neuf centièmes restants.

**Ce que ce chiffre ne dit pas, et il faut le dire à chaque citation.** Les bras disponibles
ne sont pas des répétitions du même procédé. Ils diffèrent par le modèle, par la
représentation de la personne et par le protocole d'inférence. `V_gen` mélange donc le bruit
d'une re-génération à condition identique et l'effet délibéré du choix de condition. C'est un
**majorant** de la première, pas une mesure de celle-ci. La bonne lecture est la suivante :
**le choix de configuration de génération domine massivement l'échantillonnage des personnes**,
et l'article publie un intervalle qui ne couvre que le second.

## 5. L'encadrement, par ses deux bouts

Faute de réplicat, la variabilité de re-génération n'est pas mesurée. Elle est encadrée, et
les deux bornes sont très éloignées l'une de l'autre — ce qui est en soi le résultat.

**Borne basse — le décodage seul.** `Text Persona - GPT4.1-mini` (5,5272 %) contre
`Text Persona (Default Temperature) - GPT4.1-mini` (5,5807 %) : même modèle, même
représentation de la personne, seul le réglage de décodage change. Écart **0,0534 point**,
soit **0,97 % en relatif**, IC largement recouvrants. C'est le seul contraste du dépôt qui
approche une re-génération pure, et il est presque nul. Il ne porte pas sur le bras de titre.

**Borne intermédiaire — le protocole d'inférence, à modèle et représentation constants.**
Les quatre bras `Text Persona - GPT4.1-mini` (par défaut, température par défaut,
raisonnement, questions répétées) s'étalent de **5,5272 %** à **9,3416 %** : étendue
**3,8144 points**, soit **69,01 %** en relatif du plus bas. Changer le protocole d'appel sans
changer ni le modèle ni l'invite de persona déplace donc le taux d'environ deux tiers de sa
valeur — et cet écart dépasse déjà, à lui seul, la largeur de l'intervalle publié.

**Borne haute — l'étendue entre bras**, 18,5544 points (§3), qui surestime certainement la
re-génération pure puisqu'elle intègre des changements de modèle délibérés.

Le fait qu'un changement de température ne fasse rien (0,97 %) pendant qu'un changement de
protocole d'appel fasse 69 % interdit d'extrapoler de l'un à l'autre. Nous ne savons pas où,
entre 0,97 % et l'étendue complète, se situe la re-génération du bras de titre.

## 6. Le substitut par tirages d'items, déclaré comme tel

Le mandat prévoit d'utiliser la variabilité entre tirages d'items comme borne inférieure
d'instabilité si les bras manquent. **Ce n'est pas la mesure demandée** : elle décrit ce que
le choix du sous-ensemble d'items fait bouger, pas ce que la re-génération ferait bouger. Elle
est reportée parce qu'elle est ce que nous avons.

Bras de titre, 30 tirages d'items par `k` (`c7-temoins-relecture.csv`) :

| `k` | moyenne | étendue des 30 tirages | écart type | écart type relatif |
|---:|---:|---|---:|---:|
| 12 | 1,2193 % | [0,3401 ; 3,0126] | 0,6442 pt | **52,83 %** |
| 20 | 3,2611 % | [1,5549 ; 6,0544] | 1,1633 pt | 35,67 % |
| 30 | 7,3353 % | [3,5374 ; 11,3217] | 1,9908 pt | 27,14 % |
| 40 | 11,0295 % | [4,7425 ; 16,5015] | 2,3202 pt | **21,04 %** |

Pour comparaison, la largeur relative de l'IC bootstrap du bras de titre à `k` = 60 vaut
**16,77 %**. L'instabilité entre tirages d'items reste donc, à `k` = 40, supérieure à
l'intervalle que nous publions à `k` = 60 — et elle décroît mécaniquement vers zéro à
`k` = 60, où il n'y a plus rien à tirer. Ce substitut confirme la direction sans chiffrer la
quantité demandée.

## 7. La prédiction, et son statut

Le §0 du préenregistrement le déclare sans détour : **j'avais lu la colonne `top1` de
`c7-reidentification.csv` avant d'écrire quoi que ce soit.** Aucune prédiction de ce travail
n'est aveugle sur les taux par bras, et je ne présenterai pas une rétrodiction comme une
prédiction réfutée ou confirmée. La question « ta prédiction est-elle réfutée ? » n'a donc
pas de réponse honnête ici, et c'est ma responsabilité, pas celle du mandat.

Ce qui était réellement engagé, et qui l'est resté : les **seuils** S1 (facteur 2) et S2
(50 % et 90 %), l'**estimateur** de décomposition, et les **règles d'exclusion** E1-E4, tous
fixés avant le premier calcul d'étendue ou de partage de variance. Ils ont été appliqués
mécaniquement et ils sont franchis. Un lecteur qui trouverait les seuils trop indulgents
notera qu'un seuil trois fois plus sévère — `E > 6 × L`, part de génération > 99 % — serait
**également** franchi sur le périmètre à 7 bras.

Un point mérite d'être signalé comme n'ayant pas joué en notre faveur et n'ayant pas été
cherché : le bras de titre est le **maximum** des huit. La règle R2 imposait de l'écrire quelle
qu'en soit l'explication. L'explication existe et elle est légitime — c'est aussi le bras le
plus fidèle des huit (exactitude 0,5740, rang 1 sur 8), et le couplage fidélité-fuite établi
par ailleurs rend ce maximum attendu plutôt que suspect. Mais la structure du défaut est la
même que celle du 0,13 % : **un chiffre publié seul, qui se trouve être l'extrême de la
distribution dont il est tiré.** La différence est qu'ici l'extrême s'explique, et que
l'explication doit accompagner le chiffre au lieu de le remplacer.

## 8. Ce que l'article doit écrire

La phrase exacte, à porter partout où le chiffre de titre apparaît sans son contexte :

> Ce taux repose sur une génération unique : les jumeaux que nous attaquons ont été produits
> une fois, sous un modèle et une invite donnés, et aucun réplicat de cette condition n'existe.
> L'intervalle [18,96 ; 22,43] est un bootstrap sur les personnes ; il ne borne pas la
> variabilité du procédé de génération. À bassin de candidats, items, attaque et convention de
> départage strictement constants, les sept configurations de jumeaux disponibles à effectif
> plein s'étalent de 2,13 % à 20,68 %, une étendue 5,35 fois plus large que cet intervalle, et
> 99 % de la variabilité observée est imputable à la configuration, moins de 1 % aux personnes.
> La configuration que nous rapportons est la plus élevée des sept, comme elle en est la plus
> fidèle. Ce chiffre doit donc se lire comme le taux de la configuration la plus fidèle dont
> nous disposons, non comme le taux d'un jumeau de grand modèle de langage en général.

Trois conséquences de rédaction, qui ne sont pas facultatives :

1. **Ne jamais présenter [18,96 ; 22,43] comme l'incertitude du chiffre.** C'est l'incertitude
   d'échantillonnage des personnes, et elle doit être nommée ainsi à chaque citation.
2. **Nommer la configuration à chaque citation du taux.** « 20,7 % » sans
   « JSON Persona - GPT4.1 » est une affirmation sur les jumeaux en général que nos données ne
   portent pas.
3. **Ne pas écrire que la variabilité de génération est faible.** Ce travail ne l'a pas
   mesurée. Le seul contraste proche d'une re-génération pure donne 0,97 % en relatif, mais il
   porte sur un autre bras et sur le décodage seul, tandis qu'un simple changement de protocole
   d'appel donne 69 %.

## 9. Ce qu'une dépense achèterait, et ce qu'elle n'achèterait pas

Cette décision appartient au responsable, pas à cet agent. Pour qu'elle soit prise en
connaissance de cause :

**Ce qui manque est précisément identifié** — des ré-exécutions de la condition
`JSON Persona - GPT4.1`, à invite et modèle rigoureusement constants, seule la graine
changeant. Cinq à dix exécutions donneraient l'étendue et l'écart type de re-génération du
bras de titre, et permettraient de publier un intervalle qui couvre les deux sources.

**Ce qu'une régénération n'achèterait pas.** Les invites réellement envoyées par l'équipe
amont ne sont pas observables localement : une régénération « de la même condition » serait
notre reconstruction de cette condition, pas la condition elle-même. Et l'échec complet de la
famille B — sept bras dont pas un ne dépasse le hasard — montre que reproduire un pipeline de
génération qui porte réellement la personne n'est pas acquis. Toute dépense devrait donc être
conditionnée au passage préalable de `c7_controle_interpretabilite.py`, sur un pilote de
petite taille, **avant** l'exécution complète.

En attendant, et que la dépense ait lieu ou non, la limite du §8 doit figurer dans l'article.
Elle ne dépend d'aucun résultat futur : elle décrit ce que nos données permettent de dire
aujourd'hui.
