# Projet : ???
# Auteurs : Mathéo Pasquier, Maden Ussereau

# importation des bibliothèques nécessaires
from time import time
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QGroupBox,
    QLineEdit, QRadioButton, QComboBox, QLabel
)
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl, Qt
from pathlib import Path
import os

from module_bdd import interaction_donnees as indo
from module_overpass import overpass
from module_cartes import carte


DICO_TABLES_DETAILS = {
    "arbres": "FORET_ARBRE",
    "anim": "FORET_ANIM",
    "eau": "FORET_EAU",
    "champis": "FORET_CHAMPI",
    "risques": "FORET_RISQUE"
}

DICO_CSV_DETAILS = {
    "arbres":  "bdd_arbres.csv",
    "anim":    "bdd_animaux.csv",
    "champis": "bdd_toad.csv",
    "eau":     "eau.csv",
    "risques": "bdd_risques.csv"
}


class GroupeForet(QGroupBox):
    """
    Classe représentant les éléments qui permettent à l'utilisateur
    d'enregistrer une forêt
    """
    
    def __init__(self, fenetre, foret = {}):
        """
        Entrées \\: \n
            self:GroupeAjoutForet : instance de la classe
            fenetre:FenetrePrincipale : instance de la classe FenetrePrincipale
                qui instancie cette classe

        Rôle \\: \n
            Initialisation de la classe

        Sortie \\: \n
            None (j’ai vérifié, n’en déplaise à M. Nauleau)
        """
        # initialisation de la superclasse QGroupBox
        super().__init__("Enregistrer une forêt")

        # on initialise le mode de sélection à False
        self.mode_sel = False

        self.type_details = "arbres"
        if "details" in foret:
            self.details_temp = foret["details"]
        else:
            foret["details"] = {}
            self.details_temp = {}

        # on affect fenetre à self.fen
        self.fen = fenetre
        self.dico_foret = foret

        # on affecte à cette instance l'identifiant groupe-foret
        self.setObjectName('groupe-foret')

        self.liste_details = {
            "arbres": indo.charger_donnees_csv(['data', 'bdd_arbres.csv']),
            "anim": indo.charger_donnees_csv(['data', 'bdd_animaux.csv']),
            "champis": indo.charger_donnees_csv(['data', 'bdd_toad.csv']),
            "eau": indo.charger_donnees_csv(['data', 'eau.csv']),
            "risques": indo.charger_donnees_csv(['data', 'bdd_risques.csv'])
        }

        # on appelle la méthode d'initialisation de l'interface
        self.init_interface()
        
    def init_interface(self):
        """
        Entrées \\: \n
            self:GroupeAjoutForet : instance de la classe

        Rôle \\: \n
            Initialisation de l’interface utilisateur de la classe

        Sortie \\: \n
            None
        """
        # création du layout principal qui contient les éléments de la fenêtre
        layout_principal = QVBoxLayout()

        self.setAlignment(Qt.AlignCenter)

        # création de la zone qui contient les informations générales de la
        # forêt si l'utilisateur affiche une forêt déjà existante
        layout_infos = self.creer_layout_infos()

        # création de la zone qui contient les boutons permettant d'afficher et
        # de modifier les détails de la forêt (arbres, animaux, etc.)
        layout_boutons = self.creer_layout_boutons()

        # création de la zone d'affichage et de modification de la
        # caractéristique sélectionnée (arbres, animaux, etc.)
        layout_details = self.creer_layout_details()

        # on ajoute ces trois zones au layout principal en spécifiant leur
        # ratio relatif
        layout_principal.addLayout(layout_infos, 1)
        layout_principal.addLayout(layout_boutons, 3)
        layout_principal.addLayout(layout_details, 3)

        # on définit layout_principal comme le layout du widget correspondant à
        # la classe
        self.setLayout(layout_principal)

    def creer_layout_infos(self):
        """
        """
        layout = QVBoxLayout()

        self.nom_foret = QLineEdit()
        self.nom_foret.setPlaceholderText("Nom de la forêt")

        self.superficie = QLineEdit()
        if self.dico_foret != {} and "superficie" in self.dico_foret:
            self.superficie.setText(str(self.dico_foret["superficie"]))
        self.superficie.setPlaceholderText("Superficie")

        self.nb_visit = QLineEdit()
        self.nb_visit.setPlaceholderText("Visiteurs / an")

        layout.addWidget(self.nom_foret)
        layout.addWidget(self.superficie)
        layout.addWidget(self.nb_visit)

        return layout

    def creer_layout_boutons(self):
        layout = QVBoxLayout()

        # création d'un bouton pour sélectionner une zone verte
        self.bouton_sel = QPushButton()
        # on change le texte du bouton
        self.bouton_sel.setText('Sélection')
        # on exécutera self.changer_mode_sel lors d'un clic sur ce bouton
        self.bouton_sel.clicked.connect(self.changer_mode_sel)

        # on crée un bouton pour afficher et modifier les arbres de la forêt
        self.bouton_arbres = QPushButton()
        self.bouton_arbres.setText("Arbres")
        self.bouton_arbres.clicked.connect(self.afficher_arbres)

        # on crée un bouton pour afficher et modifier les cours et étendues
        # d'eau dans la forêt
        self.bouton_eau = QPushButton()
        self.bouton_eau.setText("Rivières et lacs")
        self.bouton_eau.clicked.connect(self.afficher_eau)

        # on fait de même pour les animaux, les champignons puis les risques
        self.bouton_anim = QPushButton()
        self.bouton_anim.setText("Animaux")
        self.bouton_anim.clicked.connect(self.afficher_anim)

        self.bouton_champis = QPushButton()
        self.bouton_champis.setText("Champignons")
        self.bouton_champis.clicked.connect(self.afficher_champis)

        self.bouton_risques = QPushButton()
        self.bouton_risques.setText("Risques")
        self.bouton_risques.clicked.connect(self.afficher_risques)

        self.bouton_enregistrer = QPushButton()
        self.bouton_enregistrer.setText("Enregistrer")
        self.bouton_enregistrer.clicked.connect(self.enregistrer_foret_bdd)
        

        layout.addWidget(self.bouton_sel)
        layout.addWidget(self.bouton_arbres)
        layout.addWidget(self.bouton_anim)
        layout.addWidget(self.bouton_champis)
        layout.addWidget(self.bouton_eau)
        layout.addWidget(self.bouton_risques)
        layout.addWidget(self.bouton_enregistrer)

        return layout

    def creer_layout_details(self):
        layout = QVBoxLayout()

        self.zone_recherche = QLineEdit()
        self.zone_recherche.setPlaceholderText(self.type_details)
        self.zone_recherche.textChanged.connect(self.recherche_liste)

        self.resultat_recherche = QListWidget()
        self.resultat_recherche.itemClicked.connect(self.ajouter_valeur)

        self.liste_valeurs = QListWidget()
        self.liste_valeurs.itemClicked.connect(self.supprimer_valeur)

        self.afficher_arbres()

        layout.addWidget(self.zone_recherche)
        layout.addWidget(self.resultat_recherche)
        layout.addWidget(self.liste_valeurs)

        return layout


