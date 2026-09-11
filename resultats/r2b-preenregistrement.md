# R2b, preenregistrement : porter la comparaison appariee de 150 a 180 personnes

**Ecrit le 9 septembre 2026 a 13:19:38 CEST, AVANT le moindre appel de modele de langage
de cette extension.** Aucun `llama-server` ne tourne au moment ou ce fichier est ecrit
(`pgrep -x llama-server` vide, verifie a 13:19:38). Ce fichier n'est plus modifie ensuite :
le rapport `resultats/r2b-resultats.md` le reproduit et rapporte les mesures a cote, quel
qu'en soit le signe. En cas de divergence, cette page fait foi contre le rapport.

**Ce plan n'a pas ete depose hors machine, et R2 non plus.** `DECISIONS-CONSOLIDEES-2026-09-09.md`
nomme ce trou en toutes lettres : *« aucune page de plan deposee hors machine »*. Le depot OSF
du 9 septembre a 12:22 (https://osf.io/3r6zg/) ne couvre que R5 et R6. R2 et cette extension
R2b se decrivent donc, ici et dans le rapport, comme **« plan ecrit avant le run, horodate sur
machine, non depose »**, jamais comme « preenregistre » au sens d'un registre public. Le nom
de fichier dit « preenregistrement » par continuite de nomenclature avec R1 a R6, et cette
phrase est la pour que le nom ne trompe personne.

---

## 0. Pourquoi cette extension existe, et qui l'a decidee

`resultats/r2-resultats.md` section 3.2 publie un calcul d'effectif ecrit apres le run et
avant toute decision de le depenser. Il dit trois choses [MESURE et ESTIMATION,
`resultats/r2b-puissance.csv`] :

| contraste de F1 | effet a 150 personnes | ecart type | personnes exigees sous Holm |
|---|---|---|---|
| H1a, plancher de segment | plus 0,0315 | 0,0347 | environ **1 097** |
| H1b, `PMM k=10 famille retiree` | **moins 0,0943** | 0,0417 | **176** |
| H1b, `IM m=10 mode` | moins 0,0094 | 0,0397 | environ 15 914 |

Un seul contraste est a portee de machine : celui contre `PMM k=10 famille retiree`. R2
l'ecrit ainsi, et c'est la phrase que cette extension va tester : *« Si le dossier depense
cette nuit la, l'issue probable n'est pas "le jumeau bat PMM", c'est "PMM bat le jumeau,
decidablement". »*

`DECISIONS-CONSOLIDEES-2026-09-09.md` ligne 88, question 9 de la liste soumise a Amir :
*« Les 176 personnes de R2 (deux heures, issue probablement defavorable) : oui ou non. »*
Defaut de la question : **oui**. L'orchestrateur a pris la decision par defaut le
9 septembre a 13:18, et c'est a ce titre que ce run est lance. La question du rapporteur a
laquelle il doit repondre est exactement : **« ne bat pas PMM » ou « est battu par PMM » ?**

**Ce que R2 etablit deja, et qu'il ne faut pas confondre avec ce que R2b cherche.** R2 a
etabli, sous Holm dans une famille de sept, que le jumeau **ne bat pas** PMM : le contraste
est negatif, moins 0,0943, l'intervalle non ajuste est entierement negatif
[moins 0,1729 ; moins 0,0099], le p brut vaut 0,0400 et le p de Holm vaut 0,2400, donc il ne
decide pas. R2b cherche si la proposition symetrique, **« PMM bat le jumeau »**, est
decidable sous la meme correction. Ce n'est pas la meme phrase, et R2 a explicitement refuse
de l'ecrire faute de puissance.

---

## 1. Combien de personnes de plus, et lesquelles

**Trente personnes de plus, six par pli, portant la comparaison de 150 a 180.** Le seuil de
la section 3.2 de R2 est 176 ; 176 n'est pas divisible par 5 et briserait la stratification
sur les plis, qui n'est pas cosmetique : les baselines B1 et B2 sont entrainees pli par pli
et un echantillon desequilibre melangerait des tailles d'entrainement (motif de
`a5_agents_locaux_gss.echantillon`). Six par pli donne 180, soit **quatre personnes de marge**
au dessus du seuil exige. Le nombre est arrete ici, avant tout appel, et il ne sera pas
augmente en cours de route en fonction de ce que les chiffres montrent.

