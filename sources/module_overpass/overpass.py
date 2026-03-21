import requests
from shapely.geometry import shape, Point, Polygon, MultiPolygon, mapping
from shapely.ops import orient

class RequetesOverpass:
    def __init__(self):
        self.compteur = 0
        self.apis = [
            "https://overpass-api.de/api/interpreter",
            "https://maps.mail.ru/osm/tools/overpass/api/interpreter"
        ]
        self.headers = {
            "User-Agent": "CarteForets/1.0 (contact: lambda.light@proton.me)"
        }
        self.nb_essais = len(self.apis)

    def zone_verte(self, coords, essai = 0):
        lat, lon = coords

        delta = 0.01  # ~1km bounding box
        min_lat, max_lat = lat - delta, lat + delta
        min_lon, max_lon = lon - delta, lon + delta

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
        
        self.compteur += 1

        try:
            requete = requests.post(
                self.apis[self.compteur % len(self.apis)],
                data=query,
                timeout=60,
                headers=self.headers
            )
            requete.raise_for_status()
            data = requete.json()

            features = []
            print('Données :')
            print(data, end = '\n')

            for elt in data.get("elements", []):
                if elt["type"] == "way":
                    geom_list = elt.get("geometry")
                    if not geom_list or len(geom_list) < 3:
                        continue

                    coords_poly = [(p["lon"], p["lat"]) for p in geom_list]

                    features.append({
                        "type": "Feature",
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [coords_poly]
                        },
                        "properties": {}
                    })

                elif elt["type"] == "relation":
                    members = elt.get("members", [])
                    polygons = []

                    for m in members:
                        if m.get("role") != "outer":
                            continue

                        geom_list = m.get("geometry")
                        if not geom_list or len(geom_list) < 3:
                            continue

                        coords_poly = [(p["lon"], p["lat"]) for p in geom_list]
                        
                        # chaque polygon doit être [[coords]]
                        polygons.append([coords_poly])

                    if polygons:
                        features.append({
                            "type": "Feature",
                            "geometry": {
                                "type": "MultiPolygon",
                                "coordinates": polygons
                            },
                            "properties": {}
                        })

            if not features:
                return {"type": "FeatureCollection", "features": []}

            print('Features :', features)
            # Pick polygon that contains the click
            pnt = Point(lon, lat)

            # on cherche d'abord un polygone qui contient le clic
            containing = []
            for feature in features:
                geom = shape(feature["geometry"])

                if geom.contains(pnt):
                    containing.append(feature)

            if containing:
                closest = containing[0]
            else:
                return {"type": "FeatureCollection", "features": []}

            # Pour un MultiPolygon, on ne garde que le sous-polygone cliqué
            if closest["geometry"]["type"] == "MultiPolygon":
                geom_dict = closest["geometry"]
                meilleur = None

                # on cherche d'abord un sous-polygone qui contient strictement
                # le point cliqué
                for sous_poly in geom_dict["coordinates"]:
                    forme_poly = shape(
                        {"type": "Polygon", "coordinates": sous_poly}
                    )
                    if forme_poly.contains(pnt) and meilleur is None:
                        meilleur = sous_poly

                # si aucun ne contient strictement le point (clic sur bordure),
                # on prend le sous-polygone le plus proche du clic
                if meilleur is None:
                    meilleur = min(
                        geom_dict["coordinates"],
                        key=lambda coordonnees: shape(
                            {"type": "Polygon", "coordinates": coordonnees}
                        ).distance(pnt)
                    )

                # on crée le dictionnaire à renvoyer
                closest = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": meilleur
                    },
                    "properties": {}
                }

            # normalisation du "winding order" (anneaux extérieurs en sens 
            # antihoraire) pour afficher correctement le polygone
            try:
                geom_shapely = shape(closest["geometry"])
                geom_orientee = orient(geom_shapely, sign=1.0)
                closest["geometry"] = mapping(geom_orientee)

            except Exception as e:
                print("Erreur :", e)

            resultat = {"type": "FeatureCollection", "features": [closest]}
            return resultat

        except Exception as e:
            print("Erreur :", e)
            if essai < self.nb_essais:
                return self.zone_verte(coords, essai = essai + 1)
            else:
                return {"type": "FeatureCollection", "features": []}
