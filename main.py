import requests
import zipfile
import io
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import hdbscan
from sklearn.preprocessing import StandardScaler

import geopandas as gpd
import contextily as ctx
from shapely.geometry import Point
import warnings
warnings.filterwarnings('ignore')

zip_file_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/YcUk-ytgrPkmvZAh5bf7zA/Canada.zip"

# directory to save the extracted zip files
output_dirs = './'
os.makedirs(output_dirs, exist_ok=True)

# Download the zip file
response = requests.get(zip_file_url)
response.raise_for_status()

# Open the zip file in Memory
with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
    for file_name in zip_ref.namelist():
        if file_name.endswith('.tif'):
            zip_ref.extract(file_name, output_dirs)
            print(f"Downloaded and Extracted {file_name}")



def plot_clustered_locations(df, title="Museums Clustered by Proximity"):
    # required parameters form df --> Latitude, Longitude and Cluster columns

    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']), crs='EPSG:4326')
    gdf = gdf.to_crs(epsg=3857)

    fig, ax = plt.subplots(figsize=(15,10))
    
    non_noise = gdf[gdf['Cluster'] != -1]
    noise = gdf[gdf['Cluster'] == -1]
    
    noise.plot(ax=ax, color='k', markersize=30, ec='r', alpha=1, label='Noise')
    non_noise.plot(ax=ax, column='Cluster', markersize=30, cmap='tab10', ec='k', legend=False, alpha=0.6)

    ctx.add_basemap(ax, source='./Canada.tif',zoom=4)

    plt.title(title, )
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    ax.set_xticks([])
    ax.set_yticks([])
    plt.tight_layout()
    plt.show()

# -------- End of the function --------
url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/r-maSj5Yegvw2sJraT15FA/ODCAF-v1-0.csv'

df = pd.read_csv(url, on_bad_lines = 'warn', encoding = 'ISO-8859-1')
df = df[df['Latitude'] != '..']
df = df[df['Facility_Name'] != '#Hashtag Gallery']
for cols in ['Latitude', 'Longitude']:
    df[cols] = df[cols].str.strip().str.rstrip(',').astype(float)

print(type(df[['Latitude', 'Longitude']].values))

coords = df[['Latitude', 'Longitude']]
coords['Latitude'] = 2 * coords['Latitude']

# Set DBSCAN parameters with Eucledian distance
coords_scaled_ = StandardScaler().fit_transform(coords)

min_samples = 3
eps = 1.0
metric='euclidean'

dbscan = DBSCAN(eps=eps, min_samples = min_samples, metric = metric).fit(coords_scaled_)

df['Cluster'] = dbscan.fit_predict(coords_scaled_)
print(df['Cluster'].value_counts())

plot_clustered_locations(df, title='Museum Clustered by Proximity')

coords = df[['Latitude','Longitude']]
coords["Latitude"] = 2*coords["Latitude"]

scaler = StandardScaler()
coords_scaled = scaler.fit_transform(coords)
min_samples = None


df['Cluster'] = dbscan.fit_predict(coords_scaled_)
print(df['Cluster'].value_counts())

hdb = hdbscan.HDBSCAN(min_samples = min_samples, min_cluster_size=3,metric = metric)

df['Cluster'] = hdb.fit_predict(coords_scaled_)
print(df['Cluster'].value_counts())

plot_clustered_locations(df, title='Museums Hierarchically Clustered by Proximity')
