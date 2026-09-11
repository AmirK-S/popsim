# Brainstorm angle C, « idées folles que personne ne mesure », 11 septembre 2026

Lecture seule du dépôt ; 14 requêtes web (moteur généraliste, arXiv, ACM, PMC) ; aucun appel de modèle.
Exclu d'office : tout ce que la veille du 11 septembre range en « fait » ou « partiellement fait » (dissociation
agrégat / apparié, permutation de persona, base contre post-entraîné, non-déterminisme), les deux moonshots
enterrés (mémorisation d'un choc SCE, modèles chronologiques contre l'opinion suivante), et les vingt lignes de
`MOONSHOTS.md` (second ordre, bande humaine, qui bouge, seuils de révélation, Kuran, marché simulé, tournoi de
théorie de l'esprit). Ce que les pré-mortems ont tué : une mesure aveugle par construction à l'effet visé, un seuil
absolu sous le meilleur nul, des fenêtres qui diffèrent par autre chose que le facteur testé, une antériorité non
LLM préenregistrée. Chaque idée ci-dessous nomme donc son **tueur** : le comparateur bête qui, s'il fait aussi bien,
ferme le dossier.

Notation : [MESURE] chiffre relevé dans le dépôt ; [CONFIRMÉ] source ouverte ; [PARI] prédiction avant calcul.
Données locales vérifiées ce matin : Twin-2K-500, 2 058 personnes présentes en vague 4 (toutes avec plus de 20
réponses) [MESURE] ; 13 jeux de sorties LLM des auteurs dans `data/twin2k500/llm_specs/` (gpt-4.1, gpt-4.1-mini,
gemini-flash-2.5, fine-tune 500, démographies seules) [MESURE] ; GSS panel 2010-2014, 87 colonnes `nat*` dont les
formes Y (`natfarey`, `natracey`, `natcityy`…) présentes aux trois vagues [MESURE] ; **aucune paradonnée de temps
de réponse en local** (le CSV « formatted » de l'OSF n'est pas téléchargé) [MESURE].

---

## 1. Psychométrie sans répondants : le désaccord entre simulateurs prédit la fiabilité de retest d'un item

**Intuition.** Un item que treize configurations de jumeaux prédisent différemment pour la même personne est un
item sur lequel la personne elle-même se contredit deux semaines plus tard. La « non-attitude » de Converse serait
lisible dans la variance entre simulateurs, avant tout retest humain.

**Whoa.** Le retest coûte une vague entière ; si la variance entre configurations, calculable sans un seul humain
de plus, classe les items par fiabilité, la psychométrie gagne un instrument de pré-test gratuit — et, à l'inverse,
les benchmarks de jumeaux devraient être évalués item par item contre ce plafond, pas en moyenne.

**Premier test (< 48 h, 0 appel de modèle).** Sur les 88 items de holdout repris en vague 4 : (i) rtt par item
entre vagues 1-3 et vague 4 ; (ii) désaccord par item = variance entre les 13 configurations des auteurs, à personne
fixée, moyennée sur les personnes ; (iii) Spearman entre (ii) et 1 − rtt. Ajouter un prédicteur zéro-donnée : un
LLM local note chaque item de 1 à 5 en « attitude cristallisée / réponse inventée sur place ».
[PARI] Spearman(désaccord, 1 − rtt) = 0,45 [0,25 ; 0,60] ; note zéro-donnée à 0,30.
**Tueur.** La dispersion humaine de l'item (variance des réponses en vagues 1-3) et la longueur de l'échelle
prédisent trivialement les deux : si le désaccord n'ajoute rien après contrôle de ces deux quantités (Spearman
partiel < 0,15), l'idée est morte. Second tueur : les 13 configurations partagent gpt-4.1-mini pour 11 d'entre
elles, donc « désaccord » mesure surtout la sensibilité au format d'invite ; répliquer avec Qwen3-4B, gpt-oss-20b
et Llama-3.1-8B (3 × 88 items × 300 personnes ≈ 80 000 appels courts, une nuit).
**Coût.** Une journée, 0 €.

