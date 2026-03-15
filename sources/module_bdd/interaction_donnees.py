import sqlite3
import json
import csv
import os
import math
from shapely.geometry import shape

class BaseDeDonnees:
    """
    Classe permettant l'interaction avec le fichier de base de données
    """
    def __init__(self, nom_fichier):
        """
        Entrées \\: \n
            nom_fichier: chemin vers le fichier de base de données
        Rôle \\: \n
            initialise l'interaction avec le fichier de base de données
        Sortie \\: \n
            self.connexion contient la connexion avec la base de données
            self.curseur contient le curseur pour exécuter des commandes
        """
        # Connexion avec la base de données, a l'aide de sqlite3
        self.connexion = sqlite3.connect(nom_fichier)
        # Création du curseur, pour pouvoir exécuter des commandes
        self.curseur = self.connexion.cursor()

    def fermer(self):
        """
        Rôle \\: ferme la connexion avec la base de données
        """
        self.connexion.close()

    def ajouter_ligne(self, table, valeurs):
        """
        Entrées \\: \n
            table: str, nom de la table
            valeurs: list, liste des valeurs à insérer dans la table
        Rôle \\: \n
            ajoute une ligne dans la table spécifiée avec les valeurs
            données dans valeurs
        Sortie \\: modifie la base de données
        """
        # Variable temporaire pour le stockage des valeurs à ajouter
        temp = ", ".join(["?" for element in valeurs])
        # Variable contenant la requete SQL
        requete = f"INSERT INTO {table} VALUES ({temp})"
        # On "imprime" cette requete
        self.curseur.execute(requete, valeurs)
        # Et on l'exécute
        self.connexion.commit()

    def supprimer_ligne(self, table, identification):
        """
        Entrées \\: \n
            table: str, nom de la table
            identification: tuple(colonne: str, valeur: any), critère de
                    suppression, ex : ("id_foret", 1)
        Rôle \\: \n
            supprime une ligne dans la table spécifiée correspondant au
            critère
        Sortie \\: base de données indiquée par self modifiée
        """
        # Variables pour identifier la/les lignes à supprimer
        # Il faut que l'attribut dans la colonne colonne
        colonne = identification[0]
        # Soit égal à valeur
        valeur = identification[1]
        # Variable contenant la requete SQL
        requete = f"DELETE FROM {table} WHERE {colonne} = ?"
        # On "imprime" cette requete
        self.curseur.execute(requete, (valeur,))
        # Et on l'exécute
        self.connexion.commit()

    def modifier_ligne(self, table, modif):
        """
        Entrées \\: \n
            table: str, nom de la table
            modif: tuple, contient (
                    identification: tuple(colonne: str, valeur: any),
                    colonne: str,
                    valeur: any)
        Rôle \\: modifie une valeur dans la table spécifiée
        Sortie \\: base de données modifiée
        """
        # Dans quelle colonne on doit modifier la variable
        colonne_modif = modif[1]
        # Et la nouvelle valeur de ce dernier
        nouvelle_valeur = modif[2]

        # Variable pour l'identification de la/des colonnes à modifier
        identification = modif[0]
        # D'abord, dans quelle colonne on vérifie
        colonne_id = identification[0]
        # Et à quelle valeur ce doit être égal
        valeur_id = identification[1]

        # Variable contenant la requete SQL
        requete = f'''
            UPDATE {table}
            SET {colonne_modif} = ?
            WHERE {colonne_id} = ?
        '''
        # On "imprime" cette requete
        self.curseur.execute(requete, (nouvelle_valeur, valeur_id))
        # Et on l'exécute
        self.connexion.commit()

    def rechercher_ligne(self, table, identification):
        """
        Entrées \\: \n
            table: str, nom de la table
            identification: tuple(colonne: str, valeur: any), critère de
                    recherche, ex : ("id_foret", 1)
        Rôle \\: \n
            recherche une ligne dans la table spécifiée correspondant au
            critère
        Sortie \\: liste des lignes trouvées
        """
        # D'abord, dans quelle colonne on vérifie
        colonne = identification[0]
        # Et à quelle valeur ce doit être égal
        valeur = identification[1]
        # Variable contenant la requete SQL
        requete = f'''
            SELECT * FROM {table}
            WHERE {colonne} = ?
        '''
        # On "imprime" cette requete
        self.curseur.execute(requete, (valeur,))
        # Et on l'exécute
        return self.curseur.fetchall()

    def rechercher_valeur(self, table, identification, colonne_recherchee):
        """
        Entrées \\: \n
            table: str, nom de la table
            identification: tuple(colonne: str, valeur: any), critère de
                    recherche, ex : ("id_foret", 1)
            colonne_recherchee: str, nom de la colonne dont on veut
                    récupérer la valeur
        Rôle \\: \n
            recherche une valeur dans la table spécifiée correspondant au
            critère
        Sortie \\: liste des valeurs trouvées
        """
        # D'abord, dans quelle colonne on vérifie
        colonne = identification[0]
        # Et à quelle valeur ce doit être égal
        valeur = identification[1]
        # Variable contenant la requete SQL
        requete = f'''
            SELECT {colonne_recherchee} FROM {table}
            WHERE {colonne} = ?
        '''
        # On "imprime" cette requete
        self.curseur.execute(requete, (valeur,))
        # Et on l'exécute
        return self.curseur.fetchall()

    def recuperer_tout(self, table):
        """
        Entrées \\: \n
            table: str, nom de la table
        Rôle \\: récupérer toutes les lignes d'une table
        Sortie \\: liste de toutes les lignes de la table
        """
        requete = f"SELECT * FROM {table}"
        self.curseur.execute(requete)
        return self.curseur.fetchall()

    def vider_table(self, table):
        """
        Entrées \\: \n
            table: str, nom de la table
        Rôle \\: Supprimer toutes les lignes d'une table
        """
        requete = f"DELETE FROM {table}"
        self.curseur.execute(requete)
        self.connexion.commit()


