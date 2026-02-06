from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QRadioButton,
    QSlider,
    QComboBox
)
from PyQt5 import QtWebEngineWidgets
from pathlib import Path
import sys
import os
import csv

class ForestWindow(QWidget):

    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent

        layout_principal = QHBoxLayout()
        layout = QVBoxLayout()
        layout_texte = QVBoxLayout()


        self.donnee1 = QLineEdit()

        self.donnee2 = QLineEdit("")

        self.donnee_type_eau = QComboBox()
        with open('data/type_eau.csv', 'r') as file:
            writer = csv.reader(file, delimiter=';')
            next(writer)  # saute la première ligne du CSV
            for row in writer:
                self.row = row[1]
                self.donnee_type_eau.addItems([self.row])

        self.donnee_champignon = QComboBox()
        with open('data/base-de-donnees-champignons.csv', 'r') as file:
            writer = csv.reader(file, delimiter=';')
            next(writer)  # saute la première ligne du CSV
            for row in writer:
                self.row = row[0]
                self.donnee_champignon.addItems([self.row])

        self.donnee5 = QLineEdit("")

        self.donnee6 = QLineEdit("")

        self.donnee7 = QLineEdit("")

        self.chasseur_Oui = QRadioButton("OUI")
        self.chasseur_Non = QRadioButton("NON")
        
        """
        self.text2
        self.text3
        self.text4
        self.text5
        self.text6
        self.text7
        """

        layout.addWidget(self.donnee1)
        layout.addWidget(self.donnee2)
        layout.addWidget(self.donnee_type_eau)
        layout.addWidget(self.donnee_champignon)
        layout.addWidget(self.donnee5)
        layout.addWidget(self.donnee6)
        layout.addWidget(self.donnee7)

        layout.addWidget(self.chasseur_Oui)
        layout.addWidget(self.chasseur_Non)

        """
        layout_texte.addWidget(self.text2)
        layout_texte.addWidget(self.text3)
        layout_texte.addWidget(self.text4)
        layout_texte.addWidget(self.text5)
        layout_texte.addWidget(self.text6)
        layout_texte.addWidget(self.text7)
        """

        layout_principal.addLayout(layout_texte)
        layout_principal.addLayout(layout)

        self.setLayout(layout_principal)

        self.hide()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.fenetre_forets = ForestWindow(self)
        self.setWindowTitle("Affichage carte des forêts")
        
        layout_principal = QHBoxLayout()
        layout_principal.addWidget(self.fenetre_forets)
        layout_boutons = QVBoxLayout()

        view = QtWebEngineWidgets.QWebEngineView()
        # besoin d'être connecté à Internet pour que la carte folium marche
        html = Path("cartes", "carte.html").read_text(encoding="utf8")
        view.setHtml(html)
        

        ### BOUTON
        recherche_foret = QLineEdit("")
        recherche_foret.show()

        bouton_ajouter_foret = QPushButton("Ajouter forêt")
        bouton_ajouter_foret.show()
        bouton_ajouter_foret.clicked.connect(self.creation_foret_fenetre)

        bouton_supprimer_foret = QPushButton("Supprimer forêt")
        bouton_supprimer_foret.show()

        ### GESTION LAYOUT
        layout_boutons.addWidget(recherche_foret)
        layout_boutons.addWidget(bouton_ajouter_foret)
        layout_boutons.addWidget(bouton_supprimer_foret)

        layout_principal.addLayout(layout_boutons)
        layout_principal.addWidget(view)
        

        self.setLayout(layout_principal)
        self.show()

    def creation_foret_fenetre(self):
        self.fenetre_forets.show()

    def index_changed(self, i): # i is an int
        print(i)

    def text_changed(self, s): # s is a str
        print(s)

    def value_changed(self, i):
        print(i)

    def slider_position(self, p):
        print("position", p)
    
    def slider_pressed(self):
        print("slider pressed")

    def slider_released(self):
        print("slider released")
    
    
app = QApplication(sys.argv)
window = MainWindow()

app.exec()