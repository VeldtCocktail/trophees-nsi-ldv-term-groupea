# Projet : SilvaDaVinci
# Auteurs : Mathéo PASQUIER, Maden USSEREAU, Léon RAIFAUD, Charlélie PINEAU

# importation des bibliothèques nécessaires
import sys
import os
import signal
import traceback
import threading
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QTimer

from module_cartes import *
from module_reseau import serveur
from module_bdd import interaction_donnees as indo
from module_affichage import affichage

def gerer_erreur(type, valeur, trb):
    """
    Entrées \\: \n
        type:str : type d'erreur
        valeur:str : valeur de l'erreur
        trb:str : "traceback" de l'erreur
 
    Rôle \\: \n
        Intercepter les exceptions non gérées dans le programme et afficher
        leur type, leur message et leur traceback en console, sans faire
        planter l'application
 
    Sortie \\: \n
        None
    """
    # on affiche le type et le message de l'erreur en console
    print(f"Erreur non gérée : {type.__name__}: {valeur}")
    # on affiche le traceback formaté de l'erreur en console
    print(f"Traceback : {''.join(traceback.format_tb(trb))}")


# on définit gerer_erreur comme la fonction de gestion des exceptions non
# interceptées, en remplacement du comportement par défaut de Python qui
# affiche l'erreur et arrête le programme
sys.excepthook = gerer_erreur

# on active le partage de contexte OpenGL entre les différentes vues Qt, ce qui
# est nécessaire pour que le moteur web QtWebEngine fonctionne correctement
# dans certaines configurations matérielles
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

# debug vaut True si "--debug" est précisé au lancement du programme
debug = "--debug" in sys.argv

# on crée l'instance de l'application Qt, en lui transmettant les arguments
# de la ligne de commande
app = QApplication(sys.argv)

# on ajoute un timer qui cède brièvement la main à Python toutes les 500ms,
# lui permettant de traiter les signaux système que la boucle PyQt bloquerait
timer = QTimer()
timer.start(500)
timer.timeout.connect(lambda: None)

# on définit un gestionnaire pour le signal SIGINT (Ctrl+C) qui ferme
# proprement l'application Qt au lieu d'interrompre brutalement le processus
signal.signal(signal.SIGINT, lambda *args: app.quit())

# on définit les options de Chromium embarqué dans QtWebEngine :
# --no-sandbox désactive le bac à sable
# --force-color-profile=srgb force le profil colorimétrique sRGB pour un rendu
# uniforme des couleurs sur tous les écrans
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox " \
    "--force-color-profile=srgb"

# on active la mise à l'échelle automatique de l'interface en fonction du
# facteur de zoom de l'écran (utile pour les écrans haute résolution)
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

# on démarre le serveur HTTP local dans un thread daemon afin qu'il s'arrête
# automatiquement lorsque le processus principal se termine
threading.Thread(target = serveur.lancer_serveur, daemon = True).start()

# on attend que le serveur HTTP local soit prêt à répondre aux requêtes avant
# de charger la carte dans le moteur web, pour éviter une erreur de connexion
serveur.attendre_serveur(hote = "127.0.0.1")

# on génère la carte HTML initiale centrée sur Montaigu-Vendée, qui sera
# chargée dans le moteur web au démarrage de la fenêtre principale
carte.generer_carte((46.974, -1.314), debug = debug)

# on crée et on affiche la fenêtre principale de l'application
fenetre = affichage.FenetrePrincipale(debug = debug)
fenetre.show()

# on lance la boucle événementielle Qt et on transmet son code de retour à
# sys.exit pour fermer proprement le processus à la fin de l'application
sys.exit(app.exec())