
"""
audio_features.py
Extracts audio features from a folder of audio files using librosa.
Outputs CSV with MFCC, ZCR, spectral contrast, chroma, tonnetz, tempo, duration.
Usage:
    python music_app/extras/audio_features.py --folder data/audio --out data/audio_features.csv
"""
import os
from pathlib import Path
import argparse
import numpy as np
import pandas as pd

def extract(path):
    try:
        import librosa
    except Exception as e:
        raise RuntimeError("librosa is required. Install with: pip install librosa") from e
    y, sr = librosa.load(path, sr=None, mono=True)
    features = {}
    features["filename"] = os.path.basename(path)
    features["duration"] = float(librosa.get_duration(y=y, sr=sr))
    # tempo (BPM)
    try:
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        features["tempo"] = float(tempo)
    except Exception:
        features["tempo"] = np.nan
    # zero crossing
    try:
        features["zcr"] = float(np.mean(librosa.feature.zero_crossing_rate(y)[0]))
    except Exception:
        features["zcr"] = np.nan
    # spectral contrast and centroid
    try:
        features["spectral_centroid"] = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)[0]))
    except Exception:
        features["spectral_centroid"] = np.nan
    try:
        sc = librosa.feature.spectral_contrast(y=y, sr=sr)
        features["spectral_contrast_mean"] = float(np.mean(sc))
    except Exception:
        features["spectral_contrast_mean"] = np.nan
    # chroma
    try:
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        features["chroma_mean"] = float(np.mean(chroma))
    except Exception:
        features["chroma_mean"] = np.nan
    # tonnetz
    try:
        ton = librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr)
        features["tonnetz_mean"] = float(np.mean(ton))
    except Exception:
        features["tonnetz_mean"] = np.nan
    # mfccs mean
    try:
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        for i in range(mfccs.shape[0]):
            features[f"mfcc_{i+1}_mean"] = float(np.mean(mfccs[i]))
    except Exception:
        for i in range(13):
            features[f"mfcc_{i+1}_mean"] = np.nan
    return features

def process_folder(folder, out_csv):
    folder = Path(folder)
    rows = []
    exts = ["*.wav","*.mp3","*.flac","*.m4a","*.aac","*.ogg"]
    for ext in exts:
        for f in folder.rglob(ext):
            try:
                rows.append(extract(str(f)))
                print("extracted:", f)
            except Exception as e:
                print("skip:", f, "error:", e)
    if rows:
        df = pd.DataFrame(rows)
        df.to_csv(out_csv, index=False)
        print("Saved", out_csv)
    else:
        print("No audio files processed - check folder path or formats.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", default="data/audio")
    parser.add_argument("--out", default="data/audio_features.csv")
    args = parser.parse_args()
    process_folder(args.folder, args.out)
