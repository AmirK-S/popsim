# Rétractation de la comparaison DP, et ce qu'elle atteint dans les affirmations sur D4

statut: courant
mandat: Propager la rétractation de la comparaison « la DP coûte plus cher que D4 » dans les fichiers de résultats et le registre, établir mesures à l'appui quelles affirmations du manuscrit sur D4 deviennent indéfendables et lesquelles survivent, et préparer la fiche de report — sans toucher au manuscrit
agent: Claude Opus 5, sous-agent correction rétractation DP
ecriture: resultats/retractation-dp-d4-2026-09-13.md, resultats/c7-dp-resultats.md (en-tête et section 0 seulement), resultats/c7-dp-courbe-combinee.csv, resultats/cout-defense-synthese-2026-09-13.md (§5 seulement), resultats/registre-chiffres.csv, resultats/c7-d4-adaptatif.csv, analyses/c7_d4_adaptatif.py
lecture_seule: tout le reste
interdits: appel payant, réseau, commit sur master, arrière-plan, toute modification de article/manuscrit.md (un autre agent en est propriétaire)
cout_reel_usd: 0.00

RETRACTE: resultats/c7-dp-resultats.md

Le rapport ci-dessus est retiré en entier ; la section 5 de
`resultats/cout-defense-synthese-2026-09-13.md` est retirée en section, le reste de ce
rapport n'étant pas concerné ; et `resultats/c7-dp-courbe-combinee.csv` porte désormais,
ligne à ligne, `statut = retracte` avec son motif. Rien n'est supprimé nulle part.
Fait foi partout : `resultats/audit-comparaison-dp-2026-09-13.md`.

---

## 1. Ce qui est rétracté, et où

| objet | portée | ce qui est retiré | ce qui reste |
|---|---|---|---|
| `resultats/c7-dp-resultats.md` | rapport entier | le tableau par epsilon, la ligne de comparaison à D4, le verdict « Superposition », le « En clair » | la section « La réponse théorique » (appartenance ≠ liaison attribut-personne), qui ne dépend d'aucun chiffre du tableau |
| `resultats/cout-defense-synthese-2026-09-13.md` | §5 seulement | le tableau DP↔D4 et la phrase « D4 domine la DP composante par composante à protection égale ou supérieure » | §1 à §4 et §6 (tâches en aval, courbe de réglage), qui ne dépendent pas de la DP ; le §4 est relu, pas retiré (§5 bis) |
| `resultats/c7-dp-courbe-combinee.csv` | 19 lignes sur 19 | la colonne `perte_utilite_points` comme échelle unique : elle concatène des lignes DP mesurées humains-ajustés-contre-jumeau et des lignes de défense mesurées jumeau-contre-jumeau | les valeurs elles-mêmes, conservées avec `statut`, `fait_foi`, `motif_retractation` ; les lignes de défense restent lisibles dans `c7-defense-courbe.csv`, jamais ici |
| `resultats/registre-chiffres.csv` | 2 lignes rétractées ou déclassées, 1 rétractée, 3 ajoutées | voir §2 | aucune ligne supprimée |

## 2. État du registre

- `defense-d4-cout-groupes` (0,0) → **`retracte`**, avec sa référence de remplacement. Motif :
  ce 0,0 n'est pas un coût nul, c'est la republication exacte de la statistique.
- `defense-d4-cout-correlations` (4,4) → **`provisoire`**. Motif : tirage unique, alors que
  sur 10 graines la valeur vaut 4,373 ± 0,058 (étendue [4,254 ; 4,433]) et que l'amplitude à
  détruire vaut 4,317 — « 4,4 » signifie « toute la structure détruite », pas un coût
  comparable à celui d'un autre mécanisme.
- `twin-d4-top1-residuel` (0,13 %) → **`provisoire`**, valeur inchangée, description amendée :
  attaque naïve non adaptative, à ne jamais citer seule comme le taux de D4 ; et sur
  10 tirages de permutation la moyenne est 0,096 % (étendue [0,000 ; 0,187]), le 0,13 %
  publié étant un tirage unique en haut de cette étendue.
- Trois lignes **ajoutées** : `defense-d4-top1-adaptatif-s1` (0,29 % [0,10 ; 0,53], courant),
  `defense-d4-top1-opinion-naif` (0,245 % [0,073 ; 0,471], courant),
  `defense-d4-republication-multiensemble` (100 %, 1 560/1 560, courant).