**Antériorité.** « Psychometric Item Validation Using Virtual Respondents » (arXiv 2507.05890) simule des répondants
pour valider des items, mais ne rapporte pas le désaccord entre simulateurs à un retest humain ; « Assessing the
Reliability of Persona-Conditioned LLMs » (WWW Companion 2026) mesure la fiabilité du LLM, pas celle de l'item.
Rien de trouvé sur « désaccord entre simulateurs → rtt humain ». **Neuf, forme exacte.**

**Probabilité.** 35 % que le signal survive au tueur ; 70 % qu'il existe brut.

---

## 2. Le jumeau bat la personne : prédire la réponse future mieux que la réponse passée de l'intéressé

**Intuition.** Le retest humain vaut 0,536 sur Twin-2K-500 [CONFIRMÉ, Ahn et al.] : la réponse d'hier est un
prédicteur médiocre de la réponse de demain. Un jumeau qui intègre 500 réponses lisse le bruit du jour ; sur les
items les moins fiables, il pourrait prédire la vague 4 mieux que la propre réponse de la personne en vague 1-3.

**Whoa.** « Un modèle vous connaît mieux que votre réponse d'il y a quinze jours » renverse la hiérarchie
implicite de tout le champ, où le retest est le plafond. Si c'est vrai sur un sous-ensemble d'items nommés, la
notion de « plafond » saute pour ces items.

