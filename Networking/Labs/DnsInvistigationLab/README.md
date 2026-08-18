# DNS Investigation Lab

## Présentation

Ce lab a pour objectif d'étudier le fonctionnement de la résolution DNS sous Linux et d'apprendre à diagnostiquer méthodiquement un problème de résolution de noms.

Le scénario étudié est le suivant :

```text
ping 8.8.8.8
→ FONCTIONNE

ping google.com
→ ÉCHEC
```

La connectivité IP semble fonctionner, mais l'utilisation d'un nom de domaine échoue.

L'objectif n'est pas de modifier immédiatement la configuration réseau, mais d'isoler progressivement le maillon responsable.

---

## Environnement

Système :

```text
Ubuntu Linux
```

Interface réseau utilisée pendant le lab :

```text
wlp2s0
```

Stub DNS local :

```text
127.0.0.53
```

Second listener local observé :

```text
127.0.0.54
```

Serveur DNS sélectionné sur l'interface Wi-Fi pendant le lab :

```text
192.168.1.1
```

Port DNS :

```text
53/UDP
53/TCP
```

---

## Outils utilisés

### ping

Tester la connectivité IP :

```bash
ping -c 4 8.8.8.8
```

Comparer avec un test nécessitant une résolution de nom :

```bash
ping -c 4 google.com
```

---

### /etc/resolv.conf

Afficher la configuration utilisée par les clients DNS locaux :

```bash
cat /etc/resolv.conf
```

Configuration observée :

```text
nameserver 127.0.0.53
```

`127.0.0.53` correspond au stub DNS local de `systemd-resolved`.

---

### resolvectl

Afficher la configuration DNS :

```bash
resolvectl status
```

Permet notamment d'identifier :

- l'interface utilisant DNS ;
- le serveur DNS actuellement sélectionné ;
- les différents serveurs DNS disponibles ;
- les protocoles DNS actifs ;
- les domaines associés au lien.

Effectuer une résolution :

```bash
resolvectl query google.com
```

Afficher les statistiques du cache :

```bash
resolvectl statistics
```

Vider le cache :

```bash
sudo resolvectl flush-caches
```

---

### dig

Effectuer une résolution DNS avec la configuration normale :

```bash
dig google.com
```

Sur la machine étudiée, la requête passe par :

```text
127.0.0.53:53
```

Interroger directement le DNS configuré sur l'interface :

```bash
dig @192.168.1.1 google.com
```

Tester un autre serveur DNS :

```bash
dig @8.8.8.8 google.com
```

Cette méthode permet de contourner certains maillons de la chaîne afin d'isoler une panne.

---

### ss

Identifier les processus qui écoutent sur le port DNS :

```bash
sudo ss -lntup | grep ':53'
```

Pendant le lab, les listeners suivants ont notamment été observés :

```text
127.0.0.53:53   → systemd-resolved
127.0.0.54:53   → systemd-resolved
192.168.122.1:53 → dnsmasq
```

Le service `dnsmasq` observé sur `192.168.122.1` appartient au réseau virtuel et ne correspond pas au DNS Wi-Fi utilisé pendant l'investigation.

---

## Chaîne DNS étudiée

La résolution normale peut être représentée de manière simplifiée ainsi :

```text
Application
     ↓
127.0.0.53
Stub DNS local
     ↓
systemd-resolved
     ↓
wlp2s0
     ↓
192.168.1.1
DNS réseau
     ↓
Infrastructure DNS
     ↓
Réponse
```

`127.0.0.53` et `192.168.1.1` ne jouent donc pas le même rôle.

```text
127.0.0.53
→ point d'entrée DNS local vers systemd-resolved

192.168.1.1
→ serveur DNS configuré sur l'interface réseau
```

---

## Enregistrements DNS étudiés

### A

Adresse IPv4 :

```bash
dig google.com A
```

### AAAA

Adresse IPv6 :

```bash
dig google.com AAAA
```

### NS

Serveurs DNS autoritatifs :

```bash
dig google.com NS
```

### MX

Serveur de messagerie :

```bash
dig google.com MX
```

Le nombre associé à un MX représente sa priorité.

Plus la valeur est faible, plus le serveur est prioritaire.

### CNAME

Alias DNS :

```bash
dig www.github.com CNAME
```

Exemple observé :

```text
www.github.com
      ↓ CNAME
github.com
```

---

## TTL et cache DNS

Le TTL indique pendant combien de temps une donnée DNS peut rester valide dans un cache.

Exemple :

```text
google.com.    176    IN    A    ...
               ↑
              TTL
```

Le TTL restant diminue avec le temps.

Une fois l'information expirée, une nouvelle résolution est nécessaire si aucune autre réponse valide n'est disponible.

### Observation du cache

Statistiques :

```bash
resolvectl statistics
```

Exemple observé pendant le lab :

```text
Current Cache Size: 5
Cache Hits: 104
Cache Misses: 873
```

Un `Cache Hit` signifie qu'une information utilisable était déjà disponible dans le cache.

Un `Cache Miss` signifie que la réponse demandée n'était pas disponible de manière utilisable dans le cache.

Une observation plus directe a également été effectuée avec :

```bash
resolvectl query google.com
```

Après une résolution réseau :

```text
Data from: network
```

Une requête suivante peut utiliser :

```text
Data from: cache
```

---

## Hiérarchie DNS

La commande suivante permet d'observer la progression dans la hiérarchie DNS :

```bash
dig +trace google.com
```

Chaîne observée :

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

Le serveur racine indique où trouver les serveurs du TLD `.com`.

Les serveurs `.com` indiquent quels serveurs sont autoritatifs pour `google.com`.

Les serveurs autoritatifs fournissent ensuite les informations DNS du domaine.

---

## Méthode de diagnostic

Scénario :

```text
ping 8.8.8.8
→ FONCTIONNE

ping google.com
→ ÉCHEC
```

### 1. Vérifier la configuration locale

```bash
cat /etc/resolv.conf
resolvectl status
```

### 2. Tester la résolution normale

```bash
dig google.com
```

### 3. Tester directement le DNS de l'interface

```bash
dig @192.168.1.1 google.com
```

### 4. Tester un DNS alternatif si nécessaire

```bash
dig @8.8.8.8 google.com
```

---

## Exemple d'isolation d'une panne locale

```text
dig google.com
→ ÉCHEC

dig @192.168.1.1 google.com
→ FONCTIONNE
```

Le DNS réseau répond lorsqu'il est interrogé directement.

La zone locale devient donc suspecte :

```text
127.0.0.53
systemd-resolved
configuration locale
```

---

## Exemple d'isolation d'un DNS réseau défaillant

```text
dig google.com
→ ÉCHEC

dig @192.168.1.1 google.com
→ ÉCHEC

dig @8.8.8.8 google.com
→ FONCTIONNE
```

Le serveur DNS configuré sur l'interface ou le chemin permettant de le joindre devient le principal suspect.

---

## Compétences travaillées

- comprendre le rôle du DNS ;
- distinguer connectivité IP et résolution de noms ;
- comprendre le rôle de `systemd-resolved` ;
- distinguer stub DNS local et serveur DNS réseau ;
- utiliser `resolvectl` ;
- utiliser `dig` ;
- interroger directement un serveur DNS ;
- comprendre les enregistrements A, AAAA, NS, MX et CNAME ;
- comprendre TTL, cache hit et cache miss ;
- utiliser `dig +trace` pour observer la hiérarchie DNS ;
- identifier les listeners DNS avec `ss` ;
- isoler méthodiquement l'origine d'une panne DNS.