import json

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
