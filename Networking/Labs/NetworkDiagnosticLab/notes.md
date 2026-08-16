# NetworkDiagnosticLab — Notes

## 1. Méthode générale de diagnostic

Lorsqu'un utilisateur signale :

> « Internet ne fonctionne pas. »

Ne pas lancer des commandes au hasard.

Suivre progressivement :

```text
Interface
   ↓
Adresse IP
   ↓
Routage
   ↓
Passerelle
   ↓
Internet
   ↓
DNS
   ↓
Sockets / ports
   ↓
Processus / services
```

---

## 2. Interfaces réseau — ip link

```bash
ip link
```

Permet de voir les interfaces réseau et leur état.

Exemples :

```text
lo          → loopback
enp0s31f6   → Ethernet
wlp2s0      → Wi-Fi
virbr0      → bridge virtuel
```

États importants :

```text
UP
→ interface administrativement activée

LOWER_UP
→ lien réseau détecté/opérationnel

NO-CARRIER
→ aucun lien physique détecté

DOWN
→ interface/lien non opérationnel
```

Une interface `UP` ne signifie pas que l'accès à Internet fonctionne.

---

## 3. Configuration IP — ip addr

```bash
ip addr
```

Pour une interface précise :

```bash
ip addr show wlp2s0
```

Permet notamment d'identifier :

```text
IPv4
préfixe CIDR
broadcast
adresse MAC
IPv6
```

Exemple :

```text
10.54.209.93/24
```

donne :

```text
Adresse machine : 10.54.209.93
Réseau          : 10.54.209.0/24
Masque          : 255.255.255.0
Broadcast       : 10.54.209.255
```

`dynamic` indique une adresse obtenue dynamiquement, typiquement via DHCP.

---

## 4. Table de routage — ip route

```bash
ip route
```

Exemple :

```text
default via 10.54.209.74 dev wlp2s0
10.54.209.0/24 dev wlp2s0
```

La route :

```text
10.54.209.0/24
```

est utilisée pour joindre directement les machines du réseau local.

La route :

```text
default via 10.54.209.74
```

est utilisée lorsqu'aucune route plus spécifique ne correspond à la destination.

La passerelle devient alors le prochain saut (`next hop`).

---

## 5. Tester la passerelle

```bash
ping -c 4 <passerelle>
```

Exemple :

```bash
ping -c 4 10.54.209.74
```

Permet de vérifier :

```text
machine
   ↓
réseau local
   ↓
passerelle
```

Un résultat comme :

```text
4 transmitted
4 received
0% packet loss
```

indique que la passerelle répond aux requêtes ICMP.

---

## 6. Tester Internet sans DNS

```bash
ping -c 4 8.8.8.8
```

Une adresse IP directe permet de tester la connectivité extérieure sans avoir besoin de résoudre un nom de domaine.

Si :

```text
passerelle → OK
8.8.8.8   → OK
```

la connectivité IP vers l'extérieur fonctionne.

---

## 7. Tester la résolution DNS

```bash
ping -c 4 google.com
```

Si :

```text
8.8.8.8    → OK
google.com → échec de résolution
```

le problème peut se situer au niveau DNS.

Lorsqu'on obtient :

```text
google.com → adresse IP
```

cette adresse est l'adresse résolue du serveur distant, et non l'adresse du serveur DNS.

---

## 8. Identifier les serveurs DNS

```bash
resolvectl status
```

Informations importantes :

```text
Current DNS Server
DNS Servers
```

Exemple :

```text
Current DNS Server: 10.54.209.74
DNS Servers:        10.54.209.74
```

`DNS Servers` peut contenir plusieurs serveurs.

Les DNS peuvent notamment être :

```text
obtenus automatiquement
→ DHCP

ou

configurés manuellement
```

`systemd-resolved` gère la résolution DNS sur cette configuration Ubuntu.

---

# TCP / UDP et sockets

## 9. TCP

TCP est orienté connexion.

Établissement classique :

```text
Client                    Serveur

SYN -------------------->
    <---------------- SYN-ACK
ACK -------------------->

connexion établie
```

C'est le `3-way handshake`.

Un serveur TCP en attente d'une connexion apparaît généralement avec :

```text
LISTEN
```

---

## 10. UDP

UDP est sans connexion (`connectionless`).

Il n'utilise pas le 3-way handshake TCP.

Dans `ss`, les sockets UDP apparaissent généralement avec :

```text
UNCONN
```

