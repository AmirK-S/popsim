# C7 attaquant imparfait : préenregistrement (13 septembre 2026, AVANT tout calcul)

statut: courant
mandat: mesurer la reidentification C7 quand les donnees auxiliaires de l'attaquant se degradent (partielles, bruitees, items banals) et en situer le point de rupture
agent: Opus 5, Anthropic
ecriture: analyses/c7_attaquant_imparfait.py, resultats/c7-attaquant-imparfait-preenregistrement.md, resultats/c7-attaquant-imparfait-resultats.md, resultats/c7-attaquant-imparfait.csv
lecture_seule: tout le reste
interdits: appel payant sans GO, reseau, commit sur master, arriere-plan
cout_reel_usd: 0.0

**Écrit avant `analyses/c7_attaquant_imparfait.py` et avant le moindre chiffre.** Vérification faite
à cette minute dans l'arbre isolé `/tmp/wt-bruit` : `ls analyses/c7_attaquant_imparfait.py` et
`ls resultats/c7-attaquant-imparfait*` ne rendent rien. Aucun appel de modèle de langage, aucun
réseau, aucune recherche web, lecture seule sur `data/`. Aucun identifiant ni appariement individuel
n'est écrit : seuls des taux agrégés sortent.

Conventions de certitude : **[MESURE]** calculé ici, **[PRÉDICTION]** écrit avant de voir le chiffre.

---

## 1. La question, et pourquoi elle décide de la gravité de l'article

L'attaque C7 publiée suppose que l'attaquant détient les **vraies réponses exactes** des 2 058
candidats (`c7-resultats.md` §1 : top-1 = 20,68 % pour `JSON Persona - GPT4.1`, contre 2,13 % pour
`Demographics Only`). L'article déclare cette hypothèse mais ne la teste pas. Un attaquant réel a des
données **partielles, périmées, bruitées**.

Si l'attaque s'effondre dès la première dégradation, notre modèle de menace est de laboratoire et
l'article doit l'écrire. Si elle survit, la menace est plus grave que ce que nous publions.

## 2. Ce qui est dégradé, et ce qui ne l'est pas

**Ce qui est dégradé : les données auxiliaires de l'attaquant**, c'est-à-dire le *pool* des vecteurs
humains vague 4 contre lequel la sortie de jumeau est appariée. C'est bien sa base clients.

**Ce qui n'est PAS dégradé : la sortie de jumeau publiée** (60 items, complète). Elle est publique par
hypothèse ; la dégrader répondrait à une autre question (celle de la défense, traitée par `c7_defense`).

## 3. Protocole, et le piège du bassin

- Jeu : Twin-2K-500, 2 058 personnes, **60 items toujours renseignés** (`items_communs`), cible
  `humains vague 4`. Candidat : `JSON Persona - GPT4.1` (le plus fort de `c7-resultats.md`).
- **Bassin rigoureusement constant entre toutes les conditions** : pool = les 2 058 humains, attaqués
  = les 2 058 mêmes personnes, mêmes 60 items de départ. Le top-1 dépend mécaniquement de la taille
  du bassin (2,13 % à 2 058, 9,20 % à 200, 13,29 % à 120 pour la seule baseline démographique) : ce
  piège a déjà coûté deux conclusions à ce projet, il ne sera pas repris. Rien dans ce chantier ne
  change le bassin ; seule la **qualité** de l'information de l'attaquant varie.
- **Baseline du même bassin ET de la même dégradation** : à chaque niveau, `Demographics Only -
  GPT4.1-mini` attaque **le pool exactement aussi dégradé**, avec le même masque et le même bruit
  (mêmes graines). Comparer un top-1 dégradé à une baseline non dégradée serait la même erreur sous
  un autre nom. La baseline n'est jamais fournie en argument, elle est recalculée dans chaque
  condition.
