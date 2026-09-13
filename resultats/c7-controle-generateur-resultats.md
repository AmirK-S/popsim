# C7, controle generateur banal : resultats (13 septembre 2026)

statut: courant
mandat: Un generateur synthetique banal, sans IA, ajuste sur les memes humains, fuit-il autant qu'un jumeau LLM ?
agent: Opus 5, Anthropic
ecriture: analyses/c7_controle_generateur.py, resultats/c7-controle-generateur-preenregistrement.md, resultats/c7-controle-generateur-resultats.md, resultats/c7-controle-generateur.csv
lecture_seule: tout le reste
interdits: appel payant sans GO, reseau, commit sur master, arriere-plan
cout_reel_usd: 0

Preenregistre dans `c7-controle-generateur-preenregistrement.md`, ecrit avant la premiere
ligne de code et avant tout calcul. Calcule par `analyses/c7_controle_generateur.py`, donnees
`c7-controle-generateur.csv`. Attaque non reimplementee : `c7_reidentification.rangs_attaque`,
`c7_monde_ouvert.marges_deux_regimes` et `c7_monde_ouvert.roc_et_taux` importees telles quelles.
Aucun appel de modele de langage, aucun reseau, aucune depense, aucune bibliotheque installee.
Aucun identifiant, aucune identite, aucun appariement individuel n'est imprime ni ecrit.

## 0. Ce que ce controle tranche

L'article dit que les jumeaux LLM laissent fuiter l'identite des repondants. Rien dans le
protocole ne demontrait que le LLM y etait pour quelque chose. Si un generateur synthetique
banal, ajuste sur les memes humains et soumis a la meme attaque sur le meme bassin, atteignait
le meme taux, le resultat redecouvrait la fuite des donnees synthetiques (Narayanan-Shmatikov
2008) au lieu de dire quoi que ce soit sur les LLM.

**Verification du bassin, avant tout le reste** : le top-1 recalcule ici pour le jumeau LLM est
de 20,74 % (Twin) et 65,55 % (Park et al.), contre 20,7 % et 65,51 % deja publies dans
`c7-resultats.md` et `c7-attaquant-fort-resultats.md`. Le bassin, les items et l'attaque sont
donc bien les memes, a la troisieme decimale pres. Le piege qui a deja coute deux erreurs a ce
projet est ferme.

## 1. Les quatre generateurs classiques, bassin strictement identique

Twin-2K-500 : 2 058 attaques / 2 058 candidats / 60 items (hasard 0,049 %).
Park et al. (GSS) : 1 052 / 1 052 / 177 items (hasard 0,095 %).

| Jeu | Generateur | exactitude | top-1 [IC 95 %] | top-10 | AUC ouvert | TPR@1 % |
|---|---|---|---|---|---|---|
| Twin | G0 marginales independantes | 0,431 | **0,041 %** [0,012;0,080] | 0,52 % | 0,0002 | 0,00 % |
| Twin | G1 marginales par segment | 0,444 | **0,154 %** [0,089;0,226] | 1,03 % | 0,0008 | 0,01 % |
| Twin | G2 Chow-Liu global | 0,417 | **0,049 %** [0,016;0,089] | 0,53 % | 0,0002 | 0,00 % |
| Twin | G3 Chow-Liu par segment | 0,323 | **0,091 %** [0,043;0,148] | 0,67 % | 0,0006 | 0,00 % |
| Twin | jumeau LLM (JSON Persona GPT4.1) | 0,590 | **20,74 %** [18,99;22,47] | 42,6 % | 0,149 | 3,04 % |
| Twin | plafond humain (retest) | 0,745 | 81,40 % [79,66;83,07] | 91,6 % | 0,766 | 54,49 % |
| GSS | G0 marginales independantes | 0,495 | **0,129 %** [0,046;0,232] | 1,15 % | 0,0007 | 0,00 % |
| GSS | G1 marginales par segment | 0,546 | **2,266 %** [1,844;2,711] | 12,8 % | 0,0124 | 0,05 % |
| GSS | G2 Chow-Liu global | 0,446 | **0,133 %** [0,046;0,232] | 0,94 % | 0,0007 | 0,00 % |
| GSS | G3 Chow-Liu par segment | 0,234 | **0,456 %** [0,278;0,650] | 2,78 % | 0,0026 | 0,02 % |
| GSS | agent LLM composite (Park et al.) | 0,712 | **65,55 %** [62,66;68,31] | 90,2 % | 0,553 | 20,39 % |
| GSS | plafond humain (retest) | 0,812 | 96,75 % [95,67;97,74] | 98,4 % | 0,959 | 90,69 % |

Le meilleur generateur classique non memorisant est, sur les deux jeux, **G1, les marginales
conditionnees au segment demographique** -- exactement le generateur qu'utiliserait un
praticien. Il plafonne a 0,154 % (Twin) et 2,27 % (GSS), soit **135 fois** et **29 fois** sous
le jumeau LLM, IC a 95 % disjoints, sur un bassin strictement identique. Critere preenregistre
de non-specificite (`M >= 0,5 x L`, seuils 10,37 % et 32,78 %) : **tres loin d'etre atteint**.
En monde ouvert l'ecart est plus brutal encore : aucun generateur classique ne depasse 0,055 %
de TPR a FPR = 1 %, contre 3,04 % et 20,39 % pour les jumeaux LLM ; leur AUC est de l'ordre de
10^-3, c'est-a-dire indiscernable de l'absence totale de signal.

