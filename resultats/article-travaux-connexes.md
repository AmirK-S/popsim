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
**Ce qui nous distingue :** Ko et al. et Lermen et al., comme Carlini et Staab, partent de texte
libre porteur d'indices sémantiques directs (un lieu, une habitude décrite en mots), agrégés par un
agent qui raisonne sur ce texte. Notre canal est plus étroit et plus sec : un vecteur de réponses
catégorielles à choix fermés (achète / n'achète pas), sans texte libre, sans raisonnement agentique
et sans mémorisation, établi par ablation en H3 (`c7-mecanisme-resultats.md`).

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

## 5. Notre position

Trois éléments résistent à « c'est connu depuis 2022 ». **L'entrée de l'attaque** ne contient
aucune donnée réelle de la cible, seulement une sortie de modèle conditionnée sur un persona ;
l'attaquant compare cette sortie à des réponses qu'il détient déjà par ailleurs (modèle de menace,
`c7-contre-examen-2026-09-11.md` §4). **Des baselines internes** de même exactitude échouent où le
jumeau réussit : Demographics Only (2,13 %), PMM k=10 (0,23 %), B2 argmax (0,07 %) restent sous
3 % quand JSON Persona GPT4.1 atteint 20,7 % (retest humain 81,6 %) ; sur l'archive Stanford,
65,7 % contre 2,26 % démographique et 0,095 % au hasard. **Le canal de fuite est localisé par
ablation**, non supposé : permuter les 40 réponses d'achat fait chuter le top-1 de 33,1 % à
0,046 %, sous le hasard (`c7-mecanisme-resultats.md`) ; l'audit de provenance exclut une fuite de
la vague cible (0 colonne, symétrie 37,7 %/37,9 %).

## 6. Défenses

Réduire la fuite sans détruire l'utilité est testé, pas supposé (`c7-defense-resultats.md`) :
mélanger les 40 réponses d'achat entre personnes du même segment démographique (D4) ramène le
top-1 de 20,68 % à 0,13 %, pour 1,47 point de perte d'utilité, concentrée entièrement sur les
corrélations entre items (4,4 points) — distribution par item et écarts entre groupes restent
exacts par construction. Ce compromis se compare directement à la littérature du DCR (Yao et al.,
Ganev et De Cristofaro) qui interroge le rapport risque/utilité des défenses par similarité : ici
le coût mesuré (1,47 point) est inférieur à l'écart déjà présent entre jumeau non protégé et
humains sur ce même indicateur (5,8 points).

## Objections les plus probables

| Objection | Parade | Expérience à l'appui |
|---|---|---|
| « Connu depuis Stadler 2022 / linkability faible selon Anonymeter. » | Stadler et Anonymeter portent sur le tabulaire génératif générique ; Annamalai et al. et Ganev (seul ou avec De Cristofaro) montrent déjà que la DCR sous-estime le risque, mais aucun ne teste des jumeaux LLM catégoriels. Notre taux est un contre-exemple frontal à la conclusion de linkability faible, avec un écart de deux ordres de grandeur face à des prédicteurs non-LLM de même exactitude. | PMM/B2/donneur k=1 tous < 0,3 % à exactitude comparable (`c7-contre-examen-2026-09-11.md` §1). |
| « Le persona contient déjà les réponses de la vague cible : fuite triviale. » | Audit de provenance : 0 colonne et 0 QID de vague 4 dans le contexte ; symétrie 37,7 % vs 37,9 % ; canal de randomisation écarté. | `c7-contre-examen-2026-09-11.md` §2 ; ablation H3 (`c7-mecanisme-resultats.md`). |
| « Ce n'est pas une vraie ré-identification : il faut déjà tenir les réponses réelles de la cible. » | Assumé explicitement : c'est un résultat de linkability (au sens CAP/TCAP et RGPD/G29), pas une identification à partir d'informations publiques ; scénario de menace = détenteur de panel publiant des jumeaux sans clé. | Modèle de menace, `c7-contre-examen-2026-09-11.md` §4 ; brouillon de divulgation responsable. |

## Note de méthode

Toutes les références ci-dessus ont été vérifiées à la source (page arXiv, Crossref, actes
officiels de la conférence citée) plutôt que reprises de mémoire. La bibliographie BibTeX
correspondante vit dans `article/references.bib`.
