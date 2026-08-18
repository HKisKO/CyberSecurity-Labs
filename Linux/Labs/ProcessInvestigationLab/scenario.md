# Scenario — Process & Service Investigation Lab

## Contexte

Une machine Ubuntu semble plus lente que d'habitude.

Un administrateur soupçonne qu'un processus ou un service consomme trop de ressources.

L'objectif est d'effectuer une investigation avant d'arrêter ou de modifier quoi que ce soit.

## Mission

Identifier les processus qui consomment le plus de CPU et de mémoire, puis déterminer :

- quel utilisateur possède le processus ;
- son PID ;
- son processus parent ;
- son état ;
- sa consommation CPU et mémoire ;
- s'il appartient à un service systemd ;
- si les logs du service montrent des erreurs.

L'objectif est également de comprendre comment arrêter proprement un processus ou un service.

## Méthode d'investigation

L'enquête suit la chaîne :

```text
Machine lente
     ↓
Processus
     ↓
CPU / RAM
     ↓
PID
     ↓
PPID / parent
     ↓
Service systemd ?
     ↓
CGroup
     ↓
Logs
     ↓
Décision
```

## Étape 1 — Identifier les processus

Les processus sont inspectés avec :

```bash
ps
ps aux
```

Ils peuvent ensuite être classés selon leur consommation :

```bash
ps aux --sort=-%cpu | head
ps aux --sort=-%mem | head
```

Cela permet d'identifier rapidement les processus les plus consommateurs.

## Étape 2 — Surveillance en temps réel

La commande :

```bash
top
```

permet d'observer en temps réel :

- les processus ;
- l'utilisation CPU ;
- la mémoire ;
- la swap ;
- le nombre de tâches ;
- le load average.

## Étape 3 — Rechercher un processus

Un processus peut être recherché avec :

```bash
pgrep
pidof
```

Exemple :

```bash
pgrep -a firefox
pidof firefox
```

## Étape 4 — Identifier les relations parent/enfant

Chaque processus possède un PID et peut posséder un PPID correspondant à son processus parent.

Exemple observé pendant le lab :

```text
PID 1
systemd
   ↓
systemd --user
   ↓
gnome-shell
   ↓
firefox
   ↓
processus Firefox enfant
```

L'arborescence peut également être visualisée avec :

```bash
pstree -p
```

## Étape 5 — Relier un processus à un service

Le processus MySQL observé pendant l'enquête était géré par :

```text
mysql.service
      ↓
Main PID
      ↓
mysqld
```

La commande :

```bash
systemctl status mysql.service
```

permet notamment d'observer :

- l'état du service ;
- son PID principal ;
- sa mémoire ;
- son temps CPU ;
- ses tâches ;
- son CGroup.

## Étape 6 — Vérifier les logs

Avant de conclure qu'un service rencontre un problème, ses logs sont vérifiés :

```bash
journalctl -u mysql.service
```

Pour afficher uniquement les dernières entrées :

```bash
journalctl -u mysql.service -n 20
```

Dans le cas étudié, aucun warning ou erreur n'a été observé dans les dernières entrées du journal MySQL.

## Étape 7 — Gestion des processus

Un processus de test a été créé avec :

```bash
sleep 1000 &
```

Cela permet d'étudier les jobs Bash et les signaux sans toucher à un service important.

Un processus peut recevoir différents signaux :

```bash
kill PID
kill -STOP PID
kill -CONT PID
```

`kill PID` envoie par défaut `SIGTERM` (15).

## États observés

Pendant le lab, le processus `sleep` est passé par :

```text
S
↓
SIGSTOP
↓
T
↓
SIGCONT
↓
S
↓
SIGTERM
↓
Terminé
```

Avec :

```text
S → Sleeping
T → Stopped
Z → Zombie
```

Un zombie est un processus déjà terminé dont le parent n'a pas encore récupéré le statut de sortie.

## Conclusion

L'objectif d'une investigation n'est pas de tuer immédiatement un processus consommant des ressources.

La démarche retenue est :

```text
Observer
   ↓
Identifier
   ↓
Comprendre la hiérarchie
   ↓
Identifier le service
   ↓
Consulter les logs
   ↓
Agir seulement si nécessaire
```

Lorsqu'un processus appartient à un service systemd, il est généralement préférable de gérer le service avec `systemctl` plutôt que de tuer directement son PID.