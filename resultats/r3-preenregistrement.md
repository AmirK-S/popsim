# R3. Page de plan : la vraie ablation de l'etiquette

**Horodatage d'ecriture : 8 septembre 2026, 22:30:01 CEST (epoch 1788899401), horloge de la
machine.** Ecrite AVANT le moindre appel de modele de langage de R3. Aucun serveur n'a ete
lance par l'agent qui ecrit cette page ; a l'instant de l'ecriture, R1 tourne (file
`analyses/file_nuit_2.sh`, PID de file 89004 selon le journal de la nuit) et R2 est en
attente. Ce fichier n'est pas modifie apres le premier appel de R3. Toute divergence entre
ce plan et le rapport `resultats/r3-ablation-etiquette.md` sera declaree dans le rapport.

Reserve de forme, valable pour toute la nuit : popsim n'est pas sous suivi de version
(objection a45, journal des defauts). L'horodatage ci dessus est celui de la machine et rien
d'autre ne l'atteste. [CONFIRME par `date`, non atteste par un tiers]

---

## 1. Pourquoi ce run existe

`resultats/a45-relecture-adverse-2.md`, section 0, objection bloquante numero 1 :

> `systeme_c2` construit un prompt qui contient les onze attributs de
> `demographic_summary.csv` et rien d'autre. `systeme_c3` construit un prompt qui contient
> les environ 119 items de contexte, question et reponse en clair, et aucune demographie.
> C2 et C3 ne different donc pas par la presence ou l'absence de l'etiquette ideologique :
> ils echangent integralement leur entree.

Lecture du code faite a nouveau ici, sans intermediaire, `analyses/a5_agents_locaux_gss.py`
lignes 164 a 196 : `systeme_c2` = PREAMBULE + onze lignes `- Libelle: valeur` + CONSIGNE ;
`systeme_c3` = PREAMBULE + les blocs `Q: ... / A: ...` des items de contexte + CONSIGNE.
Aucune ligne demographique dans C3, aucune reponse d'enquete dans C2. [MESURE, lecture du
code]

Consequence : huit textes du dossier appellent « ablation de l'etiquette » un contraste ou
les deux facteurs (etiquette demographique, connaissance des reponses de la personne) sont
confondus. Les deux analogues statistiques du dossier bornent ce que le second facteur vaut
a lui seul : `B1 argmax` (regression sur les onze memes attributs) contre `B2 argmax` (plus
proche voisin sur les 119 memes items), a moteur constant et sans aucune etiquette retiree,
deplacent la chute sous permutation de 0,175 a 0,358 du plancher humain, facteur 2,0
[MESURE, a45 section 0, `a44-permutation.csv`]. Le passage de C2 a C3 vaut un facteur 6,2.

R3 fait l'ablation a un seul facteur, dans les deux regimes d'information.

## 2. Les conditions

Modele : **Qwen3-4B-Instruct-2507, Q4_K_M**, le meme fichier GGUF que C2 et C3 de a5
(`data/modeles/gguf/Qwen3-4B-Instruct-2507-Q4_K_M.gguf`). Meme gabarit de conversation
(`gabarit_qwen` de a5, variante `answer`, le prompt s'arrete sur `Answer:` sans espace
final), meme scoring par lettres a une position, memes controles de masse (`SEUIL_MASSE`
0,50 par appel), meme lecture des identifiants de tokens. Le gabarit et la variante de fin
sont **fixes d'avance et non sondes** : R2 sonde parce qu'il change de modele ; R3 ne change
pas de modele et doit rester comparable caractere pour caractere aux traces de a5.

Perimetre : les **150 personnes de `data/traces/a5-personnes.csv`** et les **58 items des six
familles** de `FAMILLES` dans `a2_baselines_gss.py` (memes items que R2 : depenses publiques,
confiance dans les institutions, avortement, libertes civiles, fin de vie, roles de genre).

Decoupage de contexte : **identique a C3**, c'est a dire les blocs de `grille()` de a2,
graine 20260903, l'item cible retire avec son bloc, les cousins thematiques presents. Ce
n'est PAS le regime severe de C3F. Les 58 items de famille se repartissent en 10, 12, 14,
10 et 12 sur les cinq blocs [MESURE], donc cinq prefixes de persona par personne pour 58
appels utiles.

