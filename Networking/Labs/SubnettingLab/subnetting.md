# IPv4 Subnetting - Notes

## IPv4 et CIDR

Une adresse IPv4 contient :

```text
32 bits
```

Un préfixe comme :

```text
/27
```

signifie :

```text
27 bits réseau
5 bits hôte
```

Calcul :

```text
Bits hôte = 32 - préfixe CIDR
```

---

## Nombre d'adresses

Avec `n` bits hôte :

```text
Nombre total d'adresses = 2^n
```

Dans les exercices classiques :

```text
Hôtes utilisables = 2^n - 2
```

Les deux adresses réservées sont :

```text
Adresse réseau
Adresse broadcast
```

Exemple `/27` :

```text
32 - 27 = 5 bits hôte

2^5 = 32 adresses
32 - 2 = 30 hôtes utilisables
```

---

## Masques fréquents

| CIDR | Masque | Taille bloc | Hôtes utilisables |
|---|---|---:|---:|
| `/24` | `255.255.255.0` | 256 | 254 |
| `/25` | `255.255.255.128` | 128 | 126 |
| `/26` | `255.255.255.192` | 64 | 62 |
| `/27` | `255.255.255.224` | 32 | 30 |
| `/28` | `255.255.255.240` | 16 | 14 |
| `/29` | `255.255.255.248` | 8 | 6 |

---

## Taille du bloc

Lorsque le subnetting se fait sur le dernier octet :

```text
Taille du bloc = 256 - valeur du masque
```

Exemple `/27` :

```text
256 - 224 = 32
```

Les blocs sont donc :

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

---

## Trouver le réseau

Exemple :

```text
172.16.34.173/27
```

Avec `/27` :

```text
Taille du bloc = 32
```

`173` appartient au bloc :

```text
160 - 191
```

Donc :

```text
Adresse réseau : 172.16.34.160
Broadcast      : 172.16.34.191
Premier hôte   : 172.16.34.161
Dernier hôte   : 172.16.34.190
```

---

## Trouver le préfixe à partir du nombre de machines

Chercher le plus petit `n` tel que :

```text
2^n - 2 >= nombre de machines
```

Exemple pour 25 machines :

```text
2^4 - 2 = 14 → insuffisant
2^5 - 2 = 30 → suffisant
```

Donc :

```text
5 bits hôte
32 - 5 = /27
```

---

# VLSM

VLSM permet d'utiliser des sous-réseaux de tailles différentes dans un même réseau principal.

Principe utilisé dans le lab :

1. classer les besoins du plus grand au plus petit ;
2. déterminer le préfixe nécessaire pour chaque besoin ;
3. attribuer le plus grand sous-réseau en premier ;
4. placer le suivant après le broadcast précédent ;
5. vérifier qu'aucun sous-réseau ne se chevauche.

Exemple :

```text
50 machines → /26
25 machines → /27
12 machines → /28
```

Découpage possible :

```text
192.168.10.0/26
192.168.10.64/27
192.168.10.96/28
```

Plages :

```text
/26 → .0  à .63
/27 → .64 à .95
/28 → .96 à .111
```

Aucun chevauchement.

---

## Raccourci mental

```text
/24 → 254 hôtes
/25 → 126
/26 → 62
/27 → 30
/28 → 14
/29 → 6
```

À retenir :

```text
plus le préfixe CIDR augmente
→ moins il reste de bits hôte
→ plus le sous-réseau est petit
```