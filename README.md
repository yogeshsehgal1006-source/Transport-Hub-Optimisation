Birmingham Transport Hub Clustering & Accessibility Mapper

A project that uses data from OpenStreetMap, K=Means Clustering and user input to create a select number of transport hubs around the city of Birmingham. It aims to find the most optimal hub locations based on address/population density.

Overview:

Residential data is downloaded based on the city of Birmingham. This data then gets grouped into K number of clusters using K-Means clustering. The script then asks for user input of an address in Birmingham, whereby the distance from the address and nearest transport hub is calculated. This is then visualized on a Folium map which you can interact with.

Features:

OpenStreetMap Integration: Downloads real residential building data for Birmingham using "osmnx".
K-Means Clustering: Groups residential points into k cluster counts (`k=200` by default) to optimize potential transport hub placements.
Distance Analysis: Calculates straight-line and walking distances from buildings to the nearest hub.
Interactive Mapping: Generates a custom HTML map (`birmingham_transport_clusters.html`) featuring color-coded clusters, hub markers, and user to hub pathing.

Dependencies:

Copy and Paste the following into your terminal to download the requirements to run this project:
pip install requests osmnx geopandas pandas scikit-learn numpy geopy folium

How to run the code:
1) Run the following:

   git clone https://github.com/yogeshsehgal1006-source/Transport-Hub-Optimisation.git

2) Then create the following directory:

   cd Transport-Hub-Optimisation

3) Then set up a virtual environment:

   python -m venv venv
   
   venv\Scripts\activate

   or (Mac/Linux)

   python3 -m venv venv

   source venv/bin/activate

4) Install the Dependencies:

   pip install requests osmnx geopandas pandas scikit-learn numpy geopy folium

5) Then run the following:

   python Transport Hub Optimisation.py











