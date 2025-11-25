
"""
organize_music.py
Organize audio files into folders by genre/artist using metadata CSV.
Usage:
    python music_app/extras/organize_music.py --csv data/music_dataset_500.csv --audio data/audio --dest organized_music
"""
import argparse
from pathlib import Path
import shutil
import pandas as pd
import os

def organize(csv_path, audio_folder, dest):
    df = pd.read_csv(csv_path)
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    audio_folder = Path(audio_folder)
    for _, r in df.iterrows():
        gid = r.get("genre","Unknown")
        artist = r.get("artist","Unknown")
        track_id = str(r.get("track_id",""))
        title = str(r.get("title",""))
        # try to find file by track id or title
        found = None
        for ext in ("*.mp3","*.wav","*.flac","*.m4a","*.ogg"):
            if audio_folder.exists():
                for f in audio_folder.rglob(ext):
                    name = f.name.lower()
                    if track_id and track_id.lower() in name:
                        found = f
                        break
                    if title and title.lower().replace(" ","") in name.replace(" ",""):
                        found = f
                        break
            if found:
                break
        target_dir = dest / (gid or "Unknown") / (artist or "Unknown")
        target_dir.mkdir(parents=True, exist_ok=True)
        if found:
            try:
                shutil.copy(found, target_dir / found.name)
                print("copied", found, "to", target_dir)
            except Exception as e:
                print("copy error", found, e)
    print("Organization complete at", dest)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="data/music_dataset_500.csv")
    parser.add_argument("--audio", default="data/audio")
    parser.add_argument("--dest", default="organized_music")
    args = parser.parse_args()
    organize(args.csv, args.audio, args.dest)
