import folium
import pathlib

carte = folium.Map(location=(46.3930189, -1.480289), zoom_start=12)

folium.GeoJson("data/forets_vendee.geojson").add_to(carte)

map_name = carte.get_name()


# portion de code générée par l'intelligence artificielle
click_js = f"""
function bindMapClick() {{
    if (typeof {map_name} !== 'undefined') {{
        {map_name}.on('click', function(e) {{
            if (window.pybridge) {{
                pybridge.envoyerCoordonnees(e.latlng.lat, e.latlng.lng);
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

carte.get_root().script.add_child(folium.Element(click_js))
carte.get_root().html.add_child(folium.Element(qwebchannel_js))

carte.save(pathlib.Path("cartes", "carte.html"))