**Controle de fidelite prealable** (`c7_controle_interpretabilite`, applique avant toute
interpretation, baseline recalculee sur le bassin reellement attaque) : G0, G1, G2 et G3
**echouent tous les quatre** -- ils ne transportent aucune information individuelle demontrable
(top-1 de 0,00 a 0,20 % contre une baseline Demographics Only de 2,15 % sur le meme bassin). Le
jumeau LLM **passe** (20,74 % contre 2,15 %). C'est l'issue attendue au preenregistrement, et
elle confirme que ces generateurs ne sont pas des jumeaux rates mais bien des generateurs de
population.

## 2. L'echelle de memorisation G4, et la ou se situe le jumeau LLM

G4(eps) recopie mot pour mot le vrai vecteur de la personne, puis remplace chaque item avec
probabilite eps par un tirage dans la marginale. eps = 0 est la memorisation totale, eps = 1
redonne G0. Vingt et un points mesures, `table = echelle_memorisation` du CSV.

| eps | Twin exactitude | Twin top-1 | GSS exactitude | GSS top-1 |
|---|---|---|---|---|
| 0,00 | 1,000 | 100,0 % | 1,000 | 100,0 % |
| 0,30 | 0,829 | 99,9 % | 0,848 | 100,0 % |
| 0,50 | 0,715 | 85,6 % | 0,748 | 100,0 % |
| 0,60 | 0,656 | 55,6 % | 0,696 | 98,9 % |
| 0,70 | 0,603 | 23,8 % | 0,647 | 81,3 % |
| 0,80 | 0,545 | 6,2 % | 0,595 | 33,0 % |
| 0,90 | 0,487 | 0,8 % | 0,546 | 4,3 % |
| 1,00 | 0,431 | 0,04 % | 0,495 | 0,19 % |

Deux lectures croisees, preenregistrees, interpolees **dans** la grille mesuree (aucune
extrapolation) :

