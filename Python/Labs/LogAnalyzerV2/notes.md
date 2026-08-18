# Notes — LogAnalyzer V2

## 1. Lecture d'un fichier

Pour ouvrir un fichier en lecture :

```python
with open(nom_fichier, "r") as fichier:
    lignes = fichier.readlines()
```

`readlines()` permet de récupérer les lignes du fichier dans une liste.

Exemple :

```python
[
    "Accepted password for admin from 192.168.1.15\n",
    "Failed password for root from 10.0.0.25\n"
]
```

Cela permet de charger le fichier une seule fois puis de transmettre `lignes` aux différentes fonctions.

---

## 2. Gestion d'un fichier inexistant

L'ouverture d'un fichier inexistant provoque :

```python
FileNotFoundError
```

On peut donc utiliser :

```python
try:
    with open(nom_fichier, "r") as fichier:
        lignes = fichier.readlines()

except FileNotFoundError:
    print("Fichier introuvable")
```

Avec une boucle `while True`, le programme peut redemander un fichier tant qu'un fichier valide n'a pas été fourni.

---

## 3. Paramètres de fonctions

Au lieu de coder le nom du fichier directement dans chaque fonction :

```python
open("auth.log", "r")
```

on peut transmettre les données :

```python
def afficher_logs(lignes):
```

Cela rend les fonctions indépendantes du nom du fichier utilisé.

---

## 4. `return`, `break` et `continue`

### `return`

Quitte complètement une fonction et peut retourner une valeur :

```python
return lignes
```

ou plusieurs valeurs :

```python
return nom_fichier, lignes
```

### `break`

Quitte uniquement la boucle actuelle :

```python
while True:
    ...
    break
```

### `continue`

Arrête l'itération actuelle et recommence immédiatement la boucle :

```python
if seuil <= 0:
    continue
```

Si une boucle arrive naturellement à la fin de son bloc, elle recommence également si sa condition est toujours vraie.

---

## 5. Vérifier une liste vide

Une liste vide est considérée comme `False`.

On peut donc utiliser :

```python
if not lignes:
    print("Fichier vide")
    return
```

au lieu de :

```python
if len(lignes) == 0:
```

---

## 6. Stocker plusieurs résultats dans une liste

Pour récupérer toutes les IP associées aux connexions échouées :

```python
ip_echecs = []

for ligne in lignes:
    if "Failed password" in ligne:
        mots = ligne.split()
        ip_echecs.append(mots[-1])
```

`append()` permet d'ajouter progressivement des éléments à une liste.

---

## 7. Compter les échecs avec un dictionnaire

Un dictionnaire permet d'associer une IP à son nombre d'échecs :

```python
echecs_par_ip = {}
```

Exemple :

```python
{
    "10.0.0.25": 3,
    "172.16.1.44": 1,
    "192.168.1.50": 8
}
```

La clé représente l'adresse IP et la valeur représente le nombre d'échecs.

---

## 8. Trier un dictionnaire selon ses valeurs

`echecs_par_ip.items()` produit des couples :

```python
("10.0.0.25", 3)
```

Dans ce tuple :

```text
element[0] → adresse IP
element[1] → nombre d'échecs
```

Pour classer les IP selon le nombre d'échecs :

```python
classement = sorted(
    echecs_par_ip.items(),
    key=lambda element: element[1],
    reverse=True
)
```

`reverse=True` permet d'obtenir un classement décroissant.

Important : `sorted()` retourne ici une **liste de tuples**, et non un dictionnaire.

---

## 9. Seuil configurable

Au lieu d'utiliser une valeur codée en dur :

```python
if nombre_echec >= 3:
```

le seuil peut être demandé à l'utilisateur :

```python
seuil = int(input("Seuil de tentatives suspectes : "))
```

Il faut gérer deux types de problèmes.

Une valeur comme :

```text
abc
```

provoque :

```python
ValueError
```

Une valeur comme `-3` est bien un entier mais n'est pas valide pour notre utilisation.

On peut donc combiner :

```python
try:
```

avec :

```python
if seuil <= 0:
```

---

# 10. Modes d'ouverture des fichiers

## `r` — Read

Lecture :

```python
open("auth.log", "r")
```

## `w` — Write

Écriture avec remplacement du contenu existant :

```python
open("rapport.txt", "w")
```

Si le fichier n'existe pas, il est créé.

## `a` — Append

Ajout à la fin du fichier :

```python
open("rapport.txt", "a")
```

