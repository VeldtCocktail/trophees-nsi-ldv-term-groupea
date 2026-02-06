from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit
)
from PyQt5 import QtWebEngineWidgets

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl
from pathlib import Path
import sys
import os
import overpass
from carte import generer_carte

class RequetesOverpass:
    def __init__(self):
        self.api = overpass.API(timeout = 60)

    def zone_verte(self, coords):
        lat, lon = coords

        requete = f"""
        [out:json][timeout:25];
        (
        way["landuse"="forest"](around:0,{lat},{lon});
        way["natural"="wood"](around:0,{lat},{lon});
        way["landcover"="trees"](around:0,{lat},{lon});
        way["natural"="scrub"](around:0,{lat},{lon});
        way["landuse"="orchard"](around:0,{lat},{lon});

        relation["landuse"="forest"](around:0,{lat},{lon});
        relation["natural"="wood"](around:0,{lat},{lon});
        relation["landcover"="trees"](around:0,{lat},{lon});
        relation["natural"="scrub"](around:0,{lat},{lon});
        relation["landuse"="orchard"](around:0,{lat},{lon});
        );
        out body;
        >;
        out skel qt;
        """

        reponse = self.api.get(requete, responseformat='json')

        return reponse


class Pont(QObject):

    def __init__(self, parent):
        self.par = parent

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
        generer_carte(coords, [zone])
        self.view.update()
    
    
app = QApplication(sys.argv)
window = MainWindow()


app.exec()
