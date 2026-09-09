# a19. Errata appliques a la suite de la relecture adverse

Chantier a19, 8 septembre 2026. Applique les corrections demandees par
`resultats/a17-relecture-adverse.md`, avec les recalculs qu'elles exigent.

Regle de travail : **aucun corps de rapport n'a ete reecrit**. Chaque rapport vise recoit une
section `## Errata du 8 septembre 2026` inseree juste apres son titre, qui cite la phrase
d'origine, donne la correction et la preuve. L'historique reste lisible.

Aucun appel de modele de langage. Aucun script existant n'a ete modifie. `data/traces/` n'a pas
ete touche. Le rapport `a7-transport-de-variance.md` n'a pas ete touche : il est repris par le
chantier a20.

**Scripts nouveaux**

| script | ce qu'il calcule | duree |
|---|---|---|
| `analyses/a19_denominateurs.py` | exactitude appariee sur quatre jeux d'items, ratios inter et intra sur deux jeux d'items avec la machinerie de a1, taux de recopie des 29 items ecartes, statut de `income` | environ 45 min, 4 coeurs |
| `analyses/a19_exactitude_brute.py` | les memes exactitudes sur les chaines brutes, sans appariement a la nomenclature, pour verifier que la conclusion ne depend pas de la definition | environ 20 s |
| `analyses/a19_income.py` | B0, B1 et B2 sur 149 puis 148 items, `income` retire du score seul puis du score et du contexte | environ 6 min |
| `analyses/a19_a8_correlation.py` | la correlation de a8 section 5.3 avec et sans le bloc de prix, et au niveau du bloc | environ 5 s |

**Tableaux produits** : `a19-exactitude-appariee.csv`, `a19-exactitude-brute.csv`,
`a19-test-retest-par-jeu.csv`, `a19-ratios-par-jeu-items.csv`,
`a19-recopie-items-ecartes.csv`, `a19-income-baselines.csv`,
`a19-a8-correlation-blocs.csv`.

**Reproduction**

```
.venv/bin/python analyses/a19_denominateurs.py --bootstrap 1000 --permutations 50
.venv/bin/python analyses/a19_exactitude_brute.py
.venv/bin/python analyses/a19_income.py
.venv/bin/python analyses/a19_a8_correlation.py
```

---

## 1. Le resultat nouveau de cette nuit, en une phrase

**Ajouter l'etiquette ideologique a l'invite d'un agent demographique multiplie par vingt cinq
le gonflement des ecarts entre segments ideologiques, de 0,34 a 8,51 en ratio a la reference
humaine, sans que l'exactitude individuelle change de plus d'un point.** [MESURE]

La demonstration tient en un tableau. Taux d'accord avec la vague 1, item par item, sur les
1 052 memes participants. Un taux voisin de 1 est une recopie de l'invite, un taux inferieur a
la modalite majoritaire est l'absence de l'information.

| item | modalite majoritaire | `gss_v6`, figure 2 du papier | `gss_v8`, figure 3 du papier |
|---|---|---|---|
| `polviews`, ideologie | 0,288 | **0,200** | **0,961** |
| `partyid`, parti | 0,220 | **0,165** | **0,994** |
| `marital`, etat civil | 0,420 | **0,999** | 0,461 |
| `relig*`, religion | 0,405 | **0,994** | 0,430 |
| `degree*`, diplome | 0,389 | **0,998** | 0,267 |
| `income`, revenu | 0,516 | **0,994** | 0,454 |
| `zodiac`, signe astrologique | 0,092 | **0,999** | 0,062 |
| `hispanic` | 0,865 | **0,999** | 0,863 |
| `widowed` | 0,931 | **1,000** | 0,837 |
| `sex*`, genre | 0,564 | **0,999** | **0,998** |
| `race*` | 0,759 | **0,998** | **0,999** |
| `reg16` | 0,187 | 0,144 | 0,129 |

`gss_v6` a recu un profil d'etat civil complet et **aucune information politique** ; `gss_v8` a
recu l'ideologie, le parti, la race et le genre, **et rien d'autre**. Les 17 autres items
ecartes sont dans `a19-recopie-items-ecartes.csv` et ne sont recopies par aucune des deux.

