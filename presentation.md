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

# 3 - Présentation des étapes du projet

Dans un premier temps, pendant nos séances du 15 et 18 décembre 2025, nous ne savions pas vraiment ce que nous voulions
faire, alors nous avons mis plusieurs idées de côté. Après un premier tri, nous avons décidé de faire une simulation de
sélection naturelle. C'est seulement après réflexion que nous avons pensé que cela aurait été trop compliqué de réussir
à concrétiser cette idée et que, de plus, beaucoup de personnes risquaient d'avoir cette idée également. Alors, nous
avons regardé de nouveau à travers la longue liste que nous avions faite et nous avons décidé de garder comme idée de
projet un site de localisation de forêts 🌲🌳.

Dans un second temps, durant la séance du 18 décembre 2025, nous avons commencé à faire des recherches sur les
différentes informations que l'on pourrait retrouver sur ces forêts. Nous avons donc créé une boucle de réflexion nous
permettant de savoir quelles informations seraient utiles ou non. Après réflexion, nous avons décidé de garder des
informations à propos des animaux qu'il est possible d'observer là-bas, de savoir si un cours d'eau passe où se trouve
dans la forêt, s'il est possible de récupérer des champignons dans cette forêt et quels sont les risques que l'on peut
retrouver sur place.

Lors de notre séance du 8 janvier 2026, il nous fallait trouver un endroit où nous pourrions stocker les données. Nous
avons alors choisi d'utiliser SQLite. Il fallait également faire en sorte de pouvoir générer une carte : nous avons donc
choisi de générer celle d'OpenStreetMap en utilisant Folium.

Le 9 janvier 2026, nous devions récupérer les forêts se trouvant sur la carte avec leur localisation. Durant cette
séance, nous avons également commencé à faire des recherches sur les bases de données que nous devions trouver,
notamment celles concernant les champignons trouvables en forêt.

Lors de notre 6e séance, le 13 janvier 2026, nous avons alors créé un dépôt de code sur [`GitHub`](https://github.com)
permettant de nous envoyer tous les documents sur lequels chacun avait travaillé. Nous avons également dû refaire une
représentation graphique de base de données sur Looping, car le premier fichier Looping que nous avions créé était
incorrectement organisé, donc nous avons refait un fichier nous permettant d'avoir un schéma plus organisé et plus clair
à comprendre pour nous. Nous avons aussi commencé à travailler sur l'architecture de donnée.
\*avec un excellent accent british\* Mais c'est qui Mark Down ?

Dans un autre temps qui est révolue depuis beaucoup trop longtemps, dans les alentours du 15 janvier 2026, nous avons
continué à chercher les bases de données que nous voulions. Nous avons également continué à travailler sur la
recherche des localisations de nos forêts. Nous avons aussi cherché à enregistrer la carte avec folium en html.

Lors de notre 8e séance, le 16 janvier 2026, nous avons dû nous occuper de l'affichage de la carte avec PyQt5.

De notre séance 9 à notre séance ... (à définir quand l'interface graphique sera fini), du 23 janvier 2026 au ... (à
définir quand l'interface graphique sera fini). Cela nous a pris pas mal de temps, car nous avions de nombreuses idées.
Déjà dans un premier temps, nous voulions creer une barre de recherche pour pouvoir accéder à toutes les forêts
disponibles. Nous avons dans un premier temps, fais en sorte que lorsqu'on tape le nom d'une forêt dans la barre de
recherche, on puisse trouver le nom de la forêt dans la liste que nous avions. Par la suite, il nous fallait également
faire en sorte de creer des fenêtres pour pouvoir faire en sorte de creer ou supprimer une forêt (dans le cas où
l'on n'aurait pas réussi à avoir toutes les forêts et si on n'y arrive pas dans le temps imparti). Dans la fenêtre de
création de forêt, nous avons alors fait en sorte d'utiliser nos bases de données que nous avions créée
ou trouvée via des sources externes pour permettre de rajouter des infos sur les forêts. Dans un premier temps, nous
avions fait en sorte d'avoir une "bande défillante" avec tous les types d'arbres trouvable en forêts et d'en
selectionner. Par la suite, nous voulions savoir si cette forêt avait un cours d'eau. Alors, nous avons mis une
"checkbox" et, si oui, est-ce que son nom se trouve dans notre base de données.
Si la forêt avait des animaux, l'utilisateur doit pouvoir en ajouter à l'aide d'une autre "bande défillante" pour
pouvoir choisir des animaux trouvable dans cette forêt, de même pour les champignons qui sont assez nombreux.
Egalement il nous fallait egalement prevenir l'utilisateur si la forêtys est exposé à de nombreux risuqe ou non.
Alors, nous avons fait comme pour les animaux et les champignons pour le moment.

# 4 -  Validation de l’opérationnalité du projet/de son fonctionnement

# 5 - Ouverture