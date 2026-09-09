# a2 : les baselines sans modele de langage

## Errata du 8 septembre 2026

Corrections apportees a la suite de la relecture adverse `a17-relecture-adverse.md`. Le corps
du rapport n'est pas reecrit, il reste lisible tel qu'il a ete rendu le 3 septembre. Chaque
point cite la phrase d'origine, donne la correction et la preuve. Recalculs :
`analyses/a19_denominateurs.py` et `analyses/a19_income.py`, tableaux
`resultats/a19-recopie-items-ecartes.csv` et `resultats/a19-income-baselines.csv`. Aucun
script existant n'a ete modifie, memes graines, memes plis, aucun appel de modele.

### E1. Section 2.1 : la deduction sur l'ideologie politique est CONFIRMEE pour `gss_v6` et INFIRMEE pour `gss_v8`. Il faut nommer la generation. Objection a17 2.3 et 8.1, contradiction C1.

**Phrase d'origine.** "L'agent demographique n'a probablement pas recu l'orientation politique.
Fait mesure : sur le seul item `polviews`, l'agent demographique de l'archive obtient 0,1996,
soit moins que la modalite majoritaire (0,2880) [...] Deduction, et c'est une deduction et non
un fait source : sa persona ne contenait pas l'orientation politique."

**Cette deduction a ete declaree fausse deux fois, par a14 section 3.1 puis par a16
section 3.3. Les deux corrections sont annulees.** La deduction est confirmee, et elle cesse
d'etre une deduction : elle devient un fait mesure. La cause de la confusion est que le mot
"agent demographique" designe deux fichiers differents dans le meme paquet de replication.

**Preuve, taux d'accord item par item avec la vague 1 sur les items ecartes.** [MESURE,
`analyses/a19_denominateurs.py`, tableau complet dans `resultats/a19-recopie-items-ecartes.csv`]

| item | modalite majoritaire | `gss_v6`, ce que a2 evalue | `gss_v8` | retest humain |
|---|---|---|---|---|
| `polviews` | 0,288 | **0,200** | **0,961** | 0,833 |
| `partyid` | 0,220 | **0,165** | **0,994** | 0,820 |
| `marital` | 0,420 | **0,999** | 0,461 | 0,953 |
| `relig*` | 0,405 | **0,994** | 0,430 | 0,887 |
| `degree*` | 0,389 | **0,998** | 0,267 | 0,913 |
| `income` | 0,516 | **0,994** | 0,454 | 0,634 |
| `zodiac` | 0,092 | **0,999** | 0,062 | 0,975 |
| `hispanic` | 0,865 | **0,999** | 0,863 | 0,974 |
| `martype*` | 0,496 | **0,990** | 0,606 | 0,873 |
| `widowed` | 0,931 | **1,000** | 0,837 | 0,985 |
| `sex*` | 0,564 | **0,999** | **0,998** | 0,988 |
| `race*` | 0,759 | **0,998** | **0,999** | 0,979 |
| `educ*` | 0,943 | 0,998 | 0,939 | 0,956 |
| `reg16` | 0,187 | 0,144 | 0,129 | 0,785 |

Un taux voisin de 1 est une recopie, un taux inferieur a la modalite majoritaire est l'absence
de l'information dans l'invite. `gss_v6` recopie l'etat civil, la religion, le diplome, le
revenu, la date de naissance par le zodiaque, l'origine hispanique, la race et le genre, et il
est **sous la modalite majoritaire** sur l'ideologie et sur le parti. `gss_v8` recopie
l'ideologie, le parti, la race et le genre, et rien d'autre.

**Ce que cela etablit.** Le papier decrit l'invite de `gss_v8` : "Ideologically, I describe
myself as conservative. Politically, I am a strong Republican. Racially, I am white. I am male.
In terms of age, I am 50 years old." Cette invite correspond point pour point aux quatre
recopies de `v8`. Le fichier que a2 evalue sous l'etiquette "agents demographiques" est
`gss_v6_summary.csv`, celui de la figure 2 du papier, qui est une autre generation, a profil
d'etat civil et sans politique.

**La reconciliation proposee par a14 est refutee par les donnees.** a14 suppose que la regle
"la question predite est retiree de l'entree" retire l'ideologie de l'invite au moment ou l'on
predit `polviews`. Si cette regle s'appliquait au descripteur demographique, `gss_v8` ne
pourrait pas obtenir 0,961 sur `polviews` ni 0,994 sur `partyid` sur les memes 1 052
participants. Elle ne s'y applique donc pas, et elle n'explique pas le 0,200 de `gss_v6`.
[MESURE]

**Le raisonnement de a16 porte sur la bonne structure de donnees et sur le mauvais fichier.**
Les trois artefacts qu'il cite, la classe `Scratch`, les 3 505 `scratch.json` de la banque
publique et les colonnes de `demographic_summary.csv`, etablissent que la representation
demographique de Stanford **peut** porter l'ideologie et le parti. Ils n'etablissent pas que
`gss_v6` les portait, et la mesure dit qu'il ne les portait pas.

**Phrase de remplacement pour la section 2.1.** "Fait mesure, et non deduction : le fichier
`gss_v6_summary.csv`, celui que la figure 2 du papier emploie comme condition demographique et
celui que nous evaluons ici, obtient 0,200 sur `polviews` et 0,165 sur `partyid`, sous la
modalite majoritaire de ces deux items, tandis que `gss_v8_summary.csv`, celui de la figure 3,
obtient 0,961 et 0,994. L'invite demographique decrite par le papier, qui contient l'ideologie
et le parti, correspond a `gss_v8` et non a `gss_v6`. La comparaison a armes egales pour `v6`
est donc bien B1 privee des deux attributs politiques, 0,5998 contre 0,5818 ; celle pour `v8`
serait B1 complet, 0,6209 contre 0,5591. Tout chiffre publie sur un agent demographique doit
nommer la generation."

