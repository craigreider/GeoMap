import sys
print(sys.prefix)
import folium
import json
import pandas as pd

# Coordinates for centering the map (example: California)
latitude, longitude = 36.7783, -119.4179

# Create a Folium map
m = folium.Map(location=[latitude, longitude], zoom_start=7)

# Load GeoJSON data for the state (replace 'state_geojson.json' with your file)
with open("california_counties.geojson", "r") as f:
    state_geojson = json.load(f)

# Add the GeoJSON layer to highlight the state
folium.GeoJson(
    state_geojson,
    name="California",
    style_function=lambda x: {
        "fillColor": "blue",
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.05,
    },
).add_to(m)

# Add a layer control and display the map
folium.LayerControl().add_to(m)
m.save("single_state_map.html")

####
# Load GeoJSON data
# geo_data = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json"
geo_data = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/subwaystations.geojson"

# Create a map
m = folium.Map(location=[40, -95], zoom_start=4,tiles="cartodb positron")
#m = folium.Map(location=[40, -95], zoom_start=4,tiles="dark_all")

# Add GeoJSON layer
folium.GeoJson(geo_data).add_to(m)

# Save the map
m.save("geojson_map.html")
m.save("subway_map.html")

#########
# Load data
data = pd.read_csv(
    "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/US_Unemployment_Oct2012.csv"
)

# Load GeoJSON data
geo_data = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json"

# Create a map
m = folium.Map(location=[40, -95], zoom_start=4)

# Add Choropleth layer
folium.Choropleth(
    geo_data=geo_data,
    name="choropleth",
    data=data,
    columns=["State", "Unemployment"],
    key_on="feature.id",
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Unemployment Rate (%)",
).add_to(m)

# Save the map
m.save("choropleth_map.html")
# msedge file:///C:/Code/GeoMap/choropleth_map.html
