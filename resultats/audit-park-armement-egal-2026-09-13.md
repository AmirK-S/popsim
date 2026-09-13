# Audit — Park à armement égal : que reste-t-il au jumeau quand le comparateur démographique porte la même arme ?

statut: courant
mandat: Reproduire independamment les 85,17 % et 29,09 % du volet T1a §1g, produire le tableau a armement egal (jumeau et comparateur demographique, attaque naive et A-LLR, monde ferme et monde ouvert, Park et Twin, bassin strictement constant), trancher ce qui reste au jumeau sur Park, tester l'explication par le nombre d'items, et nommer ce que le comparateur demographique exploite reellement.
agent: audit / Park armement egal, 13/09
ecriture: analyses/c7_park_armement_egal.py, resultats/audit-park-armement-egal-2026-09-13.md, resultats/c7-park-armement-egal.csv
lecture_seule: tout le reste du depot
interdits: appel de modele paye, reseau, recherche web, arriere-plan, commit sur master, fusion, modification d'un script existant, toute ecriture dans article/manuscrit.md et resultats/article-synthese.md
cecite: Aucune verification reseau. Les valeurs 85,17 % / 29,09 % / 90,40 % / 60,17 % annoncees par la branche agent/mesures/t1a-complements ne servent qu'a la verification de raccordement ; aucune n'est recopiee dans un calcul.
cout_reel_usd: 0.00

---

> ## AVERTISSEMENT — POST HOC, NON PRÉENREGISTRÉ AU SENS DE C7
>
> Cet audit est déclenché **après** une mesure de révision (T1a §1g), elle-même post-hoc.
> Le §0 ci-dessous fixe prédictions et critères de réfutation **avant le premier calcul**,
> mais pour une question **choisie après coup**. Il ne compte dans aucun dénominateur de
> multiplicité préenregistré et ne peut réfuter aucune prédiction préenregistrée d'origine.

---

## 0. PRÉENREGISTREMENT — écrit et commité avant le premier calcul

### 0.1 Conventions fixées d'avance

**Départage des ex æquo.** Dans ce projet, cette seule convention fait varier un taux d'un
facteur 130. Elle est donc fixée ici, avant tout calcul, et vaut pour **toutes** les
cellules du tableau, cible comme comparateur, naïf comme A-LLR, Park comme Twin :

- **Convention publiée, retenue pour tous les chiffres de tête** : espérance sous départage
  uniforme dans la classe d'ex æquo de tête, `1/|classe|` si la vraie personne est dans la
  classe de tête, 0 sinon. Calcul **exact et déterministe** (tolérance `1e-12`), pas une
  moyenne de tirages.
- **Deux bornes encadrantes publiées à côté, pour chaque cellule** : `en_faveur` (compte
  dès que rien n'est strictement meilleur) et `contre` (compte seulement si la classe de
  tête est un singleton).
- La variante à 20 tirages aléatoires de `rangs_depuis_accord` est calculée **en plus**,
  pour le seul raccordement à la chaîne publiée.

**Bassin.** Un chargement par jeu, un seul, partagé par la cible et par le comparateur :
mêmes personnes attaquées, même pool, mêmes colonnes d'items. Conformité au chargeur
canonique `c7_fort_monde_ouvert_ic` vérifiée par assertion, arrêt si écart.

**Monde ouvert.** Marge top1−top2 en deux régimes, TPR en escalier exact aux FPR cibles
0,1 % et 1 %, valeur `np.interp` publiée à côté. Protocole `c7_monde_ouvert` repris sans
modification.

**Intervalles.** Bootstrap 2 000 sur les **personnes**, graine `20260913` dérivée du nom de
la mesure. Pour les rapports cible/comparateur : bootstrap **apparié** (les mêmes personnes
rééchantillonnées simultanément pour les deux conditions), 2 000 tirages.

**Baseline.** Tout taux sort avec la baseline recalculée dans **exactement** la même
condition (même bassin, mêmes items, même attaque, même convention de départage).

**Contrôle d'interprétabilité** : `analyses/c7_controle_interpretabilite.py`, règle
inchangée — le candidat passe seulement si la borne basse de son IC est **strictement**
supérieure à la borne haute de l'IC du comparateur, les deux sous la **même** attaque et
le **même** bassin. Appliqué avant toute interprétation.

**Aucune donnée individuelle** n'est calculée, imprimée ni écrite : ni identifiant, ni
appariement, ni cellule démographique d'une personne. Seuls des agrégats sortent.

### 0.2 Prédictions et critères de réfutation

| # | Prédiction (avant calcul) | Ce qui la réfute |
|---|---|---|
| **P1** | Je reproduis, indépendamment de `c7_t1a_complements`, le top-1 monde fermé du comparateur démographique armé sur Park à **85,17 % ± 0,50 pt** et son TPR@1 % à **29,09 % ± 1,00 pt**. | Un écart au-delà de ces tolérances. **Si P1 est réfutée, je m'arrête là et le livrable est cette non-reproduction** — je ne conclus rien d'autre. |
| **P2** | À armement égal sur **Park**, en monde fermé, le rapport cible/comparateur est **≤ 1,15×** et les IC à 95 % des deux top-1 **se recouvrent**. | Rapport ≥ 1,30× avec IC disjoints. Alors un écart survit et je le publie avec son intervalle. |
| **P3** | Le top-1 A-LLR du **comparateur démographique** sur Park **croît de façon monotone** avec le nombre d'items retenus (20, 40, 60, 100, 177), à bassin constant, et le rapport cible/comparateur **décroît** sur la même grille. | Courbe plate (étendue < 5 pts entre k=20 et k=177) ou non monotone. Alors l'explication par le nombre d'items est fausse et il faut chercher ailleurs. |
| **P4** | Le comparateur démographique identifie parce que les **cellules démographiques de Park sont quasi uniques** : je prédis que **plus de 30 %** des personnes du pool Park sont **seules** dans leur cellule exacte (genre × race × âge × éducation). | Moins de 10 % de personnes isolées. Alors l'unicité de cellule n'est pas le mécanisme, et il faut l'attribuer à des items fortement déterminés par la démographie. |
| **P5** | Le top-1 armé du comparateur (85 %) **dépasse largement** le plafond que donnerait la seule cellule démographique, `moyenne(1/|cellule|)` — c'est-à-dire que A-LLR extrait plus que l'appartenance de cellule. | Le top-1 armé est **inférieur ou égal** à ce plafond : alors le comparateur ne fait que relire la cellule, et il n'y a rien de plus. |

### 0.3 Règle d'arrêt

Si P1 est réfutée, l'audit s'arrête au §1 et ne produit ni tableau ni interprétation.
**Aucune conclusion en faveur de l'article par défaut** : si le rapport sur Park est
proche de 1 avec IC recouvrants, la phrase du manuscrit sur Park doit être retirée ou
requalifiée, et le rapport le dit explicitement.

---

*(Sections 1 à 6 écrites après le calcul.)*
