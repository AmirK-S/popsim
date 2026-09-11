# Revue adverse de l’outillage R6 et de reproductibilité

Date : 2026-09-11. Revue locale, sans réseau, modèle ni ouverture de trace de campagne.
Les essais emploient uniquement des répertoires temporaires synthétiques.

## A. Analyse fine R6

Après correction, le chargeur refuse avant lecture des traces une campagne sans les 1 250
opérations réglées, ou dont l’ordre F1 894, F2 316, plancher 40 diffère du plan. Il refuse
un centre dans F2, les passes pilote déclarées ou cachées dans une ligne, et une empreinte de
requête ou un fournisseur qui ne correspondent pas à la réservation terminale. Les sorties
restent exploratoires : aucune colonne p, Holm, IC ou verdict; H1 à H3 restent hors script.

Les adversariaux couvrent l’ordre du ledger et des traces, F2, pilote, provenance
trace--ledger, leave-one-item, leave-one-family, strates sous cinq items, séries constantes
et marqueur non déterministe. Le périmètre A2/F2 reste `item × identité`, sans strate par
camp. La revue ne lit ni ne classe aucune sortie R6 réelle.

## B. Paquet public

Le contrôleur refuse désormais les répertoires interdits même vides, liens symboliques,
microdonnées, traces, ledger, `.env`, poids et clés. Le contournement démontré était une clé
placée après 2 Mio dans un fichier texte : le contrôle ne lisait alors que 2 Mio. Il lit
maintenant les fichiers par blocs avec chevauchement sans jamais afficher leur contenu.

Les manifestes ne présentent pas les licences locales inconnues comme certaines et déclarent
explicitement que les versions observées ne sont pas un lockfile. Ils restent un inventaire
local, non une certification juridique ou une reproduction fraîche complète.

## Contrôles exécutés

- `analyses/test_r6_analyse_fine.py` : 8 tests, succès.
- `analyses/test_verifier_paquet_public.py` : 4 tests, succès.
- Test supplémentaire des répertoires interdits vides : succès.
- Compilation Python, validation JSON et `git diff --check` : succès.

Conclusion : GO technique pour ces nouveaux outils, avec les limites déclarées des licences,
de la revue de divulgation et de l’environnement non verrouillé. Aucun run, donnée, trace ou
fichier existant hors des nouveaux livrables n’a été modifié.
