# Caricature x richesse du profil, resultats

Calcule avec `analyses/caricature_profil.py`, apres le preenregistrement du meme nom. Camp =
ideologie QID22 (gauche/droite), 909 gauche / 567 droite. 98 items sur 108 retenus (ecart
humain >= 0,02, identique pour toutes les configs). 8 configurations admissibles de l'audit
de provenance. Bootstrap 2 000 replicats (personnes intra-camp puis unites item x config).

## Par configuration (mediane sur 98 items)

| configuration | niveau | facteur d'exageration | compression |
|---|---|---|---|
| Demographics Only | minimal | 0,74 | 0,69 |
| JSON Persona GPT4.1 | riche | 0,68 | 0,78 |
| JSON Persona GPT4.1-mini | riche | 0,64 | 0,70 |
| Text Persona temp. defaut | riche | 0,48 | 0,74 |
| Text Persona raisonnement | riche | 0,58 | 0,82 |
| Text Persona repetition | riche | 0,79 | 0,75 |
| Text Persona mini | riche | 0,43 | 0,63 |
| Text Persona Gemini | riche | 0,47 | 0,89 |

Par niveau (IC95 bootstrap) : Demographics 0,74 [0,47;1,00] ; JSON Persona 0,66 [0,57;1,10] ;
Text Persona 0,51 [0,58;0,92] ; profils complets (JSON+Text) 0,56 [0,62;0,91].

## Verdict

**Prediction rejetee, dans les deux volets, et dans le sens inverse.** Ratio
Demographics/complets observe 1,32 (IC95 [0,60 ; 1,41]), sous le seuil preregistre de 1,5.
Le facteur des profils complets est 0,56 (IC95 [0,62 ; 0,91]), **en dessous** de 1, pas au
dessus. A tous les niveaux le facteur est **inferieur a 1** : l'IA n'exagere pas l'ecart
gauche/droite, elle l'attenue, et l'attenuation **s'accentue** avec un profil plus riche
(0,74 -> 0,66 -> 0,51) au lieu de s'attenuer elle-meme. La compression intra-camp est aussi
< 1 partout (0,63 a 0,89), sans tendance nette selon la richesse.

**En clair** : plus on donne de details sur la personne a l'IA, moins elle fait de
difference entre gauche et droite -- l'oppose de la caricature attendue.
