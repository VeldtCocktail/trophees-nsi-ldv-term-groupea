# Projet : SilvaDaVinci
# Auteurs : Mathéo PASQUIER, Maden USSEREAU, Léon RAIFAUD, Charlélie PINEAU

# importation des bibliothèques nécessaires au module
import sqlite3
import json
import csv
import os
import math
from shapely.geometry import shape, mapping
from shapely.ops import orient


class BaseDeDonnees:
    """
    Classe permettant l'interaction avec le fichier de base de données SQLite
    """

    def __init__(self, nom_fichier):
        """
        Entrées \\: \n
            self:BaseDeDonnees : instance de la classe BaseDeDonnees
            nom_fichier:str : chemin vers le fichier de base de données

        Rôle \\: \n
            Initialise l'interaction avec le fichier de base de données

        Sortie \\: \n
            None
        """
        # Connexion avec la base de données, à l'aide de sqlite3
        self.connexion = sqlite3.connect(nom_fichier)
        # Création du curseur, pour pouvoir exécuter des commandes
        self.curseur = self.connexion.cursor()

    def fermer(self):
        """
        Entrées \\: \n
            self:BaseDeDonnees : instance de la classe BaseDeDonnees

        Rôle \\: \n
            Ferme la connexion avec la base de données

        Sortie \\: \n
            None
        """
        # fermeture de la connexion
        self.connexion.close()

    def ajouter_ligne(self, table, valeurs):
        """
        Entrées \\: \n
            self:BaseDeDonnees : instance de la classe BaseDeDonnees
            table:str : nom de la table dans laquelle on veut ajouter une ligne
            valeurs:list[any] : liste des valeurs à insérer

        Rôle \\: \n
            Ajoute une ligne dans la table spécifiée avec les valeurs données
            dans valeurs

        Sortie \\: \n
            None
        """
        # Variable temporaire pour le stockage des valeurs à ajouter
        temp = ", ".join(["?" for element in valeurs])
        # Variable contenant la requête SQL
        requete = f"INSERT INTO {table} VALUES ({temp})"
        # On "imprime" cette requête
        self.curseur.execute(requete, valeurs)
        # Et on l'exécute
        self.connexion.commit()

    def supprimer_ligne(self, table, identification):
        """
        Entrées \\: \n
            self:BaseDeDonnees : instance de la classe BaseDeDonnees
            table:str : nom de la table
            identification:tuple(colonne:str, valeur:any) : critère de
                suppression, ex: ("id_foret", 1)

        Rôle \\: \n
            Supprime une ligne dans la table spécifiée correspondant au critère

        Sortie \\: \n
            None
        """
        # Variables pour identifier la/les lignes à supprimer
        # Il faut que l'attribut dans la colonne colonne
        colonne = identification[0]
        # Soit égal à valeur
        valeur = identification[1]
        # Variable contenant la requête SQL
        requete = f"DELETE FROM {table} WHERE {colonne} = ?"
        # On "imprime" cette requête
        self.curseur.execute(requete, (valeur,))
        # Et on l'exécute
        self.connexion.commit()

    def modifier_ligne(self, table, modif):
        """
        Entrées \\: \n
            self:BaseDeDonnees : instance de la classe BaseDeDonnees
            table:str : nom de la table
            modif:tuple[tuple[str, any], str, any] : critère de modification et
                valeurs à modifier

        Rôle \\: \n
            Modifie une valeur dans la table spécifiée
            
        Sortie \\: \n
            None
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

        # Variable contenant la requête SQL
        requete = f'''
            UPDATE {table}
            SET {colonne_modif} = ?
            WHERE {colonne_id} = ?
        '''
        # On "imprime" cette requête
        self.curseur.execute(requete, (nouvelle_valeur, valeur_id))
        # Et on l'exécute
        self.connexion.commit()

    def rechercher_ligne(self, table, identification):
        """
        Entrées \\: \n
            self:BaseDeDonnees : instance de la classe BaseDeDonnees
            table:str : nom de la table
            identification:tuple[str: any], critère de recherche,
                ex: ("id_foret", 1)

        Rôle \\: \n
            Recherche une ligne dans la table spécifiée correspondant au
            critère

        Sortie \\: \n
            list[list[any]] : liste des lignes trouvées
        """
        # D'abord, dans quelle colonne on vérifie
        colonne = identification[0]
        # Et à quelle valeur ce doit être égal
        valeur = identification[1]
        # Variable contenant la requête SQL
        requete = f'''
            SELECT * FROM {table}
            WHERE {colonne} = ?
        '''
        # On "imprime" cette requête
        self.curseur.execute(requete, (valeur,))
        # Et on l'exécute, en renvoyant les valeurs
        return self.curseur.fetchall()

    def rechercher_valeur(self, table, identification, colonne_recherchee):
        """
        Entrées \\: \n
            self:BaseDeDonnees : instance de la classe BaseDeDonnees
            table:str : nom de la table
            identification:tuple[str: any] : critère de recherche,
                ex: ("id_foret", 1)
            colonne_recherchee:str : nom de la colonne dont on veut récupérer
                la valeur

        Rôle \\: \n
            Recherche une valeur dans la table spécifiée correspondant au
            critère

        Sortie \\: \n
            list[list[any]] : liste des lignes trouvées
        """
        # D'abord, dans quelle colonne on vérifie
        colonne = identification[0]
        # Et à quelle valeur ce doit être égal
        valeur = identification[1]
        # Variable contenant la requête SQL
        requete = f'''
            SELECT {colonne_recherchee} FROM {table}
            WHERE {colonne} = ?
        '''
        # On "imprime" cette requête
        self.curseur.execute(requete, (valeur,))
        # Et on l'exécute, en renvoyant les valeurs
        return self.curseur.fetchall()

    def recuperer_tout(self, table):
        """
        Entrées \\: \n
            self:BaseDeDonnees : instance de la classe BaseDeDonnees
            table:str : nom de la table

        Rôle \\: \n
            Récupérer toutes les lignes d'une table

        Sortie \\: \n
            list[list[any]] : liste des lignes trouvées
        """
        # Variable contenant la requête SQL
        requete = f"SELECT * FROM {table}"
        # On "imprime" cette requête
        self.curseur.execute(requete)
        # Et on l'exécute, en renvoyant les valeurs
        return self.curseur.fetchall()

    def vider_table(self, table):
        """
        Entrées \\: \n
            self:BaseDeDonnees : instance de la classe BaseDeDonnees
            table:str : nom de la table

        Rôle \\: \n
            Supprimer toutes les lignes d'une table

        Sortie \\: \n
            list[list[any]] : liste des lignes trouvées
        """
        # Variable contenant la requête SQL
        requete = f"DELETE FROM {table}"
        # On "imprime" cette requête
        self.curseur.execute(requete)
        # Et on l'exécute
        self.connexion.commit()


class InteractionJSON:
    """
    Classe d'interaction avec le fichier JSON
    """

    def __init__(self, chemin_json):
        """
        Entrées \\: \n
            self:InteractionJSON : instance de la classe InteractionJSON
            chemin_json:str : chemin vers le fichier JSON

        Rôle \\: \n
            Initialise l'interaction avec le fichier JSON

        Sortie \\: \n
            None
        """
        # On initialise le chemin vers le fichier formaté JSON
        self.chemin_json = chemin_json
        # On ouvre ce fichier
        with open(chemin_json, 'r', encoding='utf-8') as fichier_json:
            # Et on transfère toutes ces données dans self
            self.data = json.load(fichier_json)

    def rechercher_feature(self, id_feature):
        """
        Entrées \\: \n
            self:InteractionJSON : instance de la classe InteractionJSON
            id_feature:int : identifiant de la feature à rechercher

        Rôle \\: \n
            Recherche une feature dans le GeoJSON par son ID

        Sortie \\: \n
            feature_trouvee:None ou dict[any: any] : feature trouvée
        """
        # Liste de toutes les features du GeoJSON
        features = self.data.get('features', [])
        # Nombre total de features
        nb_features = len(features)
        # Indicateur de recherche
        trouve = False
        # Index courant dans la boucle
        idx = 0
        # Résultat à retourner
        feature_trouvee = None

        # Parcours jusqu'à trouver ou avoir tout parcouru
        while idx < nb_features and not trouve:
            feature = features[idx]

            # Nettoyage des MultiPolygon corrompus
            if feature:
                # Récupération de la géométrie de la feature
                geom = feature.get('geometry')

                if geom and geom['type'] == 'MultiPolygon':
                    # On filtre les sous-polygones vides/nuls
                    coords_propres = [
                        coords for coords in geom['coordinates'] if coords
                    ]

                    if len(coords_propres) != len(geom['coordinates']):
                        # Des coordonnées corrompues ont été trouvées,
                        #alors on les retire
                        geom['coordinates'] = coords_propres
                        # On sauvegarde immédiatement la correction
                        self.sauvegarder()

            # Propriétés de la feature (id, nom, ...)
            props = feature.get('properties', {})
            if props.get('id') == id_feature or props.get('@id') == id_feature:
                # La feature correspond à l'ID recherché (format 'id' ou
                #'@id' OpenStreetMap)
                trouve = True
                feature_trouvee = feature

            # Passage à la feature suivante
            idx += 1

        return feature_trouvee

    def ajouter_foret(self, id_foret, nom, coords):
        """
        Entrées \\: \n
            self:InteractionJSON : instance de la classe InteractionJSON
            id_foret:int : identifiant de la forêt (doit être le même que dans
                la BDD)
            nom:str : nom de la forêt
            coords:list[list[list[list[float] ou float]]] : polygone GeoJSON

        Rôle \\: \n
            Ajoute une forêt au fichier GeoJSON

        Sortie \\: \n
            None
        """
        # Dictionnaire représentant la nouvelle feature
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

        # On ajoute cette feature à data
        self.data['features'].append(nouvelle_feature)
        # Et on sauvegarde
        self.sauvegarder()

    def creer_feature(self, id_feature, nom, geometry_type, coords):
        """
        Entrées \\: \n
            self:InteractionJSON : instance de la classe InteractionJSON
            id_feature:str : identifiant de la feature à créer
            nom:str : nom de la feature à créer
            geometry_type:str : type de géométrie ('Polygon' ou 'MultiPolygon')
            coords:list[list[list[list[float] ou float]]] : polygone GeoJSON

        Rôle \\: \n
            Crée une nouvelle feature si elle n'existe pas déjà

        Sortie \\: \n
            bool : True si créée, False si déjà existante
        """
        # On vérifie d'abord si la feature existe déjà
        #pour éviter les doublons
        trouve = False
        # Référence à la liste des features
        features = self.data['features']
        nb_features = len(features)
        idx = 0

        # Parcours de toutes les features existantes
        while idx < nb_features and not trouve:
            feature = features[idx]
            props = feature.get('properties', {})
            if props.get('id') == id_feature or props.get('@id') == id_feature:
                # L'ID existe déjà : on arrête
                trouve = True
            idx += 1

        if trouve:
            # Feature déjà présente, on ne crée pas de doublon
            return False

        # Dictionnaire de la nouvelle feature à rajouter
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
        # Ajout de la feature à la liste
        self.data['features'].append(nouvelle_feature)
        # Persistance dans le fichier JSON
        self.sauvegarder()
        return True

    def ajouter_a_feature(self, id_feature, nouvelles_coords):
        """
        Entrées \\: \n
            self:InteractionJSON : instance de la classe InteractionJSON
            id_feature:str : identifiant de la feature à modifier
            nouvelle_coords:list[list[list[list[float] ou float]]] : polygone
                GeoJSON à ajouter

        Rôle \\: \n
            Ajoute un polygone à une feature existante.
            Si c'est un Polygon, il devient un MultiPolygon.
            Si c'est déjà un MultiPolygon, on ajoute les coordonnées

        Sortie \\: \n
            bool : True si ajouté, False sinon
        """
        # normalisation du sens des anneaux GeoJSON
        try:
            geom_temp = shape(
                {"type": "Polygon", "coordinates": nouvelles_coords}
            )
            geom_orientee = orient(geom_temp, sign = 1.0)
            nouvelles_coords = mapping(geom_orientee)["coordinates"]

        except Exception as erreur:
            print("Erreur :", erreur)

        trouve = False
        # Référence à la liste des features
        features = self.data['features']
        nb_features = len(features)
        idx = 0

        # Parcours jusqu'à trouver la feature
        while idx < nb_features and not trouve:
            feature = features[idx]
            props = feature.get('properties', {})
            if props.get('id') == id_feature or props.get('@id') == id_feature:
                trouve = True
                # Géométrie actuelle de la feature
                geometry = feature.get('geometry')

                if not geometry:
                    # Si pas de géométrie, on en crée une
                    feature['geometry'] = {
                        "type": "Polygon",
                        "coordinates": nouvelles_coords
                    }

                elif geometry['type'] == 'Polygon':
                    # Transformation Polygon -> MultiPolygon
                    anciennes_coords = geometry['coordinates']

                    if not anciennes_coords:
                        # Polygon vide: on remplace directement
                        geometry['coordinates'] = nouvelles_coords
                    else:
                        # Polygon réel: transformation en MultiPolygon
                        geometry['type'] = 'MultiPolygon'
                        geometry['coordinates'] = [
                            # L'ancien + le nouveau polygone
                            anciennes_coords, nouvelles_coords
                        ]

                elif geometry['type'] == 'MultiPolygon':
                    # Ajout au MultiPolygon existant
                    geometry['coordinates'] = [
                        # Nettoyage des coords vides
                        coords for coords in geometry['coordinates'] if coords
                    ]
                    # Ajout du nouveau polygone
                    geometry['coordinates'].append(nouvelles_coords)

                else:
                    # Par défaut si type différent (ex: Point), on remplace
                    geometry['type'] = 'Polygon'
                    geometry['coordinates'] = nouvelles_coords

                # Persistance après modification
                self.sauvegarder()
            idx += 1

        return trouve

    def supprimer_feature(self, id_feature):
        """
        Entrées \\: \n
            self:InteractionJSON : instance de la classe InteractionJSON
            id_feature:str : identifiant de la feature à supprimer

        Rôle \\: \n
            Supprime une feature du fichier GeoJSON

        Sortie \\: \n
            bool : True si supprimée, False sinon
        """
        trouve = False
        # Référence à la liste des features
        features = self.data['features']
        nb_features = len(features)
        idx = 0

        # Parcours jusqu'à trouver la feature
        while idx < nb_features and not trouve:
            feature = features[idx]
            props = feature.get('properties', {})
            if props.get('id') == id_feature or props.get('@id') == id_feature:
                # Suppression de la feature de la liste
                features.pop(idx)
                trouve = True
                # Persistance de la suppression
                self.sauvegarder()
            idx += 1
        return trouve

    def retirer_de_feature(self, id_feature, index_polygone):
        """
        Entrées \\: \n
            self:InteractionJSON : instance de la classe InteractionJSON
            id_feature:str : identifiant de la feature à modifier
            index_polygone:int : indice du polygone à retirer dans la liste

        Rôle \\: \n
            Retire un polygone d'une feature. S'il ne reste qu'un polygone,
            on retransforme le MultiPolygon en Polygon.

        Sortie \\: \n
            bool : True si retiré, False sinon
        """
        trouve = False
        # Référence à la liste des features
        features = self.data['features']
        nb_features = len(features)
        idx = 0

        # Parcours jusqu'à trouver la feature
        while idx < nb_features and not trouve:
            feature = features[idx]
            props = feature.get('properties', {})
            if props.get('id') == id_feature or props.get('@id') == id_feature:
                trouve = True
                # Géométrie actuelle de la feature
                geometry = feature.get('geometry')

                if geometry and geometry['type'] == 'MultiPolygon':
                    coords = geometry['coordinates']
                    # Vérification que l'index est valide
                    if 0 <= index_polygone < len(coords):
                        # Suppression du polygone à cet index
                        coords.pop(index_polygone)

                        # Si il n'en reste qu'un, on repasse en Polygon
                        if len(coords) == 1:
                            # Rétrogradation MultiPolygon -> Polygon
                            geometry['type'] = 'Polygon'
                            geometry['coordinates'] = coords[0]
                        elif len(coords) == 0:
                            # Plus de géométrie
                            # On supprime la géométrie entière
                            feature['geometry'] = None

                        # Persistance après modification
                        self.sauvegarder()
                    else:
                        trouve = False # Index invalide
                elif geometry and (geometry['type'] == 'Polygon'
                                   and index_polygone == 0):
                    # Polygon à un seul polygone : on supprime la géométrie
                    feature['geometry'] = None
                    self.sauvegarder()
                else:
                    # Pas de polygone à cet index ou pas le bon type
                    trouve = False
            idx += 1
        return trouve

    def mettre_a_jour_nom(self, id_feature, nouveau_nom):
        """
        Entrées \\: \n
            self:InteractionJSON : instance de la classe InteractionJSON
            id_feature:str : identifiant de la feature à modifier
            nouveau_nom:str : nouveau nom de la feature

        Rôle \\: \n
            Met à jour le nom d'une feature

        Sortie \\: \n
            bool : True si mise à jour, False sinon
        """
        # Parcours de toutes les features
        for feature in self.data['features']:
            props = feature.get('properties', {})
            if props.get('id') == id_feature or props.get('@id') == id_feature:
                # Mise à jour du nom
                props['name'] = nouveau_nom
                print('Nom mis à jour :', id_feature, nouveau_nom)
                # Persistance de la modification
                self.sauvegarder()
                return True
        # Feature non trouvée
        return False

    def sauvegarder(self):
        """
        Entrées : \\: \n
            self:InteractionJSON : instance de la classe InteractionJSON

        Rôle \\: \n
            Sauvegarde les données actuelles dans le fichier JSON

        Sortie \\: \n
            None
        """
        # on ouvre le fichier JSON et on y enregistre les données actuelles
        with open(self.chemin_json, 'w', encoding='utf-8') as fichier_json:
            json.dump(self.data, fichier_json, indent=4)


class InteractionDonnees:
    """
    Classe de coordination entre la BDD SQLite et le fichier GeoJSON
    """

    def __init__(self, bdd_path, chemin_json, debug = False):
        """
        Entrées \\: \n
            self:InteractionDonnees : instance de la classe InteractionDonnees
            bdd_path: chemin vers le fichier de base de données
            chemin_json: chemin vers le fichier GeoJSON
            debug: booléen pour activer/désactiver le mode debug

        Rôle \\: \n
            Initialise les interactions avec la base de données SQLite et le 
            fichier GeoJSON.
            Crée une instance de BaseDeDonnees et une instance de 
            InteractionJSON.

        Sortie \\: \n
            None
        """
        # on crée une instance des deux classes
        self.bdd = BaseDeDonnees(bdd_path)
        self.json = InteractionJSON(chemin_json)

        # on affecte la valeur de debug à l'attribut debug
        self.debug = debug

        # on synchronise les bases de données SQLite et GeoJSON
        self.synchro_depuis_bdd()
        self.synchro_depuis_json()

    def ajouter_foret(self, valeurs_bdd, coords_json):
        """
        Entrées \\: \n
            self:InteractionDonnees : instance de la classe InteractionDonnees
            valeurs_bdd: list[any] : liste des valeurs pour la table FORET
                    (id_foret, id_feature, nom, nb_visi, superficie, ...)
            coords_json:list[list[list[list[float] ou float]]] : polygone JSON

        Rôle \\: \n
            Ajoute une forêt dans la BDD et dans le GeoJSON

        Sortie \\: \n
            None
        """
        # Ajout dans la BDD
        # On suppose que valeurs_bdd est une liste complète correspondant au 
        # schéma
        self.bdd.ajouter_ligne("FORET", valeurs_bdd)

        # Ajout dans le JSON
        id_feature = valeurs_bdd[1]
        nom_foret = valeurs_bdd[2]
        self.json.creer_feature(id_feature, nom_foret, "Polygon", coords_json)

    def supprimer_foret(self, id_foret):
        """
        Entrées \\: \n
            self:InteractionDonnees : instance de la classe InteractionDonnees
            id_foret:str : identifiant de la forêt à supprimer

        Rôle \\: \n
            Supprime une forêt de la BDD et du fichier GeoJSON

        Sortie \\: \n
            None
        """
        # Suppression JSON
        # Récupération des infos BDD
        infos = self.bdd.rechercher_ligne("FORET", ("id_foret", id_foret)) 
        # id_feature = colonne [1] de la table
        id_feature = str(infos[0][1]) if infos else str(id_foret)           
        # Suppression dans le GeoJSON
        self.json.supprimer_feature(id_feature)                             

        # Suppression BDD
        self.bdd.supprimer_ligne("FORET", ("id_foret", id_foret))

    def rechercher_foret(self, critere):
        """
        Entrées \\: \n
            self:InteractionDonnees : instance de la classe InteractionDonnees
            critere:tuple[str, any] : critère pour la recherche dans la BDD

        Rôle \\: \n
            Recherche des forêts dans la BDD correspondant au critère.
            Si on cherche par nom, cela permet de retrouver l’id GeoJSON.

        Sortie \\: \n
            list[tuple(any)] : ligne trouvée (liste contenant un seul tuple)
        """
        return self.bdd.rechercher_ligne("FORET", critere)

    def ajouter_polygone_a_foret(self, id_foret, nouvelles_coords):
        """
        Entrées \\: \n
            self:InteractionDonnees : instance de la classe InteractionDonnees
            id_foret:str : identifiant de la forêt
            nouvelles_coords:list[list[list[list[float] ou float]]] : polygone
                GeoJSON à ajouter à la forêt

        Rôle \\: \n
            Ajoute une zone (polygone) à une forêt existante dans le JSON

        Sortie \\: \n
            bool : True si ajouté, False sinon
        """
        # Recherche de la forêt en BDD
        infos = self.bdd.rechercher_ligne("FORET", ("id_foret", id_foret))  
        # Extraction de l'id_feature GeoJSON
        id_feature = str(infos[0][1]) if infos else str(id_foret)           
        # Ajout du polygone dans le GeoJSON
        return self.json.ajouter_a_feature(id_feature, nouvelles_coords)    

    def retirer_polygone_a_foret(self, id_foret, index_polygone):
        """
        Entrées \\: \n
            self:InteractionDonnees : instance de la classe InteractionDonnees
            id_foret:str : identifiant de la forêt
            index_polygone:int : index du polygone à retirer de la forêt
            
        Rôle \\: \n
            Retire une zone (polygone) d'une forêt dans le JSON

        Sortie \\: \n
            bool : True si retiré, False sinon
        """
        # Recherche de la forêt en BDD
        infos = self.bdd.rechercher_ligne("FORET", ("id_foret", id_foret))  
        # Extraction de l'id_feature GeoJSON
        id_feature = str(infos[0][1]) if infos else str(id_foret)           
        # Retrait du polygone dans le GeoJSON
        return self.json.retirer_de_feature(id_feature, index_polygone)     

    def rechercher_feature(self, id_feature):
        """
        Entrées \\: \n
            self:InteractionDonnees : instance de la classe InteractionDonnees
            id_feature:str : identifiant littéral de la feature

        Rôle \\: \n
            Recherche la feature correspondante dans le GeoJSON

        Sortie \\: \n
            feature:None ou dict[any: any] : feature GeoJSON si trouvée
        """
        feature = self.json.rechercher_feature(id_feature)
        return feature

    def rechercher_feature_foret(self, id_foret):
        """
        Entrées \\: \n
            self:InteractionDonnees : instance de la classe InteractionDonnees
            id_foret:str : identifiant de la forêt

        Rôle \\: \n
            Recherche la feature correspondant à id_foret dans le GeoJSON

        Sortie \\: \n
            feature:None ou dict[any: any] : feature GeoJSON si trouvée
        """
        # Recherche de la forêt en BDD
        infos = self.bdd.rechercher_ligne("FORET", ("id_foret", id_foret))  
        # Extraction de l'id_feature GeoJSON
        id_feature = str(infos[0][1]) if infos else str(id_foret)           
        # Recherche dans le GeoJSON
        feature = self.rechercher_feature(id_feature)                  
        return feature

    def synchro_depuis_json(self):
        """
        Entrées \\: \n
            self:InteractionDonnees : instance de la classe InteractionDonnees

        Rôle \\: \n
            Parcourt le GeoJSON et ajoute à la BDD les forêts manquantes.

        Sortie \\: \n
            None
        """
        # On récupère toutes les features du GeoJSON
        # Liste de toutes les features GeoJSON
        features = self.json.data.get('features', [])

        # Parcours de chaque feature GeoJSON
        for feature in features:                         
            # On extrait l'identifiant et le nom depuis les propriétés
            props = feature.get('properties', {})
            # ID OpenStreetMap (format '@id')
            id_geojson = props.get('@id')                
            # Si pas d'ID, on saute cette feature pour éviter les erreurs
            if not id_geojson:
                continue

            # Nom de la forêt, valeur par défaut si absent
            nom = props.get('name', "nom inconnu")

            # On vérifie si la forêt existe déjà dans la BDD (recherche par 
            # id_feature)
            existe = self.bdd.rechercher_ligne(
                "FORET", ("id_feature", id_geojson)
            )
            if self.debug: print('Existe : ', existe)

            # Si elle n'existe pas, on l'ajoute avec des valeurs par défaut
            if not existe:
                # Calcul d'un nouvel id_foret (numérique)
                # Toutes les forêts de la BDD
                forets_actuelles = self.bdd.recuperer_tout("FORET")
                if not forets_actuelles:
                    # Première forêt : id = 1
                    nouvel_id = 1
                else:
                    # On prend le max des id_foret et on ajoute 1
                    # Auto-incrémentation manuelle
                    nouvel_id = max(f[0] for f in forets_actuelles) + 1  

                # Structure de la table FORET:
                # id_foret, id_feature, nom, nb_visi_par_an, superficie,
                # implan_naturelle
                # Valeurs par défaut pour les champs manquants
                valeurs = [nouvel_id, id_geojson, nom, 0, 0.0, 0]   
                if self.debug: print("Ajout de la ligne", valeurs)
                # Insertion dans la BDD
                self.bdd.ajouter_ligne("FORET", valeurs)             

    def synchro_depuis_bdd(self):
        """
        Entrées \\: \n
            self:InteractionDonnees : instance de la classe InteractionDonnees

        Rôle \\: \n
            Parcourt la BDD et ajoute au GeoJSON les forêts manquantes.

        Sortie \\: \n
            None
        """
        # On récupère toutes les forêts de la BDD
        # Toutes les lignes de la table FORET
        forets = self.bdd.recuperer_tout("FORET")          

        # Parcours de chaque forêt en BDD
        for foret in forets:                               
            # Structure de la table FORET: id_foret, id_feature, nom, ...
            # Colonne id_feature (index 1)
            id_feature = foret[1]                          
            # Colonne nom (index 2)
            nom = foret[2]                                 

            # On ignore les forêts sans id_feature (données incomplètes)
            if not id_feature:                             
                continue

            # On vérifie si la forêt existe déjà dans le GeoJSON
            existe = self.json.rechercher_feature(id_feature)

            # Si elle n'existe pas, on l'ajoute avec une géométrie vide
            if not existe:
                # On utilise un MultiPolygon vide par défaut
                # Géométrie vide, à remplir plus tard
                self.json.creer_feature(id_feature, nom, "MultiPolygon", [])  

    def recuperer_centre_foret(self, nom_foret):
        """
        Entrées \\: \n
            self:InteractionDonnees : instance de la classe InteractionDonnees
            nom_foret:str : nom de la forêt

        Rôle \\: \n
            Retrouve le centre (centroid) de la forêt à partir de son nom

        Sortie \\: \n
            None ou tuple[float] : centre de la forêt si il existe
        """
        # 1. Rechercher la forêt par son nom dans la BDD pour avoir id_feature
        # Recherche par nom
        resultats = self.bdd.rechercher_ligne("FORET", ("nom", nom_foret))  
        if not resultats:
            # Forêt inconnue
            return None                                     

        # Structure de la table FORET: id_foret, id_feature, nom, ...
        # On prend le premier résultat
        # Extraction de l'id_feature (colonne index 1)
        id_feature = resultats[0][1]                        

        # 2. Rechercher la feature dans le GeoJSON
        feature = self.json.rechercher_feature(id_feature)
        # Absence de géométrie => pas de centre calculable
        if not feature or not feature.get('geometry'):      
            return None

        # 3. Calculer le centre avec shapely
        # Conversion en objet shapely
        geometrie = shape(feature['geometry'])              
        # Calcul du centroïde géographique
        centre = geometrie.centroid                         

        # Géométrie vide : pas de centroïde
        if centre.is_empty:
            return None                                     

        # Retourne (latitude, longitude)
        return centre.y, centre.x 

    def calculer_superficie_foret(self, id_entree):
        """
        Entrées \\: \n
            self:InteractionDonnees : instance de la classe InteractionDonnees
            id_entree:str ou int : identifiant de la forêt (int pour id_foret
                ou str pour id_feature)

        Rôle \\: \n
            Calcule la superficie de la forêt à partir de sa géométrie dans le
            fichier GeoJSON

        Sortie \\: \n
            superficie:float ou None : superficie de la forêt si trouvée
        """
        # Détermine l'id_feature
        if isinstance(id_entree, int):
            # C'est un ID numérique de la BDD, on cherche l'id_feature
            res = self.bdd.rechercher_ligne("FORET", ("id_foret", id_entree))
            if not res:
                # Forêt introuvable en BDD
                return None                                 
            # Extraction de l'id_feature (colonne index 1)
            id_feature = res[0][1]                          
        else:
            # On suppose que c'est l'id_feature directement
            id_feature = id_entree

        # Récupération de la feature
        feature = self.json.rechercher_feature(id_feature)
        # Absence de géométrie => superficie incalculable
        if not feature or not feature.get('geometry'):      
            return None

        # Calcul de la superficie
        # Conversion en objet shapely
        geometrie = shape(feature['geometry'])              
        # La géométrie est en degrés (WGS84)

        if geometrie.is_empty:
            # Géométrie vide => superficie nulle
            return 0.0                                      

        # On calcule l'aire en degrés carrés
        # Aire brute en degrés² (non métrique)
        aire_deg2 = geometrie.area                          

        # Conversion en hectares (approximation pour la France)
        # 1 degré de latitude ~= 111132 m
        # 1 degré de longitude ~= 111132 * cos(latitude) m
        # On utilise le centre de la géométrie pour la latitude

        # Centre de la géométrie pour la correction de longitude
        centre = geometrie.centroid                         
        # Latitude en radians (nécessaire pour cos)
        lat_rad = math.radians(centre.y)                   

        # Mètres par degré de latitude en France
        m_per_deg_lat = 111132                              
        # Mètres par degré de longitude (varie avec la latitude)
        m_per_deg_lon = 111132 * math.cos(lat_rad)         

        # Superficie en m2 = aire_deg2 * m_per_deg_lat * m_per_deg_lon
        # Conversion degrés² -> m²
        superficie_m2 = aire_deg2 * m_per_deg_lat * m_per_deg_lon

        # 1 hectare = 10 000 m2
        # Conversion m² -> hectares
        superficie_ha = superficie_m2 / 10000

        # on renvoie l'arrondi à 5 décimales de la superficie en hectares
        return float(round(superficie_ha, 5))

    def mettre_a_jour_nom_foret(self, id_foret, nouveau_nom):
        """
        Entrées \\: \n
            self:InteractionDonnees : instance de la classe InteractionDonnees
            id_feature:str : identifiant de la feature de la forêt à modifier
            nouveau_nom:str : nouveau nom de la forêt

        Rôle \\: \n
            Modifier le nom d’une forêt dans le fichier GeoJSON uniquement

        Sortie \\: \n
            None
        """
        # appel de la méthode de la classe InteractionJSON
        self.json.mettre_a_jour_nom(str(id_foret), nouveau_nom)

    def fermer(self):
        """
        Entrées \\: \n
            self:InteractionDonnees : instance de la classe InteractionDonnees

        Rôle \\: \n
            Ferme les interactions (connexion BDD)

        Sortie \\: \n
            None
        """
        self.bdd.fermer()


def charger_donnees_csv(liste, col = 1):
    """
    Entrées \\: \n
        liste:list[str] : chemin vers le fichier CSV
        col:int : indice de la colonne à extraire

    Rôle \\: \n
        Charger les données d’une colonne spécifique d’un fichier CSV

    Sortie \\: \n
        list[str] : liste des valeurs du fichier à la colonne 'col'
    """
    data = []
    # Construction du chemin depuis une liste de segments
    chemin = os.sep.join(liste)                            
    # Encodage Latin-3 (ISO 8859-3) pour les caractères spéciaux
    with open(chemin, newline='', encoding="ISO 8859-3") as f:  
        # Le fichier CSV utilise le point-virgule comme séparateur
        reader = csv.reader(f, delimiter=";")              
        # On saute la première ligne (en-tête des colonnes)
        next(reader, None)                                 
        for row in reader:
            # On vérifie que la ligne a bien la colonne demandée
            if len(row) > col:                             
                # Extraction de la valeur dans la colonne souhaitée
                data.append(row[col])                     

    # on revoie la liste des valeurs
    return data


def rechercher_dans_csv(chemin, col, valeur):
    """
    Entrées \\: \n
        chemin:str : chemin vers le fichier CSV
        col:int : indice de la colonne à rechercher
        valeur:any : valeur à rechercher dans la colonne

    Rôle \\: \n
        Recherche les lignes d'un fichier CSV où une colonne a une valeur
        spécifique

    Sortie \\: \n
        data:list[list[str]] : liste des lignes trouvées
    """
    data = []
    # Encodage Latin-3 pour les caractères spéciaux
    with open(chemin, newline="", encoding="ISO 8859-3") as fichier:  
        # Séparateur point-virgule
        reader = csv.reader(fichier, delimiter=";")        
        # Saut de la ligne d'en-tête
        next(reader, None)                                 
        for ligne in reader:
            # Vérification de la longueur et de la valeur recherchée
            if len(ligne) > col and ligne[col] == valeur:  
                # Ajout de la ligne entière si le critère est satisfait
                data.append(ligne)                         

    # on revoie la liste des lignes trouvées
    return data


def charger_noms_forets(liste):
    """
    Entrées \\: \n
        liste:list[str] : chemin vers le fichier GeoJSON

    Rôle \\: \n
        Charge les noms des forêts depuis un fichier GeoJSON

    Sortie \\: \n
        noms:list[str] : liste des noms des forêts
    """
    # Construction du chemin depuis une liste de segments
    chemin_json = os.sep.join(liste)

    # Chargement du GeoJSON en mémoire
    with open(chemin_json, encoding="utf-8") as f:
        data = json.load(f)                                

    noms = []
    # Parcours de toutes les features
    for feature in data.get("features", []):
        # Propriétés de la feature
        props = feature.get("properties", {})
        # Récupération du nom
        nom = props.get("name")
        # On ignore les features sans nom
        if nom is not None:
            noms.append(nom)

    return noms


def ajouter_a_dico(dico, liste):
        """
        Entrées \\: \n
            dico:dict[any: any]
            liste:list[str, list[list[int]], str] : listes contenant les clé à
                ajouter dans le dictionnaire, les listes de listes de nombres
                ainsi que les chemin des fichiers csv correspondant aux clés
        
        Rôle \\: \n
            Ajouter au dictionnaire dico lees clés de la liste en définissant
            leurs valeurs comme les éléments à la colonne 1 des lignes, dans
            lesquelles certains identifiants sont présents, des fichiers csv
            qui leurs correspondent
        
        Sortie \\: \n
            None
        """
        # pour chaque ligne de la liste
        for ligne in liste:
            
            # on récupère les trois éléments de la ligne
            cle, liste_listes, nom_csv = ligne

            # on construit le chemin du fichier csv correspondant
            chemin_csv = os.sep.join(["data", nom_csv])

            # on crée une liste vide en valeur de clé si la clé n'est pas dans
            # le dictionnaire
            if cle not in dico:
                dico[cle] = []

            # pour chaque liste de la liste de listes
            for elem in liste_listes:
                # on récupère l'identifiant de la valeur à rechercher
                id_val = str(elem[0])
                # on récupère les lignes pour lesquelles cette valeur est
                # présente comme identifiant dans le fichier csv adéquat
                resultat = rechercher_dans_csv(chemin_csv, 0, id_val)

                # si des lignes (une seule en réalité) ont été trouvées
                if resultat:
                    # on ajoute le nom du détail de la première (et seule)
                    # ligne obtenue depuis l'identifiant du détail
                    dico[cle].append(resultat[0][1])


def normaliser(coords):
    """
    Entrées \\: \n
        coords:list[list[list[list ou tuple[float] ou float]]] : polygone
            GeoJSON à normaliser
    
    Rôle \\: \n
        Normaliser un polygone GeoJson en transformant un objet Python en objet
        JSON, puis en repassant à un objet Python
    
    Sortie \\: \n
        coords:list[list[list[list[float] ou float]]] : polygone GeoJSON
    """
    # Sérialisation/désérialisation JSON pour convertir les tuples en listes
    # et supprimer les références partagées (deep copy via JSON)
    return json.loads(json.dumps(coords))


def sous_polygones(coords):
    """
    Entrées \\: \n
        coords:list[list[list[list ou tuple[float] ou float]]] : polygone ou
            multi-polygone GeoJSON à uniformiser
    
    Rôle \\: \n
        Uniformiser des coordonnées de polygone GeoJSON en prenant en compte
        le type de polygone ('Polygon' ou 'MultiPolygon' GeoJSON)

    Sortie \\: \n
        coords_norm:list[list[list[list[float]]]] : polygone uniformisé
    """
    # Normalisation des coordonnées (conversion tuples -> listes)
    coords_norm = normaliser(coords)               
    if coords_norm and coords_norm[0]:
        # coords peut être un Polygon ou un MultiPolygon, on détecte lequel en
        # regardant si le premier élément est une liste de points ou une liste
        # de listes

        # Si MultiPolygon : 4 niveaux d'imbrication
        if isinstance(coords_norm[0][0][0], list):  
            # MultiPolygon : déjà une liste de polygones
            return coords_norm       

        # Polygon : on l'encapsule dans une liste pour uniformiser
        return [coords_norm]         


def egaux(coords_a, coords_b, tolerance = 0.99):
    """
    Entrées \\: \n
        coords_a:list[list[list[list[float]]]] : coordonnées d'un polygone
        coords_b:list[list[list[list[float]]]] : coordonnées d'un polygone
        tolerance:float : ratio minimal d'intersection pour considérer deux
            polygones comme égaux (par défaut: 0.99)

    Rôle \\: \n
        Compare deux polygones géométriquement via shapely pour éviter
        les faux négatifs dûs aux différences de précision de flottants

    Sortie \\: \n
        bool : True si les deux polygones sont géométriquement équivalents
    """
    try:
        geo_a = shape({"type": "Polygon", "coordinates": coords_a})
        geo_b = shape({"type": "Polygon", "coordinates": coords_b})

        # si l'un des deux polygones est vide, on ne peut pas comparer
        if geo_a.area == 0 or geo_b.area == 0:
            return False

        # on calcule le ratio d'intersection sur le plus grand des polygones
        intersection = geo_a.intersection(geo_b)
        ratio = intersection.area / max(geo_a.area, geo_b.area)

        # on renvoie True si ce ratio est supérieur à la tolérance, False sinon
        return ratio > tolerance

    # on renvoie False si une erreur est survenue pendant la comparaison
    except Exception:
        return False