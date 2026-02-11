from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QRadioButton, QComboBox, QLabel, QGroupBox, QListWidget
)
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import Qt
from pathlib import Path
import sys
import csv
import json


# FONCTION
def ChargerDonneesCSV(chemin, col=1):
    data = []
    with open(chemin, newline='', encoding="ISO 8859-3") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader, None)
        for row in reader:
            if len(row) > col:
                data.append(row[col])
    return data

def ChargerNomForet(json_path):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    names = []
    for feature in data.get("features", []):
        props = feature.get("properties", {})
        name = props.get("name")
        if name:
            names.append(name)

    return names



# FENETRE FORET
class Fenetre_Foret(QGroupBox):
    def __init__(self):
        super().__init__("🌲 Création d’une forêt")
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        self.donnee_arbre = QComboBox()
        self.donnee_arbre.addItems(ChargerDonneesCSV("data/bdd_arbres.csv"))

        self.donnee_type_eau = QComboBox()
        self.donnee_type_eau.addItems(ChargerDonneesCSV("data/type_eau.csv"))

        self.donnee_animaux = QComboBox()
        self.donnee_animaux.addItems(ChargerDonneesCSV("data/bdd_animaux.csv"))

        self.donnee_champignon = QComboBox()
        self.donnee_champignon.addItems(ChargerDonneesCSV("data/bdd_toad.csv"))

        self.donnee_risques = QComboBox()
        self.donnee_risques.addItems(ChargerDonneesCSV("data/bdd_risques.csv"))

        layout.addWidget(QLabel("🌳 Type d’arbre"))
        layout.addWidget(self.donnee_arbre)

        layout.addWidget(QLabel("💧 Type d’eau"))
        layout.addWidget(self.donnee_type_eau)

        layout.addWidget(QLabel("🐾 Animaux"))
        layout.addWidget(self.donnee_animaux)

        layout.addWidget(QLabel("🍄 Champignons"))
        layout.addWidget(self.donnee_champignon)

        layout.addWidget(QLabel("⚠️ Risques"))
        layout.addWidget(self.donnee_risques)

        # Chasseur
        layout_chasseur = QHBoxLayout()
        self.chasseur_oui = QRadioButton("Oui")
        self.chasseur_non = QRadioButton("Non")
        self.chasseur_non.setChecked(True)

        layout_chasseur.addWidget(QLabel("🔫 Chasseur"))
        layout_chasseur.addWidget(self.chasseur_oui)
        layout_chasseur.addWidget(self.chasseur_non)

        layout.addLayout(layout_chasseur)

        self.setLayout(layout)


# MAIN WINDOW
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Carte des forêts")
        self.resize(1200, 700)

        main_layout = QHBoxLayout(self)

        self.nom_foret = ChargerNomForet("data/forets_vendee.geojson")

        # fentre forêt
        self.fenetre_foret_main = Fenetre_Foret()
        self.fenetre_foret_main.hide()

        # Carte
        self.view = QtWebEngineWidgets.QWebEngineView()
        html = Path("cartes/carte.html").read_text(encoding="utf-8")
        self.view.setHtml(html)

        # Barre gauche
        InterfaceGauche = QVBoxLayout()

        self.recherche = QLineEdit()
        self.recherche.setPlaceholderText("🔍 Rechercher une forêt")        
        self.recherche.textChanged.connect(self.chercher_foret)
        self.recherche.setFixedWidth(300)

        BoutonAjouterForet = QPushButton("➕ Ajouter forêt")
        BoutonAjouterForet.clicked.connect(self.AfficherFenetreForetMain)

        BoutonSupprimerForet = QPushButton("🗑 Supprimer forêt")

        self.ResultatForet = QListWidget()
        self.ResultatForet.setMaximumHeight(200)
        self.ResultatForet.setFrameShape(QListWidget.NoFrame)


        InterfaceGauche.addWidget(self.recherche)
        InterfaceGauche.addWidget(self.ResultatForet)
        InterfaceGauche.addStretch()
        InterfaceGauche.addWidget(BoutonAjouterForet)
        InterfaceGauche.addWidget(BoutonSupprimerForet)

        main_layout.addLayout(InterfaceGauche)
        main_layout.addWidget(self.fenetre_foret_main)
        main_layout.addWidget(self.view)

        self.apply_style()

    def chercher_foret(self, text):
        self.ResultatForet.clear()
        text = text.strip().lower()

        if not text:
            return

        for nom in self.nom_foret:
            if text in nom.lower():
                self.ResultatForet.addItem(nom)

    def AfficherFenetreForetMain(self):
        self.fenetre_foret_main.setVisible(not self.fenetre_foret_main.isVisible())

# STYLE SITE
    def apply_style(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #0d3c21;
                color: #eaeaea;
                font-size: 13px;
            }
            QGroupBox {
                border: 1px solid #444;
                border-radius: 8px;
                margin-top: 10px;
                padding: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QComboBox, QLineEdit {
                background-color: #2b2b2b;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #3a7afe;
                border: none;
                border-radius: 6px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #5a94ff;
            }
        """)


# LANCER
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())