# ProcessLab

Laboratoire Linux consacré à la gestion des processus, des jobs et des services systemd.

## Compétences travaillées

### Processus

Commandes utilisées :

```bash
ps
ps aux
pgrep
kill
killall
top
```

Compétences :

- identifier un processus avec son PID ;
- rechercher un processus ;
- consulter son utilisation CPU et mémoire ;
- envoyer un signal à un processus ;
- distinguer `SIGTERM` et `SIGKILL`.

### Gestion des jobs

Commandes et raccourcis utilisés :

```bash
jobs
bg
fg
Ctrl+Z
Ctrl+C
```

Concepts :

- foreground ;
- background ;
- Job ID ;
- PID ;
- suspension et reprise d'un processus.

### Services systemd

Commandes utilisées :

```bash
systemctl status
systemctl is-active
systemctl is-enabled
systemctl start
systemctl stop
systemctl restart
systemctl enable
systemctl disable
```

Utilisation d'un service systemd utilisateur de test afin de manipuler les différents états sans modifier un service système important.

## Concepts importants

- Un processus est une instance d'un programme en cours d'exécution.
- Un daemon est un programme généralement destiné à fonctionner en arrière-plan.
- Un service est une unité pouvant être gérée par un gestionnaire de services comme systemd.
- `active` et `enabled` représentent deux états différents.
- Arrêter un service ne signifie pas désactiver son démarrage automatique.