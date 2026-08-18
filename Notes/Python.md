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



# Fichiers & exceptions

## Lire un fichier

```python
with open("auth.log", "r") as fichier:
    for ligne in fichier:
        print(ligne, end="")
```

`with open()` permet d'ouvrir un fichier et de le refermer automatiquement à la fin du bloc.

---

## Découper une ligne avec split()

```python
ligne = "Failed password for root from 10.0.0.25"

mots = ligne.split()

print(mots)
```

Résultat :

```text
['Failed', 'password', 'for', 'root', 'from', '10.0.0.25']
```

Récupérer le dernier élément :

```python
adresse_ip = mots[-1]
```

---

## FileNotFoundError

Si un fichier n'existe pas :

```python
with open("auth.log", "r") as fichier:
```

Python peut déclencher :

```text
FileNotFoundError
```

Gestion avec `try / except` :

```python
try:
    with open("auth.log", "r") as fichier:
        for ligne in fichier:
            print(ligne, end="")

except FileNotFoundError as erreur:
    print(f"ERREUR : fichier {erreur.filename} introuvable.")
```

L'objet `erreur` peut contenir plusieurs informations :

```python
erreur.filename
erreur.errno
erreur.strerror
```

---

## Compter des occurrences avec un dictionnaire

Exemple : compter les échecs par adresse IP.

```python
echecs_par_ip = {}

if adresse_ip in echecs_par_ip:
    echecs_par_ip[adresse_ip] += 1
else:
    echecs_par_ip[adresse_ip] = 1
```

Le dictionnaire peut alors devenir :

```python
{
    "10.0.0.25": 3,
    "172.16.1.44": 1
}
```

Parcourir le résultat :

```python
for adresse, nombre_echec in echecs_par_ip.items():
    print(adresse, nombre_echec)
```

---

## Pattern d'analyse de logs

```text
ouvrir le fichier
        ↓
parcourir ligne par ligne
        ↓
filtrer les lignes intéressantes
        ↓
extraire les données
        ↓
compter / agréger
        ↓
afficher ou détecter
```

Exemple utilisé dans LogAnalyzer :

```text
Failed password
        ↓
extraire l'IP
        ↓
compter les échecs
        ↓
si échecs >= 3
        ↓
IP suspecte
```

## LogAnalyzer V2 — Concepts Python

### Modes d'ouverture d'un fichier

```python
"r"  # lecture
"w"  # écriture / remplacement
"a"  # ajout à la fin
"x"  # création exclusive
```

- `w` écrase le contenu existant.
- `a` conserve le contenu et ajoute à la fin.
- `x` provoque `FileExistsError` si le fichier existe déjà.

### Lecture complète d'un fichier

```python
with open(nom_fichier, "r") as fichier:
    lignes = fichier.readlines()
```

`readlines()` retourne une liste contenant les lignes du fichier.

### Écriture dans un fichier

```python
with open(nom_rapport, "a") as fichier:
    fichier.write("Résultat\n")
```

`write()` n'ajoute pas automatiquement de retour à la ligne contrairement à `print()`.

### Ajouter un élément à une liste

```python
ip_echecs = []
ip_echecs.append(adresse_ip)
```

### Trier selon une valeur

```python
classement = sorted(
    dictionnaire.items(),
    key=lambda element: element[1],
    reverse=True
)
```

- `element[0]` → clé
- `element[1]` → valeur
- `reverse=True` → ordre décroissant

`sorted()` retourne ici une liste de tuples.

### Exceptions travaillées

```python
FileNotFoundError
FileExistsError
ValueError
```

### Contrôle des boucles

```python
continue
```

Passe immédiatement à l'itération suivante.

```python
break
```

Quitte la boucle.

```python
return
```

Quitte la fonction et peut retourner une ou plusieurs valeurs.

### Retourner plusieurs valeurs

```python
return nom_fichier, lignes
```

Puis :

```python
nom_fichier, lignes = lire_fichier()
```

### Construire progressivement une chaîne

```python
resultat = "===== ANALYSE =====\n"

for adresse, nombre in classement:
    resultat += f"{adresse} : {nombre}\n"
```

Le même résultat peut ensuite être envoyé vers différentes destinations :

```python
print(resultat)
```

ou :

```python
fichier.write(resultat)
```

### Principe de séparation

Une analyse ne devrait pas être répétée simplement parce que sa destination change.

```text
Données
  ↓
Analyse
  ↓
Résultat
  ↓
Destination
  ├── Terminal
  └── Fichier
```

### Refactoring

Lorsqu'un même bloc de logique est utilisé à plusieurs endroits, il peut être déplacé dans une fonction réutilisable.

Exemple :

```python
mode_sortie, nom_rapport = configurer_sortie()
```


# Python — Sockets TCP et gestion des erreurs

## Créer une socket TCP IPv4

Module :

```python
import socket
```

Création :

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

Signification :

```text
AF_INET     → IPv4
SOCK_STREAM → socket orientée flux → TCP
```

