
"""
image_hashing.py
Compute perceptual hashes for images and find duplicates/similar images.
Usage:
    python music_app/extras/image_hashing.py --folder data/covers --out data/image_hashes.csv
"""
import argparse
from pathlib import Path
import pandas as pd
try:
    from PIL import Image
    import imagehash
except Exception as e:
    Image = None
    imagehash = None

def compute(folder, out):
    p = Path(folder)
    rows = []
    if Image is None or imagehash is None:
        raise RuntimeError("Pillow and imagehash are required. Install: pip install Pillow imagehash")
    for ext in ("*.png","*.jpg","*.jpeg","*.bmp"):
        for f in p.rglob(ext):
            try:
                h = str(imagehash.average_hash(Image.open(f)))
                rows.append({"file": str(f), "hash": h})
            except Exception as e:
                print("skip", f, e)
    if rows:
        df = pd.DataFrame(rows)
        df.to_csv(out, index=False)
        print("Saved", out)
    else:
        print("No images found in", folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", default="data/covers")
    parser.add_argument("--out", default="data/image_hashes.csv")
    args = parser.parse_args()
    compute(args.folder, args.out)
