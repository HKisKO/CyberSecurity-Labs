# SubnettingLab - Scénario

## Contexte

Une entreprise doit organiser son réseau IPv4 en plusieurs sous-réseaux afin de séparer différents départements.

En tant qu'administrateur réseau junior, ma mission est de déterminer les sous-réseaux adaptés aux besoins de chaque département et d'éviter tout chevauchement entre les plages d'adresses.

## Mission 1 - Analyse d'un sous-réseau

À partir d'une adresse IPv4 accompagnée d'un préfixe CIDR, déterminer :

- le nombre de bits réseau ;
- le nombre de bits hôte ;
- le masque de sous-réseau ;
- la taille du bloc ;
- l'adresse réseau ;
- le premier hôte ;
- le dernier hôte ;
- l'adresse de broadcast ;
- le nombre d'hôtes utilisables.

## Mission 2 - Choisir un sous-réseau

À partir d'un nombre de machines à connecter, déterminer le plus petit sous-réseau capable de les accueillir.

La formule utilisée pour les exercices est :

2^n - 2

où `n` représente le nombre de bits hôte.

## Mission 3 - VLSM

À partir d'un réseau principal, créer plusieurs sous-réseaux de tailles différentes selon les besoins des départements.

Les sous-réseaux doivent :

- être suffisamment grands ;
- utiliser efficacement l'espace d'adressage ;
- ne pas se chevaucher.

## Objectif

Réviser le subnetting IPv4 et appliquer le VLSM dans un scénario proche d'un réseau d'entreprise.