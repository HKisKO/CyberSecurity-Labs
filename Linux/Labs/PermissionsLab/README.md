# Linux PermissionsLab

Laboratoire Linux consacré à la gestion des permissions, des propriétaires, des groupes et des permissions par défaut.

L'objectif est de simuler des tâches simples d'un administrateur Linux junior tout en appliquant le principe du moindre privilège.

## Objectifs

- Auditer les permissions de fichiers Linux
- Comprendre `owner`, `group` et `others`
- Modifier les permissions avec `chmod`
- Gérer les propriétaires et les groupes
- Comprendre les groupes principaux et secondaires
- Ajouter un utilisateur à un groupe
- Comprendre le fonctionnement de `umask`
- Identifier des permissions dangereuses
- Appliquer le principe du moindre privilège

## Structure du laboratoire

```text
PermissionsLab/
├── company/
│   ├── public/
│   │   └── announcement.txt
│   ├── developers/
│   │   ├── app.conf
│   │   └── deploy.sh
│   └── confidential/
│       └── credentials.txt
├── README.md
├── scenario.md
└── notes.md
```

## Permissions Linux

Les permissions sont divisées entre :

```text
owner | group | others
```

Les permissions de base sont :

```text
r = lecture
w = écriture
x = exécution
```

Valeurs numériques :

```text
r = 4
w = 2
x = 1
```

Exemples utilisés pendant le laboratoire :

| Permission | Symbolique | Utilisation |
|---|---|---|
| `644` | `rw-r--r--` | Fichier lisible par tous |
| `640` | `rw-r-----` | Propriétaire + groupe autorisé |
| `750` | `rwxr-x---` | Script exécutable par le propriétaire et le groupe |
| `600` | `rw-------` | Fichier confidentiel |
| `700` | `rwx------` | Script privé |

## Utilisateurs et groupes

Commandes pratiquées :

```bash
id
groups
getent group
sudo groupadd developers
sudo usermod -aG developers <utilisateur>
newgrp developers
```

Un groupe `developers` a été créé afin de simuler la gestion des accès d'une équipe de développement.

Le groupe propriétaire de certains fichiers a ensuite été modifié avec :

```bash
chgrp developers <fichier>
```

Différences importantes :

```text
chmod   → modifier les permissions
chgrp   → modifier le groupe propriétaire
chown   → modifier le propriétaire d'un fichier
usermod → modifier l'appartenance d'un utilisateur aux groupes
```

## Exemple

Le fichier :

```text
app.conf
```

a été configuré comme ceci :

```text
-rw-r----- koceila developers app.conf
```

Ce qui signifie :

```text
propriétaire → lecture + écriture
developers   → lecture
autres       → aucun accès
```

## umask

Le laboratoire a également permis d'étudier les permissions attribuées par défaut lors de la création de fichiers et de répertoires.

Permissions maximales de base :

```text
Fichier    → 666
Répertoire → 777
```

Avec :

```bash
umask 0002
```

les permissions observées sont :

```text
Fichier    → 664 → rw-rw-r--
Répertoire → 775 → rwxrwxr-x
```

Exemples plus restrictifs :

```text
umask 0027

Fichier    → 640
Répertoire → 750
```

et :

```text
umask 0077

Fichier    → 600
Répertoire → 700
```

`umask` indique les permissions qui ne doivent pas être accordées par défaut.

## Audit de sécurité

L'exercice final consistait à analyser plusieurs fichiers possédant des permissions dangereuses et à déterminer les corrections appropriées.

Exemples :

```text
deploy.sh        : 777 → 750
app.conf         : 666 → 640
credentials.txt  : 644 → 600
announcement.txt : 600 → 644
backup.sh        : 755 → 700
```

Les permissions sont choisies selon les besoins réels de chaque utilisateur et groupe, plutôt qu'en accordant des droits inutiles.

## Commandes pratiquées

```bash
ls -l
ls -ld
chmod
chown
chgrp
id
groups
getent
groupadd
usermod
newgrp
umask
```

## Principe de sécurité

Le principe principal appliqué pendant ce laboratoire est :

> Accorder aux utilisateurs et aux groupes uniquement les permissions nécessaires à l'accomplissement de leurs tâches.

Il s'agit du **principe du moindre privilège**.