- **Contrôle préalable obligatoire** : `c7_controle_interpretabilite.controle_avant_interpretation`
  est appelé sur la condition **non dégradée** (2 058 personnes, 60 items) avant toute interprétation.
  S'il échoue, rien n'est interprété. Ce contrôle recalcule lui-même la baseline sur le bassin non
  dégradé ; les conditions dégradées utilisent la règle de décision **identique** (voir §5) appliquée
  à la baseline dégradée, parce que la fonction de contrôle ne prend pas de pool dégradé en argument.
- **Réutilisation sans réimplémentation** : `c7_reidentification.rangs_attaque`, `items_communs`,
  `graine_nom`, `REF_V4`, `DEMO` ; `a2_commun.distance_hamming` et `bootstrap_personnes` ;
  `t1_commun.charger` et `ecrire`. Aucun script existant n'est modifié.

## 4. Les quatre dégradations

**D1 — réponses partielles.** L'attaquant ne connaît que `p` des 60 items, `p` ∈ {75 %, 50 %, 25 %,
10 %} (soit 45, 30, 15, 6 items). Tirage **aléatoire et indépendant par candidat** (une base clients
n'a pas les mêmes champs pour tout le monde), mais **le même nombre d'items pour tous** : à masque de
taille variable, les candidats à peu d'items obtiendraient un accord artificiellement élevé (le
dénominateur de Hamming est le nombre d'items communs), ce qui fabriquerait un effet parasite.
**3 répétitions** (graines distinctes) par niveau ; le taux rapporté est la moyenne des répétitions
et l'intervalle est le bootstrap sur les personnes (2 000 tirages) de la répétition médiane.

**D2 — réponses bruitées.** Une fraction `q` ∈ {5 %, 10 %, 20 %, 30 %} des réponses connues est
fausse. La valeur fausse est tirée dans la **marginale empirique de l'item conditionnée à être
différente de la vraie** — une réponse périmée ressemble à une réponse plausible, pas à du bruit
uniforme. Je ne prétends pas que ce choix soit neutre pour l'attaquant : il est déclaré ici, avant
calcul, comme le plus réaliste, et une erreur tirée uniformément serait une variante défendable.
3 répétitions par niveau.

**D3 — les deux combinés.** Grille {75 %, 50 %, 25 %} × {10 %, 20 %, 30 %}, 3 répétitions, plus le
point d'intérêt public {50 % d'items, 10 % d'erreurs}.

**D4 — items les plus courants seulement.** L'attaquant ne connaît que les `k` items les **plus
banals**, ceux qu'on trouve dans n'importe quelle base commerciale : opérationnalisé comme les `k`
items de **plus faible entropie** de la distribution des réponses humaines vague 4 (distribution la
plus concentrée = réponse la plus prévisible = information la plus faible). `k` ∈ {45, 30, 15, 6},
donc directement comparable à D1 au même nombre d'items. Aucune répétition nécessaire (le choix est
déterministe) ; l'écart à D1 au même `k` est la quantité d'intérêt.

## 5. Règle de décision, écrite avant de voir un chiffre

Une condition est dite **au-dessus de la baseline** si la borne basse de l'IC bootstrap à 95 % du
candidat est **strictement supérieure** à la borne haute de l'IC de la baseline démographique du
**même bassin et de la même dégradation**. C'est exactement la règle de
`c7_controle_interpretabilite` (IC non chevauchants, pas une comparaison de points), choisie parce
que le sinistre que ce projet a déjà subi est un faux positif.

**Le point de rupture** est la **première** dégradation, en allant du moins dégradé au plus dégradé,
à laquelle cette condition cesse d'être remplie.

## 6. Prédictions chiffrées [PRÉDICTION]

Référence non dégradée attendue : candidat ≈ 20,7 %, baseline ≈ 2,1 %.

