from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
df = pd.read_csv("hindi_movies_cleaned.csv", encoding="utf-8", engine="python", on_bad_lines="skip")
df.columns = df.columns.str.strip().str.lower()
print("Columns in CSV:", df.columns.tolist()) 
# Rename for consistency (if needed)
df = df.rename(columns={
    'title_x': 'title',
    'poster_path': 'poster',
    'story': 'description',
    'imdb_rating': 'rating',
    'release_date': 'release'
})
# Fill missing values
df = df.fillna("")

if 'genres' not in df.columns:
    raise KeyError("'genres' column not found. Please check your CSV file header formatting.")

# --- CONTINUE ONLY IF SAFE ---
df['genres'] = df['genres'].astype(str).apply(lambda x: x.lower())

# Supported genres
supported_genres = ['action', 'drama', 'romance', 'comedy', 'thriller', 'crime', 'biography', 'war', 'horror', 'fantasy']

# Genre detection from question
def detect_genre(question):
    for genre in supported_genres:
        if genre in question.lower():
            return genre
    return None

# Get recommendations
def recommend_movies(genre, count=10):
    matching = df[df['genres'].str.contains(genre)]
    return matching.sample(n=min(count, len(matching)))

@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []
    genre_detected = ""
    message = ""

    if request.method == "POST":
        question = request.form.get("question", "")
        genre = detect_genre(question)

        if genre:
            genre_detected = genre.title()
            recs = recommend_movies(genre)
            for _, row in recs.iterrows():
                recommendations.append({
                    "title": row['title'],
                    "poster": row['poster'],
                    "release": row['release'],
                    "rating": row['rating'],
                    "description": row['description'],
                    "genres": row['genres'].title().replace("|", ", ")
                })
        else:
            message = "Could not detect a genre. Try words like 'romance', 'action', or 'comedy'."

    return render_template("index.html", recommendations=recommendations, genre=genre_detected, message=message)

if __name__ == "__main__":
    app.run(debug=True)
