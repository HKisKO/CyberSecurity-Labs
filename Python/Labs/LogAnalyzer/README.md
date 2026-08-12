# LogAnalyzer

Petit analyseur de logs SSH développé en Python.

## Fonctionnalités

- Affichage du fichier de logs
- Comptage des connexions réussies
- Comptage des connexions échouées
- Extraction des IP associées aux échecs
- Comptage des échecs par adresse IP
- Détection simple d'IP suspectes
- Gestion des erreurs de fichier
- Menu interactif

## Exemple de détection

Une adresse IP est considérée comme suspecte dans ce laboratoire si elle possède au moins 3 tentatives échouées.

Exemple :

```text
===== ECHECS PAR IP =====
10.0.0.25 : 3 échec(s)
172.16.1.44 : 1 échec(s)

===== IP SUSPECTES =====
10.0.0.25 : 3 tentatives échouées
```

## Concepts Python utilisés

- Fonctions
- Boucles `for` et `while`
- Conditions `if / elif / else`
- Dictionnaires
- `with open()`
- `split()`
- `try / except`
- `FileNotFoundError`
- `.items()`
- Manipulation de chaînes

## Fichiers

- `log_analyzer.py` : programme principal
- `auth.log` : fichier de logs utilisé pour les tests
- `scenario.md` : scénario du laboratoire