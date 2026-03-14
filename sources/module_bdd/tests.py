# temporaire → fichier de tests du module

import interaction_donnees
import os

path_db = os.sep.join(
    ['data', 'bdd.db']
)
print("cwd =", os.getcwd())
print("absolute =", os.path.abspath(path_db))
print("exists =", os.path.exists(path_db))

indo = interaction_donnees.InteractionDonnees(
    path_db,
    os.sep.join(
        ['data', 'forets_vendee.geojson']
    )
)

indo.synchro_depuis_json()

for table in [
    "FORET_ARBRE", "FORET_ANIM", "FORET_CHAMPI", "FORET_EAU", "FORET_RISQUE"
]:
    indo.bdd.vider_table(table)

print(indo.recuperer_centre_foret("Forêt de Puits Neuf"))
print(indo.calculer_superficie_foret(10))