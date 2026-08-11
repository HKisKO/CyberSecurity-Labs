# SubnettingLab

Laboratoire réseau consacré au subnetting IPv4 et au VLSM.

## Compétences travaillées

- conversion d'un préfixe CIDR en masque décimal ;
- calcul du nombre de bits réseau et hôte ;
- calcul de la taille d'un bloc ;
- identification de l'adresse réseau ;
- identification de l'adresse de broadcast ;
- calcul de la plage d'hôtes utilisables ;
- choix d'un préfixe selon le nombre de machines ;
- découpage d'un réseau avec VLSM ;
- prévention du chevauchement entre sous-réseaux.

## Exemple de subnetting

Adresse :

```text
192.168.50.142/28
```

Résultat :

```text
Masque           : 255.255.255.240
Taille du bloc   : 16

Adresse réseau   : 192.168.50.128
Premier hôte     : 192.168.50.129
Dernier hôte     : 192.168.50.142
Broadcast        : 192.168.50.143
Hôtes utilisables: 14
```

## Exemple de choix d'un préfixe

Besoin :

```text
50 machines
```

Calcul :

```text
2^5 - 2 = 30 → insuffisant
2^6 - 2 = 62 → suffisant

6 bits hôte
32 - 6 = /26
```

Résultat :

```text
Préfixe : /26
Masque  : 255.255.255.192
Hôtes   : 62
```

## Exemple VLSM

Réseau disponible :

```text
192.168.10.0/24
```

Besoins :

```text
RH          → 50 machines
IT          → 25 machines
Direction   → 12 machines
```

Découpage :

| Département | Réseau | Hôtes utilisables | Broadcast |
|---|---|---:|---|
| RH | `192.168.10.0/26` | 62 | `192.168.10.63` |
| IT | `192.168.10.64/27` | 30 | `192.168.10.95` |
| Direction | `192.168.10.96/28` | 14 | `192.168.10.111` |

Les sous-réseaux sont dimensionnés selon les besoins et ne se chevauchent pas.