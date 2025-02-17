import random
import matplotlib.pyplot as plt
import requests
import os
from dotenv import load_dotenv
from storage.storage_csv import StorageCsv
from storage.storage_json import StorageJson


load_dotenv()

class MovieApp:
    def __init__(self):
        self.api_key = os.getenv("OMDB_API_KEY")  # Load API key from .env
        if not self.api_key:
            print("API key missing!")
            return
        self._storage = self._get_storage_object()  # Choose the storage system (CSV/JSON)
        self.movies = self._storage.list_movies()

    def _get_storage_object(self):
        """
        Prompts the user to choose between CSV or JSON storage for movie data.
        Returns an instance of the appropriate storage system class.

        Returns:
            StorageCsv or StorageJson: An instance of the chosen storage system.
        """
        choice = input("Choose storage system (1 for CSV, 2 for JSON): ").strip()

        while choice not in ['1', '2']:
            print("Invalid input. Please choose 1 for CSV or 2 for JSON.")
            choice = input("Choose storage system (1 for CSV, 2 for JSON): ").strip()

        # Select the appropriate storage system based on user input
        if choice == "2":
            return StorageJson("/Users/kevinhoffmann/PycharmProjects/movie_app/data/movies.json")
        return StorageCsv("/Users/kevinhoffmann/PycharmProjects/movie_app/data/movies.csv")  # Default is CSV

    def _command_list_movies(self):
        movies = self._storage.list_movies()  # Retrieve movies from the storage
        if not movies:
            print("No movies in the database.")
        else:
            print("Movies in Database:")
            for index, movie_title in enumerate(movies, start=1):
                movie = movies[movie_title]
                print(
                    f"{index}. {movie_title}, Rating: {movie['rating']}, Year: {movie['year']}, Poster URL: {movie['poster_url']}")

    def _command_add_movie(self):
        title = input("Enter the movie title: ")
        if not self.api_key:
            print("Error: OMDB API key is missing!")
            return

        url = f"http://www.omdbapi.com/?apikey={self.api_key}&t={title}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data['Response'] == 'True':
                    movie_title = data['Title']
                    # Check if the movie already exists in the database
                    existing_movies = self._storage.list_movies()
                    if movie_title in existing_movies:
                        print(f"Movie '{movie_title}' already exists in the database.")
                        return  # Exit if the movie is already in the database

                    # Check if the year is a range and extract the first year
                    year_str = data['Year']
                    year = self._extract_year(year_str)
                    rating = float(data['imdbRating']) if data['imdbRating'] != 'N/A' else 0.0
                    poster_url = data['Poster'] if data['Poster'] != 'N/A' else 'No poster available'

                    # Save the movie
                    self._storage.add_movie(movie_title, rating, year, poster_url)
                    print(f"Movie '{movie_title}', released in {year}, with rating {rating} added successfully!")
                else:
                    print(f"Error: {data['Error']}")
            else:
                print("Error: Unable to fetch data from OMDb API.")
        except requests.exceptions.RequestException as e:
            print(f"Error: Unable to connect to OMDb API. {e}")
        except ValueError as e:
            print(f"Error processing data: {e}")

    def _extract_year(self, year_str):
        """Extracts the first year from a year range (e.g. '2006–2013')."""
        if '–' in year_str:
            return int(year_str.split('–')[0])  # If there is a range, take the first year
        return int(year_str)  # Otherwise, take the year as it is

    def _command_delete_movie(self):
        """
        Asks the user for a movie number to delete, confirms, and removes it from the database.
        """
        movies = self._storage.list_movies()

        if not movies:
            print("No movies available to delete.")
            return

        print("Movies in Database:")
        for idx, (title, movie) in enumerate(movies.items(), 1):
            print(
                f"{idx}. {title}, Rating: {movie['rating']}, Year: {movie['year']}, Poster URL: {movie['poster_url']}")

        while True:
            try:
                movie_index = int(input("Which movie do you want to delete? Enter a number: ")) - 1
                if 0 <= movie_index < len(movies):
                    movie_to_delete = list(movies.keys())[movie_index]

                    # Confirmation of deletion
                    confirmation = input(f"Are you sure you want to delete '{movie_to_delete}'? (y/n): ").lower()
                    if confirmation == 'y':
                        self._storage.delete_movie(movie_to_delete)
                        print(f"Movie '{movie_to_delete}' deleted successfully.")
                    else:
                        print(f"Movie '{movie_to_delete}' was not deleted.")
                    break
                else:
                    print(f"Invalid number. Please enter a number between 1 and {len(movies)}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def generate_website(self):
        """Generates an HTML file displaying the movies."""
        try:
            with open("templates/index_template.html", "r", encoding="utf-8") as template_file:
                template = template_file.read()

            movies = self._storage.list_movies()
            if not movies:
                print("No movies to display.")
                return

            movie_items = ""
            for title, movie in movies.items():
                movie_items += f"""
                <li>
                    <div class="movie">
                        <img src="{movie['poster_url']}" alt="{title} poster">
                        <h2>{title} <h2/>
                        <h3> ({movie['year']})</h3>
                        <p>Rating: {movie['rating']}</p>
                    </div>
                </li>
                """

            html_content = template.replace("__TEMPLATE_TITLE__", "My Movie App")
            html_content = html_content.replace("__TEMPLATE_MOVIE_GRID__", movie_items)

            with open("templates/index.html", "w", encoding="utf-8") as output_file:
                output_file.write(html_content)

            print("Website was generated successfully.")

        except FileNotFoundError:
            print("Error: index_template.html not found. Make sure the template file exists.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def _command_movie_stats(self):
        """Displays statistics about movie ratings."""
        movies = self._storage.list_movies()

        if not movies:
            print("No movies in the database to analyze.")
            return

        # Convert all ratings to floats to ensure there are no strings
        ratings = []
        for movie in movies.values():
            try:
                ratings.append(float(movie['rating']))
            except ValueError:
                print(f"Warning: Invalid rating for movie '{movie['title']}', skipping.")
                continue

        if not ratings:  # If there are no valid ratings
            print("No valid ratings to analyze.")
            return

        avg_rating = sum(ratings) / len(ratings)
        sorted_ratings = sorted(ratings)

        # Calculate median
        median_rating = sorted_ratings[len(ratings) // 2] if len(ratings) % 2 == 1 else \
            (sorted_ratings[len(ratings) // 2 - 1] + sorted_ratings[len(ratings) // 2]) / 2

        max_rating = max(ratings)
        min_rating = min(ratings)

        best_movies = [title for title, movie in movies.items() if float(movie['rating']) == max_rating]
        worst_movies = [title for title, movie in movies.items() if float(movie['rating']) == min_rating]

        print("\nStatistics:")
        print(f"Average rating: {avg_rating:.2f}")
        print(f"Median rating: {median_rating:.2f}")
        print(f"Best movie(s): {', '.join(best_movies)} with a rating of {max_rating}")
        print(f"Worst movie(s): {', '.join(worst_movies)} with a rating of {min_rating}")

    def _command_search_movie(self):
        """
        Prompts the user to enter a movie title and searches for it in the database.
        """
        search_title = input("Enter the movie title to search for: ").strip()
        movies = self._storage.list_movies()

        matching_movies = {title: movie for title, movie in movies.items() if search_title.lower() in title.lower()}

        if not matching_movies:
            print(f"No movies found matching '{search_title}'.")
        else:
            print(f"Movies matching '{search_title}':")
            for title, movie in matching_movies.items():
                print(f"{title} - Rating: {movie['rating']}, Year: {movie['year']}")

    def _command_random_movie(self):
        """Displays a random movie from the database."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies available.")
            return
        movie = random.choice(list(movies.items()))
        print(f"Random Movie: {movie[0]} ({movie[1]['year']}) - Rating: {movie[1]['rating']}")

    def _command_sort_movies(self):
        """Sorts movies by rating in either ascending or descending order."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies to sort.")
            return

        sort_order = input("Do you want to sort movies in ascending or descending order? (a/d): ").strip().lower()

        while sort_order not in ['a', 'd']:
            sort_order = input("Invalid input. Please enter 'a' for ascending or 'd' for descending: ").strip().lower()

        sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=(sort_order == 'd'))

        for title, info in sorted_movies:
            print(f"{title} ({info['year']}) - Rating: {info['rating']}")

    def _command_create_histogram(self):
        """Creates a histogram of the movie ratings."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies to create histogram.")
            return

        ratings = [movie['rating'] for movie in movies.values()]

        if not ratings:
            print("No valid ratings to create histogram.")
            return

        plt.hist(ratings, bins=10, edgecolor='black')
        plt.title("Movie Rating Distribution")
        plt.xlabel("Rating")
        plt.ylabel("Frequency")

        save_option = input("Do you want to save the histogram? (y/n): ").strip().lower()
        if save_option == 'y':
            file_path = input("Enter the file path to save the histogram (e.g., 'histogram.png'): ").strip()
            plt.savefig(file_path)
            print(f"Histogram saved to {file_path}.")
        else:
            plt.show()

    def run(self):
        """Starts the movie app and lets the user choose a command."""
        while True:
            print("\nCommands:")
            print("1. List movies")
            print("2. Add movie")
            print("3. Delete movie")
            print("4. Movie stats")
            print("5. Search movie")
            print("6. Random movie")
            print("7. Sort movies")
            print("8. Create histogram")
            print("0. Exit")

            command = input("Enter a command number: ").strip()

            if command == "0":
                print("Exiting the application.")
                break
            elif command == "1":
                self._command_list_movies()
            elif command == "2":
                self._command_add_movie()
            elif command == "3":
                self._command_delete_movie()
            elif command == "4":
                self._command_movie_stats()
            elif command == "5":
                self._command_search_movie()
            elif command == "6":
                self._command_random_movie()
            elif command == "7":
                self._command_sort_movies()
            elif command == "8":
                self._command_create_histogram()
            else:
                print("Invalid command, try again.")

if __name__ == "__main__":
    app = MovieApp()
    app.run()