# -----------Fonction liée à recherche_liste -----------

    def recherche_liste(self):
        self.resultat_recherche.clear()
        texte = self.zone_recherche.text().strip().lower()

        if self.type_details in self.liste_details.keys():
            for elem in self.liste_details[self.type_details]:
                if not texte or texte in elem.lower():
                    self.resultat_recherche.addItem(elem)

    def ajouter_valeur(self):
        elem = self.resultat_recherche.currentItem()

        if self.fen.debug: print(elem.text())

        trouve = False
        idx = 0
        while not trouve and idx < self.liste_valeurs.count():
            if elem.text() == self.liste_valeurs.item(idx).text():
                trouve = True
                if self.fen.debug: print("Déjà présent !")

            idx += 1

        if not trouve:
            self.liste_valeurs.addItem(elem.text())
            self.liste_valeurs.update()

    def supprimer_valeur(self):
        idx = self.liste_valeurs.currentRow()

        if idx != -1:
            elem = self.liste_valeurs.takeItem(idx)
            if self.fen.debug: print(elem.text())

        self.enregistrer_details_temp()
        self.liste_valeurs.removeItemWidget(self.liste_valeurs.currentItem())
        self.liste_valeurs.update()


# -----------Fonction affichage des données quand click bouton -----------

    def afficher_arbres(self):
        self.enregistrer_details_temp()
        self.type_details = "arbres"
        self.afficher_details()

    def afficher_eau(self):
        self.enregistrer_details_temp()
        self.type_details = "eau"
        self.afficher_details()

    def afficher_anim(self):
        self.enregistrer_details_temp()
        self.type_details = "anim"
        self.afficher_details()

    def afficher_champis(self):
        self.enregistrer_details_temp()
        self.type_details = "champis"
        self.afficher_details()

    def afficher_risques(self):
        self.enregistrer_details_temp()
        self.type_details = "risques"
        self.afficher_details()

    def afficher_details(self):
        self.zone_recherche.clear()
        self.zone_recherche.setPlaceholderText(self.type_details)
        self.charger_details_temp()
        self.recherche_liste()

    def enregistrer_details_temp(self):
        for idx in range(self.liste_valeurs.count()):
            elem = self.liste_valeurs.item(idx)
            if self.type_details not in self.details_temp:
                self.details_temp[self.type_details] = [elem.text()]
            else:
                list(self.details_temp[self.type_details]).clear()
                if elem.text() not in self.details_temp[self.type_details]:
                    self.details_temp[self.type_details].append(elem.text())

        if self.fen.debug: print("Enregistrement :", self.details_temp)

    def charger_details_temp(self):
        self.liste_valeurs.clear()
        if self.fen.debug: print("Chargement :", self.details_temp)
        if self.type_details in self.details_temp:
            for texte in self.details_temp[self.type_details]:
                self.liste_valeurs.addItem(texte)

    def changer_mode_sel(self):
        self.mode_sel = not self.mode_sel
        print('Sélection : ' + str(self.mode_sel))
        self.enregistrer_details_temp()

    def mettre_a_jour(self, foret):
        self.dico_foret = foret
        self.mode_sel = False
        self.nom_foret.setText(foret.get("nom", ""))
        self.superficie.setText(str(foret.get("superficie", "")))
        self.nb_visit.setText(str(foret.get("nb_visit", "")))

        if "details" in foret:
            self.details_temp = foret["details"]
        else:
            foret["details"] = {}
            self.details_temp = {}

        self.liste_valeurs.clear()
        self.afficher_arbres()

    def enregistrer_foret_bdd(self):
        self.enregistrer_details_temp()
        foret = self.dico_foret

        if "id" not in foret:
            foret["id"] = time()

        for type_detail in self.liste_details.keys():
            self.fen.inter.bdd.supprimer_ligne(
                DICO_TABLES_DETAILS[type_detail],
                ("id_foret", foret["id"])
            )

            if type_detail in self.details_temp:
                for valeur in self.details_temp[type_detail]:
                    chemin_csv = os.sep.join(
                        ["data", DICO_CSV_DETAILS[type_detail]]
                    )
                    resultat = indo.rechercher_dans_csv(
                        chemin_csv, 1, valeur
                    )

                    if resultat:
                        id_val = resultat[0][0]
                        self.fen.inter.bdd.ajouter_ligne(
                            DICO_TABLES_DETAILS[type_detail],
                            [foret["id"], id_val]
                        )


