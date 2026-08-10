 Linux Cheat Sheet

## Navigation

pwd
ls
ls -l
tree
cd
cd ..
cd ~

---

## Gestion des fichiers

mkdir
touch
cp
cp -a
mv
rm
cat
echo

>  : écrase le contenu
>> : ajoute à la fin

---

## Permissions

r = 4
w = 2
x = 1

7 = rwx
6 = rw-
5 = r-x
4 = r--
0 = ---

chmod 755

Le propriétaire :
lecture
écriture
exécution

Le groupe :
lecture
exécution

Les autres :
lecture
exécution

---

chmod 644

rw-r--r--

---

chmod 600

rw-------

Très utilisé pour les fichiers privés.


---

Premier caractère

d = dossier
- = fichier

---

Permissions d'un dossier

r : voir le contenu

w : créer/supprimer/renommer

x : entrer dans le dossier

## Compression avec tar
Brace Expansion ({})
cp avec plusieurs fichiers {}
tar
tar -czf create gzip files 
tar -tf liste files 
tar -xf extract files 
tar -xf -C estract file in certain directory 
différence entre > et >> (si ce n'était pas déjà fait)



# Processus et services

## Processus

Afficher les processus du terminal :

```bash
ps
```

Afficher les processus avec plus d'informations :

```bash
ps aux
```

Rechercher un processus :

```bash
pgrep nom_processus
```

Afficher le PID avec la commande complète :

```bash
pgrep -a nom_processus
```

Filtrer les processus :

```bash
ps aux | grep nom_processus
```

## Jobs

Lancer une commande en arrière-plan :

```bash
commande &
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

> `%1`, `%2`, etc. sont des Job IDs Bash, pas des PID.

## Arrêter des processus

Arrêt normal avec SIGTERM :

```bash
kill PID
```

ou :

```bash
kill -15 PID
```

Forcer l'arrêt avec SIGKILL :

```bash
kill -9 PID
```

SIGKILL ne doit pas être le premier choix.

Arrêter les processus portant un même nom :

```bash
killall nom_processus
```

## Surveillance des ressources

```bash
top
```

Dans `top` :

```text
P → trier par CPU
M → trier par mémoire
q → quitter
```

Colonnes importantes :

```text
PID      → identifiant du processus
USER     → propriétaire
%CPU     → utilisation CPU
%MEM     → utilisation RAM
COMMAND  → programme exécuté
```

## systemd

Lister les services actuellement actifs :

```bash
systemctl --type=service --state=running
```

Afficher l'état d'un service :

```bash
systemctl status nom.service
```

Vérifier son état actuel :

```bash
systemctl is-active nom.service
```

Vérifier son activation automatique :

```bash
systemctl is-enabled nom.service
```

Gestion immédiate :

```bash
systemctl start nom.service
systemctl stop nom.service
systemctl restart nom.service
```

Gestion du lancement automatique :

```bash
systemctl enable nom.service
systemctl disable nom.service
```

À retenir :

```text
start   → démarre maintenant
stop    → arrête maintenant
restart → arrête puis redémarre

enable  → active le lancement automatique
disable → désactive le lancement automatique
```

Donc :

```text
stop ≠ disable
start ≠ enable
```

Un service peut être :

```text
active   + enabled
inactive + enabled
active   + disabled
inactive + disabled
```

## Option --now

```bash
systemctl enable --now nom.service
```

→ `enable` + démarrage immédiat.

```bash
systemctl disable --now nom.service
```

→ `disable` + arrêt immédiat.

## Services utilisateur

Pour gérer un service systemd utilisateur :

```bash
systemctl --user ...
```

Exemple :

```bash
systemctl --user status processlab-test.service
```

## Processus, daemon et service

```text
Processus → instance d'un programme en cours d'exécution.

Daemon    → programme généralement destiné à fonctionner
            en arrière-plan.

Service   → unité gérée par un gestionnaire de services
            comme systemd.
```

## PID vs Job ID

```text
PID     → identifiant du processus au niveau Linux
Job ID  → identifiant attribué par le shell Bash
```

Exemples :

```bash
kill 1234    # PID
fg %1        # Job ID
```
