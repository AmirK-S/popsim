# <titre>

statut: courant | perime_par: <fichier> | retracte_par: <fichier>
fait_foi: <fichier>                       # obligatoire si retracte
mandat: <question à trancher, une ligne>
agent: <modèle>, <fournisseur>
ecriture: <liste de fichiers>             # comparée à git show --stat
lecture_seule: tout le reste
interdits: appel payant sans GO, réseau, commit sur master, arrière-plan
cecite: <ce que cet agent n'a pas vu>     # obligatoire pour les passes aveugles
cout_reel_usd: <valeur lue dans le grand livre, pas estimée>

---

## Déclarer qu'un rapport est invalidé : le marqueur de rétractation

Un rapport qui en invalide un autre **le déclare**, il ne le laisse pas deviner. Dans le corps
du rapport qui invalide, une **ligne entière**, à la **colonne 0** :

```
RETRACTE: resultats/<fichier>.md
INVALIDE: resultats/<fichier>.md      # synonyme strict, même effet
```

Règles de forme, toutes vérifiées par la porte P4 (`outils/portes/entetes.py --retractation`) :

- mot-clé en **capitales**, un **seul fichier par ligne**, **chemin complet** depuis la racine ;
- **rien d'autre sur la ligne** — ni phrase, ni ponctuation, ni justification (celles-ci vont
  dans les lignes qui précèdent ou qui suivent) ;
- le fichier nommé doit **exister** : un marqueur mal formé ou pointant dans le vide **fait
  échouer la porte**, il n'est jamais ignoré en silence ;
- dans le **même commit**, le fichier nommé doit recevoir `retracte_par:` (ou `perime_par:`) et
  `fait_foi:` dans son en-tête. Le toucher sans poser l'en-tête ne suffit pas.

**Pour citer le marqueur sans le déclencher** — documentation, rapport qui *parle* de
rétractations — l'indenter de quatre espaces ou l'encadrer de backticks : la ligne ne commence
alors plus par le mot-clé, et la porte ne la voit pas.

**Ce que la porte ne voit pas, et c'est assumé :** une invalidation écrite en prose **sans**
marqueur passe sans un mot. La règle n'est opposable qu'à qui pose le marqueur ; poser le
marqueur fait partie du travail d'invalider. `--indice-prose` rejoue l'ancien filet large en
notes non bloquantes, à l'usage d'un relecteur.
