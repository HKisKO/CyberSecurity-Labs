# Notes — Process & Service Investigation Lab

## 1. `ps` — Observer les processus

La commande :

```bash
ps
```

affiche par défaut les processus associés au terminal/session courante.

Exemple :

```text
PID      TTY       TIME       CMD
4615     pts/0     00:00:01   bash
12642    pts/0     00:00:00   ps
```

- `PID` : identifiant du processus ;
- `TTY` : terminal associé au processus ;
- `TIME` : temps CPU cumulé consommé ;
- `CMD` : commande associée au processus.

`TIME` ne représente pas la durée depuis laquelle le processus existe.

---

## 2. `ps aux` — Observer les processus du système

```bash
ps aux
```

permet d'obtenir une vue beaucoup plus complète des processus.

Colonnes importantes :

```text
USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND
```

### USER

Utilisateur propriétaire du processus.

### PID

Process ID : identifiant du processus.

### %CPU

Utilisation CPU du processus.

### %MEM

Pourcentage de mémoire physique utilisé.

### VSZ

Taille de l'espace mémoire virtuel du processus.

Une valeur VSZ élevée ne signifie pas que toute cette mémoire est réellement présente en RAM.

### RSS

Resident Set Size.

Quantité de mémoire du processus actuellement résidente en RAM.

### TTY

Terminal associé au processus.

`?` signifie généralement que le processus n'est pas associé à un terminal classique.

### STAT

État du processus.

### START

Moment auquel le processus a démarré.

### TIME

Temps CPU cumulé consommé.

### COMMAND

Commande complète associée au processus.

---

## 3. Classer les processus par consommation

Pour rechercher les processus consommant le plus de CPU :

```bash
ps aux --sort=-%cpu | head
```

Pour la mémoire :

```bash
ps aux --sort=-%mem | head
```

Le signe :

```text
-
```

indique ici un classement décroissant.

`head` conserve les premières lignes du résultat. Il ne supprime pas spécialement les processus à `0 %`.

---

## 4. `top` — Surveillance en temps réel

Contrairement à `ps`, qui fournit une vue ponctuelle, `top` actualise régulièrement les informations :

```bash
top
```

Informations importantes :

```text
load average
Tasks
%Cpu(s)
MiB Mem
MiB Swap
```

### Tasks

Nombre de tâches/processus et leurs différents états :

```text
running
sleeping
stopped
zombie
```

### %Cpu(s)

État global du CPU.

Quelques valeurs :

```text
us → temps CPU utilisateur
sy → temps CPU système/noyau
id → CPU idle/inutilisé
```

### MiB Mem

Informations sur la RAM physique :

```text
total
free
used
buff/cache
```

### MiB Swap

Espace de swap disponible/utilisé.

La swap est un espace généralement situé sur le stockage et pouvant être utilisé lorsque certaines pages mémoire sont déplacées hors de la RAM.

Elle est beaucoup plus lente que la RAM.

---

## 5. Load Average

`load average` ne représente pas un temps de chargement.

Exemple :

```text
load average: 1.20, 0.85, 0.60
```

Les trois valeurs représentent la charge moyenne sur environ :

```text
1 minute
5 minutes
15 minutes
```

La charge doit être interprétée en tenant compte du nombre de CPU logiques disponibles.

Le nombre de CPU logiques peut être obtenu avec :

```bash
nproc
```

Dans le lab :

```text
4 CPU logiques
```

Une valeur de load ne correspond pas directement à un pourcentage CPU.

---

## 6. Rechercher un processus

### pgrep

```bash
pgrep firefox
```

recherche des processus correspondant au nom/motif demandé et retourne leurs PID.

Avec :

```bash
pgrep -a firefox
```

la ligne de commande est également affichée.

### pidof

```bash
pidof firefox
```

recherche les PID associés au programme indiqué.

`pgrep` et `pidof` n'utilisent pas exactement les mêmes critères de recherche et peuvent donc produire des résultats différents.

