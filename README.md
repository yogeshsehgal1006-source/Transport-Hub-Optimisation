This project identifies the most optimal transport hub locations in a select area, in my case Birmingham,UK. Residential building data has been gathered using OpenStreetMap, and i had used KMeans clustering in order ot find the optimal hub locations. This project gathers information from a user, using their residential data to calculate the walking distances from their building to the nearest hub. All of the information is then presented on an interactive Folium map.

Requirements:
You must install the following package before running the code:
pip install osmnx geopandas pandas scikit-learn numpy geopy folium

How to use this code:
1) Clone the repository
2) Run the following python script: python hub_mapper.py
3) Run the code, and enter a suitable location when asked
4) Wait for a few minutes, and the script will open a HTML map in your browser
5) Run the code, but use different residential locations. Change the variable k in the script, and you will see a different amount of hubs.