**Consequence sur la valeur a citer.** La variante de B1 sans politique, 0,5998, garde son
statut de comparaison de reference face a `v6` et ne doit pas etre requalifiee en borne basse
comme a14 et a16 le recommandaient. La statistique gagne encore, l'ecart reste de 1,8 point.

### E2. Section 2.1 : une seconde fuite subsiste dans les 149 items, `income`. Objection a17 2.2, contradiction C6.

**Phrase d'origine.** "Fuite exacte sur un item. L'item GSS `polviews` est identique caractere
pour caractere a l'attribut demographique `political_ideology` [...] Il est retire. La cible
compte donc 149 items et non 150."

**Correction.** `polviews` n'etait pas le seul item a examiner. `income` reste dans les 149
items alors que a1 l'ecarte de ses 169, et il est **recopie a 99,4 pour cent par `gss_v6`**,
contre 63,4 pour cent pour le retest humain et 51,6 pour cent pour la modalite majoritaire.
C'est une recopie, du meme type que celle de `polviews` par `v8`. [MESURE]

**La fuite est du cote de l'agent, pas de la baseline.** L'attribut `income` de
`demographic_summary.csv` existe et il est bien donne a B1, mais il emploie un decoupage
different de l'item GSS : l'accord exact entre l'item et l'attribut est de **0,0000** sur les
1 052 participants, contre 1,0000 pour `polviews` et `political_ideology`. B1 n'en tire donc
aucun item gratuit. [MESURE, `analyses/a19_denominateurs.py` bloc 3]

**Effet chiffre, protocole de a2 inchange, score restreint aux 148 items.** [MESURE,
`resultats/a19-income-baselines.csv`]

| methode | 149 items, chiffre publie | 148 items, sans `income` | ecart |
|---|---|---|---|
| retest humain | 0,7950 | 0,7961 | +0,11 pt |
| B2 argmax | 0,6717 | 0,6728 | +0,11 pt |
| B1 argmax | 0,6209 | 0,6216 | +0,07 pt |
| B0 mode | 0,5934 | 0,5939 | +0,05 pt |
| agents composite | 0,6839 | 0,6857 | +0,18 pt |
| agents entretien (v3) | 0,6565 | 0,6581 | +0,16 pt |
| agents enquete | 0,6510 | 0,6533 | +0,23 pt |
| **agents demographiques `v6`** | **0,5818** | **0,5790** | **-0,28 pt** |
| agents `v7` | 0,5640 | 0,5650 | +0,10 pt |
| agents `v8` | 0,5591 | 0,5599 | +0,08 pt |

`gss_v6` est la seule ligne du tableau qui **baisse** quand on retire `income` : toutes les
autres montent, parce que `income` est un item difficile. C'est la signature d'une recopie.

**Effet chiffre, protocole entierement rejoue sur 148 items**, `income` retire de la cible
**et** du contexte de B2, memes graines, memes cinq plis, memes cinq blocs :

| methode | 149 items | 148 items rejoue | ecart |
|---|---|---|---|
| B2 argmax | 0,6717 | 0,6719 | +0,02 pt |
| B1 argmax | 0,6209 | 0,6216 | +0,07 pt |
| B0 mode | 0,5934 | 0,5939 | +0,05 pt |

B2 perd environ 0,09 point a etre privee de `income` dans son contexte, ce qui annule presque
exactement le gain de denominateur. Aucune conclusion de a2 ne bouge. [MESURE]

**Ce que la correction change dans le texte.** L'ecart entre B1 argmax et l'agent
demographique `v6` passe de 3,91 a **4,26 points**, et non de 3,9 a une valeur plus faible.
La note a publier est : "les 149 items contiennent `income`, que la condition `gss_v6` recopie
a 99,4 pour cent, ce qui gonfle son score de 0,28 point ; corrige, l'ecart avec B1 est de 4,26
points et non de 3,91." La liste `FUITE_DEMOGRAPHIQUE` de `a2_baselines_gss.py` devrait
contenir `income` dans toute reprise future ; elle n'a pas ete modifiee ici, pour que les
chiffres du 3 septembre restent reproductibles.

### E3. Sections 4 et 10 : "cinq des six conditions battues" compte trois comparaisons que le meme rapport declare non comparables. Objection a17 2.1, contradiction C5.

**Phrase d'origine, section 4 point 2 et section 10.** "B2 bat les agents entretien et enquete.
Elle perd contre l'agent composite de 1,2 point seulement. Autrement dit, **cinq des six
conditions d'agents du papier de Stanford sont battues par du scikit-learn**."

**Phrase d'origine, section 9 limite 2.** "B2 dispose de beaucoup d'information sur la personne :
environ 119 items de contexte sur le GSS. C'est comparable a ce que recoit un agent enquete,
pas a un agent demographique. Le dire autrement serait malhonnete. La comparaison B2 contre
agents demographiques n'a pas de sens ; celle contre agents enquete et entretien en a un."

**Correction.** Les cinq conditions battues sont `v3` entretien, enquete, `v6`, `v7` et `v8`.
Trois des cinq, `v6`, `v7` et `v8`, sont exactement celles que la limite 2 declare non
comparables a B2. La phrase la plus citable du rapport repose donc a 60 pour cent sur une
comparaison que le rapport lui meme invalide dix pages plus loin, et a8 section 7.1 la reprend
en la declarant "non contredite". [VERIFIE par lecture croisee]