| condition | contenu de l'invite systeme | contraste |
|---|---|---|
| **C3E** | les 11 attributs demographiques de C2, ideologie et parti compris, en tete, PUIS les ~119 reponses de la personne (item cible et son bloc retires) | **C3E contre C3** (trace `a5-C3-p1.jsonl`, memes cellules) |
| **C2S** | les 9 attributs de C2 **sans** `political_ideology` ni `political_party` | **C2 contre C2S** (trace `a5-C2-p1.jsonl`, memes cellules) |
| **C3ES** | les 9 memes attributs, PUIS les ~119 reponses | C3E contre C3ES, et C3ES contre C3 |

Construction des prompts, declaree ici pour etre verifiable : le bloc demographique de C3E
est **le corps de `systeme_c2` recopie sans un caractere de difference** (meme ordre des
onze attributs, meme convention `not reported` pour les attributs incomplets), et le bloc de
reponses est **le corps de `systeme_c3` recopie sans un caractere de difference**. Le prompt
de C2S est celui de `systeme_c2` appele sur neuf attributs. La verification hors ligne le
teste par egalite de chaines, pas par relecture a l'oeil.

Ordre d'execution : **C3E, puis C2S, puis C3ES.** Les personnes sont parcourues dans l'ordre
de `a5-personnes.csv` dans les trois conditions, de sorte qu'une troncature laisse des
**personnes entieres** et que les perimetres des conditions soient **emboites**.

## 3. Budget et ce qui se passe si le temps manque

Fenetre : R2 est arrete par SIGINT a 05:45 le 9 septembre, R3 demarre vers 05:47 et s'arrete
dur a 08:00. Budget ~2,2 h.

Couts unitaires mesures sur le run de a5 (Qwen3-4B, memes prompts, meme machine), resolus a
partir de deux equations a deux inconnues : C3 = 22 350 appels en 274,5 min avec 5 prefixes
et 149 appels par personne ; C3F = 3 498 appels en 78,1 min avec 6 prefixes et 58 appels par
personne. Il vient **8,6 s par prefixe de persona long** et **0,45 s par appel servi par le
cache** [MESURE, `data/traces/a5-run.log` et `a5-familles.log`]. C2 a tourne a 13 217
appels/h en regime etabli, soit 0,27 s par appel sur un prompt court [MESURE].

Projections [ESTIMATION] :

| condition | cout par personne | 150 personnes |
|---|---|---|
| C3E | 5 x 8,6 + 58 x 0,45 = **69 s** | 2,9 h |
| C2S | 1 prefixe court + 58 x 0,27 = **~17 s** | 0,7 h |
| C3ES | comme C3E, **69 s** | 2,9 h |

Le budget ne couvre donc pas C3E en entier. Regle fixee ici, avant tout appel : **le run
reserve a C2S le temps que la projection lui donne, majore de 15 pour cent, et fixe a C3E
une fin intermediaire egale a la fin dure moins cette reserve.** Motif : H2 est une
prediction dirigee, peu couteuse et decisive pour l'analogie v6 contre v8 ; la laisser
mourir parce que H1 a mange la nuit serait un choix fait par le hasard du debit et non par
le plan. C3ES ne tourne que si les deux premieres ont fini avant la fin dure.

Attendu : **C3E couvre environ 75 a 90 personnes sur 150, C2S les 150.** [ESTIMATION]

Consequence sur la puissance, ecrite d'avance : sur ~80 personnes et 58 items, le nombre de
cellules rares stables attendues est de l'ordre de 40 (R2 annonce 31 sur 60 personnes et ~78
sur 150). Les contrastes sur la rarete seront donc **sous puissantes** et sont declares
secondaires ; le contraste primaire H1 porte sur la chute sous permutation et l'exactitude,
qui utilisent toutes les cellules.

## 4. Hypotheses

