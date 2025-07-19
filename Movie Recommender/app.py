from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__) 

# Load and clean data
df = pd.read_csv("films.csv", encoding="latin1", engine="python", on_bad_lines="skip")
df.columns = df.columns.str.strip().str.lower()

df = df.rename(columns={
    'title_x': 'title',
    'poster_path': 'poster',
    'story': 'description',
    'imdb_rating': 'rating',
    'release_date': 'release'
})
df = df.fillna("")

# Ensure genres column exists
if 'genres' not in df.columns:
    raise KeyError("'genres' column not found. Please check your CSV file headers.")

df['genres'] = df['genres'].astype(str).apply(lambda x: x.lower())
df['release'] = pd.to_datetime(df['release'], format='%d-%m-%Y', errors='coerce')
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

# Supported genres
supported_genres = ['action', 'drama', 'romance', 'comedy', 'thriller', 'crime', 'biography', 'war', 'horror', 'fantasy']


# --- UTILITY FUNCTIONS ---

def detect_genre(question):
    for genre in supported_genres:
        if genre in question.lower():
            return genre
    return None

def recommend_movies(genre=None, filter_type="popular", count=40):
    filtered = df.copy()

    if genre:
        filtered = filtered[filtered['genres'].str.contains(genre)]

    if filter_type == "top":
        filtered = filtered.sort_values(by="rating", ascending=False)
    elif filter_type == "new":
        filtered = filtered.sort_values(by="release", ascending=False)
    else:  # popular or default
        filtered = filtered.sample(frac=1)

    # Clean for rendering
    recs = []
    for _, row in filtered.head(count).iterrows():
        recs.append({
            "title": row['title'],
            "poster": row['poster'] if row['poster'] else "https://upload.wikimedia.org/wikipedia/commons/c/c2/No_image_poster.png",
            "release": row['release'].strftime("%d %b %Y") if pd.notna(row['release']) else "Unknown",
            "rating": row['rating'] if pd.notna(row['rating']) else "N/A",
            "description": row['description'][:150],
            "genres": row['genres'].title().replace("|", ", ")
        })

    return recs


# --- FLASK ROUTE ---

@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []
    genre_name = ""
    message = ""

    if request.method == "POST":
        question = request.form.get("question", "")
        selected_genre = request.form.get("genre")
        filter_type = request.form.get("filter") or "popular"

        genre = None

        if selected_genre:
            genre = selected_genre.lower()
            genre_name = genre.title()
        elif question:
            genre = detect_genre(question)
            genre_name = genre.title() if genre else ""

        if genre:
            recommendations = recommend_movies(genre, filter_type)
        else:
            message = "No valid genre found. Try typing or selecting one."

    return render_template("index.html", recommendations=recommendations, genre=genre_name, message=message)


if __name__ == "__main__":
    app.run(debug=True)
