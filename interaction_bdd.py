import sqlite3

class BaseDeDonnees:
    """
    Classe permettant l'interaction avec le fichier de base de donnees
    """
    def __init__(self, nom_fichier):
        self.connexion = sqlite3.connect(nom_fichier)
        self.cursor = self.connexion.cursor()
    
    def ajouter_foret(self, id_foret, nom, nb_visi_par_an, superficie, 
                      implan_naturelle, id_eau, id_espece, id_risque):
        """
        Entrees : self:instance de BaseDeDonnees
                  id_foret:int identifiant unique d'une foret dans la table 
                           FORET
                  nom:str nom de la foret a ajouter
                  nb_visi_par_an:int nombre de visiteurs que cette foret a, par
                                 an
                  superficie:float la superficie de la foret, en m^2
                  implan_naturelle:int un 0 (FALSE) ou un 1 (TRUE), definissant
                                   si la foret est issue d'une implantation 
                                   naturelle ou artificielle
                  id_eau:int identifiant unique d'un cours/plan d'eau dans la 
                         table EAU
                  id_espece:int identifiant unique d'une espece dans la table 
                               ESPECE
                  id_risque:int identifiant unique d'un risque dans la table 
                               RISQUE
        Role : ajoute une nouvelle ligne dans la table FORET
        Sortie : modifie la base de donnees, sinon aucune sortie
        """
        self.cursor.execute("INSERT INTO FORET VALUES "\
                            f"({id_foret}, '{nom}', {nb_visi_par_an},"\
                            f"{superficie}, {implan_naturelle}, {id_eau},"\
                            f"{id_espece}, {id_risque})")
        self.connexion.commit()

    # /!\ Ne marche pas encore /!\ 
    # ------------------------------------------------------------------------- 
    # TODO : Corriger l'erreur disant que, aux tests :
    # sqlite3.OperationalError: near ""nom"": syntax error
    # -------------------------------------------------------------------------
    def modifier_foret(self, id_foret, colonne, valeur):
        """
        Entrees : self:instance de BaseDeDonnees
                  id_foret:int identifiant unique d'une foret dans la table 
                           FORET
                  nom:str nom de la foret a ajouter
                  nb_visi_par_an:int nombre de visiteurs que cette foret a, par
                                 an
                  superficie:float la superficie de la foret, en m^2
                  implan_naturelle:int un 0 (FALSE) ou un 1 (TRUE), definissant
                                   si la foret est issue d'une implantation 
                                   naturelle ou artificielle
                  id_eau:int identifiant unique d'un cours/plan d'eau dans la 
                         table EAU
                  id_espece:int identifiant unique d'une espece dans la table 
                               ESPECE
                  id_risque:int identifiant unique d'un risque dans la table 
                               RISQUE
        Role : modifie une ligne dans la table FORET
        Sortie : modifie la base de donnees, sinon aucune sortie
        """
        self.cursor.execute(f"UPDATE FORET"\
                    f"SET {colonne} = {valeur}"\
                    f'WHERE "id_foret" = {id_foret}')
        self.connexion.commit()    
    # - /!\ Ne marche pas encore /!\ 

    def supprimer_foret(self, id_foret):
        """
        Entrees : self:instance de BaseDeDonnees
                  id_foret:int identifiant unique d'une foret dans la table 
                           FORET
        Role : supprime une ligne dans la table FORET
        Sortie : modifie la base de donnees, sinon aucune sortie
        """
        self.cursor.execute(f"DELETE FROM FORET WHERE id_foret = {id_foret}")
        self.connexion.commit()

# Avant de recommencer quelconque test sur la bdd, penser a reset la/les tables
# affectees avant, afin d'eviter des bugs non causes par le code mais par 
# l'utilisateur, merci - Léon

# Test d'ajout de foret
bdd = BaseDeDonnees("bdd.db")
bdd.ajouter_foret(1, "Foret de test", 100, 1000, 1, 2, 3, 4)
input()

# Test de modification de foret - /!\ Ne marche pas encore /!\ 
bdd.modifier_foret(1, "", "Foret modifiee")
input()

# Test de suppression de foret
bdd.supprimer_foret(1)
