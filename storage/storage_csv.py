import csv
import os
from storage.istorage import IStorage


class StorageCsv(IStorage):

    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(self.filename):
            self._create_file_with_header()

    def _create_file_with_header(self):
        """Creates a new CSV file with a header if it does not already exist."""
        try:
            with open(self.filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["title", "rating", "year", "poster_url", "imdbID"])
        except IOError as e:
            print(f"Error creating file: {e}")

    def _write_to_file(self, movies):
        """Writes all movies (including header) back to the CSV file."""
        try:
            with open(self.filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["title", "rating", "year", "poster_url", "imdbID"])
                for movie, data in movies.items():
                    writer.writerow([movie, data["rating"], data["year"], data["poster_url"], data["imdbID"]])
        except IOError as e:
            print(f"Error writing to file: {e}")

    def load_movies(self):
        """Loads all movies from the CSV file and returns them as a dictionary."""
        movies = {}
        try:
            with open(self.filename, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row:  # Ensure the row is not empty
                        title = row.get('title', "UNKNOWN")
                        imdbID = row.get('imdbID', "NO IMDB URL")
                        imdb_url = f"https://www.imdb.com/title/{imdbID}/"
                        movies[title] = {
                            'rating': row.get('rating', "0.0"),
                            'year': row.get('year', "0000"),
                            'poster_url': row.get('poster_url', ""),
                            'imdbID': imdbID
                        }
        except FileNotFoundError:
            print("CSV file not found.")
        except IOError as e:
            print(f"Error reading the file: {e}")

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
        """Adds a new movie to the database if it doesn't already exist."""

        # Check if the movie already exists
        movies = self.load_movies()
        if any(movie['imdbID'] == imdbID or movie_title == title for movie_title, movie in movies.items()):
            return False  # Return False if the movie already exists

        # Add the new movie if no duplicates
        try:
            with open(self.filename, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([title, rating, year, poster_url, imdbID])

            # Confirmation message
            print(f"Movie '{title}' ({year}) with rating {rating} was added successfully.")
            return True
        except IOError as e:
            print(f"Error adding movie: {e}")
            return False  # Return False if there was an error adding the movie

    def delete_movie(self, title):
        """Deletes a movie by its title."""
        movies = self.load_movies()
        if title in movies:
            del movies[title]
            self._write_to_file(movies)
            print(f"Movie '{title}' successfully deleted.")
            return True
        else:
            print(f"Movie '{title}' not found.")
            return False

    def update_movie(self, title, rating, poster_url):
        """Updates the rating and poster URL of a movie."""
        movies = self.load_movies()
        if title in movies:
            movies[title]["rating"] = rating
            movies[title]["poster_url"] = poster_url
            self._write_to_file(movies)
            print(f"Movie '{title}' updated successfully.")
            return True
        else:
            print(f"The movie '{title}' was not found.")
            return False
