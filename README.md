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
│   ├── bdd.db                      # Base de données SQLite principale
│   ├── bdd_vide.db                 # Template de base de données
│   ├── forets_vendee.geojson       # Contours géographiques des forêts
│   ├── bdd_animaux.csv             # Liste des animaux par forêt
│   ├── bdd_arbres.csv              # Liste des types d'arbres
│   ├── bdd_risques.csv             # Liste des risques associés
│   ├── bdd_toad.csv                # Liste des champignons
│   ├── eau.csv                     # Données sur les points d'eau
│   ├── type_eau.csv                # Types de points d'eau
│   └── style.qss                   # Feuille de style pour PyQt5
├── cartes/                         # Cartes HTML générées
│   └── carte.html                  # Carte interactive générée par Folium
├── outils_git/                     # Outils d'automatisation Git
│   ├── commit.sh                   # Script de commit automatisé (Linux/Mac)
│   ├── commit.bat                  # Script de commit automatisé (Windows)
│   ├── git-update.sh               # Script de mise à jour (Linux/Mac)
│   └── git-update.bat              # Script de mise à jour (Windows)
├── looping/                        # Diagrammes et modèles conceptuels
├── docs/                           # Documentation complémentaire
├── main.py                         # Petit script de test pour l'affichage Folium
├── carte.py                        # Backend de génération de la carte Folium
├── affichage.py                    # Interface PyQt5 principale intégrant la carte
├── gestion_clicks.py               # Module de capture des clics via QWebChannel
├── interaction_donnees.py          # Gestion unifiée SQLite + GeoJSON
├── presentation.md                 # Document de présentation du projet
├── journal.md                      # Journal de bord du développement
├── requirements.txt                # Dépendances du projet
└── README.md                       # Documentation que vous lisez actuellement
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

## Gestion des Données

Le fichier `interaction_donnees.py` contient les classes nécessaires pour gérer les données du projet de manière synchronisée.

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
from interaction_donnees import Interaction_Donnees

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

Projet réalisé par des élèves de NSI du lycée Léonard de Vinci de Montaigu :
- Mathéo PASQUIER (T08)(#absoluteMeyzop)
- Charlélie PINEAU (T02)#CP
- Léon RAIFAUD (T02)(🥡)
- Maden USSEREAU (T03)(#legoat) 

## Journal de Bord

Consultez le fichier [`journal.md`](journal.md) pour suivre l'évolution du projet séance par séance.

## Mention Spéciale

"Mais c'est qui Mark Down ?"