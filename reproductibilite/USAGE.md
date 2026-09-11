# Socle de reproductibilite

Ce dossier documente l'environnement observe et les sources locales sans recopier de
donnees, traces, poids ou secrets. Il ne constitue pas encore une reproduction fraiche :
il n'y a ni lockfile complet, ni manifeste de sorties, ni versions publiees de tous les
poids et executables externes.

## Fichiers

- `sources.json` est le registre machine-readable des jeux et de leur regime de publication.
- `modeles.json` est le registre des references de poids et de leurs empreintes lorsqu'elles
  etaient inscrites dans le code local. `UNKNOWN_LOCAL` impose un releve avant publication.
- `dependances.json` separe les imports directs des dependances transitives observees dans
  l'environnement `.venv` du 11 septembre 2026.
- `../analyses/verifier_paquet_public.py` refuse les donnees, traces, ledger, `.env`,
  motifs de cles et poids dans un candidat d'archive publique.

## Controle avant archivage

Construire l'archive dans un repertoire propre, sans lien symbolique, puis executer :

```sh
.venv/bin/python analyses/verifier_paquet_public.py /chemin/vers/paquet-public
```

Le code 0 signifie seulement qu'aucune categorie interdite connue n'a ete detectee. Il ne
certifie ni les licences, ni l'absence de risque de reidentification dans les agregats. La
revue humaine doit encore verifier les petites cellules, le texte libre, les dates fines,
les identifiants de jointure, les notices de source et le commit effectivement archive.

## Deux paquets cibles

Le paquet minimal Twin contient du code, des fixtures synthetiques, ces manifestes et un
telechargeur a revision/hash explicites; il ne contient aucune copie des personnes. Le
paquet complet expose des adaptateurs qui exigent des entrees detenues sous licence par le
chercheur. Dans les deux cas, les poids et les appels de modeles sont optionnels et ne
doivent pas etre necessaires pour executer les tests synthetiques.
