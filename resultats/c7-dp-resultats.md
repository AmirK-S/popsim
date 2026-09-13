# C7-DP, resultats (12 septembre 2026) — RAPPORT RETRACTE le 13 septembre 2026

statut: retracte_par: resultats/audit-comparaison-dp-2026-09-13.md
fait_foi: resultats/audit-comparaison-dp-2026-09-13.md
mandat: Mesurer ce qu'un generateur synthetique sous confidentialite differentielle coute en utilite et laisse fuir, et le comparer a nos defenses — mandat dont l'execution est invalidee ci-dessous
agent: Claude Opus 5, sous-agent correction retractation DP (pose de la retractation) ; redaction d'origine, sous-agent C7-DP du 12 septembre 2026
ecriture: resultats/c7-dp-resultats.md (en-tete et section 0 seulement ; le corps d'origine est conserve mot pour mot)
lecture_seule: tout le reste
interdits: appel payant, reseau, commit sur master, arriere-plan, modification de article/manuscrit.md
cout_reel_usd: 0.00

---

## 0. Pourquoi ce rapport est retracte, et ce qui en survit

Rien n'est efface : le corps d'origine reste ci-dessous mot pour mot, pour que la trace
de ce qui a ete affirme reste lisible. Ce qui est retire, c'est son autorite.

L'audit adverse `resultats/audit-comparaison-dp-2026-09-13.md` etablit trois defauts dont
chacun suffit a invalider le tableau et le verdict :

- **Reference desappariee.** `analyses/c7_dp.py` ajuste le generateur sur les 2 058
  **humains** (ligne 148) et note son utilite contre le **jumeau** (ligne 152). La DP se
  voit donc facturer l'ecart humains-jumeau, qui vaut 3,118 points
  (`c7-defense-resultats.csv`, ligne `aucune`, colonne `erreur_distribution_hum`) — soit
  exactement le « cout » de 3,1-3,2 publie. Le meme generateur ajuste sur le jumeau tombe
  a 0,92 point a eps = 10 et 1,00 a eps = 3.
- **Le budget ne contribue a rien.** A eps = infini, c'est-a-dire **sans aucune
  confidentialite**, le cout est deja le meme (3,52 dans ce tableau, pire qu'a eps = 10).
  La contribution marginale du budget est de 0,0 a 0,3 point, non de 3,1-3,2. Ce qui est
  mesure est le cout de l'hypothese d'independance entre items, pas celui de la DP.
- **Mecanisme homme de paille.** Laplace et composition sequentielle basique (eps/60 par
  item). Une gaussienne composee sous zCDP donne sigma = 20,2 au lieu d'un ecart-type
  effectif de 56,6 au meme eps = 3, soit 2,8 fois moins de bruit.

S'y ajoutent : des taux top-1 qui valent 0 a 3 personnes sur 2 058, non monotones en
epsilon et a intervalles recouvrants (aucun classement des deux mecanismes n'est
soutenable, dans aucun sens) ; aucun replicat ni intervalle du cote de l'utilite ; et une
composante « correlations » ou les deux mecanismes detruisent 100 % de la structure
(amplitude reelle 4,32 : D4 = 4,37, DP = 4,50-4,60, tous au-dessus du plancher de
destruction totale), de sorte que l'ecart 4,40 contre 4,47-4,59 est la variance de deux
estimations de zero.

**La phrase de verdict de la section « Superposition » et la phrase « En clair » sont
retirees.** Aucune superiorite de D4 sur la confidentialite differentielle n'est
revendiquee, dans aucun sens.

**Ce qui survit, et qui n'a pas besoin de ce tableau** : la section « La reponse
theorique ». La DP protege l'appartenance a l'echantillon, notre attaque porte sur la
liaison attribut-personne ; le generateur DP ne conditionne jamais sur un individu
(fidelite < 0,2 pt a tout epsilon). Cet argument est conceptuel, il ne depend d'aucun
chiffre du tableau retracte, et il reste opposable.

**Ce qui doit etre dit a la place** : la formulation de remplacement est celle du §8 de
l'audit, reprise in extenso dans `resultats/retractation-dp-d4-2026-09-13.md`. Ce dernier
porte aussi la fiche de report vers `article/manuscrit.md`.

**Ce qu'il faudrait pour republier un chiffre ici** : amender
`resultats/c7-dp-preenregistrement.md` pour dire lequel des deux objets la DP est censee
proteger, puis reexecuter avec le mecanisme gaussien zCDP, au moins 10 graines et un
intervalle des deux cotes. Rien de tout cela n'a ete fait ; `analyses/c7_dp.py` est laisse
intact pour que `c7-dp-resultats.csv` reste reproductible.

---

*Corps d'origine, conserve sans retouche. Tout chiffre ci-dessous est retracte.*

## Mecanisme, ce qu'il garantit vraiment
Marginales par item bruitees (Laplace, sensibilite L1 = 2, budget reparti a parts egales sur 60 items, composition sequentielle basique) puis tirage i.i.d. par item (PrivBayes degre 0, aucune structure jointe). Epsilon-DP prouve pour la publication des histogrammes sur les 2 058 humains vague 4 ; le synthetique en herite par post-traitement. NON garanti : correlations et ecarts de segment S_gra (tires independamment, quel que soit epsilon) ; S_gra traite comme covariable publique non protegee (comme D1/D4) ; aucune composition avec les autres analyses du depot ; ni PrivBayes complet ni bibliotheque de reference (ecrit a la main, `analyses/c7_dp.py`).

## Tableau par epsilon (reference d'utilite = jumeau JSON Persona GPT4.1 non protege)
| epsilon | top1 [IC95%] | perte utilite (pts) | fidelite indiv. (pts) |
|---|---|---|---|
| 0,5 | 0,012 % [0 ; 0,036] | 5,61 | +0,02 |
| 1 | 0,080 % [0 ; 0,216] | 4,01 | +0,09 |
| 3 | 0,158 % [0,012 ; 0,340] | 3,33 | +0,12 |
| 10 | 0,000 % [0 ; 0] | 3,38 | +0,04 |
| infini (non prive) | 0,024 % [0 ; 0,073] | 3,52 | +0,20 |

D4 (permutation intra-segment, notre meilleure defense) : top1 = 0,126 % [0,012 ; 0,284], perte = 1,47 pt (`c7-defense-courbe.csv`). **Ce 1,47 est une moyenne de trois composantes d'erreur (distribution, ecarts de segment, correlations), dont deux sont nulles par construction pour D4** (la permutation intra-segment preserve exactement la distribution par item et les ecarts de segment) ; le cout reel de D4 ne porte que sur les correlations inter-items et vaut **4,4 points** (`c7-defense-resultats.csv`, ligne `D4_melange` : erreur_correlations = 4,3999..., utilite_globale = 1,4666... = 4,4/3). La comparaison a un epsilon DP scalaire au tableau ci-dessus reste valide, mais 1,47 sous-estime le cout de D4 d'un facteur 3 par construction, pas par un choix de mesure equivalent chez la DP. Fidelite DP quasi nulle partout (< 0,2 pt) : aucun conditionnement par personne, meme pas par segment.

## Superposition, verdict chiffre (critere preenregistre)
Prediction dementie : a eps = 3 et 10, la perte d'utilite (3,3-3,4 pts) est a moins de 5 pts de D4, et le top-1 (0,158 %, 0 %) n'est pas superieur au notre (0,126 %) — l'issue inverse annoncee. Meme le temoin non prive (eps = infini) plafonne a 3,52 pts : le plancher vient de l'architecture (erreur_groupes ~2,3-2,9 et erreur_correlations ~4,4-4,6 quasi constantes sur toute la plage), pas du budget ; seule erreur_distribution baisse avec epsilon (9,7 a 3,2 pts).

## La reponse theorique (le coeur de la question du relecteur)
Non, la DP ne repond pas a notre modele de menace. Elle protege l'APPARTENANCE d'un individu au jeu utilise pour calculer une statistique publiee — « Alice est-elle dans l'echantillon ? ». Notre attaque suppose Alice deja connue (son profil est l'entree du jumeau) et demande si LA SORTIE conditionnee sur Alice peut lui etre reliee : une liaison d'attribut/enregistrement, pas un probleme de membership. Le generateur DP ne « resout » ce probleme qu'en refusant la tache du jumeau : il ne conditionne jamais sur un individu (fidelite ~0 a tout epsilon), donc il ne peut pas se substituer a une personne precise en recherche. Sa faible fuite est un sous-produit de cette incapacite, pas du budget choisi.

## En clair
La DP la plus simple defendable egale ou bat nos defenses sur ce tableau agrege, mais elle y arrive en ne repondant jamais a la question de l'attaque : elle ne remplace jamais une personne, elle ne publie que des statistiques de population.
