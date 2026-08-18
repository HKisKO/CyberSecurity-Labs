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



# Diagnostic réseau Linux

## Méthodologie

Lorsqu'un problème réseau est signalé, diagnostiquer progressivement :

```text
Interface
   ↓
Configuration IP
   ↓
Routage
   ↓
Passerelle
   ↓
Connectivité Internet
   ↓
DNS
   ↓
Sockets / ports
   ↓
Processus / services
```

L'objectif est d'isoler le niveau de la panne avant d'agir.

---

## Interfaces réseau

Afficher les interfaces :

```bash
ip link
```

États importants :

```text
UP         → interface administrativement activée
LOWER_UP   → lien réseau présent
NO-CARRIER → absence de lien physique
DOWN       → lien/interface non opérationnel
```

Interfaces courantes :

```text
lo       → loopback
enp...   → Ethernet
wlp...   → Wi-Fi
virbr... → bridge virtuel
```

---

## Configuration IP

```bash
ip addr
```

Pour une interface précise :

```bash
ip addr show <interface>
```

Permet notamment d'identifier :

```text
adresse IPv4
préfixe CIDR
broadcast
adresse MAC
adresse IPv6
```

Exemple :

```text
10.54.209.93/24

Réseau    → 10.54.209.0/24
Masque    → 255.255.255.0
Broadcast → 10.54.209.255
```

`dynamic` indique généralement une configuration obtenue automatiquement via DHCP.

---

## Routage

Afficher la table de routage :

```bash
ip route
```

Exemple :

```text
default via 10.54.209.74 dev wlp2s0
10.54.209.0/24 dev wlp2s0
```

Destination dans le même sous-réseau :

```text
machine → destination
```

Destination extérieure :

```text
machine
   ↓
passerelle / next hop
   ↓
autres réseaux
```

La route `default` est utilisée lorsqu'aucune route plus spécifique ne correspond à la destination.

---

## Diagnostic avec ping

Tester d'abord la passerelle :

```bash
ping -c 4 <passerelle>
```

Puis tester Internet directement par IP :

```bash
ping -c 4 8.8.8.8
```

Puis tester la résolution de nom :

```bash
ping -c 4 google.com
```

Interprétation :

```text
Passerelle KO
→ problème local / accès à la passerelle

Passerelle OK
IP publique KO
→ problème de routage/connectivité extérieure possible

IP publique OK
Nom de domaine KO
→ problème DNS possible
```

`ping` utilise ICMP. L'absence de réponse à un ping ne prouve pas à elle seule qu'un service ou une machine est indisponible.

---

## DNS

Afficher la configuration DNS :

```bash
resolvectl status
```

Informations importantes :

```text
Current DNS Server
DNS Servers
```

`DNS Servers` peut contenir plusieurs serveurs DNS.

La configuration DNS peut notamment être :

```text
automatique → DHCP
manuelle    → configuration réseau
```

Ne pas confondre :

```text
serveur DNS
```

avec :

```text
adresse IP retournée par le DNS pour un nom de domaine
```

---

# TCP / UDP / Sockets

## TCP

TCP est orienté connexion.

Établissement classique :

```text
SYN
 ↓
SYN-ACK
 ↓
ACK
```

C'est le `3-way handshake`.

Un socket TCP attendant des connexions apparaît généralement comme :

```text
LISTEN
```

## UDP

UDP est sans connexion.

Il n'utilise pas le 3-way handshake TCP.

Dans `ss`, un socket UDP apparaît généralement comme :

```text
UNCONN
```

---

## Afficher les sockets

```bash
ss -tuln
```

Options :

```text
-t → TCP
-u → UDP
-l → listening
-n → affichage numérique
```

Adresses importantes :

```text
127.0.0.1:PORT
→ écoute locale / loopback

0.0.0.0:PORT
→ écoute sur les interfaces IPv4

[::]:PORT
→ écoute IPv6
```

---

## Identifier le processus derrière un port

```bash
sudo ss -tulnp
```

Le `-p` affiche les informations concernant le processus propriétaire du socket.

