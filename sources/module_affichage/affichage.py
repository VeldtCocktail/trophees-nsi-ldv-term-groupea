# Projet : ???
# Auteurs : Mathéo Pasquier, Maden Ussereau

# importation des bibliothèques nécessaires
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QGroupBox,
    QLineEdit, QRadioButton, QComboBox, QLabel
)
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl, Qt

from time import time
from pathlib import Path
import os
import copy

from module_bdd import interaction_donnees as indo
from module_overpass import overpass
from module_cartes import carte
from module_reseau import intercepteur


# constante qui associe chaque chaîne de caractères correspondant à un type de
# détail au nom de la table correspondant dans la base de données (BDD)
DICO_TABLES_DETAILS = {
    "arbres": "FORET_ARBRE",
    "anim": "FORET_ANIM",
    "eau": "FORET_EAU",
    "champis": "FORET_CHAMPI",
    "risques": "FORET_RISQUE"
}

# constante qui associe chaque chaîne de caractères correspondant à un type de
# détail au nom du fichier csv correspondant dans le répertoire .\data
DICO_CSV_DETAILS = {
    "arbres":  "bdd_arbres.csv",
    "anim":    "bdd_animaux.csv",
    "champis": "bdd_toad.csv",
    "eau":     "eau.csv",
    "risques": "bdd_risques.csv"
}

# constante qui associe chaque chaîne de caractères correspondant à un type de
# détail à la liste des valeurs possibles de ce détail dans le fichier csv qui
# lui correspond
LISTE_DETAILS = {
    "arbres": indo.charger_donnees_csv(['data', 'bdd_arbres.csv']),
    "anim": indo.charger_donnees_csv(['data', 'bdd_animaux.csv']),
    "champis": indo.charger_donnees_csv(['data', 'bdd_toad.csv']),
    "eau": indo.charger_donnees_csv(['data', 'eau.csv']),
    "risques": indo.charger_donnees_csv(['data', 'bdd_risques.csv'])
}


