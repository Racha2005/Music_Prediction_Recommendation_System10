import pandas as pd
import numpy as np
import os

BASE = os.path.join(os.path.dirname(__file__), "..", "data")
df = pd.read_csv(os.path.join(BASE, "music_dataset_500.csv"))

def recommend(seed_track_id, top_k=10):
    seed = df[df['track_id']==seed_track_id].iloc[0]
    def score_row(r):
        s = 0
        s += 2.0 if r['genre'] == seed['genre'] else 0.0
        s -= abs(r['popularity'] - seed['popularity'])/100.0
        s -= sum(abs(r[f]-seed[f]) for f in ['danceability','energy','acousticness','valence'])
        return s
    df['score_tmp'] = df.apply(score_row, axis=1)
    recs = df.sort_values('score_tmp', ascending=False).query("track_id!=@seed_track_id").head(top_k)
    return recs[['track_id','title','artist','genre','popularity']].to_dict(orient='records')

if __name__ == "__main__":
    print(recommend("track_1", top_k=5))
