import sqlite3
import json

class BaseDeDonnees:
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


class Interaction_json:
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
        for feature in self.data['features']:
            if feature['properties'].get('id') == id_feature:
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


# Avant de recommencer quelconque test sur la bdd, penser a reset la/les
# table(s) affectee(s) avant, afin d'eviter des bugs causes non pas par le code
# mais par l'utilisateur, merci - @Onions/Le G.O.A.T. du gambling 🎰
if __name__ == "__main__":
    print("Debut des tests classe 1...")
    # Test d'ajout de foret
    bdd = BaseDeDonnees("bdd.db")
    bdd.ajouter_ligne("FORET", (1, "Foret de test", 100, 1000, 1, 2, 3, 4))
    input()
    # Test de modification
    bdd.modifier_ligne("FORET", (("id_foret", 1), "nom", "Foret modifiee"))
    input()
    # Et de suppression
    bdd.supprimer_ligne("FORET", ("id_foret", 1))
    print("Fin des tests classe 1...")