class GroupeForet(QGroupBox):
    """
    Classe représentant les éléments qui permettent à l'utilisateur d'afficher,
    de modifier, de créer et d'enregistrer une forêt dans la BDD
    """
    
    def __init__(self, fenetre):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
            fenetre:FenetrePrincipale : instance de la classe FenetrePrincipale
                qui instancie cette classe

        Rôle \\: \n
            Initialisation de la classe GroupeForet

        Sortie \\: \n
            None
        """
        # initialisation de la superclasse QGroupBox
        super().__init__("Enregistrer une forêt")

        # on à self.fen l'instance de la fenêtre principale
        self.fen = fenetre

        # on initialise self.dico_foret, qui contiendra lors de l'affichage de
        # cette instance les informations correspondant à la forêt affichée
        self.dico_foret = {"details": {}}

        # on initialise le dictionnaire des détails temporaires, qui contiendra
        # lors de la modification d'une forêt les informations modifiées mais
        # pas encore enregistrées
        self.details_temp = {}

        # on initialise le type des détails affichés à "arbres"
        self.type_details = "arbres"

        # on initialise les listes des polygones à ajouter et à supprimer de la
        # forêt en cours de modification
        self.polygones_temp = []
        self.polygones_a_suppr = []

        # on initialise le mode de sélection à False
        self.mode_sel = False
        
        # on affecte à cette instance l'identifiant groupe-foret
        self.setObjectName('groupe-foret')

        # on appelle la méthode d'initialisation de l'interface de la classe
        self.init_interface()
        
    def init_interface(self):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet

        Rôle \\: \n
            Initialisation de l’interface utilisateur de la classe

        Sortie \\: \n
            None
        """
        # création du layout principal qui contient les éléments de la fenêtre
        layout_principal = QVBoxLayout()

        # on définit l'alignement du texte pour le centrer
        self.setAlignment(Qt.AlignCenter)

        # création de la zone qui contient les informations générales de la
        # forêt si l'utilisateur affiche une forêt déjà existante, ou des zones
        # de texte qui lui permettent de définir ces informations lors de la
        # création d'une forêt
        layout_infos = self.creer_layout_infos()

        # création de la zone qui contient les boutons permettant d'afficher et
        # de modifier les détails de la forêt (arbres, animaux, etc.) ainsi que
        # d'enregistrer une forêt ou d'annuler les modifications apportées
        layout_boutons = self.creer_layout_boutons()

        # création de la zone d'affichage et de modification de la
        # caractéristique sélectionnée (arbres, animaux, etc.)
        layout_details = self.creer_layout_details()

        # on ajoute ces trois zones au layout principal en spécifiant leur
        # facteur d'étirement
        layout_principal.addLayout(layout_infos, 1)
        layout_principal.addLayout(layout_boutons, 3)
        layout_principal.addLayout(layout_details, 5)

        # on définit layout_principal comme le layout du widget correspondant à
        # l'instance de la classe
        self.setLayout(layout_principal)

    def creer_layout_infos(self):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
        
        Rôle \\: \n
            Créer la zone du groupe de modification de forêt qui contient les
            informations principales comme que le nom, la superficie, le nombre
            de visiteurs par an si connu ainsi que l'origine de la forêt
            (naturelle ou articifielle) si connue
        
        Sortie \\: \n
            layout:QVBoxLayout : layout contenant les informations principales
        """
        # on crée une instance de la classe QVBoxLayout() pour représenter une
        # zone verticale dans laquelle on ajoute des éléments
        layout = QVBoxLayout()

        # on crée une zone de texte représentant le nom de la forêt et on lui
        # affecte une texte de remplacement tant qu'elle est vide
        self.nom_foret = QLineEdit()
        self.nom_foret.setPlaceholderText("Nom de la forêt")

        # on fait de même pour la superficie et le nombre de visiteurs par an
        self.superficie = QLineEdit()
        self.superficie.setPlaceholderText("Superficie")

        self.nb_visit = QLineEdit()
        self.nb_visit.setPlaceholderText("Visiteurs / an")

        # on ajoute ces trois zones de texte au layout
        layout.addWidget(self.nom_foret)
        layout.addWidget(self.superficie)
        layout.addWidget(self.nb_visit)

        # puis on renvoie le layout
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

        self.bouton_supprimer = QPushButton()
        self.bouton_supprimer.setText("Supprimer la forêt")
        self.bouton_supprimer.clicked.connect(self.supprimer_foret)
        

        layout.addWidget(self.bouton_sel)
        layout.addWidget(self.bouton_arbres)
        layout.addWidget(self.bouton_anim)
        layout.addWidget(self.bouton_champis)
        layout.addWidget(self.bouton_eau)
        layout.addWidget(self.bouton_risques)
        layout.addWidget(self.bouton_enregistrer)
        layout.addWidget(self.bouton_supprimer)

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

    def recherche_liste(self):
        self.resultat_recherche.clear()
        texte = self.zone_recherche.text().strip().lower()

        if self.type_details in LISTE_DETAILS.keys():
            for elem in LISTE_DETAILS[self.type_details]:
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

        if self.fen.debug: print("Détails temp :", self.details_temp)

        self.details_temp[self.type_details] = []

        for idx in range(self.liste_valeurs.count()):
            elem = self.liste_valeurs.item(idx)
            if self.type_details not in self.details_temp:
                self.details_temp[self.type_details] = [elem.text()]
            else:
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

    def gerer_clic_cartes(self, coord, zoom):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
            coord:tuple[float] : coordonnées du point cliqué
            zoom:int : zoom de la carte au moment du clic
        
        Rôle \\: \n
            Récupère le polygone cliqué, l'ajoute ou le retire de la liste
            des polygones temporaires et l'affiche sur la carte
        
        Sortie \\: \n
            None
        """
        resultat = self.fen.requetes.zone_verte(coord)
        features = resultat.get("features", [])

        if not features:
            if self.fen.debug:
                print("Aucun polygone trouvé")

        else:
            feature = features[0]
            coordonnees = feature["geometry"]["coordinates"]

            if self.coords_deja_dans_temp(coordonnees):
                # était "à ajouter" -> on l'annule
                self.retirer_de_temp(coordonnees)
                if self.fen.debug: print("Polygone retiré de la sélection")

            elif self.coords_deja_dans_suppr(coordonnees):
                # était "à supprimer" -> on annule la suppression
                self.retirer_de_suppr(coordonnees)
                if self.fen.debug: print("Suppression annulée")

            elif self.coords_deja_sauvegardees(coordonnees):
                # est sauvegardé -> on le marque pour suppression
                self.polygones_a_suppr.append(resultat)
                if self.fen.debug: print("Polygon marqué pour suppression")

            else:
                # nouveau -> temporaire
                self.polygones_temp.append(resultat)
                if self.fen.debug: print("Polygone temporaire ajouté")

            self.fen.recharger_carte(coord, zoom)

    def coords_deja_dans_temp(self, coords):
        sous_polys = indo.sous_polygones(coords)
        for elem in self.polygones_temp:
            coords_temp = elem["features"][0]["geometry"]["coordinates"]
            for poly in indo.sous_polygones(coords_temp):
                for sous_poly in sous_polys:
                    if indo.normaliser(poly) == indo.normaliser(sous_poly):
                        return True
        return False
    
    def retirer_de_temp(self, coords):
        sous_polys = indo.sous_polygones(coords)
        liste = []
        for elem in self.polygones_temp:
            coords_temp = elem["features"][0]["geometry"]["coordinates"]
            commun = False
            for poly in indo.sous_polygones(coords_temp):
                for sous_poly in sous_polys:
                    if indo.normaliser(poly) == indo.normaliser(sous_poly):
                        commun = True
            if not commun:
                liste.append(elem)
        self.polygones_temp = copy.deepcopy(liste)

    def coords_deja_sauvegardees(self, coords):
        id_foret = self.dico_foret.get("id")
        if not id_foret:
            return False
        
        infos = self.fen.inter.bdd.rechercher_ligne(
            "FORET", ("id_foret", id_foret)
        )

        id_feature = str(infos[0][1]) if infos else str(id_foret)
        feature = self.fen.inter.rechercher_feature(id_feature)
        if not feature or not feature.get("geometry"):
            return False
        
        geom = feature["geometry"]
        liste_coords = []
        if geom["type"] == "Polygon":
            liste_coords = [geom["coordinates"]]
        elif geom["type"] == "MultiPolygon":
            liste_coords = geom["coordinates"]
        else:
            return False

        for sous_poly in indo.sous_polygones(coords):
            for sous_poly_sauve in liste_coords:
                if indo.normaliser(sous_poly) == indo.normaliser(sous_poly_sauve):
                    return True
                
        return False

    def coords_deja_dans_suppr(self, coords):
        sous_polys = indo.sous_polygones(coords)
        for elem in self.polygones_a_suppr:
            coords_temp = elem["features"][0]["geometry"]["coordinates"]
            for poly in indo.sous_polygones(coords_temp):
                for sous_poly in sous_polys:
                    if indo.normaliser(poly) == indo.normaliser(sous_poly):
                        return True
                    
        return False
    
    def retirer_de_suppr(self, coords):
        sous_polys = indo.sous_polygones(coords)
        liste = []
        for elem in self.polygones_a_suppr:
            coords_temp = elem["features"][0]["geometry"]["coordinates"]
            commun = False
            for poly in indo.sous_polygones(coords_temp):
                for sous_poly in sous_polys:
                    if indo.normaliser(poly) == indo.normaliser(sous_poly):
                        commun = True
            if not commun:
                liste.append(elem)

        self.polygones_a_suppr = copy.deepcopy(liste)

    def enregistrer_foret_bdd(self):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
        
        Rôle \\: \n
            Enregistre la forêt dans la BDD et le GeoJSON. Si un identifiant se
            trouve dans self.dico_foret, on met à jour la forêt existante.
            Sinon, on crée une nouvelle forêt.
        
        Sortie \\: \n
            None
        """
        self.enregistrer_details_temp()
        foret = self.dico_foret
        
        if self.fen.debug: print("Détails temp :", self.details_temp)

        foret["nom"] = self.nom_foret.text().strip()
        foret["superficie"] = float(self.superficie.text() or 0)
        foret["nb_visit"] = float(self.nb_visit.text() or 0)

        if "id" in foret:
            est_nouvelle = False
        else:
            est_nouvelle = True

        if est_nouvelle:
            foret["id"] = round(time() * 10 ** 5)
            valeurs_bdd = [
                foret["id"],
                str(foret["id"]),
                foret["nom"],
                foret["nb_visit"],
                foret["superficie"],
                1
            ]

            self.fen.inter.ajouter_foret(valeurs_bdd, [])
            if self.fen.debug:
                print(f"Nouvelle forêt créée : id : {foret['id']}")
            
        else:
            self.fen.inter.bdd.modifier_ligne(
                "FORET",
                (("id_foret", foret["id"]), "nom", foret["nom"])
            )

            self.fen.inter.bdd.modifier_ligne(
                "FORET",
                (("id_foret", foret["id"]), "superficie", foret["superficie"])
            )

            self.fen.inter.bdd.modifier_ligne(
                "FORET",
                (("id_foret", foret["id"]), "nb_visi_par_an", foret["nb_visit"])
            )

            self.fen.inter.mettre_a_jour_nom_foret(foret["id"], foret["nom"])

        # enregistrement des polygones temporaires
        for elem in self.polygones_temp:
            for feature in elem["features"]:
                geom = feature["geometry"]
                coords = geom["coordinates"]

                if geom["type"] == "Polygon":
                    self.fen.inter.ajouter_polygone_a_foret(
                        foret["id"], coords
                    )

                elif geom["type"] == "MultiPolygon":
                    for sous_coords in coords:
                        self.fen.inter.ajouter_polygone_a_foret(
                            foret["id"], sous_coords
                        )

        self.polygones_temp = []

        # suppression des polygones à supprimer
        for elem in self.polygones_a_suppr:
            for feature in elem["features"]:
                coords_a_suppr = indo.normaliser(
                    feature["geometry"]["coordinates"]
                )

                feat_sauvegardee = self.fen.inter.rechercher_feature_foret(
                    foret["id"]
                )

                if feat_sauvegardee:
                    coords_liste = feat_sauvegardee["geometry"].get(
                        "coordinates", []
                    )

                    for idx in range(len(coords_liste)):
                        if 0 <= idx and idx < len(coords_liste):
                            coords_temp = coords_liste[idx]

                            if indo.normaliser(coords_temp) == coords_a_suppr:
                                self.fen.inter.retirer_polygone_a_foret(
                                    foret["id"], idx
                                )

        self.polygones_a_suppr = []

        for type_detail in LISTE_DETAILS.keys():
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
                    if self.fen.debug: print(
                        f"Recherche de {valeur} dans {chemin_csv} : {resultat}"
                    )

                    if resultat:
                        id_val = resultat[0][0]
                        self.fen.inter.bdd.ajouter_ligne(
                            DICO_TABLES_DETAILS[type_detail],
                            [foret["id"], id_val]
                        )

        self.fen.recharger_carte()
        self.fen.groupe_recherche_foret.init_donnees()
        if self.fen.debug: print("Forêt enregistrée dans la BDD :", foret)

    def supprimer_foret(self):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
    
        Rôle \\: \n
            Supprime la forêt courante de la BDD et du GeoJSON, puis
            réinitialise le groupe et recharge la carte
    
        Sortie \\: \n
            None
        """
        if "id" not in self.dico_foret:
            if self.fen.debug: print("Aucune forêt sélectionnée")
            return
    
        id_foret = self.dico_foret["id"]
    
        # Suppression des tables de détails
        for type_detail in DICO_TABLES_DETAILS.keys():
            self.fen.inter.bdd.supprimer_ligne(
                DICO_TABLES_DETAILS[type_detail],
                ("id_foret", id_foret)
            )
    
        # Suppression dans la BDD et le GeoJSON
        self.fen.inter.supprimer_foret(id_foret)
    
        if self.fen.debug: print(f"Forêt supprimée : id {id_foret}")
    
        # Réinitialisation de l'interface et rechargement de la carte
        self.reinitialiser()
        self.hide()
        self.fen.groupe_recherche_foret.init_donnees()
        self.fen.recharger_carte()

    def mettre_a_jour(self, foret):
        self.dico_foret = foret
        self.mode_sel = False
        self.polygones_temp = []
        self.polygones_a_suppr = []

        self.nom_foret.setText(foret.get("nom", ""))
        self.superficie.setText(str(foret.get("superficie", "")))
        self.nb_visit.setText(str(foret.get("nb_visit", "")))

        self.bouton_supprimer.setEnabled("id" in foret)

        if self.fen.debug: print("Update :", foret)

        self.details_temp = foret.get("details", {})
        if "details" not in foret.keys():
            foret["details"] = {}

        self.liste_valeurs.clear()
        self.type_details = "arbres"
        self.afficher_details()

    def reinitialiser(self):
        self.mettre_a_jour({})

