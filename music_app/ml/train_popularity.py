# music_app/ml/train_popularity.py

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

# Correct BASE path → project/data/
BASE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "data"
)

# Load dataset
df = pd.read_csv(os.path.join(BASE, "music_dataset_500.csv"))

# Features and target
X = df[['duration_sec', 'danceability', 'energy', 'acousticness', 'valence', 'tempo']]
y = df['popularity']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestRegressor(n_estimators=120, random_state=42)
model.fit(X_train, y_train)

# Evaluation
print("\n🎯 Train R² Score:", model.score(X_test, y_test))

# Save model inside music_app/models/
model_path = os.path.join(os.path.dirname(__file__), "..", "models", "popularity_rf.joblib")
joblib.dump(model, model_path)

print(f"\n✅ Saved popularity model → {model_path}")