# Travaux connexes (brouillon prêt à traduire)

Sources locales : `resultats/veille-anteriorite-2026-09-11.md`, `resultats/c7-resultats.md`,
`resultats/c7-contre-examen-2026-09-11.md`, `resultats/c7-mecanisme-resultats.md`,
`resultats/c7-stanford-resultats.md`, `resultats/c7-defense-resultats.md`,
`resultats/a13-positionnement-contribution.md`, `resultats/divulgation-responsable-brouillon.md`.
Le fichier `positionnement-vie-privee-2026-09-12.md` n'existe pas encore : non attendu, comme
demandé. Les références des sections 1 à 4 viennent des deux veilles bibliographiques transmises
par le coordinateur (URL fournies) ; aucune n'est inventée.

## 1. Vie privée des données synthétiques

Stadler, Oprisanu et Troncoso (USENIX Security 2022, *Synthetic Data – Anonymisation Groundhog
Day*, https://arxiv.org/abs/2011.07018) montrent que des données tabulaires générées restent
reliables à leurs sources. Giomi, Boenisch, Wehmeyer et Tasnádi (*A Unified Framework for
Quantifying Privacy Risk in Synthetic Data*, Anonymeter, PoPETs 2023, vol. 2023, n° 2, p. 312-328,
doi 10.56553/popets-2023-0055, arXiv 2211.10459, https://arxiv.org/abs/2211.10459) formalisent
trois attaques (singling out, linkability, inference) et concluent, sur leurs jeux, à un risque de
linkability faible. Cette conclusion est contestée : Annamalai, Gadotti et Rocher (USENIX Security
2024, *A Linear Reconstruction Approach for Attribute Inference Attacks against Synthetic Data*,
https://arxiv.org/abs/2301.10053), Ganev et De Cristofaro (IEEE S&P 2025, *The Inadequacy of
Similarity-based Privacy Metrics: Privacy Attacks against "Truly Anonymous" Synthetic Datasets*,
https://arxiv.org/abs/2312.05114) et le même Ganev seul (atelier GenLaw @ ICML 2024, *Synthetic
Data, Similarity-based Privacy Metrics, and Regulatory (Non-)Compliance*,
https://arxiv.org/abs/2407.16929 ; puis Ganev et De Cristofaro à nouveau, 2026, préprint sans lieu
de publication confirmé, *Rethinking Anonymity Claims in Synthetic Data Generation: A
Model-Centric Privacy Attack Perspective*, https://arxiv.org/abs/2601.22434) montrent que des
attaques par reconstruction battent les métriques de distance-au-plus-proche-voisin (DCR). Yao,
Krčo, Ganev et de Montjoye (ESORICS 2025, *The DCR Delusion*, doi
10.1007/978-3-032-07884-1_24, https://arxiv.org/abs/2505.01524) et Meeus, Guépin, Creţu et de
Montjoye (*Achilles' Heels: Vulnerable Record Identification in Synthetic Data Publishing*,
ESORICS 2023, doi 10.1007/978-3-031-51476-0_19, https://arxiv.org/abs/2306.10308) généralisent la
critique de la DCR. Golob, Pentyala et De Cock (préprint 2026, *SoK: Reconstruction Attacks on
Synthetic Tabular Data (Insights from Winning the NIST CRC)*, « SoK » faisant partie du titre et
non d'un lieu de publication, https://arxiv.org/abs/2606.08372) font de ces attaques un standard
émergent.
**Argument 1 :** Anonymeter conclut à une linkability faible sur ses jeux tabulaires ; notre taux
(20,7 %, 65,7 %) est un contre-exemple frontal, dans un régime — sorties catégorielles d'un LLM
conditionné sur une personne — qu'ils n'ont pas testé.
**Ce qui nous distingue :** ce corpus porte sur des microdonnées tabulaires produites par des
modèles génératifs classiques (GAN, copules, diffusion), évaluées par des métriques de similarité
continue. Notre objet est un vecteur de réponses catégorielles d'un LLM à un questionnaire, sans
métrique de similarité substituable à une attaque directe par appariement.
**Sur le vocabulaire de « linkability » — contradiction mesurée, mais bornée au pipeline partagé
(pertinente pour A7) :** Giomi et al. définissent formellement la linkability, section 5.2, p. 319 :
« Given two disjoint sets of original attributes, use the synthetic dataset to determine whether or
not they belong to the same individual. » L'attaquant tient les **valeurs réelles** des deux
ensembles d'attributs (T[:,A], T[:,B], p. 319), extraits d'un **seul** jeu original réel ; le
synthétique ne sert que d'intermédiaire entre deux vues d'attributs de ce même jeu. Notre scénario
diffère : nous relions **deux sorties synthétiques indépendantes** de la même personne, sans
qu'aucune valeur réelle soit détenue par l'attaquant. Sur ce point nous ne les contredisons pas —
les objets attaqués ne sont pas les mêmes. En revanche, leur résumé (p. 312) conclut : « we observe
that synthetic data exhibits the lowest vulnerability against linkability » — confirmé section 6.1,
p. 320-321 : « the risk to linkability is comparably low over all datasets evaluated. » **Nous
contredisons cette conclusion générale, mais seulement dans le régime où les deux sorties viennent
d'un pipeline partagé** (A7, 36,4 % de top-1 à 60 items communs, contrôle à 0,06 %, même équipe,
mêmes fichiers de persona) : la linkability n'y est pas un risque négligeable, dans un régime qu'ils
n'ont pas testé. Un témoin construit ensuite avec deux organisations réellement indépendantes
(modèle, gabarit de prompt et format de persona tous distincts, `c7-deux-organisations-resultats.md`)
montre que ce signal **ne survit pas** au changement de pipeline : top-1 = 1,76 % [0,35 ; 3,63] sur
142 personnes, sous la baseline démographique seule (9,2 %) et loin du leurre de segment (25,5 %) —
un résultat négatif que nous obtenons et rapportons nous-mêmes. Dans ce second régime, nous ne
contredisons plus Anonymeter, nous le corroborons. Guan, Guépin, Cretu et de Montjoye (*A Zero
Auxiliary Knowledge Membership Inference Attack on Aggregate Location Data*, ZAK-MIA, PoPETs
2024(4):80-101, DOI 10.56553/popets-2024-0108) sont hors de ce débat : leur attaque porte sur
l'**appartenance** (déterminer si un individu a contribué à l'agrégat publié), jamais sur la liaison
entre deux sorties, et l'objet attaqué est un agrégat de comptages de localisation, pas un
enregistrement tabulaire synthétique individuel. Guépin, Krawczyk et De Cristofaro (*Synthetic is
all you need*, arXiv 2307.01701) suppriment l'hypothèse de données auxiliaires réelles mais restent
eux aussi sur l'appartenance au jeu d'entraînement d'un générateur unique : jamais l'appariement
entre deux générations indépendantes du même panel. Notre canal de liaison inter-jumeaux n'a donc
pas d'antériorité qui teste le même scénario ; ce que nous revendiquons est une contradiction
mesurée, mais désormais explicitement bornée au régime pipeline-partagé, de la conclusion générale
d'Anonymeter — pas un vide bibliographique, et pas davantage une menace générique valable pour deux
publieurs quelconques.

## 2. Ré-identification de données réelles

Narayanan et Shmatikov (*Robust De-anonymization of Large Sparse Datasets*, IEEE S&P 2008, doi
10.1109/SP.2008.33, p. 111-135 ; le préprint arXiv cs/0610105, https://arxiv.org/abs/cs/0610105,
porte un titre distinct, *How To Break Anonymity of the Netflix Prize Dataset*) ré-identifient des
utilisateurs Netflix. De Montjoye et al. (*Science* 2015, doi 10.1126/science.1256297) : quatre
points spatio-temporels suffisent sur des métadonnées de carte bancaire. Rocher, Hendrickx et de
Montjoye (*Nature Communications* 2019, doi 10.1038/s41467-019-10933-3) donnent un modèle pour
estimer le risque sur un échantillon incomplet, prolongé par une loi d'échelle (*A scaling law to
model the effectiveness of identification techniques*, *Nature Communications* 2025,
https://www.nature.com/articles/s41467-024-55296-6). Taub, Elliot, Pampaka et Smith
(*Differential Correct Attribution Probability for Synthetic Data: An Exploration*, PSD 2018, LNCS
11126, p. 122-137) fondent la mesure statistique du risque de divulgation sur données synthétiques
(CAP, TCAP, probabilité d'attribution correcte) sur le postulat que la génération synthétique
rompt le lien entre identité et donnée.
**Argument 2 :** CAP et TCAP postulent que le synthétique rompt ce lien ; c'est ce postulat que
nous falsifions, sur des microdonnées d'enquête simulées par LLM plutôt que générées par un modèle
statistique classique.
**Ce qui nous distingue :** ces travaux ré-identifient à partir de vraies données auxiliaires
(notes, déplacements, achats réels). Chez nous, l'entrée de l'attaque n'est jamais une donnée
réelle de la cible : c'est une sortie de modèle générée à partir d'un persona, comparée aux vraies
réponses détenues par l'attaquant.
**Cadrage théorique de notre mesure en bits (A4), à présenter comme un instrument dérivé plutôt
qu'une découverte :** c'est un cas de fuite en min-entropie de Rényi au sens de Smith (*On the
Foundations of Quantitative Information Flow*, FoSSaCS 2009) — la probabilité de deviner juste en
un seul essai, ici log2 du rapport des probabilités de bonne devinette avant/après persona —, dans
l'esprit du surprisal employé par Eckersley (*How Unique Is Your Web Browser?*, PETS 2010
**[référence exacte à confirmer avant dépôt]**) pour les empreintes de navigateur. Elle répond au
même problème de transportabilité que le κ de la loi d'échelle de Rocher, Hendrickx et de Montjoye
(*Nat. Commun.* 2025, déjà cité ci-dessus) par une autre voie.

## 3. Vie privée et LLM

Carlini et al. (USENIX Security 2021, arXiv 2012.07805, https://arxiv.org/abs/2012.07805) :
mémorisation et régurgitation de séquences d'entraînement. Staab, Vero, Balunović et Vechev (ICLR
2024, arXiv 2310.07298, https://arxiv.org/abs/2310.07298) : inférence d'attributs personnels à
partir de texte libre anodin. Ko, Jeong, Thakur, Kim et Jia (ICML 2026, *From Weak Cues to Real
Identities: Evaluating Inference-Driven De-Anonymization in LLM Agents*, arXiv 2603.18382,
https://arxiv.org/abs/2603.18382) désanonymisent des auteurs de texte en ligne par inférence
agentique multi-indices : c'est le voisin le plus menaçant de cette section, sur le même objet
(désanonymisation par agent LLM). Lermen, Paleka, Swanson, Aerni, Carlini et Tramèr (préprint 2026,
sans lieu de publication confirmé, *Large-Scale Online Deanonymization with LLMs*, arXiv
2602.16800, https://arxiv.org/abs/2602.16800, 68 % de rappel à 90 % de précision) démontrent la
même attaque à grande échelle.
Sur le plan théorique, Yeom, Giacomelli, Fredrikson et Jha (CSF 2018, *Privacy Risk in Machine
Learning: Analyzing the Connection to Overfitting*, arXiv 1709.01604 **[identifiant à confirmer
avant dépôt]**) relient l'attaque d'appartenance au sur-apprentissage, et Feldman (STOC 2020, *Does
Learning Require Memorization? A Short Tale about a Long Tail*, arXiv 1906.05271 **[identifiant à
confirmer]**) montre que mémoriser les cas rares est nécessaire à la généralisation d'un modèle
entraîné sur la population. Bun, Ullman et Vadhan (STOC 2014, codes de traçage, arXiv 1311.3158
**[à confirmer]**) et Dwork, Smith, Steinke, Ullman et Vadhan (FOCS 2015, *Robust Traceability from
Trace Amounts*, arXiv 1502.02486 **[à confirmer]**) sont le parent formel le plus proche de notre
attaque 1-parmi-N : ils bornent le pire cas d'un adversaire optimal qui retrouve un individu dans
des statistiques agrégées, mais en dimension très supérieure au nombre d'individus.
**Ce qui nous distingue :** Ko et al. et Lermen et al., comme Carlini et Staab, partent de texte
libre porteur d'indices sémantiques directs (un lieu, une habitude décrite en mots), agrégés par un
agent qui raisonne sur ce texte. Notre canal est plus étroit et plus sec : un vecteur de réponses
catégorielles à choix fermés (achète / n'achète pas), sans texte libre, sans raisonnement agentique
et sans mémorisation, établi par ablation en H3 (`c7-mecanisme-resultats.md`). À la différence de
Yeom et Feldman, notre pipeline n'entraîne aucun modèle sur la population cible : la personne
n'appartient à aucun jeu d'entraînement, et la fidélité individuelle vient du conditionnement par
persona, pas d'un écart train/test.
**Sur la construction de témoins (nuls) pour juger une attaque, précédent méthodologique direct
pour notre nul de marge (A1) :** Das, Zhang et Tramèr (*Blind Baselines Beat Membership Inference
Attacks for Foundation Models*, arXiv 2406.16201) montrent que des témoins aveugles battent
régulièrement l'état de l'art des attaques d'inférence d'appartenance sur modèles de fondation ;
Duan et al. (COLM 2024, arXiv 2402.07841) et un position paper (IEEE SaTML 2025, arXiv 2409.19798)
soutiennent qu'une attaque ne prouve rien tant que l'hypothèse nulle n'est pas correctement
échantillonnée. Notre nul de marge (`c7-disjoint-resultats.md`) répond au même impératif pour le
couplage qualité-fuite (A1, section 6) : nous construisons le témoin qui manquait — 100
prédicteurs sans aucune empreinte individuelle — et il absorbe notre propre effet (rho nul 0,984
contre 0,969 observé). C'est le résultat que cette littérature nous invite à produire, pas un aveu
de faiblesse.

## 4. Simulation de répondants et jumeaux

Argyle et al. (*Political Analysis* 2023, arXiv 2209.06899) lancent l'usage de LLM comme
substituts de panels. Park et al. (11 auteurs, préprint, titre courant depuis juin 2026 *LLM
Agents Grounded in Self-Reports Enable General-Purpose Simulation of Individuals* — la v1 de
novembre 2024, arXiv 2411.10109, portait le titre *Generative Agent Simulations of 1,000 People*,
encore le plus connu) restreignent l'accès aux réponses individuelles de leurs 1 052 agents « pour
raison de vie privée » — un risque anticipé jamais mesuré. Toubia et al. (2025, Twin-2K-500, arXiv
2505.17479) publient le panel de 2 058 jumeaux que nous attaquons, sans traiter vie privée ni
liaison. Peng, Gui, Brucks, Merlau, Fan et al. (*Digital twins are funhouse mirrors: Five
systematic distortions*, *Science Advances* 12(36), eaeh8260, 2 septembre 2026, doi
10.1126/sciadv.aeh8260 — le titre du préprint arXiv différait) documentent des distorsions de
fidélité de groupe sur ce même panel, sans lien avec la ré-identification. Bonagiri et al. (AIES
2026, *Cognitive Digital Twins: Ethical Risks and Governance for AI Systems That Model the Mind*,
arXiv 2606.23094, https://arxiv.org/abs/2606.23094) formulent un appel normatif à évaluer ces
risques sans les mesurer : nous y répondons par une mesure chiffrée.
**Ce qui nous distingue :** aucun de ces travaux, ni les cinq de la veille d'antériorité (Ahn et
al. 2608.29455, Wang et al. 2609.07987, Chen et al. 2607.26348, Choi et al. 2606.28963,
`veille-anteriorite-2026-09-11.md` §2), ne mesure de taux de ré-identification à partir de sorties
de jumeaux. C'est le trou que nous comblons.

## 5. Antériorité la plus proche et contradicteurs

Ward, Lin, Wang et Cheng (2025, *Synth-MIA: A Testbed for Auditing Privacy Leakage in Tabular Data
Synthesis*, arXiv 2509.18014, https://arxiv.org/abs/2509.18014) testent 13 attaques sur 9
générateurs et 48 jeux tabulaires, et leur section 5.2.1 énonce en prose une relation proche de la
nôtre entre qualité et fuite. Byun et al. (KDD Workshop 2025, arXiv 2507.17066,
https://arxiv.org/abs/2507.17066) observent une frontière quasi monotone du même type, sans
coefficient. Trois différences les séparent de notre thèse : leur qualité est **agrégée** (MMD,
divergence de Jensen-Shannon, AUC en aval) et jamais une correspondance à la bonne personne ; leur
risque est l'**appartenance** au jeu d'entraînement, pas l'identification 1-parmi-N dans un pool
fermé ou ouvert ; et ils ne publient **aucun coefficient** pour cette relation — le seul chiffré
dans Synth-MIA est DCR contre Max-AUC, r = 0,225, une corrélation faible entre deux métriques
agrégées, pas entre fidélité individuelle et fuite individuelle.

Trois contradicteurs soutiennent au contraire que fidélité et risque se séparent. Platzer et
Reutterer (2021, arXiv 2104.00635, https://arxiv.org/abs/2104.00635) défendent la séparabilité.
Adams et al. (iScience 2025 **[DOI à confirmer avant dépôt]**) concluent qu'un générateur
synthétique sans garantie formelle conserve fidélité et utilité sans atteinte évidente à la vie
privée. Shafieinejad, Emerson, Zamanlooy, Bassak, Tavakoli, Kodeiri, Lotif et He (préprint 2026, arXiv
2605.06835, https://arxiv.org/abs/2605.06835, *On Privacy Leakage in Tabular Diffusion Models*)
observent, sur des modèles de diffusion tabulaire (ClavaDDPM) attaqués par inférence d'appartenance
(MIA), qu'en poussant l'entraînement d'un même modèle plus loin, la qualité synthétique plafonne
(rendements décroissants) alors que le risque MIA continue de croître sans plafond visible : «
increasing training iterations improves quality with diminishing returns while privacy risk
continues to scale » (annexe F, premier paragraphe, p. 19, texte intégral lu), confirmé par « the
observed changes in MIA success are generally not tied to precipitous falloffs in synthetic
quality » (même paragraphe) et « synthetic data quality does vary with training configuration
changes, but it does not sharply degrade in any of the scenarios » (annexe F.1, p. 20). Notre
lecture antérieure de ce travail (« un découplage où le risque croît quand la qualité sature ») est
une paraphrase fidèle de cette conclusion, ni exagérée ni inventée. **Nuance nécessaire** : leur «
qualité » est une batterie de métriques agrégées (alpha-précision/bêta-rappel, KS, TVD, écarts de
corrélation/information mutuelle, efficacité en apprentissage automatique) et leur « risque » est le
succès d'une attaque d'appartenance (MIA) sur le jeu d'entraînement — pas une ré-identification
1-parmi-N — et le levier qui fait varier les deux est le temps/volume d'entraînement d'**un seul**
modèle, non une comparaison entre méthodes hétérogènes. Ce n'est donc ni « ces deux grandeurs ne
varient jamais ensemble » (elles montent ensemble tant que l'entraînement reste modéré) ni «
améliorer l'une n'aggrave jamais l'autre » (au contraire, passé un certain point l'entraînement
aggrave le risque sans plus améliorer la qualité) : la formulation exacte est que la qualité
plafonne pendant que le risque, lui, continue de monter. **Rapport à notre propre couplage
qualité-fuite (A1)** : voisin par le thème, mais pas une antériorité directe sur notre contribution
— leur découplage oppose qualité agrégée et risque MIA *au sein d'un seul modèle entraîné plus
longtemps* ; le nôtre oppose fidélité individuelle et fuite individuelle *entre 12 méthodes
hétérogènes*, sans qu'on puisse l'exclure d'un simple effet de qualité globale
(`c7-disjoint-resultats.md`). Les deux mécanismes ne sont pas interchangeables : eux montrent que la
qualité agrégée et le risque MIA peuvent diverger dans le temps ; nous montrons qu'à travers des
méthodes différentes, qualité agrégée et fuite individuelle montent ensemble sans qu'on puisse
exclure un axe de qualité globale sans empreinte individuelle. Notre réponse : les trois mesurent une
fidélité **agrégée** (distributionnelle ou d'utilité aval), jamais la correspondance individuelle à
la bonne personne (`c7-compromis-resultats.md`), et aucun ne teste si le couplage qu'ils observent
(ou son absence) résiste à un nul construit sans aucune empreinte individuelle. Notre contribution
sur ce terrain n'est donc pas la preuve d'un axe unique, mais cinq mesures indépendantes : des
taux de liaison mesurés sur deux jeux et en monde ouvert, un canal de fuite nouveau entre jeux de
jumeaux, une mesure en bits transportable, une défense chiffrée, et un couplage qualité-fuite
documenté **mais non distinguable d'un effet de qualité globale**. Sur ce dernier point, l'analyse
de robustesse annoncée — un test préenregistré sur items disjoints, destiné à écarter l'artefact
d'un axe qui ne tiendrait que par construction de l'échantillon des 12 points — est faite : la
corrélation résiste à la disjonction (rho 0,969, IC [0,937 ; 0,993]), mais un nul de marge sans
aucune empreinte individuelle atteint un rho aussi élevé (0,984 en moyenne, 95e centile 1,000), si
bien qu'elle ne réfute pas l'hypothèse d'un simple effet de qualité globale
(`c7-disjoint-resultats.md`). **Réfuté par le test d'auto-réfutation préenregistré du 12/09**
(prédiction principale).

## 6. Notre position

La thèse n'est plus « les jumeaux LLM fuient, contrairement aux prédicteurs statistiques de même
exactitude ». Elle n'est plus non plus « la fidélité d'un jumeau à sa personne et son
identifiabilité sont un seul et même axe » : sur 12 prédicteurs confondus — 8 jumeaux LLM et 4
repères statistiques (Demographics Only, B1, B2, PMM k=10) —, la qualité globale d'imitation et le
taux de ré-identification suivent le même ordre presque parfaitement, y compris quand les deux
sont mesurés sur des items disjoints : Spearman = 0,969, IC 95 % [0,937 ; 0,993], test
préenregistré (`c7-disjoint-resultats.md`). Le contraste à exactitude égale reste vrai (20,7 %
contre 0,23 % pour PMM, `c7-contre-examen-2026-09-11.md` §1). **Mais** un nul de marge — 100
prédicteurs artificiels n'ayant qu'une marge d'exactitude conditionnelle variable par personne,
aucune empreinte individuelle — atteint un rho aussi élevé (0,984 en moyenne, 95e centile 1,000) :
l'observé (0,969) ne le dépasse pas. **Les jumeaux publiés sont reliables à leurs répondants, à des
taux que nous mesurons en monde fermé et en monde ouvert ; la qualité d'imitation et la fuite
montent ensemble ; mais nous ne pouvons pas montrer que ce couplage traduit une empreinte
individuelle spécifique, puisqu'un axe de qualité globale sans empreinte le reproduit déjà.**
**Réfuté par le test d'auto-réfutation préenregistré du 12/09** (prédiction principale) — dans
l'esprit des témoins aveugles récemment exigés pour les attaques d'inférence sur modèles de
fondation (Das, Zhang, Tramèr, arXiv 2406.16201 ; section 3), notre nul de marge est le témoin qui
manquait à ce couplage, pas un aveu de faiblesse.

Cinq apports en découlent. **Premièrement**, des taux de liaison mesurés sur deux jeux et en monde
ouvert, avec leur plafond humain (retest à 81,6 % sur Twin, 96,8 % sur Stanford) : à un taux de
fausses accusations tenable de 1 %, le meilleur jumeau retrouve la bonne personne 3,04 % du temps
sur Twin et 20,39 % sur Stanford, contre environ 0 % pour les mêmes repères statistiques, loin sous
le plafond humain (54,5 % / 90,7 %) mais loin d'être nul (`c7-monde-ouvert-resultats.md`).
**Deuxièmement**, un canal de fuite entre jeux de jumeaux, **mesuré aux deux bouts** : sous pipeline
partagé (même équipe, mêmes fichiers de persona), deux jumeaux de la même personne se désignent
mutuellement sans qu'un attaquant détienne la moindre réponse humaine, dès qu'ils partagent assez
d'items (Twin : 36,4 % à 60 items communs contre 0,06 % de contrôle, `c7-transfert-resultats.md` ;
Stanford : 11,9-13,0 % à 177 items communs contre au plus 0,31 % de contrôle,
`c7-transfert-stanford-resultats.md` ; décomposition sur Twin : 82 % de l'écart au plancher revient à
l'individu, 18 % au segment démographique-idéologique, `c7-temoin-prompt-resultats.md`). Sous
pipeline réellement indépendant — deux organisations dont le modèle, le gabarit de prompt et le
format de persona diffèrent tous les trois — ce canal **disparaît** : top-1 = 1,76 % [0,35 ; 3,63]
sur 142 personnes, sous la baseline démographique seule (9,2 %),
`c7-deux-organisations-resultats.md`, un résultat négatif obtenu et rapporté par nous-mêmes plutôt
que trouvé par un relecteur. Le canal n'a pas d'antériorité qui teste le même scénario ; nos taux
contredisent la conclusion générale d'Anonymeter selon laquelle la linkability est le risque le plus
faible des trois qu'il mesure (section 1), mais **seulement dans le régime pipeline-partagé** — sans
contredire ni sa mesure dans son propre cadre tabulaire, ni sa conclusion dans le régime de
pipelines génuinement indépendants, où notre propre témoin la corrobore. ZAK-MIA (Guan et al.,
PoPETs 2024) est une attaque d'appartenance sur des agrégats de localisation, sans rapport avec la
liaison. La réplication sur un second jeu construit différemment renforce la revendication de
nouveauté du régime pipeline-partagé ; la borne négative sous pipeline indépendant en précise
honnêtement l'étendue. **Troisièmement**, une mesure en bits transportable d'un jeu à l'autre alors que le
taux brut ne l'est pas (facteur 1,34 contre un facteur 3,2 sur le top-1, `c7-bits-resultats.md`),
cadrée comme un instrument dérivé de la min-entropie de Rényi (section 2). **Quatrièmement**, une
défense (D4, section 7), variante chiffrée d'un mécanisme ancien, qui ramène le top-1 de 20,68 % à
0,13 % pour un coût mesuré de 4,4 points sur les corrélations entre items, en préservant exactement
les marges de groupe publiées. **Cinquièmement**, le couplage qualité-fuite lui-même, documenté sur
12 méthodes hétérogènes et robuste à la disjonction des items, mais que nous ne pouvons pas
distinguer d'un effet de qualité globale sans empreinte individuelle (ci-dessus).

À cela s'ajoute une observation transversale, non comptée parmi les cinq apports : des pipelines
réels se placent très différemment sur ces mesures selon la fidélité qu'ils atteignent. Nos propres
jumeaux, produits en un seul appel à des modèles bon marché à partir d'un profil brut,
n'identifient presque personne (0 % à 0,83 %, mémorisation écartée par un contrôle verbatim,
`c7-gen-resultats.md`), quand des agents Stanford construits à partir d'un entretien seul, sans
aucune réponse d'enquête, en identifient 44,7 % sur 1 052, contamination par recopie exclue par un
test de symétrie (`c7-stanford-provenance-resultats.md`). Le risque documenté n'est donc pas une
propriété générique de « donner un profil à un LLM » : nos 7 jumeaux régénérés, testés
spécifiquement sur ce point, atteignent une fidélité (0,05–0,18) de l'ordre des prédicteurs
statistiques naïfs et tombent, sans exception, dans l'intervalle de prédiction de la courbe
fidélité-fuite (`c7-courbe-gen-resultats.md`) : ce n'est pas la recette de fabrication qui décide
de la fuite, c'est le niveau de fidélité qu'elle permet d'atteindre.

## 7. Défenses

Notre défense D4 n'est pas un mécanisme neuf : mélanger les réponses entre unités d'un même
segment est une variante du Post Randomisation Method (PRAM ; Gouweleeuw, Kooiman, Willenborg et de
Wolf, *Journal of Official Statistics* 1998 **[URL stable à confirmer avant dépôt]**), qui perturbe
les variables catégorielles par une matrice de transition connue en laissant les marges invariantes
en espérance, et du data swapping, qui les préserve exactement aux agrégations hautes — la même
famille que la tradition des données partiellement synthétiques de Reiter et Drechsler, prolongée
par Drechsler (2024, arXiv 2409.04257, https://arxiv.org/abs/2409.04257) et Bowen et al. (arXiv
2308.00872, https://arxiv.org/abs/2308.00872). Ce qui est neuf est l'application de ce mécanisme
ancien à des jumeaux LLM, avec une courbe risque-utilité mesurée et non supposée
(`c7-defense-resultats.md`) : mélanger les 40 réponses d'achat entre personnes du même segment
démographique (D4) ramène le top-1 de 20,68 % à 0,13 %, pour 1,47 point de perte d'utilité,
concentrée entièrement sur les corrélations entre items (4,4 points) — distribution par item et
écarts entre groupes restent exacts par construction, comme le prédit le PRAM. Ce compromis se
compare directement à la littérature du DCR (Yao et al., Ganev et De Cristofaro, section 1) qui
interroge le rapport risque/utilité des défenses par similarité : ici le coût mesuré (1,47 point)
est inférieur à l'écart déjà présent entre jumeau non protégé et humains sur ce même indicateur
(5,8 points).

## Objections les plus probables

| Objection | Parade | Expérience à l'appui |
|---|---|---|
| « Tautologie : bien sûr qu'un modèle fidèle à l'individu identifie. » | Objection non écartée sur le fond. Ce qui tient : rien ne prédisait ni la forme ni la force de cette relation avant de la mesurer sur 12 méthodes hétérogènes, et elle survit à la disjonction complète des items utilisés pour chaque axe ; à exactitude marginale égale, deux prédicteurs peuvent fuir à deux ordres de grandeur d'écart (20,7 % contre 0,23 %, A2). Ce qui ne tient plus : un nul de marge sans aucune empreinte individuelle — 100 prédicteurs n'ayant qu'une marge d'exactitude variable par personne — reproduit déjà la force du couplage observé (rho nul 0,984 en moyenne, 95e centile 1,000, contre 0,969 observé). Le couplage qualité-fuite est réel et n'est pas un artefact de calcul recyclé, mais il ne démontre aucune spécificité individuelle : un simple axe de qualité globale suffit, dans l'esprit des témoins aveugles récemment exigés pour les attaques d'inférence (Das, Zhang, Tramèr, arXiv 2406.16201). Test préenregistré, prédiction principale réfutée. | Spearman 0,969 [0,937 ; 0,993] sur items disjoints, nul de marge 0,984 (`c7-disjoint-resultats.md`) ; réplication inter-recettes (`c7-gen-resultats.md`, `c7-stanford-provenance-resultats.md`). **Réfuté par le test d'auto-réfutation préenregistré du 12/09.** |
| « Connu depuis Stadler 2022 / linkability faible selon Anonymeter. » | Stadler et Anonymeter portent sur le tabulaire génératif générique, avec un attaquant détenant des valeurs réelles sur un seul jeu (Anonymeter, section 5.2, p. 319) : scénario différent du nôtre, que nous ne contredisons pas. Leur conclusion générale — « synthetic data exhibits the lowest vulnerability against linkability » (résumé, p. 312 ; confirmé section 6.1, p. 320-321) — est contredite par notre taux **uniquement dans le régime pipeline-partagé** (36,4 %, `c7-temoin-prompt-resultats.md`) ; un témoin à deux organisations réellement indépendantes montre que ce signal disparaît sous pipeline indépendant (1,76 %, sous la baseline démographique de 9,2 %, `c7-deux-organisations-resultats.md`) — dans ce régime, nous corroborons Anonymeter plutôt que de le contredire. Annamalai et al. et Ganev (seul ou avec De Cristofaro) montrent déjà que la DCR sous-estime le risque, mais aucun ne teste des jumeaux LLM catégoriels. ZAK-MIA (Guan et al., PoPETs 2024) est une attaque d'appartenance sur des agrégats de localisation, sans rapport avec la liaison. Notre contre-exemple à la conclusion générale de linkability faible tient donc, mais borné au pipeline partagé, avec un écart de deux ordres de grandeur face à des prédicteurs non-LLM de même exactitude dans ce régime. | PMM/B2/donneur k=1 tous < 0,3 % à exactitude comparable (`c7-contre-examen-2026-09-11.md` §1). |
| « Votre canal inter-jumeaux (A7) n'est qu'un artefact de pipeline partagé, pas un risque de liaison réel. » | Admis et quantifié, pas nié : témoin à deux organisations réellement indépendantes (modèle, gabarit de prompt et format de persona tous distincts) — top-1 = 1,76 % [0,35 ; 3,63] sur n = 142, sous la baseline démographique (9,2 %), signal qui s'affaiblit (pas se renforce) entre n = 82 (3,66 %) et n = 142. A7 ne tient que sous pipeline partagé, où l'apport individuel (17,4 pts) domine largement l'apport de segment (3,8 pts). C'est un résultat négatif obtenu par nous-mêmes, écrit comme limite plutôt que découvert par un relecteur. | `c7-deux-organisations-resultats.md` ; `c7-temoin-prompt-resultats.md`. |
| « Le persona contient déjà les réponses de la vague cible : fuite triviale. » | Audit de provenance : 0 colonne et 0 QID de vague 4 dans le contexte ; symétrie 37,7 % vs 37,9 % ; canal de randomisation écarté. | `c7-contre-examen-2026-09-11.md` §2 ; ablation H3 (`c7-mecanisme-resultats.md`). |
| « Ce n'est pas une vraie ré-identification : il faut déjà tenir les réponses réelles de la cible. » | Assumé explicitement : c'est un résultat de linkability (au sens CAP/TCAP et RGPD/G29), pas une identification à partir d'informations publiques ; scénario de menace = détenteur de panel publiant des jumeaux sans clé. | Modèle de menace, `c7-contre-examen-2026-09-11.md` §4 ; brouillon de divulgation responsable. |
| « Connu depuis 2018 : sur-apprentissage et attaques d'appartenance (Yeom et al.), mémorisation nécessaire à la généralisation (Feldman). » | Ces résultats portent sur un modèle **entraîné** sur la population, avec un écart train/test. Notre pipeline n'entraîne rien : la personne n'appartient à aucun jeu d'entraînement, et la fidélité individuelle vient du conditionnement par persona, pas du sur-ajustement. | Absence de tout entraînement dans le pipeline d'attaque (§3) ; ablation H3 qui localise la fuite dans le motif de réponses, pas dans un modèle appris sur les cibles (`c7-mecanisme-resultats.md`). |

## Note de méthode

Toutes les références ci-dessus ont été vérifiées à la source (page arXiv, Crossref, actes
officiels de la conférence citée) plutôt que reprises de mémoire. La bibliographie BibTeX
correspondante vit dans `article/references.bib`.
