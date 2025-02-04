# storage_json.py
import json
import os
from istorage import IStorage

class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def _load_movies(self):
        """Loads movie data from the JSON file."""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return {}  # Returns an empty dictionary if the JSON file is empty or corrupted
        return {}

    def _save_movies(self, movies):
        """Saves movie data to the JSON file."""
        with open(self.file_path, 'w') as file:
            json.dump(movies, file, indent=4)

    def list_movies(self):
        """Returns all movies."""
        return self._load_movies()

    def add_movie(self, title, year, rating):
        """Adds a new movie."""
        movies = self._load_movies()
        movies[title] = {"year": year, "rating": rating}
        self._save_movies(movies)

    def delete_movie(self, title):
        """Deletes a movie."""
        movies = self._load_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)

    def update_movie(self, title, rating):
        """Updates the rating of a movie."""
        movies = self._load_movies()
        if title in movies:
            movies[title]['rating'] = rating
            self._save_movies(movies)
