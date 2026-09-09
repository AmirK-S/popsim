# R2, preenregistrement : la comparaison appariee sur les gens rares, en regime severe

**Ecrit le 8 septembre 2026 a 22:05:00 CEST, AVANT le moindre appel de modele de langage.**
Aucun serveur n'a ete lance par cet agent au moment ou ce fichier est ecrit ; la machine est
occupee par le run R1 jusque vers 01:00, et la contrainte d'un seul `llama-server` a la fois
est tenue. Ce fichier n'est plus modifie ensuite : le rapport `resultats/r2-rares-apparie.md`
le reproduit et rapporte les mesures a cote, quel qu'en soit le signe.

C'est le **verrou 1** de `MODELE-DU-MONDE.md` section 10.5 : *« la comparaison appariee du
rappel des minorites, restreinte aux raretes stables : un run en regime severe sur
gpt-oss-20b, famille retiree de l'invite [...] ; une nuit »*.

---

## 0. Etat de connaissance declare au moment de l'ecriture

Sont lus et connus : `MODELE-DU-MONDE.md` section 10 en entier, `MOONSHOTS.md`,
`resultats/a41-regime-severe.md`, `resultats/a42-plancher-de-bruit.md`,
`resultats/a35-llm-comme-imputation.md`, `resultats/a5-agents-locaux-gss.md`,
`resultats/a3-inference-locale.md`, et les scripts `a5_agents_locaux_gss.py`,
`a5_evaluer.py`, `a33_commun.py`, `a34_commun.py`, `a35_familles.py`, `a41_commun.py`,
`a42_commun.py`, `a42_plancher.py`, `a44_commun.py`.

**Ce qui n'a jamais ete calcule, sur aucune de ses marges, et qui est l'objet de ce plan :**
le croisement des deux instruments. a42 mesure le rappel des raretes **stables** sur les
**149 items** et hors regime severe. a41 mesure le regime severe sur les **58 items de
famille** mais sur le rappel minoritaire **toutes raretes confondues**, stables et instables
melangees. **La case « raretes stables x 58 items de famille x regime severe » n'existe dans
aucun fichier de `resultats/`.** Aucun appel de gpt-oss-20b n'a jamais ete fait sur le GSS :
la seule trace d'agent local en regime severe est `data/traces/a5-C3F-p1.jsonl`,
Qwen3-4B-Instruct-2507, 60 personnes completes et une partielle.

**Chiffres connus qui bornent les predictions.** [MESURE, rapports cites]

| fait connu | source |
|---|---|
| C3F Qwen3-4B perd de 4,3 a 13,4 points d'exactitude contre les six methodes du regime severe, sur 60 personnes et 58 items, six intervalles disjoints de zero | a41 section 5 |
| C3 Qwen3-4B, hors regime severe, a un exces de plus 0,1616 [0,1086 ; 0,2106] sur le plancher de segment, sur les raretes **stables**, perimetre 150 | a42 section 6 |
| C2 Qwen3-4B, meme trace, exces plus 0,0327 [moins 0,0054 ; 0,0749], non distinguable d'un tirage dans le segment | a42 section 6 |
| `agents composite` de Stanford : rappel des raretes stables 0,408 contre 0,080 pour la regression, plancher de segment 0,109, exces plus 0,289 [0,267 ; 0,311], perimetre 1 052, **hors regime severe** | a42 section 3 |
| en regime severe, sur le rappel minoritaire des 58 items, `agents composite` fait 1,86 fois `PMM k=10 famille retiree`, mais avec les cousins dans son invite, donc **non apparie** | a41 section 8 |
| debit mesure de C3F sur Qwen3-4B : 2 688 appels par heure, machine a charge 1,4 | `data/traces/a5-familles.log` |
| gpt-oss-20b contre Qwen3-4B : 9 569 contre 18 060 appels par heure en regime etabli, prefill 492 contre 790 tokens par seconde | a3 sections 4.4 et 5.1 |

---

## 1. La question, et pourquoi elle est la derniere debout

