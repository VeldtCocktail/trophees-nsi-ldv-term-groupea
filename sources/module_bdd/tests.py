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