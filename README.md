# Birmingham Transport Hub Clustering & Accessibility Mapper

A project that uses data from OpenStreetMap, K-Means Clustering and user input to create a selected number of transport hubs around the city of Birmingham. It aims to find the most optimal hub locations based on address and population density.

## Overview

Residential data is downloaded based on the city of Birmingham. This data is then grouped into K number of clusters using K-Means clustering.

The script then asks for user input of an address in Birmingham, whereby the distance from the address to the nearest transport hub is calculated. This is then visualised on a Folium map which can be interacted with.

## Features

**OpenStreetMap Integration:** Downloads real residential building data for Birmingham using `osmnx`.

**K-Means Clustering:** Groups residential points into a selected number of clusters (`k=200` by default) to optimise potential transport hub placements.

**Distance Analysis:** Calculates straight-line and walking distances from buildings to the nearest transport hub.

**Interactive Mapping:** Generates a custom HTML map (`birmingham_transport_clusters.html`) featuring colour-coded clusters, hub markers and user-to-hub pathing.

## How It Works

### Data Collection
Fetches all residential data within Birmingham boundaries.

### Centroid Extraction
Converts building polygons into point coordinates.

### Clustering
Uses the K-Means algorithm to find optimal central coordinates for the selected number of transport hubs.

### Geocoding & Distance Calculation
Uses `geopy` to locate user inputs and compute distances to the closest transport hub.

### Visualisation
Plots the data onto a Folium map using marker descriptions and a designated colour palette.

## Dependencies

Copy and paste the following into your terminal to install the required dependencies:

```bash
pip install requests osmnx geopandas pandas scikit-learn numpy geopy folium











