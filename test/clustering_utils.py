import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import hdbscan

def preprocess_data(df):
    df = df[df['Latitude'].notnull() & df['Longitude'].notnull()]
    df = df[df['Latitude'] != '..']
    for col in ['Latitude', 'Longitude']:
        df[col] = df[col].astype(str).str.strip().str.rstrip(',').astype(float)
    return df

def scale_coordinates(df, multiplier=2.0):
    coords = df[['Latitude', 'Longitude']].copy()
    coords['Latitude'] = multiplier * coords['Latitude']
    return StandardScaler().fit_transform(coords)

def run_dbscan(coords_scaled, eps=1.0, min_samples=3, metric='euclidean'):
    model = DBSCAN(eps=eps, min_samples=min_samples, metric=metric)
    return model.fit_predict(coords_scaled)

def run_hdbscan(coords_scaled, min_cluster_size=3, min_samples=None, metric='euclidean'):
    model = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples, metric=metric)
    return model.fit_predict(coords_scaled)
