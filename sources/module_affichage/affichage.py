# Projet : SilvaDaVinci
# Auteurs : Mathéo PASQUIER, Maden USSEREAU, Léon RAIFAUD, Charlélie PINEAU

# importation des bibliothèques nécessaires
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QGroupBox,
    QLineEdit, QLabel, QMessageBox
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
    "animaux": "FORET_ANIM",
    "eau": "FORET_EAU",
    "champis": "FORET_CHAMPI",
    "risques": "FORET_RISQUE"
}

# constante qui associe chaque chaîne de caractères correspondant à un type de
# détail à l'identifiant de ce détail dans la table de la BDD qui y correspond
DICO_ID_DETAILS = {
    "arbres": "id_arbre",
    "animaux": "id_anim",
    "eau": "id_eau",
    "champis": "id_champi",
    "risques": "id_risque"
}

# constante qui associe chaque chaîne de caractères correspondant à un type de
# détail au nom du fichier csv correspondant dans le répertoire .\data
DICO_CSV_DETAILS = {
    "arbres":  "bdd_arbres.csv",
    "animaux":    "bdd_animaux.csv",
    "champis": "bdd_toad.csv",
    "eau":     "eau.csv",
    "risques": "bdd_risques.csv"
}

# constante qui associe chaque chaîne de caractères correspondant à un type de
# détail à la liste des valeurs possibles de ce détail dans le fichier csv qui
# lui correspond
LISTE_DETAILS = {
    "arbres": indo.charger_donnees_csv(['data', 'bdd_arbres.csv']),
    "animaux": indo.charger_donnees_csv(['data', 'bdd_animaux.csv']),
    "champis": indo.charger_donnees_csv(['data', 'bdd_toad.csv']),
    "eau": indo.charger_donnees_csv(['data', 'eau.csv']),
    "risques": indo.charger_donnees_csv(['data', 'bdd_risques.csv'])
}