**Premier test (< 48 h, 0 appel).** Pour chaque item de holdout, trois prédicteurs de la vague 4 : (a) la réponse
vague 1-3 de la personne ; (b) la même, rétrécie vers la moyenne d'item par la formule de Kelley
(rtt·x + (1 − rtt)·x̄) ; (c) la meilleure configuration de jumeau. Erreur absolue moyenne par item, IC bootstrap
sur les personnes. Réplique GSS à 4 ans (2010 → 2014), où rtt des attitudes tombe vers 0,5 [MESURE, a12].
[PARI] (c) bat (a) sur 15 à 25 % des items, presque tous à rtt < 0,45 ; (c) bat (b) sur moins de 5 % des items.
**Tueur.** Kelley (b) : c'est la régression vers la moyenne, pas la connaissance de la personne. Second tueur :
XGBoost sur les autres réponses de la même personne (l'équivalent de Peng et al.), qui utilise la même
information que le jumeau sans modèle de langage. Si (c) ne bat pas XGBoost, le résultat est « la statistique bat
la personne », déjà connu.
**Coût.** Une journée, 0 € ; GSS avec Qwen3-4B, une nuit.

**Antériorité.** Wang et al. 2609.07987, Peng et al., Toubia et al. rapportent 87-90 % du retest, jamais un
dépassement item par item ; aucune comparaison trouvée « jumeau contre réponse antérieure de la même personne »
après rétrécissement. **Neuf**, mais la borne de Kelley rend la victoire improbable.

**Probabilité.** 10 % (contre Kelley et XGBoost) ; 50 % (contre la réponse brute, résultat « manuel »).

---

## 3. Le Turing inversé : les humains que le détecteur prend pour des IA sont les meilleurs répondants

**Intuition.** Les détecteurs de répondants synthétiques (i3, a44, ceux de Prolific et CloudResearch) repèrent la
compression et la cohérence. Or les humains attentifs et stables sont, eux aussi, compressés et cohérents. Le
faux positif du détecteur ne serait pas aléatoire : il ciblerait les répondants à fort retest.

**Whoa.** Pour un institut, cela veut dire qu'un nettoyage anti-IA supprime en priorité ses meilleurs panélistes et
laisse les bruyants ; pour un chercheur, que « cohérence » n'est pas un marqueur d'IA mais un marqueur de qualité,
et que les deux distributions se chevauchent par le haut.

**Premier test (< 48 h, 0 appel).** Classifieur humain contre jumeau sur les vecteurs de réponses aux items de
holdout (régression logistique ou le détecteur i3 réutilisé), validation croisée, score « IA-like » attribué à
chaque humain hors pli. Corréler ce score avec le rtt individuel (vagues 1-3 contre vague 4). Comparer le décile
supérieur au reste.
[PARI] rtt du décile « le plus IA » = rtt médian + 0,10 [0,05 ; 0,15] ; les 5 % « les plus IA » ont un rtt de 0,65.
**Tueur.** La distance à la moyenne d'item : si le score IA-like n'est que « typicité » (corrélation > 0,8 avec la
distance à x̄ par item) et que la typicité prédit le rtt à elle seule, on a redécouvert que les gens typiques sont
stables. Il faut que le score conserve un lien au rtt après contrôle de typicité et de style extrême (a9 fournit
déjà les indices de style [MESURE]). Second tueur : les taux de faux positifs revendiqués (0,6 % chez Prolific
[CONFIRMÉ]) sont mesurés sur des agents, pas sur des humains cohérents ; il faut le dire, pas le contredire.
**Coût.** Une journée, 0 €.

**Antériorité.** CloudResearch (blog 2025) note que les LLM « tiennent un persona cohérent » là où les humains
médiocres se contredisent ; arXiv 2510.24594 et 2607.00403 mesurent des faux positifs globaux, pas leur structure.
Aucune étude trouvée qui relie le faux positif au retest de la personne. **Neuf.**

**Probabilité.** 45 % pour la corrélation brute ; 25 % qu'elle survive au contrôle de typicité.

---

## 4. Le panel dans le corpus : Twin-2K-500 est-il déjà dans l'entraînement des modèles de 2026 ?

**Intuition.** Twin-2K-500 est un CSV de 59 Mo sous CC BY sur Hugging Face depuis mai 2025 [MESURE, PROVENANCE].
Tout modèle dont la coupure est postérieure (Qwen3-2507, les modèles OpenRouter de R6, Qwen3.6, DeepSeek V4) a pu
l'ingérer. Personne ne le vérifie avant d'évaluer des jumeaux dessus.

**Whoa.** Le pré-mortem 1 a écarté la mémorisation de microdonnées parce que « le modèle ignore userid » ; ici, les
microdonnées sont précisément le texte du persona, publié tel quel. Si un modèle de 2026 complète mot pour mot un
persona à partir de ses 200 premiers tokens, tout score de « fidélité individuelle » mesuré avec lui est suspect,
et le champ a besoin d'un canari standard.

**Premier test (< 48 h).** Trois canaris : (i) perplexité du texte de persona (parquet) contre celle d'une paraphrase
à contenu égal, sur Olmo-3-7B (coupure déc. 2024, propre [MESURE]) et gpt-oss-20b (juin 2024, propre) comme
témoins, puis Qwen3-4B-Instruct-2507 et deux modèles OpenRouter de 2026 ; (ii) complétion des 30 derniers tokens
de 200 personas, taux de reproduction exacte ; (iii) exactitude vague 4 à persona démographique seul, comparée entre
modèles propres et postérieurs, après retrait de la moyenne d'item. Un modèle contaminé bat la moyenne d'item sans
persona.
[PARI] Ratio de perplexité persona / paraphrase < 0,9 pour au moins un modèle 2026 (probabilité 15 %) ; sinon nul
propre.
**Tueur.** La perplexité plus basse d'un texte « naturel » que d'une paraphrase existe sans mémorisation : les
témoins propres donnent le plancher ; il faut que l'écart des modèles 2026 dépasse celui des témoins de deux ET.
Second tueur : la contamination peut être partielle (pages HF, pas le parquet), donc « nul au canari » n'est pas
« propre » — le dire.
**Coût.** 2 h de calcul local, ~5 € OpenRouter, une journée.

**Antériorité.** Contamination des benchmarks : littérature abondante (2406.04244, 2502.17259) ; rien sur
Twin-2K-500 ni sur aucun panel de jumeaux. **Neuf par l'objet**, banal par la méthode ; sa valeur est de devenir
l'étape zéro de tout article sur ce panel.

**Probabilité.** 15 % d'une contamination détectable ; 85 % d'un nul utile et citable.

---

## 5. Le pré-test à onze paires : les jumeaux reproduisent-ils les expériences de formulation du GSS ?

**Intuition.** Le GSS embarque depuis 1984 onze expériences de formulation randomisées (`nat*` contre `nat*y` :
« welfare » contre « assistance to the poor », « space exploration » contre « space exploration program »,
etc.), aux trois vagues du panel 2010-2014 [MESURE]. L'effet « welfare » est célèbre (30 à 50 points [CONFIRMÉ]),
les dix autres sont petits ou nuls et peu cités. Un jumeau qui pré-teste un questionnaire doit rendre les onze
amplitudes, pas la seule qu'il a lue.

**Whoa.** Le pré-test par LLM est vendu (LLM-Mirror, ISER WP 15) sans jamais être jugé contre des amplitudes
expérimentales réelles et par camp. Un résultat « le modèle rend welfare et invente les dix autres » tue une
promesse commerciale ; un résultat « il rend les onze » vaut un instrument.

**Premier test (< 48 h).** Qwen3-4B et gpt-oss-20b, 300 répondants GSS 2010 en persona (démographies + 20
réponses hors `nat*`), chaque paire posée dans les deux formes, à personnes appariées (chez les humains, la forme
est tirée au sort ; chez le jumeau on a les deux). Effet simulé par paire et par camp contre effet humain par paire
et par camp (panel 2010, trois vagues poolées, IC par famille).
[PARI] Corrélation des amplitudes sur 11 paires = 0,5, tirée par welfare ; hors welfare, r = 0,1 [−0,4 ; 0,5] ;
effet welfare simulé × 1,5 par rapport à l'humain (surdispersion habituelle, a15).
**Tueur.** Le nul « tout effet = 0 sauf welfare » : si son erreur absolue moyenne sur les 10 paires restantes est
inférieure à celle du modèle, le pré-test par LLM ne vaut pas la lecture d'un manuel. Second tueur : l'ordre des
deux formes dans le même prompt (contraste artificiel) ; poser les formes dans deux passes séparées.
**Coût.** 300 × 22 × 2 modèles ≈ 13 000 appels, deux heures ; une journée.

**Antériorité.** « LLMs for survey pretesting » (ISER 2026) juge la détection de défauts, pas les amplitudes ;
LLM-Mirror (2412.03162) pré-teste sans vérité expérimentale ; la méga-réplication d'expériences par LLM (PubMed
40634686) porte sur des scénarios de psychologie, pas sur les formes GSS. Aucun papier trouvé sur
welfare / assistance to the poor par LLM. **Neuf.**

