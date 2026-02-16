import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os
import imagehash

# ---------------------------
#     PAGE CONFIG
# ---------------------------
st.set_page_config(
    layout="wide",
    page_title="Music Prediction & Recommendation Dashboard",
    page_icon="🎧"
)

# ---------------------------
#     COLOR PALETTE
# ---------------------------
PALETTE = [
    "#7c3aed",  # Purple
    "#00e5ff",  # Cyan
    "#ff7ab6",  # Pink
    "#ffd166",  # Yellow
    "#7ee081",  # Green
    "#ffa156",  # Orange
    "#6b7cff"   # Blue
]

# ---------------------------
#     DARK NEON CSS
# ---------------------------
st.markdown("""
<style>
.stApp { background-color: #07090d; color: #e6f7ff; }
.big-title { color: #00e5ff; font-size:30px; font-weight:700; }
.subtle { color: #9bdcff; margin-bottom:15px; }
.card {
    background: linear-gradient(90deg, rgba(20,25,40,0.95), rgba(10,12,18,0.95));
    padding: 14px;
    border-radius: 12px;
    box-shadow: 0 6px 18px rgba(124,58,237,0.15);
}
.kpi { font-size:26px; font-weight:800; color:white; }
.kpi-sublabel { color:#9bdcff; font-size:13px; }
</style>
""", unsafe_allow_html=True)

# ---------------------------
#       BANNERS
# ---------------------------
banners = [
    "/mnt/data/a86fe0fa-cbb8-46e4-9899-bfc773eb081f.png",
    "/mnt/data/e2cac4a1-3508-48cb-bb5b-c751c6631adc.png",
    "/mnt/data/0b630ca9-0743-4fb8-8dca-92e21fb1e59e.png",
]

cols = st.columns(3)
for c, img in zip(cols, banners):
    try:
        c.image(Image.open(img), use_column_width=True)
    except:
        pass

st.markdown("<div class='big-title'>Music Prediction & Recommendation Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='subtle'>Colorful BI layout — KPIs, charts, clusters & artwork similarity</div>", unsafe_allow_html=True)


# ---------------------------
#     LOAD DATASET
# ---------------------------
data_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "music_dataset_500.csv")
df = pd.read_csv(data_path)

# ---------------------------
#     SIDEBAR FILTERS
# ---------------------------
with st.sidebar:
    st.header("Filters")

    gen_filter = st.multiselect("Genre",
        options=sorted(df["genre"].unique()),
        default=sorted(df["genre"].unique())
    )

    artist_filter = st.selectbox("Artist (optional)", ["All"] + sorted(df["artist"].unique()))

    min_pop = st.slider("Min Popularity", 0, 100, 1)

    duration = st.slider(
        "Duration (sec)",
        int(df["duration_sec"].min()),
        int(df["duration_sec"].max()),
        (120, 420)
    )

    show_recs = st.checkbox("Show recommendations", True)

    st.markdown("---")
    st.write("Charts use white backgrounds for BI-style clarity.")

# ---------------------------
#     APPLY FILTERS
# ---------------------------
q = df[
    (df["genre"].isin(gen_filter)) &
    (df["popularity"] >= min_pop) &
    (df["duration_sec"].between(duration[0], duration[1]))
]

if artist_filter != "All":
    q = q[q["artist"] == artist_filter]

# ---------------------------
#     TOP KPI CARDS
# ---------------------------
k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(f"<div class='card'><div class='kpi'>{len(q)}</div><div class='kpi-sublabel'>Tracks (Filtered)</div></div>", unsafe_allow_html=True)

with k2:
    st.markdown(f"<div class='card'><div class='kpi'>{q['popularity'].mean():.1f}</div><div class='kpi-sublabel'>Avg Popularity</div></div>", unsafe_allow_html=True)

with k3:
    tg = q["genre"].value_counts().idxmax() if len(q) > 0 else "N/A"
    st.markdown(f"<div class='card'><div class='kpi'>{tg}</div><div class='kpi-sublabel'>Top Genre</div></div>", unsafe_allow_html=True)

with k4:
    ad = q["duration_sec"].mean()
    st.markdown(f"<div class='card'><div class='kpi'>{ad:.0f}s</div><div class='kpi-sublabel'>Avg Duration</div></div>", unsafe_allow_html=True)

with k5:
    st.markdown(f"<div class='card'><div class='kpi'>{q['artist'].nunique()}</div><div class='kpi-sublabel'>Unique Artists</div></div>", unsafe_allow_html=True)

st.markdown("---")


# ---------------------------
#  CHARTS (COLORFUL PALETTE)
# ---------------------------

left, center, right = st.columns([0.9, 2, 1.1])

# Left summary
with left:
    st.markdown("<div class='card'><h4 style='color:#c3f5ff'>Filter Summary</h4>", unsafe_allow_html=True)
    st.write("Genres:", ", ".join(gen_filter))
    st.write("Artist:", artist_filter)
    st.write(f"Popularity ≥ {min_pop}")
    st.write(f"Duration: {duration[0]} - {duration[1]} sec")
    st.markdown("</div>", unsafe_allow_html=True)

# Center bar + line charts
with center:
    # BAR CHART (COLORFUL)
    cnt = q["genre"].value_counts().reset_index()
    cnt.columns = ["genre", "count"]

    fig = px.bar(
        cnt,
        x="genre",
        y="count",
        text="count",
        template="plotly_white",
        color="genre",
        color_discrete_sequence=PALETTE
    )
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # LINE CHART
    df_temp = q.copy()
    df_temp["tempo_bucket"] = pd.cut(df_temp["tempo"], bins=6)
    line = df_temp.groupby("tempo_bucket")["popularity"].mean().reset_index()
    line["tempo_label"] = line["tempo_bucket"].astype(str)

    fig2 = px.line(
        line,
        x="tempo_label",
        y="popularity",
        markers=True,
        template="plotly_white",
        color_discrete_sequence=["#7c3aed"]
    )
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Right top-10 table
with right:
    top = q.sort_values("popularity", ascending=False).head(10)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Top 10 Tracks")
    st.table(top[["track_id", "title", "artist", "genre", "popularity"]])
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")