**Regle de selection, mecanique et deja employee dans le dossier.** Les trente personnes sont
tirees par `a21_extension_c2.echantillon_hors(ids, plis, par_pli=6, exclus_index, graine=20260908)`,
c'est a dire :

1. la meme stratification sur les cinq plis du decoupage de `a2_baselines_gss.grille`,
   graine 20260903, que `a5_agents_locaux_gss.echantillon` ;
2. le vivier de chaque pli **ampute des 150 personnes deja jouees** (les index de
   `data/traces/a5-personnes.csv`), donc un tirage dans le complementaire, ce qui rend
   l'intersection vide par construction et non par verification ;
3. **graine fixe 20260908**, celle que `a21_extension_c2` emploie deja pour le second
   echantillon de C2, distincte de la graine du decoupage (20260903) et de celle du premier
   echantillon (20260907).

**Aucune personne n'est choisie a la main, et aucune n'est choisie sur une propriete de ses
reponses.** En particulier, les personnes ne sont pas selectionnees parce qu'elles portent des
cellules rares stables : R2 mesure que 98 personnes sur 150 n'en portent aucune, et
selectionner sur ce critere serait choisir l'echantillon sur la variable de resultat. Le
nombre de cellules rares stables apportees par les trente nouvelles personnes est donc
**inconnu au moment ou cette page est ecrite** et sera rapporte tel quel.

**Les trente pid, ecrits ici pour que le tirage soit verifiable et fige** (issus du code
ci dessus, execute a 13:20 sans aucun appel de modele) :

| pli | pid |
|---|---|
| 0 | participant_0184, participant_0290, participant_0681, participant_0813, participant_0909, participant_1002 |
| 1 | participant_0114, participant_0187, participant_0261, participant_0582, participant_0720, participant_0944 |
| 2 | participant_0248, participant_0378, participant_0518, participant_0525, participant_0562, participant_0711 |
| 3 | participant_0088, participant_0161, participant_0173, participant_0259, participant_0545, participant_0886 |
| 4 | participant_0222, participant_0377, participant_0458, participant_0527, participant_0610, participant_0791 |

Intersection avec les 150 de `a5-personnes.csv` : **vide**, verifiee sur les pid et sur les
index. Ces trente pid sont ecrits dans `data/traces/r2b-personnes-ext.csv` avant le premier
appel, comme `a5-personnes.csv` l'a ete pour R2.

---

## 2. La ou les conditions rejouees

| | |
|---|---|
| **Condition jouee** | **C3F seule** : contexte egal aux 149 items **moins toute la famille** de l'item cible, aucune demographie, aucune etiquette. C'est la condition du contraste H1b, le regime severe, celui ou les six methodes statistiques perdent aussi la famille entiere |
| Modele | **gpt-oss-20b**, GGUF MXFP4, **gabarit harmony** obligatoire (a3 section 4.5, r2 section 0), variante de fin de prompt `answer`, exactement celle que R2 a retenue apres sonde |
| Items | les **58** items des six familles de `FAMILLES` dans `a2_baselines_gss.py`, perimetre inchange |
| Appels | 30 personnes x 58 items = **1 740 appels**, six prefixes de persona par personne |
| Adversaire principal | **`PMM k=10 famille retiree`**, importee de `a35_familles.imputer_par_famille` par `a41_commun.construire_severe`, jamais recopiee |
| Adversaires secondaires | les cinq autres methodes du regime severe de a41, pour que la famille F1 garde ses sept tests et que Holm reste la meme correction |

**C3 n'est pas rejouee, et c'est un choix ecrit d'avance.** C3 (cousins conserves) s'est
arretee a 105 personnes sur 150 dans R2, faute de temps. L'etendre aux trente nouvelles
personnes donnerait une condition a 135 personnes sur 180, c'est a dire une couverture encore
plus batarde, et n'aiderait aucun contraste de F1. Le mandat porte sur H1b. **C3 reste donc a
105 personnes et rien de ce qui la concerne dans R2 n'est modifie ni recalcule autrement que
par le simple fait que les 105 sont un sous ensemble des 180.**

---

## 3. L'hypothese, et le pari ecrit

### L'hypothese

**H1b-PMM, la seule qui motive la depense.** Sur les 180 personnes et les 58 items, en regime
severe des deux cotes, la difference de rappel des raretes stables
`C3F gpt-oss-20b` **moins** `PMM k=10 famille retiree` est **strictement negative et decidable
sous Holm dans la famille primaire de sept tests**.