# constante qui correspond à une table de traduction, qui permet d'associer à
# chaque caractère "spécial" la ou les lettres qui lui correspondent sans
# accent, tilde, cédille, etc (uniquement les caractères les plus fréquents)
ACCENTS = str.maketrans({
    "à": "a", "â": "a", "ä": "a",
    "é": "e", "è": "e", "ê": "e", "ë": "e",
    "ï": "i", "î": "i", "ì": "i",
    "ò": "o", "ô": "o", "ö": "o",
    "ù": "u", "û": "u", "ü": "u",
    "ñ": "n", "ç": "c", "œ": "oe"
})


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

        # on crée une zone horizontale pour le nom
        layout_nom = QHBoxLayout()
        label_nom = QLabel("Nom")
        label_nom.setObjectName("label-champ")
        self.nom_foret = QLineEdit()
        self.nom_foret.setPlaceholderText("Nom")
        layout_nom.addWidget(label_nom)
        layout_nom.addWidget(self.nom_foret)

        # on crée une zone horizontale pour la superficie
        layout_superficie = QHBoxLayout()
        label_superficie = QLabel("Superficie (ha)")
        label_superficie.setObjectName("label-champ")
        self.superficie = QLineEdit()
        self.superficie.setPlaceholderText("Superficie")
        self.superficie.setReadOnly(True)
        self.calc_superficie = QPushButton("#")
        self.calc_superficie.clicked.connect(self.calculer)
        layout_superficie.addWidget(label_superficie)
        layout_superficie.addWidget(self.superficie)
        layout_superficie.addWidget(self.calc_superficie)

        # on crée une zone horizontale pour les visiteurs
        layout_visit = QHBoxLayout()
        label_visit = QLabel("Visiteurs/an")
        label_visit.setObjectName("label-champ")
        self.nb_visit = QLineEdit()
        self.nb_visit.setPlaceholderText("Visiteurs / an")
        layout_visit.addWidget(label_visit)
        layout_visit.addWidget(self.nb_visit)

        # on ajoute ces zones au layout
        layout.addLayout(layout_nom)
        layout.addLayout(layout_superficie)
        layout.addLayout(layout_visit)

        # puis on renvoie le layout
        return layout

    def creer_layout_boutons(self):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
        
        Rôle \\: \n
            Créer la zone du groupe de modification de forêt qui contient les
            boutons utilisables par l'utilisateur
        
        Sortie \\: \n
            layout:QVBoxLayout : layout contenant les boutons
        """
        # on crée une instance de la classe QVBoxLayout() pour représenter une
        # zone verticale dans laquelle on ajoute des éléments
        layout = QVBoxLayout()

        # création du bouton de sélection de polygones
        self.bouton_sel = QPushButton()
        # on change le texte du bouton
        self.bouton_sel.setText('Sélection')
        self.bouton_sel.setCheckable(True)
        self.bouton_sel.setObjectName("bouton-sel")
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

        # on crée une bouton pour enregistrer les modifications de la forêt
        # dans la base de données
        self.bouton_enregistrer = QPushButton()
        self.bouton_enregistrer.setText("Enregistrer")
        self.bouton_enregistrer.setObjectName("bouton-enregistrer")
        self.bouton_enregistrer.clicked.connect(self.enregistrer_foret_bdd)

        # on crée un bouton pour supprimer la forêt sélectionnée
        self.bouton_supprimer = QPushButton()
        self.bouton_supprimer.setText("Supprimer la forêt")
        self.bouton_supprimer.setObjectName("bouton-supprimer")
        self.bouton_supprimer.clicked.connect(self.supprimer_foret)

        

        # on ajoute tous ces boutons à l'intérieur du layout
        layout.addWidget(self.bouton_sel)
        layout.addWidget(self.bouton_arbres)
        layout.addWidget(self.bouton_anim)
        layout.addWidget(self.bouton_champis)
        layout.addWidget(self.bouton_eau)
        layout.addWidget(self.bouton_risques)
        layout.addWidget(self.bouton_enregistrer)
        layout.addWidget(self.bouton_supprimer)

        # puis on renvoie le layout
        return layout

    def creer_layout_details(self):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
        
        Rôle \\: \n
            Créer la zone du groupe de modification de forêt qui contient les
            zones pour ajouter et supprimer des détails (arbres, animaux, etc)
            pour la forêt sélectionnée ou en cours de création
        
        Sortie \\: \n
            layout:QVBoxLayout : layout contenant la zone de recherche et la
                liste des détails
        """
        # on crée une instance de la classe QVBoxLayout() pour représenter une
        # zone verticale dans laquelle on ajoute des éléments
        layout = QVBoxLayout()

        # on crée une zone de texte dans laquelle l'utilisateur peut saisir
        # le nom de l'arbre/animaux/etc qu'il souhaite ajouter à la forêt
        self.zone_recherche = QLineEdit()
        # on affiche comme texte de remplacement le nom du type de détails
        # sélectionné par l'utilisateur
        self.zone_recherche.setPlaceholderText(self.type_details.upper())
        # lorsque l'utilisateur écrit dans cette zone, on appelle la méthode
        # recherche_liste qui affiche la liste des choix possibles
        self.zone_recherche.textChanged.connect(self.recherche_liste)

        # on crée une zone qui contient la liste des choix possibles de détails
        # qui correspondent au texte entré par l'utilisateur dans la zone de 
        # texte
        self.resultat_recherche = QListWidget()
        # lors d'un clic sur un élément de cette liste, on appelle la méthode
        # qui ajoute cet élément aux détails de la forêt
        self.resultat_recherche.itemClicked.connect(self.ajouter_valeur)

        # on crée une zone qui contient la liste des détails de la forêt
        self.liste_valeurs = QListWidget()
        # lors d'un clic sur un élément de cette liste, on appelle la méthode
        # qui retire cet élément de la liste
        self.liste_valeurs.itemClicked.connect(self.supprimer_valeur)

        # on appelle une fois la méthode afficher_arbres pour afficher par 
        # défaut les arbres présents dans la forêt
        self.afficher_arbres()

        # on ajoute la zone de texte et les deux listes au layout
        layout.addWidget(self.zone_recherche)
        layout.addWidget(self.resultat_recherche)
        layout.addWidget(self.liste_valeurs)

        # puis on renvoie ce layout
        return layout

    def recherche_liste(self):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
        
        Rôle \\: \n
            Rechercher dans la liste des détails d'un certain type le mot écrit
            par l'utilisateur dans la zone de recherche et afficher en dessous
            les résultats qui y correspondent.
        
        Sortie \\: \n
            None
        """
        # on vide la liste des résultats de la recherche de l'utilisateur
        self.resultat_recherche.clear()
        # on récupère le texte saisi par l'utilisateur dans la zone de texte et
        # on y retire les espaces en début et fin de chaîne de caractères avant
        # de le convertir en lettre minuscules et de supprimer les accents
        texte = self.zone_recherche.text().strip().lower().translate(ACCENTS)

        # pour chaque élément de la liste des choix correspondant au type de
        # détail en cours de modification
        for elem in LISTE_DETAILS[self.type_details]:

            # on récupère le nom de cet élément en minuscule et sans accents
            nom = str(elem).strip().lower().translate(ACCENTS)

            # si rien n'est écrit ou que le texte saisi apparait dans le nom de
            # l'élément traité par la boucle
            if not texte or texte in nom:
                # on ajoute cet élément à la liste des résultats
                self.resultat_recherche.addItem(elem)

    def ajouter_valeur(self):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
        
        Rôle \\: \n
            Ajouter la valeur cliquée parmi les résultats de la recherche à la
            liste des détails de la forêt pour le type sélectionné
        
        Sortie \\: \n
            None
        """
        # on récupère l'élément sélectionné parmi les résultats de la recherche
        elem = self.resultat_recherche.currentItem()

        # message en console si debug vaut True
        if self.fen.debug: print(elem.text())

        # on initialise trouve à False et un indice à 0
        trouve = False
        idx = 0

        # tant qu'on n'a pas trouvé l'élément à ajouter dans les détails de la
        # forêt et qu'on n'a pas entièrement parcouru cette liste de détails
        while not trouve and idx < self.liste_valeurs.count():
            # si l'élément qu'on souhaite ajouter est déjà présent
            if elem.text() == self.liste_valeurs.item(idx).text():
                # on change trouve en True
                trouve = True
                # message en console si debug vaut True
                if self.fen.debug: print("Déjà présent !")

            # on incrémente l'indice
            idx += 1

        # si l'élément à ajouter n'est pas déjà présent
        if not trouve:
            # on l'ajoute à la liste des détails de la forêt
            self.liste_valeurs.addItem(elem.text())
            self.liste_valeurs.update()

    def supprimer_valeur(self):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
        
        Rôle \\: \n
            Retirer la valeur cliquée de la liste des détails de la forêt pour
            le type sélectionné
        
        Sortie \\: \n
            None
        """
        if self.fen.debug: print("Détail à supprimer")

        # on récupère l'indice de la ligne des détails de la forêt sélectionnée
        idx = self.liste_valeurs.currentRow()

        # si l'indice existe et est compris entre 0 et le nombre d'éléments de
        # la liste des détails
        if idx is not None and idx > -1 and idx < self.liste_valeurs.count():
            # on retire de la liste l'élément à cet indice en le récupérant
            elem = self.liste_valeurs.takeItem(idx)
            # message en console si debug vaut True
            if self.fen.debug: print("Suppression :", elem.text())

        # on enregistre la modification des détails temporaires de la forêt
        self.enregistrer_details_temp()

    def afficher_arbres(self):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
        
        Rôle \\: \n
            Change le type de détails affichés pour afficher les arbres de la
            forêt
        
        Sortie \\: \n
            None
        """
        # on enregistre les détails temporaires pour le type qui était affiché
        self.enregistrer_details_temp()
        # on définit le type des détails en cours de modification à "arbres"
        self.type_details = "arbres"
        # puis on appelle la méthode d'affichage des détails
        self.afficher_details()

    def afficher_eau(self):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
        
        Rôle \\: \n
            Change le type de détails affichés pour afficher les cours d'eau de
            la forêt
        
        Sortie \\: \n
            None
        """
        # on enregistre les détails temporaires pour le type qui était affiché
        self.enregistrer_details_temp()
        # on définit le type des détails en cours de modification à "eau"
        self.type_details = "eau"
        # puis on appelle la méthode d'affichage des détails
        self.afficher_details()

    def afficher_anim(self):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
        
        Rôle \\: \n
            Change le type de détails affichés pour afficher les animaux de la
            forêt
        
        Sortie \\: \n
            None
        """
        # on enregistre les détails temporaires pour le type qui était affiché
        self.enregistrer_details_temp()
        # on définit le type des détails en cours de modification à "anim"
        self.type_details = "animaux"
        # puis on appelle la méthode d'affichage des détails
        self.afficher_details()

    def afficher_champis(self):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
        
        Rôle \\: \n
            Change le type de détails affichés pour afficher les champignons de
            la forêt
        
        Sortie \\: \n
            None
        """
        # on enregistre les détails temporaires pour le type qui était affiché
        self.enregistrer_details_temp()
        # on définit le type des détails en cours de modification à "champis"
        self.type_details = "champis"
        # puis on appelle la méthode d'affichage des détails
        self.afficher_details()

    def afficher_risques(self):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
        
        Rôle \\: \n
            Change le type de détails affichés pour afficher les risques de la
            forêt
        
        Sortie \\: \n
            None
        """
        # on enregistre les détails temporaires pour le type qui était affiché
        self.enregistrer_details_temp()
        # on définit le type des détails en cours de modification à "risques"
        self.type_details = "risques"
        # puis on appelle la méthode d'affichage des détails
        self.afficher_details()

    def afficher_details(self):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
        
        Rôle \\: \n
            Remplacer le texte de remplacement dans la zone de recherche par le
            type de détail, puis appeler la méthode de chargement des détails
            temporaires de la forêt
        
        Sortie \\: \n
            None
        """
        # on vide la zone de recherche
        self.zone_recherche.clear()
        # on change le texte de remplacement de la zone de recherche pour qu'il
        # corresponde à la valeur de type_details
        self.zone_recherche.setPlaceholderText(self.type_details)
        # on appelle la méthode de chargement des détails temporaires
        self.charger_details_temp()
        # on appelle la méthode de recherche de détail parmi la liste (pour
        # vider la liste des résultats)
        self.recherche_liste()

    def enregistrer_details_temp(self):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
        
        Rôle \\: \n
            Enregistrer des détails temporaires correspondant au type de
            détails sélectionné par l'utilisateur dans le dictionnaire qui
            contient ces détails, self.details_temp
        
        Sortie \\: \n
            None
        """
        # message en console si debug vaut True
        if self.fen.debug: print("Anciens détails :", self.details_temp)

        # on remplace la liste des détails correspondant au type sélectionné
        # par une liste vide
        self.details_temp[self.type_details] = []

        # on parcourt la liste des valeurs correspondant aux détails choisis 
        # par l'utilisateur
        for idx in range(self.liste_valeurs.count()):
            # on récupère l'élément à l'indice actuel
            elem = self.liste_valeurs.item(idx)
            # si l'élément n'est pas déjà dans la liste du dictionnaire qui
            # correspond à la clé self.type_details, on l'y ajoute
            if elem.text() not in self.details_temp[self.type_details]:
                self.details_temp[self.type_details].append(elem.text())

        # message en console si debug vaut True
        if self.fen.debug: print("Enregistrement :", self.details_temp)

    def charger_details_temp(self):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
        
        Rôle \\: \n
            Charger les détails temporaires correspondant au type de détails
            sélectionné par l'utilisateur, qui sont enregistrés dans le
            dictionnaire self.details_temp
        
        Sortie \\: \n
            None
        """
        # on vide la liste des valeurs affichées pour le type de détails choisi
        self.liste_valeurs.clear()

        # message en console si debug vaut True
        if self.fen.debug: print("Chargement :", self.details_temp)

        # si le type de détails est bien une clé du dictionnaire
        if self.type_details in self.details_temp:
            # on parcourt les détails temporaires pour ce type
            for texte in self.details_temp[self.type_details]:
                # en ajoutant chaque détail à la liste des éléments affichés
                self.liste_valeurs.addItem(texte)

    def calculer(self):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
        
        Rôle \\: \n
            Calculer la superficie de la forêt et modifier les lignes dans la
            BDD ainsi que le texte du champ "Superficie"
        
        Sortie \\: \n
            None
        """
        id_foret = self.dico_foret.get('id', None)

        if id_foret:
            superficie = self.fen.inter.calculer_superficie_foret(id_foret)
            self.fen.inter.bdd.modifier_ligne(
                "FORET", (("id_foret", id_foret), "superficie", superficie)
            )
            self.superficie.setText(str(superficie))

    def changer_mode_sel(self):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
        
        Rôle \\: \n
            Changer le mode de sélection (activée/désactivée) lors d'un clic
            sur le bouton de sélection
        
        Sortie \\: \n
            None
        """
        # on remplace la valeur de mode_sel par sa négation booléenne
        self.mode_sel = not self.mode_sel
        
        # on synchronise l'état du bouton avec la variable mode_sel
        self.bouton_sel.setChecked(self.mode_sel)

        # message en console si debug vaut True
        if self.fen.debug: print('Sélection : ' + str(self.mode_sel))

        # on appelle la méthode d'enregistrement des détails temporaires
        self.enregistrer_details_temp()

    def gerer_clic_cartes(self, coord, zoom):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
            coord:tuple[float] : latitude et longitude du point cliqué
            zoom:int : facteur de zoom de la carte au moment du clic
        
        Rôle \\: \n
            Récupère le polygone cliqué, l'ajoute ou le retire de la liste
            des polygones temporaires ou de celle des polygones à supprimer et
            l'affiche sur la carte
        
        Sortie \\: \n
            None
        """
        # on appelle la méthode d'exécution d'une requête overpass pour obtenir
        # le polygone dans lequel l'utilisateur a cliqué
        resultat = self.fen.requetes.zone_verte(coord)
        # on récupère les "features" du résultat renvoyé (structure GeoJSON) ou
        # None si la clé "features" n'est pas présente dans le dictionnaire
        features = resultat.get("features", [])

        # si les features sont vides
        if not features:
            # On affiche une fenêtre popup pour en informer l'utilisateur
            self.fen.msg_box = QMessageBox()
            self.fen.msg_box.setText("Aucun polygone trouvé")
            self.fen.msg_box.show()

            # on affiche un message en console si debug vaut True
            if self.fen.debug:
                print("Aucun polygone trouvé")

        # sinon
        else:
            # on récupère le premier élément de la liste des features
            feature = features[0]
            # on récupère la liste des coordonnées des polygones de la feature
            coordonnees = feature["geometry"]["coordinates"]

            # si les coordonnées sont déjà dans la liste "temporaire"
            if self.coords_deja_dans_temp(coordonnees):
                # le polygone était "à ajouter", on l'annule
                self.retirer_de_temp(coordonnees)
                if self.fen.debug: print("Polygone retiré de la sélection")

            # si les coordonnées sont déjà dans la liste "à supprimer"
            elif self.coords_deja_dans_suppr(coordonnees):
                # le polygone était "à supprimer", on annule la suppression
                self.retirer_de_suppr(coordonnees)
                if self.fen.debug: print("Suppression annulée")

            # si les coordonnées sont déjà enregistrées dans le GeoJSON
            elif self.coords_deja_sauvegardees(coordonnees):
                # le polygone est sauvegardé, on le marque pour suppression
                self.polygones_a_suppr.append(resultat)
                if self.fen.debug: print("Polygon marqué pour suppression")

            # sinon
            else:
                # le polygone est nouveau, on le place dans la liste temporaire
                self.polygones_temp.append(resultat)
                if self.fen.debug: print("Polygone temporaire ajouté")

            # on recharge la carte pour afficher le polygone cliqué en couleur
            self.fen.recharger_carte(coord, zoom)

    def coords_deja_dans_temp(self, coords):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
            coords: list[list[tuple[float]]] : coordonnées du polygone cliqué
        
        Rôle \\: \n
            Déterminer si les coordonnées du polygone cliqué sont présentes
            dans la liste des polygones temporaires
        
        Sortie \\: \n
            bool : présence des coordonnées dans self.polygones_temp
        """
        if self.fen.debug: print("Coordonnées :", coords)

        # on récupère la liste des polygones des coordonnées
        sous_polys = indo.sous_polygones(coords)
        # on parcourt la liste des polygones temporaires
        for elem in self.polygones_temp:
            # on récupère les coordonnées du polygone temporaires
            coords_temp = elem["features"][0]["geometry"]["coordinates"]
            # on parcourt chaque polygone des coordonnées temporaires
            for poly in indo.sous_polygones(coords_temp):
                # on parcourt chaque sous polygone de la liste
                for sous_poly in sous_polys:
                    # si les deux polygones sont égaux, on renvoie True
                    if indo.egaux(poly, sous_poly):
                        return True
                    
        # si on n'a pas trouvé d'égalité de polygones, on renvoie False
        return False
    
    def coords_deja_dans_suppr(self, coords):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
            coords: list[list[tuple[float]]] : coordonnées du polygone cliqué
        
        Rôle \\: \n
            Déterminer si les coordonnées du polygone cliqué sont présentes
            dans la liste des polygones à supprimer
        
        Sortie \\: \n
            bool : présence des coordonnées dans self.polygones_a_suppr
        """
        # même fonctionnement que self.coords_deja_dans_temp

        sous_polys = indo.sous_polygones(coords)
        for elem in self.polygones_a_suppr:
            coords_temp = elem["features"][0]["geometry"]["coordinates"]
            for poly in indo.sous_polygones(coords_temp):
                for sous_poly in sous_polys:
                    if indo.egaux(poly, sous_poly):
                        return True
                    
        return False

    def coords_deja_sauvegardees(self, coords):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
            coords: list[list[tuple[float]]] : coordonnées du polygone cliqué
        
        Rôle \\: \n
            Déterminer si les coordonnées du polygone cliqué sont présentes
            dans la feature de la forêt dans le fichier GeoJSON
        
        Sortie \\: \n
            bool : présence des coordonnées le GeoJSON pour la forêt actuelle
        """
        # on récupère l'identifiant de la forêt actuelle depuis le dictionnaire
        id_foret = self.dico_foret.get("id")

        # on renvoie False si cet identifiant n'existe pas
        if not id_foret:
            return False
        
        # on récupère à partir de cet id la feature de la forêt dans le GeoJSON
        feature = self.fen.inter.rechercher_feature_foret(id_foret)
        # si cette feature n'existe pas ou n'a pas de géométrie
        if not feature or not feature.get("geometry"):
            # on renvoie False
            return False
        
        # on récupère la géométrie de la feature
        geom = feature["geometry"]
        liste_coords = []

        # on récupère la liste des coordonnées du polygone ou du multi-polygone
        if geom["type"] == "Polygon":
            liste_coords = [geom["coordinates"]]
        elif geom["type"] == "MultiPolygon":
            liste_coords = geom["coordinates"]
        else:
            return False

        # on parcourt chaque sous-polygone des coordonnées
        for sous_poly in indo.sous_polygones(coords):
            # on parcourt chaque polygone de la liste de coordonnées construite
            for poly in liste_coords:
                # si les deux polygones sont égaux, on renvoie True
                if indo.egaux(sous_poly, poly):
                    return True
                
        # si on n'a pas trouvé d'égalité, on renvoie False
        return False

    def retirer_de_temp(self, coords):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
            coords: list[list[tuple[float]]] : coordonnées du polygone cliqué
        
        Rôle \\: \n
            Retirer les coordonnées du polygone cliqué de self.polygones_temp
        
        Sortie \\: \n
            None
        """
        # on récupère la liste des sous-polygones des coordonnées coords
        sous_polys = indo.sous_polygones(coords)
        liste = []
        # pour chaque élément de la liste de polygones temporaires
        for elem in self.polygones_temp:
            # on récupère les coordonnées de cet élément
            coords_temp = elem["features"][0]["geometry"]["coordinates"]
            # on initialise commun à False
            commun = False
            # pour chaque polygone des coordonnées temporaires
            for poly in indo.sous_polygones(coords_temp):
                # pour chaque polygone parmi les sous-polygones des coordonnées
                for sous_poly in sous_polys:
                    # si les deux polygones sont égaux
                    if indo.egaux(poly, sous_poly):
                        # commun vaut True
                        commun = True

            # si commun vaut False, l'élément traité doit être retiré des
            # polygones temporaires, donc on l'ajoute à la nouvelle liste
            if not commun:
                liste.append(elem)

        # après avoir tout traité, on remplace les polygones temporaires par
        # la nouvelle liste construite uniquement avec les élément qui doivent
        # y rester
        self.polygones_temp = copy.deepcopy(liste)
    
    def retirer_de_suppr(self, coords):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
            coords: list[list[tuple[float]]] : coordonnées du polygone cliqué
        
        Rôle \\: \n
            Retirer les coordonnées du polygone cliqué de la liste des 
            polygones à supprimer self.polygones_a_suppr
        
        Sortie \\: \n
            None
        """
        # Même fonctionnement que self.retirer_de_temp

        sous_polys = indo.sous_polygones(coords)
        liste = []
        for elem in self.polygones_a_suppr:
            coords_temp = elem["features"][0]["geometry"]["coordinates"]
            commun = False
            for poly in indo.sous_polygones(coords_temp):
                for sous_poly in sous_polys:
                    if indo.egaux(poly, sous_poly):
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
        # on enregistre les détails en cours d'édition dans le dictionnaire
        self.enregistrer_details_temp()

        # on récupère le dictionnaire de la forêt en cours d'édition
        foret = self.dico_foret
        
        # message en console si debug vaut True
        if self.fen.debug: print("Détails temp :", self.details_temp)

        # on récupère les informations de la forêt depuis les zones de texte
        foret["nom"] = self.nom_foret.text().strip()
        if foret["nom"] == "":
            foret["nom"] = "Forêt sans nom"

        # on vérifie que le nom de la forêt ne désigne pas déjà une autre forêt
        for autre_foret in self.fen.groupe_recherche_foret.noms_forets:
            # si le nom est le même
            if foret['nom'] == autre_foret:
                # si l'identifiant est différent
                autre_id = self.fen.groupe_recherche_foret.foret_depuis_nom(
                    foret['nom']
                ).get('id')
                if foret.get('id', -1) != autre_id:
                    # on ajoute un caractère au nom de la forêt actuelle
                    foret['nom'] = foret['nom'] + '*'

                    # on informe l'utilisateur
                    self.fen.msg_box = QMessageBox()
                    self.fen.msg_box.setWindowTitle("Information")
                    self.fen.msg_box.setText(
                        f"Nom déjà présent dans la BDD ! \
                        Modifié en {foret['nom']} !"
                    )
                    self.fen.msg_box.show()

        try:
            foret["superficie"] = float(self.superficie.text())
        except:
            foret["superficie"] = 0.0
        
        try:
            foret["nb_visit"] = float(self.nb_visit.text())
        except:
            foret["nb_visit"] = 0.0

        # on détermine si l'action est une création ou une modification
        if "id" in foret:
            est_nouvelle = False
        else:
            est_nouvelle = True

        # si il s'agit d'une création de forêt
        if est_nouvelle:
            # on crée un identifiant à partir du moment de la création
            foret["id"] = round(time() * 10 ** 5)
            # on liste les valeurs à insérer dans la table FORET de la BDD
            valeurs_bdd = [
                foret["id"],
                str(foret["id"]),
                foret["nom"],
                foret["nb_visit"],
                foret["superficie"],
                1
            ]

            # on appelle la méthode d'enregistrement de la forêt dans les BDD
            self.fen.inter.ajouter_foret(valeurs_bdd, [])
            if self.fen.debug:
                print(f"Nouvelle forêt créée : id : {foret['id']}")
            
        # s'il s'agit d'une modification
        else:
            # on remplace les lignes de la BDD par les nouvelles informations
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
                (
                    ("id_foret", foret["id"]),
                    "nb_visi_par_an", foret["nb_visit"]
                )
            )

            # on appelle la méthode de modification du nom de la forêt dans le
            # fichier GeoJSON
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

                            if indo.egaux(coords_temp, coords_a_suppr):
                                self.fen.inter.retirer_polygone_a_foret(
                                    foret["id"], idx
                                )

        self.polygones_a_suppr = []

        # pour chaque type de détail
        for type_detail in LISTE_DETAILS.keys():
            # on supprime les détails de ce type pour la forêt qu'on modifie
            self.fen.inter.bdd.supprimer_ligne(
                DICO_TABLES_DETAILS[type_detail],
                ("id_foret", foret["id"])
            )

            # on enregistre ensuite les identifiants des détails de ce type
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

        # on recharge la carte pour afficher la forêt créée ou modifiée
        self.fen.recharger_carte()
        # on réinitialise les données du groupe de recherche de forêt avec les
        # informations mises à jour
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
        # On s'assure qu'une forêt soit en cours de modification
        if "id" not in self.dico_foret:
            if self.fen.debug: print("Aucune forêt sélectionnée")
            return
    
        # on récupère l'identifiant de la forêt
        id_foret = self.dico_foret["id"]
    
        # Suppression des occurences de la forêt dans les tables de détails
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
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
            foret:dict[str: any] : dictionnaire de la forêt à afficher
    
        Rôle \\: \n
            Mettre à jour les éléments du groupe de modification de forêt en
            remplaçant ceux affichés par ceux du dictionnaire foret passé en
            paramètre
    
        Sortie \\: \n
            None
        """
        # on modifie la valeur des attributs de la classe
        self.dico_foret = foret
        self.mode_sel = False

        # la sélection est désactivée
        self.bouton_sel.setChecked(False)

        # on vide les listes de polygone à ajouter et à supprimer
        self.polygones_temp = []
        self.polygones_a_suppr = []

        # on remplace le texte des informations par les nouvelles valeurs
        self.nom_foret.setText(foret.get("nom", ""))
        self.superficie.setText(str(foret.get("superficie", "")))
        if foret.get("nb_visit", 0) > 0:
            self.nb_visit.setText(str(foret.get("nb_visit")))
        else:
            self.nb_visit.setText("Inconnu")

        # on active ou désactive les boutons de suppression et de calcul de la
        # superficie en fonction de si on crée ou on modifie une forêt
        self.bouton_supprimer.setEnabled("id" in foret)
        self.calc_superficie.setEnabled("id" in foret)

        # message en console si debug vaut True
        if self.fen.debug: print("Update :", foret)

        # on met à jour les détails
        self.details_temp = foret.get("details", {})
        if "details" not in foret.keys():
            foret["details"] = {}

        # le détail affiché par défaut est la liste des arbres
        self.liste_valeurs.clear()
        self.type_details = "arbres"
        self.afficher_details()

    def reinitialiser(self):
        """
        Entrées \\: \n
            self:GroupeForet : instance de la classe GroupeForet
    
        Rôle \\: \n
            Vider tous les éléments du groupe de modification de forêt grâce à
            un appel de mettre_a_jour auquel on passe un dictionnaire vide en
            paramètre
    
        Sortie \\: \n
            None
        """
        # on appelle la méthode mettre_a_jour en passant un dictionnaire vide
        self.mettre_a_jour({})


