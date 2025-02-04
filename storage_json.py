# storage_json.py
import json
import os
from istorage import IStorage

class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def _load_movies(self):
        """Lädt die Filmdaten aus der JSON-Datei."""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return {}  # Leeres Dictionary, falls JSON-Datei leer/korrupt ist
        return {}

    def _save_movies(self, movies):
        """Speichert die Filmdaten in der JSON-Datei."""
        with open(self.file_path, 'w') as file:
            json.dump(movies, file, indent=4)

    def list_movies(self):
        """Gibt alle Filme zurück."""
        return self._load_movies()

    def add_movie(self, title, year, rating, poster=None):
        """Fügt einen neuen Film hinzu."""
        movies = self._load_movies()
        movies[title] = {"year": year, "rating": rating, "poster": poster}
        self._save_movies(movies)

    def delete_movie(self, title):
        """Löscht einen Film."""
        movies = self._load_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)

    def update_movie(self, title, rating):
        """Aktualisiert die Bewertung eines Films."""
        movies = self._load_movies()
        if title in movies:
            movies[title]['rating'] = rating
            self._save_movies(movies)
