# C7-recette, preenregistrement : la fuite tient-elle a la granularite de l'appel ?
**Ecrit le 12 septembre 2026, avant tout appel substantiel.** Etude de vie privee sur
Twin-2K-500 (deja public). Aucun pid ecrit dans resultats/, seuls des taux agreges.
**Transparence de sequence** : 5 appels de calibrage reels (2 "appel unique", 3 "appel
par item", meme personne/items), cout mesure 0,0090 USD, AVANT ce texte, pour fixer N.
Reponses lues seulement pour verifier le format ("5","5","5") : aucune hypothese
ci-dessous n'a ete ajustee sur du contenu.
## Plan (un seul facteur : granularite, modele fixe)
Un seul modele, `openai/gpt-4.1-mini` (classe Twin), temperature 0. Memes 60 personnes
(graine 20260912, `c7_gen.charger_personnes`) et memes 60 items (`c7_gen.charger_items`
= `c7_reidentification.items_communs`) que l'attaque C7. Profil riche R1 (texte
vagues 1-3, tronque a 8000 caracteres), identique aux deux bras :
- **Appel unique** : 60 reponses en un seul appel (`c7_gen.construire_prompt`, R1, repris
  tel quel).
- **Appel par item** : un appel par question (60 appels/personne), persona + UNE
  question, reponse numerique seule -- structure inspiree du notebook public de l'equipe
  (persona, question, consigne "un seul chiffre"), paraphrasee, pas copiee.
## Taille
Cout mesure au calibrage : ~0,0037 USD/appel unique ; ~0,0010 USD au 1er appel item puis
~0,00032 USD/appel (mise en cache du prefixe persona). Projection N=40 : ~0,95 USD, sous
le plafond. **N cible = 40.** Si l'arret dur a 1,00 USD tronque le bras item, l'analyse
porte sur le sous-ensemble reellement complete, signale comme tel.
## Prediction chiffree
L'appel par item fait monter le top-1 d'au moins un facteur 5 vs l'appel unique, a
modele et personnes egaux.
## Limites
Peu de cibles (40) : IC larges attendus. Pool de candidats = 2 058 humains (seules les
personnes attaquees sont un sous-ensemble). Un seul modele, un seul jeu.
Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
