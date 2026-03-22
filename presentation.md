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

| Période | Élèves | Temps passé | Objectifs | Résultats |
|--------|------|------------|----------|----------|
| Cours du 15/12 | Tous | 1h | Réflexion sur le projet | Plusieurs idées proposées |
| Cours du 18/12 | Tous | 1h | Choix du projet | Projet de carte de forêts choisi, réflexion sur les données |
| Cours du 08/01 | Tous | 1h | Choix des outils | Utilisation de SQLite et Folium |
| Cours du 09/01 | Tous | 1h | Récupération des données | Début récupération des forêts, recherche de BDD |
| Cours du 13/01 | Tous | 1h | Organisation du projet | GitHub mis en place, schéma BDD refait |
| Cours du 15/01 | Tous | 1h | Travail sur les données | Amélioration des données et export HTML |
| Cours du 16/01 | Tous | 1h | Affichage de la carte | Carte affichée avec PyQt5 |
| Cours du 23/01 | Tous | 1h | Début interface graphique | Interface PyQt commencée |
| Cours du 27/01 | Tous | 1h | Interface graphique | Avancement de l'interface |
| Cours du 29/01 | Tous | 1h | Interface graphique | Poursuite du développement |
| Cours du 30/01 | Tous | 1h | Interface graphique | Interface enrichie |
| Cours du 03/02 | Tous | 1h | Interaction carte | Sélection des forêts via Overpass |
| Cours du 05/02 | Partiel (car absents) | 1h | Interface graphique | Améliorations interface |
| Cours du 06/02 | Tous | 1h | Données arbres | Ajout BDD arbres |
| Cours du 10/02 | Tous | 1h | Interaction BDD | Ajout de polygones, données enrichies |
| Cours du 12/02 | Tous | 1h | Finalisation interactions | Requête overpass fonctionnelle |
| Cours du 03/03 | Tous | 1h | Finalisation | Interface + compatibilité Linux |
| Cours du 05/03 | Tous | 1h | Améliorations | Interface + README |
| Cours du 10/03 | Partiel (car absents) | 1h | Améliorations | Interface + documentation |

### Travail personnel

| Date | Élève | Temps passé | Objectifs | Résultats |
|------|------|------|----------|----------|
| 14/01 | Léon | 2h | Interaction BDD | Classe SQLite fonctionnelle |
| 21/02 | Maden | 2h30 | Organisation code | Code restructuré, zoom conservé |
| 07/03 | Maden | 4h30 | Interface graphique | Fenêtre création/modification |
| 08/03 | Maden | 3h | Gestion des données | Affichage et sauvegarde BDD |
| 13/03 | Maden | 3h | Polygones | Ajout/suppression fonctionnels |
| 14/03 | Maden | 5h | Corrections | Bugs corrigés, structure améliorée |
| 15/03 | Maden | 1h | Documentation | Commentaires |
| 16/03 | Maden | 1h | Documentation | Commentaires |
| 17/03 | Maden | 2h | Documentation | Commentaires |
| 17/03 | Léon | 3h | Documentation | Commentaires |
| 18/03 | Maden | 2h | Présentation | Rédaction d'une partie de la présentation |
| 19/03 | Charlélie | 1h | Visuel | style.qss |
| 21/03 | Maden | 9h | Commentaires | Rédaction des spécifications et des commentaires |
| 21/03 | Maden | 4h | Commentaires et rédaction | Rédaction de commentaires et poursuite de la présentation |
| 22/03 | Charlélie | 10h | Vidéo | Montage de la vidéo |

# 3 - Présentation des étapes du projet

## Conception et choix de l'implémentation

Après avoir réfléchi au programme que nous allions réaliser, listé les fonctionnalités que nous voulions y intégrer et réparti les tâches dans le groupe, nous avons commencé les recherches nécessaires pour coder ce projet.
Nous avons très vite pris conscience que notre choix initial, qui était d'afficher toutes les forêts de France, nécessiterait des bases de données très denses, et nous avons donc choisi de commencer par la Vendée en gardant la possibilité d'étendre plus tard notre projet à une zone plus large.
Nous avons initialement récupéré l'entièreté des espaces verts de Vendée en formulant une requête [Overpass](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL) sur [Overpass Turbo](https://overpass-turbo.eu/), ce qui a constitué un fichier GeoJSON de 800 000 lignes dont nous ne pouvions pas vraiment faire grand chose.
Nous avons donc ajusté notre requête pour obtenir uniquement ce qui pouvait s'apparenter à une forêt située en Vendée, et qui possédait un nom.

```cs OverpassQL
// @name forets_vendee

[out:json][timeout:60];

area["boundary"="administrative"]
     ["admin_level"="6"]
     ["ref:INSEE"="85"]
     ->.vendee;

(
  way["landuse"="forest"]["name"](area.vendee);

  relation["landuse"="forest"]["name"](area.vendee);
  
  way["natural"="wood"]["name"](area.vendee);
  
  
  relation["natural"="wood"]["name"](area.vendee);
);

out geom;
```