Les six autres tests de F1 (H1a contre le plancher de segment, et les cinq autres H1b) sont
recalcules a l'identique sur 180 personnes, avec la meme correction de Holm sur la meme
famille, parce qu'on ne peut pas retirer un test d'une famille apres avoir vu son p sans
casser la correction. F2, F3 et F4 sont recalculees aussi, aux memes seuils, et publiees ; **on
n'en attend rien de neuf** : leurs contrastes etaient deja decides a Holm 0,0015 a 0,0405 sur
150 personnes, et trente personnes de plus ne peuvent que les resserrer.

### Le pari, et il coute

**Pari ecrit du dossier : PMM reste devant, et l'ajout de trente personnes rend
« battu par PMM » decidable.** Formellement : la difference reste negative, son point estime
reste dans la bande [moins 0,13 ; moins 0,05], et son p de Holm passe sous 0,05.
[HYPOTHESE]

**Ce pari coute, et il faut dire ce qu'il coute.** C'est un pari **contre** la these des
jumeaux numeriques, qui est la these fondatrice du projet. Le gagner, c'est ecrire noir sur
blanc que sur la derniere case ou le jumeau de langage avait encore un avantage revendique,
il n'est pas seulement « non superieur » a une imputation statistique de 1975, il lui est
**inferieur de facon decidable**. Il n'y aura alors plus aucune quantite du dossier ou un
modele de langage de 20 milliards de parametres batte une methode tabulaire sur une
comparaison appariee, et la phrase de vente du projet devient entierement defensive. Le pari
est ecrit ici pour que, s'il est gagne, personne ne puisse dire qu'on l'a formule apres coup
comme une prudence ; et pour que, s'il est perdu, la perte compte.

**Trois issues, et ce que chacune autorise a ecrire.**

1. **Le pari est gagne** (difference negative, Holm sous 0,05). L'enonce autorise devient :
   *« sur les memes 180 personnes et les memes cellules, la famille thematique entiere retiree
   des deux cotes, l'appariement sur moyenne predite retrouve plus de gens rares reels qu'un
   jumeau de langage de 20 milliards de parametres, et l'ecart est decidable »*. La phrase de
   R2, « le jumeau ne bat pas PMM », est remplacee par « PMM bat le jumeau ». Aucune autre
   phrase de R2 ne change.
2. **Le pari est perdu par indecision** (difference toujours negative, Holm au dessus de 0,05).
   L'enonce de R2 tient inchange, « le jumeau ne bat pas PMM », et R2b devient une mesure de
   la robustesse de cette indecision. Il faudra alors publier que 180 personnes ne suffisent
   pas la ou l'estimation en annoncait 176, et dire pourquoi : l'estimation supposait l'effet
   constant et l'ecart type en 1 sur racine de n, ce qui n'est pas verifie.
3. **Le pari est perdu par renversement** (la difference devient positive ou proche de zero).
   Ce serait un fait nouveau et il serait rapporte comme tel, en tete du rapport, avec la
   mention explicite que l'echantillon a ete etendu par une regle mecanique et non choisi.
   Il faudrait alors reexaminer si les 150 premieres personnes etaient defavorables par
   hasard, et R2 devrait recevoir un erratum de lecture, sans etre reecrit.

### Predictions accessoires, ecrites d'avance et scorees dans le rapport

- **(a)** H1a reste indecidable, p de Holm au dessus de 0,05. Motif : R2 estime qu'il
  faudrait environ 1 100 personnes. [HYPOTHESE]
- **(b)** le rang du jumeau dans l'ordre du rappel des raretes stables ne bouge pas : il
  reste **quatrieme sur sept**, derriere PMM, E2 tirage et IM mode. [HYPOTHESE]
- **(c)** les sept contrastes de F2, les six de F3 et les six de F4 restent tous decidables
  et tous defavorables. [HYPOTHESE]
- **(d)** le nombre de cellules rares stables passe de 106 a une valeur comprise entre
  **120 et 140** sur 180 personnes. Motif : 106 cellules pour 150 personnes fait 0,71 par
  personne, et trente personnes de plus en apporteraient une vingtaine, plus l'effet du
  seuil de rarete recalcule sur un perimetre plus large. [HYPOTHESE]
- **(e)** le nombre de personnes ne portant **aucune** cellule rare stable reste au dessus
  de 60 pour cent de l'echantillon. Motif : 98 sur 150 dans R2, soit 65,3 pour cent.
  [HYPOTHESE]

---

## 4. Le test