- Aucune ligne DP n'existait au registre : les 3,33 / 3,38 / 0,158 % du manuscrit n'y ont
  jamais été déclarés. C'est en soi un constat (§6).
- Porte `outils/portes/registre_chiffres.py --registre-seul` : OK, 36 grandeurs.

## 3. Ce que nous avons remesuré nous-mêmes

`analyses/c7_d4_adaptatif.py` → `resultats/c7-d4-adaptatif.csv`. Graine 20260913, bassin
constant entre conditions (2 058 personnes, pool 2 058, mêmes fonctions d'attaque et de
bootstrap), aucune donnée individuelle imprimée, aucun appel de modèle.
`c7_controle_interpretabilite.controle_avant_interpretation` passé **avant toute
interprétation, jeu d'items par jeu d'items**, baseline démographique recalculée sur le
bassin exactement attaqué : 60 items 20,65 % contre 2,15 % ; 40 items d'achat 33,02 %
contre 6,01 % ; 20 items d'opinion 0,27 % contre 0,00 %. Les trois passent — y compris le
bloc d'opinion, dont on aurait pu croire qu'il ne porte rien.

**F1 confirmée, et elle est exacte.** 1 560 couples segment × item sur 1 560 conservés à
l'identique (39 segments de taille ≥ 2 ; l'audit annonçait 1 600 en comptant les
40 segments, dont un singleton que `defense_d4` saute). D4 republie l'histogramme de chaque
item dans chaque segment, sans bruit.

**F5 confirmée, et par le bas.** Top-1 monde fermé, l'attaquant choisissant ses colonnes :

| publication | 60 items | 40 items d'achat | 20 items d'opinion |
|---|---|---|---|
| jumeau non protégé | 20,639 % [18,960 ; 22,192] | 33,076 % [31,244 ; 34,986] | 0,260 % [0,080 ; 0,484] |
| D4, tel que publié | 0,138 % [0,010 ; 0,306] | 0,049 % [0,000 ; 0,146] | **0,245 % [0,073 ; 0,471]** |
| D4, 10 tirages de permutation | 0,096 % (étendue [0,000 ; 0,187]) | 0,053 % ([0,000 ; 0,092]) | 0,257 % ([0,248 ; 0,272]) |

Trois lectures, et pas une de plus :

1. Sur les 20 items d'opinion, D4 et le jumeau **non protégé** sont indiscernables
   (0,245 % contre 0,260 %, intervalles quasi confondus). Ce n'est pas une surprise et ce
   n'est pas un échec de D4 : par construction, D4 ne touche pas ce bloc. C'est la mesure
   de ce que la défense ne protège pas.
2. Le 0,13 % publié est un tirage unique **en haut** de l'étendue des 10 réplicats
   (moyenne 0,096 %). Sa graphie est conservatrice, mais elle n'a pas de support en
   réplicats : d'où son passage à `provisoire`.
3. Le taux sur les 20 items d'opinion, lui, ne dépend **pas** du tirage de permutation
   (écart-type 0,009 pt) : c'est le chiffre le plus stable des trois, et c'est celui qui
   plafonne la défense.

**Ce que nous ne concluons pas.** La conséquence « un adversaire connaissant les |g|−1
autres membres d'un segment reconstitue les 40 réponses de la cible » est vraie **par
construction**, pas par mesure : nous ne l'avons pas mise en œuvre, et elle suppose un
adversaire que nos données ne fournissent pas. Sans aucune connaissance latérale, la fuite
directement lisible dans la sortie D4 est **petite** : 207 cellules sur 82 280 (0,25 %) ont
un multi-ensemble dégénéré, 0,8 % des personnes en ont au moins une. Ce second chiffre ne
doit pas être présenté comme la fuite de D4 ; il borne ce qu'un lecteur passif apprend.

## 4. Verdict sur les affirmations du manuscrit relatives à D4

### Indéfendables en l'état

1. **« per-item distribution and between-segment differences being preserved exactly, by
   construction »** présenté comme une propriété d'utilité (§6, l. 794-795), et
   **« 0.0 points on the per-item distribution, 0.0 points on group differences »**
   (l. 797-798). Vrai arithmétiquement, trompeur en substance : ces zéros sont la
   republication exacte de l'histogramme intra-segment, donc la protection non fournie.
   Toute phrase qui les lit comme un coût évité doit être reformulée.
