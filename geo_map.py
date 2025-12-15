import pandas as pd
from geopy.geocoders import Nominatim
import folium
import json
import web_browser_wrapper
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="./log/geomap.log",
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
# output html folder
logger.info("Started: html file")
html_folder = Path("C:/Code/GeoMap/html")
html_file = html_folder / "geocoded_map.html"
# Build file:// URL automatically
file_url = html_file.as_uri()
logger.info("Finished: html file")
# Load dataset
data = pd.read_excel("data.xlsx")
geolocator = Nominatim(
    user_agent="distance_calculator(geo-map craigreider@yahoo.com)", timeout=10
)


def geocode_address(row):  # -> tuple | tuple[None, None]:
    """_summary_

    Args:
        row (_type_): _description_

    Returns:
        _type_: _description_
    """
    location = geolocator.geocode(f"{row['City']}, {row['State']}, {row['Country']}")
    if location:
        logger.info(
            f"city: {row['City']} lat{location.latitude}: lon: {location.longitude}"
        )
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
        popup_text = f"{row['City']}<br>Population: {row['City']}"
        # popup_text=f"{row["City"]}"
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
# Save Folium map
mymap.save(html_file)
web_browser_wrapper.open_file_in_edge(file_url, 1)
