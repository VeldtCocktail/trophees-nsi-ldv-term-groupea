# Projet : SilvaDaVinci
# Auteurs : Mathéo PASQUIER, Maden USSEREAU, Léon RAIFAUD, Charlélie PINEAU

# importation des bibliothèques nécessaires
import requests
from shapely.geometry import shape, Point, Polygon, MultiPolygon, mapping
from shapely.ops import orient


class RequetesOverpass:
    """
    Classe permettant d'exécuter des requêtes vers les API Overpass afin de
    récupérer les données géographiques des zones vertes (forêts, bois, etc.)
    présentes dans OpenStreetMap autour d'un point cliqué sur la carte
    """

    def __init__(self):
        """
        Entrées \\: \n
            self:RequetesOverpass : instance de la classe RequetesOverpass

        Rôle \\: \n
            Initialisation de la classe RequetesOverpass en définissant le
            compteur de requêtes, la liste des URL des API disponibles, les
            en-têtes HTTP à utiliser ainsi que le nombre maximal d'essais

        Sortie \\: \n
            None
        """
        # on initialise un compteur pour alterner entre les API disponibles
        self.compteur = 0

        # on définit la liste des URL des API Overpass à utiliser en rotation
        self.apis = [
            "https://overpass-api.de/api/interpreter",
            "https://maps.mail.ru/osm/tools/overpass/api/interpreter"
        ]

        # on définit les en-têtes HTTP envoyées avec chaque requête, notamment
        # le User-Agent qui identifie l'application (obligation légale)
        self.headers = {
            "User-Agent": "CarteForets/1.0 (contact: lambda.light@proton.me)"
        }

        # on définit le nombre maximum d'essais comme le nombre d'API
        # disponibles, pour pouvoir toutes les tester en cas d'échec
        self.nb_essais = len(self.apis)

    def zone_verte(self, coords, essai = 0):
        """
        Entrées \\: \n
            self:RequetesOverpass : instance de la classe RequetesOverpass
            coords:tuple[float] : latitude et longitude du point cliqué sur la
                carte, sous la forme (lat, lon)
            essai:int : numéro de l'essai en cours, initialisé à 0, utilisé
                pour la récursion en cas d'échec de la requête

        Rôle \\: \n
            Envoyer une requête Overpass pour récupérer les zones vertes
            (forêts, bois, etc.) présentes dans un rayon d'environ 1 km autour
            du point cliqué, puis identifier et renvoyer le polygone qui
            contient ce point parmi les résultats obtenus

        Sortie \\: \n
            dict : FeatureCollection GeoJSON contenant le polygone qui contient
                le point cliqué, ou une FeatureCollection vide si aucun
                polygone n'est trouvé ou en cas d'erreur
        """
        # on récupère la latitude et la longitude depuis le tuple coords
        lat, lon = coords

        # on définit le delta de la bounding box à ~1 km autour du point cliqué
        delta = 0.01  # ~1km bounding box
        min_lat, max_lat = lat - delta, lat + delta
        min_lon, max_lon = lon - delta, lon + delta

        # on construit la requête Overpass en ciblant les types de zones vertes
        # reconnus par OpenStreetMap (forêts, bois, etc)
        query = f"""
        [out:json][timeout:55];
        (
        nwr["landuse"="forest"]({min_lat},{min_lon},{max_lat},{max_lon});
        nwr["natural"="wood"]({min_lat},{min_lon},{max_lat},{max_lon});
        nwr["landcover"="trees"]({min_lat},{min_lon},{max_lat},{max_lon});
        nwr["natural"="scrub"]({min_lat},{min_lon},{max_lat},{max_lon});
        nwr["landuse"="orchard"]({min_lat},{min_lon},{max_lat},{max_lon});
        );
        out geom;
        """
        
        # on incrémente le compteur pour alterner entre les APIs disponibles
        self.compteur += 1

        try:
            # on envoie la requête Overpass en POST à l'API sélectionnée par
            # rotation via le modulo du compteur sur le nombre d'APIs
            requete = requests.post(
                self.apis[self.compteur % len(self.apis)],
                data=query,
                timeout=60,
                headers=self.headers
            )
            # on lève une exception si le code HTTP de la réponse indique une
            # erreur
            requete.raise_for_status()
            # on désérialise le JSON renvoyé par l'API
            data = requete.json()

            # on initialise la liste des features GeoJSON à construire
            features = []
            print('Données :')
            print(data, end = '\n')

            # on parcourt les éléments OSM retournés par la requête
            for elt in data.get("elements", []):

                # traitement des éléments de type "way" (polygones simples)
                if elt["type"] == "way":
                    # on récupère la liste de points de la géométrie de
                    # l'élément
                    geom_list = elt.get("geometry")
                    # on ignore les géométries trop courtes pour former un
                    # polygone
                    if not geom_list or len(geom_list) < 3:
                        continue

                    # on convertit chaque point en tuple (longitude, latitude)
                    # car GeoJSON utilise l'ordre (lon, lat)
                    coords_poly = [(p["lon"], p["lat"]) for p in geom_list]

                    # on construit la feature GeoJSON qui correspond à ce
                    # polygone
                    features.append({
                        "type": "Feature",
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [coords_poly]
                        },
                        "properties": {}
                    })

                # traitement des éléments de type "relation" (multi-polygones)
                elif elt["type"] == "relation":
                    # on récupère les membres de la relation
                    members = elt.get("members", [])
                    # on initialise la liste des polygones qui composent la
                    # relation (multi-polygone)
                    polygons = []

                    # on parcourt chaque membre de la relation
                    for m in members:
                        # on ne traite que les membres dont le rôle est "outer"
                        # (contour extérieur du polygone)
                        if m.get("role") != "outer":
                            continue

                        # on récupère la géométrie du membre
                        geom_list = m.get("geometry")
                        # on ignore les géométries insuffisantes
                        if not geom_list or len(geom_list) < 3:
                            continue

                        # on convertit chaque point en tuple (lon, lat)
                        coords_poly = [(p["lon"], p["lat"]) for p in geom_list]
                        
                        # chaque polygone est enveloppé dans une liste pour
                        # respecter la structure GeoJSON des MultiPolygon
                        polygons.append([coords_poly])

                    # si la relation contient au moins un polygone valide, on
                    # construit la feature GeoJSON de type MultiPolygon
                    if polygons:
                        features.append({
                            "type": "Feature",
                            "geometry": {
                                "type": "MultiPolygon",
                                "coordinates": polygons
                            },
                            "properties": {}
                        })

            # si aucune feature n'a pu être construite, on renvoie une
            # FeatureCollection vide
            if not features:
                return {"type": "FeatureCollection", "features": []}

            print('Features :', features)

            # on crée un objet Point Shapely à partir des coordonnées cliquées
            # en ordre (longitude, latitude) comme attendu par Shapely
            pnt = Point(lon, lat)

            # on cherche parmi toutes les features celles dont le polygone
            # contient le point cliqué par l'utilisateur
            contiennent = []
            for feature in features:
                # on convertit la géométrie GeoJSON en objet Shapely
                geom = shape(feature["geometry"])

                # si le polygone contient le point cliqué, on l'ajoute à la
                # liste
                if geom.contains(pnt):
                    contiennent.append(feature)

            # si au moins une feature contient le point, on prend la première
            if contiennent:
                closest = contiennent[0]
            # si aucune feature ne contient le point (clic sur une zone vide),
            # on renvoie une FeatureCollection vide
            else:
                return {"type": "FeatureCollection", "features": []}

            # traitement spécifique des multi-polygones : on ne conserve que le
            # sous-polygone qui contient effectivement le point cliqué
            if closest["geometry"]["type"] == "MultiPolygon":
                geom_dict = closest["geometry"]
                meilleur = None

                # on cherche d'abord un sous-polygone qui contient strictement
                # le point cliqué (cas normal)
                for sous_poly in geom_dict["coordinates"]:
                    forme_poly = shape(
                        {"type": "Polygon", "coordinates": sous_poly}
                    )
                    if forme_poly.contains(pnt) and meilleur is None:
                        meilleur = sous_poly

                # si aucun sous-polygone ne contient strictement le point (cas
                # d'un clic sur une bordure), on prend le sous-polygone le plus
                # proche du point cliqué
                if meilleur is None:
                    meilleur = min(
                        geom_dict["coordinates"],
                        key=lambda coordonnees: shape(
                            {"type": "Polygon", "coordinates": coordonnees}
                        ).distance(pnt)
                    )

                # on reconstruit la feature en ne gardant que le sous-polygone
                # sélectionné, converti en type Polygon simple
                closest = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": meilleur
                    },
                    "properties": {}
                }

            # normalisation du "winding order" du polygone : les anneaux
            # extérieurs doivent être orientés dans le sens antihoraire pour
            # que Leaflet affiche correctement le polygone sur la carte
            try:
                # on convertit la géométrie GeoJSON en objet Shapely
                geom_shapely = shape(closest["geometry"])
                # on réoriente les anneaux dans le sens antihoraire
                geom_orientee = orient(geom_shapely, sign=1.0)
                # on reconvertit l'objet Shapely en dictionnaire GeoJSON
                closest["geometry"] = mapping(geom_orientee)

            # on affiche une éventuelle erreur
            except Exception as erreur:
                print("Erreur :", erreur)

            # on construit et on renvoie la FeatureCollection finale contenant
            # le seul polygone sélectionné
            resultat = {"type": "FeatureCollection", "features": [closest]}
            return resultat

        except Exception as erreur:
            print("Erreur :", erreur)
            # en cas d'erreur, on réessaie avec l'API suivante si le nombre
            # maximum d'essais n'a pas encore été atteint
            if essai < self.nb_essais:
                return self.zone_verte(coords, essai = essai + 1)
            
            # sinon, on renvoie une FeatureCollection vide
            else:
                return {"type": "FeatureCollection", "features": []}