---

## 11. Afficher les sockets en écoute

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

Permet de répondre à :

```text
Quels ports sont ouverts/en écoute ?
TCP ou UDP ?
Sur quelle adresse locale ?
```

---

## 12. Adresse d'écoute

### Loopback

```text
127.0.0.1:PORT
```

Le service écoute uniquement localement.

Exemple observé :

```text
127.0.0.1:3306
```

---

### Toutes les interfaces IPv4

```text
0.0.0.0:PORT
```

Le socket écoute sur les interfaces IPv4 locales.

Exemple :

```text
0.0.0.0:22
```

---

### IPv6

```text
[::]:PORT
```

Indique une écoute IPv6.

---

## 13. Identifier le processus derrière un port

```bash
sudo ss -tulnp
```

Le `-p` ajoute les informations sur le processus propriétaire du socket.

Exemples observés pendant le lab :

```text
22   → systemd
80   → apache2
3306 → mysqld
8081 → bettercap
```

On peut ainsi suivre :

```text
PORT
 ↓
SOCKET
 ↓
PROCESSUS
 ↓
PID
```

---

## 14. Attention avec grep

Commande :

```bash
sudo ss -tulnp | grep "22"
```

ne signifie pas forcément :

> afficher uniquement le port 22.

`grep` cherche la chaîne `22` partout dans la ligne.

Il peut donc également correspondre à :

```text
192.168.122.1
PID 2237
etc.
```

Toujours vérifier ce qui a réellement été filtré.

---

# systemd et socket activation

## 15. SSH observé pendant le lab

Le port 22 était détenu par :

```text
systemd
PID 1
```

et non directement par `sshd`.

Vérification :

```bash
systemctl status ssh.socket
systemctl status ssh.service
```

Résultat :

```text
ssh.socket
→ enabled
→ active (listening)

ssh.service
→ disabled
→ inactive (dead)
```

---

## 16. Socket activation

Fonctionnement observé :

```text
systemd
   ↓
ssh.socket
   ↓
écoute sur TCP :22
   ↓
connexion entrante
   ↓
trigger
   ↓
ssh.service
   ↓
sshd
```

La socket peut donc attendre la connexion avant que le service correspondant soit démarré.

---

## 17. enabled / active

Ne pas confondre :

```text
enabled
→ configuration concernant notamment l'activation au démarrage

active
→ unité actuellement active
```

Ainsi :

```text
ssh.service → inactive
```

ne suffit pas pour conclure que SSH n'est pas accessible.

Il faut également vérifier :

```bash
systemctl status ssh.socket
ss -tulnp
```

---

## 18. Lister les sockets systemd

```bash
systemctl list-sockets
```

Permet notamment de voir :

```text
LISTEN
UNIT
ACTIVATES
```

Exemple observé :

```text
0.0.0.0:22 → ssh.socket → ssh.service
[::]:22    → ssh.socket → ssh.service
```

---

# Méthode rapide de troubleshooting

## Problème : « Internet ne fonctionne pas »

```text
ip link
   ↓
Interface/lien OK ?

ip addr
   ↓
Adresse IP correcte ?

ip route
   ↓
Route default présente ?

ping <passerelle>
   ↓
Passerelle joignable ?

ping <IP publique>
   ↓
Internet accessible sans DNS ?

résolution d'un nom + resolvectl
   ↓
DNS fonctionnel ?
```

## Problème : « Le service réseau ne fonctionne pas »

```text
ss -tuln
   ↓
Le port écoute ?

Adresse d'écoute ?
   ↓
127.0.0.1 ?
0.0.0.0 ?
[::] ?

sudo ss -tulnp
   ↓
Quel processus ?
Quel PID ?

systemctl status <unité>
   ↓
Service actif ?
Socket active ?
Socket activation ?
```

---

## 19. Principe à retenir

Une commande de diagnostic doit répondre à une question précise.

```text
ip link     → ai-je une interface/lien ?
ip addr     → ai-je une configuration IP ?
ip route    → où seront envoyés mes paquets ?
ping        → cette destination répond-elle à ICMP ?
resolvectl  → quelle est ma configuration DNS ?
ss          → quels sockets/ports sont présents ?
ss -p       → quels processus possèdent ces sockets ?
systemctl   → quel est l'état des unités correspondantes ?
```

Le but n'est pas seulement de mémoriser les commandes, mais de savoir **pourquoi et dans quel ordre les utiliser**.