`MODELE-DU-MONDE.md` 10.4 ecrit, apres a44 : *« Son seul avantage mesure tient sur les gens
rares reels [...] et il attend sa comparaison appariee. »* Les trois autres avantages sont
tombes. L'exactitude est tombee en regime apparie (a41 sections 4 et 5). La structure est
tombee contre les imputations a tirage (a41 section 7). Les mesures de gonflement et
d'ecrasement sont reproduites par un generateur sans structure individuelle (a44).

Il reste une case, et elle est mal mesuree pour une raison precise : **la comparaison n'est
appariee ni chez Stanford ni chez nous.** Les six conditions d'agents de Stanford gardent les
items cousins de la question dans leur invite, alors que les methodes statistiques du regime
severe perdent la famille entiere de leur contexte (a8 errata E1, a41 section 0.2). Et la
seule condition ou nous imposons le regime severe aux deux cotes, C3F, tourne sur un modele
de 4 milliards de parametres et sur 60 personnes.

**Question de R2.** Dans le regime severe, la famille thematique entiere retiree de l'invite
comme elle l'est du contexte des methodes statistiques, un jumeau de langage serieux
retrouve t il les **gens rares reels** (les raretes que la personne redonne en vague 2) mieux
que les imputations statistiques a tirage, sur les **memes personnes** et les **memes
cellules** ?

---

## 2. Le perimetre, fixe d'avance

| | |
|---|---|
| Personnes | les 150 de `data/traces/a5-personnes.csv`, 30 par pli, graine 20260907, ecrites avant le premier appel de a5 et non retirees |
| Items | les 58 items des six familles thematiques de `FAMILLES` dans `a2_baselines_gss.py`, exactement le perimetre de a8, a35 section 6, a41 |
| Condition primaire | **C3F**, contexte = les 149 items moins **toute la famille** de l'item cible, soit 132 a 144 items, aucune demographie, aucune etiquette |
| Condition secondaire | **C3**, contexte = les 119 items du bloc de a2, cousins compris, memes 150 personnes, memes 58 items cibles |
| Modele primaire | **gpt-oss-20b**, GGUF MXFP4, coupure publiee juin 2024, gabarit de conversation obligatoire (a3 section 4.5) |
| Modele de repli | **Qwen3-30B-A3B-Instruct-2507** Q4_K_M, si et seulement si gpt-oss echoue le smoke test de masse ; le repli est ecrit dans le journal et dans le rapport |
| Cellules jugees | les cellules **minoritaires reelles** au seuil de 10 pour cent (definition de `a8_commun.modalites_minoritaires`, importee) que la personne **redonne a l'identique en vague 2** (partition P_A de a42, importee de `a42_commun.classes_stabilite`) |
| Plancher | tirage dans la marginale du segment ideologie x genre x age, sans la personne (`a34_commun.frequence_segment`, importe), le plancher de bruit de cellule de la lecture 01 |
| Adversaires | les six methodes du regime severe de a41 : `E1 famille retiree (argmax)`, `E2 famille retiree (tirage)`, `PMM k=10 famille retiree`, `IM m=10 mode, famille retiree`, `B2 famille retiree (argmax)`, `B2 famille retiree (tirage)`, importees de `a35_familles.imputer_par_famille` et de `a33_commun.b2_famille_retiree` par `a41_commun.construire_severe` |
| Reperes non testes | `C3F` Qwen3-4B (trace a5 existante, 60 personnes), `B3 foret`, `B0 mode`, `B0 tirage`, `humains vague 2` |

**Ordre des appels.** Personne par personne, famille par famille, comme a5. Une troncature a
08:00 coute des **personnes entieres**, jamais des items : toute personne evaluee porte ses
58 cellules. Les mesures sont des rapports de sommes par personne, le bootstrap porte sur les
personnes, et un echantillon tronque reste un echantillon de personnes completes.

