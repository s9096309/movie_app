import random
import matplotlib.pyplot as plt
import requests
import os
from dotenv import load_dotenv
from storage.storage_csv import StorageCsv
from storage.storage_json import StorageJson
from config import load_data_source, save_data_source, BASE_DIR

load_dotenv()

class MovieApp:
    def __init__(self):
        self.api_key = os.getenv("OMDB_API_KEY")  # Load API key from .env
        self.ask_user_for_data_source()
        # If no valid selection was made, ask the user
        if self.data_source not in ['csv', 'json']:
            self.ask_for_data_source()
        if not self.api_key:
            print("API key missing!")
            return
        self._storage = self.get_storage_object()  # Choose the storage system (CSV/JSON)
        self.movies = self._storage.load_movies()

    def ask_user_for_data_source(self):
        """Asks the user for their storage choice and saves it."""
        choice = input("Choose storage system (1 for CSV, 2 for JSON): ").strip()

        while choice not in ['1', '2']:
            print("Invalid input. Please choose 1 for CSV or 2 for JSON.")
            choice = input("Choose storage system (1 for CSV, 2 for JSON): ").strip()

        # Save the chosen data source
        self.data_source = "csv" if choice == "1" else "json"
        save_data_source(self.data_source)  # Save the choice to config.json

        print(f"Data source selected: {'CSV' if self.data_source == 'csv' else 'JSON'}")

    def get_storage_object(self):
        """Returns the appropriate storage object based on the user's choice."""
        if self.data_source == "csv":
            csv_file_path = os.path.join(BASE_DIR, "data", "movies.csv")
            if not os.path.exists(csv_file_path):
                print("CSV file not found. Creating a new file.")
                with open(csv_file_path, 'w') as file:
                    file.write("")  # Create an empty CSV file if it doesn't exist
            return StorageCsv(csv_file_path)
        else:
            json_file_path = os.path.join(BASE_DIR, "data", "movies.json")
            return StorageJson(json_file_path)

    def _command_list_movies(self):
        movies = self._storage.load_movies()  # Retrieve movies from the storage
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
                    # Check if the year is a range and extract the first year
                    year_str = data['Year']
                    year = self._extract_year(year_str)
                    rating = float(data['imdbRating']) if data['imdbRating'] != 'N/A' else 0.0
                    poster_url = data['Poster'] if data['Poster'] != 'N/A' else 'No poster available'
                    imdbID = data['imdbID'] if data['imdbID'] else 'No IMDb ID available'

                    # Save the movie
                    self._storage.add_movie(movie_title, rating, year, poster_url, imdbID)
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
        movies = self._storage.load_movies()

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
                    else:
                        print(f"Movie '{movie_to_delete}' was not deleted.")
                    break
                else:
                    print(f"Invalid number. Please enter a number between 1 and {len(movies)}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def _command_generate_website(self):
        """Generates an HTML file displaying the movies."""
        try:
            with open("templates/index_template.html", encoding="utf-8") as template_file:
                template = template_file.read()

            movies = self._storage.load_movies()
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
        movies = self._storage.load_movies()

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
        movies = self._storage.load_movies()

        matching_movies = {title: movie for title, movie in movies.items() if search_title.lower() in title.lower()}

        if not matching_movies:
            print(f"No movies found matching '{search_title}'.")
        else:
            print(f"Movies matching '{search_title}':")
            for title, movie in matching_movies.items():
                print(f"{title} - Rating: {movie['rating']}, Year: {movie['year']}")

    def _command_random_movie(self):
        """Displays a random movie from the database."""
        movies = self._storage.load_movies()
        if not movies:
            print("No movies available.")
            return
        movie = random.choice(list(movies.items()))
        print(f"Random Movie: {movie[0]} ({movie[1]['year']}) - Rating: {movie[1]['rating']}")

    def _command_sort_movies(self):
        """Sorts movies by rating in either ascending or descending order."""
        movies = self._storage.load_movies()
        if not movies:
            print("No movies to sort.")
            return

        sort_order = input("Do you want to sort movies in ascending or descending order? (a/d): ").strip().lower()

        while sort_order not in ['a', 'd']:
            sort_order = input("Invalid input. Please enter 'a' for ascending or 'd' for descending: ").strip().lower()

        # Convert ratings to float for proper comparison
        sorted_movies = sorted(movies.items(), key=lambda x: float(x[1]['rating']), reverse=(sort_order == 'd'))

        for title, info in sorted_movies:
            print(f"{title} ({info['year']}) - Rating: {info['rating']}")


    def _command_create_histogram(self):
        """Creates and shows a histogram of the movie ratings."""
        movies = self._storage.load_movies()
        if not movies:
            print("No movies to create histogram.")
            return
        ratings = [float(movie['rating']) for movie in movies.values()]

        if not ratings:
            print("No valid ratings to create histogram.")
            return

        # Create and display the histogram
        plt.hist(ratings, bins=10, edgecolor='black')
        plt.title("Movie Rating Distribution")
        plt.xlabel("Rating")
        plt.ylabel("Frequency")
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
            print("8. Generate Website")
            print("9. Create histogram")
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
                self._command_generate_website()
            elif command == "9":
                self._command_create_histogram()
            else:
                print("Invalid command, try again.")


if __name__ == "__main__":
    app = MovieApp()
    app.run()