**Phrase de remplacement.** "B2 bat les deux conditions d'agents nourries au meme type
d'information que la baseline, entretien et enquete, et perd de 1,2 point contre l'agent
composite. Les trois conditions pauvres, `v6`, `v7` et `v8`, sont egalement en dessous de B2,
mais cette comparaison n'a pas de sens et ne doit pas etre comptee : B2 dispose de 119 items de
contexte sur la personne, elles n'en ont aucun. La comparaison qui les concerne est celle de la
section 4 point 1, contre B1 sur demographies, et contre B0 mode."

Le fait le plus desagreable du rapport, point 3 de la section 4, n'est pas affecte : la
modalite majoritaire B0, qui n'utilise aucune information sur l'individu, obtient 0,5934, soit
davantage que trois conditions d'agents sur six. C'est cette phrase la qu'il faut mettre en
avant, elle n'a pas de probleme d'appariement d'information.

### E4. Ce que ces errata ne changent pas

Le tableau de la section 4, la courbe de croisement, le regime des questions jamais posees, le
couple exactitude et diversite et l'ensemble des resultats Twin ne sont pas touches. a8
section 7.1 a rejoue les chiffres du GSS a l'identique. Le retrait de `polviews` reste
entierement justifie, l'identite caractere pour caractere entre l'item et l'attribut etant un
fait mesure sur les 1 052 participants.

---

Rapport du 3 septembre 2026. Chantier 2 de la passation, moitie non LLM du test existentiel.
Aucun appel de modele n'a ete fait pour produire ces chiffres.

Scripts : `analyses/a2_commun.py`, `analyses/a2_baselines_gss.py`,
`analyses/a2_baselines_twin.py`, `analyses/a2_telecharger_twin.py`, `analyses/a2_figures.py`.
Resultats bruts : `resultats/a2_gss_resultats.json`, `resultats/a2_twin_resultats.json`.
Rejouable en trois commandes, environ quatre minutes en tout.

```
python3 analyses/a2_telecharger_twin.py
python3 analyses/a2_baselines_gss.py && python3 analyses/a2_baselines_twin.py
python3 analyses/a2_figures.py
```

---

## 1. Ce qu'il faut retenir

**La menace annoncee dans la passation est confirmee, et elle est pire que prevu.** Sur le
GSS, la regression logistique sur les seules demographies atteint 0,6209, ce qui reproduit
presque exactement le 0,622 de la litterature. Elle bat l'agent demographique de Stanford,
0,5818, et elle bat aussi ses agents dits "persona", 0,5640 et 0,5591. Confiance : haute,
mesure sur les donnees d'origine.

**Mais l'adversaire reel n'est pas la regression, c'est le plus proche voisin.** B2 atteint
0,6717 sur le GSS, soit 84,5 pour cent du plancher humain. Elle depasse l'agent entretien
(0,6565) et l'agent enquete (0,6510), c'est a dire deux des trois conditions du papier de
Stanford. Seul l'agent composite tient encore, a 0,6839, et l'ecart est de 1,2 point.
Confiance : haute.

**Le resultat qui sauve le projet est ailleurs.** Sur Twin-2K-500, la hierarchie s'inverse :
GPT-4.1-mini avec persona complet obtient 0,5530 la ou notre meilleure baseline plafonne a
0,5301. Le regime ou le modele de langage gagne existe donc, et il est identifiable. Ce n'est
pas le regime demographique, ou la statistique gagne sur les deux jeux. C'est le regime ou la
question posee n'a pas de correlat statistique dans les donnees dont on dispose. Confiance :
moyenne, un seul modele et une seule famille de questions le montrent.

**Le compromis exactitude contre diversite est net et mesurable.** Toute baseline qui
maximise l'exactitude le fait en detruisant la dispersion. B0 en modalite majoritaire obtient
0,5934 sur le GSS avec 3,3 pour cent de la diversite humaine. La meme baseline en tirage
marginal conserve 99,9 pour cent de la diversite et tombe a 0,4918. Aucune baseline non LLM
ne tient les deux bouts. Les agents de Stanford, eux, tiennent mieux les deux : l'agent
composite fait 0,6839 avec 89,6 pour cent de diversite conservee. C'est, a ce stade, le seul
avantage clair et reproductible des modeles de langage dans nos mesures. Confiance : haute.

---

## 2. Les donnees

### 2.1 GSS, archive OSF t6g7k

`figure2/data/new_analysis_summaries/gss_filtered/preparation/`, 1 052 participants,
177 items, reponses en clair, **aucune cellule manquante**. `p_wave1_summary.csv` et
`p_wave2_summary.csv` sont les memes humains a deux semaines d'ecart.

Les demographies existent et elles sont riches. `figure3/data/demographic_summary.csv` donne
11 attributs pour les 1 052 participants :

| attribut | modalites | renseigne |
|---|---|---|
| age | 7 tranches | 100 % |
| census_division | 10 | 100 % |
| political_ideology | 7 | 100 % |
| political_party | 8 | 100 % |
| education | 5 | 100 % |
| race | 3 | 100 % |
| ethnicity | 20 | 99,3 % |
| gender | 2 | 100 % |
| income | 11 tranches | 82,9 % |
| neighborhood | 3 | 82,9 % |
| sexual_orientation | 6 | 82,7 % |

**Elles ne sont pas trop pauvres, au contraire.** Onze attributs dont l'orientation politique
et le parti, c'est un conditionnement plus riche que celui de la plupart des papiers du champ,
qui s'en tiennent au bloc de recensement. Les trois attributs incomplets sont conserves avec
une modalite explicite "non renseigne" plutot que de supprimer 17 pour cent des participants.

Deux points de vigilance trouves en verifiant, et pas avant :