2. **Toute la comparaison à la DP** (§6.2, l. 831-846) et **la ligne 14 du tableau des
   prédictions** (l. 900). Référence désappariée, budget qui ne contribue à rien,
   mécanisme homme de paille, effectifs de 0 à 3 personnes, intervalles recouvrants.
3. **« its top-1 (0.158 %, 0.000 %) is not above ours (0.13 %) »** (l. 838-839). Les deux
   membres sont mesurés sous des attaquants différents : le nôtre est contraint aux
   60 items. Sous le meilleur attaquant que nous ayons mesuré de chaque côté, l'ordre
   s'inverse (D4 0,29 % contre DP ≤ 0,085 %).
4. **« even on correlations, DP is slightly more expensive (4.47-4.59 against 4.40) »**,
   partout où cet écart est présenté comme un avantage. L'amplitude à détruire vaut 4,317 :
   les trois valeurs sont le même nombre, « tout est détruit ».
5. **Le résumé et l'introduction** (l. 42-43, l. 169-174) : « reduces closed-world top-1
   from 20.7 % to 0.13 % » met en tête le taux non adaptatif, et « Against our own
   preregistered prediction, differential privacy is *not* dominated by it on aggregate
   utility » repose sur le tableau retiré.

### Qui survivent, et pourquoi

- **Le taux sous attaquant adaptatif, 0,29 % [0,10 ; 0,53]** (§6.1). Il est mesuré, il est
  déjà publié, et notre remesure indépendante le corrobore **par le bas** (0,245 %). Il
  n'est atteint par aucune des failles de l'audit.
