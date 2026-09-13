# Audit : le contraste jumeau / comparateur avantagé dépend-il du choix de k ? (13 septembre 2026)

statut: préenregistrement (section 0 seule) — résultats à suivre, dans un commit ultérieur
mandat: trancher l'objection n°3 (R3) de `resultats/relecture-post-nuit-2026-09-13.md` : le donneur k=1 ajusté sur le bloc cible fait 0,00 % en top-1 mais 53,2 % en top-10, au-dessus du jumeau (42,7 %) ; la comparaison centrale du §5.2 serait « un fait sur la métrique »
agent: Claude Opus 5, Anthropic — sous-agent audit dépendance top-k
ecriture: analyses/c7_audit_dependance_topk.py, resultats/audit-dependance-topk-2026-09-13.md, resultats/c7-audit-dependance-topk.csv
lecture_seule: tout le reste du dépôt, article/ compris
interdits: appel payant, réseau, recherche web, arrière-plan, commit sur master, fusion, écriture dans article/, impression de tout identifiant / réponse / appariement individuel
cout_reel_usd: 0.00

---

## 0. Préenregistrement — écrit et commité AVANT le script et avant tout calcul

**Statut honnête.** Ce test est **post-hoc** au sens fort : le résultat qu'il interroge (0,00 % /
53,2 %) est connu depuis le 12/09 02:17 (commit `0ea9668`), et je l'ai lu avant d'écrire ces
lignes. Ce qui est préenregistré ici, ce sont mes prédictions sur les quantités **nouvelles**
(courbe top-k complète, AUC de rang, AUC à segment constant du donneur, top-1 du donneur une fois
ses propres donneurs retirés du bassin, monde ouvert du donneur), qui n'ont jamais été calculées.

### 0.1 Comparateur visé
« Donneur plus proche voisin (ajusté sur bloc cible), k=1 », `analyses/c7_synth_ajuste.py`,
`c_poids` = 0,01 (calibration publiée), exactitude 0,584 ; bassin 2 058 humains vague 4, 60 items
de `items_communs`, attaque naïve `rangs_attaque` (20 tirages de départage, graine
`[20260912, crc32("donneur"), 500]`). Jumeau : `JSON Persona - GPT4.1`, même bassin, même attaque.
Baseline : `Demographics Only - GPT4.1-mini`.

### 0.2 Ce que je lis dans la construction avant de calculer
Pour la personne i et l'item j, le donneur est la personne d'entraînement la plus proche de i
**sur ses 59 autres réponses vraies au bloc cible**. Le vecteur synthétique est donc un patchwork
de réponses vraies d'**autres membres du bassin**, choisis parce qu'ils ressemblent à i sur le bloc
attaqué. Deux conséquences attendues :
- l'information portée est **individuelle** (elle est calculée à partir des réponses de i), pas
  seulement de segment ;
- les donneurs **sont eux-mêmes candidats** dans le bassin : le vecteur synthétique leur ressemble
  mécaniquement (ils lui ont fourni ses réponses), et ils doivent occuper le rang 1 à la place de i.

### 0.3 Prédictions chiffrées
- **P0 (reproduction).** Donneur : top-1 0,00 %, top-10 53,2 % ± 0,5 pt. Jumeau : 20,7 % / 42,7 %.
- **P1 (courbe).** Le donneur passe devant le jumeau entre k = 2 et k = 10 ; il reste devant pour
  tout k ≥ 10 ; son AUC de rang est **supérieure ou égale** à celle du jumeau.
- **P2 (segment constant) — prédiction contraire à l'hypothèse du mandat.** Le donneur **ne**
  retombe **pas** au hasard à segment constant : AUC intra-segment (S_gra) ≥ 0,85, borne basse
  > 0,55. L'explication « information de segment » est prédite **fausse**.
- **P3 (masquage par les donneurs, test nouveau).** Si l'on retire du bassin de chaque personne
  les seules personnes qui lui ont servi de donneurs (au plus 60), le top-1 du donneur remonte
  au-dessus de 20 %.
- **P4 (monde ouvert).** TPR du donneur à FPR = 1 % ≈ 0 (≤ 0,5 %), sous attaque naïve comme forte.
  **Je note d'avance que ce n'est pas une confirmation indépendante** : le TPR de `roc_et_taux`
  ne compte que les attaques dont le rang 1 est correct, il est donc borné par le top-1.

### 0.4 Critère de verdict, fixé maintenant
- **L'objection tombe pour une raison de segment** si l'AUC intra-segment du donneur a sa borne
  haute < 0,55 pendant que celle du jumeau reste ≥ 0,85.
- **L'objection tient sur le fond** (le donneur porte un signal individuel que le top-1 ne voit
  pas) si la borne basse de l'AUC intra-segment du donneur est > 0,55. Dans ce cas, le 0,00 % ne
  peut plus être présenté comme une preuve que le comparateur « fuit moins », et l'article doit
  reformuler.
- **Si P3 tient** (top-1 hors donneurs ≥ 20,7 %), le 0,00 % est un **artefact de construction**
  (le comparateur copie des membres du bassin), et le contraste du §5.2 au top-1 ne mesure pas
  une moindre fuite individuelle du comparateur.
- Aucune issue n'est déclarée favorable à l'article par défaut ; le §5 du rapport dira laquelle
  est observée, et la phrase pour le §5.2 en découlera.

### 0.5 Métrique principale : ce que je vérifierai dans git
Si la définition de menace du manuscrit (T1) et le choix du top-1 / monde ouvert comme mesure
principale sont **antérieurs** au commit `0ea9668`. Si seul un texte postérieur existe, je le
dirai.
