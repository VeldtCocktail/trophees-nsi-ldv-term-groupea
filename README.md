# Carte des Forêts de Vendée

## Description

Application de visualisation et de gestion des forêts en Vendée. Ce projet permet d'afficher sur une carte interactive les différentes forêts du département, avec des informations détaillées sur chacune d'entre elles (superficie, biodiversité, champignons, etc.).

Développé dans le cadre du cours de NSI (Numérique et Sciences Informatiques).

## Fonctionnalités

- **Carte interactive** : Visualisation géographique des forêts de Vendée grâce à Folium
- **Interface graphique** : Affichage de la carte dans une fenêtre PyQt5 avec QtWebEngine
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
├── looping/                        # Diagrammes et modèles
├── docs/                           # Documentation
├── main.py                         # Script principal (affichage dans le navigateur)
├── carte.py                        # Génération de la carte HTML
├── affichage.py                    # Interface PyQt5 pour afficher la carte
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

### Afficher la carte dans une fenêtre PyQt5
```bash
python affichage.py
```
Cette commande affiche la carte dans une fenêtre d'application graphique.

### Générer uniquement le fichier HTML
```bash
python carte.py
```
Génère le fichier `carte.html` sans l'afficher.

## Base de Données

La classe `BaseDeDonnees` dans `interaction_bdd.py` permet d'interagir avec la base de données SQLite. Elle offre les méthodes suivantes :

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

## Équipe

Projet réalisé par des élèves de NSI :
- Maden : Interface PyQt5
- Léon : Base de données et interactions

## Journal de Bord

Consultez le fichier [`journal.md`](journal.md) pour suivre l'évolution du projet séance par séance.
