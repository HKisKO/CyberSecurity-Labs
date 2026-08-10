# ProcessLab - Scénario

## Contexte

Un développeur signale que certaines applications semblent continuer à fonctionner en arrière-plan et que certains services du système pourraient poser problème.

En tant qu'administrateur Linux junior, ma mission est d'analyser les processus actifs, comprendre leur consommation de ressources et apprendre à gérer les services avec systemd.

## Mission

### Partie 1 - Processus

- Afficher les processus actifs.
- Identifier leurs PID.
- Rechercher un processus par son nom.
- Lancer plusieurs processus en arrière-plan.
- Arrêter un processus précis.
- Arrêter plusieurs processus portant le même nom.
- Observer la consommation CPU et mémoire.

### Partie 2 - Jobs

Manipuler des processus depuis le shell :

- lancer une commande en arrière-plan ;
- suspendre un processus ;
- reprendre un processus en arrière-plan ;
- ramener un processus au premier plan ;
- distinguer Job ID et PID.

### Partie 3 - Services

Utiliser systemd pour :

- lister les services actifs ;
- consulter l'état d'un service ;
- comprendre `active` et `enabled` ;
- démarrer et arrêter un service ;
- redémarrer un service ;
- activer et désactiver son lancement automatique.

## Objectif

Comprendre la différence entre processus, jobs, daemons et services et acquérir les bases de la gestion des processus et services sous Linux.