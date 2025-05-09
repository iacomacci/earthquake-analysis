import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
from branca.element import Template, MacroElement
from jinja2 import Template
import folium
from folium import Popup
from fetch_earthquakes import get_earthquake_data
from map_templates import earthquakes_DBSCAN_map_title_html, earthquakes_DBSCAN_map_build_legend_html

df, yearly, monthly = get_earthquake_data()

X = df[['latitude', 'longitude', 'depth_km', 'magnitude']].copy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

def k_distance_graph(X_scaled):
    # Calculate the k-distance graph to help choose eps for DBSCAN
    # X_scaled: scaled data
    # k: number of neighbors to consider (min_samples in DBSCAN)
    # This function will plot the sorted distances to the k-th nearest neighbor

    # Number of neighbors (k) to consider for DBSCAN
    #k = min_samples (common choice: 4 or 5)
    k = 5  
    neighbors = NearestNeighbors(n_neighbors=k)
    neighbors_fit = neighbors.fit(X_scaled)

    # Get distances to the k-th nearest neighbor
    distances, indices = neighbors_fit.kneighbors(X_scaled)

    # Get the distance to the k-th neighbor for each point
    k_distances = np.sort(distances[:, k - 1])

    # Plot the sorted distances
    plt.figure(figsize=(8, 4))
    plt.plot(k_distances)
    plt.xlabel("Points sorted by distance")
    plt.ylabel(f"{k}th nearest neighbor distance")
    plt.title("k-distance Graph to Help Choose eps for DBSCAN")
    plt.grid(True)
    plt.show(block=False)   
    plt.pause(5)  # Pause for 5 seconds
    plt.close()

#k_distance_graph(X_scaled) # Uncomment this line to visualize the k-distance graph

dbscan = DBSCAN(eps=0.48, min_samples=5) # eps was chosen based on the k-distance graph (Elbow method)
labels = dbscan.fit_predict(X_scaled)
df['cluster'] = labels

# Center the map (e.g., around mean location)
map_center = [df['latitude'].mean(), df['longitude'].mean()]
map_all_clusters = folium.Map(location=map_center, zoom_start=2) #Map 1 will include all clusters. 
map_without_noise = folium.Map(location=map_center, zoom_start=2) #Map 2 will exclude noise.


# Number of unique clusters excluding noise
n_clusters = df['cluster'].nunique() - (1 if -1 in df['cluster'].values else 0)
colormap = cm.get_cmap('YlOrRd', n_clusters)

# Create a color dictionary
cluster_labels = sorted(df['cluster'].unique())
color_dict = {}
for i, label in enumerate(cluster_labels):
    if label == -1:
        color_dict[label] = 'black'  # noise
    else:
        rgb = colormap(i)[:3]
        color_dict[label] = colors.to_hex(rgb)

def create_popup(row):
    #Popup html setup
    return Popup(f"""
        <table style="font-size: 12px;">
        <tr><td><strong>Magnitude:</strong></td><td>{row['magnitude']}</td></tr>
        <tr><td><strong>Cluster:</strong></td><td>{row['cluster']}</td></tr>
        <tr><td><strong>Depth:</strong></td><td>{row['depth_km']} km</td></tr>
        </table>
    """, max_width=250)

def add_markers(map_obj, data):
    for _, row in data.iterrows():
        popup = create_popup(row)
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=2 + row['magnitude'],
            color=color_dict[row['cluster']],
            fill=True,
            fill_opacity=0.4,
            popup=popup
        ).add_to(map_obj)

for _, row in df.iterrows():

    popup_html_defined = create_popup(row)
add_markers(map_all_clusters, df)

# Filter out noise points (label == -1)
clustered_df = df[df['cluster'] != -1]

for _, row in clustered_df.iterrows():

    popup_html_defined = create_popup(row)
add_markers(map_without_noise, clustered_df)

clean_color_dict = {int(k): v for k, v in color_dict.items()}

legend_template = earthquakes_DBSCAN_map_build_legend_html(clean_color_dict)

class Legend(MacroElement):
    def __init__(self):
        super().__init__()
        self._template = Template(legend_template)

map_all_clusters.get_root().add_child(Legend())
map_without_noise.get_root().add_child(Legend())

macro1 = MacroElement()
macro1._template = Template(earthquakes_DBSCAN_map_title_html)
macro2 = MacroElement()
macro2._template = Template(earthquakes_DBSCAN_map_title_html)
map_all_clusters.get_root().add_child(macro1)
map_without_noise.get_root().add_child(macro2)

map_all_clusters.save("clustered_earthquakes_map.html")
map_without_noise.save("non_noise_clustered_earthquakes_map.html")