Relation :

```text
Port
 ↓
Socket
 ↓
Processus
 ↓
PID
```

Exemples rencontrés :

```text
22   → SSH / systemd socket activation
80   → apache2
3306 → mysqld
8081 → bettercap
```

Attention :

```bash
grep "22"
```

cherche `22` partout dans une ligne et pas uniquement dans le numéro de port.

---

# systemd socket activation

Certaines unités systemd peuvent écouter sur un socket et déclencher un service uniquement lorsqu'il est nécessaire.

Exemple rencontré avec SSH :

```text
systemd
   ↓
ssh.socket
   ↓
écoute TCP :22
   ↓
connexion entrante
   ↓
trigger
   ↓
ssh.service
   ↓
sshd
```

Commandes utiles :

```bash
systemctl status ssh.socket
systemctl status ssh.service
systemctl list-sockets
```

Un service :

```text
inactive
```

n'est donc pas nécessairement inaccessible si une unité `.socket` correspondante est active.

Ne pas confondre :

```text
enabled  → activation configurée au démarrage
active   → unité actuellement active
```

---

# Commandes essentielles

```bash
ip link
ip addr
ip route

ping -c 4 <destination>

resolvectl status

ss -tuln
sudo ss -tulnp

systemctl status <unité>
systemctl list-sockets
```

## Principe

Toujours associer une commande à une question :

```text
ip link
→ Mon interface et mon lien sont-ils opérationnels ?

ip addr
→ Ai-je une configuration IP ?

ip route
→ Où la machine va-t-elle envoyer le paquet ?

ping
→ La destination répond-elle à ICMP ?

resolvectl
→ Quelle configuration DNS est utilisée ?

ss
→ Quels sockets et ports sont présents ?

ss -p
→ Quel processus possède le socket ?

systemctl
→ Quel est l'état de l'unité correspondante ?
```

# DNS — Domain Name System

## Rôle du DNS

Le DNS permet notamment de résoudre un nom de domaine en adresse IP.

```text
google.com
    ↓ DNS
172.217.x.x
```

Une machine peut avoir une connectivité IP fonctionnelle mais une résolution DNS défaillante.

```text
ping 8.8.8.8     → FONCTIONNE
ping google.com  → ÉCHEC

→ problème DNS possible
→ investigation nécessaire avant de conclure
```

---

## DNS sous Ubuntu avec systemd-resolved

Afficher la configuration utilisée par les clients locaux :

```bash
cat /etc/resolv.conf
```

Exemple :

```text
nameserver 127.0.0.53
```

`127.0.0.53` est le stub DNS local de `systemd-resolved`.

Il ne faut pas le confondre avec le serveur DNS configuré sur l'interface réseau.

Afficher la configuration DNS réelle :

```bash
resolvectl status
```

Exemple observé :

```text
Interface : wlp2s0
Stub local : 127.0.0.53
DNS réseau : 192.168.1.1
```

Chaîne simplifiée :

```text
Application
     ↓
127.0.0.53:53
Stub local
     ↓
systemd-resolved
     ↓
wlp2s0
     ↓
192.168.1.1
DNS réseau
     ↓
Infrastructure DNS
```

---

## Listeners DNS locaux

Afficher les processus écoutant sur le port DNS :

```bash
sudo ss -lntup | grep ':53'
```

Observé avec `systemd-resolved` :

```text
127.0.0.53:53
127.0.0.54:53
```

`127.0.0.53` est le stub local principal utilisé via `/etc/resolv.conf`.

`127.0.0.54` est un second listener local de `systemd-resolved` avec un fonctionnement de proxy plus direct.

Le DNS utilise principalement :

```text
UDP/53
```

mais peut également utiliser :

```text
TCP/53
```

---

## dig

Résolution avec la configuration DNS normale :

```bash
dig google.com
```

Identifier notamment :

```text
status: NOERROR
SERVER: 127.0.0.53#53
```

Interroger directement un serveur DNS :

```bash
dig @192.168.1.1 google.com
```