**Identique a R2, sans une seule modification, et c'est la condition pour que les 150
anciennes personnes et les 30 nouvelles se melangent legitimement.**

| | |
|---|---|
| Evaluateur | `analyses/r2_evaluer.py`, **le meme fichier, non modifie**, appele par un enveloppeur `analyses/r2b_evaluer.py` qui ne fait que lui designer la population de 180 et la trace unifiee |
| Cellules jugees | cellules minoritaires reelles au seuil de **10 pour cent** que la personne redonne a l'identique en vague 2, partition P_A de `a42_commun.classes_stabilite` |
| Definition de rarete | **sur le perimetre**, c'est a dire le seuil applique aux 180 personnes ; la definition sur population (1 052) est publiee a cote comme sensibilite, sans correction, exactement comme dans R2 |
| Plancher | tirage dans la marginale du segment ideologie x genre x age sans la personne, `a34_commun.frequence_segment`, 98 cases, calcule sur les 1 052 humains et jamais sur le perimetre |
| Adversaires | les six methodes du regime severe, importees de `a41_commun.construire_severe`, restreintes aux **memes 180 personnes** et aux **memes 58 items** |
| Statistique | p de bootstrap **apparie sur les personnes**, memes **4 000** tirages pour toutes les methodes, graine `a41_commun.GRAINE_A41`, plancher du p a 1 sur 4 000, contraste a denominateur vide a p = 1 |
| Correction | **Holm par famille**, sur les memes quatre familles que R2 : F1 sept tests, F2 sept tests, F3 six tests corriges plus H3b hors correction, F4 six tests. Benjamini Hochberg rapporte a cote |
| Permutations | 200, comme R2, pour H4c descriptif |

**Les trois ecarts a la page de plan que R2 a declares sont conserves tels quels**, pour que
les deux rapports restent comparables : F4 compte six tests et non huit (le regime severe n'a
que trois methodes a tirage) ; H3b est calcule sans correction ; F1 et F2 sont declarees
diriges et testees avec un p bilateral, ce qui est le sens conservateur. **Aucun de ces trois
points n'est corrige ici**, parce que les corriger changerait la barre de Holm entre R2 et
R2b et rendrait la comparaison avant/apres illisible.

**Deux precisions sur ce que « 180 personnes » veut dire pour les quantites qui bougent.**

1. La **definition de rarete sur le perimetre** est recalculee sur 180 personnes, donc
   l'ensemble des cellules jugees n'est pas le sur ensemble exact des 106 cellules de R2 :
   une modalite a 9,8 pour cent sur 150 peut passer a 10,3 pour cent sur 180 et sortir. C'est
   la definition declaree de R2 et elle est conservee ; l'ampleur du glissement sera mesuree
   et publiee (nombre de cellules entrantes et sortantes).
2. Les **planchers de population** (segment, item, humains vague 2) ne bougent pas : ils sont
   calcules une fois sur les 1 052 humains de la vague 1, regle de a34 reprise par a42.

**Ce qui n'est pas rejoue et ne le sera pas** : la passe 2 en ordre inverse des modalites (le
biais de position reste non controle, comme dans R2, et il est le meme pour toutes les
conditions) ; les six conditions d'agents de Stanford (interdiction 4 de a41 section 7) ; la
condition C3 ; la trace `C3F Qwen3-4B`, qui reste a 60 personnes et dont les contrastes
croises resteront donc sur 60 personnes communes.

---

## 5. La regle d'arret, ecrite d'avance

Le run s'arrete proprement, ferme sa trace, ecrit son resume, arrete son serveur et le
rapport se fait sur ce qui est fait, des que **l'une** de ces conditions est vraie :

1. **Trois heures** de run ecoulees depuis le demarrage du serveur. Fin dure calculee au
   demarrage et inscrite dans le journal. Au debit mesure de R2, 1 932 appels par heure, les
   1 740 appels demandent **0,90 heure** : la marge est de plus de trois pour un.
2. **Le swap depasse 10 Go.** `sysctl vm.swapusage` est lu toutes les 60 secondes par une
   sonde separee ecrivant dans `data/traces/r2b-memoire.csv` ; au dessus de 10 240 Mio
   utilises, le fichier d'arret est pose. **Etat de depart, mesure a 13:19 avant tout
   lancement : 6 672 Mio utilises sur 8 192 Mio de swap total**, machine deja chargee. Le
   seuil de 10 Go est donc a 3,3 Go au dessus du point de depart, et il peut etre atteint.
   Motif du garde fou : dans la nuit du 7 au 8 septembre, gpt-oss-20b a huit slots a mis la
   machine a **14 Go** de swap.