class InteractionJSON:
    """
    Classe d'interaction avec le fichier JSON
    """
    def __init__(self, json_path):
        """
        Entrées \\: \n
            json_path: chemin vers le fichier JSON
        Rôle \\: initialise l'interaction avec le fichier JSON
        Sortie \\: self.data contient les données du fichier JSON
        """
        self.json_path = json_path
        with open(json_path, 'r', encoding='utf-8') as file_json:
            self.data = json.load(file_json)

    def rechercher_feature(self, id_feature):
        """
        Entrées \\: \n
            id_feature: identifiant de la feature à rechercher
        Rôle \\: Recherche une feature dans le GeoJSON par son ID
        Sortie \\: La feature si trouvée, None sinon
        """
        features = self.data.get('features', [])
        nb_features = len(features)
        trouve = False
        idx = 0
        feature_trouvee = None

        while idx < nb_features and not trouve:
            feature = features[idx]

            # nettoyage des MultiPolygon corrompus
            if feature:
                geom = feature.get('geometry')
                
                if geom and geom['type'] == 'MultiPolygon':
                    coords_propres = [
                        coords for coords in geom['coordinates'] if coords
                    ]

                    if len(coords_propres) != len(geom['coordinates']):
                        geom['coordinates'] = coords_propres
                        self.sauvegarder()
            
            props = feature.get('properties', {})
            if props.get('id') == id_feature or props.get('@id') == id_feature:
                trouve = True
                feature_trouvee = feature
            idx += 1

        return feature_trouvee

    def ajouter_foret(self, id_foret, nom, coords):
        """
        Entrées \\: \n
            id_foret: identifiant de la foret (doit être le meme que dans
                    la BDD)
            nom: nom de la foret
            coords: liste de polygones (MultiPolygon coords)
        Rôle \\: Ajoute une foret au fichier GeoJSON
        """
        nouvelle_feature = {
            "type": "Feature",
            "properties": {
                "id": id_foret,
                "name": nom
            },
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": coords
            }
        }

        self.data['features'].append(nouvelle_feature)
        self.sauvegarder()

    def creer_feature(self, id_feature, nom, geometry_type, coords):
        """
        Entrées \\: \n
            id_feature: identifiant de la feature
            nom: nom de la feature
            geometry_type: type de géometrie (ex: 'Polygon' ou
                    'MultiPolygon')
            coords: coordonnées de la géometrie
        Rôle \\: Cree une nouvelle feature si elle n'existe pas deja
        Sortie \\: True si cree, False si deja existante
        """
        # On vérifie d'abord si la feature existe deja pour éviter les doublons
        trouve = False
        features = self.data['features']
        nb_features = len(features)
        idx = 0

        while idx < nb_features and not trouve:
            feature = features[idx]
            props = feature.get('properties', {})
            if props.get('id') == id_feature or props.get('@id') == id_feature:
                trouve = True
            idx += 1

        if trouve:
            return False

        nouvelle_feature = {
            "type": "Feature",
            "properties": {
                "id": id_feature,
                "name": nom
            },
            "geometry": {
                "type": geometry_type,
                "coordinates": coords
            }
        }
        self.data['features'].append(nouvelle_feature)
        self.sauvegarder()
        return True

    def ajouter_a_feature(self, id_feature, nouvelles_coords):
        """
        Entrées \\: \n
            id_feature: identifiant de la feature à modifier
            nouvelles_coords: coordonnées du nouveau polygone à ajouter
        Rôle \\: \n
            Ajoute un polygone a une feature existante.
            Si c'est un Polygon, il devient un MultiPolygon.
            Si c'est deja un MultiPolygon, on ajoute les coordonnées
        Sortie \\: True si ajoute, False sinon
        """
        trouve = False
        features = self.data['features']
        nb_features = len(features)
        idx = 0

        while idx < nb_features and not trouve:
            feature = features[idx]
            props = feature.get('properties', {})
            if props.get('id') == id_feature or props.get('@id') == id_feature:
                trouve = True
                geometry = feature.get('geometry')

                if not geometry:
                    # Si pas de géometrie, on en cree une
                    feature['geometry'] = {
                        "type": "Polygon",
                        "coordinates": nouvelles_coords
                    }

                elif geometry['type'] == 'Polygon':
                    # Transformation Polygon -> MultiPolygon
                    anciennes_coords = geometry['coordinates']

                    if not anciennes_coords:
                        # Polygon vide : on remplace directement
                        geometry['coordinates'] = nouvelles_coords
                    else:
                        # Polygon réel : transformation en MultiPolygon
                        geometry['type'] = 'MultiPolygon'
                        geometry['coordinates'] = [
                            anciennes_coords, nouvelles_coords
                        ]

                elif geometry['type'] == 'MultiPolygon':
                    # Ajout au MultiPolygon existant
                    geometry['coordinates'] = [
                        coords for coords in geometry['coordinates'] if coords
                    ]
                    geometry['coordinates'].append(nouvelles_coords)

                else:
                    # Par défaut si type different (ex: Point), on remplace
                    geometry['type'] = 'Polygon'
                    geometry['coordinates'] = nouvelles_coords

                self.sauvegarder()
            idx += 1

        return trouve

    def supprimer_feature(self, id_feature):
        """
        Entrées \\: \n
            id_feature: identifiant de la feature à supprimer
        Rôle \\: Supprime une feature du fichier GeoJSON
        Sortie \\: True si supprimée, False sinon
        """
        trouve = False
        features = self.data['features']
        nb_features = len(features)
        idx = 0

        while idx < nb_features and not trouve:
            feature = features[idx]
            props = feature.get('properties', {})
            if props.get('id') == id_feature or props.get('@id') == id_feature:
                features.pop(idx)
                trouve = True
                self.sauvegarder()
            idx += 1
        return trouve

    def retirer_de_feature(self, id_feature, index_polygone):
        """
        Entrées \\: \n
            id_feature: identifiant de la feature a modifier
            index_polygone: index du polygone a retirer dans la liste
        Rôle \\: \n
            Retire un polygone d'une feature. S'il ne reste qu'un polygone,
            on retransforme le MultiPolygon en Polygon.
        Sortie \\: True si retire, False sinon
        """
        trouve = False
        features = self.data['features']
        nb_features = len(features)
        idx = 0

        while idx < nb_features and not trouve:
            feature = features[idx]
            props = feature.get('properties', {})
            if props.get('id') == id_feature or props.get('@id') == id_feature:
                trouve = True
                geometry = feature.get('geometry')

                if geometry and geometry['type'] == 'MultiPolygon':
                    coords = geometry['coordinates']
                    if 0 <= index_polygone < len(coords):
                        coords.pop(index_polygone)

                        # Si il n'en reste qu'un, on repasse en Polygon
                        if len(coords) == 1:
                            geometry['type'] = 'Polygon'
                            geometry['coordinates'] = coords[0]
                        elif len(coords) == 0:
                            # Plus de géometrie
                            feature['geometry'] = None

                        self.sauvegarder()
                    else:
                        trouve = False # Index invalide
                elif geometry and (geometry['type'] == 'Polygon'
                                   and index_polygone == 0):
                    feature['geometry'] = None
                    self.sauvegarder()
                else:
                    trouve = False # Pas de polygone a cet index ou pas le bon type
            idx += 1
        return trouve

    def mettre_a_jour_nom(self, id_feature, nouveau_nom):
        for feature in self.data['features']:
            props = feature.get('properties', {})
            if props.get('id') == id_feature or props.get('@id') == id_feature:
                props['name'] = nouveau_nom
                self.sauvegarder()
                return True
        return False

    def sauvegarder(self):
        """
        Rôle \\: Sauvegarde les données actuelles dans le fichier JSON
        """
        with open(self.json_path, 'w', encoding='utf-8') as file_json:
            json.dump(self.data, file_json, indent=4)