class GroupeRecherche(QGroupBox):
    def __init__(self, fenetre):
        super().__init__("Rechercher une forêt")
        self.fen = fenetre

        if self.fen.debug: print("Chargement des forêts...")
        self.noms_forets = indo.charger_noms_forets(
            ['data', 'forets_vendee.geojson']
        )
        if self.fen.debug: print("Forêts chargées !")

        self.init_interface()

    def init_interface(self):
        layout = QVBoxLayout()

        self.recherche = QLineEdit()
        self.recherche.setPlaceholderText("Rechercher une forêt")        
        self.recherche.textChanged.connect(self.chercher_foret)

        self.resultats_recherche = QListWidget()
        self.resultats_recherche.setFrameShape(QListWidget.NoFrame)

        bouton_modif_foret = QPushButton("Modifier forêt")
        bouton_modif_foret.clicked.connect(self.afficher_groupe_foret)

        layout.addWidget(self.recherche)
        layout.addWidget(self.resultats_recherche)
        layout.addWidget(bouton_modif_foret)

        self.setLayout(layout)

    def chercher_foret(self, text):
        self.resultats_recherche.clear()
        text = text.strip().lower()

        if not text:
            return

        for nom in self.noms_forets:
            if text in nom.lower():
                self.resultats_recherche.addItem(nom)

    def afficher_groupe_foret(self):
        self.fen.groupe_modif_foret.enregistrer_details_temp()

        if self.fen.groupe_modif_foret.isHidden():
            if self.resultats_recherche.currentItem():
                
                nom = self.resultats_recherche.currentItem().text()

                foret = self.foret_depuis_nom(nom)
                self.fen.groupe_modif_foret.mettre_a_jour(foret)

            self.fen.groupe_modif_foret.show()
        else:
            self.fen.groupe_modif_foret.hide()

    def foret_depuis_nom(self, nom):
        liste_infos = self.fen.inter.rechercher_foret(("nom", nom))
        if self.fen.debug: print(liste_infos)

        id_foret = liste_infos[0][0]
        superficie = liste_infos[0][4]

        if superficie == 0.0:
            superficie = self.fen.inter.calculer_superficie_foret(id_foret)
            self.fen.inter.bdd.modifier_ligne(
                "FORET", (("id_foret", id_foret), "superficie", superficie)
            )

        dico_details = self.rechercher_details_foret(id_foret)

        dico = {
            "id": id_foret,
            "nom": nom,
            "superficie": superficie,
            "nb_visit": liste_infos[0][3],
            "implan_natur": True if liste_infos[0][5] == 1 else False,
            "details": dico_details
        }

        if self.fen.debug: print(dico)
        return dico
    
    def rechercher_details_foret(self, id_foret):
        dico_details = {}

        liste_id_arbres = self.fen.inter.bdd.rechercher_valeur(
            "FORET_ARBRE", ("id_foret", id_foret), "id_arbre"
        )
        liste_id_anim = self.fen.inter.bdd.rechercher_valeur(
            "FORET_ANIM", ("id_foret", id_foret), "id_anim"
        )
        liste_id_champis = self.fen.inter.bdd.rechercher_valeur(
            "FORET_CHAMPI", ("id_foret", id_foret), "id_champi"
        )
        liste_id_eau = self.fen.inter.bdd.rechercher_valeur(
            "FORET_EAU", ("id_foret", id_foret), "id_eau"
        )
        liste_id_risques = self.fen.inter.bdd.rechercher_valeur(
            "FORET_RISQUE", ("id_foret", id_foret), "id_risque"
        )
        
        self.ajouter_a_dico(
            dico_details,
            [
                ("arbres", liste_id_arbres, "bdd_arbres.csv"),
                ("anim", liste_id_anim, "bdd_animaux.csv"),
                ("champis", liste_id_champis, "bdd_toad.csv"),
                ("eau", liste_id_eau, "eau.csv"),
                ("risques", liste_id_risques, "bdd_risques.csv")
            ]
        )

        return dico_details

    def ajouter_a_dico(self, dico, liste):
        for ligne in liste:
            
            cle, liste_id, nom_csv = ligne

            chemin_csv = os.sep.join(["data", nom_csv])

            if cle not in dico:
                dico[cle] = []


            for id_tuple in liste_id:
                id_val = str(id_tuple[0])
                resultat = indo.rechercher_dans_csv(chemin_csv, 0, id_val)

                if resultat:
                    dico[cle].append(resultat[0][1])


