import sqlite3
import json
import os

class BaseDeDonnees:
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

    def fermer(self):
        """
        Role : ferme la connexion avec la base de donnees
        """
        self.connexion.close()

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

    def supprimer_feature(self, id_feature):
        """
        Entrees : id_feature: identifiant de la feature a supprimer
        Role : Supprime une feature du fichier GeoJSON
        Sortie : True si supprimee, False sinon
        """
        trouve = False
        features = self.data['features']
        nb_features = len(features)
        i = 0
        
        while i < nb_features and not trouve:
            feature = features[i]
            if feature['properties'].get('id') == id_feature:
                features.pop(i)
                trouve = True
                self.sauvegarder()
            i += 1
        return trouve

    def retirer_de_feature(self, id_feature, index_polygone):
        """
        Entrees : id_feature: identifiant de la feature a modifier
                  index_polygone: index du polygone a retirer dans la liste
        Role : Retire un polygone d'une feature. S'il ne reste qu'un polygone,
               on retransforme le MultiPolygon en Polygon.
        Sortie : True si retire, False sinon
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
                
                if geometry and geometry['type'] == 'MultiPolygon':
                    coords = geometry['coordinates']
                    if 0 <= index_polygone < len(coords):
                        coords.pop(index_polygone)
                        
                        # Si il n'en reste qu'un, on repasse en Polygon
                        if len(coords) == 1:
                            geometry['type'] = 'Polygon'
                            geometry['coordinates'] = coords[0]
                        elif len(coords) == 0:
                            # Plus de geometrie
                            feature['geometry'] = None
                        
                        self.sauvegarder()
                    else:
                        trouve = False # Index invalide
                elif geometry and geometry['type'] == 'Polygon' and index_polygone == 0:
                    feature['geometry'] = None
                    self.sauvegarder()
                else:
                    trouve = False # Pas de polygone a cet index ou pas le bon type
            i += 1
        return trouve

    def sauvegarder(self):
        """
        Role : Sauvegarde les donnees actuelles dans le fichier JSON
        """
        with open(self.json_path, 'w', encoding='utf-8') as file_json:
            json.dump(self.data, file_json, indent=4)


class Interaction_Donnees:
    """
    Classe de coordination entre la BDD SQLite et le fichier GeoJSON
    """
    def __init__(self, bdd_path, json_path):
        """
        Entrees : bdd_path: chemin vers la base de donnees
                  json_path: chemin vers le fichier GeoJSON
        Role : initialise les deux types d'interaction
        """
        self.bdd = BaseDeDonnees(bdd_path)
        self.json = Interaction_JSON(json_path)

    def ajouter_foret(self, valeurs_bdd, coords_json):
        """
        Entrees : valeurs_bdd: liste des valeurs pour la table FORET
                           (id_foret, nom, nb_visi, superficie, ...)
                  coords_json: coordonnees initiales (Polygon) pour le GeoJSON
        Role : Ajoute une foret dans la BDD et dans le GeoJSON
        """
        # Ajout dans la BDD
        # On suppose que valeurs_bdd est une liste complete correspondant au schema
        self.bdd.ajouter_ligne("FORET", valeurs_bdd)
        
        # Ajout dans le JSON
        id_foret = valeurs_bdd[0]
        nom_foret = valeurs_bdd[1]
        self.json.creer_feature(id_foret, nom_foret, "Polygon", coords_json)

    def supprimer_foret(self, id_foret):
        """
        Entrees : id_foret: identifiant de la foret a supprimer
        Role : Supprime une foret de la BDD et du fichier GeoJSON
        """
        # Suppression BDD
        self.bdd.supprimer_ligne("FORET", ("id_foret", id_foret))
        
        # Suppression JSON
        self.json.supprimer_feature(id_foret)

    def rechercher_foret(self, critere):
        """
        Entrees : critere: tuple (colonne, valeur) pour la recherche
        Role : Recherche des forets dans la BDD correspondant au critere
        Sortie : liste des resultats (lignes de la table FORET)
        """
        return self.bdd.rechercher_ligne("FORET", critere)

    def ajouter_polygone_a_foret(self, id_foret, nouvelles_coords):
        """
        Entrees : id_foret: identifiant de la foret
                  nouvelles_coords: coordonnees du nouveau polygone
        Role : Ajoute une zone (polygone) a une foret existante dans le JSON
        """
        return self.json.ajouter_a_feature(id_foret, nouvelles_coords)

    def retirer_polygone_a_foret(self, id_foret, index_polygone):
        """
        Entrees : id_foret: identifiant de la foret
                  index_polygone: index du polygone a retirer
        Role : Retire une zone (polygone) d'une foret dans le JSON
        """
        return self.json.retirer_de_feature(id_foret, index_polygone)

    def fermer(self):
        """
        Role : ferme les interactions (connexion BDD)
        """
        self.bdd.fermer()


# Avant de recommencer quelconque test sur la bdd, penser a reset la/les
# table(s) affectee(s) avant, afin d'eviter des bugs causes non pas par le code
# mais par l'utilisateur, merci - @Onions/Le G.O.A.T. du gambling 🎰