from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QRadioButton,
    QComboBox,
    QLabel
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

        self.donnee_arbre = QComboBox()
        with open('data/bdd_arbres.csv', 'r') as file:
            writer = csv.reader(file, delimiter=';')
            next(writer)  # saute la première ligne du CSV
            for row in writer:
                self.row = row[1]
                self.donnee_arbre.addItems([self.row])

        self.donnee_type_eau = QComboBox()
        with open('data/type_eau.csv', 'r') as file:
            writer = csv.reader(file, delimiter=';')
            next(writer)  # saute la première ligne du CSV
            for row in writer:
                self.row = row[1]
                self.donnee_type_eau.addItems([self.row])

        self.donnee_animaux = QComboBox()
        with open('data/bdd_animaux.csv', 'r') as file:
            writer = csv.reader(file, delimiter=';')
            next(writer)  # saute la première ligne du CSV
            for row in writer:
                self.row = row[1]
                self.donnee_animaux.addItems([self.row])

        self.donnee_champignon = QComboBox()
        with open('data/bdd_toad.csv', 'r') as file:
            writer = csv.reader(file, delimiter=';')
            next(writer)  # saute la première ligne du CSV
            for row in writer:
                self.row = row[1]
                self.donnee_champignon.addItems([self.row])

        self.donnee_risques = QComboBox()
        with open('data/bdd_risques.csv', 'r') as file:
            writer = csv.reader(file, delimiter=';')
            next(writer)  # saute la première ligne du CSV
            for row in writer:
                self.row = row[1]
                self.donnee_risques.addItems([self.row])
        
        layout_chasseur = QHBoxLayout()
        self.txt_chasseur = QLabel("Chasseur :")
        self.chasseur_Oui = QRadioButton("OUI")
        self.chasseur_Non = QRadioButton("NON")

        layout_chasseur.addWidget(self.txt_chasseur)
        layout_chasseur.addWidget(self.chasseur_Oui)
        layout_chasseur.addWidget(self.chasseur_Non)

        layout.addWidget(self.donnee_arbre)
        layout.addWidget(self.donnee_type_eau)
        layout.addWidget(self.donnee_animaux)
        layout.addWidget(self.donnee_champignon)
        layout.addWidget(self.donnee_risques)

        layout.addLayout(layout_chasseur)

        layout_principal.addLayout(layout)
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
    
app = QApplication(sys.argv)
window = MainWindow()

app.exec()