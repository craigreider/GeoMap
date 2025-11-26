import pandas as pd
from geopy.geocoders import Nominatim
import folium

# Load dataset
data = pd.read_excel("data.xlsx")

# geolocator = Nominatim(user_agent="craigreider@yahoo.com")
geolocator = Nominatim(user_agent="distance_calculator", timeout=10)


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
mymap = folium.Map(location=map_center, zoom_start=4)  # adjust as needed

# Add markers
for index, row in data.iterrows():
    if row["Latitude"] and row["Longitude"]:
        folium.Marker([row["Latitude"], row["Longitude"]], popup=row["City"]).add_to(
            mymap
        )

# Save

mymap.save("geocoded_map.html")
