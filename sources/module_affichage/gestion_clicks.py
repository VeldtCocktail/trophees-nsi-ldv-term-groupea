from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit
)
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtWebChannel import QWebChannel
from pathlib import Path
import sys
import os

from module_cartes import *
from module_overpass import *


class MainWindow(QWidget):
    def __init__(self):
        self.requetes = overpass.RequetesOverpass()

        super().__init__()

        self.setWindowTitle("Affichage carte des forêts")
        
        layout_principal = QHBoxLayout()
        layout_boutons = QVBoxLayout()

        self.view = QtWebEngineWidgets.QWebEngineView()
        # besoin d'être connecté à Internet pour que la carte folium marche
        chemin_html = os.path.abspath(os.sep.join(['cartes', 'carte.html']))
        obj_path = Path(chemin_html).resolve()

        self.view.page().profile().clearHttpCache()

        self.view.load(QUrl.fromLocalFile(str(obj_path)))

        self.bridge = carte.Pont(self)
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

    def update_carte(self, coords, zoom):
        zone = self.requetes.zone_verte(coords)
        print(zone["features"])

        carte.generer_carte(coords, zoom, [zone])

        html_path = Path("cartes", "carte.html").resolve()

        self.view.load(QUrl.fromLocalFile(str(html_path)))
    
    