**Fuite exacte sur un item.** L'item GSS `polviews` est **identique caractere pour caractere**
a l'attribut demographique `political_ideology` sur les 1 052 participants, accord 1,0000. Le
garder dans la cible donnerait a B1 un item gratuit a 100 pour cent. Il est retire. La cible
compte donc 149 items et non 150, et tous les scores d'agents cites ici ont ete **recalcules
sur ces memes 149 items**, pour que l'ecart ne vienne pas du denominateur. Effet du retrait
sur B1 : environ +0,25 point si on le remettait, negligeable mais reel.

**L'agent demographique n'a probablement pas recu l'orientation politique.** Fait mesure : sur
le seul item `polviews`, l'agent demographique de l'archive obtient 0,1996, soit **moins que
la modalite majoritaire** (0,2880), alors que la reponse lui aurait ete donnee mot pour mot si
l'attribut figurait dans sa persona. Deduction, et c'est une deduction et non un fait source :
sa persona ne contenait pas l'orientation politique. Consequence, la comparaison B1 contre
agent demographique n'est pas un duel a armes egales. Une variante de B1 privee de
`political_ideology` et `political_party` est donc rapportee : **0,5998**, contre 0,5818 pour
l'agent. La statistique gagne encore, mais l'ecart passe de 3,9 a 1,8 point.

### 2.2 Twin-2K-500

Identifiant verifie le 3 septembre 2026 via l'API Hugging Face :
`LLM-Digital-Twin/Twin-2K-500`, `private: false`, `gated: false`, `disabled: false`,
licence `cc-by-4.0`. Aucun jeton ni acceptation de conditions. Telechargement reussi, rien a
contourner. Papier associe : arXiv 2505.17479.

**Description, elle servira a tout le monde.**

- **2 058 participants**, echantillon representatif des Etats-Unis, identifiant `pid` de 1 a
  2 058.
- **Quatre vagues.** Les vagues 1 a 3 sont lancees a une semaine d'intervalle et melangent
  demographies, echelles psychologiques, tests cognitifs, preferences economiques et
  experiences d'economie comportementale. La **vague 4**, lancee deux semaines apres la
  vague 3, **repose les experiences d'heuristiques et de biais** des vagues precedentes. Elle
  fournit donc une mesure de fidelite test retest sur les memes personnes et les memes
  questions.
- **Le comptage des questions a trois niveaux**, et les melanger est la premiere erreur a ne
  pas faire : 256 identifiants Qualtrics au catalogue, environ 500 questions reellement
  posees a chaque participant une fois les matrices depliees, 760 colonnes de CSV une fois les
  choix multiples eclates en indicatrices. Le "plus de 500 questions" du depot correspond au
  niveau intermediaire.
- **Repartition des ~500 questions** : personnalite 279 (19 tests, 26 construits, dont le
  BFI-44), tests cognitifs 85, preferences economiques 34, preferences de prix sur 40 produits,
  experiences d'economie comportementale environ 48, heuristiques non experimentales 5,
  demographies 14.
- **Decoupage d'evaluation fourni par les auteurs**, configuration `wave_split` :
  `wave1_3_persona_text` et `wave1_3_persona_json` servent d'entree,
  `wave4_Q_wave4_A` sert de verite terrain, et `wave4_Q_wave1_3_A` donne les reponses des
  memes personnes aux memes questions avant la vague 4, c'est a dire le test retest.
- **Fichiers mis au propre**, configuration `question_catalog_and_human_response_csv` :
  `wave1_3_response.csv` 2 058 x 761 et `wave4_response.csv` 2 058 x 127, en codes numeriques,
  plus leurs jumeaux `_label` en clair, plus `question_catalog.json` qui donne pour chaque
  question son type, ses modalites, son bloc et ses colonnes de CSV.
- **Baselines deja calculees par les auteurs** : le dossier `LLM_simulation_results` contient
  onze configurations de simulation, avec pour chacune les reponses simulees au format du
  fichier humain. On y trouve GPT-4.1 et GPT-4.1-mini en persona JSON et en persona texte,
  Gemini-Flash-2.5 en persona texte, des variantes temperature, raisonnement et repetition des
  questions, une condition **demographies seules**, et un **modele affine sur 500 exemples**.
  Chaque dossier porte aussi une evaluation d'exactitude par MAD et des figures de
  distribution. Il n'y a en revanche **aucune baseline statistique** publiee par les auteurs :
  ni regression, ni plus proche voisin, ni copule. C'est exactement le trou que ce rapport
  comble.

**Verification importante avant toute comparaison.** Le persona des vagues 1 a 3 fourni au
modele **ne contient pas** les questions de la vague 4. Verifie sur le fichier
`wave_split/chunks/wave_persona_chunk_001.parquet` : les blocs presents dans
`wave1_3_persona_json` sont Cognitive tests, Demographics, Economic preferences, Forward Flow
et Personality, et aucun libelle de question de la vague 4 n'apparait dans le texte de 25
personas testes. Le modele n'a donc pas vu la reponse anterieure de la personne a la question
qu'on lui demande de predire. Notre B2 est construite sur exactement la meme information, ce
qui rend la comparaison honnete.

---

## 3. Le protocole, et l'endroit ou l'on triche sans le vouloir

### 3.1 GSS : deux decoupages simultanes

- **Sur les personnes.** Validation croisee a 5 plis, tirage fixe (graine 20260903). Aucune
  reponse d'une personne du pli de test n'entre dans l'estimation d'un parametre, ni dans une
  marginale, ni dans un encodage de variable.
- **Sur les items.** Les 149 items sont repartis en 5 blocs aleatoires. A chaque tour, un bloc
  est **secret** (environ 30 items) et les quatre autres (environ 119 items) forment le
  **contexte** disponible sur la personne testee. Chaque item est secret exactement une fois.

