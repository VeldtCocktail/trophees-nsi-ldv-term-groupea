import sqlite3
import os
from .interaction_bdd import Interaction_bdd
from .interaction_json import Interaction_json

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
        for f in self.json_manager.data['features']:

            if f['properties'].get('id') == id_foret:

                target_feature = f
                break
        
        if not target_feature:

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