import requests
import osmnx as ox
import geopandas as gp
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import time
import folium
from folium.plugins import MarkerCluster
import webbrowser

# 1. Defining the place i want to do this project on
place = "Birmingham, United Kingdom"

# 2. Downloading residential building data
print(" Downloading residential building data from OpenStreetMap...")
buildings = ox.features_from_place(place, tags={'building': 'residential'})

# Drop rows without geometry and reset index
buildings = buildings.dropna(subset=['geometry']).reset_index()

# Convert building polygons to simple points(Centroids)
residential = buildings[['geometry']].copy()
residential['geometry'] = residential.centroid

residential = residential.set_geometry('geometry').to_crs(epsg=4326)

# Extracting latitude and longitude
residential['lat'] = residential.geometry.y
residential['lon'] = residential.geometry.x

# Show sample coordinates
print("\n Sample coordinates:")
print(residential[['lat', 'lon']].head())

# 3. Clustering residential buildings into hubs
coordinates = residential[['lat', 'lon']].values
k = 20  # Number of transport hubs, variable so can change this value

print(f"\n Clustering into {k} hubs...")
kmeans = KMeans(n_clusters=k, random_state=0)
kmeans.fit(coordinates)

# Hub coordinates (cluster centers)
hub_coords = kmeans.cluster_centers_
hubs = gp.GeoDataFrame(geometry=gp.points_from_xy(
    hub_coords[:, 1], hub_coords[:, 0]), crs='EPSG:4326')

# Assign each building to the nearest hub
residential['hub_id'] = kmeans.predict(coordinates)

# 4. Compute straight-line distance to each building's hub


def compute_distance(row):
    hub_lat, hub_lon = hub_coords[row['hub_id']]
    return geodesic((row['lat'], row['lon']), (hub_lat, hub_lon)).meters


print("\n Computing walking distances...")
residential['dist_to_hub'] = residential.apply(compute_distance, axis=1)

# Report average distance
average_distance = residential['dist_to_hub'].mean()
print(
    f"\n Average walking distance to the nearest hub: {average_distance:.2f} meters")

# 5. Ask for user location input with retry
geolocator = Nominatim(user_agent="transport-hub-mapper")


def try_geocode(address):
    try:
        location = geolocator.geocode(address, timeout=10)
        return location
    except Exception as e:
        print(f" Geocoding error: {e}")
        return None


user_lat = user_lon = None
while True:
    user_input = input(
        "\n Enter your location (e.g. '123 High Street, Birmingham'): ").strip()

    if not user_input:
        print(" You must enter a location. Try again.")
        continue

    # Normalize input: capitalize and ensure it includes 'Birmingham'
    if "birmingham" not in user_input.lower():
        user_input += ", Birmingham"

    print(f" Trying to geocode: {user_input}")
    location = try_geocode(user_input)

    if location:
        user_lat = location.latitude
        user_lon = location.longitude
        print(f"✅ Location found: {location.address}")
        print(f"Coordinates: ({user_lat}, {user_lon})")
        break
    else:
        print(
            " Location not found. Please try again with more detail (e.g. street + city).")
        time.sleep(1)

# 6. Find nearest hub to user location
min_dist = float('inf')
nearest_hub = None
if user_lat is not None and user_lon is not None:
    for idx, (hub_lat, hub_lon) in enumerate(hub_coords):
        dist = geodesic((user_lat, user_lon), (hub_lat, hub_lon)).meters
        if dist < min_dist:
            min_dist = dist
            nearest_hub = idx

    print(
        f"\n Distance from your location to nearest hub (Hub {nearest_hub}): {min_dist:.2f} meters")

# 7. Create interactive Folium map
print("\n Creating map...")
center_lat = residential['lat'].mean()
center_lon = residential['lon'].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# Cluster colors
colors = [
    "#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231", "#911eb4", "#46f0f0",
    "#f032e6", "#bcf60c", "#fabebe", "#008080", "#e6beff", "#9a6324", "#fffac8",
    "#800000", "#aaffc3", "#808000", "#ffd8b1", "#000075", "#808080"
]

# Add residential points
print(" Plotting residential buildings...")
for idx, row in residential.iterrows():
    color = colors[row['hub_id'] % len(colors)]
    folium.CircleMarker(
        location=(row['lat'], row['lon']),
        radius=2,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        weight=0,
    ).add_to(m)

# Add hub markers
print("🚏 Plotting transport hubs...")
for idx, hub in hubs.iterrows():
    folium.Marker(
        location=[hub.geometry.y, hub.geometry.x],
        icon=folium.Icon(color='red', icon='bus', prefix='fa'),
        popup=f'Hub {idx}'
    ).add_to(m)

# Add user location marker and line to nearest hub
if user_lat is not None and user_lon is not None and nearest_hub is not None:
    folium.Marker(
        location=[user_lat, user_lon],
        icon=folium.Icon(color='blue', icon='user', prefix='fa'),
        popup=f'Your Location<br>Distance to Hub {nearest_hub}: {min_dist:.2f} meters'
    ).add_to(m)

    # Draw line to hub
    folium.PolyLine(
        locations=[
            [user_lat, user_lon],
            [hub_coords[nearest_hub][0], hub_coords[nearest_hub][1]]
        ],
        color='blue',
        weight=2,
        dash_array='5,5',
        tooltip=f'Distance: {min_dist:.2f} meters'
    ).add_to(m)

# 8. Save and open the map
map_filename = 'birmingham_transport_clusters.html'
m.save(map_filename)
print(f"\n✅ Map saved to '{map_filename}'")
print(" Opening map in browser...")
webbrowser.open(map_filename)
