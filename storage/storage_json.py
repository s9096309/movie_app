import json
import os
from storage.istorage import IStorage

class StorageJson(IStorage):
    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(self.filename):
            self._save_movies({})  # Initialize with an empty dictionary if the file does not exist

    def _save_movies(self, movies):
        """Saves movie data to the JSON file."""
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(movies, file, indent=4)
        except IOError as e:
            print(f"Error saving to file {self.filename}: {e}")

    def load_movies(self):
        """Loads all movies from the JSON file."""
        movies = {}
        try:
            with open(self.filename, 'r', encoding='utf-8') as jsonfile:
                movies = json.load(jsonfile)
                if not isinstance(movies, dict):  # If the JSON file is not in the expected format
                    print("Warning: JSON file is not in the expected format. Resetting movies list.")
                    movies = {}
        except FileNotFoundError:
            print("JSON file not found. Creating a new movie list.")
            movies = {}  # Initialize with an empty dictionary
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error reading JSON file: {e}. Resetting movies list.")

        return movies

    def list_movies(self):
        """Prints the list of movies when explicitly requested by the user."""
        movies = self.load_movies()
        if movies:
            print("Movies in the database:")
            for index, (title, data) in enumerate(movies.items(), start=1):
                print(
                    f"{index}. {title}, Rating: {data['rating']}, Year: {data['year']}, Poster URL: {data['poster_url']}, IMDb Link: {data['imdbID']}")
        else:
            print("No movies found.")

    def add_movie(self, title, rating, year, poster_url, imdbID):
        """Adds a new movie to the JSON file if it does not already exist."""
        movies = self.load_movies()

        # Check if the movie already exists (by IMDb ID)
        if any(movie.get("imdbID") == imdbID for movie in movies.values()):
            print(f"Movie '{title}' is already in the database.")
            return False  # Return False if the movie is already in the database

        # Add the movie if it does not exist yet
        movies[title] = {
            "year": year,
            "rating": rating,
            "poster_url": poster_url,
            "imdbID": imdbID,
        }
        self._save_movies(movies)
        return True  # Return True after successfully adding the movie

    def delete_movie(self, title):
        """Deletes a movie by its title."""
        movies = self.load_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)
            print(f"Movie '{title}' deleted successfully.")
        else:
            print(f"The movie '{title}' was not found.")

    def update_movie(self, title, rating, poster_url):
        """Updates the rating, poster URL, and IMDb link of a movie."""
        movies = self.load_movies()
        if title in movies:
            movies[title]['rating'] = rating
            movies[title]['poster_url'] = poster_url
            self._save_movies(movies)
            print(f"Movie '{title}' updated successfully.")
        else:
            print(f"The movie '{title}' was not found.")