Toutes les hypotheses sont enoncees dans le sens ou la these du dossier les predit. La
these, apres a44 et a45, est : **l'etiquette demographique, et d'abord l'etiquette
ideologique, fabrique un gabarit de groupe** ; elle rend les personnes du meme segment
echangeables, elle gonfle l'ecart entre segments, elle fait oser des modalites rares
typiques du groupe plutot que de la personne.

### H1. Ajouter l'etiquette a C3 (C3E contre C3)

**H1 n'est pas « la chute sous permutation augmente ».** C'est l'inverse, et c'est le point
qui rend le test refutable :

- **H1a** [dirigee] la chute d'exactitude sous permutation intra segment **diminue** de C3
  a C3E : `chute(C3E) < chute(C3)`. Si l'etiquette fabrique du gabarit de groupe, les
  personnes d'un meme segment deviennent plus echangeables, donc permuter coute moins.
- **H1b** [dirigee] le **ratio inter** (dispersion entre segments rapportee aux humains)
  **augmente** de C3 a C3E.
- **H1c** [dirigee] la **rarete de groupe sur personne** de a31 (`groupe_sur_personne`)
  **augmente** de C3 a C3E.
- **H1d** [dirigee] l'**exactitude par personne** de C3E est **superieure ou egale** a celle
  de C3 : ajouter de l'information vraie ne doit pas nuire. Une baisse serait un resultat en
  soi, contre la these naive « l'etiquette aide ».

### H2. Retirer l'ideologie de C2 (C2 contre C2S)

- **H2a** [dirigee] le **ratio inter sur l'axe ideologie** **tombe** de C2 a C2S. C'est
  l'analogue exact de v6 contre v8 chez Stanford, ou l'ecart entre camps s'effondre quand
  l'etiquette ideologique sort de l'invite.
- **H2b** [dirigee] la **chute sous permutation intra segment sous la segmentation
  ideologie** **augmente** de C2 a C2S (moins de gabarit ideologique, donc moins
  d'echangeabilite intra camp) ; **sans prediction** sous la segmentation sans ideologie.
- **H2c** [dirigee] la **rarete de groupe sur personne** **diminue** de C2 a C2S.
- **H2d** [bilaterale] exactitude par personne, C2 contre C2S.

### H3. L'etiquette ideologique pese plus que les neuf autres attributs

- **H3** [dirigee] |effet de C3E contre C3ES| **>** |effet de C3ES contre C3| sur la mesure
  primaire (chute sous permutation, segmentation sans ideologie). Autrement dit, les deux
  lignes `Political ideology` et `Political party` font plus que les neuf autres lignes
  reunies. Testee seulement si C3ES tourne sur au moins 30 personnes communes ; sinon
  declaree **non testee**, jamais « non rejetee ».

## 5. Mesures

Toutes sur les **memes cellules** (personnes communes aux deux conditions comparees, 58
items de famille), toutes appariees sur les personnes.

1. **Chute d'exactitude sous permutation intra segment**, `a44_commun.permuter_intra` et
   `a44_commun.exactitude`, 200 permutations, sous **DEUX segmentations**, comme a45
   l'exige :
   - `S_ideo` : les sept niveaux d'ideologie (segmentation publiee par a44) ;
   - `S_gra` : genre x race x age, **sans ideologie** (la segmentation de l'objection 2 de
     a45, celle sous laquelle v8 passe de 0,072 a 0,266).
   Publiees cote a cote. Aucune des deux n'est declaree « la vraie » ; H1a et H2b portent
   sur les deux et le verdict n'est retenu que si le signe est le meme.
   Repli declare : un segment de moins de 10 personnes dans le perimetre rend la permutation
   quasi identique ; la chute est alors NaN et non zero.
2. **Ratios inter et intra** de dispersion, rapportes aux humains de la vague 1 sur les
   memes personnes et items.
3. **Rarete de groupe** : `a44_commun.covariables_rarete` et `groupe_sur_personne`, qui est
   la definition de a31 section 2.3 (lift de rarete de segment divise par lift de rarete de
   personne, mesures sur les fausses raretes contre le temoin aveugle a la personne).
4. **Rappel des raretes stables** : `a42_commun`, partition P_A (stabilite en vague 2),
   seuil de rarete 0,10, exces sur les trois planchers (item, segment, humains vague 2).
   Declare **secondaire et sous puissant** (section 3).
5. **Exactitude par personne**, `a2_commun.exactitude_par_personne`.

## 6. Tests et decision

- Bootstrap **apparie sur les personnes**, 4 000 tirages, memes tirages pour toutes les
  conditions comparees ; IC a 95 pour cent par percentiles ; p de bootstrap bilateral avec
  plancher a 1 sur le nombre de tirages. Un contraste a denominateur vide recoit p = 1
  (convention conservatrice de a29, a31, a34, a42).
- Correction **Holm par famille d'hypotheses**, familles separees : F1 = {H1a x 2
  segmentations, H1b, H1c, H1d} (5 tests) ; F2 = {H2a, H2b x 2 segmentations, H2c, H2d}
  (5 tests) ; F3 = {H3} (1 test). Benjamini Hochberg rapporte a cote, jamais substitue.