Chaque couple (personne, item) est donc predit une fois et une seule, ce qui produit une
matrice de predictions de la meme forme que la verite. C'est ce qui permet d'appliquer ensuite
telle quelle la mesure de diversite de `analyses/a0_diversite_osf.py`.

Precision qui evite un malentendu : **B0 et B1 n'utilisent aucun item de contexte.** Le
decoupage en blocs ne les concerne pas, il n'existe que pour B2. Elles sont donc calculees une
fois par pli de personnes, pour les 149 items.

### 3.2 Twin-2K-500 : le decoupage est temporel et fourni

Pas besoin de decouper les items, les auteurs l'ont fait : le contexte est la vague 1 a 3, la
cible est la vague 4. Validation croisee a 5 plis sur les personnes.

- **Cible** : les 108 colonnes de la vague 4 qui sont categorielles, c'est a dire de type MC a
  reponse unique ou Matrix. Les curseurs de 0 a 100 et les saisies libres sont exclus,
  l'exactitude exacte n'y a pas de sens. C'est 108 des 126 colonnes reposees.
- **Contexte** : les 494 colonnes categorielles des vagues 1 a 3 **qui ne sont pas reposees en
  vague 4**. Les 126 colonnes reposees sont retirees du contexte. Les garder donnerait a B2 la
  reponse anterieure de la personne a la question meme qu'on lui demande de predire, ce qui ne
  mesurerait plus rien d'autre que la stabilite test retest. Cette stabilite est mesuree a
  part et sert de plafond.
- **Demographies** : les 14 questions du bloc Demographics des vagues 1 a 3.
- 24,1 pour cent des cellules de la cible sont vides, parce que plusieurs experiences sont
  inter sujets et que chaque personne ne voit qu'une condition. Ces cellules sont exclues du
  numerateur et du denominateur, elles ne comptent jamais comme une erreur.

### 3.3 Les trois baselines

- **B0**, plancher absolu. Deux variantes, et il faut les deux. `B0 tirage` echantillonne dans
  la distribution marginale observee sur les personnes d'entrainement : c'est le vrai plancher
  et il conserve la diversite marginale. `B0 mode` repond toujours la modalite majoritaire :
  exactitude bien plus haute, diversite quasi nulle. L'ecart entre les deux est la mesure
  directe du compromis.
- **B1**, regression logistique multinomiale sur les seules demographies, une par item,
  indicatrices ajustees sur le pli d'entrainement seul (`handle_unknown='ignore'`). Variante
  `argmax`, la classe la plus probable, qui est le reglage de la litterature ; variante
  `tirage`, echantillonnage dans la distribution predite.
- **B2**, plus proches voisins. Distance de Hamming normalisee sur les seuls items de
  contexte, voisins cherches uniquement parmi les personnes d'entrainement, k = 30, vote
  majoritaire (`argmax`) ou tirage dans la distribution des voisins (`tirage`). L'item predit
  ne participe jamais au calcul de la distance.

### 3.4 Metriques

- **Exactitude par personne** sur les items secrets, egalite exacte de chaine ou de code.
- **Intervalle de confiance a 95 pour cent par bootstrap**, 2 000 tirages, **l'unite de
  reechantillonnage est la personne** et non la cellule. Deux reponses d'un meme individu ne
  sont pas independantes ; un bootstrap sur les cellules donnerait un intervalle faussement
  etroit.
- **Diversite conservee** : somme des entropies de Shannon des predictions, item par item,
  rapportee a la somme des entropies humaines sur les memes items. Reprise a l'identique de
  `a0_diversite_osf.py`.
- **Accord par paires** : probabilite que deux repondants tires au hasard donnent la meme
  reponse, indice de Simpson. Plus il est haut, plus la population predite est homogene. Chez
  les humains du GSS il vaut 49,3 pour cent.

---

## 4. Resultats, GSS

1 052 personnes, 149 items, plancher humain test retest **0,7950** [0,7897 ; 0,7999].

| methode | exactitude | IC 95 % | normalise | diversite conservee | accord paires |
|---|---|---|---|---|---|
| **B2 argmax** | **0,6717** | [0,6675 ; 0,6756] | 84,5 % | 58,5 % | 69,4 % |
| **B1 argmax** | **0,6209** | [0,6169 ; 0,6250] | 78,1 % | 74,0 % | 62,5 % |
| B1 argmax, recensement seul | 0,5998 | [0,5958 ; 0,6038] | 75,4 % | 63,7 % | non mesure |
| **B0 mode** | **0,5934** | [0,5890 ; 0,5976] | 74,6 % | 3,3 % | 98,1 % |
| B2 tirage | 0,5752 | [0,5713 ; 0,5790] | 72,4 % | 95,4 % | 51,7 % |
| B1 tirage | 0,5426 | [0,5391 ; 0,5461] | 68,2 % | 100,0 % | 49,2 % |
| **B0 tirage** | **0,4918** | [0,4891 ; 0,4947] | 61,9 % | 99,9 % | 49,3 % |

Points de repere, **recalcules sur les memes 149 items** :

| condition d'agent | exactitude | normalise | diversite conservee | accord paires |
|---|---|---|---|---|
| humains reinterroges | 0,7950 | 100 % | 100,4 % | 49,1 % |
| agents composite | 0,6839 | 86,0 % | 89,6 % | 53,9 % |
| agents entretien (v3) | 0,6565 | 82,6 % | 87,1 % | 55,9 % |
| agents enquete | 0,6510 | 81,9 % | 86,1 % | 55,4 % |
| agents demographiques (v6) | 0,5818 | 73,2 % | 63,9 % | 67,7 % |
| agents persona (v7) | 0,5640 | 70,9 % | 64,2 % | 68,3 % |
| agents v8 | 0,5591 | 70,3 % | 80,6 % | 58,0 % |