---

## 7. PID et PPID

Un processus peut être inspecté avec :

```bash
ps -p PID -o user,pid,ppid,stat,%cpu,%mem,cmd
```

`PPID` signifie :

```text
Parent Process ID
```

Il indique le PID du processus parent.

Exemple observé :

```text
systemd
PID 1
   ↓
systemd --user
   ↓
gnome-shell
PID 2485
   ↓
firefox
PID 3639
   ↓
firefox enfant
PID 3836
```

Le PPID est la donnée fiable permettant d'identifier le parent.

Il ne faut pas supposer qu'un PID inférieur appartient forcément au parent : les PID peuvent être réutilisés.

---

## 8. `pstree`

Pour visualiser directement les relations parent/enfant :

```bash
pstree -p
```

ou à partir d'un processus précis :

```bash
pstree -p PID
```

Cela permet d'obtenir une représentation arborescente des processus.

---

## 9. systemd système et systemd utilisateur

Pendant l'investigation, la chaîne suivante a été observée :

```text
PID 1
/sbin/init
   ↓
systemd --user
   ↓
gnome-shell
   ↓
firefox
```

Le PID `1` correspond au processus init du système, assuré par systemd sur cette machine Ubuntu.

Une instance :

```text
systemd --user
```

existe également pour gérer la session et les unités utilisateur.

---

## 10. Relier processus et service systemd

Le processus MySQL a été identifié avec :

```text
mysqld
PID 1535
```

Puis :

```bash
systemctl status mysql.service
```

a montré :

```text
mysql.service
      ↓
Main PID: 1535
      ↓
mysqld
```

Cela permet de relier :

```text
service
   ↓
processus principal
   ↓
PID
```

---

## 11. Informations de `systemctl status`

Exemple :

```text
Loaded: loaded (...mysql.service; enabled; preset: enabled)
Active: active (running)
Main PID: 1535 (mysqld)
Tasks: 37
Memory: 389.1M
CPU: ...
CGroup: /system.slice/mysql.service
```

### Loaded

Indique que systemd a chargé la définition de l'unité et indique son fichier.

### enabled

Le service est configuré pour être activé automatiquement via systemd au démarrage lorsque les dépendances/targets correspondantes sont atteintes.

### preset

Politique de preset fournie pour l'unité.

Elle est différente de l'état actuellement configuré de l'unité.

### Active

État actuel du service.

### Main PID

PID du processus principal du service.

### Tasks

Nombre actuel de tâches associées au service/cgroup.

Ce n'est pas le nombre de tâches exécutées depuis son démarrage.

### Memory

Mémoire comptabilisée pour le service.

`peak` indique le pic observé.

### CPU

Temps CPU cumulé consommé par l'unité.

---

## 12. CGroup

systemd utilise les Linux Control Groups pour organiser et gérer les processus appartenant aux unités.

Exemple :

```text
/system.slice/mysql.service
        ↓
PID 1535 /usr/sbin/mysqld
```

Les cgroups permettent notamment de regrouper des processus et de suivre ou contrôler certaines ressources.

On peut donc avoir :

```text
service
   ↓
CGroup
   ↓
processus
   ↓
CPU / mémoire / tâches
```

---

## 13. `journalctl`

Pour consulter les logs d'une unité systemd :

```bash
journalctl -u mysql.service
```

`-u` permet de sélectionner une unité.

Pour afficher les 20 dernières entrées :

```bash
journalctl -u mysql.service -n 20
```

`-n 20` signifie :

```text
20 dernières entrées
```

Pour suivre les nouvelles entrées en direct :

```bash
journalctl -u mysql.service -f
```

`-f` signifie `follow`.

Pendant le lab, les dernières entrées MySQL ne contenaient pas de warning ou d'erreur visible.

---

## 14. Vérifier avant d'agir

Une consommation mémoire importante n'est pas suffisante pour conclure qu'un service est défaillant.

