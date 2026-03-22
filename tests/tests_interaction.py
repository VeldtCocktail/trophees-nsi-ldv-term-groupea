# Projet : SilvaDaVinci
# Auteurs : Mathéo PASQUIER, Maden USSEREAU, Léon RAIFAUD, Charlélie PINEAU

# importation des bibliothèques nécessaires
import os
from sources.module_bdd import interaction_donnees as indo

# on crée une instance de la classe InteractionDonnees
interaction = indo.InteractionDonnees(
    os.sep.join(["tests", "bdd_test.db"]),
    os.sep.join(["tests", "forets_test.geojson"]),
    debug = True
)

# divers tests des méthodes du module d'interaction avec les bases de données
ligne_foret = interaction.rechercher_foret(("id_foret", 1))
print("Forêt recherchée :", ligne_foret)

id_feature = ligne_foret[0][1]
print("Identifiant de la feature :", id_feature)

interaction.mettre_a_jour_nom_foret(id_feature, "Nom mis à jour (test)")

liste_noms_forets = indo.charger_noms_forets(["tests", "forets_test.geojson"])
print("Forêts : \n", liste_noms_forets)

liste_arbres = indo.charger_donnees_csv(["tests", "bdd_arbres_test.csv"])
print("Arbres : \n", liste_arbres)

nom_foret = interaction.rechercher_foret(("id_foret", 4))[0][2]
centre = interaction.recuperer_centre_foret(nom_foret)
print("Centre de la forêt", nom_foret, ":", centre)