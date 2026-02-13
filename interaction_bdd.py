import sqlite3
import json

class Interaction_BDD:
    """
    Classe permettant l'interaction avec le fichier de base de donnees
    """
    def __init__(self, nom_fichier):
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


class Interaction_JSON:
    """
    Classe d'interaction avec le fichier JSON
    """
    def __init__(self, json_path):
        self.json_path = json_path
        with open(json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

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
                "nom": nom
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
        trouve = False
        features = self.data['features']
        nb_features = len(features)
        i = 0
        
        while i < nb_features and not trouve:
            feature = features[i]
            if feature['properties'].get('id') == id_feature:
                trouve = True
            i += 1
        
        if trouve:
            return False
            
        nouvelle_feature = {
            "type": "Feature",
            "properties": {
                "id": id_feature,
                "nom": nom
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
        trouve = False
        features = self.data['features']
        nb_features = len(features)
        i = 0
        
        while i < nb_features and not trouve:
            feature = features[i]
            if feature['properties'].get('id') == id_feature:
                trouve = True
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
            i += 1

        return trouve



    def supprimer_foret(self, id_foret):
        """
        Entree : id_foret:int identifiant de la foret a supprimer
        Role : Supprime une foret du fichier GeoJSON
        """
        self.data['features'] = [
            f for f in self.data['features'] 
            if f['properties'].get('id') != id_foret
        ]
        self.sauvegarder()

    def sauvegarder(self):
        """
        Role : Ecrit les modifications dans le fichier JSON
        """
        with open(self.json_path, 'w', encoding='utf-8') as f:

            json.dump(self.data, f, ensure_ascii=False, indent=2)


class Interaction_Donnees:
    """
    Classe de coordination entre la base de donnees SQL et le fichier JSON
    """
    def __init__(self, db_path, json_path):
        """
        Entrees : db_path: str chemin vers le fichier .db
                  json_path: str chemin vers le fichier .geojson
        Role : Initialise les deux interfaces d'interaction
        """
        self.bdd = Interaction_BDD(db_path)
        self.json = Interaction_JSON(json_path)

    def ajouter_foret(self, id_foret, nom, coords_json, valeurs_sql):
        """
        Entrees : id_foret: int identifiant unique
                  nom: str nom de la foret
                  coords_json: list coordonnees MultiPolygon pour le GeoJSON
                  valeurs_sql: list toutes les valeurs pour la table SQL
        Role : Ajoute une foret dans les deux supports de stockage
        Sortie : True si reussi
        """
        # Ajout dans SQL
        self.bdd.ajouter_ligne("FORET", valeurs_sql)
        # Ajout dans JSON
        self.json.ajouter_foret(id_foret, nom, coords_json)
        
        return True

    def supprimer_foret(self, id_foret):
        """
        Entrees : id_foret: int identifiant de la foret
        Role : Supprime la foret des deux supports
        Sortie : True si reussi
        """
        # Suppression SQL
        self.bdd.supprimer_ligne("FORET", ("id_foret", id_foret))
        # Suppression JSON
        self.json.supprimer_foret(id_foret)

        return True

    def rechercher_foret(self, id_foret):
        """
        Entrees : id_foret: int identifiant
        Role : Recherche les informations dans les deux supports
        Sortie : dict contenant les infos SQL et la geometrie JSON
        """
        res_sql = self.bdd.rechercher_ligne("FORET", (("id_foret", id_foret),))
        feat_json = None
        
        trouve = False
        features = self.json.data['features']
        nb_features = len(features)
        i = 0
        
        while i < nb_features and not trouve:

            feature = features[i]

            if feature['properties'].get('id') == id_foret:

                feat_json = feature
                trouve = True

            i += 1
        
        return {
            "sql": res_sql,
            "json": feat_json
        }


    def modifier_foret_nom(self, id_foret, nouveau_nom):
        """
        Entrees : id_foret: int identifiant
                  nouveau_nom: str nouveau nom
        Role : Modifie le nom dans SQL et JSON
        """
        # Modif SQL
        self.bdd.modifier_ligne("FORET", (("id_foret", id_foret), "nom",
                                         nouveau_nom))
        # Modif JSON
        trouve = False
        features = self.json.data['features']
        nb_features = len(features)
        i = 0
        
        while i < nb_features and not trouve:

            feature = features[i]

            if feature['properties'].get('id') == id_foret:

                feature['properties']['nom'] = nouveau_nom
                trouve = True

            i += 1
            
        self.json.sauvegarder()
        return True


    def rechercher_par_critere(self, table, identification):
        """
        Entrees : table: str nom de la table
                  identification: tuple(tuple(colonne, valeur)) critere
        Role : Recherche dans SQL et renvoie aussi les infos JSON si c'est
               une foret
        Sortie : liste de dicts contenant les donnees SQL et JSON
        """
        resultats_sql = self.bdd.rechercher_ligne(table, identification)
        resultats_complets = []
        
        features = self.json.data['features']
        nb_features = len(features)
        
        for ligne in resultats_sql:
            # On suppose que l'id est en premiere colonne (idx 0) pour FORET
            id_foret = ligne[0]
            info_json = None
            
            trouve = False
            j = 0
            while j < nb_features and not trouve:

                feature = features[j]
                if feature['properties'].get('id') == id_foret:

                    info_json = feature
                    trouve = True
                    
                j += 1
            
            resultats_complets.append({
                "sql": ligne,
                "json": info_json
            })
            
        return resultats_complets


