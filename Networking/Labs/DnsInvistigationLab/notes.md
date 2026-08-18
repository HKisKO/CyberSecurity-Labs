# DNS Investigation Lab — Notes

## 1. DNS : rôle général

Le DNS permet de traduire un nom de domaine en informations utilisables par les machines.

Exemple :

```text
google.com
    ↓ DNS
172.217.20.46
```

Une machine peut donc avoir une connectivité IP fonctionnelle tout en ayant un problème de résolution DNS.

Exemple :

```text
ping 8.8.8.8     → FONCTIONNE
ping google.com  → ÉCHEC

→ problème de résolution DNS possible
→ ne pas conclure immédiatement
```

---

## 2. DNS local sous Ubuntu

Afficher :

```bash
cat /etc/resolv.conf
```

Configuration observée :

```text
nameserver 127.0.0.53
```

`127.0.0.53` est une adresse loopback locale utilisée par le stub DNS de `systemd-resolved`.

Elle ne représente pas directement le serveur DNS du réseau.

Chaîne simplifiée :

```text
Application
     ↓
127.0.0.53:53
     ↓
systemd-resolved
     ↓
Interface réseau
     ↓
DNS configuré
```

---

## 3. Trouver le vrai DNS réseau

Commande :

```bash
resolvectl status
```

Configuration observée pendant le lab :

```text
Link 3 (wlp2s0)
Current Scopes: DNS
Current DNS Server: 192.168.1.1
DNS Domain: home
```

Donc :

```text
127.0.0.53
→ stub DNS local

192.168.1.1
→ DNS actuellement sélectionné pour l'interface Wi-Fi
```

---

## 4. 127.0.0.53 et 127.0.0.54

Commande utilisée :

```bash
sudo ss -lntup | grep ':53'
```

Observation :

```text
127.0.0.53:53 → systemd-resolved
127.0.0.54:53 → systemd-resolved
```

Les deux sont des listeners DNS locaux de `systemd-resolved`.

`127.0.0.53` est le stub DNS local utilisé par `/etc/resolv.conf`.

`127.0.0.54` est un autre listener local de `systemd-resolved`, avec un fonctionnement de proxy plus direct.

Test direct :

```bash
dig @127.0.0.54 google.com
```

---

## 5. dnsmasq et le réseau virtuel

La commande `ss` a également montré :

```text
192.168.122.1:53 → dnsmasq
```

Cette adresse correspond au réseau virtuel `virbr0`.

Elle ne correspond pas au DNS utilisé par l'interface Wi-Fi pendant le lab.

Il est donc important de ne pas considérer automatiquement tous les processus écoutant sur le port 53 comme faisant partie du chemin DNS utilisé par la connexion Internet actuelle.

---

## 6. Tester une résolution avec dig

Résolution normale :

```bash
dig google.com
```

La sortie peut contenir :

```text
status: NOERROR
SERVER: 127.0.0.53#53
```

`NOERROR` indique que la requête DNS a été traitée sans erreur DNS.

`SERVER` indique le serveur directement interrogé par `dig`.

Dans notre configuration :

```text
dig
 ↓
127.0.0.53
 ↓
systemd-resolved
```

---

## 7. Interroger directement un DNS

Syntaxe :

```bash
dig @serveur_dns domaine
```

Exemple :

```bash
dig @192.168.1.1 google.com
```

Cela permet de contourner le stub DNS local pour tester directement le DNS configuré sur le réseau.

On peut également tester un DNS alternatif :

```bash
dig @8.8.8.8 google.com
```

Cela permet d'isoler progressivement la panne.

---

## 8. Principaux types d'enregistrements DNS

### A

Adresse IPv4 :

```bash
dig google.com A
```

Exemple observé :

```text
google.com → 172.217.20.46
```

### AAAA

Adresse IPv6 :

```bash
dig google.com AAAA
```

Exemple observé :

```text
google.com → 2a00:1450:4007:80f::200e
```

### NS

Serveurs DNS autoritatifs :

```bash
dig google.com NS
```

Observation :

```text
ns1.google.com
ns2.google.com
ns3.google.com
ns4.google.com
```

### MX

Serveur de messagerie :

```bash
dig google.com MX
```

Observation :

```text
10 smtp.google.com.
```

Le `10` représente la priorité MX.

Plus la valeur est petite, plus le serveur est prioritaire.

### CNAME

Alias DNS :

```bash
dig www.github.com CNAME
```

Observation :

```text
www.github.com
      ↓ CNAME
github.com
```

`www.github.com` est l'alias.

`github.com` est la cible canonique.

---

## 9. TTL

Exemple :

```text
google.com.    176    IN    A    172.217.20.46
               ↑
              TTL
```

TTL signifie :

```text
Time To Live
```

Il représente la durée pendant laquelle une information DNS peut rester valide dans un cache.

Le TTL restant diminue avec le temps :

```text
176
 ↓
175
 ↓
174
 ↓
...
 ↓
0
```

Une fois l'information expirée, elle ne doit plus être utilisée comme réponse valide.

