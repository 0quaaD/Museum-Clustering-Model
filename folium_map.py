import folium
import pandas as pd
import hdbscan as hdb
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
# Function to create folium map with clusters (DBSCAN & HDBSCAN)
def create_folium_map(df):
    # Assuming 'df' contains 'Latitude', 'Longitude', and 'Cluster' columns
    map_center = [df['Latitude'].mean(), df['Longitude'].mean()]
    folium_map = folium.Map(location=map_center, zoom_start=10)

    # Create Layer Groups
    dbscan_layer = folium.FeatureGroup(name='DBSCAN Clusters')
    hdbscan_layer = folium.FeatureGroup(name='HDBSCAN Clusters')

    # Plot DBSCAN results
    for _, row in df.iterrows():
        if row['Cluster_DBSCAN'] != -1:  # Assuming 'Cluster_DBSCAN' column
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=5,
                color='blue',
                fill=True,
                fill_color='blue',
                fill_opacity=0.6,
                popup=f"{row['Facility_Name']} (DBSCAN Cluster {row['Cluster_DBSCAN']})"
            ).add_to(dbscan_layer)

    # Plot HDBSCAN results
    for _, row in df.iterrows():
        if row['Cluster_HDBSCAN'] != -1:  # Assuming 'Cluster_HDBSCAN' column
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=5,
                color='green',
                fill=True,
                fill_color='green',
                fill_opacity=0.6,
                popup=f"{row['Facility_Name']} (HDBSCAN Cluster {row['Cluster_HDBSCAN']})"
            ).add_to(hdbscan_layer)

    # Add layers and LayerControl
    dbscan_layer.add_to(folium_map)
    hdbscan_layer.add_to(folium_map)
    folium.LayerControl().add_to(folium_map)

    return folium_map

# Read the dataset
df1 = pd.read_csv('./dataset/ODCAF-v1-0.csv', on_bad_lines='warn', encoding='ISO-8859-1')

# Preprocessing: Clean Latitude and Longitude columns
df1 = df1[df1['Latitude'] != '..']
for col in ['Latitude', 'Longitude']:
    df1[col] = df1[col].str.strip().str.rstrip(',').astype(float)

coords = df1[['Latitude', 'Longitude']]
coords_scaled = StandardScaler().fit_transform(coords)

dbscan_labels = DBSCAN(eps = 1.0, metric='euclidean', min_samples=3).fit_predict(coords_scaled)
hdbscan_labels = hdb.HDBSCAN(metric='euclidean', min_samples = None, min_cluster_size=3).fit_predict(coords_scaled)

df1['Cluster_DBSCAN'] = dbscan_labels
df1['Cluster_HDBSCAN'] = hdbscan_labels

# Create and save the interactive folium map
interactive_map = create_folium_map(df1)
interactive_map.save("museum_clusters_map.html")  # Save as HTML file