- **La réserve qui borne la garantie** (l. 826-829 : le résidu vient entièrement des
  20 items d'opinion, « 0.29 % is not a bound on the defense in general »). Non seulement
  elle survit, mais nos mesures la renforcent : sur ce bloc, D4 et le jumeau non protégé
  sont indiscernables.
- **Le coût de 4,4 points sur les corrélations et l'aggravation de 68,1 % de l'écart aux
  humains** (§6). Ils ne sont pas atteints par la critique de la DP. Réserve à porter :
  tirage unique, 4,373 ± 0,058 sur 10 graines.
- **§6.3, le coût pour l'analyste en aval** (deux coefficients perdent leur significativité,
  45 % des loadings de l'axe 1 inversés). Aucune dépendance à la DP.
- **La ligne 13 du tableau des prédictions** (P3 réfutée dans le sens favorable à la
  défense, « never above 1 % ») : factuellement exacte. Mais elle ne doit plus voisiner avec
  une phrase suggérant que D4 est de ce fait plus sûr que la DP.
- **L'ascendance PRAM** (§2.6) et le fait que D4 n'est pas nouveau.

### Ce qui manquait et doit être ajouté

D4 **n'offre aucune garantie formelle**. Le manuscrit ne le dit nulle part en toutes
lettres. C'est l'ajout le plus important de cette passe.

## 5. Faut-il publier un nouveau taux à la place de 0,05 % et 0,13 % ?

**Non pour le chiffre, oui pour la hiérarchie.** Il n'y a pas de nouveau nombre à minter :
le taux à publier existe déjà, il vaut **0,29 % [0,10 ; 0,53]** (stratégie adaptative S1,
`c7-attaquant-fort.csv`), il est plus élevé — donc plus conservateur — que notre remesure
indépendante (0,245 % [0,073 ; 0,471]), et il est déjà au §6.1. Ce qui doit changer, c'est
lequel des trois chiffres est en tête :

- **0,29 %** devient le taux de D4, au résumé, en §6 et partout où D4 est comparé à autre
  chose. C'est le taux sous le meilleur attaquant que nous ayons mesuré.
- **0,13 %** reste, nommé pour ce qu'il est : attaque naïve, non adaptative, contrainte aux
  60 items, tirage unique de permutation.
- **0,05 %** (S3 seule) ne doit **jamais** être cité comme « le taux sous attaquant
  adaptatif » : c'est la plus faible des trois stratégies testées. Le manuscrit le présente
  déjà correctement, entre parenthèses ; il faut seulement qu'il n'en sorte pas.

Et la phrase qui manque : aucun de ces taux n'est une borne. Ce sont les taux des attaques
que nous avons construites, contre un mécanisme sans garantie formelle.

## 6. Fiche de report pour le manuscrit (passes T4 et T5)

Sept endroits. Le manuscrit n'est pas modifié par cette passe.

### R1 — Résumé, l. 42-43

*Actuel :* « Finally, a 1998 mechanism (PRAM) applied to twins reduces closed-world top-1
from 20.7 % to 0.13 % at a measured cost of 4.4 points on inter-item correlations, holding
at 0.29 % against an adaptive attacker who knows the mechanism. »

*Cible :* « Finally, a 1998 mechanism (PRAM) applied to twins brings closed-world top-1
from 20.7 % to 0.29 % [0.10 ; 0.53] against the best attacker we measured — one who knows
the mechanism and attacks the block it leaves untouched — at a measured cost of 4.4 points
on inter-item correlations. It carries no formal guarantee: it republishes each item's
within-segment histogram exactly, so its zero distribution and group error are that
republication, not a cost avoided. »

### R2 — §1, contribution (6), l. 169-174

*Actuel :* « … tested against an attacker who knows how the defense works (§6). Against our
own preregistered prediction, differential privacy is *not* dominated by it on aggregate
utility (§6.2). »

*Cible :* « … tested against an attacker who knows how the defense works, and reported with
what it does not protect: it offers no formal guarantee, and it republishes the
within-segment item histogram exactly (§6). We preregistered a comparison with differential
privacy and withdraw it: our DP implementation was a straw man, measured against a
mismatched reference, and at eps = infinity — with no privacy at all — the cost was already
the same. We claim no superiority over differential privacy (§6.2). »

### R3 — §6, l. 793-798

*Actuel :* « … brings closed-world top-1 from **20.7 % [19.0 ; 22.4]** to **0.13 %
[0.01 ; 0.28]**, per-item distribution and between-segment differences being preserved
**exactly, by construction**, as PRAM predicts. » puis « Reported by component: 0.0 points
on the per-item distribution, 0.0 points on group differences, and **4.4 points on
inter-item correlations**. »

*Cible :* « … brings closed-world top-1 from **20.7 % [19.0 ; 22.4]** to **0.13 %
[0.01 ; 0.28]** against the naive, non-adaptive attack, and to **0.29 % [0.10 ; 0.53]**
against the best attacker we measured (§6.1) — the figure we report as the defense's rate.
Per-item distribution and between-segment differences are preserved **exactly, by
construction**, as PRAM predicts, and that exactness is also the mechanism's central
limitation: shuffling item by item within a segment leaves the within-segment multiset of
each item identical (1 560 of 1 560 segment × item pairs), so D4 republishes each item's
within-segment histogram without noise. An adversary who knows the other members of a
segment recovers the target's 40 answers by difference. **D4 offers no formal privacy
guarantee.** » puis « Reported by component: **0.0 points on the per-item distribution and
0.0 points on group differences — which is the republication just described, not a cost
avoided** — and **4.4 points on inter-item correlations** (4.373 ± 0.058 over ten seeds;
the amplitude to be destroyed is 4.317, so this component is destroyed in full). »

### R4 — §6.1, l. 819-821

*Actuel :* « Top-1 goes from 0.13 % (naive) to **0.24 %** under the recalibrated strong
attack, and the **adaptive** attacker plateaus at **0.29 %** (strategy S1, leaving the
20 opinion items intact; segment-invariant strategy S3 alone 0.05 %). »

*Cible :* inchangé quant aux chiffres, plus une phrase : « On those 20 opinion items alone,
the defended and the **undefended** twin are indistinguishable (0.245 % [0.073 ; 0.471]
against 0.260 % [0.080 ; 0.484]): the residue is not a residue of the defense, it is the
part of the publication the defense never touches. None of these rates is a bound; they are
the rates of the attacks we built. »

### R5 — §6.2 en entier, l. 831-846

*Actuel :* tout le paragraphe, de « We preregistered the prediction … » à « … only
distribution error falling with epsilon (9.7 → 3.2 points). »

*Cible :* le §8 de `resultats/audit-comparaison-dp-2026-09-13.md`, **repris in extenso**,
traduit sans rien y ajouter. En français dans l'audit, il dit : nous n'avons pas comparé le
coût de la DP à celui de D4 ; sur ces 2 058 personnes un générateur à marginales d'item
indépendantes coûte 0,9 à 1,0 point de distribution et 2,7 à 2,9 points sur les écarts
entre segments, qu'il soit bruité à eps = 3, à eps = 10, ou pas bruité du tout, la
contribution marginale du budget étant de 0,1 à 0,3 point à eps = 3 ; sur les corrélations
D4 (4,37) et le générateur DP (4,50-4,55) détruisent l'un comme l'autre la totalité de la
structure, dont l'amplitude vaut 4,32 ; D4 n'offre aucune garantie formelle et republie
exactement l'histogramme intra-segment ; notre top-1 mesure un attaquant fixé, et un
attaquant qui écarte le bloc brouillé porte la fuite de D4 de 0,13 % à 0,24 %, au-dessus du
générateur DP à eps = 3 (0,09 %), ces taux valant 0 à 3 personnes sur 2 058 ; **nous ne
revendiquons aucune supériorité de D4 sur la confidentialité différentielle**, seulement un
compromis différent, sans garantie, contre l'attaque particulière que nous avons construite.

Ce qui **reste** du §6.2 : le plancher architectural (le témoin non privé coûte autant), qui
cesse d'être une note de bas de page pour devenir le résultat de la section. Et, déplacée
depuis `c7-dp-resultats.md`, la réponse théorique : la DP protège l'appartenance, notre
attaque porte sur la liaison attribut-personne.

### R6 — Tableau des prédictions, ligne 14, l. 900

*Actuel :* « **Refuted.** eps = 3/10 lose 3.33/3.38 points on the composite utility index
against D4's 1.47 on that same index (never D4's cost, §6); top-1 0.158 % / 0.000 % against
0.13 % | `c7-dp-resultats.md` »

