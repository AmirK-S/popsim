# Brainstorm A, « exploiter nos atouts et nos surprises », 11 septembre 2026

Lecture seule du dépôt, aucun calcul lancé, 13 requêtes web (résumés seulement). Marques : [MESURE] relevé ici dans le
dépôt ; [NON VÉRIFIÉ] à contrôler avant lancement. Ce qui est déjà pris ailleurs vient de `veille-anteriorite-2026-09-11.md`,
les faiblesses de `revue-hostile-programme-2026-09-11.md`, les moonshots rejetés des deux pré-mortems ; les idées ci-dessous
évitent le cadran de polarisation (moonshot 3), la mémorisation SCE (moonshot 1) et les modèles à coupure (moonshot 2).

## Quatre faits relevés avant d'écrire, qui changent les plans

1. **Twin : la vague 4 arrive deux semaines après la vague 3** (`data/twin2k500/README.md` l. 45) [MESURE]. Les
   28,8 % de cellules « changées » sont donc surtout du bruit de retest et de l'ambivalence, pas des conversions. Le
   signal AUC 0,65 détecte des réponses fragiles ; « opinions en train de basculer » exige un délai long (GSS panel).
2. **Demographics Only atteint déjà AUC 0,607** (`memoire-resultats.md`) [MESURE]. Une grosse part du signal peut
   être de l'atypicité par rapport au segment démographique, ou la volatilité propre à l'item, sans « connaissance » de
   la personne. Toute idée ci-dessous doit battre ces deux nuls.
3. **Pas d'indicateur d'inattention exploitable dans nos fichiers Twin** : `attention_1`, `attention_2` et
   `Duration (in seconds)` n'ont qu'une valeur non vide (la ligne d'en-tête Qualtrics) sur 2 059 lignes
   (`llm_specs/humains_wave1_3.csv`) ; aucune colonne de ce type dans `wave1_3_response.csv` (761 colonnes) [MESURE].
4. **Stanford permet une réplication à zéro appel** : `osf-t6g7k-stanford/figure2/.../gss_filtered/preparation/`
   contient `p_wave1_summary.csv`, `p_wave2_summary.csv` et les agents `gss_v3/v6/v7/v8`, `composite_agents`,
   `survey_agents`, au format personne × item (1 052 lignes) [MESURE]. Retest à deux semaines : consistance moyenne
   0,795, 10,6 % des personnes sous 0,70 ; GSS panel : 0,690 à deux ans, environ 0,67 à quatre ans
   (`a12-retest-individu.csv`, `a12-delai-de-retest.md`) [MESURE]. La consistance par item à deux semaines, deux ans
   et quatre ans est dans `a12-items-stables-instables.csv`.

---

## 1. La question qui tremble ou la personne qui doute ?

**Intuition.** L'AUC de 0,65 peut venir de trois sources : des items volatils (le jumeau et l'humain hésitent aux
mêmes endroits), des personnes volatiles, ou l'interaction propre (cette personne, sur cet item). Seule la troisième
serait de la connaissance individuelle ; la décomposition dit ce que le jumeau voit vraiment.

**Pourquoi surprenant, pour qui.** Si le signal survit aux effets fixes item et personne, un jumeau LLM repère la réponse
précise qui ne tiendra pas. C'est le premier usage « à la personne » des jumeaux qui ne soit pas une exactitude, et un
retournement du constat d'Ahn et al. (le persona n'apporte rien au-delà de la moyenne d'item) : ici le persona servirait à
prédire l'erreur, pas la réponse. Pour les méthodologistes d'enquête (Zaller et Feldman, Achen) et pour les équipes
Twin-2K-500.