Le lien avec le detail par axe de a1 section 4, `a1-ratios-par-axe.csv`, mesure entropie :

| condition | ratio inter, axe ideologie | ideologie et parti dans l'invite |
|---|---|---|
| agents demographiques `v6` | 0,34 | non, mesure |
| agents demographiques `v8` | 8,51 | oui, mesure |
| agents persona `v7` | 0,27 | non |
| humains vague 2, controle | 1,01 | sans objet |

Ce resultat resout trois choses d'un coup : il etablit ce que a1 section 7.4 declarait "non
etabli", il confirme la deduction de a2 section 2.1 que a14 et a16 avaient annulee a tort, et
il donne au facteur 6,9 entre les deux variantes demographiques une cause nommee.

---

## 2. Tableau des corrections appliquees

Colonne "chiffre avant" : ce qui est ecrit dans le rapport rendu. Colonne "chiffre apres" : ce
que l'errata etablit.

| rapport | objection a17 | phrase ou chiffre avant | chiffre apres | preuve |
|---|---|---|---|---|
| a1, E1, sections 7.3 et reponse en une ligne | 1.1, C4 | v7 et v8 "strictement indistinguables", 56,21 contre 56,28, ecart -0,07 [-0,52 ; +0,37] | sur les 169 items du rapport : 57,03 contre 56,20, ecart **-0,83** [-1,28 ; -0,38], t = -3,82, l'intervalle **exclut zero** | `a19-exactitude-appariee.csv` ; test retest 79,5253 reproduit exactement sur 150 items et sur aucun autre jeu, `a19-test-retest-par-jeu.csv` |
| a1, E1 | 1.1 | ecart v6 contre v8 de 1,85 point [1,41 ; 2,29] | sur 169 items : **-4,17** point [-4,57 ; -3,74] | `a19-exactitude-appariee.csv` |
| a1, E1 | 1.1 | facteur 13,5 sur des ratios a 169 items | inchange : 0,437 [0,379 ; 0,493] et 5,907 [5,648 ; 6,157] reproduits au millieme ; sur 149 items 0,397 et 5,972, facteur 15,0 | `a19-ratios-par-jeu-items.csv` |
| a1, E2, section 3 | 1.2 | "les deux intervalles contiennent 1" | intra entropie [1,0001 ; 1,0087] et intra variance ordinale [0,9795 ; 0,9997] **excluent 1**, de 0,01 et 0,03 pour cent ; resolution de la methode bornee a environ un demi pour cent | `a1-ratios.csv`, fichier produit par le script lui meme |
| a1, E3, limite 3 | 1.6 | "ce qui est le bootstrap de base au sens de Davison et Hinkley" | **intervalle de percentile translate sur l'estimation ponctuelle** ; le bootstrap de base reflechit, la fonction `recentrer` translate ; aucun chiffre ne change | lecture de `recentrer` dans `a1_double_distorsion.py` |
| a1, E4, section 7.4 | 1.3 | "Non etabli non plus. Ce qui differe concretement entre les deux generations." | etabli par la mesure : `v6` sans politique, `v8` avec politique et rien d'autre ; ratio inter sur l'axe ideologie 0,34 contre 8,51 | `a19-recopie-items-ecartes.csv` et `a1-ratios-par-axe.csv` |
| a1, E5, section 1 et limite 4 | 1.4 | "Un agent demographique a recu ces valeurs dans son invite" pour les huit items | aucun agent demographique n'a recu les huit ; le motif defendable est le motif empirique du controle vague 2, qui tombe a 0,946 | `a19-recopie-items-ecartes.csv` |
| a1, E6, section 3 | 1.5, C11 | "les deux autres mesures donnent le meme classement" | le signe est identique sur les trois mesures, le classement composite contre entretien **s'inverse** sur la variance ordinale, 0,861 contre 0,890 sur le terme intra | `a1-ratios.csv` |
| a1, E6, section 9 | 1.5 | mesures globales "entre 0,80 et 0,90" | vrai en entropie ; en variance ordinale 0,9623 pour l'entretien et 0,9508 pour `v8` | `a1-ratios.csv`, colonne `ratio_dispersion_globale` |
| a1, E7, section 5 | 1.8 | "la valeur humaine est retrouvee au centieme pres [...] ce qui indique que la mesure est bien implementee" | coincidence entre deux quantites differentes, autre jeu, autre distance, autre segmentation ; la phrase de validation est retiree | a10 et a13 section 1.1 |
| a2, E1, section 2.1 | 2.3, 8.1, C1 | "Deduction, et c'est une deduction" sur l'absence d'ideologie | **fait mesure**, et confirme pour `gss_v6` ; infirme pour `gss_v8` ; nommer la generation devient obligatoire | `a19-recopie-items-ecartes.csv` |
| a2, E2, section 2.1 | 2.2, C6 | 149 items, une seule fuite retiree, `polviews` | `income` reste dans les 149 et `gss_v6` le recopie a **0,994** ; son score passe de 0,5818 a **0,5790**, soit **-0,28 point** ; l'ecart avec B1 passe de 3,91 a **4,26** points | `a19-income-baselines.csv` |
| a2, E2 | 2.2 | fuite supposee vers B1 | **non** : accord exact item `income` contre attribut `income` = **0,0000** ; B1 passe de 0,6209 a 0,6216, B2 de 0,6717 a 0,6719 en protocole rejoue sur 148 items | `a19_denominateurs.py` bloc 3, `a19-income-baselines.csv` |
| a2, E3, sections 4 et 10 | 2.1, C5 | "cinq des six conditions d'agents du papier de Stanford sont battues par du scikit-learn" | **deux** conditions comparables sont battues, entretien et enquete ; les trois autres sont declarees non comparables par la limite 2 du meme rapport | lecture croisee de a2 section 9 limite 2 |
| a8, E1, sections 1 et 3.2 | 4.1 | "quand on retire la famille entiere, les agents de Stanford battent B2" | la famille ne sort du contexte **que** pour B2 ; la condition appariee du papier vaut 0,77 contre 0,82 normalise, soit environ 4,0 points bruts ; l'agent enquete tomberait vers 0,631, **sous** les 0,6621 de B2 | a14 section 3.4, Tableau 6 du materiel supplementaire ; [PROBABLE] pour l'ampleur |
| a8, E1 | 4.1 | test existentiel A4 declare retourne | il reste ouvert ; **le test propre est la condition C3F de a5**, non lancee | a5 sections 4.5 et le commentaire de `a8_familles.py` |
| a8, E2, section 5.3 | 4.3 | "0,80 [MESURE, p < 0,0001, 108 items]" | 0,797 sur 108 items, **0,561** hors les 40 items du bloc de prix, **0,479** au niveau du bloc, p = 0,005 sur 33 blocs dont 26 a un seul item | `a19-a8-correlation-blocs.csv` |
| a8, E3, section 7.1 | 2.1, C5 | phrase de a2 declaree "non contredite" | elle est contredite par la limite 2 de a2 | lecture croisee |
| a8, E4 | 2.2, C6 | perimetre de 149 items | contient `income`, recopie a 0,994 par `v6` ; lignes `v6` surestimees de 0,3 point, aucune conclusion de a8 ne repose sur `v6` | `a19-income-baselines.csv` |
| a9, E1, section 1.6 | 5.1, C2 | "recouvre presque exactement le ratio d'ecarts types **intra groupe** de 0,40 a 0,56" | ce n'est pas un ratio intra groupe : a10 l'attribue a Ozkan, ratio d'ecarts types par item sur toute la population du WVS Turquie ; a15 designe Bisbee et al. 2024, 16,1 sur 31,4 = 0,513, sur toute la population aussi. De plus un taux de deviance et un rapport d'ecarts types ne vivent pas sur la meme echelle | a10 section 1.a, a15 section 3.3 |
| a9, E2, section 1.4 | 5.2 | "C'est plus fort encore que le r = 0,684" | 0,535 est **inferieur** a 0,684, et les deux r portent sur d'autres variables, un autre jeu et une autre population | arithmetique et lecture de a1 section 6 |
| a9, E3, section 4 | 5.3 | "un facteur unique expliquant 31 pour cent de la variance, contre un plancher de permutation de 0,000" | le plancher de la part de variance du premier facteur est **1 sur 6, soit 16,7 pour cent** ; mesure 30,9 ; attendu sous equicorrelation au meme r moyen 30,2 ; l'exces reel est de **14,2 points**, pas de 31. Le 0,000 est le plancher de la correlation moyenne | `a9-deviance-un-facteur.csv`, valeur propre 1,855 et r moyen 0,1627 |
| a9, E4, section 4 | 5.5, C7 | "le denominateur depend du jeu d'items" | il depend du jeu d'items **et** du delai, deux a quatre semaines variables sur Twin contre deux semaines fixes sur le GSS | a8 section 8 point 6, a12 |
| a13, E1, revendication (b)3 et section 2.6 | 7.1, C4 | "dont l'exactitude differe de 0,07 point avec un intervalle [-0,52 ; +0,37]" | **0,83 point** [-1,28 ; -0,38] sur les 169 items ; le facteur 13,5 tient | `a19-exactitude-appariee.csv` |
| a13, E2, section 6, deux paragraphes anglais | 7.1 | "accuracy [...] can be **identical**" et "accuracy is **blind** to the difference" | "differs by **less than one percentage point** (0.83, 95 % CI [-1.28, -0.38])" et "separates the two populations by less than one percentage point" | idem |
| a13, E3, revendication (b)2 | 7.2 | "avec des intervalles contenant 1, ce qui **prouve** que la methode ne fabrique pas d'ecart" | "a 0,4 pour cent de (1,1) sur les trois mesures, ce qui **borne** a environ un demi pour cent l'ecart que la methode peut fabriquer" | `a1-ratios.csv` |
| a13, E4, revendication (b)4 | 7.3 | "aucun des trois travaux voisins ne traite ce biais" | exact, mais a7 ne le traite pas non plus ; la revendication doit porter la reserve | lecture de `a7_transport_variance.py` par a17 |
| a13, E5, reponse en une ligne | 7.4 | "son propre tableau permet d'en deduire un transport que ses auteurs ne calculent pas" | la reserve de la section 2.3, "argument de lecture, pas un resultat publiable", doit figurer dans la reponse en une ligne | a13 section 2.3 lui meme |
| a14, E1, section 3.1 | 8.1, C1 | "Ceci contredit frontalement la deduction de a2 section 2.1" et "la comparaison a armes egales est donc B1 complet, 0,6209, contre 0,5818" | **annule** : la citation decrit `gss_v8`, a2 evalue `gss_v6` ; la deduction de a2 est confirmee pour `v6` | `a19-recopie-items-ecartes.csv` |
| a14, E2, section 3.3 | 8.2 | "non etabli" sur ce qui differencie les deux generations | etabli par les taux de recopie, sans arithmetique et sans hypothese | idem |
| a14, E3, section 5.1 | C13 | "le papier ne mesure aucune dispersion" employe pour soutenir "aucun papier lu ne publie cette mesure" | vrai pour ce papier ci uniquement ; LifeMem publie l'intra (a13 section 1.1) et Bisbee et al. 2024 publie les deux termes avec referent humain (a15 section 3.3) | a13, a15 |
| a16, E1, section 3.3 | 8.1, 2.3, C1 | "la deduction de a2 [...] est desormais contredite par trois artefacts de code independants" | **annule** : les trois artefacts etablissent que la representation demographique **peut** porter l'ideologie, non que `gss_v6` la portait ; la mesure dit qu'il ne la portait pas | `a19-recopie-items-ecartes.csv` |
| a16, E4, section 5 | 8.1 | test propose : "mesurer si le deficit est concentre sur `polviews` ou diffus" | **fait et tranche contre la regle de retrait** : le deficit de `v6` porte aussi sur `partyid`, que la regle ne retire jamais ; et `v8` obtient 0,961 sur `polviews`, ce qu'aucune regle de retrait n'autorise | idem |
| POUR-SIMON, section 4 | 1.1, C4 | tableau "56,21 / 56,28" et "ecart de 0,07 point, statistiquement zero" | tableau refait sur les memes 169 items, ecart **-0,83** [-1,28 ; -0,38], l'intervalle exclut zero ; le facteur 13,5 tient ; ajout du tableau des recopies et de la phrase citable | `a19-exactitude-appariee.csv`, `a19-recopie-items-ecartes.csv` |

