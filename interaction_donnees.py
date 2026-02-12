import sqlite3
import json
import os

class Interaction_bdd:
    """
    Classe permettant l'interaction avec le fichier de base de donnees
    """
    def __init__(self, nom_fichier):
        """
        Entrees : nom_fichier: chemin vers le fichier de base de donnees
        Role : initialise l'interaction avec le fichier de base de donnees
        Sortie : self.connexion contient la connexion avec la base de donnees
                 self.curseur contient le curseur pour executer des commandes
        """
        # Connexion avec la base de donnees, a l'aide de sqlite3
        self.connexion = sqlite3.connect(nom_fichier)
        # Creation du curseur, pour pouvoir executer des commandes
        self.curseur = self.connexion.cursor()

    def ajouter_ligne(self, table, valeurs):
        """
        Entrees : self:instance de BaseDeDonnees
                  table:str nom de la table
                  valeurs:list liste des valeurs a inserer dans la table
        Role : ajoute une ligne dans la table specifiee avec les valeurs
               donnees dans valeurs
        Sortie : modifie la base de donnees
        """
        # Variable temporaire pour le stockage des valeurs a ajouter
        temp = ", ".join(["?" for element in valeurs])
        # Variable contenant la requete SQL
        requete = f"INSERT INTO {table} VALUES ({temp})"
        # On "imprime" cette requete
        self.curseur.execute(requete, valeurs)
        # Et on l'execute
        self.connexion.commit()

    def supprimer_ligne(self, table, identification):
        """
        Entrees : self:instance de BaseDeDonnees
                  table:str nom de la table
                  identification:tuple(colonne:str, valeur:any) critere de
                          suppression, ex: ("id_foret", 1)
        Role : supprime une ligne dans la table specifiee correspondant au
               critere
        Sortie : base de donnees indiquee par self modifiee
        """
        # Variables pour identifier la/les lignes a supprimer
        # Il faut que l'attribut dans la colonne colonne
        colonne = identification[0]
        # Soit egal a valeur
        valeur = identification[1]
        # Variable contenant la requete SQL
        requete = f"DELETE FROM {table} WHERE {colonne} = ?"
        # On "imprime" cette requete
        self.curseur.execute(requete, (valeur,))
        # Et on l'execute
        self.connexion.commit()

    def modifier_ligne(self, table, modif):
        """
        Entrees : self:instance de BaseDeDonnees
                  table:str nom de la table
                  modif:tuple contient (
                  identification:tuple(colonne:str, valeur:any),
                                 colonne:str,
                                 valeur:any)
        Role : modifie une valeur dans la table specifiee
        Sortie : base de donnees modifiee
        """
        # Dans quelle colonne on doit modifier la variable
        colonne_modif = modif[1]
        # Et la nouvelle valeur de ce dernier
        nouvelle_valeur = modif[2]

        # Variable pour l'identification de la/des colonnes a modifier
        identification = modif[0]
        # D'abord, dans quelle colonne on verifie
        colonne_id = identification[0]
        # Et a quelle valeur ce doit etre egal
        valeur_id = identification[1]

        # Variable contenant la requete SQL
        requete = f'''
            UPDATE {table}
            SET {colonne_modif} = ?
            WHERE {colonne_id} = ?
        '''
        # On "imprime" cette requete
        self.curseur.execute(requete, (nouvelle_valeur, valeur_id))
        # Et on l'execute
        self.connexion.commit()

    def rechercher_ligne(self, table, identification):
        """
        Entrees : self:instance de BaseDeDonnees
                  table:str nom de la table
                  identification:tuple(colonne:str, valeur:any) critere de
                          recherche, ex: ("id_foret", 1)
        Role : recherche une ligne dans la table specifiee correspondant au
               critere
        Sortie : liste des lignes trouvees
        """
        # Variable pour l'identification de la/des colonnes a rechercher
        identification = identification[0]
        # D'abord, dans quelle colonne on verifie
        colonne = identification[0]
        # Et a quelle valeur ce doit etre egal
        valeur = identification[1]
        # Variable contenant la requete SQL
        requete = f'''
            SELECT * FROM {table}
            WHERE {colonne} = ?
        '''
        # On "imprime" cette requete
        self.curseur.execute(requete, (valeur,))
        # Et on l'execute
        return self.curseur.fetchall()

    def rechercher_valeur(self, table, identification, colonne_recherchee):
        """
        Entrees : self:instance de BaseDeDonnees
                  table:str nom de la table
                  identification:tuple(colonne:str, valeur:any) critere de
                          recherche, ex: ("id_foret", 1)
                  colonne_recherchee:str nom de la colonne dont on veut
                          recuperer la valeur
        Role : recherche une valeur dans la table specifiee correspondant au
               critere
        Sortie : liste des valeurs trouvees
        """
        # Variable pour l'identification de la/des colonnes a rechercher
        identification = identification[0]
        # D'abord, dans quelle colonne on verifie
        colonne = identification[0]
        # Et a quelle valeur ce doit etre egal
        valeur = identification[1]
        # Variable contenant la requete SQL
        requete = f'''
            SELECT {colonne_recherchee} FROM {table} 
            WHERE {colonne} = ?
        '''
        # On "imprime" cette requete
        self.curseur.execute(requete, (valeur,))
        # Et on l'execute
        return self.curseur.fetchall()


