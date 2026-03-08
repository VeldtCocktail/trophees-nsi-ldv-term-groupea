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
            Initialisation de la classe

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
    def envoyerCoordonnees(self, lat, long, zoom):
        """
        Entrées \\: \n
            self:Pont : instance de la classe Pont
            lat:float : latitude des coordonnées envoyées par le JavaScript
            long:float : longitude des coordonnées envoyées par le JavaScript

        Rôle \\: \n
            Initialisation de la classe

        Sortie \\: \n
            None
        """
        print(f'Click enregistré en : {lat}, {long} | Zoom : {zoom}')
        self.fen.update_carte((lat, long), zoom)


def generer_carte(coordonnees_depart, zoom = 12, donnees = []):
    fonction_style = lambda x: {
        "fillColor": (
            "#0000ff"
        )
    }

    carte = folium.Map(location = coordonnees_depart, zoom_start = zoom)

    folium.GeoJson("data/forets_vendee.geojson").add_to(carte)
    for donnees_json in donnees:
        folium.GeoJson(donnees_json, style_function = fonction_style).add_to(carte)

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
