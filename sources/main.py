import sys
from module_cartes import *
from module_affichage import affichage

carte.generer_carte((46.3930189, -1.480289))
app = affichage.QApplication(sys.argv)
window = affichage.MainWindow()
window.show()
sys.exit(app.exec())