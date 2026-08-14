# PermissionsLab — Scenario

## Contexte

Je travaille en tant qu'administrateur Linux junior.

Une entreprise possède plusieurs fichiers utilisés par différents utilisateurs et groupes. Certaines permissions ont été mal configurées et peuvent provoquer des problèmes de sécurité.

L'objectif est d'auditer les permissions existantes et de les corriger en appliquant le principe du moindre privilège.

## Structure

```text
company/
├── public/
│   └── announcement.txt
├── developers/
│   ├── app.conf
│   └── deploy.sh
└── confidential/
    └── credentials.txt
```

## Situation initiale

Plusieurs fichiers possèdent volontairement des permissions trop permissives :

```text
announcement.txt → 666 → rw-rw-rw-
app.conf         → 666 → rw-rw-rw-
deploy.sh        → 777 → rwxrwxrwx
credentials.txt  → 666 → rw-rw-rw-
```

Ces permissions permettent à des utilisateurs non autorisés de lire, modifier ou exécuter certains fichiers.

## Mission 1 — Audit des permissions

Analyser les permissions de chaque fichier en distinguant :

```text
owner
group
others
```

Identifier les droits :

```text
r → read
w → write
x → execute
```

et déterminer les risques associés aux permissions trop permissives.

## Mission 2 — Correction des permissions

Appliquer le principe du moindre privilège.

Les permissions retenues sont :

```text
announcement.txt → 644 → rw-r--r--
app.conf         → 640 → rw-r-----
deploy.sh        → 750 → rwxr-x---
credentials.txt  → 600 → rw-------
```

Objectif :

- les annonces sont lisibles par tous mais modifiables uniquement par leur propriétaire ;
- la configuration de l'application est modifiable par son propriétaire et lisible par le groupe autorisé ;
- le script de déploiement est modifiable uniquement par son propriétaire ;
- les credentials restent accessibles uniquement à leur propriétaire.

## Mission 3 — Utilisateurs et groupes

Créer un groupe :

```text
developers
```

Puis ajouter l'utilisateur au groupe afin de comprendre la gestion des groupes secondaires.

Commandes étudiées :

```bash
id
groups
getent group
groupadd
usermod -aG
newgrp
```

Le groupe `developers` est ensuite attribué aux fichiers :

```text
app.conf
deploy.sh
```

afin que les permissions de groupe puissent être utilisées par les développeurs autorisés.

Les commandes `chgrp` et `chown` permettent respectivement de modifier le groupe propriétaire et le propriétaire d'un fichier.

## Mission 4 — umask

Étudier les permissions attribuées automatiquement lors de la création de fichiers et de répertoires.

Permissions de base :

```text
fichier   → 666
répertoire → 777
```

Avec le `umask` observé :

```text
0002
```

les nouvelles permissions obtenues sont :

```text
fichier   → 664 → rw-rw-r--
répertoire → 775 → rwxrwxr-x
```

D'autres valeurs de `umask` ont également été étudiées afin de comprendre comment limiter les permissions accordées par défaut.

## Mission finale — Audit de sécurité

Analyser plusieurs fichiers présentant des permissions potentiellement dangereuses.

Pour chaque fichier :

1. identifier les permissions actuelles ;
2. identifier le propriétaire et le groupe ;
3. déterminer les droits réellement nécessaires ;
4. supprimer les permissions inutiles ;
5. appliquer le principe du moindre privilège.

Exemples de corrections :

```text
deploy.sh       : 777 → 750
app.conf        : 666 → 640
credentials.txt : 644 → 600
announcement.txt: 600 → 644
backup.sh       : 755 → 700
```

## Objectif du laboratoire

Comprendre comment Linux contrôle l'accès aux fichiers grâce aux utilisateurs, groupes et permissions, et savoir auditer une configuration afin de limiter les accès inutiles.