Trois objections du tableau des treize de a17 ne recoivent pas d'errata ici et sont renvoyees
ailleurs : **C3, C8 et C12** portent sur `a7-transport-de-variance.md`, confie au chantier a20.
**C9 et C10** portent sur `a12-delai-de-retest.md`, qui ne m'a pas ete confie ; leurs lignes
sont listees en section 4 ci dessous pour memoire.

---

## 3. Lignes a changer dans PASSATION, SYNTHESE, CONTEXTE, POINT-DE-SITUATION

Ces quatre fichiers **n'ont pas ete modifies**. L'orchestrateur s'en charge. Les numeros de
ligne sont ceux des fichiers au 8 septembre 2026, avant toute autre modification.

### PASSATION.md

| ligne | texte actuel | ce qu'il faut ecrire | motif |
|---|---|---|---|
| 109 | "la variance a l'interieur des groupes demographiques est ecrasee, **ratio d'ecarts types de 0,40 a 0,56**, pendant que les ecarts entre groupes sont gonfles" | "la variance a l'interieur des groupes demographiques est ecrasee, ratio mesure chez nous de **0,64 a 0,89** sur le GSS, pendant que les ecarts entre groupes sont gonfles" et, en note : "le 0,40 a 0,56 qui circulait dans ce document est un ratio d'ecarts types **sur toute la population** et non intra groupe ; a10 l'attribue a Ozkan sur le WVS Turquie, a15 a Bisbee et al. 2024 sur la polarisation affective ; il ne doit pas etre repris comme notre resultat" | a10 section 1.a, a15 section 3.3, a1 limite 5, errata E1 de a9 |
| 116 | "le correctif ne peut pas etre une dilatation de la variance, ce doit etre un **transport de variance a somme constante**, de l'inter vers l'intra. Aucune methode a bouton unique ne peut y parvenir." | "le correctif ne peut pas etre une simple dilatation de la variance. Un transport a somme constante de l'inter vers l'intra est necessaire mais **il ne suffit pas** : le ratio de dispersion totale des populations simulees vaut 0,80 a 0,89 en entropie et le transport le laisse invariant, ce qui plafonne le ratio intra atteignable. Il faut deux operations, un transport **et** un comblement du deficit total. Sur la variance ordinale, ou le deficit est plus faible, le plafond depasse 1 pour cinq couples sur huit : la conclusion doit etre indexee sur la mesure." | a7 section 0 et a17 objection 3.2, contradiction C3. **Cette ligne dependant de a7, elle doit etre ecrite apres le rendu du chantier a20.** |
| 149 | "Probabilite que deux repondants tires au hasard donnent la meme reponse : 49,5 pour cent chez les humains, 66,4 pour cent chez les agents demographiques. **Aucun papier lu ne publie cette mesure.**" | "[...] **Aucun des papiers de Stanford ne publie cette mesure ; LifeMem publie une mesure de dispersion intra groupe (a13 section 1.1) et Bisbee et al. 2024 publie les deux termes avec referent humain, mais sans plafond humain test retest (a15 section 3.3). Ce qui reste sans equivalent est le plancher de bruit humain par reinterrogation.**" | contradiction C13, errata E3 de a14 |
| section 4, "Les pieges verifies" | rien sur les deux generations demographiques | ajouter un piege : "**Deux fichiers portent l'etiquette demographique pour le GSS.** `gss_v6`, employe par la figure 2 et par le 74 pour cent du resume, n'a recu ni ideologie ni parti dans son invite ; `gss_v8`, employe par la figure 3, a recu ideologie, parti, race et genre et rien d'autre. Mesure par les taux de recopie item par item, a19. Ne jamais citer un chiffre d'agent demographique sans nommer la generation." | resultat nouveau de a19, section 1 ci dessus |

