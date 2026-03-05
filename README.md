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
├── data/                           # Données du projet (GeoJSON, SQLite, styles)
├── sources/                        # Code source Python
│   ├── main.py                     # Script de test/lancement
│   ├── module_affichage/           # Interface PyQt5 et gestion des vues
│   ├── module_bdd/                 # Gestion SQLite et GeoJSON
│   ├── module_cartes/              # Génération de cartes Folium
│   └── module_overpass/            # Interaction avec l'API Overpass (OSM)
├── cartes/                         # Cartes HTML générées
├── outils_git/                     # Scripts d'automatisation Git
├── looping/                        # Diagrammes et modèles conceptuels
├── docs/                           # Documentation technique
├── journal.md                      # Journal de bord du développement
├── presentation.md                 # Présentation du projet
├── requirements.txt                # Dépendances Python
├── start.sh                        # Script de lancement (Linux)
└── README.md                       # Documentation principale
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
python sources/main.py
```
Cette commande génère et ouvre la carte des forêts directement dans votre navigateur web.

### Afficher la carte avec interface de gestion
```bash
python sources/module_affichage/affichage.py
```
Cette commande affiche la carte dans une fenêtre d'application graphique avec des boutons pour ajouter et supprimer des forêts.

### Tester la gestion des clics sur la carte
```bash
python sources/module_affichage/gestion_clicks.py
```
Cette commande affiche la carte avec capture des coordonnées GPS lors des clics (affichées dans la console).

### Générer uniquement le fichier HTML
```bash
python sources/module_cartes/carte.py
```
Génère le fichier `carte.html` sans l'afficher.

## Gestion des Données

Le fichier `sources/module_bdd/interaction_donnees.py` contient les classes nécessaires pour gérer les données du projet de manière synchronisée.

### Classes principales

- **BaseDeDonnees** : Gère les opérations CRUD (Create, Read, Update, Delete) sur la base SQLite.
- **Interaction_JSON** : Gère la lecture et la modification du fichier GeoJSON (ajout/suppression de zones géographiques).
- **Interaction_Donnees** : Classe coordinatrice qui synchronise les changements entre la base SQLite et le fichier GeoJSON.

### Méthodes de la coordinatrice

- `ajouter_foret(valeurs_bdd, coords_json)` : Ajoute une forêt partout.
- `supprimer_foret(id_foret)` : Supprime une forêt partout.
- `rechercher_foret(critere)` : Recherche des forêts dans la BDD.
- `ajouter_polygone_a_foret(id_foret, coords)` : Ajoute une zone géographique.
- `retirer_polygone_a_foret(id_foret, index)` : Retire une zone géographique.

### Exemple d'utilisation
```python
from sources.module_bdd.interaction_donnees import Interaction_Donnees

inter = Interaction_Donnees("data/bdd.db", "data/forets_vendee.geojson")
# Ajout d'une forêt dans la BDD et le GeoJSON simultanément
inter.ajouter_foret([1, "Forêt de Mervent", 5000, 10000, 1, 2, 3, 4], [[[-1.5, 46.5], ...]])
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

### Fenêtre principale (`sources/module_affichage/affichage.py`)

L'interface graphique PyQt5 comprend :
- Une carte interactive Folium intégrée via QtWebEngine
- Un panneau latéral avec des boutons de gestion
- Une fenêtre modale pour ajouter/modifier des forêts avec :
  - 7 champs de saisie pour les informations de la forêt
  - Des boutons radio pour indiquer la présence de chasseurs

### Gestion des clics (`sources/module_affichage/gestion_clicks.py`)

Démonstrateur de la communication JavaScript ↔ Python :
- Utilise `QWebChannel` pour créer un pont entre le JavaScript de la carte Folium et Python
- Capture les coordonnées GPS (latitude, longitude) lors des clics sur la carte
- Affiche les coordonnées dans la console Python en temps réel

## Équipe

Projet réalisé par des élèves de NSI du lycée Léonard de Vinci de Montaigu :
- Mathéo PASQUIER (T08)(#absoluteMeyzop)
- Charlélie PINEAU (T02)#CP
- Léon RAIFAUD (T02)(🥡)
- Maden USSEREAU (T03)(#legoat) 

## Journal de Bord

Consultez le fichier [`journal.md`](journal.md) pour suivre l'évolution du projet séance par séance.

## Explication du lancement

Note : pour une isolation des imports de librairies externes, on utilisera un environnement virtuel pour la suite du guide. On peut en initialiser un avec ```python3 -m venv .venv``` sur systèmes d'explotiation Linux et Windows, avec Python 3 d'installé. Pour installer les librairies nécessaires, on fera :
Sur Linux : 
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Sur Linux (type Debian/Ubuntu, avec apt)
D'abord, il faut faire en sorte que le fichier ```start.sh``` soit exécutable, avec ```chmod```:
```bash
chmod u+x start.sh
```
Ensuite, pour lancer le projet en lui-même, on exécute ce script avec :
```bash
./start.sh --distro-type "debian"
```
Note : en lançant ```start.sh```, il est nécessaire d'avoir les droits de superutilisateur. Il nous est en effet nécessaire de garantir l'installation de certains paquets via ```apt```
### Sur Linux (type Fedora/Red Hat, avec dnf)
D'abord, il faut faire en sorte que le fichier ```start.sh``` soit exécutable, avec ```chmod```:
```bash
chmod u+x start.sh
```
Ensuite, pour lancer le projet en lui-même, on exécute ce script avec :
```bash
./start.sh --distro-type "fedora"
```
Note : en lançant ```start.sh```, il est nécessaire d'avoir les droits de superutilisateur. Il nous est en effet nécessaire de garantir l'installation de certains paquets via ```dnf```
### Sur Linux (type Arch, avec pacman)
D'abord, il faut faire en sorte que le fichier ```start.sh``` soit exécutable, avec ```chmod```:
```bash
chmod u+x start.sh
```
Ensuite, pour lancer le projet en lui-même, on exécute ce script avec :
```bash
./start.sh --distro-type "arch"
```
Note : en lançant ```start.sh```, il est nécessaire d'avoir les droits de superutilisateur. Il nous est en effet nécessaire de garantir l'installation de certains paquets via ```pacman```

## Mention Spéciale

"Mais c'est qui Mark Down ?"