Lecture directe, sans adoucissement :

1. B1 sur demographies bat les trois conditions d'agents les plus faibles, dont l'agent
   demographique, de 3,9 points. Meme privee des attributs politiques elle le bat encore, de
   1,8 point.
2. B2 bat les agents entretien et enquete. Elle perd contre l'agent composite de 1,2 point
   seulement. Autrement dit, **cinq des six conditions d'agents du papier de Stanford sont
   battues par du scikit-learn**.
3. La modalite majoritaire, qui n'utilise aucune information sur l'individu, obtient 0,5934,
   soit **davantage que trois conditions d'agents sur six**. C'est le chiffre le plus
   desagreable du rapport et il est solide.

---

## 5. Resultats, Twin-2K-500

2 058 personnes, 108 items de la vague 4, plancher humain test retest **0,7119**
[0,7081 ; 0,7156].

| methode | exactitude | IC 95 % | normalise | diversite conservee | accord paires |
|---|---|---|---|---|---|
| GPT-4.1-mini, persona complet | 0,5530 | [0,5495 ; 0,5565] | 77,7 % | 58,6 % | 65,7 % |
| **B2 argmax** | **0,5301** | [0,5264 ; 0,5337] | 74,5 % | 53,4 % | 69,0 % |
| **B0 mode** | **0,5216** | [0,5170 ; 0,5261] | 73,3 % | 1,1 % | 99,2 % |
| **B1 argmax** | **0,5184** | [0,5148 ; 0,5221] | 72,8 % | 76,2 % | 57,5 % |
| GPT-4.1-mini, demographies seules | 0,4996 | [0,4960 ; 0,5032] | 70,2 % | 51,1 % | 68,9 % |
| B1 tirage | 0,4620 | [0,4593 ; 0,4645] | 64,9 % | 99,9 % | 44,4 % |
| B2 tirage | 0,4620 | [0,4593 ; 0,4645] | 64,9 % | 96,8 % | 46,1 % |
| **B0 tirage** | 0,4425 | [0,4402 ; 0,4449] | 62,2 % | 99,7 % | 44,4 % |

La hierarchie s'inverse par rapport au GSS, et c'est le resultat le plus interessant du
rapport.

1. **Le modele de langage avec persona complet gagne**, 0,5530 contre 0,5301 pour la meilleure
   baseline. L'ecart, 2,3 points, est bien au dela des intervalles de confiance.
2. **Dans le regime demographique, la statistique gagne encore**, comme sur le GSS : B1 obtient
   0,5184 contre 0,4996 pour la condition demographies seules du meme modele. Ici la
   comparaison est propre, les 14 questions demographiques ont ete fournies au modele et a la
   regression.
3. **La condition demographies seules du modele est en dessous de la modalite majoritaire**
   (0,4996 contre 0,5216). Un modele de langage a qui l'on ne donne que des demographies fait
   moins bien que repondre toujours la reponse la plus frequente.
4. B1 ne rattrape jamais B0 mode sur ce jeu, meme avec 1 646 personnes d'entrainement.

Pourquoi l'inversion. Hypothese, et elle est etiquetee comme telle : la cible de la vague 4
est faite d'experiences d'heuristiques et de biais, ou la reponse depend de la structure du
probleme bien plus que de qui repond. Les demographies et les traits de personnalite n'y
correlent presque rien, ce qui prive B1 et B2 de matiere, tandis qu'un modele de langage
dispose d'un savoir sur la tache elle meme. A verifier item par item avant d'en faire un
argument de papier.

---

## 6. La courbe de croisement

Figures : `resultats/a2-courbe-croisement-gss.png` et `.svg`,
`resultats/a2-courbe-croisement-twin.png` et `.svg`. Le pli de test est fixe et ne varie
jamais de taille, seul le corpus d'entrainement varie ; sans cela une courbe montante
confondrait l'effet de la taille avec la variance d'un test qui retrecit. Six tirages par
taille, ecart type en bande.

**GSS**

| n entrainement | B0 mode | B1 argmax | B2 argmax |
|---|---|---|---|
| 50 | 0,5846 | 0,5733 | 0,6140 |
| 100 | 0,5916 | 0,5761 | 0,6375 |
| 150 | 0,5907 | 0,5824 | 0,6467 |
| 200 | 0,5913 | 0,5893 | 0,6534 |
| 300 | 0,5928 | 0,5990 | 0,6589 |
| 400 | 0,5944 | 0,6047 | 0,6640 |
| 600 | 0,5940 | 0,6142 | 0,6682 |
| 841 | 0,5944 | 0,6222 | 0,6727 |

**Forme de la courbe.** B0 est plate des 100 personnes : une marginale se stabilise vite. B1
part **sous** B0, la croise vers **220 repondants**, puis monte encore de facon reguliere sans
signe de plateau a 841. B2 est au dessus de tout des 50 repondants, monte fort jusqu'a 200 puis
s'aplatit nettement.

Croisements avec les agents, par interpolation sur l'echelle logarithmique :

- B1 depasse l'agent demographique (0,5818) vers **145 repondants**.
- B2 depasse l'agent enquete (0,6510) vers **180 repondants** et l'agent entretien (0,6565)
  vers **250 repondants**.
- Ni B1 ni B2 ne rejoignent l'agent composite (0,6839) dans la plage mesuree, et la pente de
  B2 a 841 rend improbable qu'elle le rejoigne avant plusieurs milliers de personnes.

**Twin-2K-500**