Pendant le lab :

```text
MySQL
↓
~390 MiB de mémoire
↓
service actif
↓
Server is operational
↓
journal sans erreur observée
```

Il faut donc investiguer avant de tuer ou redémarrer un processus.

---

## 15. `Restart=on-failure`

La commande :

```bash
systemctl show mysql.service -p KillSignal -p Restart
```

a retourné :

```text
Restart=on-failure
KillSignal=15
```

`Restart=on-failure` indique que systemd peut redémarrer le service lorsque sa terminaison correspond à certaines conditions d'échec.

Un arrêt volontaire avec :

```bash
systemctl stop mysql.service
```

est différent d'un crash du service.

---

## 16. Signaux Linux

`KillSignal=15` correspond à :

```text
SIGTERM
```

SIGTERM demande au processus de se terminer proprement.

La commande :

```bash
kill PID
```

envoie par défaut SIGTERM.

À distinguer de :

```text
SIGKILL = 9
```

SIGKILL provoque une terminaison forcée immédiate et ne permet pas au processus d'effectuer son nettoyage normal.

Il doit donc être réservé aux situations où un arrêt normal ne fonctionne pas.

---

## 17. Service vs processus

Pour un processus appartenant à un service systemd, préférer généralement :

```bash
sudo systemctl stop service
```

à :

```bash
sudo kill PID
```

systemd connaît l'unité, ses processus, son cgroup, son état et sa configuration.

`kill` agit directement en envoyant un signal au processus ciblé.

---

## 18. Jobs Bash

Un processus peut être lancé en arrière-plan avec :

```bash
sleep 1000 &
```

Bash peut répondre :

```text
[1] 17278
```

Les deux nombres sont différents :

```text
[1]   → Job ID géré par Bash
17278 → PID géré par le système
```

Les jobs du shell peuvent être affichés avec :

```bash
jobs
```

---

## 19. États des processus

États principaux rencontrés :

```text
R → Running / Runnable
S → Interruptible Sleep
D → Uninterruptible Sleep
T → Stopped
Z → Zombie
```

Des caractères supplémentaires peuvent apparaître après l'état principal dans `STAT`.

Exemple :

```text
Ssl
```

La première lettre `S` représente l'état principal.

---

## 20. SIGSTOP et SIGCONT

Un processus de test a été créé :

```bash
sleep 1000 &
```

Son état initial était :

```text
S
```

Puis :

```bash
kill -STOP PID
```

a produit :

```text
T
```

Le processus était suspendu.

Ensuite :

```bash
kill -CONT PID
```

l'a fait revenir à :

```text
S
```

Enfin :

```bash
kill PID
```

a envoyé SIGTERM et terminé le processus.

Cycle observé :

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

---

## 21. Processus zombie

Un processus zombie possède l'état :

```text
Z
```

Il s'agit d'un processus qui a déjà terminé son exécution mais dont le parent n'a pas encore récupéré le statut de terminaison.

Cycle normal :

```text
processus enfant
      ↓
termine
      ↓
parent récupère son statut
      ↓
entrée supprimée
```

Si le parent n'a pas encore récupéré le statut :

```text
enfant terminé
      ↓
Z — Zombie
```

Envoyer `SIGKILL` à un zombie ne résout pas directement le problème puisqu'il est déjà terminé.

Il faut notamment investiguer le comportement de son processus parent.

---

## 22. Méthodologie retenue

La principale leçon du lab est de ne pas commencer une investigation par :

```text
processus gourmand
      ↓
KILL
```

Mais plutôt :

```text
Machine lente
     ↓
ps / top
     ↓
identifier CPU / RAM
     ↓
PID
     ↓
PPID / pstree
     ↓
service ?
     ↓
systemctl
     ↓
journalctl
     ↓
comprendre le problème
     ↓
agir si nécessaire
```

Un administrateur doit d'abord observer et comprendre l'état du système avant de modifier ou arrêter un service.