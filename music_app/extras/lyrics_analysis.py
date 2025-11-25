
"""
lyrics_analysis.py
Perform basic sentiment analysis on lyrics column using NLTK VADER if available.
Outputs data/lyrics_analysis.csv with sentiment scores.
Usage:
    python music_app/extras/lyrics_analysis.py --csv data/music_dataset_500.csv --out data/lyrics_analysis.csv
"""
import argparse
from pathlib import Path
import pandas as pd
import numpy as np

def analyze(csv_path, out):
    df = pd.read_csv(csv_path)
    if "lyrics" not in df.columns:
        df["lyrics"] = ""
    # try to use nltk vader
    try:
        from nltk.sentiment import SentimentIntensityAnalyzer
        import nltk
        try:
            nltk.data.find('sentiment/vader_lexicon.zip')
        except:
            nltk.download('vader_lexicon')
        sia = SentimentIntensityAnalyzer()
        df["lyrics_sentiment_compound"] = df["lyrics"].fillna("").astype(str).apply(lambda x: sia.polarity_scores(x)["compound"] if x.strip() else 0.0)
    except Exception as e:
        print("NLTK VADER not available; using naive sentiment placeholder.")
        df["lyrics_sentiment_compound"] = df["lyrics"].fillna("").astype(str).apply(lambda x: 0.0)
    df.to_csv(out, index=False)
    print("Lyrics analysis saved to", out)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="data/music_dataset_500.csv")
    parser.add_argument("--out", default="data/lyrics_analysis.csv")
    args = parser.parse_args()
    analyze(args.csv, args.out)
