import csv
import os
from storage.istorage import IStorage

class StorageCsv(IStorage):

    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["title", "rating", "year", "poster_url"])

    def list_movies(self):
        """List all movies from the CSV file."""
        movies = {}
        try:
            with open(self.filename, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    title = row['title']
                    # Hier wird sichergestellt, dass das Ergebnis ein Dictionary ist
                    movies[title] = {
                        'rating': row['rating'],
                        'year': row['year'],
                        'poster_url': row['poster_url']
                    }
        except FileNotFoundError:
            print("CSV file not found.")
        return movies

    def add_movie(self, title, rating, year, poster_url):
        """
        Adds a new movie to the CSV file, including the poster URL.
        """
        with open(self.filename, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([title, rating, year, poster_url])

    def delete_movie(self, title):
        """Löscht einen Film basierend auf dem Titel."""
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            with open(self.filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["title", "rating", "year", "poster_url"])  # Überschreibe die Header-Zeile
                for movie, data in movies.items():
                    writer.writerow([movie, data["rating"], data["year"], data["poster_url"]])  # Speichere alle Daten
        else:
            print(f"The movie '{title}' was not found.")
    def update_movie(self, title, rating, poster_url):
        """
        Updates the rating and poster URL of a movie in the CSV file.
        """
        movies = self.list_movies()
        if title in movies:
            movies[title]["rating"] = rating
            movies[title]["poster_url"] = poster_url  # Update the poster URL as well
            with open(self.filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["title", "rating", "year", "poster_url"])  # Write the header again
                for movie, data in movies.items():
                    writer.writerow([movie, data["rating"], data["year"], data["poster_url"]])  # Save all data, including poster URL
        else:
            print(f"The movie '{title}' was not found.")