**Probabilité.** 20 % que le modèle batte le nul « welfare seul » ; le nul est publiable comme mise en garde.

---

## 6. La loi d'échelle plate : le signal apparié ne croît pas avec la taille du modèle

**Intuition.** Tout le monde suppose que la fidélité individuelle est une capacité émergente : il suffirait
d'attendre le prochain modèle. Les données des auteurs contiennent déjà la même invite JSON sur gpt-4.1 et
gpt-4.1-mini, plus gemini-flash-2.5 [MESURE] ; le dépôt sait mesurer la chute sous permutation rapportée au
retest (C2). Si l'agrégat monte avec la taille et que l'apparié ne bouge pas, « attendre » est une erreur.

**Whoa.** Une courbe à deux pentes — agrégat en hausse, personne à plat — dit que la fidélité individuelle n'est
pas une question de capacité mais d'information, ce qui rejoint Ahn (surrogates) et Peng (XGBoost à 75 humains)
par un chemin qu'aucun des deux n'a pris : la taille.

**Premier test (< 48 h, 0 appel puis une nuit).** Étape 0 : sur les sorties des auteurs, exactitude agrégée et
chute sous permutation conditionnelle au segment (le code de C2) pour gpt-4.1-mini contre gpt-4.1 à invite JSON
identique, et pour gemini. Étape 1 : Qwen3-4B, Llama-3.1-8B, gpt-oss-20b, Qwen3-30B-A3B sur 300 personnes × 88
items, même invite. Tracer les deux quantités contre le log des paramètres actifs.
[PARI] Agrégat : +3 points entre mini et 4.1 ; chute sous permutation : différence dans ± 0,01 (IC couvrant 0) ;
sur les modèles locaux, pente de l'apparié non distinguable de 0 entre 4B et 30B.
**Tueur.** XGBoost entraîné sur 75 humains, à information égale : si l'apparié des grands modèles dépasse XGBoost
alors que celui des petits ne l'atteint pas, la loi n'est pas plate et l'idée s'inverse (résultat tout aussi
intéressant, mais opposé). Second tueur : les paramètres actifs de 30B-A3B (3 B) ne sont pas une « taille » ;
rapporter aux deux axes.
**Coût.** Étape 0 : 0 €, une demi-journée ; étape 1 : une nuit.

