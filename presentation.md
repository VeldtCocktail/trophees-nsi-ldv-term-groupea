# 1 - Présentation globale du projet

## A - Naissance de l'idée

Dans un premier temps, nous ne savions pas vraiment ce que nous voulions faire, alors nous avons proposé plusieurs idées.
Après un premier tri, nous avions pensé réaliser une simulation de sélection naturelle.
Cependant, après réflexion, nous avions peur de ne pas réussir à aboutir à un projet original, puisque cela a déjà été fait à de nombreuses reprises, et de nombreuses vidéos YouTube proposent ce type de programme.
En poursuivant notre réflexion, nous avons donc choisi de réaliser un programme permettant d'afficher les emplacements des forêts en France ainsi que certaines informations les concernant.

## B - Problématique Initiale

Après avoir réfléchi à notre idée générale de projet, nous nous sommes interrogés sur la forme de l'interface graphique, la manière dont nous pourrions enregistrées les données.
Nous avons également réfléchi à la manière dont nous pourrions remplir notre base de données.

## C - Objectifs

Les fonctionnalités initiales que nous avions choisis pour la réalisation de notre application étaient les suivants :
- Affichage des forêts sur une carte : nous avons dès le début souhaité afficher en couleur les forêts sur une carte interactive
- Création et modification des données géométriques : nous souhaitions implémenter la possiblité pour l'utilisateur de modifier les espaces des forêts, d'en enregistrer de nouvelles ou encore de modifier leurs caractéristiques, même si nous ne savions pas encore comment nous nous y prendrions
- Affichage d'informations à propos de chaque forêt : nous voulions permettre à l'utilisateur de rechercher des forêts et d'accéder à plusieurs informations les concernant, telles que les variétés d'arbres ou les espèces qu'on peut y trouver.

# 2 - Organisation du travail

## A - Présentation de l'équipe

Notre équipe est composée de quatre personnes :

- **Maden USSEREAU**, élève en T03, spécialités Maths et NSI
- **Léon RAIFAUD**, élève en T02, spécialités Maths et NSI
- **Charlélie PINEAU**, élève en T02, spécialités Maths et NSI
- **Mathéo PASQUIER**, élève en T08, spécialités Maths et NSI

## B - Rôle de chaque membre du groupe

Nous avons initialement choisi de séparer les tâches à réaliser en plusieurs parties, en fonction des préférences de chaque membre du groupe :

- Maden : Dans un premier temps, récupérer les données correspondant aux positions géographiques des forêts et générer la carte en affichant ces données ; ensuite, gérer la partie logique et algorithmique de l'interface utilisateur
- Mathéo : Créer l'interface utilisateur du projet en implémentant l'affichage des informations concernant chaque forêt et en intégrant la carte générée à la fenêtre du programme
- Léon : Créer la base de données SQL ainsi que les classes et méthodes qui permettent l'interaction avec cette BDD et avec le fichier GeoJSON où sont enregistrés les polygones correspondant aux forêts à afficher
- Charlélie : Récupérer des bases de données d'arbres, d'animaux, de champignons ; définir l'apparence de l'interface graphique à travers le style QSS

## C - Répartition des tâches

Voici la répartition de la programmation des modules du projet :

- Module *affichage* : 

  Maden : création, modification et suppression de forêts et de polygones, lien entre l'interface graphique et le module *bdd* \
  Mathéo : affichage de tous les éléments nécessaires : carte et listes de forêts, d'informations, de détails dans les fenêtres de recherche et de modification \
  Charlélie : éléments de style de la carte

- Module *bdd* : 

  Léon : classes principales du module pour pemettre l'interaction avec la base de données SQLite et avec le fichier GeoJSON \
  Maden : correction d'erreurs liées à la recherche ou à la suppression des forêts \
  Charlélie : fonctions pour récupérer sous forme de listes les données des fichiers csv

- Module *cartes* :

  Maden : génération du fichier `carte.html`

- Module *overpass* :

  Maden : méthode qui exécute une requête overpass pour obtenir le polygone correspondant à la zone verte cliquée

- Module *reseau* : 

  Maden : création d'un serveur asynchrone depuis lequel est chargée la carte, afin de charger les tuiles OpenStreetMap de façon conforme à leurs conditions d'utilisation

