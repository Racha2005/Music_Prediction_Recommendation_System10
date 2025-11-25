# music_app/ml/train_mood.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
import os

# BASE path → project/data/
BASE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "data"
)

print(f"Loading dataset: {os.path.join(BASE, 'music_dataset_500.csv')}")

# Load dataset
df = pd.read_csv(os.path.join(BASE, "music_dataset_500.csv"))

# Create synthetic mood labels (based on valence & energy)
df['mood'] = np.where(
    (df['valence'] > 0.5) & (df['energy'] > 0.5), 
    "Energetic",
    np.where(df['valence'] > 0.5, "Happy",
    np.where(df['energy'] < 0.3, "Sad", "Calm"))
)

# Features
X = df[['danceability', 'energy', 'acousticness', 'valence', 'tempo']]
y = df['mood']

# Train split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Classifier
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Show metrics
print("\n", classification_report(y_test, y_pred))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
moods = sorted(df['mood'].unique())

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Purples',
            xticklabels=moods, yticklabels=moods)
plt.title("Mood Prediction Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# Save model
model_path = os.path.join(os.path.dirname(__file__), "..", "models", "mood_clf.pkl")
joblib.dump(model, model_path)

print(f"\n🎉 Saved mood model: {model_path}")