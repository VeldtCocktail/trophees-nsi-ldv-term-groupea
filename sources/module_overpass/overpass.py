import requests
from shapely.geometry import shape, Point, Polygon, MultiPolygon

class RequetesOverpass:
    def __init__(self):
        self.compteur = 0
        self.apis = [
            "https://overpass-api.de/api/interpreter",
            "https://maps.mail.ru/osm/tools/overpass/api/interpreter"
        ]

    def zone_verte(self, coords):
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
                timeout=60
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
                        polygons.append([coords_poly])  # chaque polygon doit être [[coords]]

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

            containing = []
            for f in features:
                geom = shape(f["geometry"])

                if geom.contains(pnt):
                    containing.append(f)

            if containing:
                closest = containing[0]
                geom = closest["geometry"]

                # Pour un MultiPolygon, ne garder que le sous-polygone cliqué
                if geom["type"] == "MultiPolygon":
                    for sous_poly in geom["coordinates"]:
                        forme_poly = shape(
                            {"type": "Polygon", "coordinates": sous_poly}
                        )

                        if forme_poly.contains(pnt):
                            closest = {
                                "type": "Feature",
                                "geometry": {
                                    "type": "Polygon",
                                    "coordinates": sous_poly
                                },
                                "properties": {}
                            }

                            return {
                                "type": "FeatureCollection",
                                "features": [closest]
                            }


            else:
                return {"type": "FeatureCollection", "features": []}


            return {"type": "FeatureCollection", "features": [closest]}

        except Exception as e:
            print("Erreur :", e)
            return {"type": "FeatureCollection", "features": []}