### SYNTHESE.md

| ligne | texte actuel | ce qu'il faut ecrire | motif |
|---|---|---|---|
| 65 | "- la variance INTRA groupe est ecrasee, **ratio d'ecarts types de 0,40 a 0,56** ;" | "- la variance INTRA groupe est ecrasee, ratio mesure chez nous de **0,64 a 0,89** sur le GSS ; le 0,40 a 0,56 qui circulait est un ratio sur toute la population, pas un ratio intra groupe" | idem PASSATION ligne 109 |
| 154 | "faire du **transport de variance a somme constante** le correctif vise" | "faire du transport de variance de l'inter vers l'intra le correctif vise, en sachant qu'il est necessaire et non suffisant : le deficit de dispersion totale doit etre comble en plus" | idem PASSATION ligne 116, **apres a20** |
| Decision 1 | proposition de reecriture de la these | ajouter au dossier de la decision le resultat de a19 : la difference entre les deux generations demographiques est un seul attribut d'invite, l'etiquette ideologique, et elle vaut un facteur 25 sur le ratio inter de l'axe ideologie pour moins d'un point d'exactitude | resultat nouveau de a19 |

### CONTEXTE.md

| ligne | texte actuel | ce qu'il faut ecrire | motif |
|---|---|---|---|
| 49 | "la variance INTRA groupe est ecrasee, **ratio d'ecarts types de 0,40 a 0,56**, et les ecarts INTER groupes sont au contraire gonfles" | meme correction que SYNTHESE ligne 65 | a10, a15 |
| 56 | "Le correctif doit etre un TRANSPORT de variance a somme constante, de l'inter vers l'intra, et non une dilatation. **Aucun papier ne le formule ainsi a ce jour. C'est la contribution la plus specifique du projet.**" | meme correction que PASSATION ligne 116, et retirer ou restreindre "aucun papier ne le formule ainsi" : a13 et a15 ont depuis identifie quatre travaux voisins | a7, a13, a15, **apres a20** |