**Premier test (< 24 h, 0 $, 0 appel).** Réutiliser `analyses/memoire_twin.py`. Score = nombre de configurations, parmi
les 8, en désaccord avec la réponse passée (0 à 8). Modèles logistiques emboîtés sur 168 768 cellules : (a) volatilité
de l'item estimée sur une moitié des personnes ; (b) + taux de changement de la personne calculé en excluant l'item
courant ; (c) + score du jumeau ; (d) + atypicité démographique (désaccord de Demographics Only). Métriques : AUC moyenne
intra-item et ΔAUC de (c) sur (b), IC bootstrap personnes × items (graine 20260909).
**Prédictions.** AUC intra-item du score 0,60 [0,58 ; 0,62] ; ΔAUC (c)−(b) = +0,025 ; ΔAUC du jumeau riche au-delà de
Demographics Only (d) = +0,01. **On continue** si ΔAUC (c)−(b) ≥ +0,015 avec une borne basse > 0 ; **on abandonne** sous
+0,005.

**Antériorité (2 requêtes).** Rien trouvé sur le désaccord entre un jumeau LLM et une réponse humaine passée comme
prédicteur du changement au retest. Travaux voisins : instabilité des réponses *du LLM* (2511.10688, 2606.16011) ;
dissociation agrégat / signal apparié (Wang et al. 2609.07987). **Neuf à notre connaissance.**

**Risque principal.** Le signal est de la volatilité d'item habillée : le jumeau hésite là où tout le monde hésite, et
ΔAUC tombe à ~0 après effets fixes.

## 2. Ne réinterrogez que ce que le jumeau conteste

**Intuition.** P4 a échoué parce que la règle *remplaçait* la réponse passée par celle du jumeau (−9,4 points). Le bon
usage d'un signal faible mais réel est de décider *quoi revérifier* : réinterroger en priorité les cellules contestées
par le jumeau.

**Pourquoi surprenant, pour qui.** Les programmes de réinterview (Census, Biemer) tirent au hasard ou sur des critères
d'enquêteur ; un jumeau LLM qui double le rendement d'un budget de réinterview serait un gain opérationnel immédiat pour
les instituts de panel et les études longitudinales. Pour les praticiens, c'est un usage défendable des jumeaux : on ne
substitue rien, on cible.

**Premier test (< 24 h, 0 $, 0 appel).** Simulation sur Twin : budget de 10 % des cellules réinterrogées (la réponse de
vague 4 tient lieu de réinterview). Règles : hasard ; volatilité d'item (moitié des personnes) ; score du jumeau (0-8) ;
combinaison item + jumeau. Métriques : taux de changement dans les cellules choisies, rappel des cellules changées et gain
de consistance du fichier corrigé. Réplication Stanford (agents `gss_v8` contre `p_wave1`, cible `p_wave2`).
**Prédictions.** Taux de changement dans le décile choisi : hasard 28,8 % [MESURE], item seul 37 %, jumeau seul 40 %,
combinaison 43 %. **On continue** si la combinaison bat l'item seul de ≥ 3 points (IC bootstrap). Stanford : même ordre,
avec des niveaux plus bas (base ~20 %).

