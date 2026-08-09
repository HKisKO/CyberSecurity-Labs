# IPv4

## Qu'est-ce qu'une adresse IPv4 ?

C'un identifiant logique ,elle est sur 4 octets sous forme X.X.X.X ou x represente un octet en decimale entre 0 et 255 . Il y a des adresses privées et publics . Il y a trois type d adresses : hotes , defusions et réseaux.

### Définition plus technique :
Une adresse IPv4 est une adresse logique de 32 bits attribuée à une interface réseau. Elle permet notamment d'identifier son réseau et l'interface dans ce réseau.

---

## Structure d'une adresse IPv4

Exemple :

192.168.1.15

- 4 octets chaque octet = 8 bits
- 32 bits
- Chaque octet est compris entre 0 et 255

---

## Adresse réseau
### definition:
c'est la partie en commun des adresses hôtes. Il existe des adresses réseaux publiques et privées.

### À quoi sert-elle
 identifier le reseau localement et au niveau exterieur 

Exemple : 10.0.0.0/24 privé et 200.0.0.0/8(publique /sur internet)

---

## Adresse hôte
Une adresse IP d'hôte est un numéro unique qui sert à identifier un appareil précis (ordinateur, téléphone ou imprimante) connecté à un réseau informatique. Elle se compose d'une partie réseau et d'une partie propre à la machine.

---

## Broadcast
Une adresse de broadcast (ou adresse de diffusion) est une adresse IP spéciale qui permet d'envoyer un message ou des données à tous les appareils d'un même réseau local (LAN) en une seule fois, sans avoir à connaître l'adresse de chaque machine


---

## Masque de sous-réseau

Un masque de sous-réseau est un nombre de 32 bits qui sépare une adresse IP en deux parties : la partie réseau (le lieu) et la partie hôte (la machine). Il indique quels appareils se trouvent sur le même réseau local et lesquels nécessitent un routeur pour communiquer.

---

## Résumé

Les trois adresses importantes :

- Network 
- Host 
- Broadcast

---

## Calcul d'un sous-réseau

Pour analyser une adresse IPv4 avec son préfixe CIDR :

### 1. Trouver les bits réseau et hôte

Une adresse IPv4 contient 32 bits.

Exemple avec `/27` :

- Bits réseau : 27
- Bits hôte : 32 - 27 = 5

### 2. Trouver le masque

Quelques masques utiles :

| CIDR | Masque |
|------|-----------------|
| /8   | 255.0.0.0 |
| /16  | 255.255.0.0 |
| /24  | 255.255.255.0 |
| /25  | 255.255.255.128 |
| /26  | 255.255.255.192 |
| /27  | 255.255.255.224 |
| /28  | 255.255.255.240 |

### 3. Trouver la taille du bloc

Exemple avec `/27` :

5 bits sont disponibles pour la partie hôte.

2^5 = 32 adresses par bloc.

Les blocs sont donc :

0 - 31
32 - 63
64 - 95
96 - 127
128 - 159
160 - 191
192 - 223
224 - 255

### 4. Trouver le nombre d'hôtes utilisables

Nombre d'adresses du bloc - 2 :

- une adresse pour le réseau ;
- une adresse pour le broadcast.

Exemple `/27` :

2^5 - 2 = 30 hôtes utilisables.

---

## Exemple complet

Adresse :

`10.20.30.197/27`

Résultat :

- Masque : `255.255.255.224`
- Taille du bloc : 32
- Adresse réseau : `10.20.30.192`
- Premier hôte : `10.20.30.193`
- Dernier hôte : `10.20.30.222`
- Broadcast : `10.20.30.223`
- Hôtes utilisables : 30

## À utiliser :
- 2^0 = 1
- 2^1 = 2
- 2^2 = 4
- 2^3 = 8
- 2^4 = 16
- 2^5 = 32
- 2^6 = 64
- 2^7 = 128


