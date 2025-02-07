import random
import matplotlib.pyplot as plt
import requests


class MovieApp:
    def __init__(self, storage):
        """Initializes the MovieApp with a storage object."""
        self._storage = storage

    def _command_list_movies(self):
        """Lists all movies in the database."""
        movies = self._storage.list_movies()  # This already contains the poster_url
        if not movies:
            print("No movies found.")
        else:
            # Ensure that 'None' is handled correctly for the year
            sorted_movies = sorted(
                movies.items(),
                key=lambda x: (x[1].get('year') if x[1].get('year') is not None else float('inf')),
                reverse=True
            )

            print("Movies in Database:")
            for index, (title, movie) in enumerate(sorted_movies, start=1):
                year_display = movie['year'] if movie['year'] is not None else "Unknown"
                poster_url = movie['poster_url']  # This comes from the list_movies method
                print(f"{index}. {title} ({year_display}) Rating: {movie['rating']:.1f} - Poster URL: {poster_url}")

    def add_movie(self):
        title = input("Enter the movie title: ")
        api_key = "1299a8a"
        url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data['Response'] == 'True':
                    movie_title = data['Title']
                    year = data['Year']
                    rating = data['imdbRating']
                    poster_url = data['Poster'] if data['Poster'] != 'N/A' else 'No poster available'
                    # Save the movie data to storage
                    self._storage.add_movie(movie_title, rating, year, poster_url)
                    print(f"Movie '{movie_title}' added successfully!")
                else:
                    print(f"Error: {data['Error']}")
            else:
                print("Error: Unable to fetch data from OMDb API.")
        except requests.exceptions.RequestException as e:
            print(f"Error: Unable to connect to OMDb API. {e}")

    def _command_delete_movie(self):
        """Deletes a movie from the database."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies to delete.")
            return

        self._command_list_movies()

        try:
            ask_user_index = int(input("Which movie do you want to delete? Enter a number: "))
            ask_user_index -= 1  # Convert to zero-based index

            if not (0 <= ask_user_index < len(movies)):
                print("Invalid input. Please enter a valid number.")
                return

            sorted_movies = sorted(movies.items(),
                                   key=lambda x: (x[1].get('year') if x[1].get('year') is not None else float('inf')),
                                   reverse=True)

            movie_title = sorted_movies[ask_user_index][0]

            confirm = input(f"Are you sure you want to delete '{movie_title}'? (y/n): ").strip().lower()
            if confirm == 'y':
                self._storage.delete_movie(movie_title)
                print(f"'{movie_title}' has been deleted from the list.")
            else:
                print(f"'{movie_title}' was not deleted.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    def _command_update_movie(self):
        """Updates the rating of an existing movie."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies to update.")
            return

        self._command_list_movies()

        try:
            ask_user_index = int(input("Which movie do you want to update? Enter a number: "))
            ask_user_index -= 1  # Convert to zero-based index

            if not (0 <= ask_user_index < len(movies)):
                print("Invalid input. Please enter a valid number.")
                return

            sorted_movies = sorted(movies.items(),
                                   key=lambda x: (x[1].get('year') if x[1].get('year') is not None else float('inf')),
                                   reverse=True)

            movie_title = sorted_movies[ask_user_index][0]

            new_rating = float(input(f"Enter the new rating for '{movie_title}' (1-10): "))
            if 1 <= new_rating <= 10:
                self._storage.update_movie(movie_title, new_rating)
                print(f"Updated '{movie_title}' with new rating: {new_rating}")
            else:
                print("Invalid rating. Please enter a number between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    def _command_movie_stats(self):
        """Displays statistics about movie ratings."""
        movies = self._storage.list_movies()

        if not movies:
            print("No movies in the database to analyze.")
            return

        ratings = [movie['rating'] for movie in movies.values()]
        avg_rating = sum(ratings) / len(ratings)
        sorted_ratings = sorted(ratings)

        median_rating = sorted_ratings[len(ratings) // 2] if len(ratings) % 2 == 1 else \
            (sorted_ratings[len(ratings) // 2 - 1] + sorted_ratings[len(ratings) // 2]) / 2

        max_rating = max(ratings)
        min_rating = min(ratings)

        best_movies = [title for title, movie in movies.items() if movie['rating'] == max_rating]
        worst_movies = [title for title, movie in movies.items() if movie['rating'] == min_rating]

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
        """Runs the MovieApp interface."""
        while True:
            print("""*** Welcome to My Movies Database ***
    1. List movies
    2. Add movie
    3. Delete movie
    4. Update movie
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
                self.add_movie()  # This will only be called when the user selects option 2
            elif user_input == 3:
                self._command_delete_movie()
            elif user_input == 4:
                self._command_update_movie()
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