class GroupeRecherche(QGroupBox):
    """
    Classe qui implémente le groupe de recherche de forêt par nom ou bien par
    présence d'un détail de n'importe quel type (arbres, animaux, ...)
    """
    
    def __init__(self, fenetre):
        """
        Entrées \\: \n
            self:GroupeRecherche : instance de la classe GroupeRecherche
            fenetre:FenetrePrincipale : instance de la classe FenetrePrincipale
                qui instancie cette classe
        
        Rôle \\: \n
            Initialisation de la classe GroupeRecherche
        
        Sortie \\: \n
            None
        """
        # on initialise la superclasse QGroupBox
        super().__init__("Rechercher une forêt")
        # on enregistre la fenêtre principale comme attribut d'instance
        self.fen = fenetre

        # on initialise les données du groupe puis son interface graphique
        self.init_donnees()
        self.init_interface()

    def init_donnees(self):
        """
        Entrées \\: \n
            self:GroupeRecherche : instance de la classe GroupeRecherche
        
        Rôle \\: \n
            Initialisation des données de la classe GroupeRecherche
        
        Sortie \\: \n
            None
        """
        # on charge la liste des noms des forêts grâce au module BDD
        if self.fen.debug: print("Chargement des forêts...")
        self.noms_forets = indo.charger_noms_forets(
            ['data', 'forets_vendee.geojson']
        )
        if self.fen.debug: print("Forêts chargées !")

    def init_interface(self):
        """
        Entrées \\: \n
            self:GroupeRecherche : instance de la classe GroupeRecherche
        
        Rôle \\: \n
            Initialisation de l'interface de la classe GroupeRecherche
        
        Sortie \\: \n
            None
        """
        # on définit le nom de l'objet PyQt
        self.setObjectName('groupe-foret')

        # on crée un layout vertical qui contiendra tous les éléments
        layout = QVBoxLayout()

        # zone de recherche de forêts
        self.rech_for = QLineEdit()
        self.rech_for.setPlaceholderText("Rechercher une forêt")        
        self.rech_for.textChanged.connect(self.chercher_foret)

        # liste des résultats de la recherche
        self.res_rech_for = QListWidget()
        self.res_rech_for.itemClicked.connect(
            self.afficher_groupe_foret
        )

        # zone de recherche de détails
        self.rech_det = QLineEdit()
        self.rech_det.setPlaceholderText("Rechercher un détail")
        self.rech_det.textChanged.connect(self.chercher_detail)

        # liste des résultats de la recherche
        self.res_rech_det = QListWidget()
        self.res_rech_det.itemClicked.connect(self.chercher_forets_det)

        # on ajoute ces 4 éléments au layout créé
        layout.addWidget(self.rech_for)
        layout.addWidget(self.res_rech_for)
        layout.addWidget(self.rech_det)
        layout.addWidget(self.res_rech_det)

        # puis on définit ce layout comme layout principal de la classe
        self.setLayout(layout)

    def chercher_foret(self, texte):
        """
        Entrées \\: \n
            self:GroupeRecherche : instance de la classe GroupeRecherche
            texte:str : texte qu'on cherche parmi les noms des forêts
        
        Rôle \\: \n
            Mettre à jour la liste des forêts dont le nom contient le texte que
            l'utilisateur a saisi dans la zone de recherche de forêts par leur
            nom
        
        Sortie \\: \n
            None
        """
        # on vide la liste des résultats de recherche
        self.res_rech_for.clear()
        # on retire les majuscules, espaces inutiles et accents du texte saisi
        texte = str(texte).strip().lower().translate(ACCENTS)

        # si le texte est non vide
        if texte:
            # pour chaque nom de forêt dans la liste des noms chargée plus tôt
            for nom in self.noms_forets:
                # si le texte est présent dans le nom
                if texte in nom.strip().lower().translate(ACCENTS):
                    # on ajoute ce nom de forêt à la liste des résultats
                    self.res_rech_for.addItem(nom)

    def afficher_groupe_foret(self):
        """
        Entrées \\: \n
            self:GroupeRecherche : instance de la classe GroupeRecherche
        
        Rôle \\: \n
            Afficher le groupe de modification de la forêt dont le nom a été
            cliqué dans la zone des résultats de la recherche de forêt
        
        Sortie \\: \n
            None
        """
        # si un élément de la liste des résultats de recherche est sélectionné
        if self.res_rech_for.currentItem():
            
            # on récupère le nom cliqué
            nom = self.res_rech_for.currentItem().text()

            # on utilise ce nom pour récupérer le dictionnaire de la forêt qui
            # lui correspond
            foret = self.foret_depuis_nom(nom)

            # si ce dictionnaire n'existe pas, on qutte la méthode
            if foret is None:
                return
        
            # on met à jour le groupe de modification de forêt à partir de la
            # forêt choisie par l'utilisateur
            self.fen.groupe_modif_foret.mettre_a_jour(foret)
            # puis on rechage la carte aux coordonnées de la forêt sélectionnée
            self.fen.recharger_carte()

            # on cache le groupe de recherche
            self.hide()
            # puis on affiche le groupe de modifications
            self.fen.groupe_modif_foret.show()

    def chercher_detail(self, texte):
        """
        Entrées \\: \n
            self:GroupeRecherche : instance de la classe GroupeRecherche
            texte:str : texte qu'on cherche parmi les noms des détails
        
        Rôle \\: \n
            Mettre à jour la liste des détails dont le nom contient le texte
            que l'utilisateur a saisi dans la zone de recherche de détails
        
        Sortie \\: \n
            None
        """
        # on vide la liste des résultats de recherche
        self.res_rech_det.clear()
        # on retire les majuscules, espaces inutiles et accents du texte saisi
        texte = str(texte).strip().lower().translate(ACCENTS)

        # si le texte est non vide
        if texte:
            # pour chaque clé de dictionnaire de détails dans la liste
            for cle_dico in LISTE_DETAILS:
                # pour chaque nom de détail de ce type
                for nom_det in LISTE_DETAILS[cle_dico]:
                    # si le nom du détail contient le texte saisi
                    if texte in nom_det.strip().lower().translate(ACCENTS):
                        # on ajoute le nom du détail à la liste des résultats
                        self.res_rech_det.addItem(nom_det)

    def chercher_forets_det(self):
        """
        Entrées \\: \n
            self:GroupeRecherche : instance de la classe GroupeRecherche
        
        Rôle \\: \n
            Rechercher les forêts pour lesquelles le détail sélectionné parmi
            la liste des résultats de recherche de détail est présent
        
        Sortie \\: \n
            None
        """
        # on récupère le détail cliqué
        detail = self.res_rech_det.currentItem().text()
        # on initialise le type de détail à None
        type_det = None

        # on détermine le type du détail en parcourant les listes
        for cle_dico in LISTE_DETAILS:
            if detail in LISTE_DETAILS[cle_dico]:
                type_det = cle_dico
                if self.fen.debug: print("Type détail :", type_det)

        # si on a trouvé un type au détail
        if type_det:
            # on vide la liste des résultats de recherche de forêt
            self.res_rech_for.clear()

            # on récupère le chemin du fichier csv correspondant à ce type
            chemin_csv = os.sep.join(
                ["data", DICO_CSV_DETAILS[type_det]]
            )

            # on récupère l'identifiant du détail dans le fichier csv
            resultat = indo.rechercher_dans_csv(
                chemin_csv, 1, detail
            )
            id_det = resultat[0][0]

            # on récupère la liste des lignes de la table d'association entre
            # la forêt et le type du détail recherché qui contiennent cet id
            liste_listes_id = self.fen.inter.bdd.rechercher_valeur(
                DICO_TABLES_DETAILS[type_det],
                (DICO_ID_DETAILS[type_det], id_det),
                "id_foret"
            )

            # pour chaque ligne de cette liste
            for elem in liste_listes_id:
                # on récupère l'identifiant de la forêt
                id_foret = elem[0]
                # puis on récupère la liste des forêts qui ont cet identifiant
                foret = self.fen.inter.rechercher_foret(("id_foret", id_foret))
                # puis le nom de la première (et seule) forêt qui a cet id
                nom = foret[0][2]
                # on ajoute enfin ce nom à la liste des résultats de recherche
                self.res_rech_for.addItem(nom)

    def foret_depuis_nom(self, nom):
        """
        Entrées \\: \n
            self:GroupeRecherche : instance de la classe GroupeRecherche
            nom:str : nom de la forêt dont on veut récupérer le dictionnaire
        
        Rôle \\: \n
            Construire à partir du nom d'une forêt le dictionnaire contenant
            ses informations principales et ses détails
        
        Sortie \\: \n
            dict[str: any] : dictionnaire de la forêt qui possède ce nom
        """
        # on récupère la liste des informations de la forêt dans la BDD
        liste_infos = self.fen.inter.rechercher_foret(("nom", nom))
        # message en console si debug vaut True
        if self.fen.debug: print(liste_infos)

        # si la liste d'informations n'existe pas ou est vide
        if not liste_infos:
            # message en console si debug vaut True
            if self.fen.debug: print(f"Forêt '{nom}' introuvable en BDD")
            # on renvoie un dictionnaire vide
            return {}

        # sinon, on récupère l'identifiant de la forêt depuis la liste d'infos
        id_foret = liste_infos[0][0]

        # on calcule la superficie de la forêt à partir de son identifiant
        superficie = self.fen.inter.calculer_superficie_foret(id_foret)

        # on modifie la ligne de la BDD avec la superficie calculée
        self.fen.inter.bdd.modifier_ligne(
            "FORET", (("id_foret", id_foret), "superficie", superficie)
        )

        # on récupère le dictionnaire des détails de la forêt
        dico_details = self.rechercher_details_foret(id_foret)

        # puis on construit le dictionnaire qui contient l'ensemble des infos
        # de la forêt qu'on veut récupérer
        dico = {
            "id": id_foret,
            "nom": nom,
            "superficie": superficie,
            "nb_visit": liste_infos[0][3],
            "implan_natur": True if liste_infos[0][5] == 1 else False,
            "details": dico_details
        }

        # message en console si debug vaut True
        if self.fen.debug: print(dico)

        # on renvoie le dictionnaire construit
        return dico
    
    def rechercher_details_foret(self, id_foret):
        """
        Entrées \\: \n
            self:GroupeRecherche : instance de la classe GroupeRecherche
            id_foret:str : identifiant de la forêt dont on veut créer le
                dictionnaire des détails
        
        Rôle \\: \n
            Construire à partir du nom d'une forêt le dictionnaire contenant
            ses informations principales et ses détails
        
        Sortie \\: \n
            dict[str: any] : dictionnaire des détails de la forêt construit
        """
        # on initialise un dictionnaire vide
        dico_details = {}

        # on liste les détails de la forêt pour chacun des cinq types de détail
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
        
        # on ajoute au dictionnaire les types de détails pour les clés, et pour
        # valeurs les listes des identifiants des détails trouvés dans la forêt
        indo.ajouter_a_dico(
            dico_details,
            [
                ("arbres", liste_id_arbres, "bdd_arbres.csv"),
                ("animaux", liste_id_anim, "bdd_animaux.csv"),
                ("champis", liste_id_champis, "bdd_toad.csv"),
                ("eau", liste_id_eau, "eau.csv"),
                ("risques", liste_id_risques, "bdd_risques.csv")
            ]
        )

        # on renvoie le dictionnaire de détails construit
        return dico_details


