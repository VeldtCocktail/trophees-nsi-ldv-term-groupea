# importation des bibliothèques nécessaires
import sys
import os
import signal
import traceback
import threading
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from module_cartes import *
from module_reseau import serveur
from module_bdd import interaction_donnees as indo
from module_affichage import affichage

def gerer_erreur(type, valeur, trb):
    """
    Entrées \\: \n
        type:str type d'erreur
        valeur:str : valeur de l'erreur
        trb:str "traceback" de l'erreur
    Rôle \\: \n
        Permet de gérer les erreurs sans faire crash le programme
    Sortie : \\: \n
        None
    """
    # Messages en console
    print(f"Erreur non gérée : {type.__name__}: {valeur}")
    print(f"Traceback : {''.join(traceback.format_tb(trb))}")

sys.excepthook = gerer_erreur
signal.signal(signal.SIGINT, lambda *args: app.quit())
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox " \
    "--force-color-profile=srgb"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

threading.Thread(target = serveur.lancer_serveur, daemon = True).start()

carte.generer_carte((46.3930189, -1.480289), debug = True)
app = QApplication(sys.argv)

window = affichage.FenetrePrincipale(debug = True)
window.show()

sys.exit(app.exec())