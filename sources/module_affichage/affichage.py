from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QRadioButton, QComboBox, QLabel, QGroupBox, QListWidget
)
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import Qt
from pathlib import Path
import sys

from module_bdd import interaction_donnees as indo

# FENETRE FORET
class Fenetre_foret(QGroupBox):
    def __init__(self):
        super().__init__("Création d'une forêt")

        self.sel = False
        self.init_interface_fenetre_foret()
        
    def init_interface_fenetre_foret(self):
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        self.selectionner = QPushButton()
        self.selectionner.setText('Sélection')
        self.selectionner.clicked.connect(self.selection)

        self.donnee_arbre = QComboBox()
        self.donnee_arbre.addItems(
            indo.ChargerDonneesCSV(["data", "bdd_arbres.csv"])
        )

        self.donnee_type_eau = QComboBox()
        self.donnee_type_eau.addItems(
            indo.ChargerDonneesCSV(["data", "type_eau.csv"])
        )
        self.donnee_type_eau.hide()


        self.donnee_animaux = QComboBox()
        self.donnee_animaux.addItems(
            indo.ChargerDonneesCSV(["data", "bdd_animaux.csv"])
        )

        self.donnee_champignon = QComboBox()
        self.donnee_champignon.addItems(
            indo.ChargerDonneesCSV(["data", "bdd_toad.csv"])
        )

        self.donnee_risques = QComboBox()
        self.donnee_risques.addItems(
            indo.ChargerDonneesCSV(["data", "bdd_risques.csv"])
        )

        layout.addWidget(self.selectionner)

        layout.addWidget(QLabel("Type d'arbre que l'on trouve le plus"))
        layout.addWidget(self.donnee_arbre)

        
        # Eau
        layout_eau = QHBoxLayout()
        self.eau_oui = QRadioButton("Oui")
        self.eau_non = QRadioButton("Non")
        self.eau_non.setChecked(True)
        self.eau_oui.clicked.connect(self.affichage_type_eau)            
        self.eau_non.clicked.connect(self.affichage_type_eau)


        layout_eau.addWidget(QLabel("Eau"))
        layout_eau.addWidget(self.eau_oui)
        layout_eau.addWidget(self.eau_non)

        layout.addLayout(layout_eau)

        self.texte_type_eau = QLabel("Type d'eau")
        self.texte_type_eau.hide()
        layout.addWidget(self.texte_type_eau)
        layout.addWidget(self.donnee_type_eau)

        layout.addWidget(QLabel("Animaux"))
        layout.addWidget(self.donnee_animaux)

        layout.addWidget(QLabel("Champignons"))
        layout.addWidget(self.donnee_champignon)

        layout.addWidget(QLabel("Risques"))
        layout.addWidget(self.donnee_risques)

        self.setLayout(layout)

    def selection(self):
        self.sel = not self.sel
        print('Sélection : ' + str(self.sel))

    def affichage_type_eau(self):
        if self.eau_oui.isChecked():
            self.donnee_type_eau.show()
            self.texte_type_eau.show()
        else:
            self.donnee_type_eau.hide()
            self.texte_type_eau.hide()


class Fenetre_supr_foret(QGroupBox):
    def __init__(self):
        super().__init__("Suppresion forêt")
        self.setFixedWidth(300)

        layout = QVBoxLayout(self)

# MAIN WINDOW
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_interface_main()

    def init_interface_main(self):
        self.setWindowTitle("Carte des forêts")
        self.resize(1200, 700)

        main_layout = QHBoxLayout(self)

        self.nom_foret = indo.ChargerNomForet(
            ['data', 'forets_vendee.geojson']
        )

        # fenetre forêt
        self.fenetre_foret_main = Fenetre_foret()
        self.fenetre_foret_main.hide()
        self.fenetre_supr_foret_main = Fenetre_supr_foret()
        self.fenetre_supr_foret_main.hide()

        # Carte
        self.view = QtWebEngineWidgets.QWebEngineView()
        html = Path("cartes/carte.html").read_text(encoding="utf-8")
        self.view.setHtml(html)

        # Barre gauche
        interface_gauche = QVBoxLayout()

        self.recherche = QLineEdit()
        self.recherche.setPlaceholderText("Rechercher une forêt")        
        self.recherche.textChanged.connect(self.chercher_foret)
        self.recherche.setFixedWidth(300)

        bouton_ajouter_foret = QPushButton("Ajouter forêt")
        bouton_ajouter_foret.clicked.connect(self.afficher_fenetre_foret_main)
        bouton_ajouter_foret.setFixedWidth(300)


        bouton_supprimer_foret = QPushButton("Supprimer forêt")
        bouton_supprimer_foret.clicked.connect(self.afficher_fenetre_supr_foret_main)
        bouton_supprimer_foret.setFixedWidth(300)

        self.resultat_foret = QListWidget()
        self.resultat_foret.setMaximumHeight(200)
        self.resultat_foret.setFrameShape(QListWidget.NoFrame)
        self.resultat_foret.setFixedWidth(300)



        interface_gauche.addWidget(self.recherche)
        interface_gauche.addWidget(self.resultat_foret)
        interface_gauche.addStretch()
        interface_gauche.addWidget(bouton_ajouter_foret)
        interface_gauche.addWidget(bouton_supprimer_foret)

        main_layout.addLayout(interface_gauche)
        main_layout.addWidget(self.fenetre_foret_main)
        main_layout.addWidget(self.fenetre_supr_foret_main)
        main_layout.addWidget(self.view)

    def chercher_foret(self, text):
        self.resultat_foret.clear()
        text = text.strip().lower()

        if not text:
            return

        for nom in self.nom_foret:
            if text in nom.lower():
                self.resultat_foret.addItem(nom)

    def afficher_fenetre_foret_main(self):
        self.fenetre_supr_foret_main.hide()
        self.fenetre_foret_main.show()

    def afficher_fenetre_supr_foret_main(self):
        self.fenetre_foret_main.hide()
        self.fenetre_supr_foret_main.show()