- Seuil 0,05 sur le p de Holm.

**Criteres de chute, ecrits avant de voir les chiffres.**

| ce qui tombe | condition de chute |
|---|---|
| **La these de l'etiquette comme fabrique de gabarit** | H1a est **rejetee dans le sens contraire** sous les deux segmentations : ajouter l'etiquette a C3 **augmente** significativement la chute sous permutation. Cela dirait que l'etiquette individualise au lieu de typer, et invalide la lecture de a38, a39, a44 et de MODELE 10.4. |
| **La lecture « v6 contre v8 »** | H2a n'est pas verifiee : retirer l'ideologie de C2 ne fait **pas** tomber le ratio inter sur l'axe ideologie (IC contenant zero, ou signe inverse). Cela dirait que l'analogie entre nos conditions et le couple v6/v8 de Stanford est fausse. |
| **La revendication de nouveaute** | les deux effets, H1 et H2, sont **tous deux nuls** : alors ni l'ajout ni le retrait de l'etiquette ne fait rien a modele, personnes, questions et traces constants, et la phrase « l'etiquette produit la caricature » n'a aucun support experimental dans ce dossier. |
| **Le run lui meme** | masse mediane des lettres sur les 20 appels du smoke test inferieure a 0,90, ou masse minimale inferieure a 0,50, ou plus de 25 pour cent d'appels a modalite absente : le run s'arrete sans ecrire de trace utile. Ou : les prompts C3E ne contiennent pas exactement les 11 lignes demographiques et les reponses attendues (verification hors ligne, section 7). |

**Ce qui ne sera PAS conclu.** Un effet mesure sur un modele de 4 milliards de parametres,
quantifie en 4 bits, sur 150 personnes du GSS et 58 items de six familles, avec les
personnes de C3E possiblement limitees a ~80. Aucune generalisation a d'autres modeles,
d'autres jeux ou d'autres tailles. Aucune conclusion causale sur « ce que fait l'etiquette
dans un pipeline de simulation sociale » : R3 mesure ce que fait **une ligne de texte dans
une invite**, sur ce modele la.

## 7. Verifications hors ligne, avant tout appel

Faites par `analyses/r3_ablation_etiquette.py --verification-seule`, qui n'allume aucun
serveur. Elles doivent toutes passer avant que la file lance le run :

1. l'echantillon retire est identique a `a5-personnes.csv`, 150 personnes, 30 par pli ;
2. 58 items de famille, repartis 10/12/14/10/12 sur les cinq blocs ;
3. le prompt C3E **contient les 11 libelles demographiques** dans l'ordre de a5 et **le
   corps exact de `systeme_c3`** pour la meme personne et le meme bloc ; egalite de chaines,
   pas inspection visuelle ;
4. le prompt C3E **ne contient pas** l'item cible ni aucun item de son bloc ;
5. le prompt C2S **ne contient ni `Political ideology` ni `Political party`**, et ses neuf
   lignes sont exactement celles de `systeme_c2` restreint ;
