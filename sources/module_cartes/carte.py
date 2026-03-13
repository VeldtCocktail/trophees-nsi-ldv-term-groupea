# importation des bibliothèques nécessaires
import folium
import pathlib
from PyQt5.QtCore import QObject, pyqtSlot


class Pont(QObject):
    """
    Classe qui implémente un pont entre le JavaScript de la carte et l'instance
    python de la fenêtre principale
    """
    
    def __init__(self, fenetre):
        """
        Entrées \\: \n
            self:Pont : instance de la classe Pont
            fenetre:FenetrePrincipale : instance de la classe FenetrePrincipale

        Rôle \\: \n
            Initialisation de la classe Pont

        Sortie \\: \n
            None
        """
        # initialisation de la superclasse QObject
        super().__init__()
        # on affecte à self.fen la valeur de fenêtre, l'instance de la classe
        # principale du programme (classe FenetrePrincipale)
        self.fen = fenetre

    # décorateur pyqtSlot qui permet de faire le lien avec le JavaScript
    @pyqtSlot(float, float, int)
    def envoyerCoordonnees(self, lat, lon, zoom):
        """
        Entrées \\: \n
            self:Pont : instance de la classe Pont
            lat:float : latitude des coordonnées envoyées par le JavaScript
            lon:float : longitude des coordonnées envoyées par le JavaScript
            zoom:int : facteur actuel de zoom de la carte

        Rôle \\: \n
            Recevoir les coordonnées envoyées par le JavaScript intégré à la
            carte lors d’un clic sur celle ci, et transmettre ces coordonnées à
            la méthode gerer_clic de la fenêtre principale

        Sortie \\: \n
            None
        """
        # si le mode debug de la fenêtre principale est activé
        if self.fen.debug:
            # on affiche un message de debug en console
            print(f'Click enregistré en : {lat}, {lon} | Zoom : {zoom}')
            
        # on appelle la méthode gerer_clic de la fenêtre principale en passant
        # en paramètres les coordonnées du point cliqué et le facteur de zoom
        self.fen.gerer_clic((lat, lon), zoom)


def generer_carte(
        coord_depart, zoom = 12, donnees = [], donnees_select = [],
        donnees_suppr=[], debug = False
    ):
    """
    Entrées \\: \n
        coord_depart:tuple(int) : latitude et longitude du centre de la carte
        zoom:int : facteur de zoom de la carte
        donnees:list[dict[str: any]] : dictionnaire des données temporaires à
            ajouter sur la carte, de la forme {'type':'FeatureCollection', 
            'features': list[dict[str: any]]}
        debug:bool : affichage des messages de debug en console
    
    Rôle \\: \n
        Générer un fichier carte.html qui contient les polygones du fichier
        data/forets_vendee.geojson, les données temporaires <donnees> ainsi
        qu’une fonction JavaScript qui permet de relier la carte à la fenêtre
        principale du programme Python
    
    Sortie \\: \n
        None
    """

    carte = folium.Map(location = coord_depart, zoom_start = zoom)

    folium.GeoJson(
        "data/forets_vendee.geojson", style_function = fonction_style_permanent
    ).add_to(carte)
    
    # polygones temporaires en cours de sélection
    for donnees_json in donnees:
        folium.GeoJson(
            donnees_json, style_function = fonction_style_temp
        ).add_to(carte)

    # polygones sauvegardés de la forêt sélectionnée
    for donnees_json in donnees_select:
        folium.GeoJson(
            donnees_json, style_function = fonction_style_select
        ).add_to(carte)

    # polygones sélectionnés à supprimer
    for donnees_json in donnees_suppr:
        folium.GeoJson(
            donnees_json, style_function = fonction_style_suppr
        ).add_to(carte)

    map_name = carte.get_name()

    # portion de code générée par l'intelligence artificielle
    click_js = f"""
    function bindMapClick() {{
        if (typeof {map_name} !== 'undefined') {{
            {map_name}.on('click', function(e) {{
                if (window.pybridge) {{
                    var zoomLevel = {map_name}.getZoom();
                    pybridge.envoyerCoordonnees(
                    e.latlng.lat,
                    e.latlng.lng,
                    zoomLevel
                );
                }}
            }});
        }} else {{
            setTimeout(bindMapClick, 100);
        }}
    }}
    bindMapClick();
    """

    qwebchannel_js = """
    <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
    <script>
    new QWebChannel(qt.webChannelTransport, function(channel) {
        window.pybridge = channel.objects.pybridge;
    });
    </script>
    """
    # fin de cette portion

    carte.get_root().script.add_child(folium.Element(click_js))
    carte.get_root().html.add_child(folium.Element(qwebchannel_js))

    carte.save(pathlib.Path("cartes", "carte.html"))

def fonction_style_permanent(elem):
    return {
        "fillColor": "#3700ff",
        "color": "#0000ff00",
        "weight": 2,
        "fillOpacity": 0.4
    }

def fonction_style_select(elem):
    return {
        "fillColor": "#0e8014",
        "color": "#0000ff00",
        "weight": 3,
        "fillOpacity": 0.5
    }

def fonction_style_temp(elem):
    return {
        "fillColor": "#eeff00",
        "color": "#0000ff00",
        "weight": 4,
        "fillOpacity": 0.4
    }

def fonction_style_suppr(elem):
    return {
        "fillColor": "#ff0000",
        "color": "#0000ff00",
        "weight": 2,
        "fillOpacity": 0.5
    }