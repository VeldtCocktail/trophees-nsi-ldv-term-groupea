# Explication de la base de donnees

## Table FORET
- **id_foret** : identifiant unique de la foret, un INT
- nom : nom de la foret, un TEXT
- nb_visi_par_an : nombre de visites par an, un INT
- superficie : superficie de la foret, un REAL (equivalent du flottant en Python)
- implan_naturelle : implantation naturelle, un INT (0 pour FALSE, 1 pour TRUE)
- \#id_eau : cle etrangere, pointant vers un identifiant unique d'un cours d'eau dans la table EAU
- \#id_espece : cle etrangere, pointant vers un identifiant unique d'une espece dans la table ESPACE
- \#id_risque : cle etrangere, pointant vers un identifiant unique d'un risque dans la table RISQUE

## Table EAU
- **id_eau** : identifiant unique d'un cours d'eau, un INT
- nom : nom du cours d'eau, un TEXT
- type : type de cours d'eau, un TEXT

## Table ESPECE
- **id_espece** : identifiant unique d'une espece, un INT
- nom : nom de l'espece, un TEXT
- scientifique : nom scientifique de l'espece, un TEXT
- mammifere : si c'est un mammifere ou non, un INT (0 pour FALSE, 1 pour TRUE)

## Table RISQUE
- **id_risque** : identifiant unique d'un risque, un INT
- type : type de risque, un TEXT
- mortel : si c'est mortel ou non, un INT (0 pour FALSE, 1 pour TRUE)
- commentaire : court commentaire sur ce risque (plus de details), un TEXT
