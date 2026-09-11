# B123. Preenregistrement : ce que les baselines gratuites obtiennent sur les metriques vitrines

Ecrit le 11 septembre 2026, avant `analyses/b123_baselines_vendeurs.py` et avant tout calcul.
Zero appel de modele, aucun LLM local. Fusion B1+B2+B3 (`resultats/tri-idees-2026-09-11.md`
section 4.3 ; `resultats/idees-B-industrie-2026-09-11.md`, B1-B3).

**Declaration exigee par le tri.** Le comite a deja vu, sur le GSS (panels 2008/2010, vague 1),
une marge d'une autre cohorte a 0,985 en 1-MAE, 0,978 en KS, 1,0 en Spearman median, et
l'uniforme a 0,836 en 1-MAE (script jetable, non conserve, items non fixes a l'avance). Le
protocole ci-dessous est fige SANS chercher a reproduire ces chiffres ; un ecart sera rapporte tel quel.

## Metriques des vendeurs (definitions de `idees-B-industrie` section 1)
- **1-MAE** (Electric Twin) : 1 − erreur absolue moyenne des proportions par option (K options),
  mediane sur les items.
- **Similarite KS** (PyMC Labs/SSR, arXiv 2510.08338) : 1 − distance de Kolmogorov-Smirnov entre
  CDF sur options ordonnees. Items ordinaux seulement (Twin : type Matrix) ; non calculee sur le
  GSS, ordre indefini pour la plupart des items nominaux — ecart declare.
- **Recouvrement 1-TV** (Artificial Societies, Evidenza) : 1 − demi-somme des ecarts absolus.
- **Spearman median** (Aaru) : correlation de rang entre proportions des K options, mediane sur
  les items. NDAM (Electric Twin) non reconstruite : definition trop vague (regle 5, idees-B §0).

## Baselines et jeux
- **GSS** : panels NORC 2008 et 2010, vague 1, deux cohortes distinctes. Items categoriels
  communs, 2-7 modalites, N >= 200/cohorte. B0 uniforme ; B1 marge de l'autre cohorte ; B2 marge
  par sexe de l'autre cohorte, reponderee par la composition de la cohorte cible.
- **Twin-2K-500** : 108 items, humains vagues 1-3 contre verite vague 4 (retest, memes
  personnes). B0 uniforme ; B1 = persistance (marge vagues 1-3). B2 omise : memes personnes des
  deux cotes, effectifs de segment identiques, B2 serait numeriquement egale a B1.
- **SCE** : hors perimetre de cette passe, faute d'un chargeur simple ; note dans le rapport.

## Sensibilite : bon contre mauvais simulateur
**Item permute** : B1 appliquee a un AUTRE item de meme nombre de modalites. **Camp inverse** :
B1 avec l'ordre des modalites renverse. Une metrique ou ces deux conditions restent proches du
plancher gratuit est peu discriminante, quel que soit son score sur B1.

## Predictions [PARI]
Sur au moins 3 des 4 metriques et au moins 1 des 2 jeux, B1 egale ou depasse le chiffre-vitrine.
Recouvrement et Spearman median restent proches du plancher sous item permute (perte < 30 % vs
B1). 1-MAE se degrade le moins sous camp inverse : metrique jugee la moins discriminante a l'avance.
