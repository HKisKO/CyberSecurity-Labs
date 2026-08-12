# LogAnalyzer - Scénario

## Contexte

Un administrateur système fournit un fichier de logs SSH contenant des connexions réussies et échouées.

L'objectif est de créer un programme Python permettant d'analyser ce fichier et d'identifier des comportements potentiellement suspects.

## Mission

Le programme doit permettre de :

1. Afficher les logs.
2. Compter les connexions réussies et échouées.
3. Extraire les adresses IP associées aux échecs.
4. Compter le nombre d'échecs par adresse IP.
5. Signaler les adresses IP ayant au moins 3 échecs.
6. Gérer l'absence du fichier de logs.
7. Utiliser un menu interactif.

## Contraintes

Le programme doit utiliser notamment :

- `with open()`
- boucles `for`
- conditions
- dictionnaires
- fonctions
- `split()`
- `try / except`
- `FileNotFoundError`

## Objectif

Construire un premier outil Python simple d'analyse de logs orienté cybersécurité.