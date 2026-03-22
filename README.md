# SilvaDaVinci

## Description

SilvaDaVinci est une application à but informatif. Notre projet permet de visualiser des forêts sur une carte
et de gérer des données à leur sujet : on peut notamment y renseigner les différents type d’arbres, les espèces animales présentes, les risques et d’autres données encore.
L’application permet également de créer des nouvelles forêts en sélectionnant leur localisation sur la carte interactive et en y ajoutant les données connues, qui pourront ensuite être modifiées par l’utilisateur.

Ce projet a été développé dans le cadre du concours des Trophées NSI.

## Fonctionnalités

- **Carte interactive** : Visualisation géographique des forêts de Vendée grâce à Folium
- **Interface graphique avancée** : Affichage de la carte dans une fenêtre PyQt5 avec QtWebEngine
- **Gestion des clics** : Capture et traitement des coordonnées GPS lors des clics sur la carte (communication 
JavaScript ↔ Python via QWebChannel)
- **Interface de gestion des forêts** : Fenêtres dédiées pour ajouter et modifier les informations sur les forêts
- **Base de données SQLite** : Stockage et gestion des informations sur les forêts
- **Données géographiques** : Utilisation de fichiers GeoJSON pour les contours des forêts
- **Informations complémentaires** : Base de données sur les champignons et les risques associés

## Structure du Projet

```
├── data/                           # Données du projet (GeoJSON, SQLite, styles)
│   ├── cartes/                     # Répertoire des cartes HTML créées et utilisées
│   │   └── carte.html              # Fichier HTML de la carte affichée
│   ├── bdd_animaux.csv             # Liste des animaux pouvant être sélectionnés
│   ├── bdd_arbres.csv              # Liste des arbres pouvant être sélectionnés
│   ├── bdd_risques.csv             # Liste des risques pouvant être sélectionnés
│   ├── bdd_toad.csv                # Liste des champignons pouvant être sélectionnés
│   ├── bdd.db                      # Base de données SQLite contenant les données à afficher
│   ├── eau.csv                     # Liste des cours d'eau pouvant être sélectionnés
│   ├── forets_vendee.geojson       # Base de données GeoJSON contenant les forêts à afficher sur la carte
│   └── style.qss                   # Fichier de style de l'interface graphique
├── docs/                           # Documentation technique
│   ├── docs_csv.md                 # Documentation des fichiers CSV
│   └── docs_bdd.md                 # Documentation de la base de données SQLite
├── sources/                        # Code source Python
│   ├── module_affichage/           # Gestion de l'interface PyQt5
│   │   ├── __init__.py             # Initialisation du module
│   │   └── affichage.py            # Fenêtre principale de l'application
│   ├── module_bdd/                 # Gestion de l'interaction avec les bases de données
│   │   ├── __init__.py             # Initialisation du module
│   │   └── interaction_donnees.py  # Classes et fonctions utiles à la communication avec les BDD
│   ├── module_cartes/              # Gestion de la création des cartes HTML
│   │   ├── __init__.py             # Initialisation du module
│   │   └── carte.py                # Génération de la carte affichée par le programme
│   ├── module_overpass/            # Gestion des requêtes Overpass
│   │   ├── __init__.py             # Initialisation du module
│   │   └── overpass.py             # Requête Overpass lors d'un clic sur la carte
│   ├── module_reseau/              # Gestion des composantes réseau du projet
│   │   ├── __init__.py             # Initialisation du module
│   │   ├── intercepteur.py         # Intercepteur et modificateur de requêtes
│   │   └── serveur.py              # Gestion du serveur local
│   ├── dependances.sh              # Installation des dépendances système pour certaines distributions Linux
│   ├── main.py                     # Script de lancement de l'application pour Windows
│   └── start.sh                    # Script de lancement de l'application pour Linux
├── tests/                          # Module de tests de l'application
│   ├── __init__.py                 # Initialisation du module
│   ├── bdd_arbres_test.csv         # Fichier CSV de test
│   ├── bdd_test.db                 # Base de données de test
│   ├── forets_test.geojson         # Données géographiques de test
│   └── tests_interaction.py        # Script de test du module d'interaction avec les bases de données
├── journal.md                      # Journal de la création du projet
├── presentation.md                 # Fichier de présentation du projet
├── README.md                       # Documentation principale
└── requirements.txt                # Dépendances Python
```

## Technologies Utilisées