| n entrainement | B0 mode | B1 argmax | B2 argmax |
|---|---|---|---|
| 50 | 0,5016 | 0,4789 | 0,5033 |
| 100 | 0,5114 | 0,4805 | 0,5127 |
| 200 | 0,5154 | 0,4824 | 0,5181 |
| 400 | 0,5195 | 0,4914 | 0,5205 |
| 800 | 0,5210 | 0,5059 | 0,5252 |
| 1200 | 0,5210 | 0,5137 | 0,5286 |
| 1646 | 0,5213 | 0,5183 | 0,5305 |

Meme forme, echelle ecrasee. B0 sature vers 800. B1 reste sous B0 sur toute la plage et ne la
croise pas a 1 646. B1 depasse la condition demographies seules du modele vers **590
repondants**. Aucune baseline n'atteint le modele a persona complet.

**Ce que la courbe dit pour la suite.** L'ordre de grandeur a retenir est de **quelques
centaines de repondants reels**, pas quelques milliers. Passe 200 a 250 personnes du meme
echantillon, une methode statistique classique rend inutile un agent de langage nourri au
questionnaire ou a l'entretien, sur le GSS. En dessous de 100, l'agent garde l'avantage. Ce
seuil est le nerf du dossier : toute condition experimentale du projet qui dispose de plus de
250 repondants comparables doit justifier son emploi d'un modele de langage autrement que par
l'exactitude.

---

## 7. Le regime des questions jamais posees

Une question jamais posee a personne n'a **aucune ligne d'entrainement** : ni B1 ni B2 ne sont
definies, elles n'ont rien pour apprendre. Il faut distinguer deux regimes que la litterature
confond souvent.

- **Regime R1, jamais posee a personne.** Aucune cible, aucun voisin informatif. Seul survit un
  tirage uniforme sur les modalites declarees. C'est le vrai plancher.
- **Regime R2, posee a d'autres mais jamais a cette personne.** C'est le protocole standard des
  sections 4 et 5, B1 et B2 s'y appliquent normalement.

Entre les deux se glisse un cas intermediaire qu'il faut nommer, car c'est lui qui compte :
**la marginale de la question est connue par une autre enquete, mais aucun lien individuel ne
l'est**. Alors la modalite majoritaire redevient calculable, et c'est elle le vrai adversaire
d'un modele de langage sur ce terrain, puisqu'un modele a lui aussi lu ces marginales quelque
part pendant son entrainement.

**Familles retenues sur le GSS**, definies par lecture des libelles des 149 items :

| famille | items | modalites | plancher uniforme | plafond modalite majoritaire | accord paires humain |
|---|---|---|---|---|---|
| depenses publiques (`nat*`) | 17 | 3,0 | 33,3 % | 57,7 % | 45,9 % |
| confiance dans les institutions (`con*`) | 13 | 3,0 | 33,3 % | 50,5 % | 41,5 % |
| avortement (`ab*`) | 7 | 2,0 | 50,0 % | 74,4 % | 64,8 % |
| libertes civiles (`spk`/`col`/`lib`) | 11 | 2,0 | 50,0 % | 75,0 % | 65,4 % |
| fin de vie (`suicide*`, `letdie1`) | 5 | 2,0 | 50,0 % | 72,8 % | 60,9 % |
| roles de genre (`fe*`) | 5 | 3,8 | 29,0 % | 48,0 % | 38,0 % |

Ces six familles sont retenues parce qu'elles sont thematiquement fermees, verifiables au
libelle, et assez fournies pour que le chiffre soit stable. Une famille entiere se retire
proprement du corpus, cible **et** contexte, sans laisser de correlat evident dans le reste du
questionnaire.

**Familles retenues sur Twin-2K-500**, blocs du catalogue :

| famille | items | modalites | plancher uniforme | plafond modalite majoritaire | accord paires humain |
|---|---|---|---|---|---|
| Product Preferences - Pricing | 40 | 2,0 | 50,0 % | 55,9 % | 50,7 % |
| False consensus | 10 | 5,0 | 20,0 % | 39,7 % | 28,3 % |
| Non-experimental heuristics and biases | 10 | 6,2 | 18,9 % | 36,1 % | 27,5 % |
| Probability matching, probleme 1 | 10 | 2,0 | 50,0 % | 77,2 % | 65,9 % |

**Ce que ce tableau etablit.** Les familles a beaucoup de modalites et a faible accord humain
sont le terrain le plus favorable a un modele de langage : sur "Non-experimental heuristics and
biases", 10 items a 6,2 modalites en moyenne, le plancher tombe a 18,9 pour cent et le plafond
informe a 36,1 pour cent. Un modele de langage y est structurellement a l'abri d'une defaite
contre une methode entrainee, puisque aucune methode entrainee n'existe. C'est la que doivent
se placer les conditions experimentales du projet, et c'est aussi la que la valeur ajoutee
devra etre demontree en valeur absolue, faute de quoi elle ne sera pas demontree du tout.

Inversement, sur "Probability matching, probleme 1", le plafond informe est a 77,2 pour cent :
un modele de langage qui n'atteint pas ce chiffre y perd contre une ligne de code qui ne
regarde personne.

---

## 8. Exactitude et diversite, le couple

Figure : `resultats/a2-exactitude-diversite.png` et `.svg`.

