# 🎵 Music Prediction & Recommendation Analysis Project

### ▶ Run the Streamlit Dashboard
`streamlit run music_app/app_streamlit/streamlit_dashboard_dark.py`

### ▶ Run Desktop Demo
`python -m music_app.app_desktop.desktop_app`  
(or)  
`python music_app/app_desktop/desktop_app.py`

### ▶ Train ML Models
`python -m music_app.ml.train_popularity`  
`python -m music_app.ml.train_mood`



# Music Prediction and Recommendation System

A complete end-to-end **Music Intelligence System** featuring:

- 🌐 Streamlit Analytics Dashboard  
- 💻 Tkinter Desktop App  
- 🤖 ML Models (Popularity + Mood)  
- 🎧 Audio Feature Extraction  
- 🖼️ Album Cover Image Hashing  
- 📝 Lyrics Sentiment Analysis  
- 🔍 UMAP + KMeans Clustering  
- 🎼 Content-Based Recommender  
- 🌙 Modern Dark Neon UI  



## ⭐ Overview

This system helps users:

- Analyze music trends  
- Predict popularity  
- Understand mood & energy  
- Explore genre patterns  
- View BI-style dashboards  
- Generate recommendations  
- Perform audio, image & lyrics analysis  
- Use both web & desktop interfaces  



## 📁 Folder Structure

music_prediction_recommendation_analysis_project/  
│  
├── setup.py  
├── pyproject.toml  
├── requirements.txt  
│  
├── data/  
│ ├── music_dataset_500.csv  
│ ├── audio_features.csv  
│ ├── image_hashes.csv  
│ ├── lyrics_analysis.csv  
│ ├── clusters.csv  
│ ├── covers/  
│ └── audio/  
│  
└── music_app/  
   ├── config.py  
   ├── cli.py  
   │  
   ├── models/  
   │ ├── popularity_rf.joblib  
   │ └── mood_rf.joblib  
   │  
   ├── ml/  
   │ ├── train_popularity.py  
   │ ├── train_mood.py  
   │ ├── recommender.py  
   │  
   ├── extras/  
   │ ├── audio_features.py  
   │ ├── image_hashing.py  
   │ ├── lyrics_analysis.py  
   │ ├── clustering.py  
   │ ├── recommenders.py  
   │ ├── organize_music.py  
   │ └── voice_commands.py  
   │  
   ├── app_streamlit/  
   │ └── streamlit_dashboard_dark.py  
   │  
   ├── app_desktop/  
   │ └── desktop_app.py  
   │  
   └── app_flask/  
       ├── app.py  
       └── templates/  
           └── index.html  



## 🚀 Run Commands

### Activate Virtual Environment
```
.venv\Scripts\Activate.ps1
```

### Streamlit Dashboard
```
streamlit run music_app/app_streamlit/streamlit_dashboard_dark.py
```

### Desktop App
```
python music_app/app_desktop/desktop_app.py
```

### Train ML Models
```
python -m music_app.ml.train_popularity
python -m music_app.ml.train_mood
```

### Extract Audio Features
```
python music_app/extras/audio_features.py --folder data/audio --out data/audio_features.csv
```

### Generate Image Hashes
```
python music_app/extras/image_hashing.py --folder data/covers --out data/image_hashes.csv
```

### Lyrics Sentiment Analysis
```
python music_app/extras/lyrics_analysis.py --csv data/music_dataset_500.csv --out data/lyrics_analysis.csv
```

### UMAP + KMeans Clustering
```
python music_app/extras/clustering.py --features data/audio_features.csv --out data/clusters.csv --n 8
```



## 📊 Features

### 1. Streamlit Dashboard (Dark Neon)
- KPI cards  
- Genre distribution (bar, donut)  
- Popularity vs tempo  
- Mood distribution  
- Energy histogram  
- Filters (genre, artist, duration)  
- Recommendation table  
- Image hashing viewer  
- Audio features view  
- Lyrics sentiment  
- Cluster visualization  



### 2. Tkinter Desktop App
- Top tracks list  
- Genre chart  
- Recommendation popup  
- Audio import  
- Lightweight & offline  



## 🤖 Machine Learning Models

### Popularity Model
- RandomForestRegressor  
- Inputs: energy, valence, acousticness, danceability, tempo, duration  

### Mood Model
- RandomForestClassifier  
- Output: Positive / Neutral-Calm  

### Content-Based Recommender
Uses genre match, popularity gap, and feature distance.



## 📦 Technologies Used

### Core  
Python, Streamlit, Tkinter  

### ML  
scikit-learn, numpy, pandas, joblib  

### Audio / Text / Image  
librosa, nltk, pillow, imagehash  

### Clustering  
UMAP, KMeans



## 🎼 Dataset Info

Contains 500 tracks with:  
Genre, artist, title, duration, tempo  
Energy, valence, danceability  
Acousticness, loudness  
Popularity score  



## 🎯 Purpose

Ideal for:  
- Internship submissions  
- College projects  
- ML + Data Visualization learning  
- Portfolio-grade showcase  



## 🔥 Key Outcomes

- Analytics dashboard  
- Desktop app  
- ML predictions  
- Audio, image & lyrics analysis  
- Intelligent recommendations  



## 📄 License

MIT License
