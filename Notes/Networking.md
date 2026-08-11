# Networking Cheat Sheet

## Modèles réseau

### OSI

```text
7 - Application
6 - Présentation
5 - Session
4 - Transport
3 - Réseau
2 - Liaison de données
1 - Physique
```

### TCP/IP

```text
Application
Transport
Internet
Accès réseau
```

---

# IPv4

Une adresse IPv4 contient :

```text
32 bits
```

Exemple :

```text
192.168.1.70/25
```

Le préfixe CIDR `/25` signifie :

```text
25 bits réseau
7 bits hôte
```

Formule :

```text
Bits hôte = 32 - préfixe CIDR
```

---

# Subnetting

## Nombre d'adresses

Avec `n` bits hôte :

```text
Adresses totales = 2^n
```

Dans les exercices IPv4 classiques :

```text
Hôtes utilisables = 2^n - 2
```

Une adresse est réservée pour le réseau et une pour le broadcast.

## Masques courants

| CIDR | Masque | Taille bloc | Hôtes utilisables |
|---|---|---:|---:|
| `/24` | `255.255.255.0` | 256 | 254 |
| `/25` | `255.255.255.128` | 128 | 126 |
| `/26` | `255.255.255.192` | 64 | 62 |
| `/27` | `255.255.255.224` | 32 | 30 |
| `/28` | `255.255.255.240` | 16 | 14 |
| `/29` | `255.255.255.248` | 8 | 6 |

## Taille du bloc

Lorsque le découpage concerne le dernier octet :

```text
Taille du bloc = 256 - valeur du masque
```

Exemple :

```text
/27
Masque = 255.255.255.224

256 - 224 = 32
```

Blocs :

```text
0
32
64
96
128
160
192
224
```

## Identifier un sous-réseau

Pour une IP donnée :

```text
Adresse réseau   → première adresse du bloc
Premier hôte     → réseau + 1
Broadcast        → dernière adresse du bloc
Dernier hôte     → broadcast - 1
```

---

# Choisir un préfixe selon le nombre d'hôtes

Chercher le plus petit nombre de bits hôte `n` tel que :

```text
2^n - 2 >= nombre de machines
```

Exemple pour 50 machines :

```text
2^5 - 2 = 30 → insuffisant
2^6 - 2 = 62 → suffisant

6 bits hôte
32 - 6 = /26
```

Donc :

```text
50 machines → /26
```

---

# VLSM

VLSM permet de créer des sous-réseaux de tailles différentes selon les besoins.

Méthode :

```text
1. Classer les besoins du plus grand au plus petit
2. Calculer le préfixe nécessaire
3. Attribuer le plus grand sous-réseau en premier
4. Continuer à partir du bloc disponible suivant
5. Vérifier qu'il n'y a aucun chevauchement
```

Exemple :

```text
50 machines → /26
25 machines → /27
12 machines → /28
```

Allocation possible :

```text
192.168.10.0/26
192.168.10.64/27
192.168.10.96/28
```

---

# Raccourci CIDR

```text
/24 → 254 hôtes
/25 → 126 hôtes
/26 → 62 hôtes
/27 → 30 hôtes
/28 → 14 hôtes
/29 → 6 hôtes
```

Règle importante :

```text
CIDR augmente
      ↓
moins de bits hôte
      ↓
moins d'adresses disponibles
      ↓
sous-réseau plus petit
```