3. **Le fichier `data/traces/STOP` existe.** Convention de `analyses/README.md` : la boucle le
   relit entre deux appels, ecrit `ARRET DEMANDE`, ferme sa trace, ecrit son resume et sort
   avec le code 0. `r2_rares_apparie.py` **ne lit pas** ce fichier, c'est un manque connu et
   c'est l'une des raisons pour lesquelles R2b passe par un script nouveau ; le script de
   R2b le lit.
4. **Un `llama-server` tourne deja** au moment du lancement : le run ne demarre pas, il
   attend en boucle et **ne tue jamais** le serveur d'autrui.

**Configuration serveur, fixee d'avance** : `-np 4` (et non 8), `-c 8192` par slot, cache KV
q8_0, port libre choisi a partir de 8200, un seul serveur, arret du serveur dans un `finally`.
Le passage de 8 a 4 slots est la consequence directe de l'incident memoire du 7 au 8
septembre ; il divise par deux le KV alloue.

**Marqueur de fin.** Le run ecrit `RUN TERMINE` dans `data/traces/r2b-run.log`, et **jamais**
dans un journal d'essai : le mode `--verification-seule` et le mode `--essai` ecrivent dans
`r2b-verification.log` et `r2b-essai.log`, qui ne contiennent pas ce marqueur.

**En cas d'arret avant la fin**, le rapport publie la couverture reelle en tete de chaque
tableau et **ne conclut pas sur H1b** si le total des personnes completes est inferieur a
**176**, qui est le seuil de la section 3.2 de R2. C'est le plancher de lisibilite de cette
extension, et il est fixe ici, avant de savoir combien de personnes le run couvrira.

---

## 6. Ce que cette extension ne fera pas

- **Elle ne rouvre pas H1a.** R2 estime a environ 1 100 personnes l'effectif necessaire ;
  180 n'en approche pas. H1a est recalcule parce qu'il appartient a la famille F1 et qu'on ne
  retire pas un test d'une famille apres coup, pas parce qu'on en attend une decision.
- **Elle ne change aucun fichier existant.** Ni `resultats/r2-resultats.md`, ni
  `resultats/r2-preenregistrement.md`, ni `MODELE-DU-MONDE.md`, ni les CSV `r2-*-def.csv`, ni
  les scripts `r2_rares_apparie.py` et `r2_evaluer.py`, ni les traces `r2-C3F-gptoss.jsonl` et
  `r2-C3-gptoss.jsonl`. Tout ce que R2b ecrit porte le prefixe `r2b-`. Ce que R2b change **en
  texte** a R2 et a `MODELE-DU-MONDE.md` section 12.2 est dit dans le rapport, en toutes
  lettres, sans qu'aucun de ces fichiers soit modifie.
- **Elle ne generalise pas aux 1 052.** 180 personnes restent un sous echantillon stratifie
  sur les cinq plis.
- **Elle ne mesure pas la contamination.** La coupure de gpt-oss-20b est publiee, juin 2024,
  jamais verifiee (a3 section 2).
- **Elle ne sort rien de la machine.** Aucun appel distant, aucun depot. La trace ne contient
  pas la vraie reponse de la personne : l'evaluateur la relit dans `data/`.

---

## 7. Sorties attendues

| fichier | contenu |
|---|---|
| `data/traces/r2b-personnes-ext.csv` | les 30 nouvelles personnes, ecrit **avant** le premier appel |
| `data/traces/r2b-C3F-gptoss-ext.jsonl` | la trace des 1 740 appels, meme format que a5 et R2 |
| `data/traces/r2b-run.log` | le journal du run, avec `RUN TERMINE` a la fin |
| `data/traces/r2b-memoire.csv` | swap et charge, une ligne par minute |
| `data/traces/r2b-resume-gptoss.json` | resume de fin de run |
| `resultats/r2b-tableau-180.csv` et les autres `r2b-*-180.csv` | les mesures et contrastes sur 180 personnes |
| `resultats/r2b-resultats.md` | le rapport |

---

*Fin du preenregistrement. Horodatage : 9 septembre 2026, 13:19:38 CEST. Ecrit avant le
premier appel de modele de langage de R2b, aucun `llama-server` en cours a cet instant, page
non deposee hors machine.*
