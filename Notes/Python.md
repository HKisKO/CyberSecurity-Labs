# Python Cheat Sheet

## Dictionnaires

Créer un dictionnaire :

```python
services = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS"
}
```

Accéder à une valeur :

```python
services[22]
```

Tester si une clé existe :

```python
if 22 in services:
    print(services[22])
```

Parcourir clés et valeurs :

```python
for port, service in services.items():
    print(port, service)
```

Tester les valeurs :

```python
if "SSH" in services.values():
    print("Service existant")
```

Ajouter ou modifier :

```python
services[53] = "DNS"
```

Supprimer :

```python
services.pop(53)
```

`pop()` peut aussi récupérer la valeur supprimée :

```python
service = services.pop(53)
```

---

## Fonctions

Une fonction permet de regrouper une tâche précise.

```python
def afficher_services():
    for port, service in services.items():
        print(port, service)
```

Appel :

```python
afficher_services()
```

### return

`return` permet de renvoyer une valeur :

```python
def menu():
    choix = int(input("Choix : "))
    return choix
```

Mais `return` permet aussi de quitter immédiatement une fonction :

```python
if port in services:
    print("Port déjà existant")
    return
```

---

## Boucle while

```python
while True:
    choix = input("Choix : ")
```

`while True` continue tant qu'on ne provoque pas une sortie.

### break

`break` quitte la boucle :

```python
while True:
    choix = input("Choix : ")

    if choix == "6":
        break
```

### continue

`continue` recommence immédiatement l'itération suivante de la boucle :

```python
while True:
    choix = input("Choix : ")

    if choix == "":
        continue
```

Différence importante :

- `return` → quitte la fonction
- `break` → quitte la boucle
- `continue` → recommence la boucle

---

## Gestion des erreurs — try / except

Une conversion peut provoquer une erreur :

```python
port = int(input("Port : "))
```

Si l'utilisateur entre :

```text
bonjour
```

Python provoque :

```text
ValueError
```

On peut empêcher le programme de planter :

```python
try:
    port = int(input("Port : "))

except ValueError:
    print("Le port doit être un entier.")
```

Avec une boucle :

```python
while True:
    try:
        port = int(input("Port : "))
        break

    except ValueError:
        print("Veuillez entrer un entier.")
```

---

## input() et types

`input()` retourne toujours une chaîne de caractères :

```python
nom = input("Nom : ")
```

Il n'est donc pas nécessaire de faire :

```python
str(input("Nom : "))
```

Pour récupérer un entier :

```python
port = int(input("Port : "))
```

---

## Manipulation de chaînes

Convertir en majuscules :

```python
service = input("Service : ").upper()
```

Exemple :

```text
ssh → SSH
```

Attention :

```python
.upper()
```

exécute la méthode.

Alors que :

```python
.upper
```

fait référence à la méthode sans l'exécuter.

---

## Bonnes pratiques apprises avec ServiceManager

Éviter de répéter du code.

Au lieu de répéter plusieurs fois le menu, créer :

```python
def menu():
    ...
```

Donner des responsabilités précises aux fonctions :

```text
menu()
afficher_services()
rechercher_par_port()
rechercher_par_service()
ajout_de_services()
delete_service()
```

Un programme devient ainsi plus facile à lire, tester et modifier.