6. le prompt C2S est plus court que celui de C2 d'exactement les deux lignes retirees ;
7. l'index de reprise relit une trace tronquee sans echouer ;
8. le calcul de la fin dure passe minuit du bon cote (epoch avec le jour) ;
9. le verdict du smoke test, fonction pure importee de `r2_rares_apparie`, rend le bon
   verdict sur des masses synthetiques ;
10. aucun `llama-server` ne tourne au moment ou le run demarre (refus sinon, `pgrep -x`).

## 8. Ce que chaque issue change a MODELE-DU-MONDE 10.4

`MODELE-DU-MONDE.md` 10.4 dit aujourd'hui : « le meme modele, les memes personnes et les
memes questions donnent 7 pour cent du plancher humain avec l'etiquette et 45 pour cent
sans ». a45 a montre que la phrase confond deux facteurs. Les issues possibles :

| issue | ce que 10.4 devient |
|---|---|
| **H1a et H2a verifiees** | 10.4 est **reecrite mais tenue** : « a information de la personne constante, ajouter l'etiquette fait chuter la part du plancher humain de X a Y ; a etiquette constante, retirer l'ideologie fait tomber le ratio inter de Z a W ». Le chiffre « 7 contre 45 » est remplace par les deux effets a un facteur, et la difference entre 6,2 et le produit des deux effets est publiee comme la part imputable au changement d'information. |
| **H1a nulle, H2a verifiee** | 10.4 devient : **l'etiquette n'agit que dans le regime pauvre.** Ajoutee a 119 reponses, elle ne change rien ; seule elle, elle fait tout. C'est une these plus faible et plus interessante : le gabarit de groupe est ce que le modele fait **faute de mieux**, pas ce qu'il prefere. Toutes les phrases « l'etiquette produit la caricature » deviennent « l'etiquette seule produit la caricature ». |
| **H1a verifiee, H2a nulle** | 10.4 est **retournee** : l'etiquette agit en presence de la personne mais pas seule, ce qui contredit l'analogie v6/v8 et demande de rouvrir a38 et a39. |
| **H1a rejetee dans le sens contraire** | 10.4 tombe, et avec elle la lecture de a38 4.4, a39, a44 7.2 et ARBITRAGE point 2. Le rapport devra le dire dans son premier paragraphe. |
| **Les deux nulles** | la revendication de nouveaute numero un du dossier est vide (section 5 de MODELE-DU-MONDE) ; il reste le contraste de conditionnement, qui n'est pas une ablation, et il faut le nommer ainsi partout. |
| **H3 verifiee** | 10.4 gagne une phrase : l'effet est porte par les deux lignes politiques, pas par la demographie en general. |
| **C3E non couverte (moins de 30 personnes)** | rien ne change a 10.4 ; le rapport declare le verrou **ouvert** et donne la commande de reprise. La trace est resumable. |

## 9. Registre du modele

A relire dans la trace elle meme, pas ici : chaque ligne de `data/traces/r3-*.jsonl` porte
`modele`, `quantification`, `gabarit`, `variante_fin` et `version_prompt`. Attendu :
`Qwen3-4B-Instruct-2507`, `Q4_K_M`, `qwen`, `answer`, `r3-p1-qwen4-answer`. Coupure de
connaissances publiee : **aucune** (carte de modele, rapport technique et documentation
muets) [CONFIRME, registre de `r2_rares_apparie.py`].

Version de llama-server : relevee au demarrage par `MoteurA5.demarrer()` et ecrite dans
`data/traces/r3-run.log`.

## 10. Ce que ce plan ne couvre pas

- La passe 2 (ordre des modalites inverse) n'est pas faite pour R3 : les traces C2 et C3
  auxquelles R3 se compare sont des passes 1. Le biais de position n'est donc pas neutralise,
  il est **constant entre les conditions comparees**, ce qui suffit pour un contraste et pas
  pour un niveau.
- Aucune condition n'est evaluee en **tirage** (objection 8 de a45) : R3 reste en argmax
  comme tout le dossier. Les distributions sont dans la trace, un tirage pourra etre
  reconstruit sans nouvel appel.
- R3 ne dit rien du regime severe : son decoupage est celui de C3, cousins presents. Le
  couple etiquette x regime severe reste ouvert.