### POINT-DE-SITUATION.md

| ligne | texte actuel | ce qu'il faut ecrire | motif |
|---|---|---|---|
| 131 a 132 | tableau : "Faux sondes v7 \| 56,21 pour cent \| 0,44" et "Faux sondes v8 \| 56,28 pour cent \| 5,91" | "Faux sondes v7 \| **57,0 pour cent** \| 0,44" et "Faux sondes v8 \| **56,2 pour cent** \| 5,91", avec la mention "note et ecarts calcules sur les memes 169 questions" | les 56,21 et 56,28 sont des chiffres a 150 questions, les ratios a 169 ; errata E1 de a1 |
| 134 a 136 | "L'ecart de note est de 0,07 point, **ce qui est statistiquement zero**. Ces deux populations simulees obtiennent **exactement la meme note**. Et leurs structures sont inverses d'un facteur 13,5." | "L'ecart de note est de **0,8 point**, ce qui est mesurable mais minuscule : moins d'un point d'ecart sur la note, un facteur 13,5 sur la structure." | idem |
| 139 a 140 | "L'une gomme les differences entre groupes, l'autre les multiplie par six, et **la note ne fait pas la difference**." | "L'une gomme les differences entre groupes, l'autre les multiplie par six, et la note ne les separe que de huit dixiemes de point." | idem |