class FenetrePrincipale(QWidget):
    """
    Classe de la fenêtre principale de l'application, qui contient les groupes
    de modification et de recherche ainsi que la carte dans un navigateur
    """

    def __init__(self, debug = False):
        """
        Entrées \\: \n
            self:FenetrePrincipale : instance de la classe FenetrePrincipale
            debug:bool : messages de debug en console
        
        Rôle \\: \n
            Initialisation de la classe FenetrePrincipale
        
        Sortie \\: \n
            None
        """
        # on initialise la superclasse QWidget
        super().__init__()

        # on affecte debug à un attribut d'instance
        self.debug = debug

        # on crée une instance de la classe RequetesOverpass
        self.requetes = overpass.RequetesOverpass()

        # on crée une instance de la classe InteractionDonnees
        self.inter = indo.InteractionDonnees(
            os.sep.join(["data", "bdd.db"]),
            os.sep.join(["data", "forets_vendee.geojson"]),
            debug
        )
        
        # on crée un moteur web à partir de la classe QWebEngineView de PyQt
        self.moteur = QtWebEngineWidgets.QWebEngineView()

        # on crée une instance de la classe IntercepteurRequetes
        self.intercepteur = intercepteur.IntercepteurRequetes(self, self.debug)

        # on crée le profil utilisé par le navigateur
        profil = QtWebEngineWidgets.QWebEngineProfile.defaultProfile()
        # on définit l'intercepteur de requêtes lié à ce profil
        profil.setUrlRequestInterceptor(self.intercepteur)
        # on définit l'agent utilisé pour les requêtes HTTP (nécessité légale)
        profil.setHttpUserAgent(
            "DaVinciMap/1.0 (educational project)"
        )

        # on crée une instance de la classe Pont pour communiquer avec le JS
        self.pont = carte.Pont(self)
        # on crée une chaîne web pour permettre la communication JavaScript
        self.chaine = QWebChannel()
        # on enregistre le pont créé pour la chaîne
        self.chaine.registerObject("pybridge", self.pont)

        # on crée la page du moteur web de PyQt en appliquant le profil créé
        page = QtWebEngineWidgets.QWebEnginePage(profil, self.moteur)
        # on définit la chaîne web créée comme la chaîne web de cette page
        page.setWebChannel(self.chaine)
        # puis on définit cette page comme celle du moteur web
        self.moteur.setPage(page)

        # on charge depuis le serveur local la carte HTML des forêts
        self.moteur.load(QUrl("http://127.0.0.1:8000/data/cartes/carte.html"))

        # on appelle la méthode d'initialisation de l'interface graphiqe
        self.init_interface()

        # puis on affiche la fenêtre principale
        self.show()

    def init_interface(self):
        """
        Entrées \\: \n
            self:FenetrePrincipale : instance de la classe FenetrePrincipale
        
        Rôle \\: \n
            Initialisation de l'interface graphique de la fenêtre principale
        
        Sortie \\: \n
            None
        """
        # on définit le nom et la taille de la fenêtre
        self.setWindowTitle("DaVinciMap - Carte des forêts")
        self.resize(1200, 700)

        # on crée le layout horizontal principal
        layout_principal = QHBoxLayout()

        # groupe de modification de forêt
        self.groupe_modif_foret = GroupeForet(self)
        self.groupe_modif_foret.hide()

        # groupe de recherche de forêt
        self.groupe_recherche_foret = GroupeRecherche(self)
        self.groupe_recherche_foret.hide()

        # barre d'action à gauche de la carte
        barre_gauche = QVBoxLayout()

        # bouton de création de forêt
        bouton_nouveau = QPushButton("+")
        bouton_nouveau.setObjectName("bouton-action")
        bouton_nouveau.clicked.connect(self.afficher_nouvelle_foret)

        # bouton de recherche de forêt
        bouton_recherche = QPushButton("🔍")
        bouton_recherche.clicked.connect(self.afficher_groupe_recherche)
        bouton_recherche.setObjectName("bouton-action")

        # on ajoute les deux boutons en bas de la barre d'action
        barre_gauche.addStretch()
        barre_gauche.addWidget(bouton_recherche)
        barre_gauche.addWidget(bouton_nouveau)

        # on ajoute au layout principal la barre d'action, les groupe d'actions
        # des forêts puis le moteur web qui contient la carte HTML
        layout_principal.addLayout(barre_gauche)
        layout_principal.addWidget(self.groupe_recherche_foret)
        layout_principal.addWidget(self.groupe_modif_foret)
        layout_principal.addWidget(self.moteur, 1)

        # on définit layout_principal comme layout de la fenêtre
        self.setLayout(layout_principal)

        # on applique le style QSS à l'interface graphique depuis le fichier
        with open(os.sep.join(['data', 'style.qss'])) as fichier:
            self.setStyleSheet(fichier.read())

    def afficher_nouvelle_foret(self):
        """
        Entrées \\: \n
            self:FenetrePrincipale : instance de la classe FenetrePrincipale
        
        Rôle \\: \n
            Afficher l'interface permettant d'enregistrer une nouvelle forêt
            dans la base de données
        
        Sortie \\: \n
            None
        """
        # on met à jour le groupe de modification de forêt à partir d'un
        # dictionnaire vide
        self.groupe_modif_foret.mettre_a_jour({})
        # on cache le groupe de recherche de forêt
        self.groupe_recherche_foret.hide()
        # puis on affiche le groupe de modification de forêt
        self.groupe_modif_foret.show()

    def afficher_groupe_recherche(self):
        """
        Entrées \\: \n
            self:FenetrePrincipale : instance de la classe FenetrePrincipale
        
        Rôle \\: \n
            Afficher l'interface permettant de rechercher une forêt par son nom
            ou par un des détails enregistrés
        
        Sortie \\: \n
            None
        """
        # on cache le groupe de modification de forêt
        self.groupe_modif_foret.hide()
        # on désactive la sélection
        self.groupe_modif_foret.mode_sel = False

        # si le groupe de recherche est caché, on l'affiche, sinon on le cache
        if self.groupe_recherche_foret.isVisible():
            self.groupe_recherche_foret.hide()
        else:
            self.groupe_recherche_foret.show()

    def gerer_clic(self, coord, zoom):
        """
        Entrées \\: \n
            self:FenetrePrincipale : instance de la classe FenetrePrincipale
            coord:tuple[float] : latitude et longitude du clic enregistré
            zoom:int : facteur de zoom de la carte
        
        Rôle \\: \n
            Gérer un clic sur la carte en déléguant cette gestion au groupe de
            modification de forêt si la sélection est activée
        
        Sortie \\: \n
            None
        """
        # on récupère la latitude et la longitude du clic
        lat, lon = coord

        # message en console si debug vaut True
        if self.debug:
            print(f'Click reçu en : {lat}, {lon} | Zoom : {zoom}')

        # si la sélection est activée
        if self.groupe_modif_foret.mode_sel:
            # message en console si debug vaut True
            if self.debug: print("Clic enregistré et sélection activée :)")

            # on appelle la méthode de gestion de clic du groupe adéquat
            self.groupe_modif_foret.gerer_clic_cartes(coord, zoom)

    def recharger_carte(self, coord = None, zoom = 13):
        """
        Entrées \\: \n
            self:FenetrePrincipale : instance de la classe FenetrePrincipale
            coord:tuple[float] : latitude et longitude du clic enregistré
            zoom:int : facteur de zoom de la carte
        
        Rôle \\: \n
            Remplacer la carte du moteur web par une nouvelle carte centrée sur
            les coordonnées passées en paramètres et sur laquelle la forêt en
            cours de modification est colorée, de même que les polygones à
            ajouter et supprimer
        
        Sortie \\: \n
            None
        """
        # on récupère l'identifiant de la forêt en cours de modification s'il
        # existe (None sinon)
        id_foret = self.groupe_modif_foret.dico_foret.get("id")

        # si les coordonnées ne sont pas en paramètres
        if coord is None:
            # on tente de récupérer les coordonnées du centre de la forêt en
            # cours de modification
            if id_foret:
                nom = self.groupe_modif_foret.dico_foret.get("nom", "")
                coord = self.inter.recuperer_centre_foret(nom)

            # s'il n'y en a pas, on tente de récupérer celles d'un point d'un
            # des polygones à ajouter
            if coord is None and self.groupe_modif_foret.polygones_temp:
                premier = self.groupe_modif_foret.polygones_temp[0]
                geom = premier["features"][0]["geometry"]["coordinates"]
                if geom and geom[0]:
                    point = geom[0][0]
                    coord = (point[1], point[0])

            # si les coordonnées valent toujours None, on crée par défaut la
            # carte à la latitude et la longitude de Montaigu-Vendée
            if coord is None:
                coord = (46.974, -1.314)

        # on récupère les polygones à ajouter et supprimer pour les colorer
        donnees_temp = self.groupe_modif_foret.polygones_temp
        donnees_suppr = self.groupe_modif_foret.polygones_a_suppr

        # on récupère les polygones de la forêt sélectionnée, dans la BDD
        donnees_select = []
        if id_foret:
            # on récupère les lignes de la BDD
            infos = self.inter.bdd.rechercher_ligne(
                "FORET", ("id_foret", id_foret)
            )

            # on récupère un éventuel identifiant de la feature correspondant à
            # la forêt sélectionnée, on prend l'identifiant de la forêt sinon
            id_feature = str(infos[0][1]) if infos else str(id_foret)

            # on récupère la feature de la forêt sélectionnée
            feature = self.inter.rechercher_feature(str(id_feature))
            if feature and "geometry" in feature:
                # puis on affecte à donnees_select une collection contenant
                # cette feature, pour la mettre en couleur sur la carte
                donnees_select = [
                    {"type": "FeatureCollection", "features": [feature]}
                ]

        # on apelle la méthode de génération de la carte
        carte.generer_carte(
            coord, zoom, donnees_temp, donnees_select, donnees_suppr,
            self.debug
        )

        # puis on recharge cette carte dans le moteur web depuis le serveur
        self.moteur.load(QUrl("http://127.0.0.1:8000/data/cartes/carte.html"))