*Cible :* « **Withdrawn, not decided.** The comparison that produced this verdict is
retracted: the DP generator was fitted on the humans and scored against the twin, and at
eps = infinity — no privacy at all — the cost was already the same. We report no verdict on
this prediction. | `audit-comparaison-dp-2026-09-13.md` »

Conséquence de décompte, à répercuter l. 891-905 : la ligne 14 sort des quatorze réfutations
et devient une prédiction **retirée**. Le décompte publié (« Seventeen rows, fourteen
refutations, two inconclusive, one untestable ») devient **treize réfutations, deux
non concluantes, une non testable, une retirée**. Toutes les occurrences de « fourteen
preregistered predictions were refuted » (dont le résumé, l. 38-39) suivent.

### R7 — §8, défenses recommandées, point (e), l. 1081-1085

*Actuel :* « (e) Within-segment shuffling (§6), with its real cost stated: 4.4 points on
inter-item correlations, a 68.1 % worsening of the gap to human correlations
(5.775 → 9.709), and the loss of every inter-item analysis downstream (§6.3) — it holds at
0.29 % against an attacker who knows the mechanism, but only for a split that shuffles the
informative block (§6.1). »

*Cible :* identique, plus, avant le tiret : « — and with what it does not provide: **no
formal guarantee**, and exact republication of each item's within-segment histogram, so an
adversary who knows a segment's other members recovers the target's answers. It holds at
0.29 % … ». Et le point (f) sur la DP doit perdre toute formulation qui la présente comme le
choix le plus coûteux.

### Renvois de fichiers

Partout où le manuscrit ou `article/article-synthese.md` renvoie à `c7-dp-resultats.md`,
substituer `audit-comparaison-dp-2026-09-13.md`. `c7-dp-courbe-combinee.csv` ne doit
alimenter aucune figure.

## 7. La leçon de processus, en trois lignes

1. Le préenregistrement ne disait pas **lequel des deux objets** — les humains ou le jumeau —
   le générateur DP est censé protéger ; une ligne de plus dans
   `c7-dp-preenregistrement.md` et le désappariement humains↔jumeau était impossible à écrire.
2. Le témoin eps = infini était **dans le CSV livré** et disait déjà que le coût était le même
   sans aucune confidentialité : aucune porte n'exige qu'un témoin présent dans les données
   soit lu avant la rédaction du verdict, et personne ne l'a lu.
3. Aucun des chiffres de la comparaison (3,33, 3,38, 0,158 %) n'a jamais été déclaré au
   registre : une comparaison entre deux mécanismes a été transmise au responsable alors que
   la moitié de ses grandeurs n'existait dans aucun fichier opposable — c'est le seuil qui
   manque, pas la vertu.
