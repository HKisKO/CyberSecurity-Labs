# NetworkDiagnosticLab

Laboratoire pratique de diagnostic réseau sous Linux.

L'objectif est de construire une méthodologie structurée permettant d'identifier l'origine d'un problème réseau, depuis l'interface locale jusqu'aux services réseau.

## Objectifs

- Identifier les interfaces réseau disponibles
- Vérifier l'état d'une interface
- Analyser la configuration IPv4 et IPv6
- Identifier le sous-réseau d'une machine
- Lire une table de routage
- Identifier la passerelle par défaut
- Tester progressivement la connectivité
- Distinguer un problème réseau d'un problème DNS
- Identifier les serveurs DNS utilisés
- Examiner les sockets TCP et UDP
- Identifier les ports en écoute
- Associer un port à un processus et à son PID
- Comprendre la socket activation avec systemd

## Méthodologie de diagnostic

Le diagnostic est effectué progressivement :

```text
Interface réseau
      ↓
Configuration IP
      ↓
Table de routage
      ↓
Passerelle
      ↓
Connectivité Internet
      ↓
Résolution DNS
      ↓
Sockets / ports
      ↓
Processus / services
```

Cette méthode permet d'isoler le niveau auquel se situe une panne au lieu de lancer des commandes au hasard.

## Interfaces réseau

Commande utilisée :

```bash
ip link
```

Interfaces observées pendant le laboratoire :

```text
lo          → loopback
enp0s31f6   → Ethernet
wlp2s0      → Wi-Fi
virbr0      → bridge réseau virtuel
```

Les états `UP`, `LOWER_UP`, `DOWN` et `NO-CARRIER` permettent d'obtenir des informations sur l'état administratif et physique d'une interface.

## Configuration IP

Commande :

```bash
ip addr show wlp2s0
```

Exemple observé :

```text
IPv4      : 10.54.209.93/24
Réseau    : 10.54.209.0/24
Broadcast : 10.54.209.255
```

Cette étape permet de vérifier que la machine possède une configuration IP cohérente.

## Routage

Commande :

```bash
ip route
```

Routes observées :

```text
default via 10.54.209.74 dev wlp2s0
10.54.209.0/24 dev wlp2s0
```

Une destination appartenant au même sous-réseau peut être atteinte directement.

Une destination extérieure utilise la route par défaut et la passerelle comme prochain saut.

## Tests de connectivité

Les tests sont effectués dans un ordre précis.

### Passerelle locale

```bash
ping -c 4 10.54.209.74
```

Permet de vérifier la communication avec la passerelle.

### Internet sans DNS

```bash
ping -c 4 8.8.8.8
```

Permet de tester la connectivité IP extérieure sans dépendre de la résolution DNS.

### Résolution de nom

```bash
ping -c 4 google.com
```

Si une IP publique fonctionne mais qu'un nom de domaine ne peut pas être résolu, le diagnostic peut s'orienter vers le DNS.

## DNS

Commande utilisée :

```bash
resolvectl status
```

Exemple observé :

```text
Current DNS Server: 10.54.209.74
DNS Servers:        10.54.209.74
```

Cette commande permet d'identifier les serveurs DNS configurés et le serveur actuellement utilisé.

## Sockets et ports

Commande :

```bash
ss -tuln
```

Options :

```text
-t → TCP
-u → UDP
-l → sockets en écoute
-n → affichage numérique
```

Quelques ports observés pendant le laboratoire :

```text
22   → SSH
80   → HTTP
3306 → MySQL
8081 → service local
```

Les adresses d'écoute donnent également une information importante :

```text
127.0.0.1:PORT → loopback / accès local
0.0.0.0:PORT   → interfaces IPv4
[::]:PORT      → interfaces IPv6
```

## Port vers processus

Pour identifier le processus propriétaire d'un socket :

```bash
sudo ss -tulnp
```

Exemples réellement observés :

```text
22   → systemd
80   → apache2
3306 → mysqld
8081 → bettercap
```

Cette analyse permet de suivre la chaîne :

```text
port
 ↓
socket
 ↓
processus
 ↓
PID
```

## Socket activation avec systemd

Le port `22` était possédé par `systemd` plutôt que directement par `sshd`.

Vérification :

```bash
systemctl status ssh.socket
systemctl status ssh.service
systemctl list-sockets
```

État observé :

```text
ssh.socket
→ enabled
→ active (listening)

ssh.service
→ disabled
→ inactive (dead)
```

`ssh.socket` écoute sur le port TCP 22 et peut déclencher `ssh.service` lorsqu'une connexion arrive.

```text
systemd
   ↓
ssh.socket
   ↓
connexion TCP :22
   ↓
ssh.service
   ↓
sshd
```

Cela montre qu'un service `inactive` ne signifie pas nécessairement que son point d'entrée réseau est inaccessible.

## Commandes pratiquées

```bash
ip link
ip addr
ip route
ping
resolvectl
ss -tuln
ss -tulnp
systemctl status
systemctl list-sockets
```

## Compétences travaillées

Ce laboratoire relie plusieurs notions :

```text
Subnetting
    +
Routage IP
    +
DNS
    +
TCP / UDP
    +
Ports
    +
Processus Linux
    +
Services systemd
```

L'objectif principal est de savoir **où chercher lorsqu'un problème réseau est signalé**, et de vérifier chaque couche progressivement avant de passer à la suivante.