Le contenu existant est conservé.

## `x` — Exclusive creation

Création uniquement si le fichier n'existe pas :

```python
open("rapport.txt", "x")
```

S'il existe déjà :

```python
FileExistsError
```

`x` ne signifie donc pas "execute".

---

## 11. Préparer un rapport puis l'alimenter

Dans LogAnalyzer V2, `w`, `a` et `x` servent d'abord à déterminer comment préparer le rapport.

Une fois celui-ci créé, les différentes analyses utilisent :

```python
open(nom_rapport, "a")
```

pour ajouter leurs résultats sans supprimer ce qui a déjà été écrit.

Exemple :

```text
création du rapport
       ↓
w / a / x
       ↓
rapport prêt
       ↓
option 1 ──a──> rapport
option 2 ──a──> rapport
option 3 ──a──> rapport
option 4 ──a──> rapport
```

---

## 12. `write()` et `print()`

`print()` affiche dans le terminal :

```python
print(f"Échecs : {compteur_echec}")
```

`write()` écrit dans un fichier :

```python
fichier.write(f"Échecs : {compteur_echec}\n")
```

Contrairement à `print()`, `write()` ne rajoute pas automatiquement un retour à la ligne.

Il faut donc utiliser :

```python
\n
```

---

## 13. Le fichier doit rester ouvert pendant `write()`

Correct :

```python
with open(nom_rapport, "a") as fichier:
    fichier.write("Analyse\n")
```

Incorrect :

```python
with open(nom_rapport, "a") as fichier:
    pass

fichier.write("Analyse\n")
```

Après la sortie du `with`, le fichier est fermé.

---

## 14. Ne pas ouvrir le fichier à chaque tour de boucle

À éviter :

```python
for ligne in lignes:
    with open(nom_rapport, "a") as fichier:
        fichier.write(ligne)
```

Préférer :

```python
with open(nom_rapport, "a") as fichier:
    for ligne in lignes:
        fichier.write(ligne)
```

Le fichier est ainsi ouvert une seule fois.

---

## 15. Séparer analyse et destination

Une amélioration importante de V2 a été de ne pas refaire l'analyse selon le mode de sortie.

À éviter :

```text
si terminal
    → analyser
    → afficher

si fichier
    → analyser une deuxième fois
    → écrire
```

Préférer :

```text
données
   ↓
analyse une seule fois
   ↓
résultat
   ↓
destination
   ├── terminal
   └── fichier
```

---

## 16. Construire un résultat avant de l'afficher

Pour les analyses plus longues, on peut construire une chaîne :

```python
resultat = "\n===== ECHECS PAR IP =====\n"

for adresse, nombre_echec in classement:
    resultat += f"{adresse} : {nombre_echec} échec(s)\n"
```

Puis utiliser exactement le même résultat :

```python
if mode_sortie == "terminal":
    print(resultat)

elif mode_sortie == "fichier":
    with open(nom_rapport, "a") as fichier:
        fichier.write(resultat)
```

Cela évite de dupliquer les boucles d'affichage.

---

## 17. Refactoring

Quand le même bloc de code commence à apparaître plusieurs fois, il peut être intéressant de créer une fonction.

Exemple avec la configuration de sortie :

```python
def configurer_sortie():
    ...
```

Le programme peut ensuite simplement faire :

```python
mode_sortie, nom_rapport = configurer_sortie()
```

Cette fonction peut être réutilisée au démarrage et lors d'un changement de fichier.

---

## 18. Architecture retenue pour V2

```text
lire_fichier()
      ↓
fichier chargé
      ↓
configurer_sortie()
      │
      ├── terminal
      │
      └── fichier
             ↓
       choisir_mode_fichier()
             ↓
          w / a / x
             ↓
         nom_rapport
      ↓
menu principal
      ↓
analyse
      ↓
résultat
      ↓
terminal / rapport
```

---

## 19. Idées retenues pour V3

Pour LogAnalyzer V3 :

- accepter uniquement des fichiers `.log` en entrée ;
- créer uniquement des rapports `.txt` ;
- afficher les fichiers `.log` disponibles avant la sélection ;
- afficher les rapports `.txt` existants ;
- utiliser `pathlib` pour travailler avec les chemins et fichiers ;
- ajouter des statistiques générales ;
- afficher un Top N des IP suspectes ;
- demander confirmation avant d'écraser un rapport ;
- améliorer encore la séparation entre analyse et affichage ;
- commencer à utiliser les expressions régulières (`regex`).