- **Python 3.13.0**
- **Folium** : Création de cartes interactives
- **OpenStreetMap** : Tuiles de la carte Folium
- **Overpass** : API de requêtes OpenStreetMap
- **PyQt5** : Interface graphique
- **QtWebEngine** : Affichage de contenu web dans PyQt5
- **QWebChannel** : Communication bidirectionnelle JavaScript ↔ Python
- **SQLite3** : Base de données SQL
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

## Utilisation (Windows)

### Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

### Lancer le projet
```bash
python sources/main.py
```
Cette commande lance l'interface graphique de l'application

### Générer uniquement le fichier HTML
```bash
python sources/module_cartes/carte.py
```
Génère le fichier `carte.html` sans l'afficher.

### Lancer le script de tests de l'interaction avec les données
```bash
python -m tests.tests_interaction
```

## Utilisation (Linux)

### Sur les distributions Linux les plus populaires :
Note : pour une isolation des imports de librairies externes, on utilisera un environnement virtuel pour la suite du 
guide. On peut en initialiser un avec ```python3 -m venv .venv``` sur systèmes d'exploitation Linux avec 
Python 3 d'installé.
Afin de permettre un lancement sans accroc, il faut d'abord installer certaines dépendances système. Cela est géré avec 
```dependences.sh```. Ensuite, ```start.sh``` gère un fonctionnement normal. Il n'est nécessaire d'exécuter
```dependences.sh``` qu'une seule fois par système, mais il faut utiliser ```start.sh``` à chaque fois que l'utilisateur
veut utiliser le programme.

 Pour installer les librairies nécessaires, on fera, une fois les dépendances installées :
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Installation des dépendances sur Linux type Debian/Ubuntu, avec apt
D'abord, il faut faire en sorte que le fichier ```start.sh``` soit exécutable, avec ```chmod```, même chose avec 
```dependences.sh```:
```bash
chmod u+x dependences.sh
chmod u+x start.sh
```
Ensuite, pour lancer le projet en lui-même, on exécute ce script avec :
```bash
./dependences.sh --distro-type "debian"
./start.sh
```
Note : en lançant ```dependences.sh```, il est nécessaire d'avoir les droits de superutilisateur. Il nous est en effet 
nécessaire de garantir l'installation de certains paquets via ```apt```

### Sur Linux type Fedora/Red Hat, avec dnf
D'abord, il faut faire en sorte que le fichier ```start.sh``` soit exécutable, avec ```chmod```, même chose avec 
```dependences.sh```:
```bash
chmod u+x dependences.sh
chmod u+x start.sh
```
Ensuite, pour lancer le projet en lui-même, on exécute ce script avec :
```bash
./dependences --distro-type "fedora"
./start.sh
```
Note : en lançant ```dependences.sh```, il est nécessaire d'avoir les droits de superutilisateur. Il nous est en effet 
nécessaire de garantir l'installation de certains paquets via ```dnf```

### Sur Linux type Arch, avec pacman
D'abord, il faut faire en sorte que le fichier ```start.sh``` soit exécutable, avec ```chmod```, même chose avec 
```dependences.sh```:
```bash
chmod u+x dependences.sh
chmod u+x start.sh
```
Ensuite, pour lancer le projet en lui-même, on exécute ce script avec :
```bash
./dependences.sh --distro-type "arch"
./start.sh
```
Note : en lançant ```dependences.sh```, il est nécessaire d'avoir les droits de superutilisateur. Il nous est en effet 
nécessaire de garantir l'installation de certains paquets via ```pacman```

## Gestion des Données

Le fichier `sources/module_bdd/interaction_donnees.py` contient les classes nécessaires pour gérer les données du projet de manière synchronisée.

### Classes principales

- **BaseDeDonnees** : Gère les opérations CRUD (Create, Read, Update, Delete) sur la base SQLite.
- **Interaction_JSON** : Gère la lecture et la modification du fichier GeoJSON (ajout/suppression de zones  géographiques).
- **Interaction_Donnees** : Classe coordinatrice qui synchronise les changements entre la base SQLite et le fichier GeoJSON.

## Interface Graphique

### Fenêtre principale (`sources/module_affichage/affichage.py`)

L'interface graphique PyQt5 comprend :
- Une carte interactive Folium intégrée via QtWebEngine
- Un panneau latéral avec des boutons de gestion
- Une fenêtre modale pour ajouter/modifier des forêts

## Auteurs

Projet réalisé par des élèves de NSI du lycée Léonard de Vinci de Montaigu :
- Mathéo PASQUIER (T08)
- Charlélie PINEAU (T02)
- Léon RAIFAUD (T02)
- Maden USSEREAU (T03)

## License

Ce projet est sous licence GNU GPL v3+ - voir le fichier LICENSE pour plus d'informations.