**Ce qui est identique a a5, mot pour mot, et sera controle :** le decoupage de
`a2_baselines_gss.grille` graine 20260903, l'echantillon de 150 personnes graine 20260907, la
construction du prompt systeme C3 et C3F, le bloc utilisateur, l'ordre des modalites de
`question_master/gss/main.csv`, le scoring par lettre a un token verifie par encodage du
prefixe, le seuil de rejet de masse a 0,5, le format de trace. **Ce qui change et rien
d'autre : le modele, et donc le gabarit de conversation.**

---

## 3. La famille d'hypotheses, ecrite avant tout appel

Quatre familles, **corrigees separement par Holm**, Benjamini Hochberg rapporte a cote. Tous
les p sont des p de bootstrap **apparie sur les personnes**, memes tirages pour toutes les
methodes, 4 000 tirages, plancher du p a 1 sur 4 000. Un contraste a denominateur vide recoit
p = 1, convention conservatrice de a29, a31, a34 et a42.

### F1, primaire, le rappel des raretes stables en regime severe. 7 tests.

| | enonce | direction |
|---|---|---|
| **H1a** | l'exces de rappel de `C3F gpt-oss` sur le **plancher de segment**, sur les raretes **stables** des 58 items, est strictement positif | dirige |
| **H1b** | pour chacune des **six** methodes du regime severe, l'avantage de rappel de `C3F gpt-oss` sur les raretes stables des 58 items est strictement positif | dirige, 6 tests |

### F2, secondaire, la precision. 7 tests.

| | enonce | direction |
|---|---|---|
| **H2a** | la precision de `C3F gpt-oss` sur les raretes stables des 58 items est strictement superieure a celle d'un tirage dans le segment | dirige |
| **H2b** | pour chacune des six methodes du regime severe, la precision de `C3F gpt-oss` sur les raretes stables est strictement superieure | dirige, 6 tests |

La precision est declaree parce que le rappel seul est achetable : une methode qui ose une
modalite minoritaire partout a un rappel eleve et une precision nulle. Le F1 est rapporte a
cote, sans test declare.

### F3, tertiaire, l'exactitude globale. 7 tests.

| | enonce | direction |
|---|---|---|
| **H3a** | difference d'exactitude par personne entre `C3F gpt-oss` et chacune des six methodes du regime severe, sur les memes personnes et les memes 58 items | bilateral, 6 tests |
| **H3b** | difference d'exactitude entre `C3F gpt-oss` et `C3F Qwen3-4B` sur les 60 personnes communes | bilateral, 1 test |

### F4, quaternaire, la structure. 8 tests, plus un descriptif.

| | enonce | direction |
|---|---|---|
| **H4a** | difference de diversite conservee entre `C3F gpt-oss` et les quatre methodes a **tirage** du regime severe | bilateral, 4 tests |
| **H4b** | difference des **ecarts absolus a 1** du ratio intra segment, `C3F gpt-oss` moins chacune des quatre methodes a tirage (critere de proximite de `a41_commun.contraste_proximite`) | bilateral, 4 tests |
| **H4c** | descriptif, hors famille : chute d'exactitude sous permutation des personnes a l'interieur de leur camp ideologique (`a44_commun.permuter_intra`), pour `C3F gpt-oss`, `C3F Qwen3-4B`, les six methodes severes et les humains de la vague 2 | descriptif |

H4c est declare **descriptif et non testable** ici : a44 mesure la chute sur 149 items et
1 052 personnes ; sur 58 items et au plus 150 personnes, le segment ideologie x genre x age
compte une a trois personnes par case et la permutation intra segment y est presque
l'identite. La quantite sera calculee sur le **camp** a trois niveaux (gauche, droite,
centre), qui est la segmentation de a44 section 5, et rapportee avec son plancher humain ;
si le nombre de personnes par camp descend sous dix, elle sera declaree non calculable et
la case restera vide. C'est ecrit d'avance pour qu'un resultat absent ne soit pas lu comme
un resultat neutre.

---

## 4. Les criteres de chute, ecrits d'avance