**Antériorité (1 requête).** Réinterview et réconciliation (Biemer et Forsman ; littérature d'erreur de réponse),
prédiction de la difficulté du répondant par ML sur les mouvements de souris (2011.06916) ; aucun ciblage par un jumeau
LLM trouvé. **Neuf à notre connaissance.**

**Risque principal.** Le gain sur « item seul » est trop petit pour justifier un LLM, et à deux semaines d'intervalle on
cible du bruit, pas de l'information : un relecteur demandera la preuve sur un vrai budget de réinterview.

## 3. Le répondant qui ne ressemble pas à son jumeau

**Intuition.** Agrégé par personne, le désaccord moyen entre le jumeau et les réponses réelles de la personne est une
statistique d'ajustement de la personne (*person-fit*), fondée sur le sens des questions plutôt que sur un modèle IRT.
Les répondants que leur jumeau ne reconnaît pas devraient être les inattentifs, les instables ou ceux qui n'ont pas
d'attitude.

**Pourquoi surprenant, pour qui.** Détecter les répondants bâclés sans question-piège, sans temps de réponse et sans
échelle inversée, avec les seules réponses, sur n'importe quel questionnaire : utile aux panels en ligne, alors que les
LLM contournent désormais les contrôles classiques. Si le jumeau fait mieux qu'un indice de *person-fit* statistique, la
compréhension sémantique ajoute quelque chose de mesurable.

**Premier test (< 24 h, 0 $, 0 appel).** Stanford d'abord, puisque Twin n'a pas de contrôles d'attention exploitables
(fait 3) : désaccord moyen agent `gss_v8` / vague 1 par personne ; critère = consistance vague 1 → vague 2 < 0,70 (10,6 %
des personnes) [MESURE]. Comparateurs : distance à la modalité du segment démographique (atypicité), indice lz
polytomique ou rareté des patrons de réponse, taux de non-réponse. Réplication Twin : désaccord moyen sur 8 configurations
contre taux de changement de la personne.
**Prédictions.** AUC (instable < 0,70) = 0,68 [0,63 ; 0,73] ; Spearman (désaccord moyen, taux de changement) = 0,30 sur
Twin et 0,25 sur Stanford ; gain au-delà de l'atypicité démographique ΔAUC = +0,03.
**On continue** si ΔAUC ≥ +0,02 au-delà de l'atypicité et de lz.

**Antériorité (1 requête).** Réponses négligentes par gradient boosting (Schroeders et al. 2022), échelle de charabia
(Bloy et al. 2025), LLM qui passent les contrôles (ACM CI 2025) ; *person-fit* IRT classique. Jumeau LLM comme détecteur
non trouvé. **Partiellement voisin, forme neuve.**

**Risque principal.** Le désaccord est une atypicité banale : les personnes sincères mais hors stéréotype sont signalées
comme « inattentives ». Il y a aussi un risque d'équité (minorités sur-signalées) et, dans nos fichiers, pas de vérité
terrain d'inattention.

## 4. Bruit ou conversion : ce que le jumeau voit selon le délai

**Intuition.** Si le désaccord signale l'ambivalence (Zaller et Feldman), son pouvoir prédictif est le même à deux
semaines et à quatre ans. S'il signale une attraction vers le « type » de la personne, qui finit par l'emporter, il croît
avec le délai, et les changements vont vers la réponse du jumeau.

**Pourquoi surprenant, pour qui.** Un jumeau qui prévoit *dans quel sens* une personne va basculer sur quatre ans
détecterait des opinions en train de basculer ; un signal plat trancherait, avec un outil nouveau, un vieux débat de
science politique (instabilité d'attitude contre erreur de mesure). Pour la science politique et la sociologie des
panels, dans les deux cas.

**Premier test (< 24 h, 0 $).** Trois délais. Deux semaines : Stanford, zéro appel, agents `gss_v8` (exclure
`survey_agents` et `composite`, qui ont vu les réponses). Deux et quatre ans : panel GSS 2010-2012-2014, 137 items
appariés [MESURE, pré-mortem 2]. Jumeau local gpt-oss-20b nourri des réponses 2010 aux *autres* familles d'items
(`a8-familles-gss.csv`) : 300 personnes × 60 items = 18 000 appels, environ 2 h 30 à 7 200 appels/h [MESURE, pré-mortem
1]. Cible : changement 2010→2012 et 2010→2014. Secondaire : parmi les changeurs dont le jumeau diffère de la réponse 2010,
part qui rejoint la réponse du jumeau, contre la part qui rejoint la modalité du segment.
**Prédictions.** AUC deux semaines 0,64 ; deux ans 0,60 ; quatre ans 0,60, soit un profil plat à ±0,03 (probabilité
0,65). Part des changeurs qui rejoignent le jumeau : 0,40 contre 0,38 pour la modalité du segment, écart non significatif
(probabilité 0,7). **Résultat fort** si l'AUC gagne ≥ +0,04 entre deux et quatre ans, ou si l'attraction du jumeau bat la
modalité de ≥ 5 points.

**Antériorité (2 requêtes).** Rien trouvé sur l'AUC en fonction du délai ; Peng et al. (2509.19088) montrent que le
changement d'attitude *des jumeaux* régresse vers la moyenne, à l'inverse des humains (voisin, autre objet). **Neuf à notre
connaissance.**

**Risque principal.** Délais non comparables : jeux, items, jumeaux (GPT-4o sur interview contre 20 B local) et
contamination GSS diffèrent tous. Un profil plat ou montant peut refléter le jumeau plutôt que la dynamique des opinions.
Contrôle minimal : le même jumeau local sur Stanford.

## 5. L'hésitation de la machine épouse celle des humains

**Intuition.** Deux sources d'« hésitation machine » sont déjà dans le dépôt : le désaccord entre les 8 configurations
Twin sur une même cellule, et la variation de DeepSeek entre deux passes à T = 0 (R6, par item et par camp). Si elles
tombent là où les humains changent d'avis au retest, le non-déterminisme n'est pas qu'un défaut : c'est une mesure de
l'ambivalence de la question.

**Pourquoi surprenant, pour qui.** R6 est « déjà fait » comme constat (Atil et al.) ; le transformer en signal serait un
retournement. L'enjeu va aux concepteurs de questionnaires (prétester la fiabilité d'un item sans panel) et aux auditeurs
de simulateurs (séparer l'instabilité légitime de l'instabilité de service).

**Premier test (< 24 h, 0 $, 0 appel).** (a) Cellules Twin : entropie du vote des 8 configurations, contre le changement
humain ; comparer à l'AUC d'une seule configuration (0,649). (b) Items GSS : `tv_essais` moyen par item dans
`r6-instabilite-pilote-deepseek.csv`, contre `1 − consistance_2sem`, corrigée du hasard `hasard_stanford`, dans
`a12-items-stables-instables.csv`. Contrôles : nombre de modalités, part de la modalité dominante.
**Prédictions.** (a) AUC de l'entropie = 0,66 [0,65 ; 0,67], soit +0,01 sur la meilleure configuration seule.
(b) Spearman partiel à nombre de modalités fixé = 0,25 [0,08 ; 0,40] ; le Spearman brut sera plus haut (0,35). **Échec**
si le partiel contient 0.

**Antériorité (2 requêtes).** L'incertitude des LLM est alignée sur le *désaccord entre annotateurs* (2503.12528,
2605.30675) ; le non-déterminisme à T = 0 est documenté par Atil et al. (2408.04667). Pas de lien trouvé avec
l'instabilité *intra-personne* au retest. **Partiellement voisin, forme neuve.**

