
"""
recommenders.py
Provides: content_based, collaborative_simple (item-based), hybrid recommendation functions.
Usage (example usage inside main):
    python music_app/extras/recommenders.py --csv data/music_dataset_500.csv --seed TRACK_ID
"""
import argparse
from pathlib import Path
import pandas as pd
import numpy as np

def content_based(df, seed_id, top_k=10):
    features = ["danceability","energy","acousticness","valence"]
    for f in features:
        if f not in df.columns:
            df[f] = 0.0
    X = df[features].fillna(0).values
    ids = df["track_id"].values
    try:
        from sklearn.metrics.pairwise import cosine_similarity
        cos = cosine_similarity(X, X)
        idx = int(np.where(ids==seed_id)[0][0])
        scores = list(enumerate(cos[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        selected = [i for i,_ in scores[1:top_k+1]]
        return df.iloc[selected][["track_id","title","artist","genre","popularity"]].to_dict(orient="records")
    except Exception as e:
        print("sklearn not available; returning top popular tracks")
        return df.sort_values("popularity", ascending=False).head(top_k)[["track_id","title","artist","genre","popularity"]].to_dict(orient="records")

def collaborative_simple(df, user_item=None, top_k=10):
    """
    Placeholder simple collaborative: expects user_item matrix with users as rows; items columns.
    For now returns popular tracks as placeholder.
    """
    return df.sort_values("popularity", ascending=False).head(top_k)[["track_id","title","artist","genre","popularity"]].to_dict(orient="records")

def hybrid(df, seed_id, top_k=10):
    cb = content_based(df, seed_id, top_k=top_k*2)
    # boost by popularity
    df_map = {r["track_id"]: r for r in df.to_dict(orient="records")}
    out = []
    for r in cb:
        score = r.get("popularity",0)
        out.append((score, r))
    out = sorted(out, key=lambda x: x[0], reverse=True)
    return [r for _,r in out[:top_k]]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="data/music_dataset_500.csv")
    parser.add_argument("--seed", required=False)
    parser.add_argument("--top", type=int, default=10)
    args = parser.parse_args()
    df = pd.read_csv(args.csv)
    seed = args.seed if args.seed else df["track_id"].iloc[0]
    recs = content_based(df, seed, top_k=args.top)
    print("Recommendations for", seed)
    for r in recs:
        print(r)
