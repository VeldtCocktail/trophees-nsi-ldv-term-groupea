# Carte des Forêts de Vendée

## Description

Application de visualisation et de gestion des forêts en Vendée. Ce projet permet d'afficher sur une carte interactive les différentes forêts du département, avec des informations détaillées sur chacune d'entre elles (superficie, biodiversité, champignons, etc.).

Développé dans le cadre du cours de NSI (Numérique et Sciences Informatiques).

## Fonctionnalités

- **Carte interactive** : Visualisation géographique des forêts de Vendée grâce à Folium
- **Interface graphique avancée** : Affichage de la carte dans une fenêtre PyQt5 avec QtWebEngine
- **Gestion des clics** : Capture et traitement des coordonnées GPS lors des clics sur la carte (communication JavaScript ↔ Python via QWebChannel)
- **Interface de gestion des forêts** : Fenêtres dédiées pour ajouter et modifier les informations sur les forêts
- **Base de données SQLite** : Stockage et gestion des informations sur les forêts
- **Données géographiques** : Utilisation de fichiers GeoJSON pour les contours des forêts
- **Informations complémentaires** : Base de données sur les champignons et les risques associés

## Structure du Projet

```
racine/
├── data/                           # Données du projet
│   ├── forets_vendee.geojson      # Contours géographiques des forêts
│   ├── bdd.db                      # Base de données SQLite principale
│   ├── bdd_vide.db                 # Template de base de données
│   ├── base-de-donnees-champignons.csv
│   ├── base_de_donnees_des_risques.csv
│   └── eau.csv
├── cartes/                         # Cartes HTML générées
│   └── carte.html
├── outils_git/                     # Outils d'automatisation Git
│   ├── commit.sh                   # Script de commit automatisé (Linux/Mac)
│   ├── commit.bat                  # Script de commit automatisé (Windows)
│   ├── git-update.sh               # Script de mise à jour (Linux/Mac)
│   └── git-update.bat              # Script de mise à jour (Windows)
├── looping/                        # Diagrammes et modèles
├── docs/                           # Documentation
├── main.py                         # Script principal (fait absolument rien, merci Maden)
├── carte.py                        # Génération de la carte HTML
├── affichage.py                    # Interface PyQt5 avec gestion des forêts
├── gestion_clicks.py               # Gestion des clics sur la carte (QWebChannel)
├── interaction_bdd.py              # Classe pour interagir avec la base de données
├── journal.md                      # Journal de bord du projet
├── requirements.txt                # Dépendances Python
└── README.md                       # Ce fichier
```

## Technologies Utilisées

- **Python 3.x**
- **Folium** : Création de cartes interactives
- **PyQt5** : Interface graphique
- **QtWebEngine** : Affichage de contenu web dans PyQt5
- **QWebChannel** : Communication bidirectionnelle JavaScript ↔ Python
- **SQLite3** : Base de données
- **GeoJSON** : Format de données géographiques

## Installation

1. **Cloner le projet** (ou le télécharger)

2. **Créer un environnement virtuel** (recommandé) :
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Sur Linux/Mac
   # ou
   .venv\Scripts\activate     # Sur Windows
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

### Afficher la carte dans le navigateur
```bash
python main.py
```
Cette commande génère et ouvre la carte des forêts directement dans votre navigateur web.

### Afficher la carte avec interface de gestion
```bash
python affichage.py
```
Cette commande affiche la carte dans une fenêtre d'application graphique avec des boutons pour ajouter et supprimer des forêts.

### Tester la gestion des clics sur la carte
```bash
python gestion_clicks.py
```
Cette commande affiche la carte avec capture des coordonnées GPS lors des clics (affichées dans la console).

### Générer uniquement le fichier HTML
```bash
python carte.py
```
Génère le fichier `carte.html` sans l'afficher.

## Base de Données

La classe `BaseDeDonnees` dans `interaction_bdd.py` permet d'interagir avec la base de données SQLite. Elle a été refactorisée pour offrir une interaction généralisée et robuste avec n'importe quelle base de données compatible SQLite.

### Méthodes disponibles

- `ajouter_ligne(table, valeurs)` : Ajouter une entrée
- `supprimer_ligne(table, identification)` : Supprimer une entrée
- `modifier_ligne(table, modif)` : Modifier une entrée
- `rechercher_ligne(table, identification)` : Rechercher des lignes
- `rechercher_valeur(table, identification, colonne_recherchee)` : Rechercher des valeurs spécifiques

### Exemple d'utilisation
```python
from interaction_bdd import BaseDeDonnees

bdd = BaseDeDonnees("data/bdd.db")
bdd.ajouter_ligne("FORET", (1, "Forêt de Mervent", 5000, 10000, 1, 2, 3, 4))
```

## Outils Git (Automatisation)

Le dossier `outils_git/` contient des scripts pour automatiser les opérations Git courantes.

### Scripts de commit automatisé

**Linux/Mac** :
```bash
./outils_git/commit.sh -f nom_du_fichier "message de commit"
./outils_git/commit.sh -d nom_du_dossier "message de commit"
```

**Windows** :
```cmd
outils_git\commit.bat -f nom_du_fichier "message de commit"
outils_git\commit.bat -d nom_du_dossier "message de commit"
```

Ces scripts ajoutent automatiquement le fichier ou dossier spécifié, créent un commit avec le message fourni, et poussent les changements vers la branche `main`.

### Scripts de mise à jour

**Linux/Mac** :
```bash
./outils_git/git-update.sh
```

**Windows** :
```cmd
outils_git\git-update.bat
```

Ces scripts récupèrent les dernières modifications depuis le dépôt distant.

## Interface Graphique

### Fenêtre principale (`affichage.py`)

L'interface graphique PyQt5 comprend :
- Une carte interactive Folium intégrée via QtWebEngine
- Un panneau latéral avec des boutons de gestion
- Une fenêtre modale pour ajouter/modifier des forêts avec :
  - 7 champs de saisie pour les informations de la forêt
  - Des boutons radio pour indiquer la présence de chasseurs

### Gestion des clics (`gestion_clicks.py`)

Démonstrateur de la communication JavaScript ↔ Python :
- Utilise `QWebChannel` pour créer un pont entre le JavaScript de la carte Folium et Python
- Capture les coordonnées GPS (latitude, longitude) lors des clics sur la carte
- Affiche les coordonnées dans la console Python en temps réel

## Équipe

Projet réalisé par des élèves de NSI :
- Mathéo PASQUIER (T08)(#absoluteMeyzop)
- Charlélie PINEAU (T02)
- Léon RAIFAUD (T02)(🥡)
- Maden USSEREAU (T03)(#legoat) 

## Journal de Bord

Consultez le fichier [`journal.md`](journal.md) pour suivre l'évolution du projet séance par séance.
