# C7, generateurs individualises : preenregistrement (12 septembre 2026)
**Ecrit avant tout calcul.** Objection tranchee (`c7-contre-examen-2026-09-11.md`) : PMM et
B2 sont des PREDICTEURS qui tendent vers le mode, pas des GENERATEURS individualises ; un
relecteur dira que tout generateur conditionne sur la personne identifierait autant.
## 1. Generateurs (`analyses/c7_generateur.py`), conditionnes sur le contexte de
`t1_baselines` (494 items de vagues 1-3 + 14 demographies), jamais sur les 60 items cibles :
- **G-LR** : regression logistique multinomiale par item, TIRAGE dans la distribution
  predite (temperature T) au lieu de l'argmax. Difference cle avec B1/B2/PMM.
- **G-copule** : memes probabilites personnalisees que G-LR, mais les 60 tirages d'une meme
  personne sont correles par une copule gaussienne (scores normaux par rang, correlation
  estimee sur le pli d'entrainement seul).
- CART sequentiel (`synthpop`) : absent de l'environnement Python -> non teste.
## 2. Calibration
Balayage de temperature (0,02 a 3), exactitude sur les 60 items, cible = 0,590 (JSON Persona
GPT4.1). [HYPOTHESE] Risque anticipe : un LR sur ce contexte a deja plafonne a 0,475 en argmax
dans le contre-examen (throwaway hors depot) ; si nos generateurs restent sous 0,590, le T le
plus proche de la cible est retenu quand meme et l'ecart est rapporte tel quel.
## 3. Attaque et mesures
`c7_reidentification.rangs_attaque` importee sans modification (pool = 2 058 humains vague 4,
60 items), 5 tirages de generation par generateur, IC par `a2_commun.bootstrap_personnes`,
top-1, top-10, rang median.
## 4. Predictions chiffrees et les trois issues
[HYPOTHESE] exactitude plafonnant vers 0,48-0,55, top-1 attendu **< 1 %**, proche de PMM
(0,23 %) et B2 (0,07 %), loin des 20,7 % du jumeau.
- (a) top-1 >= 10 % ou >= moitie du jumeau -> generateurs individualises fuient en general,
  publiable mais titre a changer.
- (b) top-1 << jumeau, comme predit -> specificite LLM confirmee, resultat fort.
- (c) top-1 > jumeau -> la structure de dependance entre items identifie, pas le modele.
