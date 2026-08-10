# ProcessLab - Notes

## Processus

Afficher les processus du terminal courant :

```bash
ps
```

Afficher une liste détaillée des processus :

```bash
ps aux
```

Rechercher un processus :

```bash
pgrep sleep
```

Afficher le PID et la commande :

```bash
pgrep -a sleep
```

Filtrer une sortie :

```bash
ps aux | grep sleep
```

## PID

PID = Process ID.

Il identifie un processus au niveau du système.

---

## Jobs

Lancer une commande en arrière-plan :

```bash
sleep 1000 &
```

Afficher les jobs :

```bash
jobs
```

Suspendre le processus au premier plan :

```text
Ctrl+Z
```

Reprendre en arrière-plan :

```bash
bg
```

Ramener au premier plan :

```bash
fg
```

Choisir un job précis :

```bash
fg %1
bg %2
```

`%1` représente un Job ID et non un PID.

---

## Arrêter un processus

Arrêt normal :

```bash
kill PID
```

Par défaut, `kill` envoie SIGTERM.

Équivalent :

```bash
kill -15 PID
```

SIGTERM demande au processus de se terminer proprement.

Forcer l'arrêt :

```bash
kill -9 PID
```

SIGKILL force l'arrêt du processus et ne devrait pas être le premier choix.

Arrêter les processus portant un nom :

```bash
killall sleep
```

---

## top

Surveiller les processus en temps réel :

```bash
top
```

Trier par CPU :

```text
P
```

Trier par mémoire :

```text
M
```

Quitter :

```text
q
```

Colonnes importantes :

- `PID` : identifiant du processus
- `USER` : propriétaire
- `%CPU` : utilisation CPU
- `%MEM` : utilisation RAM
- `COMMAND` : programme exécuté

---

## systemd

Afficher les services actifs :

```bash
systemctl --type=service --state=running
```

État détaillé :

```bash
systemctl status nom.service
```

Vérifier si le service fonctionne actuellement :

```bash
systemctl is-active nom.service
```

Vérifier son activation automatique :

```bash
systemctl is-enabled nom.service
```

### start / stop / restart

```bash
systemctl start nom.service
systemctl stop nom.service
systemctl restart nom.service
```

- `start` : démarre maintenant
- `stop` : arrête maintenant
- `restart` : arrête puis redémarre

### enable / disable

```bash
systemctl enable nom.service
systemctl disable nom.service
```

- `enable` : configure l'activation automatique
- `disable` : retire cette activation automatique

Important :

```text
stop ≠ disable
start ≠ enable
```

Un service peut donc être :

```text
active   + enabled
inactive + enabled
active   + disabled
inactive + disabled
```

### --now

```bash
systemctl enable --now nom.service
```

Active le démarrage automatique et démarre également le service maintenant.

```bash
systemctl disable --now nom.service
```

Désactive le démarrage automatique et arrête également le service maintenant.

---

## Service utilisateur

Les services utilisateur sont manipulés avec :

```bash
systemctl --user
```

Exemple :

```bash
systemctl --user status processlab-test.service
```

Le service de test du laboratoire a permis d'observer les changements d'état sans manipuler un service système important.

---

## À retenir

```text
PID      → identifiant système d'un processus
Job ID   → identifiant d'un job dans le shell

Ctrl+Z   → suspend
Ctrl+C   → interrompt
bg       → reprend en arrière-plan
fg       → ramène au premier plan

kill     → cible généralement un PID
killall  → cible par nom

start    → démarre maintenant
stop     → arrête maintenant
enable   → activation automatique
disable  → désactivation automatique
```