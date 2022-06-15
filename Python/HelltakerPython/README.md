# Solveur Helltaker Python 


## Ajout de cartes dans la base de données 

Les dossiers suivants sont conçus pour enregistrer les différentes maps/cartes à tester: 
    - homemade_tests
        Il vise à contenir des maps non issues du jeu 
    - tests
        Il vise à contenir des maps issues du jeu

Chaque carte de niveau est enregistrée sous la forme d'un fichier .txt

## Représentation de la carte 

Une carte est composé de 3 parties : 
    - Une première ligne avec le titre
    - Une deuxième ligne avec le nombre supposé nécessaire pour accomplir le niveau
        A noter que cette valeur ne vise qu'à être exploitée que par l'utilisateur et non pas le programme 
    - Une représentation de la carte elle-même avec des symboles

### Les symboles
Une carte doit seulement et uniquement être constitué des symboles suivants
- `H`: hero
- `D`: demoness
- `#`: wall
- ` ` : empty
- `B`: block
- `K`: key
- `L`: lock
- `M`: mob (skeleton)
- `S`: spikes
- `T`: trap (open, safe)
- `U`: trap (closed, unsafe)
- `O`: block on spike
- `P`: block on trap (open)
- `Q`: block on trap (closed)

### Exemple de carte
```
Level 1
23
     ###
  ### H#
 #  M  #
 # M M#
#  ####
# B  B #
# B B  D#
#########
```

## Execution du solver python 

Le fichier à executer pour faire appel au solver python est main.py

Après exécution, le fichier demandera le chemin vers le fichier à tester, 
puis s'il le trouve lance la résolution

### Exemple de chemin à renseigner 

tests/level1.txt
homemade_tests/impossible.txt

### Le retour 

Après renseignement du chemin, 
le programme retourne : 
    - la carte interprétée sous forme de matrice
    - Une série de déplacement permettant de résoudre le niveau 
    - Ainsi que le nom d'actions nécessaire
