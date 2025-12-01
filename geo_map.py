import pandas as pd
from geopy.geocoders import Nominatim
import folium
import json

# Load dataset
data = pd.read_excel("data.xlsx")

# geolocator = Nominatim(user_agent="craigreider@yahoo.com")
geolocator = Nominatim(user_agent="distance_calculator(geo-map craigreider@yahoo.com)", timeout=10)


def geocode_address(row):
    location = geolocator.geocode(f"{row['City']}, {row['State']}, {row['Country']}")
    if location:
        return location.latitude, location.longitude
    else:
        return None, None


data["Latitude"], data["Longitude"] = zip(*data.apply(geocode_address, axis=1))

# Calculate mean of coordinates for map center
map_center = [data["Latitude"].mean(), data["Longitude"].mean()]

# make map with folium
mymap = folium.Map(location=map_center, zoom_start=7)  # adjust as needed

# Add markers
for index, row in data.iterrows():
    if row["Latitude"] and row["Longitude"]:
        popup_text=f"{row["City"]}<br>Population: {row["City"]}"
        #popup_text=f"{row["City"]}"
        folium.Marker([row["Latitude"], row["Longitude"]], popup=popup_text).add_to(
            mymap
        )

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
).add_to(mymap)

# Add a layer control and display the map
folium.LayerControl().add_to(mymap)
# Save

mymap.save("geocoded_map.html")
