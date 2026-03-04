# MATHEO MERCI DE REVOIR TON CODE POUR RESPECTER LA PEP 8 -> Noms des variables

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
class Fenetre_Foret(QGroupBox):
    def __init__(self):
        super().__init__("Création d'une forêt")
        self.setFixedWidth(300)

        layout = QVBoxLayout()

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

        layout.addWidget(QLabel("Type d'arbre que l'on trouve le plus"))
        layout.addWidget(self.donnee_arbre)

        
        # Eau
        layout_eau = QHBoxLayout()
        self.eau_oui = QRadioButton("Oui")
        self.eau_non = QRadioButton("Non")
        self.eau_non.setChecked(True)
        self.eau_oui.clicked.connect(self.affichage_type_eau)


        layout_eau.addWidget(QLabel("Eau"))
        layout_eau.addWidget(self.eau_oui)
        layout_eau.addWidget(self.eau_non)

        layout.addLayout(layout_eau)

        self.setLayout(layout)

        layout.addWidget(QLabel("Type d'eau"))
        layout.addWidget(self.donnee_type_eau)

        layout.addWidget(QLabel("Animaux"))
        layout.addWidget(self.donnee_animaux)

        layout.addWidget(QLabel("Champignons"))
        layout.addWidget(self.donnee_champignon)

        layout.addWidget(QLabel("Risques"))
        layout.addWidget(self.donnee_risques)

    def affichage_type_eau(self):
        if self.eau_oui.isChecked():
            self.donnee_type_eau.show()
        else:
            self.donnee_type_eau.hide()


class Fenetre_Supr_Foret(QGroupBox):
    def __init__(self):
        super().__init__("Suppresion forêt")
        self.setFixedWidth(300)

        layout = QVBoxLayout(self)

# MAIN WINDOW
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Carte des forêts")
        self.resize(1200, 700)

        main_layout = QHBoxLayout(self)

        self.nom_foret = indo.ChargerNomForet(
            ['data', 'forets_vendee.geojson']
        )

        # fenetre forêt
        self.fenetre_foret_main = Fenetre_Foret()
        self.fenetre_foret_main.hide()
        self.fenetre_supr_foret_main = Fenetre_Supr_Foret()
        self.fenetre_supr_foret_main.hide()

        # Carte
        self.view = QtWebEngineWidgets.QWebEngineView()
        html = Path("cartes/carte.html").read_text(encoding="utf-8")
        self.view.setHtml(html)

        # Barre gauche
        InterfaceGauche = QVBoxLayout()

        self.recherche = QLineEdit()
        self.recherche.setPlaceholderText("Rechercher une forêt")        
        self.recherche.textChanged.connect(self.chercher_foret)
        self.recherche.setFixedWidth(300)

        BoutonAjouterForet = QPushButton("Ajouter forêt")
        BoutonAjouterForet.clicked.connect(self.AfficherFenetreForetMain)
        BoutonAjouterForet.setFixedWidth(300)


        BoutonSupprimerForet = QPushButton("Supprimer forêt")
        BoutonSupprimerForet.clicked.connect(self.AfficherFenetreSuprForetMain)
        BoutonSupprimerForet.setFixedWidth(300)

        self.ResultatForet = QListWidget()
        self.ResultatForet.setMaximumHeight(200)
        self.ResultatForet.setFrameShape(QListWidget.NoFrame)
        self.ResultatForet.setFixedWidth(300)



        InterfaceGauche.addWidget(self.recherche)
        InterfaceGauche.addWidget(self.ResultatForet)
        InterfaceGauche.addStretch()
        InterfaceGauche.addWidget(BoutonAjouterForet)
        InterfaceGauche.addWidget(BoutonSupprimerForet)

        main_layout.addLayout(InterfaceGauche)
        main_layout.addWidget(self.fenetre_foret_main)
        main_layout.addWidget(self.fenetre_supr_foret_main)
        main_layout.addWidget(self.view)

    def chercher_foret(self, text):
        self.ResultatForet.clear()
        text = text.strip().lower()

        if not text:
            return

        for nom in self.nom_foret:
            if text in nom.lower():
                self.ResultatForet.addItem(nom)

    def AfficherFenetreForetMain(self):
        self.fenetre_supr_foret_main.hide()
        self.fenetre_foret_main.setVisible(not self.fenetre_foret_main.isVisible())

    def AfficherFenetreSuprForetMain(self):
        self.fenetre_foret_main.hide()
        self.fenetre_supr_foret_main.setVisible(not self.fenetre_supr_foret_main.isVisible())
        