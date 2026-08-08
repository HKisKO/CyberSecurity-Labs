# Python Cheat Sheet

## Dictionnaires

Créer

services = {
    22: "SSH",
    80: "HTTP"
}

---

Accéder

services[22]

---

Ajouter

services[21] = "FTP"

---

Modifier

services[80] = "HTTP/1.1"

---

Supprimer

services.pop(21)

---

Parcourir

for port, service in services.items():

---

Clés

services.keys()

---

Valeurs

services.values()

---

Longueur

len(services)

---

Tri

sorted(services)

---

Recherche

if port in services:

---

Entrée utilisateur

input()

int(input())