# Classe principale de l'application
class FenetrePrincipale(QWidget):
    def __init__(self, debug = False):
        super().__init__()

        self.requetes = overpass.RequetesOverpass()
        self.inter = indo.InteractionDonnees(
            os.sep.join(["data", "bdd.db"]),
            os.sep.join(["data", "forets_vendee.geojson"]),
            debug
        )
        self.view = QtWebEngineWidgets.QWebEngineView()
        self.debug = debug

        # Carte
        chemin_html = os.path.abspath(os.sep.join(['cartes', 'carte.html']))
        obj_path = Path(chemin_html).resolve()

        self.view.load(QUrl.fromLocalFile(str(obj_path)))

        self.pont = carte.Pont(self)
        self.channel = QWebChannel()
        self.channel.registerObject("pybridge", self.pont)
        self.view.page().setWebChannel(self.channel)

        self.init_interface()

        with open(os.sep.join(['data', 'style.qss'])) as fichier:
            self.setStyleSheet(fichier.read())

        self.show()

    def init_interface(self):
        self.setWindowTitle("Carte des forêts")
        self.resize(1200, 700)

        main_layout = QHBoxLayout(self)

        # fenetre forêt
        self.groupe_modif_foret = GroupeForet(self)
        self.groupe_modif_foret.hide()

        self.groupe_recherche_foret = GroupeRecherche(self)
        self.groupe_recherche_foret.show()

        # Barre gauche
        interface_gauche = QVBoxLayout()

        #TODO:Boutons "+" et "Recherche"

        main_layout.addLayout(interface_gauche)
        main_layout.addWidget(self.groupe_recherche_foret)
        main_layout.addWidget(self.groupe_modif_foret)
        main_layout.addWidget(self.view)

    def gerer_clic(self, coord, zoom):
        lat, lon = coord

        if self.debug:
            print(f'Click reçu en : {lat}, {lon} | Zoom : {zoom}')

        if self.groupe_modif_foret.mode_sel:
            if self.debug: print("Clic enregistré et sélection activée :)")

            #TODO
            # appeler une méthode de self.groupe_modif_foret équivalente à
            # update_cartes de gestion_clicks.py