- Répertoire *data* :

  Léon : création de la base de données SQLite `bdd.db` \
  Maden : création de la base de données `forets_vendee.geojson` \
  Charlélie : création des fichiers csv et du style dans le fichier `style.qss`

## D - Temps passé sur le projet

### En classe

| Période | Élève | Temps passé | Objectifs | Résultats |
|--------|------|------------|----------|----------|
| Cours du 15/12 | Tous | 1h | Réflexion sur le projet | Plusieurs idées proposées |
| Cours du 18/12 | Tous | 1h | Choix du projet | Projet de carte de forêts choisi, réflexion sur les données |
| Cours du 08/01 | Tous | 1h | Choix des outils | Utilisation de SQLite et Folium |
| Cours du 09/01 | Tous | 1h | Récupération des données | Début récupération des forêts, recherche de BDD |
| Cours du 13/01 | Tous | 1h | Organisation du projet | GitHub mis en place, schéma BDD refait |
| Cours du 15/01 | Tous | 1h | Travail sur les données | Amélioration des données et export HTML |
| Cours du 16/01 | Maden | 1h | Affichage de la carte | Carte affichée avec PyQt5 |
| Cours du 23/01 | Tous | 1h | Début interface graphique | Interface PyQt commencée |
| Cours du 27/01 | Tous | 1h | Interface graphique | Avancement de l’interface |
| Cours du 29/01 | Tous | 1h | Interface graphique | Poursuite du développement |
| Cours du 30/01 | Tous | 1h | Interface graphique | Interface enrichie |
| Cours du 03/02 | Tous | 1h | Interaction carte | Sélection des forêts via Overpass |
| Cours du 05/02 | Partiel | 1h | Interface graphique | Améliorations interface |
| Cours du 06/02 | Tous | 1h | Données arbres | Ajout BDD arbres |
| Cours du 10/02 | Tous | 1h | Interaction BDD | Ajout de polygones, données enrichies |
| Cours du 12/02 | Tous | 1h | Finalisation interactions | Requête overpass fonctionnelle |
| Cours du 03/03 | Tous | 1h | Finalisation | Interface + compatibilité Linux |
| Cours du 05/03 | Tous | 1h | Améliorations | Interface + README |
| Cours du 10/03 | Partiel | 1h | Améliorations | Interface + documentation |

### Travail personnel

| Date | Élève | Temps | Objectifs | Résultats |
|------|------|------|----------|----------|
| 14/01 | Léon | 2h | Interaction BDD | Classe SQLite fonctionnelle |
| 21/02 | Maden | 2h30 | Organisation code | Code restructuré, zoom conservé |
| 07/03 | Maden | 4h30 | Interface graphique | Fenêtre création/modification |
| 08/03 | Maden | 3h | Gestion des données | Affichage et sauvegarde BDD |
| 13/03 | Maden | 3h | Polygones | Ajout/suppression fonctionnels |
| 14/03 | Maden | 5h | Corrections | Bugs corrigés, structure améliorée |
| 15–17/03 | Maden / Léon | 6h | Documentation | Commentaires et nettoyage |
| 18/03 | Maden | 2h | Présentation | Fichier final rédigé |
| 19/03 | Charlélie | 1h | Visuel | Style.qss |

# 3 - Présentation des étapes du projet

# 4 -  Validation de l’opérationnalité du projet/de son fonctionnement

# 5 - Ouverture

## A – Idées d'amélioration du projet

Pour améliorer notre programme permettant d'afficher les emplacements des forêts, nous pourrions travailler sur plusieurs aspects différents.

Au niveau esthétique, nous pourrions améliorer le style des barres de recherche 

Nous pourrions enfin faire en sorte de pouvoir élargir ce programme pour qu'il soit accessible au monde entier et réussir à capturer toutes les forêts du monde. Mais également nous pourrions faire en sorte de connaitre de nouvelles informations si des choses arrive dans la forêt ou encore si des activités sont accessibles tels que des chemins de randonnées ou encore si des compétitions sportives se font ici etc ... 

## B – Analyse critique

## C – Compétences personnelles développées

## D – Accessibilité et inclusion
