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
        """
        Reads the CSV file and returns a dictionary of movies, including the poster URL.
        """
        movies = {}
        try:
            with open(self.filename, "r", newline="") as file:
                reader = csv.DictReader(file)
                print("CSV Header:", reader.fieldnames)  # Prints the header row
                for row in reader:
                    title = row["title"]
                    # Prevent issues with empty year
                    year = row["year"] if row["year"] else "Unknown"  # Default value for empty year
                    poster_url = row["poster_url"] if row["poster_url"] else "No poster available"  # Default value if no poster
                    movies[title] = {
                        "rating": float(row["rating"]),
                        "year": year,
                        "poster_url": poster_url
                    }
        except Exception as e:
            print("Error reading the CSV file:", e)
        return movies

    def add_movie(self, title, rating, year, poster_url):
        """
        Adds a new movie to the CSV file, including the poster URL.
        """
        with open(self.filename, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([title, rating, year, poster_url])

    def delete_movie(self, title):
        """
        Deletes a movie from the CSV file.
        """
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            with open(self.filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["title", "rating", "year", "poster_url"])  # Write the header again
                for movie, data in movies.items():
                    writer.writerow([movie, data["rating"], data["year"], data["poster_url"]])  # Save data including poster URL
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
