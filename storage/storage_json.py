import json
import os
from storage.istorage import IStorage

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
                    return {}  # Gibt ein leeres Dictionary zurück, wenn die JSON-Datei leer oder beschädigt ist
        return {}

    def _save_movies(self, movies):
        """Speichert die Filmdaten in der JSON-Datei."""
        with open(self.file_path, 'w') as file:
            json.dump(movies, file, indent=4)

    def list_movies(self):
            """Returns all movies."""
            movies = self._load_movies()
            return movies  # Entferne die print-Anweisung

    def add_movie(self, title, rating, year, poster_url):
        """Fügt einen neuen Film hinzu."""
        movies = self._load_movies()
        movies[title] = {"year": year, "rating": rating, "poster_url": poster_url}
        self._save_movies(movies)

    def delete_movie(self, movie_title):
        """Löscht einen Film basierend auf dem Titel."""
        movies = self._load_movies()
        if movie_title in movies:
            del movies[movie_title]  # Löscht den Film mit diesem Titel
            self._save_movies(movies)
            print(f"Movie '{movie_title}' has been deleted.")
        else:
            print(f"The movie '{movie_title}' was not found.")

    def update_movie(self, title, rating, poster_url):
        """Aktualisiert die Bewertung und das Poster-URL eines Films."""
        movies = self._load_movies()
        if title in movies:
            movies[title]['rating'] = rating
            movies[title]['poster_url'] = poster_url
            self._save_movies(movies)