Une nouvelle résolution sera nécessaire si aucune autre réponse valide n'est disponible.

---

## 10. Cache de systemd-resolved

Afficher les statistiques :

```bash
resolvectl statistics
```

Exemple observé :

```text
Current Cache Size: 5
Cache Hits: 104
Cache Misses: 873
```

### Cache Hit

```text
requête
   ↓
information déjà disponible et valide
   ↓
réponse depuis le cache
```

### Cache Miss

```text
requête
   ↓
information absente / inutilisable
   ↓
DNS amont
   ↓
réponse réseau
```

Les compteurs sont globaux à `systemd-resolved`.

D'autres programmes peuvent effectuer des résolutions en même temps, donc :

```text
3 commandes ≠ forcément exactement 3 nouveaux hits
```

---

## 11. Vider le cache

Commande :

```bash
sudo resolvectl flush-caches
```

Puis :

```bash
resolvectl query google.com
```

Après avoir vidé le cache, nous avons observé :

```text
Data from: network
```

La donnée a dû être obtenue depuis le réseau.

En relançant ensuite :

```bash
resolvectl query google.com
```

on peut observer :

```text
Data from: cache
```

La réponse précédente a été réutilisée.

Expérience :

```text
flush-caches
     ↓
query google.com
     ↓
Data from: network
     ↓
réponse mise en cache
     ↓
query google.com
     ↓
Data from: cache
```

Le cache ne crée pas les informations DNS.

Il conserve temporairement des réponses obtenues auparavant.

---

## 12. Que se passe-t-il si le DNS réseau tombe ?

Si une réponse est encore disponible et valide dans le cache :

```text
Application
     ↓
127.0.0.53
     ↓
systemd-resolved
     ↓
Cache HIT
     ↓
réponse
```

La résolution peut encore fonctionner sans nouvelle requête vers le DNS amont.

Mais pour une information absente ou expirée :

```text
Application
     ↓
127.0.0.53
     ↓
systemd-resolved
     ↓
Cache MISS
     ↓
192.168.1.1
     ↓
ÉCHEC
```

La nouvelle résolution échoue si aucun DNS amont utilisable ne peut fournir la réponse.

---

## 13. Hiérarchie DNS

Commande :

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
Adresse IP
```

### Root

La racine DNS est représentée par :

```text
.
```

Elle permet d'orienter vers les serveurs responsables des TLD.

### TLD

Exemples :

```text
.com
.fr
.org
.net
```

Pour `google.com`, les serveurs `.com` indiquent quels serveurs DNS sont autoritatifs pour `google.com`.

### Serveur autoritatif

Il possède les informations DNS du domaine.

Exemple simplifié :

```text
Root "."
   ↓
« demande aux serveurs .com »

.com
   ↓
« google.com est géré par ces serveurs »

NS de google.com
   ↓
« voici son enregistrement A »

Adresse IPv4
```

---

# Méthode de diagnostic DNS

## Étape 1 — Tester la connectivité IP

```bash
ping -c 4 8.8.8.8
```

Si cela fonctionne mais :

```bash
ping -c 4 google.com
```

échoue, la résolution DNS devient suspecte.

Ne pas conclure immédiatement.

---

## Étape 2 — Vérifier la configuration DNS locale

```bash
cat /etc/resolv.conf
```

Puis :

```bash
resolvectl status
```

Identifier :

```text
stub DNS local
interface réseau
DNS actuellement sélectionné
```

---

## Étape 3 — Tester la résolution normale

```bash
dig google.com
```

Dans notre configuration :

```text
dig
 ↓
127.0.0.53
 ↓
systemd-resolved
 ↓
DNS réseau
```

---

## Étape 4 — Tester directement le DNS réseau

```bash
dig @192.168.1.1 google.com
```

### Cas 1

```text
dig google.com
→ ÉCHEC

dig @192.168.1.1 google.com
→ FONCTIONNE
```

Le DNS réseau fonctionne lorsqu'il est interrogé directement.

Zone suspecte :

```text
127.0.0.53
systemd-resolved
configuration DNS locale
```

---

## Étape 5 — Tester un DNS alternatif

Si :

```text
dig google.com
→ ÉCHEC

dig @192.168.1.1 google.com
→ ÉCHEC
```

tester :

```bash
dig @8.8.8.8 google.com
```

Si :

```text
dig @8.8.8.8 google.com
→ FONCTIONNE
```

le DNS configuré sur l'interface ou le chemin permettant de le joindre devient le principal suspect.

---

# Réflexe d'administration

Ne pas faire :

```text
« google.com ne marche pas »
        ↓
« DNS cassé »
        ↓
modifier la configuration au hasard
```

Faire :

```text
Observer
   ↓
Tester la connectivité IP
   ↓
Identifier la configuration DNS
   ↓
Tester le stub local
   ↓
Tester directement le DNS configuré
   ↓
Tester éventuellement un DNS alternatif
   ↓
Comparer les résultats
   ↓
Isoler le maillon défaillant
   ↓
Intervenir seulement ensuite
```