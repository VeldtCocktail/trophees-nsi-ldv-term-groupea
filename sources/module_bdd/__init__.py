# Projet : SilvaDaVinci
# Auteurs : Mathéo PASQUIER, Maden USSEREAU, Léon RAIFAUD, Charlélie PINEAU

# importation des bibliothèques nécessaires au module
import sqlite3
import json
import csv
import os
import math
from shapely.geometry import shape, mapping
from shapely.ops import orient

# fichiers à importer lorsqu'on exécute " from module_affichage import * "
__all__ = ['interaction_donnees']