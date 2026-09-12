# <chantier>-<expérience> — préenregistrement

statut: courant
famille: <chantier>          # premier de la famille : nb_max_experiences: N, porte_titre: <id>
rang: primaire | secondaire | exploratoire
commit_parent: <sha>
horodatage_ots: preuves/<fichier>.ots

## 1. Question et résultat qui réfuterait
## 2. Instrument
   contrôle : <nom>, seuil : <…>, vu échouer sur : <fichier de test / cas>
## 3. Famille de tests
   hypothèses H1..Hk, hiérarchie, correction (Holm | BH), gatekeeping
## 4. Prédictions chiffrées avec intervalle a priori
## 5. Règle de décision — toutes les issues, dont « rien montré »
## 6. Paramètres figés
   graines, n_replicats, plafond USD, modèles, versions, durée estimée
## 7. Clause de réduction
   paramètre : <--replicats>, règle : toute valeur réduite porte n_replicats dans le registre
## 8. Clauses
   Aucun autre seuil n'est ajouté après coup. Le résultat rapporté est celui obtenu.
   Aucun appel n'a eu lieu au moment où ce fichier est écrit et commité.