| jeu | methode | exactitude | diversite conservee |
|---|---|---|---|
| GSS | B0 mode | 0,5934 | 3,3 % |
| GSS | B0 tirage | 0,4918 | 99,9 % |
| GSS | B1 argmax | 0,6209 | 74,0 % |
| GSS | B1 tirage | 0,5426 | 100,0 % |
| GSS | B2 argmax | 0,6717 | 58,5 % |
| GSS | B2 tirage | 0,5752 | 95,4 % |
| GSS | agents composite | 0,6839 | 89,6 % |
| Twin | B0 mode | 0,5216 | 1,1 % |
| Twin | B0 tirage | 0,4425 | 99,7 % |
| Twin | B1 argmax | 0,5184 | 76,2 % |
| Twin | B1 tirage | 0,4620 | 99,9 % |
| Twin | B2 argmax | 0,5301 | 53,4 % |
| Twin | B2 tirage | 0,4620 | 96,8 % |
| Twin | GPT-4.1-mini persona complet | 0,5530 | 58,6 % |

Trois lectures.

**Chaque baseline achete son exactitude en detruisant la dispersion.** Le passage de `tirage` a
`argmax` gagne 8 a 12 points d'exactitude et coute 25 a 45 points de diversite. La forme
extreme est B0 : 10 points d'exactitude achetes contre 96 points de diversite.

**B1 est plus interessante qu'il n'y parait sur ce plan.** A 0,6209 elle conserve 74,0 pour
cent de la diversite humaine, contre 58,5 pour cent pour B2 a 0,6717. B2 est plus exacte mais
plus grossiere : son accord par paires monte a 69,4 pour cent contre 49,3 pour cent chez les
humains, ce qui est exactement la signature d'ecrasement mesuree en a0 sur les agents.

**Le seul avantage clair des modeles de langage dans nos mesures est ce couple.** L'agent
composite du GSS fait 0,6839 avec 89,6 pour cent de diversite conservee : personne d'autre ne
tient les deux. Aucune de nos baselines n'atteint ce coin du plan. C'est un resultat favorable
au projet et il est mesure, pas espere. Il ne dit rien de la these de la double distorsion, qui
demande de separer variance intra et inter et que ce rapport ne fait pas.

---

## 9. Limites, et ce qui affaiblit ces chiffres

1. **Le k de B2 a ete choisi sur un pli de test.** Balayage sur le pli 0 : k = 1 donne 0,6063,
   k = 25 donne 0,6763, k = 40 donne 0,6782, k = 200 donne 0,6584. La courbe est plate entre 15
   et 60, k = 30 a ete retenu. L'optimisme induit est d'au plus 0,2 point, mais il est reel et
   un protocole propre passerait par une validation interne au pli d'entrainement.
2. **B2 dispose de beaucoup d'information sur la personne** : environ 119 items de contexte sur
   le GSS. C'est comparable a ce que recoit un agent enquete, pas a un agent demographique. Le
   dire autrement serait malhonnete. La comparaison B2 contre agents demographiques n'a pas de
   sens ; celle contre agents enquete et entretien en a un.
3. **L'exactitude exacte est une metrique dure sur des echelles ordinales.** Repondre "agree"
   quand la personne a repondu "strongly agree" compte comme une erreur complete. La
   litterature emploie aussi la correlation ou la MAD, qui donneraient d'autres classements.
   Le choix de l'exactitude exacte est celui de Stanford, il permet la comparaison directe,
   c'est sa seule justification.
4. **Sur Twin, seuls 108 des 126 items reposes sont evalues.** Les curseurs et les saisies
   libres sont exclus. La comparaison avec les chiffres publies par les auteurs, qui reposent
   sur une MAD sur l'ensemble des colonnes, n'est donc pas immediate.
5. **Un seul modele de langage sert de repere sur Twin**, GPT-4.1-mini, dans deux
   configurations. Les neuf autres configurations disponibles n'ont pas ete evaluees, faute
   d'utilite immediate. Le classement modele contre baseline pourrait bouger avec un autre
   modele.
6. **Les variantes `tirage` reposent sur un tirage aleatoire unique**, avec graine fixee. Leur
   exactitude porte une variance d'echantillonnage non quantifiee ici, de l'ordre de quelques
   dixiemes de point.
7. **Le decoupage en blocs d'items du GSS est aleatoire**, donc un bloc secret peut contenir
   plusieurs items d'une meme famille tandis que ses cousins restent dans le contexte. B2 en
   profite. Un decoupage par famille, plus severe, donnerait un B2 plus bas. C'est le
   prolongement le plus utile de ce travail.
8. **Aucune copule gaussienne n'a ete construite**, alors que la passation la cite comme
   egalant 37 modeles. B2 en est un substitut non parametrique, pas un equivalent.

---

## 10. Ce que ces resultats impliquent pour le projet

**Le test existentiel n'est pas passe, il est partage.** Sur le GSS, en regime demographique
comme en regime questionnaire, une methode statistique classique suffit et le modele de langage
ne se justifie pas par l'exactitude. Sur Twin-2K-500, en regime persona complet et sur des
questions sans correlat statistique, il se justifie.

Trois consequences directes.

1. **La baseline non LLM devient obligatoire dans toute condition, et ce n'est plus B1.** C'est
   B2, plus proches voisins sur les questions connues, k = 30. B1 seule sous estimerait
   l'adversaire de 5 points.
2. **Le terrain a defendre est celui des questions jamais posees et des familles a nombreuses
   modalites**, pas celui de l'exactitude globale sur un questionnaire dense. La section 7
   donne les familles a retenir et leurs planchers.
3. **La mesure sur laquelle le projet peut revendiquer une contribution est le couple
   exactitude et diversite**, pas l'exactitude seule. C'est la seule dimension ou les agents de
   langage dominent nettement toutes nos baselines, et c'est aussi celle qu'aucun papier lu ne
   publie.

Un chiffre desagreable trouve cette semaine vaut mieux que le meme chiffre trouve par un
relecteur dans six mois. Les voici : cinq des six conditions d'agents du papier de Stanford
sont battues par du scikit-learn, et la modalite majoritaire en bat trois.