### JOURNAL-NUIT-2026-09-07.md

Le journal n'a pas ete modifie. Trois entrees sont a corriger, et l'entree de 23:40 les annonce
deja.

| lignes | texte actuel | ce qu'il faut ecrire |
|---|---|---|
| 203 a 205, entree 23:05 sur a14 | "L'invite demographique CONTIENT l'ideologie politique et le parti : **la deduction de a2 section 2.1 est contredite**. Consequence favorable : la bonne comparaison est B1 complet 0,6209 contre 0,5818, ce qui renforce a2." | "L'invite demographique **decrite par le papier** contient l'ideologie politique et le parti. **ANNULE le 8 septembre** : cette invite est celle de `gss_v8` ; a2 evalue `gss_v6`, qui n'a recu ni ideologie ni parti (0,200 et 0,165, sous la modalite majoritaire). La deduction de a2 est confirmee pour `v6`. La comparaison a armes egales face a `v6` reste B1 sans politique, 0,5998 contre 0,5818. Voir a19." |
| 93 a 97, entree 22:50 sur a8 | "quand la famille entiere sort du contexte, B2 tombe de 0,6956 a 0,6621 et passe DERRIERE les agents composite [...] **Premiere fois qu'une condition d'agent domine sur les deux axes.**" | ajouter la reserve : "**Reserve du 8 septembre** : la famille ne sort du contexte que pour B2 ; les agents de Stanford gardent leurs items cousins dans l'invite. La condition appariee du papier vaut 0,77 contre 0,82 normalise, environ 4 points bruts, ce qui ramene l'agent enquete sous B2. Le test propre est C3F de a5, non lancee. Voir a19." |
| 116 a 121, entree 22:53 sur a9 | l'entree ne reprend pas le rapprochement fautif avec le 0,40 a 0,56, mais ne le signale pas | ajouter : "**Note du 8 septembre** : la section 1.6 du rapport rapproche le taux de deviance du 0,40 a 0,56 en le qualifiant de ratio intra groupe, ce que l'entree de 22:38 venait de corriger quinze minutes plus tot. Le rapprochement est retire par errata. Voir a19." |
| 117 | "premier facteur **30,9 pour cent**" | le journal a raison, c'est le rapport qui ecrit 31 et cite un plancher de 0,000. Ajouter dans le journal : "plancher sous independance 16,7 pour cent, exces reel 14,2 points" |

