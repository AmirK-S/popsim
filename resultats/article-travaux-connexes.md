# Travaux connexes (brouillon prêt à traduire)

Sources locales utilisées : `resultats/veille-anteriorite-2026-09-11.md`, `resultats/c7-resultats.md`,
`resultats/c7-contre-examen-2026-09-11.md`, `resultats/c7-mecanisme-resultats.md`,
`resultats/c7-stanford-resultats.md`, `resultats/a13-positionnement-contribution.md`,
`resultats/divulgation-responsable-brouillon.md`. Le fichier `positionnement-vie-privee-2026-09-12.md`
n'existe pas encore dans le dépôt : non attendu, comme demandé. Les références hors de ces
rapports (sections 1 à 4) viennent de la consigne elle-même ; celles sans identifiant vérifié
localement sont marquées **[à vérifier avant dépôt]** plutôt qu'inventées.

## 1. Vie privée des données synthétiques

Stadler, Oprisanu et Troncoso (USENIX Security 2022, *Synthetic Data – Anonymisation Groundhog
Day*, https://arxiv.org/abs/2011.07018) montrent que des données tabulaires générées restent
reliables à leurs enregistrements sources, et que les métriques de similarité vendues comme
« preuve d'anonymat » ne le garantissent pas. Anonymeter (Giomi et al., arXiv 2211.10459,
https://arxiv.org/abs/2211.10459 — déjà cité dans `c7-contre-examen-2026-09-11.md`) formalise
trois attaques de liaison (singling out, linkability, inference) devenues standard pour le
tabulaire de synthèse ; sa composante de linkability est jugée faible par la littérature
ultérieure, notamment Annamalai et al. (2024) et Ganev et De Cristofaro, qui montrent que des
attaques par reconstruction battent les métriques de type distance-au-plus-proche-voisin (DCR)
sur des données dites « vraiment anonymes » **[à vérifier avant dépôt : identifiants arXiv exacts
non retrouvés localement]**. Un SoK NIST 2026 sur la vie privée des données synthétiques est cité
dans la consigne mais absent des veilles locales **[à vérifier avant dépôt]**.
**Ce qui nous distingue :** tout ce corpus porte sur des microdonnées tabulaires générées par des
modèles génératifs classiques (GAN, modèles de copules, diffusion tabulaire). Notre objet est
différent : des textes ou JSON produits par un LLM conditionné sur une personne, où l'attaque ne
dispose d'aucune métrique de similarité continue mais d'un vecteur de réponses catégorielles à
un questionnaire.

## 2. Ré-identification de données réelles

Narayanan et Shmatikov (IEEE S&P 2008, *Robust De-anonymization of Large Sparse Datasets*,
https://arxiv.org/abs/cs/0610105) ré-identifient des utilisateurs Netflix à partir d'un petit
nombre de notes. De Montjoye et al. (*Science* 2015, doi 10.1126/science.1256297) montrent que
quatre points spatio-temporels suffisent à ré-identifier 95 % des personnes dans des métadonnées
de carte bancaire. Rocher, Hendrickx et de Montjoye (*Nature Communications* 2019, doi
10.1038/s41467-019-10933-3) donnent un modèle génératif pour estimer le risque de
ré-identification dans un échantillon incomplet. Une « loi d'échelle » 2025 sur la
ré-identification est mentionnée dans la consigne mais aucun rapport local ne la documente
**[à vérifier avant dépôt]**.
**Ce qui nous distingue :** ces travaux ré-identifient à partir de vraies données auxiliaires
publiques ou quasi publiques (notes de films, déplacements, achats réels). Chez nous, l'entrée de
l'attaque n'est jamais une donnée réelle de la cible : c'est une sortie de modèle générée à partir
d'un persona, comparée ensuite aux vraies réponses détenues par l'attaquant. Le canal de fuite est
donc un modèle statistique appris, pas une trace comportementale directe.

## 3. Vie privée et LLM

Carlini et al. (USENIX Security 2021, *Extracting Training Data from Large Language Models*,
arXiv 2012.07805, https://arxiv.org/abs/2012.07805) montrent qu'un LLM peut mémoriser et régurgiter
des séquences d'entraînement identifiantes. Staab, Vero, Balunović et Vechev (ICLR 2024, *Beyond
Memorization: Violating Privacy via Inference with LLMs*, arXiv 2310.07298,
https://arxiv.org/abs/2310.07298) montrent qu'un LLM infère des attributs personnels (localisation,
revenu, genre) à partir de texte libre anodin. Deux dé-anonymiseurs agentiques de 2026 sont cités
dans la consigne, arXiv 2603.18382 (https://arxiv.org/abs/2603.18382) et arXiv 2602.16800
(https://arxiv.org/abs/2602.16800) **[titres et auteurs à vérifier avant dépôt, non retrouvés dans
les veilles locales]** ; `c7-contre-examen-2026-09-11.md` cite dans le même registre arXiv 2601.05918,
ré-identification par agents LLM sur du texte et le web.
**Ce qui nous distingue :** Carlini et Staab partent de mémorisation ou de texte libre contenant
des indices sémantiques directs (un lieu, une habitude décrite en mots). Notre canal est plus
étroit et plus sec : un vecteur de réponses catégorielles à choix fermés (achète / n'achète pas),
sans aucun texte, sans aucune mémorisation nécessaire — établi par ablation en H3
(`c7-mecanisme-resultats.md`).

## 4. Simulation de répondants et jumeaux

Argyle et al. (*Political Analysis* 2023, *Out of One, Many*, arXiv 2209.06899,
https://arxiv.org/abs/2209.06899) lancent l'usage de LLM comme substituts de panels humains. Park
et al. (2024, arXiv 2411.10109) construisent 1 052 agents génératifs à partir d'entretiens et
restreignent l'accès aux réponses individuelles « pour raison de vie privée » — un risque anticipé
mais jamais mesuré (`c7-contre-examen-2026-09-11.md`, §5). Toubia et al. (2025, Twin-2K-500, arXiv
2505.17479) publient le panel de 2 058 jumeaux que nous attaquons ; leur papier « ne traite ni vie
privée ni liaison » (même source). Peng et al. (2509.19088, *Digital Twins as Funhouse Mirrors*)
documentent des distorsions de fidélité de groupe sur ce même panel, sans lien avec la
ré-identification.
**Ce qui nous distingue :** aucun de ces quatre travaux, ni les cinq travaux de la veille
d'antériorité du 11 septembre (Ahn et al. 2608.29455, Wang et al. 2609.07987, Chen et al.
2607.26348, Choi et al. 2606.28963, `resultats/veille-anteriorite-2026-09-11.md` §2) ne mesure de
taux de ré-identification à partir de sorties de jumeaux. C'est le trou que nous comblons.

## 5. Notre position

Trois éléments résistent à l'objection « c'est connu depuis 2022 ». **Premièrement**, l'entrée de
l'attaque ne contient aucune donnée réelle de la cible, seulement une sortie de modèle conditionnée
sur un persona ; l'attaquant compare cette sortie à des réponses réelles qu'il détient déjà par
ailleurs (modèle de menace détaillé dans `c7-contre-examen-2026-09-11.md` §4 et le brouillon de
divulgation responsable). **Deuxièmement**, des baselines internes de même exactitude échouent où
le jumeau réussit : Demographics Only (2,13 %), PMM k=10 (0,23 %) et B2 argmax (0,07 %) restent
sous 3 % quand JSON Persona GPT4.1 atteint 20,7 % sur Twin-2K-500, et le retest humain plafonne
l'ensemble à 81,6 % (`c7-contre-examen-2026-09-11.md` §1). Sur l'archive Stanford, le même patron
se reproduit à plus grande échelle : 65,7 % contre 2,26 % démographique et 0,095 % au hasard
(`c7-stanford-resultats.md`). **Troisièmement**, le canal de fuite est localisé par ablation et non
supposé : H3 montre que permuter l'ordre des 40 réponses d'achat fait chuter le top-1 de 33,1 % à
0,046 %, sous le hasard (`c7-mecanisme-resultats.md`) ; H1 et H4 excluent l'entropie par item et la
stéréotypie de segment comme explications ; l'audit de provenance exclut une fuite de la vague
cible dans le contexte (0 colonne, symétrie 37,7 %/37,9 %, `c7-contre-examen-2026-09-11.md` §2).

## Objections les plus probables

| Objection | Parade | Expérience à l'appui |
|---|---|---|
| « Connu depuis Stadler 2022 : les synthétiques sont reliables. » | Stadler traite du tabulaire génératif générique avec métrique de similarité continue ; nous mesurons un taux de ré-identification catégoriel propre aux jumeaux LLM, avec un écart de deux ordres de grandeur face à des prédicteurs non-LLM de même exactitude. | Comparateurs PMM/B2/donneur k=1, tous < 0,3 % à exactitude comparable (`c7-contre-examen-2026-09-11.md` §1). |
| « Le persona contient déjà les réponses de la vague cible : c'est une fuite triviale, pas un signal. » | Audit de provenance : 0 colonne et 0 QID de vague 4 dans le contexte des baselines ; test de symétrie sur les jumeaux (37,7 % vs 37,9 %, sans biais vers la vague cible) ; canal de randomisation écarté. | `c7-contre-examen-2026-09-11.md` §2, réplique par ablation H3 (`c7-mecanisme-resultats.md`). |
| « Ce n'est pas une vraie ré-identification : il faut déjà tenir les réponses réelles de la cible. » | Exact, et assumé explicitement : c'est un résultat de linkability au sens RGPD/G29 (fichier reliable à ses microdonnées sources), pas une identification à partir d'informations publiques ; le scénario de menace est un détenteur de panel publiant des jumeaux sans clé. | Modèle de menace explicite, `c7-contre-examen-2026-09-11.md` §4 ; brouillon de divulgation responsable aux auteurs de Twin-2K-500. |

**Trous à combler avant dépôt :** identifiants exacts pour Annamalai et al. 2024, Ganev et De
Cristofaro, le SoK NIST 2026, la « loi d'échelle » 2025, et les deux dé-anonymiseurs agentiques
(2603.18382, 2602.16800) — aucun n'est documenté dans les veilles locales ; à vérifier mot à mot
avant citation, comme le recommande déjà `veille-anteriorite-2026-09-11.md` pour les sources lues
en résumé.