1. **Si H1a echoue pour `C3F gpt-oss`**, c'est a dire si son rappel des raretes stables en
   regime severe n'est pas distinguable d'un tirage au sort dans le segment de la personne :
   **le dernier avantage du jumeau de langage tombe**, et la phrase de `MODELE-DU-MONDE.md`
   10.4, « son seul avantage mesure tient sur les gens rares reels », doit recevoir la
   restriction « hors du regime ou l'information la plus proche manque ». Le verrou 1 se
   ferme dans le sens negatif.
2. **Si H1a passe mais que H1b echoue contre `PMM k=10 famille retiree` et
   `IM m=10 mode, famille retiree`** : l'avantage existe contre le hasard mais pas contre
   l'imputation. La formulation autorisee devient « il bat le tirage dans le segment, il ne
   bat pas l'appariement sur moyenne predite », et la these perd sa derniere superiorite
   comparative. C'est la conclusion de a41 etendue au dernier critere.
3. **Si H1a et H1b passent tous les deux** : c'est la premiere mesure appariee du dossier qui
   soutient la these, et le verrou 1 s'ouvre. L'enonce autorise sera exactement, et pas plus :
   « quand la famille thematique entiere de la question manque des deux cotes, un jumeau de
   langage de 20 milliards de parametres retrouve les reponses rares que la personne redonne
   deux semaines plus tard mieux que l'imputation statistique sur les memes cellules ».
4. **Si H3a est entierement negatif**, ce qui est attendu : la phrase reste « le rappel des
   rares, et lui seul », jamais « l'exactitude ». Un H3a positif contre une methode a tirage
   serait un fait nouveau et devrait etre reverifie avant publication.
5. **Si le run ne couvre pas au moins 60 personnes avant 08:00** : le rapport publie les
   mesures sur ce qu'il a, declare la couverture en tete de chaque tableau, et **ne conclut
   pas sur le verrou 1** ; la comparaison a 60 personnes est exactement la taille de la
   trace Qwen3-4B existante, donc le plancher de lisibilite est fixe la.
6. **Si le smoke test de 20 appels ne place pas au moins 0,90 de masse de probabilite sur les
   lettres**, le run s'arrete sans ecrire une ligne de trace utile, le modele de repli est
   lance, et l'echec est ecrit dans le rapport. Le seuil de 0,90 est au dessus du seuil de
   rejet par appel de a5, qui est 0,50 : un modele mal gabarite doit etre attrape au
   demarrage et non appel par appel.

---

## 5. Les predictions, ecrites d'avance

Elles sont ecrites pour que le lecteur puisse constater qu'elles ont ete faites avant, et
pour qu'une prediction fausse compte contre nous. [HYPOTHESE pour les cinq]

- **(a) H1a passe** pour `C3F gpt-oss`. Motif : C3 Qwen3-4B, plus petit et hors regime
  severe, a deja plus 0,1616 d'exces sur ce plancher (a42 section 6).
- **(b) H1b passe contre `B2 famille retiree (argmax)`, `E1 famille retiree` et
  `IM m=10 mode`, et est incertain contre `PMM k=10 famille retiree` et
  `E2 famille retiree (tirage)`.** Motif : a42 place `PMM k=10` a plus 0,2025 d'exces sur les
  raretes stables hors regime severe, donc au dessus de C3 Qwen3-4B ; a41 section 6 mesure
  que le retrait de la famille coute a `PMM k=10` moins 8,9 points de rappel minoritaire,
  plus qu'a toute autre methode. Les deux effets vont en sens contraire et je ne sais pas
  lequel domine.
- **(c) H2 echoue au moins contre `PMM k=10 famille retiree`.** Motif : un modele de langage
  ose plus de modalites minoritaires qu'une imputation par appariement, et paie en precision
  ce qu'il gagne en rappel.
- **(d) H3a reste entierement negatif**, mais l'ecart median passe sous les 9,8 points de
  Qwen3-4B contre `PMM k=10`. Autrement dit : gpt-oss reduit l'ecart, il ne le renverse pas.
  Une inversion contre `E1 famille retiree` serait une surprise.
