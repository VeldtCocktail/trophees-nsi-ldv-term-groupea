from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit
)
from PyQt5 import QtWebEngineWidgets

from PyQt5.QtCore import QObject, QUrl, pyqtSlot
from PyQt5.QtWebChannel import QWebChannel
from pathlib import Path
import sys
import os
import requests
from shapely.geometry import shape, Point, Polygon, MultiPolygon
from carte import generer_carte

class RequetesOverpass:
    def __init__(self):
        self.compteur = 0
        self.apis = [
            "https://overpass-api.de/api/interpreter",
            "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
            "https://overpass.private.coffee/api/interpreter"
        ]

    def zone_verte(self, coords):
        lat, lon = coords
        delta = 0.01  # ~1km bounding box
        min_lat, max_lat = lat - delta, lat + delta
        min_lon, max_lon = lon - delta, lon + delta

        query = f"""
        [out:json][timeout:25];
        (
        nwr["landuse"="forest"]({min_lat},{min_lon},{max_lat},{max_lon});
        nwr["natural"="wood"]({min_lat},{min_lon},{max_lat},{max_lon});
        nwr["landcover"="trees"]({min_lat},{min_lon},{max_lat},{max_lon});
        nwr["natural"="scrub"]({min_lat},{min_lon},{max_lat},{max_lon});
        nwr["landuse"="orchard"]({min_lat},{min_lon},{max_lat},{max_lon});
        );
        out geom;
        """

        try:
            r = requests.post(
                self.apis[self.compteur % 3],
                data=query,
                timeout=30
            )
            self.compteur += 1
            r.raise_for_status()
            data = r.json()

            features = []

            print(data)
            for el in data.get("elements", []):
                geom_list = el.get("geometry")
                if not geom_list or len(geom_list) < 3:
                    continue  # skip nodes or broken polygons

                coords_poly = [(p["lon"], p["lat"]) for p in geom_list]

                # Make everything GeoJSON compliant
                if el.get("type") == "relation":
                    # MultiPolygon (may still be only one polygon inside)
                    coords_geojson = [coords_poly]  # list of polygons
                    geom_type = "MultiPolygon"
                else:
                    coords_geojson = [coords_poly]  # list of linear rings
                    geom_type = "Polygon"

                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": geom_type,
                        "coordinates": coords_geojson if geom_type == "MultiPolygon" else coords_geojson
                    },
                    "properties": {}
                })

            if not features:
                return {"type": "FeatureCollection", "features": []}

            # Pick polygon that contains the click
            point = Point(lon, lat)
            containing = [f for f in features if shape(f["geometry"]).contains(point)]
            if containing:
                closest = containing[0]
            else:
                print('Aucun polygone ne contient le point')
                return {"type": "FeatureCollection", "features": []}

            return {"type": "FeatureCollection", "features": [closest]}

        except Exception as e:
            print("Erreur Overpass :", e)
            return {"type": "FeatureCollection", "features": []}


class Pont(QObject):

    def __init__(self, parent):
        self.par = parent
        super().__init__(parent)

    @pyqtSlot(float, float)
    def envoyerCoordonnees(self, lat, long):
        print(f'Click enregistré en : {lat}, {long}')
        self.par.update_carte((lat, long))

class MainWindow(QWidget):
    def __init__(self):
        self.requetes = RequetesOverpass()

        super().__init__()

        self.setWindowTitle("Affichage carte des forêts")
        
        layout_principal = QHBoxLayout()
        layout_boutons = QVBoxLayout()

        self.view = QtWebEngineWidgets.QWebEngineView()
        # besoin d'être connecté à Internet pour que la carte folium marche
        html_path = Path("cartes", "carte.html").resolve()

        self.view.setHtml(
            html_path.read_text(encoding="utf8"),
            QUrl.fromLocalFile(str(html_path.parent) + "/")
        )
        
        self.bridge = Pont(self)
        self.channel = QWebChannel()
        self.channel.registerObject("pybridge", self.bridge)
        self.view.page().setWebChannel(self.channel)


        self.champ = QLineEdit("")
        self.champ.show()

        ### BOUTON
        bouton_ajouter_foret = QPushButton("Ajouter forêt")
        bouton_ajouter_foret.show()

        bouton_supprimer_foret = QPushButton("Supprimer forêt")
        bouton_supprimer_foret.show()
        bouton_supprimer_foret.clicked.connect(self.appui_bouton)

        ### GESTION LAYOUT
        layout_boutons.addWidget(self.champ)
        layout_boutons.addWidget(bouton_ajouter_foret)
        layout_boutons.addWidget(bouton_supprimer_foret)

        layout_principal.addLayout(layout_boutons)
        layout_principal.addWidget(self.view)
        

        self.setLayout(layout_principal)
        self.show()

    def appui_bouton(self):
        texte = self.champ.text()
        print(texte)

    def update_carte(self, coords):
        zone = self.requetes.zone_verte(coords)
        print(zone["features"])

        generer_carte(coords, [zone])

        html_path = Path("cartes", "carte.html").resolve()

        self.view.setHtml(
            html_path.read_text(encoding="utf8"),
            QUrl.fromLocalFile(str(html_path.parent) + "/")
        )
    
    
app = QApplication(sys.argv)
window = MainWindow()


app.exec()
