# PermissionsLab — Notes

## 1. Permissions Linux

Une permission Linux est divisée en trois catégories :

```text
owner | group | others
```

Les droits sont :

```text
r = read    = lecture   = 4
w = write   = écriture  = 2
x = execute = exécution = 1
```

Exemple :

```text
-rwxr-x---
```

correspond à :

```text
owner  → rwx → 7
group  → r-x → 5
others → --- → 0

chmod 750 fichier
```

---

## 2. Permissions courantes

```text
600 → rw------- → propriétaire : lecture + écriture
640 → rw-r----- → propriétaire : rw, groupe : r
644 → rw-r--r-- → propriétaire : rw, autres : lecture
700 → rwx------ → propriétaire : tous les droits
750 → rwxr-x--- → propriétaire : rwx, groupe : rx
755 → rwxr-xr-x → propriétaire : rwx, autres : rx
```

Ne pas ajouter une permission simplement parce qu'elle ne semble pas dangereuse.

Principe :

> Si un utilisateur n'a pas besoin d'un droit, on ne lui donne pas.

---

## 3. chmod

Modifier les permissions :

```bash
chmod 640 fichier
```

Exemple :

```text
avant : rw-rw-rw- → 666
après : rw-r----- → 640
```

---

## 4. Identifier utilisateur et groupes

Afficher l'UID, le GID principal et les groupes :

```bash
id
```

Afficher les groupes :

```bash
groups
```

Exemple :

```text
uid=1000(koceila)
gid=1000(koceila)
```

`uid` :

```text
User ID
```

`gid` :

```text
Group ID principal
```

---

## 5. Rechercher un groupe

```bash
getent group developers
```

Exemple :

```text
developers:x:1004:koceila
```

Signification :

```text
developers → nom du groupe
x          → champ mot de passe / placeholder
1004       → GID
koceila    → membre du groupe
```

Le `x` ici n'est PAS une permission d'exécution.

---

## 6. Créer un groupe

```bash
sudo groupadd developers
```

Ajouter un utilisateur au groupe :

```bash
sudo usermod -aG developers koceila
```

Options :

```text
-a → append : ajouter sans supprimer les groupes existants
-G → groupes secondaires
```

Attention à ne pas oublier `-a` lorsqu'on veut conserver les groupes secondaires existants.

---

## 7. newgrp

Après l'ajout d'un utilisateur à un groupe, la session actuelle peut ne pas immédiatement utiliser cette nouvelle appartenance.

```bash
newgrp developers
```

ouvre un nouveau shell avec `developers` comme groupe principal actif.

Vérification :

```bash
id
groups
```

---

## 8. chgrp

Modifier le groupe propriétaire d'un fichier :

```bash
chgrp developers app.conf
```

Exemple :

```text
avant :
koceila koceila app.conf

après :
koceila developers app.conf
```

---

## 9. chown

Modifier le propriétaire :

```bash
sudo chown alice app.conf
```

Modifier propriétaire + groupe :

```bash
sudo chown alice:developers app.conf
```

Important :

```text
chown alice:developers fichier
```

ne signifie PAS qu'Alice devient membre du groupe `developers`.

Pour ajouter Alice au groupe :

```bash
sudo usermod -aG developers alice
```

---

## 10. Différence entre les commandes

```text
chmod   → permissions du fichier
chgrp   → groupe propriétaire du fichier
chown   → propriétaire et éventuellement groupe du fichier
usermod → configuration de l'utilisateur et de ses groupes
```

---

# umask

## 11. Permissions de base

Lors de la création :

```text
fichier ordinaire → base 666 → rw-rw-rw-
répertoire        → base 777 → rwxrwxrwx
```

Un fichier ordinaire ne reçoit pas automatiquement `x`.

Un répertoire utilise `x` pour permettre sa traversée / l'accès à son contenu.

---

## 12. Fonctionnement de umask

Afficher le masque actuel :

```bash
umask
```

`umask` indique quelles permissions doivent être retirées lors de la création.

Exemple :

```text
umask 0002
```

Résultat :

```text
fichier :
666 → 664 → rw-rw-r--

répertoire :
777 → 775 → rwxrwxr-x
```

---

## 13. Exemples de umask

```text
umask 0002
fichier    → 664
répertoire → 775

umask 0022
fichier    → 644
répertoire → 755

umask 0027
fichier    → 640
répertoire → 750

umask 0077
fichier    → 600
répertoire → 700
```

Signification des chiffres du masque :

```text
0 → ne retire aucun droit
1 → retire x
2 → retire w
4 → retire r

3 → retire w + x
5 → retire r + x
6 → retire r + w
7 → retire tous les droits
```

`umask` est un masque de permissions, pas simplement une soustraction arithmétique.

---

# Sécurité

## 14. Principe du moindre privilège

Toujours se demander :

```text
Qui est le propriétaire ?
        ↓
Quel est le groupe propriétaire ?
        ↓
Quels droits sont réellement nécessaires ?
        ↓
owner ?
group ?
others ?
        ↓
Retirer les permissions inutiles
```

Exemple :

```text
credentials.txt
```

Si seul le propriétaire doit lire et modifier :

```text
rw-------
600
```

et non :

```text
700
```

car le droit `x` n'est pas nécessaire.

---

## 15. Méthode d'audit

Pour analyser un fichier :

```bash
ls -l fichier
```

Puis vérifier :

```text
1. propriétaire
2. groupe
3. permissions owner
4. permissions group
5. permissions others
6. besoin réel
7. permissions inutiles ou dangereuses
```

Exemple :

```text
-rwxrwxrwx root developers deploy.sh
```

Analyse :

```text
root       → rwx
developers → rwx
others     → rwx
```

Si les développeurs doivent seulement lire et exécuter et que les autres ne doivent avoir aucun accès :

```text
rwxr-x---
750
```

Correction :

```bash
chmod 750 deploy.sh
```