**Risque principal.** Le nombre de modalités et les items à mi-échelle expliquent les deux instabilités à la fois, et le
partiel s'annule. Le pilote R6 est petit (pilote DeepSeek, un service).

## 6. L'étiquette convoque les partis dans nos têtes

**Intuition.** R3 : nommer le segment multiplie l'écart inter-segments par 2,9 sans toucher la correspondance
individuelle. Mécanisme candidat : l'étiquette tire la personne simulée vers la composition *stéréotypée* du camp (les
électeurs imaginés d'Ahler et Sood), donc l'inflation devrait se concentrer sur les items liés aux traits surestimés
(religion, revenu élevé, syndicat, LGBT).

**Pourquoi surprenant, pour qui.** Passer d'un constat (« les LLM gonflent les écarts de 2 à 4 fois », Chen et al.) à
une loi item par item prédite par une mesure humaine indépendante des perceptions erronées donnerait un mécanisme
testable et un correctif : repondérer les items selon leur charge stéréotypique. Pour la psychologie politique et les
auteurs de benchmarks de fidélité de groupe.

**Premier test (< 24 h, 0 $, 0 appel).** Recalculer, depuis les traces R3 (`analyses/r3_ablation_etiquette.py`,
condition C3E, 94 personnes, 58 items [MESURE `r3-tableau.csv`]), l'inflation par item = log(écart avec étiquette /
écart sans étiquette). Prédicteur humain par item : corrélation, dans les données Stanford vague 1, entre la réponse et
les traits de composition d'Ahler et Sood, pondérée par l'ampleur de la perception erronée (`fig_1_data_perc.dta` contre
`fig_1_data_actual.dta`). Bootstrap par famille d'items.
**Prédiction.** Spearman = 0,30 [−0,05 ; 0,55] sur 58 items : l'IC contiendra probablement 0, ce qui en fait un test
pilote, pas un verdict. Si l'estimé ≥ 0,30, on étend l'essai aux 149 items en description (R1, un appel par item × camp,
~300 appels).