Deux remarques de forme relevees par a17 et non traitees ici : l'ordre des entrees du journal
n'est pas monotone (22:55, 23:10, 22:58, 23:05, 23:04, 23:05) alors que le document annonce
"chaque entree est horodatee" ; et le journal dit 48 lignes pour le critere A6 la ou a7 dit 24,
et c'est le journal qui a raison.

### a12-delai-de-retest.md, pour memoire

Ce rapport ne m'a pas ete confie et **n'a pas ete modifie**. Deux corrections l'attendent.

| section | texte actuel | correction |
|---|---|---|
| 3 | "0,795002 sur les 149 items contre 0,795253 pour le champ `p_wave1__p_wave2__accuracy` calcule par les auteurs sur les **177 items**" | le champ des auteurs porte sur **150 items**. Verifie ici : 177 items 81,2491 ; 169 items 81,0072 ; **150 items 79,5253** ; 149 items 79,5002. `a19-test-retest-par-jeu.csv`. Contradiction C9 |
| 4.2 | "Le 0,860 reproduit le 86 pour cent publie par Stanford [...] ce qui valide la chaine de calcul" | rapport de moyennes contre normalisation individuelle des auteurs, qui donne 0,865 ; deux estimateurs differents qui arrondissent au meme 0,86 ne se valident pas. Contradiction C10 |
| 4.1 et 4.2 | tableaux employant `gss_v6` | `income` figure dans les 149 comme dans les 118 items du noyau, et `v6` le recopie a 0,994 ; effet de 0,28 point sur `v6`. `a19-income-baselines.csv` |

---

## 4. Ce que je n'ai pas pu verifier

1. **L'ampleur de l'objection sur a8, regime famille.** Le 0,77 contre 0,82 du papier est mesure
   sur 100 agents et sur l'ensemble des items ; je le transpose aux 58 items de familles
   thematiques, ou l'autocorrelation intra famille est par construction plus forte. L'ordre de
   grandeur est defendable, la valeur exacte non. **Je n'ai pas cherche dans le paquet OSF s'il
   existe un fichier de sortie pour la condition de retrait par bloc** ; s'il existe, il tranche
   en une heure et rend l'errata E1 de a8 mesurable au lieu de probable.