| Jeu | eps* qui reproduit la FUITE du jumeau | eps* qui reproduit son EXACTITUDE | ecart | lecture preenregistree |
|---|---|---|---|---|
| Twin | **0,714** | **0,720** | **0,006** | **se comporte comme un copieur** |
| GSS | **0,735** | **0,570** | **0,165** | **generalise** (fuit moins qu'un copieur de meme exactitude) |

**Twin, le resultat central.** Un generateur sans aucun modele, qui recopie litteralement
29 % des reponses d'une vraie personne (17 items sur 60) et tire les 43 autres au hasard dans
la marginale de la population, atteint **exactement** l'exactitude du jumeau LLM (0,590) **et
exactement** sa re-identification (19,5 % predite contre 20,74 % mesuree, rapport 1,06). Sur ce
jeu, la fuite du jumeau LLM est, au point pres, celle qu'implique mecaniquement son niveau
d'exactitude individuelle : ni exces de memorisation, ni deficit.

**GSS, resultat different et il faut le dire.** L'agent composite a une exactitude de 0,712 ;
un copieur de meme exactitude (eps = 0,570) re-identifie **99,5 %** des personnes, contre
65,6 % pour l'agent. L'agent fuit donc nettement **moins** qu'un copieur equivalent en
exactitude : sur 177 items a trois modalites, il y a de la place pour se tromper « comme un
humain » plutot que « comme un tirage », et l'agent l'occupe.

**Ma prediction preenregistree (`eps*_fuite > eps*_exactitude`, le jumeau generalise) est donc
REFUTEE sur Twin** (ecart 0,006, tolerance +-0,10 : le verdict tombe dans la case « copieur »,
pas dans celle que j'avais annoncee) **et confirmee sur GSS**. Je la rapporte telle quelle.

## 3. Verdict

1. **La fuite n'est pas la fuite generique des donnees synthetiques.** Marginales, marginales
   par cellule demographique, arbre de Chow-Liu global, arbre de Chow-Liu par cellule : aucun
   generateur classique ajuste sur les memes humains ne depasse 0,16 % (Twin) et 2,3 % (GSS),
   contre 20,7 % et 65,6 %. Le critere preenregistre de non-specificite est manque d'un facteur
   67 et 14. Le titre de l'article tient, et il est renforce.
2. **Mais le mecanisme n'est PAS une memorisation propre au LLM.** L'echelle G4 le montre : sur
   Twin, la fuite du jumeau est exactement celle d'un copieur banal de meme exactitude. Ce qui
   est propre au LLM n'est pas de memoriser, c'est **d'atteindre ce niveau d'exactitude
   individuelle** -- niveau qu'aucun generateur classique n'atteint sans recopier de vraies
   reponses. La fuite en decoule mecaniquement. Ecrire l'inverse serait surinterpreter.
3. **Consequence de redaction** : la phrase de secours du preenregistrement (section 7) n'a pas
   lieu d'etre publiee -- le verdict ne tombe pas contre nous. Mais la phrase du point 2 doit
   etre publiee, car elle corrige par avance une lecture que le lecteur fera spontanement.

**Phrase exacte que l'article devrait ecrire :**

> Aucun generateur synthetique classique ajuste sur les memes repondants -- marginales
> independantes, marginales par cellule demographique, arbre de Chow-Liu global ou par cellule
> -- ne depasse 0,15 % (Twin-2K-500) et 2,3 % (Park et al.) de re-identification au rang 1 sur
> un bassin strictement identique, contre 20,7 % et 65,6 % pour les jumeaux produits par un
> modele de langage : ce que nous mesurons n'est pas la fuite generique des donnees
> synthetiques. Ce n'est pas non plus une memorisation propre aux modeles de langage. Un
> generateur sans aucun modele, qui recopie mot pour mot une fraction des reponses d'une vraie
> personne et tire le reste dans la marginale de la population, reproduit la meme
> re-identification des qu'il reproduit la meme exactitude par personne (Twin-2K-500 :
> fraction copiee de 29 %, exactitude 0,590 et re-identification 19,5 %, contre 0,590 et
> 20,7 % pour le jumeau). Ce qui est propre au modele de langage est d'atteindre ce niveau
> d'exactitude individuelle sans avoir recopie quoi que ce soit ; la fuite en decoule.

## 4. Ecarts au preenregistrement, nommes

Deux, tous deux dans le sens qui ne nous arrange pas ou sans effet sur le verdict :

1. **Segmentation GSS.** Le preenregistrement annoncait genre x race x age (42 cellules, repli
   global sous 10 personnes). Mesure faite avant tout calcul de fuite : cette grille laissait
   plus de la moitie des personnes en repli global (taille mediane de cellule 14), ce qui aurait
   **affaibli artificiellement** G1 et G3, donc arrange notre these. Remplacee par une hierarchie
   genre x race x age x education -> genre x race x age -> genre x age -> age, chaque personne
   generee dans la cellule la plus fine atteignant le seuil, parametres estimes sur tous les
   membres de cette cellule. C'est l'ecart qui donne au comparateur sa meilleure chance.
2. **Tirages d'ex aequo.** 5 au lieu des 20 de `rangs_attaque`, pour tenir la contrainte « tout
   en avant-plan » (321 s + 99 s au total). Verification : le top-1 du jumeau LLM recalcule
   ainsi (20,74 %, 65,55 %) reproduit a 0,05 point pres les valeurs a 20 tirages deja publiees
   (20,7 %, 65,51 %). Sans effet sur le verdict.

## 5. Limites, toutes declarees

- **Les generateurs classiques ne sont pas apparies en exactitude** (0,23-0,55 contre 0,59-0,71
  pour les jumeaux). C'est une propriete du probleme, pas un defaut de protocole : aucun d'eux
  ne peut atteindre cette exactitude sans voir les reponses cibles d'autres personnes
  (`c7_synth_ajuste.py`) ou de la personne elle-meme (G4). C'est precisement pour cela que G4
  existe, et c'est G4 qui repond a la question de l'appariement.
- **Attaquant naif partout.** Le chiffre de 60,17 % cite en tete de l'article est celui de
  l'attaquant fort (A-LLR, `c7-attaquant-fort-resultats.md`) sur GSS ; ce controle emploie
  l'attaquant naif de Hamming pour **tous** les generateurs, jumeau LLM compris (20,39 % en
  monde ouvert pour l'agent composite). Le rapport entre generateurs, seul objet de ce
  controle, est mesure a attaque constante. Un attaquant plus fort ne changerait pas le verdict
  dans le sens qui nous arrange : les generateurs classiques n'ont aucun signal individuel a
  extraire (AUC ~ 10^-3), un meilleur extracteur ne peut donc pas leur en trouver.
- **G3 (Chow-Liu par cellule) a une exactitude effondree** (0,32 et 0,23) : ajuster un arbre a
  60-177 items sur une cellule de 30 a 100 personnes surajuste. Il reste rapporte tel quel ;
  ce n'est pas lui qui porte le verdict, c'est G1.
- **Reductions declarees** (budget local, aucun appel paye) : 5 tirages de generation par
  generateur classique, 2 pour les 21 points de la courbe G4, 5 tirages de depart d'ex aequo au
  lieu de 20 dans `rangs_attaque` (meme valeur que `c7_monde_ouvert.py`), grille eps au pas de
  0,05. IC par bootstrap de personnes, 2 000 reechantillonnages. Graine 20260913.
- **Segmentation** : Twin `S_gra` (35 cellules >= 10 personnes) ; GSS hierarchie
  genre x race x age x education avec replis successifs, pour donner au generateur classique
  sa meilleure chance plutot qu'un repli global penalisant.
- `synthpop`, `copulas`, `sdv`, `ctgan` sont absents du venv : **rien n'a ete installe**, et le
  Chow-Liu a ete code ici (information mutuelle par paires, arbre couvrant maximal,
  echantillonnage ancestral, une centaine de lignes).
