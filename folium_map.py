import folium
from folium.plugins import MarkerCluster
import pandas as pd

def create_folium_map(df, title="Museum Clusters"):
    """
    Create an interactive map to visualize museum clusters using Folium.
    
    Args:
        df (DataFrame): Dataframe containing museum locations and clusters.
        title (str): The title of the map.
    
    Returns:
        folium.Map: Interactive folium map.
    """
    # Create a base map centered around the average location of the museums
    map_center = [df['Latitude'].mean(), df['Longitude'].mean()]
    m = folium.Map(location=map_center, zoom_start=12, control_scale=True)
    
    # Create a MarkerCluster to group nearby markers
    marker_cluster = MarkerCluster().add_to(m)
    
    # Add markers for each museum
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=8,
            popup=f"{row['Facility_Name']} - Cluster: {row['Cluster']}",
            color=f"#{hex(row['Cluster'] * 10)[2:]}0000",  # Color by cluster index (just a simple method)
            fill=True,
            fill_color=f"#{hex(row['Cluster'] * 10)[2:]}0000",
            fill_opacity=0.7,
        ).add_to(marker_cluster)
    
    # Add a title (optional)
    folium.CustomIcon("https://www.google.com/favicon.ico", icon_size=(30, 30))  # Example icon
    folium.Marker(
        location=map_center,
        popup=title,
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

    return m

# Now you can create and save the folium map
# Assuming `df` is your dataframe containing museum data with 'Latitude', 'Longitude', and 'Cluster' columns.
#df = pd.read_csv('./dataset/ODCAF-v1-0.csv',on_bad_lines = 'warn', encoding='ISO-8859-1')

# Example DataFrame
df = pd.DataFrame({
    'Facility_Name': ['Museum A', 'Museum B', 'Museum C', 'Museum D'],
    'Latitude': [45.4, 45.401, 45.402, 45.403],
    'Longitude': [-75.6, -75.601, -75.602, -75.603],
    'Cluster': [0, 1, 2, 0]
})
interactive_map = create_folium_map(df)
interactive_map.save("museum_clusters_map.html")  # Save the map as an HTML file

# Optionally, you can display the map in a Jupyter notebook or Streamlit app
# For Streamlit: st.components.v1.html(interactive_map._repr_html_(), height=500)
