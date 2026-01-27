from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit
)
from PyQt5 import QtWebEngineWidgets
from pathlib import Path
import sys
import os

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Affichage carte des forêts")
        
        layout_principal = QHBoxLayout()
        layout_boutons = QVBoxLayout()

        view = QtWebEngineWidgets.QWebEngineView()
        # besoin d'être connecté à Internet pour que la carte folium marche
        html = Path("cartes", "carte.html").read_text(encoding="utf8")
        view.setHtml(html)
        
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
        layout_principal.addWidget(view)
        

        self.setLayout(layout_principal)
        self.show()

    def appui_bouton(self):
        texte = self.champ.text()
        print(texte)
    
app = QApplication(sys.argv)
window = MainWindow()


app.exec()
