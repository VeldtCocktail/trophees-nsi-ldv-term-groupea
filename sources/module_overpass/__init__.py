# Projet : SilvaDaVinci
# Auteurs : Mathéo PASQUIER, Maden USSEREAU, Léon RAIFAUD, Charlélie PINEAU

# importation des bibliothèques nécessaires
import requests
from shapely.geometry import shape, Point, Polygon, MultiPolygon, mapping
from shapely.ops import orient

# fichiers à importer lorsqu'on exécute " from module_overpass import * "
__all__ = ['overpass']