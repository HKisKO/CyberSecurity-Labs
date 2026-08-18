# LogAnalyzer V2

LogAnalyzer V2 est un outil Python en ligne de commande permettant d'analyser un fichier de logs contenant des tentatives de connexion.

Cette version fait évoluer LogAnalyzer V1 en améliorant l'architecture du programme, la gestion des fichiers, le traitement des erreurs et l'export des résultats.

## Objectifs

Ce projet a pour objectif de pratiquer plusieurs concepts Python dans un contexte proche de l'administration système et de la cybersécurité :

- lecture et écriture de fichiers ;
- fonctions et paramètres ;
- utilisation de `return` ;
- listes et dictionnaires ;
- boucles et conditions ;
- gestion des exceptions ;
- tri de données avec `sorted()` et `lambda` ;
- validation des entrées utilisateur ;
- refactoring et réduction de la répétition de code.

## Fonctionnalités

LogAnalyzer V2 permet de :

- charger un fichier de logs choisi par l'utilisateur ;
- vérifier que le fichier existe avant de lancer l'analyse ;
- afficher le contenu des logs ;
- compter les connexions réussies et échouées ;
- afficher les adresses IP associées aux tentatives échouées ;
- compter le nombre d'échecs par adresse IP ;
- classer les IP de la plus suspecte à la moins suspecte ;
- définir un seuil configurable de tentatives suspectes ;
- choisir entre un affichage dans le terminal et un export dans un fichier texte ;
- changer de fichier à analyser sans redémarrer le programme.

## Modes de sortie

L'utilisateur peut choisir entre deux modes.

### Terminal

Les résultats de l'analyse sont directement affichés dans le terminal.

### Fichier texte

Les résultats peuvent être enregistrés dans un rapport.

Trois modes de création sont disponibles :

- `w` : créer ou remplacer le rapport ;
- `a` : ajouter à un rapport existant ;
- `x` : créer le rapport uniquement s'il n'existe pas.

Une fois le rapport préparé, les différentes analyses sont ajoutées au fichier sans supprimer les résultats précédents.

## Exemple de fichier analysé

```text
Accepted password for admin from 192.168.1.15
Failed password for root from 10.0.0.25
Failed password for admin from 10.0.0.25
Accepted password for user from 192.168.1.30
Failed password for root from 172.16.1.44
```

## Exemple d'analyse

```text
===== ECHECS PAR IP =====

10.0.0.25 : 2 échec(s)
172.16.1.44 : 1 échec(s)

===== IP SUSPECTES =====

10.0.0.25 : 2 tentatives échouées
```

Le seuil utilisé pour considérer une adresse IP comme suspecte est configurable par l'utilisateur.

## Gestion des erreurs

Le programme gère notamment :

- `FileNotFoundError` lorsqu'un fichier de logs n'existe pas ;
- `FileExistsError` lors de l'utilisation du mode `x` sur un rapport existant ;
- `ValueError` lorsqu'une valeur entière attendue n'est pas correctement saisie ;
- les fichiers vides ;
- les choix invalides dans les menus.

## Architecture générale

```text
Démarrage
    |
    v
Chargement du fichier
    |
    v
Configuration de la sortie
    |
    +---- Terminal
    |
    +---- Fichier
            |
            +---- w
            +---- a
            +---- x
    |
    v
Menu principal
    |
    +---- Afficher les logs
    +---- Compter les connexions
    +---- Afficher les IP en échec
    +---- Classer les IP / détecter les IP suspectes
    +---- Changer de fichier
    +---- Quitter
```

## Concepts travaillés

Cette V2 m'a notamment permis de travailler sur la séparation entre :

```text
Données
   ↓
Analyse
   ↓
Construction du résultat
   ↓
Destination
   ├── Terminal
   └── Fichier
```

Cette séparation permet d'éviter de refaire la même analyse simplement parce que la destination du résultat change.

## Évolutions prévues — V3

La prochaine version pourra notamment introduire :

- sélection des fichiers `.log` disponibles ;
- validation stricte des fichiers d'entrée en `.log` ;
- rapports limités au format `.txt` ;
- affichage des rapports existants avant création ou modification ;
- utilisation de `pathlib` pour la gestion des fichiers ;
- statistiques générales sur les logs ;
- Top N des adresses IP les plus suspectes ;
- confirmation avant écrasement d'un rapport ;
- amélioration de l'architecture interne ;
- introduction progressive des expressions régulières (`regex`).

## Technologies

- Python 3
- Linux / Ubuntu
- Git
- GitHub