Une socket permet à un programme de communiquer via le réseau.

---

## Tester une connexion TCP

```python
resultat = sock.connect_ex((ip, port))
```

Exemple :

```python
resultat = sock.connect_ex(("127.0.0.1", 22))
```

`connect_ex()` tente d'établir une connexion TCP et retourne un code.

```text
0
→ connexion réussie
```

Un résultat différent de `0` correspond à une erreur qu'il faut interpréter.

---

## Timeout

```python
sock.settimeout(1)
```

Permet de limiter le temps d'attente des opérations bloquantes de la socket.

```text
Connexion refusée
→ une réponse indique que la connexion ne peut pas être établie

Timeout
→ aucune réponse exploitable dans le délai configuré
```

---

## errno

```python
import errno
```

Permet d'utiliser des noms explicites pour les codes d'erreur système.

```python
if resultat == errno.ECONNREFUSED:
    status = "FERME"

elif resultat == errno.ETIMEDOUT:
    status = "TIMEOUT"
```

À préférer à :

```python
if resultat == 111:
```

car le nom de l'erreur rend le code plus compréhensible.

---

## os.strerror()

```python
import os
```

Convertit un code d'erreur système en message lisible :

```python
os.strerror(resultat)
```

Exemple observé :

```text
111
↓
Connection refused
```

Différence :

```text
errno
→ identifier/comparer une erreur

os.strerror()
→ afficher le message associé à l'erreur
```

---

## try / except / finally

Structure :

```python
try:
    # opération susceptible d'échouer

except socket.error as erreur:
    # traitement de l'erreur

finally:
    sock.close()
```

### try

Exécute le code susceptible de produire une exception.

### except

Intercepte une exception.

### finally

S'exécute dans tous les cas.

Même si un `return` se trouve dans `try`, le bloc `finally` est exécuté avant de quitter la fonction.

Utile pour libérer des ressources :

```python
finally:
    sock.close()
```

---

## Exceptions socket

Exception générale :

```python
except socket.error as erreur:
```

Exception plus spécifique liée à la résolution d'une adresse :

```python
except socket.gaierror as erreur:
```

Ordre recommandé :

```python
except socket.gaierror as erreur:
    # erreur spécifique

except socket.error as erreur:
    # erreur plus générale
```

Toujours traiter l'exception spécifique avant l'exception générale.

---

## Valider une IPv4

Module :

```python
import ipaddress
```

Validation :

```python
ipaddress.IPv4Address(ip)
```

Exemples :

```text
127.0.0.1    → valide
192.168.1.10 → valide

127.0.       → ValueError
999.1.1.1    → ValueError
::1          → ValueError pour IPv4Address
```

Gestion :

```python
try:
    ipaddress.IPv4Address(ip)

except ValueError:
    print("Adresse IPv4 invalide.")
```

---

## Validation utilisateur avec while

```python
while True:
    try:
        ip = input("Adresse IPv4 : ")

        ipaddress.IPv4Address(ip)

        break

    except ValueError:
        print("Adresse IPv4 invalide.")
```

Logique :

```text
input
 ↓
validation
 ↓
invalide → except → recommencer
 ↓
valide → break
```

---

## Dictionnaires et .items()

Exemple :

```python
services = {
    22: "SSH",
    80: "HTTP",
    3306: "MySQL"
}
```

Parcourir les clés et valeurs :

```python
for port, service in services.items():
    print(port, service)
```

Produit successivement :

```text
22   SSH
80   HTTP
3306 MySQL
```

---

## Séparer la logique dans une fonction

Exemple :

```python
def verifier_port(ip, port):
    # logique réseau
    return status
```

Puis :

```python
for port, service in services.items():
    statut = verifier_port(ip, port)
    print(f"{ip}:{port} {service} → {statut}")
```

Principe :

```text
fonction
→ effectue une tâche précise

programme principal
→ orchestre les différentes tâches
```

Cela rend le code plus lisible et réutilisable.

---

## Une ressource doit être libérée

Lorsqu'une socket est créée :

```python
sock = socket.socket(...)
```

elle doit être fermée lorsqu'elle n'est plus nécessaire :

```python
sock.close()
```

Pour plusieurs connexions :

```text
itération 1
→ créer socket
→ utiliser
→ fermer

itération 2
→ créer nouvelle socket
→ utiliser
→ fermer
```

Ne pas essayer de réutiliser une socket déjà fermée.

---

# Schéma à retenir

```text
input utilisateur
       ↓
validation
       ↓
boucle
       ↓
fonction
       ↓
création ressource
       ↓
try
       ↓
opération
       ↓
gestion du résultat
       ↓
except si exception
       ↓
finally
       ↓
libération ressource
       ↓
return
```

## Nouveaux concepts vus avec ServiceChecker V1

```text
socket
AF_INET
SOCK_STREAM
connect_ex()
settimeout()

errno
os.strerror()

try
except
finally

socket.error
socket.gaierror

ipaddress
IPv4Address()

.items()
validation utilisateur
gestion des ressources
```