Tester un DNS alternatif :

```bash
dig @8.8.8.8 google.com
```

Syntaxe :

```text
dig @DNS domaine type
```

---

## Principaux enregistrements DNS

```text
A      → adresse IPv4
AAAA   → adresse IPv6
NS     → serveurs DNS autoritatifs
MX     → serveurs de messagerie
CNAME  → alias vers un autre nom
```

Commandes :

```bash
dig google.com A
dig google.com AAAA
dig google.com NS
dig google.com MX
dig www.github.com CNAME
```

### MX

Exemple :

```text
10 smtp.google.com.
```

`10` représente la priorité.

Plus la valeur est faible, plus le serveur MX est prioritaire.

### CNAME

Exemple :

```text
www.github.com
      ↓ CNAME
github.com
```

`www.github.com` est l'alias.

---

## TTL

TTL signifie :

```text
Time To Live
```

Exemple :

```text
google.com.   176   IN   A   172.217.x.x
              ↑
             TTL
```

Le TTL indique combien de temps une donnée DNS peut rester valide dans un cache.

```text
176 → 175 → 174 → ... → 0
```

À expiration, une nouvelle résolution est nécessaire si aucune autre réponse valide n'est disponible.

---

## Cache DNS

Afficher les statistiques :

```bash
resolvectl statistics
```

Informations importantes :

```text
Current Cache Size
Cache Hits
Cache Misses
```

### Cache Hit

```text
requête
   ↓
réponse valide déjà en cache
   ↓
réutilisation
```

### Cache Miss

```text
requête
   ↓
réponse absente / inutilisable
   ↓
requête vers DNS amont
```

Vider le cache :

```bash
sudo resolvectl flush-caches
```

Tester :

```bash
resolvectl query google.com
```

Après vidage du cache :

```text
Data from: network
```

Une requête suivante peut donner :

```text
Data from: cache
```

Le cache conserve des réponses DNS obtenues précédemment. Il ne crée pas lui-même les informations DNS.

---

## Hiérarchie DNS

Observer la résolution :

```bash
dig +trace google.com
```

Chaîne simplifiée :

```text
Root "."
   ↓
TLD ".com"
   ↓
Serveurs autoritatifs de google.com
   ↓
Enregistrement A
   ↓
Adresse IPv4
```

Le serveur Root indique où trouver les serveurs du TLD.

Le TLD indique quels serveurs sont autoritatifs pour le domaine.

Le serveur autoritatif fournit les données DNS du domaine.

---

## Diagnostic d'une panne DNS

Scénario :

```text
ping 8.8.8.8
→ FONCTIONNE

ping google.com
→ ÉCHEC
```

### 1. Vérifier la configuration

```bash
cat /etc/resolv.conf
resolvectl status
```

### 2. Tester la résolution normale

```bash
dig google.com
```

### 3. Tester directement le DNS configuré

```bash
dig @192.168.1.1 google.com
```

### 4. Tester un DNS alternatif

```bash
dig @8.8.8.8 google.com
```

### Cas : problème local

```text
dig google.com
→ ÉCHEC

dig @192.168.1.1 google.com
→ FONCTIONNE
```

Principal suspect :

```text
stub 127.0.0.53
systemd-resolved
configuration DNS locale
```

### Cas : DNS configuré suspect

```text
dig google.com
→ ÉCHEC

dig @192.168.1.1 google.com
→ ÉCHEC

dig @8.8.8.8 google.com
→ FONCTIONNE
```

Principal suspect :

```text
DNS configuré sur l'interface
ou chemin réseau vers celui-ci
```

---

## Méthode à retenir

```text
IP fonctionne mais domaine échoue
              ↓
      suspecter DNS
              ↓
      /etc/resolv.conf
              ↓
       resolvectl status
              ↓
         dig domaine
              ↓
      dig @DNS_interface
              ↓
       dig @DNS_alternatif
              ↓
       comparer les résultats
              ↓
       isoler le problème
```

Ne pas modifier la configuration avant d'avoir identifié le maillon suspect.