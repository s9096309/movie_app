import csv
import json
import os
from dotenv import load_dotenv
from flask import Flask, render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


load_dotenv()  # Ensure environment variables are loaded
DATA_SOURCE = os.getenv("MOVIE_DATA_SOURCE", "csv")  # Standard: CSV
print(f"🔍 DATA_SOURCE set to: {DATA_SOURCE}")  # Debugging


CSV_PATH = "data/movies.csv"
JSON_PATH = "data/movies.json"


def load_movies():
    """Loads the movie data either from CSV or JSON."""
    try:
        if DATA_SOURCE == "json":
            with open(JSON_PATH, encoding="utf-8") as jsonfile:
                movies = json.load(jsonfile)
                print("Loaded movies from JSON:", movies)  # Debugging line to check the structure

                if isinstance(movies, dict):  # Ensure it's in the expected format (dict)
                    # Converting the dictionary into a list format for template rendering
                    return [{"title": title, **data} for title, data in movies.items()]
                else:
                    print("Warning: JSON file is not in the expected format.")
                    return []
        else:  # Default: CSV
            with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                return list(reader)
    except FileNotFoundError:
        print(f"⚠ Error: File {CSV_PATH if DATA_SOURCE == 'csv' else JSON_PATH} not found.")
        return []
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading data: {e}.")
        return []


@app.route('/')
def index():
    title = "My Movie App"
    movie_grid = load_movies()
    print("Rendering movie grid:", movie_grid)  # Debugging line to check the data passed to template
    return render_template('index_template.html', title=title, movie_grid=movie_grid)


load_dotenv()

app.secret_key = os.getenv("FLASK_SECRET_KEY")
if __name__ == '__main__':
    app.run(debug=True)