- **(e) H4a place `C3F gpt-oss` sous 80 pour cent de diversite conservee**, donc sous les
  98,0 de `PMM k=10 famille retiree` et les 99,5 de `E2 famille retiree`. Motif : C3F
  Qwen3-4B est a 59,0 pour cent et l'ecrasement de la dispersion est le fait le plus stable
  du dossier.

---

## 6. Ce que chaque issue voudrait dire pour `MOONSHOTS.md`

Le juge a recommande le **programme A**, l'oracle des camps, avec le **programme B**, la
bande humaine comme norme d'audit, en second et « le seul ou le dossier detient deja la
mesure ». R2 ne decide ni A ni B directement ; il decide ce que ces programmes ont le droit
de promettre.

- **Issue 1, H1a et H1b passent.** Le dossier detient une seconde quantite de personne, a
  cote de la chute sous permutation de a44 : le rappel des raretes stables en regime severe.
  Le **programme B** y gagne une statistique de reserve de plus, prise sur la personne et non
  sur les marges, exactement le type de mesure que sa section « ce qui ne se leve pas »
  reclame ; et l'audit des simulateurs vendus (moonshot 9 du jugement, E1 et E2) gagne son
  critere d'achat : un simulateur qui ne retrouve pas les rares stables d'un panel tenu cache
  ne vaut pas son prix. **Le programme A n'est pas touche** : il porte sur le mode
  description, pas sur l'imputation.
- **Issue 2, H1a passe et H1b echoue.** La formule de vente du dossier devient defensive :
  « une population simulee ne fabrique pas une societe sans minorites, mais l'imputation
  statistique en fabrique moins encore ». Le **programme B** garde sa norme, qui ne depend
  pas de la superiorite du langage mais de la detectabilite d'un flux ; le **moonshot de
  l'audit des simulateurs** perd son argument commercial, puisque la reponse a l'acheteur
  devient « achetez le modele tabulaire », ce que le jugement anticipait deja pour le
  programme E3.
- **Issue 3, H1a echoue.** `MODELE-DU-MONDE.md` 10.4 doit etre reecrit une fois de plus, et
  le dossier n'a plus aucun avantage mesure du jumeau de langage sur une comparaison
  appariee. C'est **l'issue qui renforce le programme B et affaiblit tout le reste** : si
  meme les gens rares tombent, la seule chose que le projet sache faire est de dire si une
  population contient des personnes, ce qui est exactement l'enonce du programme B. Ce n'est
  pas un echec du projet, c'est le resultat negatif qui compte autant que le positif, selon
  le quatrieme critere du jugement.
- **Dans les trois cas**, la couverture en personnes et la ligne « ce que je n'ai pas pu
  verifier » sont publiees, et le rapport n'ecrit aucune phrase sur les agents de Stanford :
  R2 mesure **nos** agents, pas les leurs, interdiction 4 de a41 section 7.

---

## 7. Ce que ce plan ne fera pas

- **Il ne replace pas les six conditions de Stanford dans le regime severe.** C'est
  impossible sans relancer leur pipeline, et l'errata E1 de a8 le dit. Elles sont citees
  comme reperes, jamais comme adversaires apparies.
- **Il ne fait pas la passe 2.** L'ordre inverse des modalites est la parade au biais de
  position ; elle coute un doublement des appels et le budget de la nuit ne le permet pas.
  Le biais de position est donc **non controle** dans R2, et cela est ecrit dans le rapport.
  Il est le meme pour les deux conditions C3F et C3, donc il ne biaise pas leur comparaison.
- **Il ne mesure pas la contamination.** La coupure publiee de gpt-oss-20b, juin 2024, est
  anterieure a la vague du GSS employee ; le choix du modele est fait pour la coupure
  **publiee**, pas verifiee, et a3 section 2 rappelle que ce n'est pas une garantie.
- **Il ne conclut rien sur les 1 052 personnes.** Les 150 personnes sont un sous echantillon
  stratifie sur les cinq plis ; la generalisation aux 1 052 n'est pas dans le perimetre.

---

*Fin du preenregistrement. Horodatage : 8 septembre 2026, 22:05:00 CEST.*