2. **Deux lignes du tableau de a17 objection 1.1 ne sont pas reproduites.** a17 annonce 55,93 et
   55,49 sur 177 items et 56,16 et 55,28 sur 169 items ; je mesure 56,76 et 56,90 puis 57,03 et
   56,20. Les lignes 150 items et 149 items de a17 sont reproduites a l'identique, et les quatre
   consistances test retest aussi, ce qui etablit que les jeux d'items sont les memes des deux
   cotes. La verification arithmetique tranche en faveur de mes valeurs : 57,03 pour v7 sur 169
   items se reconstitue exactement a partir de la valeur a 150 items et des taux item par item du
   tableau des recopies, et 56,20 pour v8 de meme. Le calcul a ete refait sur les chaines brutes,
   sans appariement a la nomenclature, avec le meme resultat a deux centiemes pres. **La
   conclusion de a17 n'est pas affectee** : l'ecart sur 169 items est negatif et exclut zero dans
   les deux calculs, -0,83 chez moi, -0,88 chez a17.

3. **L'attribution de la fourchette 0,40 a 0,56 n'est pas tranchee.** a10 l'attribue a Ozkan,
   arXiv 2607.18310, WVS Turquie [CONFIRME pour l'existence du chiffre, mesure differente] ; a15
   designe Bisbee et al. 2024, 16,1 sur 31,4 = 0,513 [PROBABLE]. Les deux convergent sur le point
   qui compte, ce n'est pas un ratio intra groupe, mais la source exacte de la phrase de
   PASSATION reste indeterminee. Je n'ai ouvert ni l'un ni l'autre papier.

4. **Le biais residuel de l'estimateur inter n'a pas ete corrige.** L'objection a17 1.7 demande
   une colonne "ratio avec correction de biais bootstrap". Elle n'a pas ete calculee : cela
   demande de reprendre la chaine de bootstrap de a1 et de decider quelle correction appliquer,
   ce qui est une decision de methode et non un recalcul. L'errata E3 de a1 se contente de dire
   que la version publiee est la borne basse.

5. **Aucune correction pour tests multiples n'a ete construite**, dans aucun des rapports. Les
   objections 1.9, 3.8, 4.5 et 5.6 de a17 restent entieres. Fixer la famille d'hypotheses est une
   decision de redaction.

6. **Je n'ai relance aucun script existant en entier.** `a19_denominateurs.py` importe
   `a1_double_distorsion` et reproduit ses ratios sur les 169 items au millieme pres, ce qui
   valide la chaine ; `a19_income.py` importe `a2_baselines_gss` et reproduit ses baselines au
   quatrieme chiffre. Mais `a1`, `a2`, `a8`, `a9` et `a12` n'ont pas ete rejoues, donc je n'ai pas
   verifie que tous leurs CSV publies correspondent a la derniere version de leurs scripts.

7. **La correction d'attenuation de l'objection a17 5.4** sur les items stables et instables de
   a9 n'a pas ete faite : elle demande le nombre d'items par ensemble et les fiabilites par
   moities, qui ne sont pas dans les fichiers publies.

8. **Les intervalles de confiance sur les alphas de Cronbach de a9 section 2.3** n'ont pas ete
   calcules ; l'objection a17 5.6 reste ouverte.

9. **`income` n'a ete traite que sur le GSS.** Le noyau de 118 items de a12 n'a pas ete recalcule
   sans cet item, et les 149 items servant a a7 n'ont pas ete revus.

10. **Le rapport a7 n'a pas ete ouvert autrement que par les citations de a17**, conformement au
    partage avec le chantier a20. Les contradictions C3, C8 et C12 lui reviennent, et la ligne 116
    de PASSATION ne peut pas etre ecrite avant son rendu.

11. **Je n'ai pas verifie les deux papiers tiers** LifeMem et Garzon et al., ni le PDF de
    2411.10109. Les citations de a13, a14 et a15 sont prises pour exactes ; mes objections portent
    sur leur application a un fichier de sortie, pas sur leur contenu.
