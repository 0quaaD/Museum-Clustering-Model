import pandas as pd
import numpy as np
from clustering_utils import preprocess_data, scale_coordinates, run_dbscan

def test_dbscan_clusters():
    df = pd.DataFrame({
        'Latitude': [45.4, 45.401, 43.6],
        'Longitude': [-75.6, -75.601, -79.4]
    })
    coords_scaled = scale_coordinates(df)
    labels = run_dbscan(coords_scaled, eps=0.5, min_samples=1)

    assert len(labels) == 3
    assert np.all(labels >= 0)