Après avoir obtenu un fichier de taille plus raisonnable, notre professeur nous a parlé de folium pour générer des cartes en HTML, et nous avons donc lu la documentation pour apprendre à l'utiliser.
Nous avons en parallèle fait le choix d'utiliser PyQt5 pour l'interface graphique, puisque certains membres du groupe l'avaient déjà utilisé auparavant et que nous avions trouvé pendant nos recherche une manière d'afficher des fichiers HTML grâce à un moteur web intégré à PyQt.

Au même moment, nous avons de plus créé la base de données SQLite pour accueillir les données concernant les forêts de Vendée.

## Développement des fonctionnalités de base

Nous avons progressivement implémenté certaines fonctionnalités du projet, ce qui a constitué la base fonctionnelle de notre application.
- Nous avons créé le code permettant de générer une carte sur lesquelles les polygones correspondant aux forêts de Vendée sont en couleur.
- Nous avons téléchargé et modifié, ou bien créé, quelques fichiers CSV contenant les données dont nous avions besoin pour enregistrer des détails pour chaque forêt.
- Nous avons réalisé un début d'interface graphique du projet, qui permettait seulement de visualiser la carte HTML des forêts dans un moteur web.

## Implémentation des objectifs déterminés lors de la phase de réflexion

Ensuite, nous avons avancé simultanément sur les quatre principaux aspects du projet :
- L'exécution d'une requête Overpass lors d'un clic sur la carte, qui permet de récupérer l'espace vert cliqué, ce qui est absolument nécessaire pour que l'utilisateur puisse enregistrer une forêt.
- L'interface graphique de l'application, pour permettre à l'utilisateur de consulter, d'ajouter, de modfifier et de supprimer des forêts.
- La recherche de types de détails à afficher et la construction de fichiers CSV pour contenir ces listes de détails.
- L'interaction avec les bases de données SQLite et CSV, pour permettre la création, la recherche, la modification et la suppression des forêts par l'utilisateur ainsi que l'enregistrement de détails concernant ces forêts.

## Implémentation des fonctionnalités plus complexes, interopérabilité et finalisation

Enfin, en parallèle de la finalisation de l'interface graphique et de la correction de bugs, nous avons implémenté les aspects plus complexes du projet, tels que la gestion des polygones d'une forêt, le calcul automatique de la superficie, ainsi que le déplacement de la carte sur une forêt lorsqu'on la sélectionne dans la zone de recherche.
Nous avons également rendu le projet fonctionnel sur les principales distributions Linux à travers la gestion des dépendances système et un script de lancement de l'application spécifique à ces systèmes d'exploitation.

Pour finaliser le projet, nous avons fini par corriger les bugs qui subsistaient, restructurer le code, charger la carte depuis un serveur local pour respecter les conditions d'utilisation des tuiles OpenStreetMap et rédiger tous les commentaires et toutes les spécifications des fonctions du programme.


# 4 -  Validation de l'opérationnalité du projet et de son fonctionnement

## A - Vérification des bugs et bon fonctionnement de l'application

