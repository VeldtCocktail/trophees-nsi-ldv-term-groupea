# 1 - Présentation du projet

## 1 - Naissance de l'idée

Dans un premier temps, nous ne savions pas vraiment ce que nous voulions faire, alors nous avons mis plusieurs idées de
côté. Après un premier tri, nous avons décidé de faire une simulation de sélection naturelle. C'est seulement après
réflexion que nous avons pensé que cela aurait été trop compliqué de réussir à concrétiser cette idée et que, de plus,
beaucoup de personnes risquaient d'avoir la même idée également. Alors, nous avons regardé de nouveau à travers la
longue liste que nous avions faite et nous avons décidé de garder comme idée de projet un site de localisation de forêts
🌲🌳.

## 2 - Problématique Initiale

Après avoir réfléchi à notre idée générale de projet, il a fallu répondre à plusieurs problématiques. Par exemple, il
nous fallait trouver via quel procédé l'on devrait générer une carte sous format HTML. Aussi, nous avons dû déterminer
sous quelle forme stocker les informations telles
Comment allons-nous générer une carte ? Comment allons-nous stocker les informations ? Comment faire en sorte de trouver
toutes les informations par rapport aux forêts ? Comment se répartir le travail convenablement ? Comment faire si l'on
veut ajouter une fôrets ? Que doit-on faire si on recherche une forêt ? Et que doit-on trouver comme information sur
cette forêt ?

## 3 - Objectifs

# 2 - Organisation du travail

## 1 - Présentation de l'équipe
Notre équipe est composée de quatre personnes :

- ***USSEREAU Maden***, alias **LambdaLight**, élève en Terminale 3, Lycée Léonard de Vinci, Montaigu-Vendée, Vendée,
  Pays de la Loire, France, Europe, la Planète Terre, Le Système Solaire, La Voie lactée, l'Univers, ayant comme
  spécialité Mathématique et NSI
- ***RAIFAUD Léon***, alias **Onions**, élève en Terminale 2, Lycée Léonard de Vinci, Montaigu-Vendée, Vendée, Pays de
  la Loire, Europe, France, la Planète Terre, Le Système Solaire, La Voie lactée, l'Univers, ayant comme spécialité
  Mathématique et NSI
- ***PASQUIER Mathéo***, alias **Meyzop**, élève en Terminale 8, Lycée Léonard de Vinci, Montaigu-Vendée, Vendée,
  Pays de la Loire, France, Europe, la Planète Terre, Le Système Solaire, La Voie lactée, l'Univers, ayant comme
  spécialité Mathématique et NSI
- ***PINEAU Charlélie***, alias **.**, élève en Terminale 2, Lycée Léonard de Vinci, Montaigu-Vendée, Vendée, Pays de la
  Loire, France, Europe, la Planète Terre, Le Système Solaire, La Voie lactée, l'Univers, ayant comme spécialité
  Mathématique et NSI

## 2 - Organisation du travail

***USSEREAU Maden***, qui s'est occupé de la carte, son affichage, la séléction des forêts.
***RAIFAUD Léon***, Qui s'est occupé de la gestion des données nécessaires, via une base de données SQL, ainsi qu'un
fichier GeoJSON.
***PASQUIER Mathéo***, qui s'est principalement occupé de l'interface graphique.
***PINEAU Charlélie***, qui s'est occupé des bases de données, ainsi que l'interface graphique.


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