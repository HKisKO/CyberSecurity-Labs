# BackupLab

## Scenario

Vous êtes administrateur système dans une entreprise.

Un développeur vient de terminer une nouvelle version d'une application.

Avant de poursuivre ses tests, il souhaite sauvegarder les journaux (logs) les plus importants afin de pouvoir les restaurer en cas de problème.

Votre mission est de préparer cette sauvegarde.

---

## Objectifs

Créer un laboratoire simulant une opération de sauvegarde de fichiers de logs sous Linux.

---

## Tâches

### 1. Préparer l'environnement

Créer l'arborescence suivante :

BackupLab/

├── logs/

├── backup/

└── archive/

---

### 2. Créer les journaux

Créer les fichiers suivants :

- app.log
- nginx.log
- ssh.log
- mysql.log

Ajouter un court message dans chacun des fichiers.

---

### 3. Sauvegarder les fichiers importants

Le développeur souhaite uniquement conserver :

- ssh.log
- nginx.log

Copier ces deux fichiers dans le dossier :

backup/

---

### 4. Créer une archive

Créer une archive compressée contenant le dossier :

backup/

Nom de l'archive :

logs.tar.gz

L'archive devra être enregistrée dans :

archive/

---

### 5. Vérifier l'archive

Afficher le contenu de l'archive sans l'extraire.

---

### 6. Tester la restauration

Créer un dossier :

restore/

Extraire l'archive dans ce dossier.

Vérifier que les fichiers restaurés sont présents.

---

### 7. Permissions

Appliquer les permissions suivantes :

archive/

755

backup/

700

Vérifier les permissions obtenues.

---

## Commandes attendues

Les commandes suivantes doivent être utilisées pendant le laboratoire :

- mkdir
- touch
- echo
- cat
- cp
- tree
- tar
- chmod
- ls

---

## Compétences développées

À la fin du laboratoire, vous devez être capable de :

- créer une arborescence de travail ;
- manipuler des fichiers de logs ;
- copier des fichiers spécifiques ;
- créer une archive avec tar ;
- extraire une archive ;
- comprendre les options principales de tar ;
- gérer les permissions d'accès ;
- distinguer un chemin absolu, un chemin relatif et le raccourci `~`.

---

## Livrables

Le laboratoire doit contenir :

BackupLab/

├── README.md

├── scenario.md

├── logs/

├── backup/

└── archive/
