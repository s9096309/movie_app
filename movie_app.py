import random
import matplotlib.pyplot as plt
import requests

from storage.storage_csv import StorageCsv
from storage.storage_json import StorageJson


class MovieApp:
    def __init__(self):
        self._storage = self._get_storage_object()  # Auswahl des Formats passiert hier
        self.movies = self._storage.list_movies()

    def _get_storage_object(self):
        choice = input("Wählen Sie das Speichersystem (1 für CSV, 2 für JSON): ").strip()
        if choice == "2":
            return StorageJson("/Users/kevinhoffmann/PycharmProjects/movie_app/data/movies.json")
        return StorageCsv("/Users/kevinhoffmann/PycharmProjects/movie_app/data/movies.csv")  # Standardmäßig CSV

    def _command_list_movies(self):
        movies = self._storage.list_movies()  # Hole Filme aus dem Speicher
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
        api_key = "1299a8a"
        url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data['Response'] == 'True':
                    movie_title = data['Title']
                    # Überprüfen, ob das Jahr einen Bereich darstellt und das erste Jahr extrahieren
                    year_str = data['Year']
                    year = self._extract_year(year_str)
                    rating = float(data['imdbRating']) if data[
                                                              'imdbRating'] != 'N/A' else 0.0  # Sicherstellen, dass die Bewertung eine Zahl ist
                    poster_url = data['Poster'] if data['Poster'] != 'N/A' else 'No poster available'

                    # Speichern des Films
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
            return int(year_str.split('–')[0])  # Falls es einen Bereich gibt, nimm das erste Jahr
        return int(year_str)  # Ansonsten nimm das Jahr wie es ist

    def _command_delete_movie(self):
        # Vorherige Logik bleibt
        movies = self._storage.list_movies()  # Hole Filme aus dem Speicher
        movie_titles = list(movies.keys())  # Liste der Filmtitel
        if movie_titles:
            print("Movies in Database:")
            for idx, title in enumerate(movie_titles, 1):
                movie = movies[title]
                print(
                    f"{idx}. {title}, Rating: {movie['rating']}, Year: {movie['year']}, Poster URL: {movie['poster_url']}")

            movie_index = int(input("Which movie do you want to delete? Enter a number: ")) - 1
            if 0 <= movie_index < len(movie_titles):
                movie_title = movie_titles[movie_index]
                confirmation = input(f"Are you sure you want to delete '{movie_title}'? (y/n): ")
                if confirmation.lower() == "y":
                    self._storage.delete_movie(movie_title)  # Verwende die delete_movie Methode
                    print(f"'{movie_title}' has been deleted.")
            else:
                print("Invalid movie choice.")
        else:
            print("No movies available to delete.")

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

        # Konvertiere alle Bewertungen in floats, um sicherzustellen, dass keine Strings dabei sind
        ratings = []
        for movie in movies.values():
            try:
                ratings.append(float(movie['rating']))
            except ValueError:
                print(f"Warning: Invalid rating for movie '{movie['title']}', skipping.")
                continue

        if not ratings:  # Wenn keine gültigen Bewertungen vorhanden sind
            print("No valid ratings to analyze.")
            return

        avg_rating = sum(ratings) / len(ratings)
        sorted_ratings = sorted(ratings)

        # Median berechnen
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
        """Searches for movies by title or keyword."""
        search_term = input("Enter the movie title or keyword to search: ").strip().lower()
        movies = self._storage.list_movies()
        found_movies = {title: info for title, info in movies.items() if search_term in title.lower()}
        if found_movies:
            for title, info in found_movies.items():
                print(f"{title} ({info['year']}) - Rating: {info['rating']}")
        else:
            print("No movies found with that title.")

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

    def _command_show_as_histogram(self):
        """Displays movie ratings as a histogram."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies to display.")
            return

        ratings = []
        for title, movie in movies.items():
            if isinstance(movie, dict) and 'rating' in movie and movie['rating'] is not None:
                ratings.append(movie['rating'])

        if ratings:
            plt.hist(ratings, bins=10, edgecolor='black')
            plt.title('Movie Ratings Histogram')
            plt.xlabel('Rating')
            plt.ylabel('Frequency')
            plt.show()
        else:
            print("No valid ratings found to display.")

    def run(self):
        print("Movie App started with:", type(self._storage).__name__)

        while True:
            print("""*** Welcome to My Movies Database ***
       1. List movies
       2. Add movie
       3. Delete movie
       4. Generate Website
       5. Stats
       6. Random movie
       7. Search movie
       8. Sort Movies
       9. Show as histogram
       0. Exit
               """)
            user_input = input("Enter choice (0-9): ")

            while not user_input.isdigit() or not (0 <= int(user_input) <= 9):
                user_input = input("Invalid choice. Please enter a number between 0 and 9: ")

            user_input = int(user_input)

            if user_input == 1:
                self._command_list_movies()
            elif user_input == 2:
                self._command_add_movie()
            elif user_input == 3:
                self._command_delete_movie()  # Aufruf der Methode ohne Argumente
            elif user_input == 4:
                self.generate_website()
            elif user_input == 5:
                self._command_movie_stats()
            elif user_input == 6:
                self._command_random_movie()
            elif user_input == 7:
                self._command_search_movie()
            elif user_input == 8:
                self._command_sort_movies()
            elif user_input == 9:
                self._command_show_as_histogram()
            elif user_input == 0:
                print("Exiting MovieApp.")
                break