**Antériorité (2 requêtes).** Des personas LLM approchent les perceptions erronées partisanes (2504.11673, *Deep Binding*),
ils ont des stéréotypes marqués (Cheng et al. 2305.18189) et ils écrasent ou caricaturent les groupes (Wang, Morgenstern,
Dickerson 2402.01908). Aucun lien item par item entre l'inflation d'écart et une mesure humaine de stéréotype n'a été
trouvé. **Partiellement fait** : le phénomène est pris, le mécanisme prédictif ne l'est pas.

**Risque principal.** `a46` l'a établi : Ahler et Sood mesurent des compositions, pas des opinions. Le pont par
corrélation trait-item est indirect, et 58 items d'une seule condition donnent une puissance quasi nulle.

## 7. Les exemples déplacent le camp, jamais la personne

**Intuition.** R3 montre que l'étiquette gonfle le groupe sans toucher la personne ; R5 montre que trois exemples
déplacent l'écart entre camps. Test de la double dissociation en incarnation : des exemples *incongruents* (réponses
d'humains de l'autre camp) retournent-ils l'écart de groupe tout en laissant intacte la correspondance individuelle ?

**Pourquoi surprenant, pour qui.** Si oui, le résumé tient en une phrase : dans un échantillon silicium, le niveau de
groupe est un réglage d'invite, le niveau individuel est porté par le persona, et les deux se mesurent séparément. Le
résultat va aux utilisateurs de panels synthétiques à exemples (few-shot), qui publient des écarts de groupe. Il se
distingue du moonshot 3 (loi additive du cadran) et du plan factoriel de la revue hostile (description, pas incarnation).

**Premier test (< 24 h, 0 $).** Protocole C3E de R3 (94 personnes Stanford, 58 items), gpt-oss-20b local. Trois
conditions : sans exemple, trois exemples congruents (humains du même segment idéologique, autres items), trois exemples
incongruents (humains du segment opposé). Coût : 94 × 58 × 3 ≈ 16 400 appels, environ 2 h 30. Mesures : ratio inter-camps
(S_ideo) comme dans `r3-tableau.csv`, exactitude individuelle, chute sous permutation intra-segment.
**Prédictions.** L'écart inter-camps incongruent baisse d'au moins 40 % par rapport au congruent (retournement de signe
sur ≥ 30 % des items orientés). La chute sous permutation varie de < 0,02 entre les conditions. L'exactitude baisse de 2
à 4 points en incongruent.

**Antériorité (1 requête).** Meister et al. (2411.05403, few-shot > persona) ; Choi et al. (2606.28963, plan 2×2 où le
few-shot dégrade la structure) ; les personas incongruents sont moins cohérents (littérature sur les répondants virtuels).
Aucune double dissociation groupe / personne sous exemples incongruents trouvée. **Partiellement voisin.**

**Risque principal.** L'ancrage : le modèle recopie les nombres ou les modalités des exemples (R5 : la relance recopie
son exemple chiffré 45 fois sur 45 [MESURE `r5_gabarit_exemples.py` l. 34]), et la « dissociation » devient un artefact
de copie. Autre limite : 94 personnes et un seul modèle.

## 8. Les questions orphelines, là où le texte bat la statistique

**Intuition.** Sur le bloc B tenu à l'écart, les LLM à persona riche battent PMM, à rebours de Peng et al. et de Chen et
al. Hypothèse : l'avantage se concentre sur les items « orphelins », qu'aucun item du bloc A ne prédit statistiquement,
où PMM n'a pas de voisin et où seul le sens de la question permet de transférer.

