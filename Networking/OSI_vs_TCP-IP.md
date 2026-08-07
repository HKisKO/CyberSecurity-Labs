# OSI vs TCP/IP

## Pourquoi existe-t-il plusieurs modèles ?

Les modèles OSI et TCP/IP servent à décrire la manière dont les données circulent entre deux machines connectées à un réseau.

Le modèle OSI est un modèle théorique utilisé principalement pour comprendre le fonctionnement des réseaux.

Le modèle TCP/IP est le modèle réellement utilisé sur Internet.

---

# Modèle OSI

Le modèle OSI est composé de 7 couches.

```
7 Application
6 Présentation
5 Session
4 Transport
3 Réseau
2 Liaison de données
1 Physique
```

---

## Couche 7 – Application

Rôle :

Permet aux applications de communiquer avec le réseau.

Exemples :

- HTTP
- HTTPS
- FTP
- DNS
- SMTP

---

## Couche 6 – Présentation

Rôle :

Transforme les données dans un format compréhensible.

Exemples :

- chiffrement
- compression
- encodage

---

## Couche 5 – Session

Rôle :

Ouvre, maintient et ferme la communication entre deux machines.

---

## Couche 4 – Transport

Rôle :

Assure le transport des données.

Protocoles :

- TCP
- UDP

---

## Couche 3 – Réseau

Rôle :

Permet le routage des paquets entre différents réseaux.

Protocoles :

- IPv4
- IPv6
- ICMP

Équipement :

- Routeur

---

## Couche 2 – Liaison de données

Rôle :

Permet la communication entre deux équipements d'un même réseau local.

Protocoles :

- Ethernet

Adresse utilisée :

Adresse MAC

Équipement :

Switch

---

## Couche 1 – Physique

Rôle :

Transmet les bits sous forme électrique, optique ou radio.

Supports :

- câble cuivre
- fibre
- Wi-Fi

---

# Modèle TCP/IP

Le modèle TCP/IP comporte 4 couches.

```
Application

Transport

Internet

Accès réseau
```

---

## Correspondance

```
OSI                 TCP/IP

Application
Présentation  --->  Application
Session

Transport     --->  Transport

Réseau        --->  Internet

Liaison
Physique      --->  Accès réseau
```

---

# Comparaison

OSI

- 7 couches
- modèle théorique
- utilisé pour apprendre

TCP/IP

- 4 couches
- utilisé sur Internet
- utilisé par tous les systèmes modernes

---

# Les protocoles les plus importants

HTTP

Navigation Web

Couche Application

---

HTTPS

Navigation Web sécurisée

Application

---

DNS

Résolution de noms

Application

---

TCP

Communication fiable

Transport

---

UDP

Communication rapide

Transport

---

IPv4

Adressage

Internet

---

ICMP

Ping

Internet

---

Ethernet

Communication locale

Accès réseau
