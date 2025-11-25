
"""
clustering.py
Cluster audio features using KMeans and produce UMAP or PCA embedding.
Usage:
    python music_app/extras/clustering.py --features data/audio_features.csv --out data/clusters.csv --n 8
"""
import argparse
from pathlib import Path
import pandas as pd
import numpy as np

def cluster(features_csv, out_csv, n_clusters=8):
    if not Path(features_csv).exists():
        print("Features CSV not found:", features_csv)
        return
    df = pd.read_csv(features_csv)
    X = df.select_dtypes(include=[float,int]).fillna(0)
    # use sklearn KMeans
    try:
        from sklearn.cluster import KMeans
        km = KMeans(n_clusters=n_clusters, random_state=42)
        labels = km.fit_predict(X)
        df["cluster"] = labels
    except Exception as e:
        print("sklearn not available", e)
        df["cluster"] = 0
    # compute 2D embedding with umap or PCA
    try:
        import umap
        reducer = umap.UMAP(n_components=2, random_state=42)
        emb = reducer.fit_transform(X)
        df["umap_x"] = emb[:,0]
        df["umap_y"] = emb[:,1]
    except Exception:
        from sklearn.decomposition import PCA
        pca = PCA(n_components=2)
        emb = pca.fit_transform(X)
        df["umap_x"] = emb[:,0]
        df["umap_y"] = emb[:,1]
    df.to_csv(out_csv, index=False)
    print("Clusters saved to", out_csv)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", default="data/audio_features.csv")
    parser.add_argument("--out", default="data/clusters.csv")
    parser.add_argument("--n", type=int, default=8)
    args = parser.parse_args()
    cluster(args.features, args.out, args.n)
