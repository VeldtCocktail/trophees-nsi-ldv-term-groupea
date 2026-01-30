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

class ForestWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent

        layout_principal = QHBoxLayout()
        layout = QVBoxLayout()
        layout_texte = QVBoxLayout()


        self.donnee1 = QLineEdit("")
        self.donnee2 = QLineEdit("")
        self.donnee3 = QLineEdit("")
        self.donnee4 = QLineEdit("")
        self.donnee5 = QLineEdit("")
        self.donnee6 = QLineEdit("")
        self.donnee7 = QLineEdit("")

        layout.addWidget(self.donnee1)
        layout.addWidget(self.donnee2)
        layout.addWidget(self.donnee3)
        layout.addWidget(self.donnee4)
        layout.addWidget(self.donnee5)
        layout.addWidget(self.donnee6)
        layout.addWidget(self.donnee7)


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
        
        self.champ = QLineEdit("")

        ### BOUTON
        bouton_ajouter_foret = QPushButton("Ajouter forêt")
        bouton_ajouter_foret.show()
        bouton_ajouter_foret.clicked.connect(self.creation_foret_fenetre)


        bouton_supprimer_foret = QPushButton("Supprimer forêt")
        bouton_supprimer_foret.show()

        ### GESTION LAYOUT
        layout_boutons.addWidget(self.champ)
        layout_boutons.addWidget(bouton_ajouter_foret)
        layout_boutons.addWidget(bouton_supprimer_foret)

        layout_principal.addLayout(layout_boutons)
        layout_principal.addWidget(view)
        

        self.setLayout(layout_principal)
        self.show()

    def creation_foret_fenetre(self):
        self.fenetre_forets.show()
    
    
app = QApplication(sys.argv)
window = MainWindow()

app.exec()