**Pourquoi surprenant, pour qui.** Cela réconcilierait deux littératures contradictoires : les baselines statistiques
gagnent quand la structure de corrélation existe, les LLM quand elle manque. Le résultat dirait où un jumeau vaut son
coût : les *questions nouvelles*, jamais posées au panel. Il concerne les concepteurs de questionnaires, les instituts et
Peng et al., et c'est le seul usage de C3 qui transforme un constat descriptif en hypothèse testable.

**Premier test (< 24 h, 0 $, 0 appel).** Recalculer la perte B *par item* avec `tab_evaluer.py` sur les 108 items de
`tab-partition-items.csv`. Prédictibilité statistique de chaque item B = R² maximal (ou Cramér) avec les items A chez les
humains. Avantage par item = perte PMM − perte de la meilleure configuration riche. Contrôle : B0 mode, pour écarter les
items où « tout le monde répond la modalité ».
**Prédictions.** Spearman (avantage, prédictibilité) = −0,40 [−0,60 ; −0,15]. Avantage moyen dans le tercile le moins
prédictible : +0,08 ; dans le tercile le plus prédictible : +0,00. **Échec instructif** si la pente est positive, dans le
sens de Hu et al.

**Antériorité (2 requêtes).** Kim et Lee (2305.09620) : les opinions jamais posées sont les plus dures pour le LLM.
2606.09351 : l'écart ICL contre MICE est le plus grand pour les opinions jamais posées (lu au résumé). Hu et al.
(2402.10811) : le LLM prédit mieux quand les variables du persona expliquent davantage, prédiction de signe opposé.
2609.02526 : la baseline statistique choisit mieux les attributs. **Partiellement fait** ; la stratification par
prédictibilité, contre PMM sur Twin, n'a pas été trouvée.

**Risque principal.** Le bloc B compte peu de familles (levier L15) et les items orphelins sont souvent peu variables :
l'avantage peut venir de la modalité, pas du sens. Le résultat serait aussi post hoc sur un bloc déjà ouvert, donc à
préenregistrer avant tout calcul par item.

---

## Ordre suggéré (coût zéro d'abord)

1, 2 et 5a le même après-midi : un seul script, qui part de `memoire_twin.py`. Ensuite 3 et le bras Stanford de 4 (zéro
appel), puis 8. 4 (GSS) et 7 demandent une nuit locale chacun. 6 reste un pilote tant que R1 n'a pas été étendu. Chaque
test fait l'objet d'une page de plan horodatée *avant* le calcul (revue hostile, faiblesse 1).

## Sources ouvertes (résumés)

- [Wang et al. 2609.07987](https://arxiv.org/html/2609.07987) ; [Peng et al. 2509.19088](https://arxiv.org/pdf/2509.19088)
- [2511.10688, instabilité multi-tours](https://arxiv.org/abs/2511.10688) ; [2606.16011, Who Flips?](https://arxiv.org/pdf/2606.16011)
- [Zaller et Feldman 1992](https://calgara.github.io/Pol1_Fall2017/Zaller_Feldman1992.pdf)
- [Schroeders et al. 2022](https://journals.sagepub.com/doi/10.1177/00131644211004708) ; [Bloy et al. 2025](https://journals.sagepub.com/doi/10.1177/25152459251378420) ; [ACM CI 2025, LLM et contrôles](https://dl.acm.org/doi/10.1145/3715928.3737491)
- [2011.06916, difficulté du répondant](https://arxiv.org/pdf/2011.06916)
- [2503.12528](https://arxiv.org/pdf/2503.12528) ; [2605.30675](https://arxiv.org/html/2605.30675)
- [2504.11673, Deep Binding](https://arxiv.org/pdf/2504.11673) ; [Marked Personas 2305.18189](https://arxiv.org/abs/2305.18189)
- [Kim et Lee 2305.09620](https://arxiv.org/html/2305.09620v4) ; [2606.09351](https://arxiv.org/html/2606.09351) ; [Hu et al. 2402.10811](https://arxiv.org/html/2402.10811v2) ; [2609.02526](https://arxiv.org/html/2609.02526)
