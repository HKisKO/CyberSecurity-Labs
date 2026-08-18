# DNS Investigation Lab — Scénario

## Contexte

Un utilisateur signale qu'il n'arrive plus à accéder aux services en utilisant leurs noms de domaine.

La machine semble pourtant toujours avoir accès au réseau.

## Symptôme initial

Premier test de connectivité :

```bash
ping -c 4 8.8.8.8
```

Résultat :

```text
FONCTIONNE
```

Test avec un nom de domaine :

```bash
ping -c 4 google.com
```

Résultat :

```text
ÉCHEC
```

La connectivité IP semble donc fonctionner, mais la résolution de noms semble poser problème.

À ce stade, aucune conclusion définitive n'est faite sur l'origine de la panne.

## Mission

L'objectif est d'identifier à quel niveau de la chaîne DNS se situe le problème.

Chaîne étudiée :

```text
Application
    ↓
127.0.0.53
DNS stub local
    ↓
systemd-resolved
    ↓
Interface réseau
    ↓
Serveur DNS configuré
    ↓
Infrastructure DNS
```

L'investigation doit permettre de distinguer notamment :

- un problème de résolution locale ;
- un problème lié à `systemd-resolved` ;
- un problème avec le serveur DNS configuré sur l'interface ;
- un problème DNS extérieur ;
- une réponse provenant du cache ou du réseau.

## Environnement observé pendant le lab

Interface utilisée :

```text
wlp2s0
```

Stub DNS local :

```text
127.0.0.53
```

Serveur DNS actuellement sélectionné sur l'interface Wi-Fi :

```text
192.168.1.1
```

Un second listener de `systemd-resolved` a également été observé sur :

```text
127.0.0.54:53
```

## Principe d'investigation

Ne pas modifier immédiatement la configuration DNS.

Chaque maillon doit être testé séparément afin d'isoler la panne avant d'intervenir.

Exemple :

```text
Résolution normale
        ↓
ÉCHEC
        ↓
Test direct du DNS de l'interface
        ↓
ÉCHEC
        ↓
Test avec un DNS alternatif
        ↓
FONCTIONNE
        ↓
DNS configuré sur l'interface = principal suspect
```

## Objectif final

Être capable de déterminer si une panne de résolution provient :

```text
du client
    ↓
du stub DNS local
    ↓
de systemd-resolved
    ↓
du DNS configuré sur l'interface
    ↓
ou de l'infrastructure DNS extérieure
```

Le diagnostic doit être effectué avant toute modification de la configuration réseau.