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

