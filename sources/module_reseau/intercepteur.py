# Projet : SilvaDaVinci
# Auteurs : Mathéo PASQUIER, Maden USSEREAU, Léon RAIFAUD, Charlélie PINEAU

# importation des bibliothèques nécessaires
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor

class IntercepteurRequetes(QWebEngineUrlRequestInterceptor):
    """
    Classe permettant d'intercepter et de modifier les requêtes réseau
    réalisées par le moteur web PyQt
    """

    def __init__(self, parent, debug):
        """
        Entrées \\: \n
            self:IntercepteurRequetes : instance de la classe
                IntercepteurRequetes
            parent:FenetrePrincipale : intance de la classe FenetrePrincipale
            debug:bool : messages de debug en console
        
        Rôle \\: \n
            Initialisation de la classe IntercepteurRequetes
        
        Sortie \\: \n
            None
        """
        # on initialise la superclasse QWebEngineUrlRequestInterceptor
        super().__init__(parent)
        # on affecte debug à l'attribut debug de la classe
        self.debug = debug

    def interceptRequest(self, info):
        """
        Entrées \\: \n
            self:IntercepteurRequetes : instance de la classe
                IntercepteurRequetes
            info:QWebEngineUrlRequestInfo : informations de la requête
        
        Rôle \\: \n
            Intercepter une requête du moteur web de la fenêtre principale et
            en modifier les informations
        
        Sortie \\: \n
            None
        """
        # on récupère l'url de la requête
        url = info.requestUrl().toString()
        # message en console si debug vaut True
        if self.debug: print("Requête :", url)

        # si l'url correspond au chargement d'une tuile OpenStreetMap
        if "tile.openstreetmap" in url:
            # on modifie l'en-tête HTTP de la requête pour y ajouter l'agent
            # utilisateur et le "Referer"
            info.setHttpHeader(
                b"Referer",
                b"https://www.openstreetmap.org/"
            )
            info.setHttpHeader(
                b"User-Agent",
                b"CarteForets/1.0 (educational project)"
            )
