# C7-temoin-prompt, resultats : la personne, le prompt ou le segment ?

Calcule par `analyses/c7_temoin_prompt.py`, preenregistre dans
`c7-temoin-prompt-preenregistrement.md`. Deux executions identiques (graine 20260912) :
memes chiffres au centieme pres. 30 paires dirigees a 60 items communs parmi les 7
configurations riches (mêmes paires que `c7-transfert-resultats.md`), segmentation `S_fin`
(bloc d'ideologie x genre x age, 24 segments, tailles 25-192, mediane 82, couverture
2 058/2 058). Detail personne x paire dans `resultats/c7-temoin-prompt.csv` (61 740 lignes,
aucun identifiant, seulement une position interne) ; decomposition agregee dans
`resultats/c7-temoin-prompt-decomposition.csv` ; temoin de population dans
`resultats/c7-temoin-prompt-mode-segment.csv`.

## Decomposition de l'accord (fraction d'items ou les deux jumeaux s'accordent)
IC 95 % par bootstrap sur les personnes, 2 000 tirages, moyenne sur les 30 paires puis sur
les 2 058 personnes. La decomposition est une identite exacte (telescopage) :
`plancher + apport_segment + apport_individuel = accord_vrai`.

| terme | valeur | IC 95 % |
|---|---|---|
| plancher (accord de fond, hors segment) | **46,00 %** | [45,92 ; 46,09] |
| accord meme segment (= permutation intra-segment exacte) | 49,83 % | [49,70 ; 49,98] |
| accord au vrai jumeau | 67,21 % | [66,99 ; 67,43] |
| **apport de segment** (meme-seg − plancher) | **3,83 pts** | [3,75 ; 3,91] |
| **apport individuel** (vrai − meme-seg) | **17,38 pts** | [17,21 ; 17,56] |

Sur l'ecart total entre le plancher et l'accord vrai (21,21 pts), le segment demographique
et ideologique (`S_fin`) n'en explique que 18 % (3,83 pts) ; la personne en explique 82 %
(17,38 pts). Le plancher lui-meme (46,00 %) est substantiel — sur des echelles categorielles
a peu de modalites, deux inconnus s'accordent presque une fois sur deux par construction du
format — mais l'ecart entre inconnus et vrai jumeau est domine par l'individu, pas par le
gabarit ni le segment.

## Temoin de population pure : top-1 par mode de segment (leave-one-out)
Chaque jumeau du bassin est remplace par le code le plus frequent de son segment `S_fin`,
en excluant sa propre reponse (aucune information individuelle). Top-1 moyen sur les
30 paires : **0,07 %** [0,04 ; 0,11], a comparer au hasard du bassin entier (1/2 058 =
0,0486 %) et au **top-1 individuel deja publie sur les memes 30 paires : 36,38 %**
(`c7-transfert-voletA.csv`, non recalcule). Le mode de segment n'apporte donc **aucun**
avantage identifiable au-dessus du hasard pur — moins meme que la prediction preenregistree
(≈1,2 %, soit 1/82, taille mediane du segment) : sur des echelles d'opinion souvent proches
d'un partage 50/50 a l'interieur d'un segment de ~82 personnes, exclure une seule personne du
calcul du mode suffit a faire flotter le profil d'un membre a l'autre, si bien que le
« mode de segment » ne colle a aucun membre en particulier mieux qu'au hasard.

## Verdict sur le critere preenregistre
Aucune des deux conditions destructrices n'est remplie :
- top-1 mode-segment (0,07 %) **tres en dessous** du seuil destructeur (36,38 % / 3 =
  12,13 %) ;
- apport_individuel (17,38 pts) **tres au-dessus** de apport_segment (3,83 pts).

**A2 survit ce temoin.** Le canal inter-jumeaux transporte une information individuelle
mesurable, nettement au-dessus de ce que le prompt/format (plancher) et le segment
demographique-ideologique expliquent a eux seuls.

## Ce que les donnees n'ont pas permis
- Aucun axe de segmentation plus fin que les quatre deja codes par `t1_commun.segmentations`
  (`S_ideo`, `S_parti`, `S_gra`, `S_fin`) n'a ete construit : un axe revenu ou region
  demanderait de retravailler `demographies_brutes`, hors perimetre de ce chantier.
- `S_gra` (genre x ethnicite x age) a ete ecarte pour le mode leave-one-out : des segments
  de taille 1 y rendent le mode indefini pour certaines personnes ; `S_fin` a ete prefere
  car il couvre 100 % des 2 058 personnes avec un minimum de 25.
- Les 12 paires a 19 items communs (impliquant `JSON Persona - GPT4.1-mini`) sont exclues :
  deja pres du plancher dans `c7-transfert-resultats.md` (0,45 % de top-1), et 19 items sont
  trop peu pour un mode de segment lisible ; aucun temoin n'a ete calcule sur ce sous-groupe.

## Phrase pour l'article
« Le canal inter-jumeaux (A2) ne se reduit pas a la ressemblance du gabarit de prompt : sur
60 items communs, l'accord de fond entre inconnus est de 46,0 % [45,9 ; 46,1], le segment
demographique-ideologique n'ajoute que 3,8 points [3,8 ; 3,9], et la personne en ajoute 17,4
points [17,2 ; 17,6] — 82 % de l'ecart au-dessus du plancher. Un temoin de population pure
(mode de segment, sans aucune information individuelle) n'identifie la bonne personne que
0,07 % du temps, contre 36,4 % pour l'attaque reelle : le segment seul ne transporte
pratiquement aucune information d'identification, la difference vient de l'individu. »
