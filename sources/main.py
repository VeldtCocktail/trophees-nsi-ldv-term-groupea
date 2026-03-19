# importation des bibliothèques nécessaires
import sys
import os
import signal
import socket
import time
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

def attendre_serveur(hote="127.0.0.1", port=8000, timeout=5.0, intervalle=0.05):
    """
    Entrées \\: \n
        hote:str : adresse du serveur HTTP local
        port:int : port du serveur HTTP local
        timeout:float : durée maximale d'attente en secondes
        intervalle:float : intervalle entre chaque tentative en secondes
    Rôle \\: \n
        Bloquer jusqu'à ce que le serveur HTTP local soit prêt à accepter des
        connexions, ou jusqu'à expiration du délai d'attente
    Sortie \\: \n
        None
    """
    echeance = time.time() + timeout
    while time.time() < echeance:
        try:
            # on tente une connexion TCP au serveur
            with socket.create_connection((hote, port), timeout=intervalle):
                return  # le serveur répond : on peut continuer
        except OSError:
            # le serveur n'est pas encore prêt : on attend un peu
            time.sleep(intervalle)
    print(f"Avertissement : le serveur {hote}:{port} n'a pas répondu après "
          f"{timeout} s")

sys.excepthook = gerer_erreur
signal.signal(signal.SIGINT, lambda *args: app.quit())
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox " \
    "--force-color-profile=srgb"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

# on démarre le serveur HTTP local dans un thread daemon
threading.Thread(target = serveur.lancer_serveur, daemon = True).start()

# on attend que le serveur soit prêt avant de charger la page dans le WebEngine
attendre_serveur()

carte.generer_carte((46.3930189, -1.480289), debug = True)
app = QApplication(sys.argv)

window = affichage.FenetrePrincipale(debug = True)
window.show()

sys.exit(app.exec())