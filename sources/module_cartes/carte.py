import folium
import pathlib
from PyQt5.QtCore import QObject, pyqtSlot

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

class Pont(QObject):

    def __init__(self, parent):
        self.par = parent
        super().__init__(parent)

    @pyqtSlot(float, float, int)
    def envoyerCoordonnees(self, lat, long, zoom):
        print(f'Click enregistré en : {lat}, {long} | Zoom : {zoom}')
        self.par.update_carte((lat, long), zoom)