**Antériorité.** SimBench (ICLR 2026) montre une loi d'échelle sur l'agrégat ; Peng et al. comparent des personas,
pas des tailles ; Ahn et al. varient l'information, pas le modèle. Aucun tracé trouvé du signal apparié contre la
taille. **Neuf par la quantité tracée.**

**Probabilité.** 55 % pour la platitude ; c'est un nul, mais un nul qui ferme une croyance payante.

---

## 7. Le jumeau qui balance : les sorties d'un jumeau ré-identifient la personne

**Intuition.** Les auteurs publient les réponses simulées de chaque jumeau (13 CSV) à côté des réponses humaines.
Si un vecteur de sorties de jumeau se rattache à sa personne mieux qu'au hasard, alors publier des jumeaux, c'est
publier des personnes — et la « protection » qu'on prête à la simulation est un mythe.

**Whoa.** Le champ vend les jumeaux comme substitut qui *évite* de collecter des humains ; personne ne mesure
qu'ils *fuient* les humains dont ils sont faits. Une attaque de liaison à 30 % de top-1 sur 2 058 personnes est
un chiffre qu'un comité d'éthique retient.

**Premier test (< 48 h, 0 appel).** Attaque de liaison : pour chaque ligne de sorties de jumeau (holdout, vague 4
simulée), plus proche voisin parmi les 2 058 vecteurs humains de vagues 1-3 (items disjoints du holdout, donc pas
de copie). Taux de top-1 et de top-10, par configuration ; comparer persona complet, résumé, JSON, démographies
seules. Répéter en sens inverse (humain → jumeau).
[PARI] Top-1 = 25 % [15 ; 40] pour le persona complet, contre 0,05 % au hasard et 3 % pour démographies seules ;
top-10 > 50 %.
**Tueur.** Les démographies seules : si la liaison par démographies (âge, sexe, État, revenu) atteint déjà 20 %,
le jumeau n'ajoute rien à ce que les quasi-identifiants font. Il faut rapporter la liaison à démographies
retirées. Second tueur : la corrélation humain-jumeau (r ≈ 0,2-0,3, Peng) rend une liaison forte improbable ; si
top-1 < 5 % hors démographies, la fuite est négligeable et l'idée devient un argument rassurant, publiable aussi.
**Coût.** Une demi-journée, 0 €.

**Antériorité.** Ré-identification de données synthétiques : littérature classique (2407.07926) ; « Synthetic
Personalities » (2606.04592) mime des répondants depuis des microdonnées sans mesurer la liaison inverse ; rien
trouvé sur les jumeaux LLM. **Neuf pour cet objet.**