class GroupeRecherche(QGroupBox):
    def __init__(self, fenetre):
        super().__init__("Rechercher une forêt")
        self.fen = fenetre

        self.init_donnees()
        self.init_interface()

    def init_donnees(self):
        if self.fen.debug: print("Chargement des forêts...")
        self.noms_forets = indo.charger_noms_forets(
            ['data', 'forets_vendee.geojson']
        )
        if self.fen.debug: print("Forêts chargées !")

    def init_interface(self):
        layout = QVBoxLayout()

        self.recherche = QLineEdit()
        self.recherche.setPlaceholderText("Rechercher une forêt")        
        self.recherche.textChanged.connect(self.chercher_foret)

        self.resultats_recherche = QListWidget()
        self.resultats_recherche.itemClicked.connect(
            self.afficher_groupe_foret
        )
        self.resultats_recherche.setFrameShape(QListWidget.NoFrame)

        layout.addWidget(self.recherche)
        layout.addWidget(self.resultats_recherche)

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
        if self.resultats_recherche.currentItem():
            
            nom = self.resultats_recherche.currentItem().text()

            foret = self.foret_depuis_nom(nom)

            if not foret:
                return
        
            self.fen.groupe_modif_foret.mettre_a_jour(foret)
            self.fen.recharger_carte()

            self.hide()
            self.fen.groupe_modif_foret.show()

    def foret_depuis_nom(self, nom):
        liste_infos = self.fen.inter.rechercher_foret(("nom", nom))
        if self.fen.debug: print(liste_infos)

        if not liste_infos:
            if self.fen.debug: print(f"Forêt '{nom}' introuvable en BDD")
            return {}

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

        self.debug = debug

        self.requetes = overpass.RequetesOverpass()
        self.inter = indo.InteractionDonnees(
            os.sep.join(["data", "bdd.db"]),
            os.sep.join(["data", "forets_vendee.geojson"]),
            debug
        )
        
        self.view = QtWebEngineWidgets.QWebEngineView()
        self.intercepteur = intercepteur.IntercepteurRequetes()
        profil = QtWebEngineWidgets.QWebEngineProfile.defaultProfile()
        profil.setRequestInterceptor(self.intercepteur)
        profil.setHttpUserAgent(
            "CarteForets/1.0 (educational project)"
        )

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
        self.groupe_recherche_foret.hide()

        # Barre gauche
        interface_gauche = QVBoxLayout()

        bouton_nouveau = QPushButton("+")
        bouton_nouveau.clicked.connect(self.afficher_nouvelle_foret)

        bouton_recherche = QPushButton("?")
        bouton_recherche.clicked.connect(self.afficher_groupe_recherche)

        interface_gauche.addWidget(bouton_nouveau)
        interface_gauche.addWidget(bouton_recherche)
        interface_gauche.addStretch()

        main_layout.addLayout(interface_gauche)
        main_layout.addWidget(self.groupe_recherche_foret)
        main_layout.addWidget(self.groupe_modif_foret)
        main_layout.addWidget(self.view)

    def afficher_nouvelle_foret(self):
        self.groupe_modif_foret.mettre_a_jour({})
        self.groupe_recherche_foret.hide()
        self.groupe_modif_foret.show()

    def afficher_groupe_recherche(self):
        self.groupe_modif_foret.hide()
        self.groupe_recherche_foret.show()

    def gerer_clic(self, coord, zoom):
        lat, lon = coord

        if self.debug:
            print(f'Click reçu en : {lat}, {lon} | Zoom : {zoom}')

        if self.groupe_modif_foret.mode_sel:
            if self.debug: print("Clic enregistré et sélection activée :)")

            self.groupe_modif_foret.gerer_clic_cartes(coord, zoom)

    def recharger_carte(self, coord = None, zoom = 12):
        id_foret = self.groupe_modif_foret.dico_foret.get("id")

        if coord is None:
            if id_foret:
                nom = self.groupe_modif_foret.dico_foret.get("nom", "")
                coord = self.inter.recuperer_centre_foret(nom)

            if coord is None and self.groupe_modif_foret.polygones_temp:
                premier = self.groupe_modif_foret.polygones_temp[0]
                geom = premier["features"][0]["geometry"]["coordinates"]
                if geom and geom[0]:
                    point = geom[0][0]
                    coord = (point[1], point[0])

            if coord is None:
                coord = (46.67, -1.43)

        donnees_temp = self.groupe_modif_foret.polygones_temp
        donnees_suppr = self.groupe_modif_foret.polygones_a_suppr

        donnees_select = []
        if id_foret:
            infos = self.inter.bdd.rechercher_ligne(
                "FORET", ("id_foret", id_foret)
            )

            id_feature = str(infos[0][1]) if infos else str(id_foret)

            feature = self.inter.rechercher_feature(str(id_feature))
            if feature and "geometry" in feature:
                donnees_select = [
                    {"type": "FeatureCollection", "features": [feature]}
                ]

        carte.generer_carte(
            coord, zoom, donnees_temp, donnees_select, donnees_suppr,
            self.debug
        )

        chemin = os.path.abspath(os.sep.join(["cartes", "carte.html"]))
        self.view.load(QUrl.fromLocalFile(chemin))