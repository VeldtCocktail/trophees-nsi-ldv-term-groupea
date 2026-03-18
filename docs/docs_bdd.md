# Explication de la base de donnees

## Table FORET
- **id_foret** : identifiant unique de la foret (INT)
- id_feature : identifiant unique de la "feature" correspondant à la forêt dans le fichier GeoJSON (TEXT)
- nom : nom de la foret (TEXT)
- nb_visi_par_an : nombre de visites par an (INT)
- superficie : superficie de la foret (REAL)
- implan_naturelle : implantation naturelle (INT) (0 pour FALSE, 1 pour TRUE)

## Table FORET_ANIM
- **id_foret** : identifiant unique de la forêt qu'on met en relation (INT)
- **id_anim** : identifiant dans le fichier csv de l'animal qu'on met en relation avec une forêt (INT)

## Table FORET_ARBRE
- **id_foret** : identifiant unique de la forêt qu'on met en relation (INT)
- **id_arbre** : identifiant dans le fichier csv de l'arbre qu'on met en relation avec une forêt (INT)

## Table FORET_CHAMPI
- **id_foret** : identifiant unique de la forêt qu'on met en relation (INT)
- **id_champi** : identifiant dans le fichier csv du champignon qu'on met en relation avec une forêt (INT)

## Table FORET_EAU
- **id_foret** : identifiant unique de la forêt qu'on met en relation (INT)
- **id_eau** : identifiant dans le fichier csv du cours d'eau qu'on met en relation avec une forêt (INT)

## Table FORET_RISQUE
- **id_foret** : identifiant unique de la forêt qu'on met en relation (INT)
- **id_risque** : identifiant dans le fichier csv du risque qu'on met en relation avec une forêt (INT)