class InteractionDonnees:
    """
    Classe de coordination entre la BDD SQLite et le fichier GeoJSON
    """
    def __init__(self, bdd_path, json_path, debug=False):
        """
        Entrées \\: \n
            bdd_path: chemin vers le fichier de base de données
            json_path: chemin vers le fichier GeoJSON
            debug: booléen pour activer/désactiver le mode debug (par défaut: False)
        Rôle \\: \n
            Initialise les interactions avec la base de données SQLite et le fichier GeoJSON.
            Cree une instance de BaseDeDonnees et une instance de InteractionJSON.
        Sortie \\: \n
            self.bdd: instance de BaseDeDonnees pour interagir avec la base de données
            self.json: instance de InteractionJSON pour interagir avec le fichier GeoJSON
            self.debug: booléen indiquant si le mode debug est active
        """
        self.bdd = BaseDeDonnees(bdd_path)
        self.json = InteractionJSON(json_path)
        self.debug = debug

        self.synchro_depuis_bdd()
        self.synchro_depuis_json()

    def ajouter_foret(self, valeurs_bdd, coords_json):
        """
        Entrées \\: \n
            valeurs_bdd: liste des valeurs pour la table FORET
                    (id_foret, id_feature, nom, nb_visi,
                    superficie, ...)
            coords_json: coordonnées initiales (Polygon) pour le GeoJSON
        Rôle \\: Ajoute une foret dans la BDD et dans le GeoJSON
        """
        # Ajout dans la BDD
        # On suppose que valeurs_bdd est une liste complete correspondant au schema
        self.bdd.ajouter_ligne("FORET", valeurs_bdd)

        # Ajout dans le JSON
        id_feature = valeurs_bdd[1]
        nom_foret = valeurs_bdd[2]
        self.json.creer_feature(id_feature, nom_foret, "Polygon", coords_json)

    def supprimer_foret(self, id_foret):
        """
        Entrées \\: \n
            id_foret: identifiant de la foret à supprimer
        Rôle \\: Supprime une foret de la BDD et du fichier GeoJSON
        """
        # Suppression JSON
        infos = self.bdd.rechercher_ligne("FORET", ("id_foret", id_foret))
        id_feature = str(infos[0][1]) if infos else str(id_foret)
        self.json.supprimer_feature(id_feature)

        # Suppression BDD
        self.bdd.supprimer_ligne("FORET", ("id_foret", id_foret))

    def rechercher_foret(self, critere):
        """
        Entrées \\: \n
            critère: tuple (colonne, valeur) pour la recherche
        Rôle \\: \n
            Recherche des forets dans la BDD correspondant au critère.
            Si on cherche par nom, cela permet de retrouver l'id GeoJSON.
        Sortie \\: liste des résultats (lignes de la table FORET)
        """
        return self.bdd.rechercher_ligne("FORET", critere)

    def ajouter_polygone_a_foret(self, id_foret, nouvelles_coords):
        """
        Entrées \\: \n
            id_foret: identifiant de la foret
            nouvelles_coords: coordonnées du nouveau polygone
        Rôle \\: Ajoute une zone (polygone) à une foret existante dans le JSON
        Sortie \\: True si ajoute, False sinon
        """
        infos = self.bdd.rechercher_ligne("FORET", ("id_foret", id_foret))
        id_feature = str(infos[0][1]) if infos else str(id_foret)
        return self.json.ajouter_a_feature(id_feature, nouvelles_coords)

    def retirer_polygone_a_foret(self, id_foret, index_polygone):
        """
        Entrées \\: \n
            id_foret: identifiant de la foret
            index_polygone: index du polygone à retirer
        Rôle \\: Retire une zone (polygone) d'une foret dans le JSON
        Sortie \\: True si retire, False sinon
        """
        infos = self.bdd.rechercher_ligne("FORET", ("id_foret", id_foret))
        id_feature = str(infos[0][1]) if infos else str(id_foret)
        return self.json.retirer_de_feature(id_feature, index_polygone)

    def rechercher_feature(self, id_feature):
        """
        Entrées \\: \n
            id_feature: identifiant literal de la feature
        Rôle \\: Recherche la feature correspondante dans le GeoJSON
        Sortie \\: La feature si trouvée, None sinon
        """
        feature = self.json.rechercher_feature(id_feature)
        return feature
    
    def rechercher_feature_foret(self, id_foret):
        """
        Entrées \\: \n
            id_foret: identifiant de la foret
        Rôle \\: Recherche la feature correspondante dans le GeoJSON
        Sortie \\: La feature si trouvée, None sinon
        """
        infos = self.bdd.rechercher_ligne("FORET", ("id_foret", id_foret))
        id_feature = str(infos[0][1]) if infos else str(id_foret)
        feature = self.json.rechercher_feature(id_feature)
        return feature

    def synchro_depuis_json(self):
        """
        Rôle \\: \n
            Parcourt le GeoJSON et ajoute à la BDD les forets manquantes.
            C'est utile si le fichier GeoJSON contient plus de données
            que la BDD
        Sortie \\: Modifie la BDD en y ajoutant les lignes manquantes
        """
        # On recupere toutes les features du GeoJSON
        features = self.json.data.get('features', [])
        if self.debug: print(features)

        for feature in features:
            # On extrait l'identifiant et le nom depuis les propriétés
            props = feature.get('properties', {})
            id_geojson = props.get('@id')
            # Si pas d'ID, on saute cette feature pour éviter les erreurs
            if not id_geojson:
                continue

            nom = props.get('name', 'Foret inconnue')

            # On vérifie si la foret existe deja dans la BDD (recherche par id_feature)
            existe = self.bdd.rechercher_ligne("FORET", ("id_feature", id_geojson))
            if self.debug: print('Existe : ', existe)

            # Si elle n'existe pas, on l'ajoute avec des valeurs par défaut
            if not existe:
                # Calcul d'un nouvel id_foret (numérique)
                forets_actuelles = self.bdd.recuperer_tout("FORET")
                if not forets_actuelles:
                    nouvel_id = 1
                else:
                    # On prend le max des id_foret et on ajoute 1
                    nouvel_id = max(f[0] for f in forets_actuelles) + 1

                # Structure de la table FORET :
                # id_foret, id_feature, nom, nb_visi_par_an, superficie,
                # implan_naturelle
                valeurs = [nouvel_id, id_geojson, nom, 0, 0.0, 0]
                if self.debug: print("Ajout de la ligne", valeurs)
                self.bdd.ajouter_ligne("FORET", valeurs)

    def synchro_depuis_bdd(self):
        """
        Rôle \\: \n
            Parcourt la BDD et ajoute au GeoJSON les forets manquantes.
            C'est utile si la BDD contient plus de données que le
            fichier GeoJSON
        Sortie \\: Modifie le GeoJSON en y ajoutant les features manquantes
        """
        # On recupere toutes les forets de la BDD
        forets = self.bdd.recuperer_tout("FORET")

        for foret in forets:
            # Structure de la table FORET : id_foret, id_feature, nom, ...
            id_feature = foret[1]
            nom = foret[2]

            if not id_feature:
                continue

            # On vérifie si la foret existe deja dans le GeoJSON
            existe = self.json.rechercher_feature(id_feature)

            # Si elle n'existe pas, on l'ajoute avec une géometrie vide
            if not existe:
                # On utilise un MultiPolygon vide par défaut
                self.json.creer_feature(id_feature, nom, "MultiPolygon", [])

    def recuperer_centre_foret(self, nom_foret):
        """
        Entrées \\: \n
            nom_foret: nom de la foret
        Rôle \\: \n
            Retrouve le centre (centroid) de la foret à partir de son nom
        Sortie \\: (longitude, latitude) du centre, ou None si non trouvé
        """
        #1. Rechercher la foret par son nom dans la BDD pour avoir l'id_feature
        resultats = self.bdd.rechercher_ligne("FORET", ("nom", nom_foret))
        if not resultats:
            return None

        # Structure de la table FORET : id_foret, id_feature, nom, ...
        # On prend le premier resultat
        id_feature = resultats[0][1]

        #2. Rechercher la feature dans le GeoJSON
        feature = self.json.rechercher_feature(id_feature)
        if not feature or not feature.get('geometry'):
            return None

        #3. Calculer le centre avec shapely
        geometrie = shape(feature['geometry'])
        centre = geometrie.centroid

        if centre.is_empty:
            return None

        return centre.y, centre.x

    def calculer_superficie_foret(self, id_entree):
        """
        Entrées \\: \n
            id_entree: identifiant de la foret (int pour id_foret ou
                    str pour id_feature)
        Rôle \\: \n
            Calcule la superficie de la foret à partir de sa géometrie
            dans le GeoJSON
        Sortie \\: superficie:float ou None : superficie de la forêt si trouvée
        """
        # Determine l'id_feature
        if isinstance(id_entree, int):
            # C'est un ID numérique de la BDD, on cherche l'id_feature
            res = self.bdd.rechercher_ligne("FORET", ("id_foret", id_entree))
            if not res:
                return None
            id_feature = res[0][1]
        else:
            # On suppose que c'est l'id_feature directement
            id_feature = id_entree

        # Recuperation de la feature
        feature = self.json.rechercher_feature(id_feature)
        if not feature or not feature.get('geometry'):
            return None

        # Calcul de la superficie
        geometrie = shape(feature['geometry'])
        # La géometrie est en degrés (WGS84)

        if geometrie.is_empty:
            return 0.0

        # On calcule l'aire en degrés carres
        aire_deg2 = geometrie.area

        # Conversion en hectares (approximation pour la France/Vendee)
        # 1 degré de latitude ~= 111132 m
        # 1 degré de longitude ~= 111132 * cos(latitude) m
        # On utilise le centre de la géometrie pour la latitude
        centre = geometrie.centroid
        lat_rad = math.radians(centre.y)

        m_per_deg_lat = 111132
        m_per_deg_lon = 111132 * math.cos(lat_rad)

        # Superficie en m2 = aire_deg2 * m_per_deg_lat * m_per_deg_lon
        superficie_m2 = aire_deg2 * m_per_deg_lat * m_per_deg_lon

        # 1 hectare = 10 000 m2
        superficie_ha = superficie_m2 / 10000

        return float(superficie_ha)

    def mettre_a_jour_nom_foret(self, id_foret, nouveau_nom):
        self.json.mettre_a_jour_nom(str(id_foret), nouveau_nom)

    def fermer(self):
        """
        Rôle \\: ferme les interactions (connexion BDD)
        """
        self.bdd.fermer()


