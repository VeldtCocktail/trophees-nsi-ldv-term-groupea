import sys
import os
import signal
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from module_cartes import *
from module_bdd import interaction_donnees as indo
from module_affichage import affichage

def gerer_erreur(type, valeur, message):
    print(f"Erreur non gérée : {type.__name__}: {valeur}")
    print(f"Traceback : {message}")

sys.excepthook = gerer_erreur
signal.signal(signal.SIGINT, lambda *args: app.quit())
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

carte.generer_carte((46.3930189, -1.480289), debug=True)
app = QApplication(sys.argv)

window = affichage.FenetrePrincipale(debug = True)
window.show()

sys.exit(app.exec())