- **[P1]** D1 à 75 % d'items : top-1 candidat entre **15 % et 20 %**, au-dessus de la baseline.
- **[P2]** D1 à 50 % : entre **8 % et 15 %**, au-dessus de la baseline.
- **[P3]** D1 à 25 % : entre **3 % et 8 %**, encore au-dessus de la baseline.
- **[P4]** D1 à 10 % (6 items) : **sous 2 %**, et IC chevauchant celui de la baseline.
  **Point de rupture prédit pour D1 : entre 25 % et 10 % d'items connus, donc autour de 10 %.**
- **[P5]** D2 à 30 % d'erreurs : top-1 **au-dessus de 5 %** et toujours au-dessus de la baseline —
  **aucun point de rupture sur le bruit seul dans la plage testée.** Le bruit dégrade moins que la
  perte d'items parce que 60 items en accord partiel restent un vecteur très spécifique.
- **[P6]** D3 au point public {50 % d'items, 10 % d'erreurs} : top-1 entre **5 % et 12 %**, au-dessus
  de la baseline. Je prédis donc explicitement que la phrase forte « il suffit de connaître la moitié
  des réponses, même avec 10 % d'erreurs, pour identifier **six personnes sur dix** » sera **fausse**
  d'un ordre de grandeur : ce sera plutôt **une personne sur dix à une sur vingt**, ce qui reste
  cent fois le hasard (0,049 %) et plusieurs fois la baseline.
- **[P7]** D4 (items les plus banals) à `k` égal : top-1 **inférieur d'au moins un tiers en relatif**
  à D1 au même `k`, et rupture **plus précoce** — dès `k` = 15 items banals.
- **[P8]** La baseline démographique se dégrade **elle aussi**, et dans les mêmes proportions
  relatives : l'écart candidat/baseline en ratio se maintiendra plus longtemps que l'écart absolu.
  Une rupture peut donc arriver par **effondrement du candidat** ou par **chevauchement des IC quand
  les deux tombent dans le bruit** ; les deux seront distinguées dans le rapport.

## 7. Ce qui me ferait conclure que l'attaque est FRAGILE, et affaiblir l'article

Écrit avant calcul, et il s'agit d'un livrable de pleine valeur, pas d'un échec :

1. **Rupture dès 75 % d'items** ou **dès 5 % d'erreurs** : la menace n'existe que sous connaissance
   quasi parfaite. L'article devrait alors écrire que son modèle d'attaquant est **de laboratoire**.
2. **Chute de plus de la moitié en relatif** entre 100 % et 75 % d'items : la courbe est une falaise,
   pas un plateau ; toute affirmation sur un « attaquant réel » devrait être retirée.
3. **D4 sous la baseline dès `k` = 45** : l'attaque n'exploite que des items rares, donc des données
   qu'aucune base commerciale ne détient — la menace serait théorique.

Si l'un des trois se produit, ce rapport propose **le retrait des affirmations correspondantes**, et
c'est ce qui sera écrit, même si cela coûte le résultat le plus vendeur du chapitre.

## 8. Ce qui serait au contraire une aggravation

Si le point de rupture n'est **atteint dans aucune** des conditions testées — c'est-à-dire si même
{25 % d'items, 30 % d'erreurs} reste significativement au-dessus de la baseline — alors l'hypothèse
« vraies réponses exactes » n'est **pas** la condition de l'attaque, et l'article sous-estime
aujourd'hui sa propre menace. Ce serait le résultat le plus important du papier et il serait écrit
comme tel.

## 9. Budget de calcul et réductions déclarées d'avance

Machine locale, aucun coût d'API. Coût réel : 0,00 USD.

`rangs_attaque` est appelée deux fois (candidat + baseline) par condition et répétition, soit de
l'ordre de 70 attaques sur 2 058 × 2 058. **Réductions déclarées ici, avant calcul** : nombre de
tirages de départage des ex æquo ramené de 20 à **5** (il ne sert qu'à casser les égalités de rang,
son effet sur un taux agrégé est du troisième ordre), bootstrap maintenu à **2 000**, répétitions
limitées à **3**. Toute réduction supplémentaire décidée en cours de route sera écrite dans le
rapport de résultats, avec son motif.
