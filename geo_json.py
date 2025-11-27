import folium
import json

# Coordinates for centering the map (example: California)
latitude, longitude = 36.7783, -119.4179

# Create a Folium map
m = folium.Map(location=[latitude, longitude], zoom_start=7)

# Load GeoJSON data for the state (replace 'state_geojson.json' with your file)
with open('california_counties.geojson', 'r') as f:
    state_geojson = json.load(f)

# Add the GeoJSON layer to highlight the state
folium.GeoJson(
    state_geojson,
    name="California",
    style_function=lambda x: {
        'fillColor': 'blue',
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.05
    }
).add_to(m)

# Add a layer control and display the map
folium.LayerControl().add_to(m)
m.save("single_state_map.html")