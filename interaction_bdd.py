import sqlite3

class BaseDeDonnees:
    """
    Classe permettant l'interaction avec le fichier de base de donnees
    """
    def __init__(self, nom_fichier):
        self.connexion = sqlite3.connect(nom_fichier)
        self.curseur = self.connexion.cursor()
    
    def ajouter_ligne(self, table, valeurs):
        """
        Entrees : self:instance de BaseDeDonnees
                  table:str nom de la table
                  valeurs:list liste des valeurs a inserer dans la table
        Role : ajoute une ligne dans la table specifiee avec les valeurs 
               donnees dans valeurs
        Sortie : modifie la base de donnees
        """
        temp = ", ".join(["?" for element in valeurs])
        requete = f"INSERT INTO {table} VALUES ({temp})"
        self.curseur.execute(requete, valeurs)
        self.connexion.commit()

    def supprimer_ligne(self, table, identification):
        """
        Entrees : self:instance de BaseDeDonnees
                  table:str nom de la table
                  identification:tuple(colonne:str, valeur:any) critere de 
                          suppression, ex: ("id_foret", 1)
        Role : supprime une ligne dans la table specifiee correspondant au 
               critere
        Sortie : base de donnees indiquee par self modifiee
        """
        colonne = identification[0]
        valeur = identification[1]
        requete = f"DELETE FROM {table} WHERE {colonne} = ?"
        self.curseur.execute(requete, (valeur,))
        self.connexion.commit()

    def modifier_ligne(self, table, modif):
        """
        Entrees : self:instance de BaseDeDonnees
                  table:str nom de la table
                  modif:tuple contient (
                  identification:tuple(colonne:str, valeur:any),
                                 colonne:str, 
                                 valeur:any)
        Role : modifie une valeur dans la table specifiee
        Sortie : base de donnees modifiee
        """
        identification = modif[0]
        colonne_modif = modif[1]
        nouvelle_valeur = modif[2]
        
        colonne_id = identification[0]
        valeur_id = identification[1]
        
        requete = f'''
            UPDATE {table} 
            SET {colonne_modif} = ?
            WHERE {colonne_id} = ?
        '''
        self.curseur.execute(requete, (nouvelle_valeur, valeur_id))
        self.connexion.commit()

# Avant de recommencer quelconque test sur la bdd, penser a reset la/les 
# table(s) affectee(s) avant, afin d'eviter des bugs causes non pas par le code
# mais par l'utilisateur, merci - Léon

# Test d'ajout de foret
bdd = BaseDeDonnees("bdd.db")
bdd.ajouter_ligne("FORET", (1, "Foret de test", 100, 1000, 1, 2, 3, 4))
input()
# Test de modification
bdd.modifier_ligne("FORET", (("id_foret", 1), "nom", "Foret modifiee"))
input()
# Et de suppression
bdd.supprimer_ligne("FORET", ("id_foret", 1))