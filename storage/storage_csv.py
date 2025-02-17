import csv
import os
from storage.istorage import IStorage

class StorageCsv(IStorage):

    def __init__(self, filename):
        self.filename = filename
        # Wenn die Datei nicht existiert, wird sie mit einem Header erstellt
        if not os.path.exists(self.filename):
            self._create_file_with_header()

    def _create_file_with_header(self):
        """Erstellt eine neue Datei mit einem Header, falls diese noch nicht existiert."""
        try:
            with open(self.filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["title", "rating", "year", "poster_url"])
        except IOError as e:
            print(f"Error creating file: {e}")

    def _write_to_file(self, movies):
        """Schreibt alle Filme (inkl. Header) zurück in die CSV-Datei."""
        try:
            with open(self.filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["title", "rating", "year", "poster_url"])  # Header
                for movie, data in movies.items():
                    writer.writerow([movie, data["rating"], data["year"], data["poster_url"]])
        except IOError as e:
            print(f"Error writing to file: {e}")

    def list_movies(self):
        """Listet alle Filme aus der CSV-Datei auf."""
        movies = {}
        try:
            with open(self.filename, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    title = row['title']
                    movies[title] = {
                        'rating': row['rating'],
                        'year': row['year'],
                        'poster_url': row['poster_url']
                    }
        except FileNotFoundError:
            print("CSV file not found.")
        except IOError as e:
            print(f"Error reading file: {e}")
        return movies

    def add_movie(self, title, rating, year, poster_url):
        """Fügt einen neuen Film zur CSV-Datei hinzu."""
        try:
            with open(self.filename, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([title, rating, year, poster_url])
        except IOError as e:
            print(f"Error adding movie: {e}")

    def delete_movie(self, title):
        """Löscht einen Film basierend auf dem Titel."""
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            self._write_to_file(movies)
        else:
            print(f"The movie '{title}' was not found.")

    def update_movie(self, title, rating, poster_url):
        """Aktualisiert den Rating und Poster-URL eines Films."""
        movies = self.list_movies()
        if title in movies:
            # Year bleibt unverändert, falls es nicht notwendig ist
            movies[title]["rating"] = rating
            movies[title]["poster_url"] = poster_url
            self._write_to_file(movies)
        else:
            print(f"The movie '{title}' was not found.")
