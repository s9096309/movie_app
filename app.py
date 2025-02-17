import csv
import json
import os
from dotenv import load_dotenv
from flask import Flask, render_template

app = Flask(__name__)

DATA_SOURCE = os.getenv("MOVIE_DATA_SOURCE", "csv")  # Standard: CSV

CSV_PATH = "data/movies.csv"
JSON_PATH = "data/movies.json"


def load_movies():
    """Loads the movie data either from CSV or JSON."""
    try:
        if DATA_SOURCE == "json":
            with open(JSON_PATH, encoding="utf-8") as jsonfile:
                return json.load(jsonfile)
        else:  # Default: CSV
            with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                return list(reader)
    except FileNotFoundError:
        print(f"⚠ Error: File {CSV_PATH if DATA_SOURCE == 'csv' else JSON_PATH} not found.")
        return []


@app.route('/')
def index():
    title = "My Movie App"
    movie_grid = load_movies()
    return render_template('index_template.html', title=title, movie_grid=movie_grid)



load_dotenv()

app.secret_key = os.getenv("FLASK_SECRET_KEY")
if __name__ == '__main__':
    app.run(debug=True)
