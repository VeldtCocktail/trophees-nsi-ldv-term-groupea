import sys
from module_cartes import *
from module_affichage import affichage, gestion_clicks

carte.generer_carte((46.3930189, -1.480289))

app = affichage.QApplication(sys.argv)

window = affichage.MainWindow(debug = True)
window.show()

sys.exit(app.exec())