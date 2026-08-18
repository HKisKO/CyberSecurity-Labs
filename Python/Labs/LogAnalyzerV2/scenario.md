# Scénario — LogAnalyzer V2

## Contexte

Un administrateur système dispose d'un fichier de logs contenant des tentatives de connexion à un système.

Exemple :

```text
Accepted password for admin from 192.168.1.15
Failed password for root from 10.0.0.25
Failed password for admin from 10.0.0.25
Accepted password for user from 192.168.1.30
Failed password for root from 172.16.1.44
```

Lire manuellement ce fichier peut fonctionner lorsqu'il contient quelques lignes, mais devient rapidement inefficace lorsque le nombre d'événements augmente.

L'objectif est donc de créer un outil Python permettant d'automatiser une première analyse de ces logs.

---

## Mission

Faire évoluer LogAnalyzer afin que l'utilisateur puisse choisir lui-même le fichier à analyser et obtenir plusieurs informations utiles sur les tentatives de connexion.

Le programme doit permettre de :

1. charger un fichier de logs choisi par l'utilisateur ;
2. vérifier que le fichier existe ;
3. afficher son contenu ;
4. compter les connexions réussies et échouées ;
5. identifier les adresses IP associées aux échecs ;
6. compter le nombre d'échecs par adresse IP ;
7. classer les IP selon leur nombre de tentatives échouées ;
8. définir un seuil permettant d'identifier les IP suspectes.

---

## Choix de la sortie

L'utilisateur doit pouvoir choisir ce qu'il souhaite faire des résultats :

```text
===== MODE DE SORTIE =====

1 - Afficher uniquement dans le terminal
2 - Exporter aussi dans un fichier texte
```

### Sortie terminal

Les résultats sont directement affichés dans le terminal.

### Sortie fichier

L'utilisateur choisit un fichier de rapport ainsi que son mode de création :

```text
===== MODE D'ÉCRITURE =====

1 - Créer/remplacer le rapport
2 - Ajouter au rapport existant
3 - Créer uniquement s'il n'existe pas
4 - Annuler
```

Les modes utilisés sont :

```text
w → créer/remplacer
a → ajouter
x → créer uniquement si le fichier n'existe pas
```

Une fois le rapport préparé, les résultats des différentes analyses sont ajoutés progressivement au fichier.

---

## Menu principal

Une fois le fichier chargé et la sortie configurée, l'utilisateur accède au menu :

```text
========== Log Analyzer ==========

1 - Afficher les logs
2 - Afficher le nombre de connexions échouées et réussies
3 - Afficher les adresses IP qui ont échoué à se connecter
4 - Afficher le nombre d'échecs par IP et les IP suspectes
5 - Changer de fichier
6 - Quitter
```

L'utilisateur peut effectuer plusieurs analyses successivement sans relancer le programme.

L'option `5` permet de charger un nouveau fichier et de configurer à nouveau le mode de sortie.

---

## Détection des IP suspectes

Les tentatives échouées sont regroupées par adresse IP.

Exemple :

```text
10.0.0.25 : 3 échec(s)
172.16.1.44 : 1 échec(s)
192.168.1.50 : 8 échec(s)
```

Les résultats sont ensuite classés du plus grand au plus petit nombre d'échecs :

```text
192.168.1.50 : 8 échec(s)
10.0.0.25 : 3 échec(s)
172.16.1.44 : 1 échec(s)
```

L'utilisateur définit ensuite un seuil.

Par exemple :

```text
Seuil de tentatives suspectes : 3
```

Le programme considère alors comme suspectes les IP ayant au moins trois tentatives échouées :

```text
===== IP SUSPECTES =====

192.168.1.50 : 8 tentatives échouées
10.0.0.25 : 3 tentatives échouées
```

---

## Contraintes de la V2

Cette version reste volontairement simple.

L'analyse repose notamment sur :

```python
"Failed password" in ligne
```

et :

```python
ligne.split()
```

Il n'y a pas encore d'expressions régulières.

Le programme suppose également que les logs analysés respectent le format attendu.

La gestion plus avancée des fichiers, la validation des extensions `.log` / `.txt` et l'utilisation de regex seront étudiées dans une prochaine version.

---

## Résultat attendu

À la fin de cette mission, LogAnalyzer V2 doit être capable de suivre la chaîne suivante :

```text
Fichier de logs
      ↓
Chargement et validation
      ↓
Analyse des événements
      ↓
Comptage / classement
      ↓
Détection des IP suspectes
      ↓
Résultat
   ├── Terminal
   └── Rapport texte
```

L'objectif principal de cette V2 est de transformer un premier script d'analyse en un petit outil CLI mieux structuré, réutilisable et capable de gérer plusieurs modes de sortie.