# ---------------------------
#   PIE CHARTS + HISTOGRAM
# ---------------------------
d1, d2, d3 = st.columns(3)

with d1:
    pie = q["genre"].value_counts().reset_index()
    pie.columns = ["genre", "count"]
    figp = px.pie(
        pie,
        values="count",
        names="genre",
        hole=0.5,
        color="genre",
        template="plotly_white",
        color_discrete_sequence=PALETTE
    )
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.plotly_chart(figp, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with d2:
    qq = q.copy()
    qq["mood"] = ((qq["valence"] > 0.5) & (qq["energy"] > 0.5)).map(
        {True: "Positive", False: "Calm/Neutral"}
    )
    mood = qq["mood"].value_counts().reset_index()
    mood.columns = ["mood", "count"]
    figm = px.pie(
        mood,
        values="count",
        names="mood",
        hole=0.4,
        template="plotly_white",
        color_discrete_sequence=["#7c3aed", "#00e5ff"]
    )
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.plotly_chart(figm, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with d3:
    figh = px.histogram(
        q,
        x="energy",
        nbins=20,
        template="plotly_white",
        color_discrete_sequence=["#7c3aed"]
    )
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.plotly_chart(figh, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")


# ---------------------------
#   RECOMMENDATIONS
# ---------------------------
if show_recs:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Recommendations (Content-Based)")

    seed_track = st.selectbox("Seed Track", df["track_id"].tolist(), index=0)
    seed = df[df["track_id"] == seed_track].iloc[0]

    def score_row(r):
        s = 0
        s += 2 if r["genre"] == seed["genre"] else 0
        s -= abs(r["popularity"] - seed["popularity"]) / 100
        s -= sum(abs(r[f] - seed[f]) for f in ["danceability", "energy", "acousticness", "valence"])
        return s

    df["score_tmp"] = df.apply(score_row, axis=1)
    recs = df.sort_values("score_tmp", ascending=False).query("track_id != @seed_track").head(12)

    st.dataframe(recs[["track_id", "title", "artist", "genre", "popularity"]])
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='color:#808f9a;font-size:12px'>Charts use white backgrounds for BI-style clarity.</div>", unsafe_allow_html=True)


# ------------------------------
#     ADVANCED FEATURES (TABS)
# ------------------------------
st.sidebar.markdown("## Advanced Features")
tab1, tab2, tab3, tab4 = st.tabs(["Audio Features", "Image Hashing", "Lyrics Analysis", "Clustering"])


# AUDIO FEATURES TAB
with tab1:
    st.header("Audio Feature Explorer")
    if os.path.exists("data/audio_features.csv"):
        st.dataframe(pd.read_csv("data/audio_features.csv"))
    else:
        st.info("Run audio_features.py to generate audio_features.csv")


# IMAGE HASHING TAB
with tab2:
    st.header("Album Artwork Similarity")

    if os.path.exists("data/image_hashes.csv"):
        df_hash = pd.read_csv("data/image_hashes.csv")

        st.subheader("Hash Table")
        st.dataframe(df_hash)

        st.markdown("---")
        st.subheader("Image Preview Grid")

        # GRID
        grid_cols = st.columns(3)
        index = 0
        for _, row in df_hash.iterrows():
            img_path = row["file"]
            if os.path.exists(img_path):
                try:
                    img = Image.open(img_path)
                    with grid_cols[index % 3]:
                        st.image(img, caption=os.path.basename(img_path), use_container_width=True)
                except:
                    pass
                index += 1

        st.markdown("---")
        st.subheader("Similar Cover Viewer")

        # SELECTED IMAGE
        selected = st.selectbox("Select artwork", df_hash["file"].tolist())
        img1 = Image.open(os.path.join("music_app", "assets", selected))
        hash1 = df_hash[df_hash["file"] == selected]["hash"].iloc[0]

        # COMPUTE SIMILARITY
        def dist(h1, h2):
            return imagehash.hex_to_hash(h1) - imagehash.hex_to_hash(h2)

        df_hash["distance"] = df_hash["hash"].apply(lambda h: dist(hash1, h))
        df_sorted = df_hash.sort_values("distance")

        similar_file = df_sorted.iloc[1]["file"]
        img2 = Image.open(similar_file)
        sim_d = df_sorted.iloc[1]["distance"]

        colA, colB = st.columns(2)
        colA.image(img1, caption="Selected", use_container_width=True)
        colB.image(img2, caption=f"Most Similar (distance={sim_d})", use_container_width=True)

    else:
        st.info("Run image_hashing.py to generate image_hashes.csv")


# LYRICS TAB
with tab3:
    st.header("Lyrics Analysis")
    if os.path.exists("data/lyrics_analysis.csv"):
        st.dataframe(pd.read_csv("data/lyrics_analysis.csv"))
    else:
        st.info("Run lyrics_analysis.py to generate lyrics_analysis.csv")


# CLUSTERING TAB
with tab4:
    st.header("Song Clusters (UMAP + KMeans)")
    if os.path.exists("data/clusters.csv"):
        st.dataframe(pd.read_csv("data/clusters.csv"))
    else:
        st.info("Run clustering.py to generate clusters.csv")
