import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "music_dataset_500.csv")

class DesktopApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Music Prediction & Recommendation Desktop App")
        self.geometry("1000x650")
        self.configure(bg="#0b0f17")

        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('TButton', foreground='#e6f7ff', background='#111827')

        self.df = pd.read_csv(DATA_PATH)
        self.create_widgets()

    def create_widgets(self):
        header = tk.Label(self, text="Music Prediction & Recommendation Desktop App", bg="#0b0f17", fg="#00e5ff",
                          font=("Segoe UI", 18, "bold"))
        header.pack(pady=8)

        frame = tk.Frame(self, bg="#0b0f17")
        frame.pack(fill="both", expand=True, padx=12, pady=6)

        left = tk.Frame(frame, bg="#0b0f17")
        left.pack(side="left", fill="y", padx=6)

        tk.Label(left, text="Top Tracks", bg="#0b0f17", fg="#e6f7ff").pack(anchor="w")

        self.listbox = tk.Listbox(
            left, width=40, height=18, bg="#071126", fg="#e6f7ff",
            selectbackground="#084b6e"
        )
        self.listbox.pack(padx=6, pady=6)

        for _, row in self.df.sort_values("popularity", ascending=False).head(50).iterrows():
            self.listbox.insert("end", f"{row['track_id']} - {row['title']} ({row['popularity']})")

        btn_frame = tk.Frame(left, bg="#0b0f17")
        btn_frame.pack(pady=8)

        tk.Button(btn_frame, text="Recommend",
                  command=self.show_recommendations).pack(side="left", padx=4)
        tk.Button(btn_frame, text="Add audio files",
                  command=self.add_audio_files).pack(side="left", padx=4)

        right = tk.Frame(frame, bg="#0b0f17")
        right.pack(side="left", fill="both", expand=True, padx=12)

        # Chart
        fig, ax = plt.subplots(figsize=(6,4))
        genres = self.df["genre"].value_counts().head(10)
        ax.bar(genres.index, genres.values, color="#7c3aed")

        ax.set_title("Genre distribution")
        ax.tick_params(colors="#e6f7ff")
        fig.patch.set_facecolor('#0b0f17')
        ax.set_facecolor('#0b0f17')

        canvas = FigureCanvasTkAgg(fig, master=right)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

    def show_recommendations(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Select track", "Please select a track to get recommendations.")
            return

        track_line = self.listbox.get(sel[0])
        track_id = track_line.split(" - ")[0]
        seed = self.df[self.df["track_id"] == track_id].iloc[0]

        def score_row(r):
            s = 0
            s += 2.0 if r["genre"] == seed["genre"] else 0.0
            s -= abs(r["popularity"] - seed["popularity"]) / 100.0
            s -= sum(abs(r[f] - seed[f])
                     for f in ["danceability", "energy", "acousticness", "valence"])
            return s

        self.df["score_tmp"] = self.df.apply(score_row, axis=1)
        recs = self.df.sort_values("score_tmp", ascending=False).query(
            "track_id != @track_id"
        ).head(6)

        win = tk.Toplevel(self)
        win.title("Recommendations")
        win.geometry("420x300")
        win.configure(bg="#071126")

        tk.Label(win, text=f"Recommended for {seed['title']}",
                 bg="#071126", fg="#e6f7ff",
                 font=("Segoe UI", 12, "bold")).pack(pady=6)

        for _, r in recs.iterrows():
            tk.Label(
                win,
                text=f"{r['track_id']} - {r['title']} ({r['genre']}, pop={r['popularity']})",
                bg="#071126",
                fg="#e6f7ff",
                anchor="w",
                justify="left"
            ).pack(fill="x", padx=10)

    def add_audio_files(self):
        files = filedialog.askopenfilenames(
            title="Select audio files",
            filetypes=[("Audio", "*.mp3 *.wav")]
        )

        if files:
            dest = os.path.join(os.path.dirname(__file__), "..", "data", "audio")
            os.makedirs(dest, exist_ok=True)

            import shutil
            for f in files:
                try:
                    shutil.copy(f, dest)
                except Exception as e:
                    print("copy error:", e)

            messagebox.showinfo("Added", f"Added {len(files)} files to data/audio.")


if __name__ == "__main__":
    app = DesktopApp()
    app.mainloop()