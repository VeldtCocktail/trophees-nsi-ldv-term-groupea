import folium

carte = folium.Map(location=(46.3930189, -1.480289), zoom_start=12)

folium.GeoJson("forets_vendee.geojson").add_to(carte)

carte.show_in_browser()