import pandas as pd
import numpy as np
from clustering_utils import preprocess_data, scale_coordinates, run_hdbscan
import warnings
warnings.filterwarnings("ignore",category=FutureWarning)

def test_hdbscan_clusters():
    import numpy as np
    import pandas as pd
    from clustering_utils import scale_coordinates, run_hdbscan

    # Generate two dense clusters manually
    lat1 = np.full(5, 45.4)
    long1 = np.linspace(-75.6, -75.595, 5)

    lat2 = np.full(5, 45.5)
    long2 = np.linspace(-75.5, -75.495, 5)

    df = pd.DataFrame({
        'Latitude': np.concatenate([lat1, lat2]),
        'Longitude': np.concatenate([long1, long2])
    })

    coords_scaled = scale_coordinates(df)
    labels = run_hdbscan(coords_scaled, min_cluster_size=3)

    print("Labels:", labels)
    assert len(labels) == 10
    assert np.any(labels != -1), "All points marked as noise"
    assert len(set(labels)) > 1, "Only one or no clusters found"