def charger_donnees_csv(liste, col=1):
    """
    Entrées \\: \n
        liste: liste de str, chemin vers le fichier CSV
        col: int, index de la colonne à extraire (par défaut : 1)
    Rôle \\: Charge les données d'une colonne spécifique d'un fichier CSV
    Sortie \\: liste des valeurs de la colonne spécifiée
    """
    data = []
    chemin = os.sep.join(liste)
    with open(chemin, newline='', encoding="ISO 8859-3") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader, None)
        for row in reader:
            if len(row) > col:
                data.append(row[col])

    return data

def rechercher_dans_csv(chemin, col, valeur):
    """
    Entrées \\: \n
        chemin: str, chemin vers le fichier CSV
        col: int, index de la colonne è rechercher
        valeur: any, valeur è rechercher dans la colonne
    Rôle \\: Recherche les lignes d'un fichier CSV ou une colonne a une valeur spécifique
    Sortie \\: liste des lignes correspondant au critère
    """
    data = []
    with open(chemin, newline="", encoding="ISO 8859-3") as fichier:
        reader = csv.reader(fichier, delimiter=";")
        next(reader, None)
        for ligne in reader:
            if len(ligne) > col and ligne[col] == valeur:
                data.append(ligne)

    return data

def charger_noms_forets(liste):
    """
    Entrées \\: \n
        liste: liste de str, chemin vers le fichier GeoJSON
    Rôle \\: Charge les noms des forets depuis un fichier GeoJSON
    Sortie \\: liste des noms des forets
    """
    json_path = os.sep.join(liste)

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    names = []
    for feature in data.get("features", []):
        props = feature.get("properties", {})
        name = props.get("name")
        if name:
            names.append(name)


    return names

def normaliser(coords):
    return json.loads(json.dumps(coords))

def sous_polygones(coords):
    coords_norm = normaliser(coords)
    if coords_norm and coords_norm[0]:
        # coords peut être un Polygon ou un MultiPolygon, on détecte lequel en
        # regardant si le premier élément est une liste de points ou une liste
        # de listes
        if isinstance(coords_norm[0][0][0], list):
            return coords_norm       # MultiPolygon
    
    return [coords_norm]         # Polygon