class Interaction_json:
    """
    Classe d'interaction avec le fichier JSON
    """
    def __init__(self, json_path):
        """
        Entrees : json_path: chemin vers le fichier JSON
        Role : initialise l'interaction avec le fichier JSON
        Sortie : self.data contient les donnees du fichier JSON
        """
        self.json_path = json_path
        with open(json_path, 'r', encoding='utf-8') as file_json:
            self.data = json.load(file_json)

    def ajouter_foret(self, id_foret, nom, coords):
        """
        Entrees : id_foret: identifiant de la foret (doit etre le meme que dans
                  la BDD)
                  nom: nom de la foret
                  coords: liste de polygones (MultiPolygon coords)
        Role : Ajoute une foret au fichier GeoJSON
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
        Entrees : id_feature: identifiant de la feature
                  nom: nom de la feature
                  geometry_type: type de geometrie (ex: 'Polygon' ou 
                                 'MultiPolygon')
                  coords: coordonnees de la geometrie
        Role : Cree une nouvelle feature si elle n'existe pas deja
        """
        # On verifie d'abord si la feature existe deja pour eviter les doublons
        for feature in self.data['features']:

            if feature['properties'].get('id') == id_feature:

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
        Entrees : id_feature: identifiant de la feature a modifier
                  nouvelles_coords: coordonnees du nouveau polygone a ajouter
        Role : Ajoute un polygone a une feature existante. 
               Si c'est un Polygon, il devient un MultiPolygon.
               Si c'est deja un MultiPolygon, on ajoute les coordonnees
        """
        for feature in self.data['features']:

            if feature['properties'].get('id') == id_feature:

                geometry = feature.get('geometry')

                if not geometry:
                    # Si pas de geometrie, on en cree une
                    feature['geometry'] = {
                        "type": "Polygon",
                        "coordinates": nouvelles_coords
                    }

                elif geometry['type'] == 'Polygon':

                    # Transformation Polygon -> MultiPolygon
                    anciennes_coords = geometry['coordinates']
                    geometry['type'] = 'MultiPolygon'
                    geometry['coordinates'] = [anciennes_coords,
                                               nouvelles_coords]

                elif geometry['type'] == 'MultiPolygon':

                    # Ajout au MultiPolygon existant
                    geometry['coordinates'].append(nouvelles_coords)

                else:
                    # Par defaut si type different (ex: Point), on remplace
                    geometry['type'] = 'Polygon'
                    geometry['coordinates'] = nouvelles_coords
                
                self.sauvegarder()

                return True

        return False


    def supprimer_foret(self, id_foret):
        """
        Entree : id_foret:int identifiant de la foret a supprimer
        Role : Supprime une foret du fichier GeoJSON
        """
        self.data['features'] = [
            feature for feature in self.data['features'] 
            if feature['properties'].get('id') != id_foret
        ]
        self.sauvegarder()

    def sauvegarder(self):
        """
        Role : Ecrit les modifications dans le fichier JSON
        """
        with open(self.json_path, 'w', encoding='utf-8') as file_json:

            json.dump(self.data, file_json, ensure_ascii=False, indent=2)


class Interaction_donnees:
    """
    Classe permettant d'interagir avec les donnees du projet (BDD et GeoJSON)
    """
    def __init__(self, bdd_path="data/bdd.db", 
                geojson_path="data/forets_vendee.geojson"):
        """
        Entrees : self:instance de Interaction_donnees
                  bdd_path:str chemin vers le fichier de base de donnees
                  geojson_path:str chemin vers le fichier GeoJSON
        Role : Initialise l'instance, connecte a la BDD et charge le 
               gestionnaire GeoJSON.
        Sortie : Nouvelle instance de Interaction_donnees
        """
        self.bdd = Interaction_bdd(bdd_path)
        self.json_manager = Interaction_json(geojson_path)

    def ajouter_foret(self, nom, stats, polygone):
        """
        Entrees : self:instance de Interaction_donnees
                  nom:str nom de la foret
                  stats:dict dictionnaire contenant les statistiques de la foret
                  (superficie, implan_naturelle, etc.)
                  polygone:list liste de coordonnees (liste de [lat, lon]) 
                  definissant la foret
        Role : Ajoute une nouvelle foret dans la base de donnees et dans le 
               fichier GeoJSON.
        Sortie : int : l'identifiant (id_foret) de la nouvelle foret creee
        """
        # 1. BDD
        # Genere ID (max + 1)
        res = self.bdd.curseur.execute('''
            SELECT MAX(id_foret) FROM FORET
        ''').fetchone()
        new_id = (res[0] + 1) if res and res[0] is not None else 1

        # Prepare les valeurs pour la table FORET
        # Schema: id_foret, nom, nb_visi_par_an, superficie, implan_naturelle, 
        # id_eau, id_espece, id_risque
        valeurs = [
            new_id,
            nom,
            0, # nb_visi_par_an valeur par defaut 0
            stats.get("superficie", 0.0),
            stats.get("implan_naturelle", 1),
            stats.get("id_eau", None),
            stats.get("id_espece", None),
            stats.get("id_risque", None)
        ]
        self.bdd.ajouter_ligne("FORET", valeurs)

        # 2. GeoJSON
        # Interaction_json.creer_feature demande (id, nom, type, coords)
        #coords pour le type Polygon devrait etre [ring] donc [polygone]
        self.json_manager.creer_feature(new_id, nom, "Polygon", [polygone])
        
        return new_id

    def retirer_foret(self, nom):
        """
        Entrees : self:instance de Interaction_donnees
                  nom:str nom de la foret a retirer
        Role : Retire une foret de la base de donnees et du fichier GeoJSON en 
               utilisant son nom.
        Sortie : bool : True si la suppression a reussi, False sinon
        """
        # 1. BDD
        # rechercher_valeur demande [("col", val)]
        forets = self.bdd.rechercher_valeur("FORET", [("nom", nom)], "id_foret")
        if not forets:
            return False
            
        id_foret = forets[0][0]
        self.bdd.supprimer_ligne("FORET", ("id_foret", id_foret))

        # 2. GeoJSON
        self.json_manager.supprimer_foret(id_foret)
        return True

    def rechercher_foret(self, identification):
        """
        Entrees : self:instance de Interaction_donnees
                  identification:tuple (colonne:str, valeur:any) 
                  critere de recherche, ex: ("nom", "NomForet") ou 
                  ("id_foret", 12)
        Role : Recherche une ou des forets dans la base de donnees correspondant
               au critere.
        Sortie : list : liste des tuples correspondant aux lignes trouvees dans 
                        la BDD
        """
        # rechercher_ligne demande [identification]
        return self.bdd.rechercher_ligne("FORET", [identification])

    def ajouter_polygone_foret(self, nom_foret, nouveau_polygone):
        """
        Entrees : self:instance de Interaction_donnees
                  nom_foret:str nom de la foret a laquelle ajouter le polygone
                  nouveau_polygone:list liste de coordonnees definissant le 
                  nouveau polygone a ajouter
        Role : Ajoute un polygone a la geometry d'une foret existante dans le 
               GeoJSON (transforme en MultiPolygon si necessaire).
        Sortie : bool : True si l'ajout a reussi, False sinon
        """
        # Besoin de l'ID pour utiliser Interaction_json
        forets = self.bdd.rechercher_valeur("FORET", [("nom", nom_foret)], 
                                            "id_foret")
        if not forets:

            return False

        id_foret = forets[0][0]

        # Interaction_json.ajouter_a_feature demande (id, coords)
        # Il gere la conversion Polygon->MultiPolygon
        # Il demande les coords pour le NOUVEAU polygone.
        # Si c'est un simple Polygon, les coordonnees sont [ring]. 
        #nouveau_polygone est ring.
        # Donc passer [nouveau_polygone] comme coordonnees du polygone.
        return self.json_manager.ajouter_a_feature(id_foret, [nouveau_polygone])

    def retirer_polygone_foret(self, nom_foret, index_polygone):
        """
        Entrees : self:instance de Interaction_donnees
                  nom_foret:str nom de la foret
                  index_polygone:int index du polygone a retirer (dans le cas 
                  d'un MultiPolygon)
        Role : Retire un polygone specifique d'une foret de type MultiPolygon 
               dans le GeoJSON.
        Sortie : bool : True si le retrait a reussi, False sinon
        """
        # Need ID to find feature in manager's data
        forets = self.bdd.rechercher_valeur("FORET", [("nom", nom_foret)],
                                            "id_foret")
        if not forets:

            return False

        id_foret = forets[0][0]

        target_feature = None
        # Replacement for searching feature without break
        targeted_features = [
            feature for feature in self.json_manager.data['features']
            if feature['properties'].get('id') == id_foret
        ]

        if targeted_features:
            target_feature = targeted_features[0]
        
        if not target_feature:

            return False

        # Fix: Check si geometry existe
        if target_feature["geometry"] is None:
            # La foret n'a pas de polygone
            return False

        geom_type = target_feature["geometry"]["type"]
        coords = target_feature["geometry"]["coordinates"]

        if geom_type == "MultiPolygon":

            if 0 <= index_polygone < len(coords):

                coords.pop(index_polygone)
                # Si seulement 1 restant, on convertit en Polygon, 
                #mais MultiPolygon avec 1 item est valide.
                # On garde simple ou on convertit si len == 1.
                if len(coords) == 1:

                    target_feature["geometry"]["type"] = "Polygon"
                    target_feature["geometry"]["coordinates"] = coords[0]
                    
                self.json_manager.sauvegarder()
                return True
        
        return False