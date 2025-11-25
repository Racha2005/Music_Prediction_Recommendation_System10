import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Dataset
DATA_LOCAL = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "music_dataset_500.csv"))
DATA_FALLBACK = DATA_LOCAL  # fallback same file

# Model paths
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_POP = os.path.join(MODEL_DIR, "popularity_rf.pkl")
MODEL_MOOD = os.path.join(MODEL_DIR, "mood_clf.pkl")