Afin d'éviter les bugs, nous avons mis en place plusieurs tests et vérifications. 
Pour permettre une meilleure organisation des tests, nous avons décidé de vérifier le bon fonctionnement de chaque module séparément, puis de vérifier le bon fonctionnement de l'application dans son ensemble.
Cela se manifeste par des fichiers (absents aujourd'hui) qui ont permis de tester plusieurs fonctionnalités cruciales du programme. 
Par exemple, dans le cas du module s'occupant de la base de données (voir le dossier ```module_bdd```), un fichier précédemment nommé ```tests.py``` nous a permis d'essayer et tester de nouvelles fonctions/ méthodes associées à la base de données. 
Aussi, cela nous a permis d'utiliser des extraits de données pour tester le bon fonctionnement de l'application, sans avoir à les charger dans leur entièreté.

## B - Difficultés rencontrées et solutions algorithmiques

Tout au long du développement de notre projet, plusieurs difficultés se sont placées sur notre chemin. Cela nous a obligé à réfléchir à des solutions pertinentes, efficaces et pouvant être incluses dans notre programme de façon cohérente et facilement compréhensible.

Un des défis associés à lister et afficher les forêts est de réussir à récupérer les polygones correspondant aux forêts. En effet, un de nos objectifs était non seulement de lister et afficher les forêts que nous pouvons trouver via Overpass (et par extension OpenStreetMap), mais également de permettre à l'utilisateur d'en créer de nouvelles, d'en supprimer, et de les modifier en termes de détails (arbres, animaux, etc.).
Malgré l'existence de bibliothèques comme Shapely et JSON nous permettant d'interagir avec ces polygones, il a fallu faire correspondre les données liées aux polygones seulement de [forets_vendee.geojson](data/forets_vendee.geojson) avec les données de la base de données SQLite [bdd.db](data/bdd.db), comme par exemple les noms des forêts, leur superficie, etc. Nous sommes donc parvenus à enregistrer les identifiants des _features_ GeoJSON dans notre base de données SQLite grâce à la méthode [`synchro_depuis_json`](sources/module_bdd/interaction_donnees.py#L793) de la classe `InteractionDonnees`.

Nous avons également dû réfléchir au cas de la modification des détails d'une forêt dans la base de données.
En effet, lors de la modification de ces détails, il fallait enregistrer dans la base de données les associations `FORET - ARBRES`, `FORET - ANIMAUX`, etc.
Cela implique de réfléchir à ce qui devait se passer si ces détails étaient enregistrés dans une forêt, puis que l'utilisateur choisissait de les retirer lors de la modification de la forêt.
Pour simplifier le programme et éviter les doublons, nous avons choisi de supprimer toutes les lignes concernant cette forêt des tables d'associations avant d'enregistrer uniquement les détails sélectionnés par l'utilisateur à l'issue de la modification de la forêt, quitte à enregistrer à nouveau ce qui l'était déjà et qui n'a pas été modifié.

```python
# extrait de GroupeForet.enregistrer_foret_bdd()

# pour chaque type de détail
for type_detail in LISTE_DETAILS.keys():
    # on supprime les détails de ce type pour la forêt qu'on modifie
    self.fen.inter.bdd.supprimer_ligne(
        DICO_TABLES_DETAILS[type_detail],
        ("id_foret", foret["id"])
    )

    # on enregistre ensuite les identifiants des détails de ce type
    if type_detail in self.details_temp:
        for valeur in self.details_temp[type_detail]:
            chemin_csv = os.sep.join(
                ["data", DICO_CSV_DETAILS[type_detail]]
            )
            resultat = indo.rechercher_dans_csv(
                chemin_csv, 1, valeur
            )
            if self.fen.debug: print(
                f"Recherche de {valeur} dans {chemin_csv} : {resultat}"
            )

            if resultat:
                id_val = resultat[0][0]
                self.fen.inter.bdd.ajouter_ligne(
                    DICO_TABLES_DETAILS[type_detail],
                    [foret["id"], id_val]
                )
```

Il est évident que cette approche devient peu efficace lorsqu'on manipule des grandes quantités de données, parce que cela remplace toutes les lignes des tables d'association, même celles qui n'ont pas été modifiées. 
Néanmoins, dans le cas de notre application de gestion de forêts, l'utilisation de ces associations ne nécessite pas cette optimisation.
En effet, étant donné le nombre relativement faible de détails pouvant être enregistrés, même si l'utilisateur associe plusieurs dizaines de détails à la forêt, la suppression de toutes les lignes et l'enregistrement des nouveaux détails reste extrêmement rapide, bien trop pour que cela change quelque chose à son expérience.

# 5 - Ouverture

## A – Analyse critique

Nous estimons que le programme que nous avons réalisé est relativement facilement accessible, que ce soit dans les recherche de forêts (permettant à l'utilisateur d'avoir la localisation de la forêt et des informations dessus) mais également dans la création ou la modification d'une forêt (en lui permettant de modifier les informations lorsque celles-ci sont fausses ou encore de rajouter une forêt si celle-ci viens d'etre créée) grâce aux boutons, aux fenêtres ou encore aux barres de recherches, que nous avons tenté de rendre assez visibles et intuitifs.

Le nombre de fonctionnalités est toutefois relativement limité, ce qui est dû principalement à un manque d'idées et de temps pour en réaliser certaines.

## B – Idées d'amélioration du projet

Pour améliorer notre programme permettant d'afficher les emplacements des forêts, nous pourrions travailler sur plusieurs aspects différents.

Au niveau esthétique, nous pourrions améliorer le style des barres de recherche, et nous pourrions également faire en sorte de mettre des icones ou des images sur les différentes fenêtres de sélection pour permettre à un utilisateur de se repérer plus facilement.

Au niveau fonctionnel, nous pourrions prendre une carte ayant plus de précisions pour permettre à l'utilisateur de visualiser plus précisément où se trouve la forêt. Nous pourrions aussi faire en sorte que l'utilisateur puisse mettre une note et un commentaire pour chaque forêt, que l'on enregistrerait comme information sur la forêt. Nous pourrions également implémenter un système de comptes et d'administration, pour que les modifications soient vérifiées par un modérateur avant d'être appliquées.

Nous pourrions enfin augmenter l'efficacité de la recherche et de la modification de forêts en enregistrant les informations par zone géographique (département ou région) afin de pouvoir élargir à la France entière tout en restant rapide et efficace. Nous pourrions également ajouter des informations sur les activités accessibles telles que des chemins de randonnée ou la pratique d'autres sports. 

## C – Compétences développées

Grâce à ce projet assez conséquent pour cette année de Terminale, nous avons pu développer certaines compétences techniques et des façons de travailler nouvelles. Il a fallu que nous apprenions à gérer notre temps : chaque séance devait être productive afin de ne pas ralentir le groupe et l'avancée du projet, tout en aidant les autres face aux différentes difficultés que nous pouvions rencontrer. Nous avons également amélioré la maîtrise du codage, notamment l'utilisation de PyQt pour l'interface, ainsi que la manière de penser pour écrire un code suffisamment lisible et compréhensible.

## D – Accessibilité et inclusion

Application intuitive, sans trop de texte dans tous les sens, couleurs vives et distinctes.