**Probabilité.** 60 % que la liaison dépasse démographies seules d'au moins 10 points ; whoa réel seulement si
top-1 > 15 %.

---

## 8. Le reste d'Ahn est du style : le signal individuel qui survit à la moyenne d'item est un style de réponse

**Intuition.** Ahn et al. montrent qu'après retrait de la moyenne d'item, le jumeau garde 5,7 % du plafond. Le
persona contient 500 réponses de la personne : de quoi apprendre qu'elle coche les extrêmes, le milieu, ou acquiesce.
Ce résidu serait un « surrogate de personne » (style), pas de la connaissance de ses opinions.

**Whoa.** Si le peu de signal apparié qui reste est du style, deux conséquences : la fidélité individuelle des
jumeaux est reproductible par trois indices (moyenne de la personne, ERS, acquiescement) sans LLM ; et,
symétriquement, un jumeau à trois exemples de style bien choisis devrait rattraper le persona de 500 réponses.

**Premier test (< 48 h, 0 appel).** Sur Twin-2K-500 : indices de style par personne sur vagues 1-3 (moyenne,
extrême, milieu, acquiescement ; a9 en a le code [MESURE]). Prédicteur « surrogate de style » de la vague 4 :
moyenne d'item + style de la personne. Comparer son R² apparié (après moyenne d'item) à celui de chaque
configuration de jumeau ; puis résidualiser humains et jumeaux du style et recalculer la corrélation appariée.
[PARI] Le surrogate de style atteint 4 % du plafond contre 5,7 % pour le jumeau ; après résidualisation, la
corrélation appariée du jumeau tombe de 0,25 à 0,15.
**Tueur.** Si la corrélation appariée résiduelle reste ≥ 0,22, le jumeau porte du contenu et l'idée est morte. Second
tueur, mais dans l'autre sens : le style est lui-même prédit par les démographies (âge, éducation) ; la part
« style » doit être rapportée après démographies pour ne pas recompter Ahn.
**Coût.** Une journée, 0 €. Étape 2 (jumeau à trois exemples de style, Qwen3-4B) : une nuit.

**Antériorité.** Ahn et al. (item-mean surrogates) ne testent pas de surrogate de personne ; a9 mesure les styles
contre la déviance, pas contre la fidélité du jumeau ; « Polypersona » et « Persona-Based Simulation at Population
Scale » ne décomposent pas le résidu. Aucun papier trouvé « response style surrogates ». **Neuf, suite directe d'Ahn.**

**Probabilité.** 40 %.

---

## Classement honnête

| # | Idée | 1er test | P(succès) | Nouveauté | Valeur du nul |
|---|---|---|---|---|---|
| 7 | Ré-identification par les sorties | 0 appel, ½ j | 60 % | neuve | moyenne (rassurant) |
| 6 | Loi d'échelle plate | 0 appel puis 1 nuit | 55 % | neuve (quantité) | forte |
| 3 | Turing inversé | 0 appel, 1 j | 45 / 25 % | neuve | faible |
| 8 | Le reste d'Ahn est du style | 0 appel, 1 j | 40 % | neuve, suite d'Ahn | moyenne |
| 1 | Psychométrie sans répondants | 0 appel, 1 j | 35 % | neuve | faible |
| 5 | Onze paires de formulation | 13 000 appels, 1 j | 20 % | neuve | forte (mise en garde) |
| 4 | Panel dans le corpus | 2 h + 5 € | 15 % | neuve par l'objet | forte (étape zéro) |
| 2 | Le jumeau bat la personne | 0 appel, 1 j | 10 % | neuve | faible |

Trois d'entre elles (1, 6, 8) se calculent le même jour sur les mêmes 13 CSV et le même code C2 ; c'est le lot à
lancer en premier. 4 et 7 sont des « étapes zéro » que n'importe quel relecteur exigera dès qu'elles existeront.
