# NetworkDiagnosticLab — Scénario

## Contexte

Je travaille en tant qu'administrateur Linux junior.

Un utilisateur signale simplement :

> « Internet ne fonctionne pas. »

L'objectif n'est pas de lancer des commandes réseau au hasard, mais de construire une méthodologie de diagnostic permettant d'isoler progressivement l'origine d'un problème.

Le diagnostic est effectué du plus local vers l'extérieur.

## Méthodologie

La démarche utilisée pendant le laboratoire est :

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

---

## Mission 1 — Identifier les interfaces réseau

Afficher les interfaces disponibles :

```bash
ip link
```

Interfaces observées :

```text
lo          → loopback
enp0s31f6   → Ethernet
wlp2s0      → Wi-Fi
virbr0      → bridge réseau virtuel
```

L'interface Wi-Fi `wlp2s0` était active avec :

```text
UP
LOWER_UP
```

L'interface Ethernet était activée administrativement mais ne possédait pas de lien physique :

```text
NO-CARRIER
state DOWN
```

Cette étape permet de vérifier qu'une interface réseau existe et qu'un lien est disponible.

---

## Mission 2 — Vérifier la configuration IP

Afficher la configuration de l'interface Wi-Fi :

```bash
ip addr show wlp2s0
```

Configuration observée :

```text
IPv4      : 10.54.209.93/24
Réseau    : 10.54.209.0/24
Broadcast : 10.54.209.255
IPv6      : fe80::8ef4:9:ec44:486a/64
```

L'adresse IPv4 était indiquée comme dynamique, ce qui correspond à une configuration obtenue automatiquement, typiquement via DHCP.

Cette étape permet de vérifier qu'une adresse IP cohérente a été attribuée à la machine.

---

## Mission 3 — Vérifier le routage

Afficher la table de routage :

```bash
ip route
```

Routes principales observées :

```text
default via 10.54.209.74 dev wlp2s0
10.54.209.0/24 dev wlp2s0
```

La passerelle par défaut était :

```text
10.54.209.74
```

Une destination appartenant au réseau :

```text
10.54.209.0/24
```

peut être atteinte directement.

Une destination extérieure au sous-réseau utilise la route par défaut et la passerelle comme prochain saut.

---

## Mission 4 — Tester la passerelle

Avant de tester Internet, vérifier que la passerelle est joignable :

```bash
ping -c 4 10.54.209.74
```

Résultat observé :

```text
4 paquets transmis
4 reçus
0 % de perte
```

La communication entre la machine et la passerelle locale fonctionnait correctement.

---

## Mission 5 — Tester la connectivité Internet

Tester ensuite une adresse IP publique directement :

```bash
ping -c 4 8.8.8.8
```

Le test a réussi.

L'utilisation directe d'une adresse IP permet de tester la connectivité IP vers l'extérieur sans dépendre de la résolution DNS.

---

## Mission 6 — Tester la résolution DNS

Tester ensuite un nom de domaine :

```bash
ping -c 4 google.com
```

Le nom a correctement été résolu en adresse IP.

Le serveur DNS réellement utilisé par la machine a ensuite été identifié avec :

```bash
resolvectl status
```

Configuration observée :

```text
Current DNS Server: 10.54.209.74
DNS Servers:        10.54.209.74
```

Cette étape permet de distinguer :

```text
serveur DNS
     ↓
résolution du nom
     ↓
adresse IP de destination
```

---

## Mission 7 — Examiner les sockets et ports

Afficher les sockets TCP et UDP en écoute :

```bash
ss -tuln
```

Options utilisées :

```text
-t → TCP
-u → UDP
-l → sockets en écoute
-n → adresses et ports numériques
```

Plusieurs ports ont été observés sur la machine.

Exemples :

```text
22   → SSH
80   → HTTP
3306 → MySQL
8081 → service local
```

Une attention particulière a été portée aux adresses d'écoute :

```text
127.0.0.1:PORT
→ écoute locale uniquement

0.0.0.0:PORT
→ écoute sur les interfaces IPv4

[::]:PORT
→ écoute IPv6
```

---

## Mission 8 — Identifier les processus

Afficher les processus propriétaires des sockets :

```bash
sudo ss -tulnp
```

Processus observés :

```text
Port 22   → systemd
Port 80   → apache2
Port 3306 → mysqld
Port 8081 → bettercap
```

Cette étape permet de construire la relation :

```text
port
 ↓
socket
 ↓
processus
 ↓
PID
```

---

## Mission 9 — Étudier la socket activation avec SSH

Le port TCP 22 était en écoute, mais appartenait à :

```text
systemd
PID 1
```

L'état des unités SSH a donc été vérifié :

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

La socket SSH reste en écoute sur :

```text
0.0.0.0:22
[::]:22
```

Lorsqu'une connexion SSH arrive, `ssh.socket` peut déclencher `ssh.service`.

```text
systemd
   ↓
ssh.socket
   ↓
connexion TCP :22
   ↓
trigger
   ↓
ssh.service
   ↓
sshd
```

Cette observation montre qu'un service `inactive` ne signifie pas nécessairement que le service réseau correspondant est inaccessible : une socket systemd peut être active et attendre une connexion.

---

## Résultat du diagnostic

Dans le scénario observé, la chaîne réseau fonctionnait correctement :

```text
Interface réseau          → OK
Adresse IP                → OK
Route locale              → OK
Passerelle                → OK
Connectivité locale       → OK
Connectivité Internet     → OK
Résolution DNS            → OK
Sockets réseau            → observées
Processus associés        → identifiés
```

Aucune panne réseau n'a donc été détectée pendant le laboratoire.

## Objectif du laboratoire

Construire une méthode structurée de troubleshooting réseau sous Linux et comprendre comment relier :

```text
interface
→ adresse IP
→ sous-réseau
→ route
→ passerelle
→ Internet
→ DNS
→ port
→ socket
→ processus
→ service systemd
```

L'objectif principal est de comprendre quelle question chaque commande permet de résoudre plutôt que de simplement mémoriser une liste de commandes.